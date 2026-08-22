From Coq Require Import List.
Import ListNotations.
Set Implicit Arguments.

Section ClosureLifting.
Context {State Original Inserted : Type}.
Inductive merged := retained : Original -> merged | inserted : Inserted -> merged.
Variable step : State -> Original -> State.
Variable add : State -> Inserted -> State.

Fixpoint project_original (tr : list merged) : list Original :=
  match tr with
  | [] => []
  | retained a :: rest => a :: project_original rest
  | inserted _ :: rest => project_original rest
  end.
Fixpoint run_original (s : State) (tr : list Original) : State :=
  match tr with [] => s | a::rest => run_original (step s a) rest end.
Fixpoint run_merged (s : State) (tr : list merged) : State :=
  match tr with
  | [] => s
  | retained a::rest => run_merged (step s a) rest
  | inserted a::rest => run_merged (add s a) rest
  end.

Variable R : State -> State -> Prop.
Hypothesis R_trans : forall a b c, R a b -> R b c -> R a c.
Hypothesis increasing : forall s a, R s (add s a).
Hypothesis forward : forall a s t, R s t -> R (step s a) (step t a).

Lemma closure_lifting_aux : forall tr s t,
  R s t -> R (run_original s (project_original tr)) (run_merged t tr).
Proof.
  induction tr as [|h rest IH]; intros s t H; simpl; auto.
  destruct h.
  - apply IH. now apply forward.
  - apply IH. eapply R_trans; eauto using increasing.
Qed.

Variable Unsafe : State -> Prop.
Hypothesis initial : forall s, R s s.
Hypothesis upward : forall s t, R s t -> Unsafe s -> Unsafe t.
Theorem closure_preserves_unsafe : forall s tr,
  Unsafe (run_original s (project_original tr)) -> Unsafe (run_merged s tr).
Proof.
  intros s tr HU. eapply upward; eauto. apply closure_lifting_aux. apply initial.
Qed.
End ClosureLifting.
