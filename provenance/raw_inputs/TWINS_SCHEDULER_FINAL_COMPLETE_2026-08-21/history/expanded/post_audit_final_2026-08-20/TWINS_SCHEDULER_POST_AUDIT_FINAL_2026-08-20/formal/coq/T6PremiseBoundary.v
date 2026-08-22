From Coq Require Import Bool.
Record premises := { S1:bool; S2:bool; Rq:bool; D:bool; T:bool; Ed:bool; X:bool }.
Definition U p e r := andb (orb (negb (S1 p)) e)
  (orb (negb (S2 p)) (andb (orb (negb (Rq p)) e)
    (negb (andb r (andb (D p) (T p)))))).
Definition strict p := andb (X p) (andb (Ed p)
  (andb (U p true false) (andb (negb (U p false false)) (negb (U p true true))))).
Definition closed p := andb (S2 p) (andb (D p) (andb (T p)
  (andb (Ed p) (andb (X p) (orb (S1 p) (Rq p)))))).
Theorem strict_closed : forall p, strict p = closed p.
Proof. intros [s1 s2 rq d t ed x]; destruct s1,s2,rq,d,t,ed,x; reflexivity. Qed.
Definition p0111111 := {|S1:=false;S2:=true;Rq:=true;D:=true;T:=true;Ed:=true;X:=true|}.
Definition p1101111 := {|S1:=true;S2:=true;Rq:=false;D:=true;T:=true;Ed:=true;X:=true|}.
Definition p1111111 := {|S1:=true;S2:=true;Rq:=true;D:=true;T:=true;Ed:=true;X:=true|}.
Theorem strict_three : forall p, strict p = true <-> p=p0111111 \/ p=p1101111 \/ p=p1111111.
Proof. intros [s1 s2 rq d t ed x]; destruct s1,s2,rq,d,t,ed,x; simpl; intuition congruence. Qed.
