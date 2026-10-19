from dataclasses import replace

import pytest

from twins_scheduler.concrete_trace import (
    ConcreteTrace,
    GRAMMARS,
    IllegalAction,
    evaluate_suite,
    run_trace,
)


def _milestone(loop: ConcreteTrace, name: str) -> dict:
    return next(row for row in loop.milestones if row["name"] == name)


def _signed(loop: ConcreteTrace, name: str, round_: int, kind: str):
    return [message for message in loop.messages.values()
            if (message.signer, message.round, message.kind) == (name, round_, kind)]


def test_six_canonical_cases_four_timing_controls_and_two_fifo_relay_controls() -> None:
    suite = evaluate_suite()
    assert suite["status"] == "PASS"
    assert len(suite["cases"]) == 12
    assert all(suite["checks"].values())
    expected = {
        ("G_T_PHASE_SPECIFIC", "BASELINE"): {"A": 0},
        ("G_D_EDGE_OFF", "BASELINE"): {"P": 1, "C": 1},
        ("G_D_EDGE_ON", "BASELINE"): {"A": 0, "P": 0},
        ("G_T_PHASE_SPECIFIC", "MISSING_LOCK_UPDATE"): {"A": 0, "P": 1, "C": 1},
        ("G_D_EDGE_OFF", "MISSING_LOCK_UPDATE"): {"P": 1, "C": 1},
        ("G_D_EDGE_ON", "MISSING_LOCK_UPDATE"): {"A": 0, "P": 0},
    }
    for case in suite["cases"]:
        assert all(case["audit"].values())
        if case["repair_timing"] == "before_round_1":
            assert case["decisions"] == expected[(case["grammar"], case["variant"])]


def test_conflicting_certificates_are_sets_of_emitted_signed_votes() -> None:
    loop = run_trace("G_T_PHASE_SPECIFIC", "MISSING_LOCK_UPDATE")
    for receiver, round_, value, signers in (("A", 0, 0, ["A", "B", "P"]),
                                            ("C", 1, 1, ["B", "C", "P"])):
        certificate = next(row for row in loop.certificates
                           if (row["receiver"], row["round"], row["kind"], row["value"])
                           == (receiver, round_, "PRECOMMIT", value))
        assert certificate["signers"] == signers
        for key in certificate["vote_ids"]:
            message = loop.messages[key]
            assert loop._authenticate(message)
            assert (message.kind, message.round, message.value) == ("PRECOMMIT", round_, value)
            assert any(row["action"] == "ACCEPT_VOTE" and row["actor"] == receiver
                       and row["message"] == key and row["index"] < certificate["formed_at"]
                       for row in loop.log)
    assert not any(message.kind in ("POLKA", "COMMIT") for message in loop.messages.values())


def test_c_nil_vote_and_both_round_advances_have_legal_mixed_quorums() -> None:
    loop = run_trace("G_T_PHASE_SPECIFIC", "MISSING_LOCK_UPDATE")
    assert _signed(loop, "C", 0, "PREVOTE")[0].value is None
    assert _signed(loop, "C", 0, "PRECOMMIT")[0].value is None
    assert any(row["action"] == "TIMEOUT" and row["actor"] == "C"
               and row["timer"] == "PREVOTE" for row in loop.log)
    advances = [row for row in loop.log if row["action"] == "ROUND_ADVANCE"]
    assert {row["actor"] for row in advances} == {"P", "C"}
    for row in advances:
        evidence = [loop.messages[key] for key in row["evidence"]]
        assert {(vote.signer, vote.value) for vote in evidence} == {("A", 0), ("P", 0), ("C", None)}
    c = _milestone(loop, "round_1_entry")["states"]["C"]
    assert (c["valid_value"], c["valid_round"]) == (None, -1)


