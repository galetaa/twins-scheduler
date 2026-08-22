from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import re
from typing import Any


@dataclass(frozen=True, slots=True)
class SourceObligation:
    obligation: str
    relative_path: str
    required_fragments: tuple[str, ...]
    scientific_mapping: str


OBLIGATIONS: tuple[SourceObligation, ...] = (
    SourceObligation(
        obligation="duplicate_vote_is_stuttering",
        relative_path="inputs/cometbft_v0.40.0/vote_set.go",
        required_fragments=(
            "Duplicate votes return added=false, err=nil.",
            "if existing, ok := voteSet.getVote(valIndex, blockKey, &vote.BlockID); ok {",
            "return false, nil // duplicate",
        ),
        scientific_mapping=(
            "Exact replay of the same signed vote does not add a new logical "
            "contribution before quorum accounting."
        ),
    ),
    SourceObligation(
        obligation="voting_power_added_once_per_validator_slot",
        relative_path="inputs/cometbft_v0.40.0/vote_set.go",
        required_fragments=(
            "voteSet.votes[valIndex] = vote",
            "voteSet.sum += votingPower",
        ),
        scientific_mapping=(
            "Quorum contribution is associated with the validator index/voting "
            "power, not the number of identical message instances."
        ),
    ),
    SourceObligation(
        obligation="polka_establishes_persistent_lock",
        relative_path="inputs/cometbft_v0.40.0/state.go",
        required_fragments=(
            "At this point, +2/3 prevoted for a particular block.",
            "cs.LockedRound = round",
            "cs.LockedBlock = cs.ProposalBlock",
        ),
        scientific_mapping=(
            "The abstract POLKA transition establishes the persistent locked round "
            "and value before the validator precommits."
        ),
    ),
    SourceObligation(
        obligation="proposal_carries_valid_round",
        relative_path="inputs/cometbft_v0.40.0/state.go",
        required_fragments=(
            "proposal := types.NewProposal(height, round, cs.ValidRound, propBlockID)",
            "cs.ValidRound = cs.Round",
            "cs.ValidBlock = cs.ProposalBlock",
        ),
        scientific_mapping=(
            "The second kernel's valid-round evidence is an explicit protocol state, "
            "not a scheduler-specific invention."
        ),
    ),
    SourceObligation(
        obligation="official_spec_round_and_lock_vocabulary",
        relative_path="inputs/cometbft_v0.40.0/consensus.md",
        required_fragments=(
            "Propose -> Prevote -> Precommit",
            "If the validator has a PoLC",
            "it (re)locks (or changes lock to)",
        ),
        scientific_mapping=(
            "The bounded stage names and lock transition follow the official "
            "Tendermint/CometBFT consensus specification."
        ),
    ),
)


def _normalize(text: str) -> str:
    """Collapse formatting whitespace while retaining all lexical tokens."""
    return re.sub(r"\s+", " ", text).strip()


def verify_source_mapping(root: Path) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for obligation in OBLIGATIONS:
        path = root / obligation.relative_path
        row = asdict(obligation)
        if not path.exists():
            row.update(
                {
                    "path_exists": False,
                    "missing_fragments": list(obligation.required_fragments),
                    "matching_mode": "whitespace-normalized exact fragment",
                    "status": "FAIL",
                }
            )
            rows.append(row)
            continue

        text = _normalize(path.read_text(encoding="utf-8"))
        missing = [
            fragment
            for fragment in obligation.required_fragments
            if _normalize(fragment) not in text
        ]
        row.update(
            {
                "path_exists": True,
                "missing_fragments": missing,
                "matching_mode": "whitespace-normalized exact fragment",
                "status": "PASS" if not missing else "FAIL",
            }
        )
        rows.append(row)

    return {
        "source": "CometBFT v0.40.0",
        "tag_commit": "0880b4d378f347ab16e54ec677ff50d803f37d62",
        "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
        "obligations": rows,
    }
