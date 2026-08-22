From Coq Require Import List Bool.
Import ListNotations.
Set Implicit Arguments.

Section ReplayErasure.
Context {State Event Rel : Type}.
Variable step : State -> Event -> State.
Variable project : State -> Rel.
Variable duplicate : Event -> bool.

Fixpoint run (s : State) (tr : list Event) : State :=
  match tr with
  | [] => s
  | e :: rest => run (step s e) rest
  end.

Fixpoint erase_marked (tr : list Event) : list Event :=
  match tr with
  | [] => []
  | e :: rest => if duplicate e then erase_marked rest else e :: erase_marked rest
  end.

Hypothesis projection_congruence :
  forall s t e, project s = project t -> project (step s e) = project (step t e).
Hypothesis duplicate_stutter :
  forall s e, duplicate e = true -> project (step s e) = project s.

Lemma replay_erasure_aux : forall tr left right,
  project left = project right ->
  project (run left (erase_marked tr)) = project (run right tr).
Proof.
  induction tr as [|e rest IH]; intros left right Hrel; simpl.
  - exact Hrel.
  - destruct (duplicate e) eqn:Hdup.
    + apply IH. rewrite (duplicate_stutter right e Hdup). exact Hrel.
    + apply IH. now apply projection_congruence.
Qed.

Theorem replay_erasure : forall s tr,
  project (run s (erase_marked tr)) = project (run s tr).
Proof. intros; apply replay_erasure_aux; reflexivity. Qed.
End ReplayErasure.

Inductive counter_event := X | Y.
Record counter_state := { relevant : bool; hidden : bool }.
Definition counter_step (s : counter_state) (e : counter_event) : counter_state :=
  match e with
  | X => {| relevant := relevant s; hidden := negb (hidden s) |}
  | Y => {| relevant := hidden s; hidden := hidden s |}
  end.
Definition counter_initial := {| relevant := false; hidden := true |}.
Example hidden_state_counterexample :
  relevant (run counter_step counter_initial [X;X;Y]) = true /\
  relevant (run counter_step counter_initial [X;Y]) = false.
Proof. reflexivity. Qed.
