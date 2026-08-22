From Coq Require Import Bool Arith Lia.

Inductive value := zero | one.
Record state := {
  enabled : bool; disabled : bool; cert0 : bool; cert1 : bool;
  left_decision : option value; right_decision : option value
}.
Definition init := {| enabled:=false; disabled:=false; cert0:=false; cert1:=false;
  left_decision:=None; right_decision:=None |}.
Inductive policy := phase_specific | directed (edge:bool).
Definition deliverE p := match p with phase_specific=>true | directed e=>e end.
Definition deliverR p := match p with phase_specific=>false | directed e=>e end.
Definition exec (p:policy) : state :=
  let s1 := if deliverE p then {| enabled:=true; disabled:=false; cert0:=false; cert1:=false; left_decision:=None; right_decision:=None |} else init in
  let s2 := if enabled s1 then {| enabled:=enabled s1; disabled:=disabled s1; cert0:=true; cert1:=cert1 s1; left_decision:=Some zero; right_decision:=right_decision s1 |} else s1 in
  let s3 := if deliverR p then {| enabled:=enabled s2; disabled:=true; cert0:=cert0 s2; cert1:=cert1 s2; left_decision:=left_decision s2; right_decision:=right_decision s2 |} else s2 in
  if andb (enabled s3) (negb (disabled s3)) then
    {| enabled:=enabled s3; disabled:=disabled s3; cert0:=cert0 s3; cert1:=true; left_decision:=left_decision s3; right_decision:=Some one |}
  else s3.
Definition unsafe (s:state) : Prop := left_decision s = Some zero /\ right_decision s = Some one.
Theorem phase_specific_unsafe : unsafe (exec phase_specific).
Proof. split; reflexivity. Qed.
Theorem directed_safe : forall e, ~ unsafe (exec (directed e)).
Proof. destruct e; simpl; intros [H _]; discriminate. Qed.
Definition quorum (f:nat) := 2*f+1.
Definition base (f:nat) := 2*f.
Theorem quorum_pivot : forall f, 1 <= f ->
  base f + 1 = quorum f /\ base f < quorum f /\
  unsafe (exec phase_specific) /\ forall e, ~unsafe (exec (directed e)).
Proof. intros; unfold base, quorum; repeat split; try lia; auto using phase_specific_unsafe, directed_safe. Qed.