def test_missing_lock_mutation_keeps_p_valid_block_and_other_validators_lock() -> None:
    mutant = run_trace("G_T_PHASE_SPECIFIC", "MISSING_LOCK_UPDATE")
    baseline = run_trace("G_T_PHASE_SPECIFIC", "BASELINE")
    p = _milestone(mutant, "after_enabling_opportunity")["states"]["P"]
    assert (p["locked_value"], p["locked_round"]) == (None, -1)
    assert (p["valid_value"], p["valid_round"]) == (0, 0)
    baseline_p = _milestone(baseline, "after_enabling_opportunity")["states"]["P"]
    assert (baseline_p["locked_value"], baseline_p["locked_round"]) == (0, 0)
    round1_p = _milestone(mutant, "after_pivot_precommit_opportunity")["states"]["P"]
    assert (round1_p["locked_value"], round1_p["locked_round"]) == (1, 1)
    assert (round1_p["valid_value"], round1_p["valid_round"]) == (1, 1)
    for name in ("A", "C"):
        nonnil_precommits = [row for row in mutant.log if row["action"] == "SIGN"
                             and row["actor"] == name
                             and mutant.messages[row["message"]].kind == "PRECOMMIT"
                             and mutant.messages[row["message"]].value is not None]
        assert nonnil_precommits
        for row in nonnil_precommits:
            vote = mutant.messages[row["message"]]
            assert (row["states"][name]["locked_value"], row["states"][name]["locked_round"]) == (
                vote.value, vote.round
            )


def test_a_pivot_proposer_would_reuse_valid_block_zero() -> None:
    loop = run_trace("G_T_PHASE_SPECIFIC", "MISSING_LOCK_UPDATE",
                     stop_after_round_0=True, proposers=("B", "P"))
    assert loop.replicas["P"].round == 1
    proposal_id = loop.propose("P", 1, ("P",))
    proposal = loop.messages[proposal_id]
    assert (proposal.value, proposal.valid_round) == (0, 0)
    assert _signed(loop, "P", 1, "PREVOTE")[0].value == 0


def test_proposal_relay_preserves_signature_and_controlled_edge_contains_only_e_r() -> None:
    for grammar in GRAMMARS:
        loop = run_trace(grammar, "MISSING_LOCK_UPDATE")
        controlled = [envelope for envelope in loop.envelopes.values()
                      if (envelope.sender, envelope.receiver) == ("B", "P")
                      and loop.messages[envelope.message_id].round == 0]
        assert {loop.messages[envelope.message_id].kind for envelope in controlled} == {
            "PREVOTE", "PRECOMMIT"
        }
        relay = next(envelope for envelope in loop.envelopes.values()
                     if (envelope.sender, envelope.receiver) == ("A", "P")
                     and loop.messages[envelope.message_id].kind == "PROPOSAL")
        assert relay.status == "DELIVERED"
        assert loop.messages[relay.message_id].signer == "B"


def test_repair_after_prevote_prevents_precommit_even_though_c_can_lock_one() -> None:
    loop = run_trace("G_D_EDGE_ON", "MISSING_LOCK_UPDATE", repair_timing="after_pivot_prevote")
    assert not loop.result()["unsafe"]
    assert loop.result()["decisions"] == {"A": 0, "P": 0}
    assert _signed(loop, "P", 1, "PREVOTE")[0].value == 1
    assert not _signed(loop, "P", 1, "PRECOMMIT")
    assert _signed(loop, "C", 1, "PRECOMMIT")[0].value == 1


def test_repair_after_signed_precommit_cannot_retract_the_buffered_vote() -> None:
    loop = run_trace("G_D_EDGE_ON", "MISSING_LOCK_UPDATE", repair_timing="after_pivot_precommit")
    assert loop.result()["decisions"] == {"A": 0, "P": 0, "C": 1}
    pivot_vote = _signed(loop, "P", 1, "PRECOMMIT")[0]
    signed_at = next(row["index"] for row in loop.log
                     if row["action"] == "SIGN" and row["message"] == pivot_vote.id)
    repair_at = next(row["index"] for row in loop.log if row["action"] == "DELIVER"
                     and row["receiver"] == "P"
                     and (loop.messages[row["message"]].signer,
                          loop.messages[row["message"]].round,
                          loop.messages[row["message"]].kind) == ("B", 0, "PRECOMMIT"))
    p_decides_at = next(row["index"] for row in loop.log if row["action"] == "DECIDE" and row["actor"] == "P")
    vote_arrives_at = next(row["index"] for row in loop.log if row["action"] == "DELIVER"
                          and row["receiver"] == "C" and row["message"] == pivot_vote.id)
    c_decides_at = next(row["index"] for row in loop.log if row["action"] == "DECIDE" and row["actor"] == "C")
    assert signed_at < repair_at < p_decides_at < vote_arrives_at < c_decides_at
    assert any(row["action"] == "WAIT_COMMIT_BLOCK" and row["actor"] == "P" for row in loop.log)
    assert any(row["action"] == "BLOCK_SEND" and row["actor"] == "A" for row in loop.log)


def test_illegal_timeout_precommit_and_unemitted_delivery_are_rejected() -> None:
    loop = ConcreteTrace()
    with pytest.raises(IllegalAction, match="never emitted"):
        loop.deliver("invented-certificate")
    with pytest.raises(IllegalAction, match="not armed"):
        loop.timeout("P", "PRECOMMIT")
    with pytest.raises(IllegalAction, match="requires a PoLC"):
        loop._enter_precommit("P")
    with pytest.raises(IllegalAction, match="designated proposer"):
        loop.propose("P", 0, ("P",))


def test_authentication_failure_is_rejected_before_delivery() -> None:
    loop = ConcreteTrace()
    key = loop.byzantine_vote(0, "PREVOTE", 0)
    envelope = loop.vote_envelope("B", "P", 0, "PREVOTE")
    assert envelope is not None
    loop.messages[key] = replace(loop.messages[key], value=1)
    with pytest.raises(IllegalAction, match="authentication"):
        loop.deliver(envelope)
    assert loop.envelopes[envelope].status == "BUFFERED"


def test_replayed_signed_vote_is_not_a_second_sender_contribution() -> None:
    loop = ConcreteTrace()
    key = loop.byzantine_vote(0, "PREVOTE", 0)
    loop.deliver_vote("B", "A", 0, "PREVOTE")
    loop.deliver(loop.relay("B", "A", key))
    assert len(loop._votes("A", 0, "PREVOTE")) == 1
    assert not loop.certificates
    assert any(row["action"] == "DUPLICATE_VOTE" for row in loop.log)
    with pytest.raises(IllegalAction, match="does not possess"):
        loop.relay("C", "P", key)


def test_envelope_cannot_be_delivered_twice_and_correct_validator_cannot_double_sign() -> None:
    loop = ConcreteTrace()
    loop.byzantine_vote(0, "PREVOTE", 0)
    key = loop.vote_envelope("B", "A", 0, "PREVOTE")
    assert key is not None
    loop.deliver(key)
    with pytest.raises(IllegalAction, match="only once"):
        loop.deliver(key)
    loop.timeout("C", "PROPOSE")
    with pytest.raises(IllegalAction, match="second vote"):
        loop._sign_correct_vote("C", "PREVOTE", 1, "invalid test action")


def test_audit_detects_certificate_claimed_before_its_votes_arrived() -> None:
    loop = run_trace("G_T_PHASE_SPECIFIC", "MISSING_LOCK_UPDATE")
    assert all(loop.audit().values())
    loop.certificates[0]["formed_at"] = 0
    assert not loop.audit()["certificate_votes_received_before_certificate_formation"]


def test_fifo_relay_control_preserves_signature_and_still_exposes_the_conflict() -> None:
    direct = run_trace("G_D_EDGE_ON", "MISSING_LOCK_UPDATE", repair_timing="after_pivot_precommit")
    relay = run_trace("G_D_EDGE_ON", "MISSING_LOCK_UPDATE", repair_timing="after_pivot_precommit",
                      round1_b_prevote_route="via_C")
    assert not direct.vote_channel_order()["admitted_vote_envelopes_fifo"]
    assert relay.vote_channel_order()["admitted_vote_envelopes_fifo"]
    assert relay.result()["decisions"] == {"A": 0, "P": 0, "C": 1}
    forwarded = next(envelope for envelope in relay.envelopes.values()
                     if (envelope.sender, envelope.receiver) == ("C", "P")
                     and (relay.messages[envelope.message_id].signer,
                          relay.messages[envelope.message_id].round,
                          relay.messages[envelope.message_id].kind) == ("B", 1, "PREVOTE"))
    assert forwarded.status == "DELIVERED"
    assert relay._authenticate(relay.messages[forwarded.message_id])
    assert any(certificate["receiver"] == "P" and certificate["round"] == 1
               and certificate["kind"] == "PREVOTE" and certificate["signers"] == ["B", "C", "P"]
               for certificate in relay.certificates)
