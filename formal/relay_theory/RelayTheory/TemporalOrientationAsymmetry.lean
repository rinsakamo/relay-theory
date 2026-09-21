namespace RelayTheory
namespace TemporalOrientationAsymmetry

/-- The asymmetric part of an arbitrary binary relation. -/
def StrictPart {α : Type} (R : α → α → Prop) (x y : α) : Prop :=
  R x y ∧ ¬ R y x

/-- Every admissible edge also admits its reversal. -/
def ReversalClosed {α : Type} (Adm : α → α → Prop) : Prop :=
  ∀ ⦃x y : α⦄, Adm x y → Adm y x

/-- Every nontrivial admissible edge follows one strict orientation of R. -/
def StrictlyOrientedBy {α : Type}
    (Adm R : α → α → Prop) : Prop :=
  ∀ ⦃x y : α⦄, Adm x y → x ≠ y → StrictPart R x y

/-- The admissibility surface contains at least one nontrivial edge. -/
def NontrivialAdmissibility {α : Type}
    (Adm : α → α → Prop) : Prop :=
  ∃ x y, Adm x y ∧ x ≠ y

/--
A reversal-closed admissibility surface cannot have every nontrivial admissible
edge lie in one strict orientation of any relation R.
-/
theorem reversalClosed_no_nontrivial_strict_orientation
    {α : Type} {Adm R : α → α → Prop}
    (hrev : ReversalClosed Adm)
    (horient : StrictlyOrientedBy Adm R) :
    ¬ NontrivialAdmissibility Adm := by
  intro hnontrivial
  rcases hnontrivial with ⟨x, y, hxy, hne⟩
  have hforward : StrictPart R x y := horient hxy hne
  have hyx : Adm y x := hrev hxy
  have hbackward : StrictPart R y x :=
    horient hyx (fun h => hne h.symm)
  exact hforward.2 hbackward.1

/-- Diagonal edges plus both directions between distinguished points. -/
def TwoWayPairAdm {α : Type} (a b : α) (x y : α) : Prop :=
  x = y ∨ (x = a ∧ y = b) ∨ (x = b ∧ y = a)

theorem twoWayPair_reversalClosed {α : Type} (a b : α) :
    ReversalClosed (TwoWayPairAdm a b) := by
  intro x y hxy
  rcases hxy with hdiag | hab | hba
  · exact Or.inl hdiag.symm
  · exact Or.inr (Or.inr ⟨hab.2, hab.1⟩)
  · exact Or.inr (Or.inl ⟨hba.2, hba.1⟩)

theorem twoWayPair_nontrivial
    {α : Type} {a b : α} (hne : a ≠ b) :
    NontrivialAdmissibility (TwoWayPairAdm a b) := by
  exact ⟨a, b, Or.inr (Or.inl ⟨rfl, rfl⟩), hne⟩

/--
A genuine two-way pair cannot be globally strictly oriented by any proposed R.
-/
theorem twoWayPair_not_strictlyOriented
    {α : Type} {a b : α} (hne : a ≠ b) (R : α → α → Prop) :
    ¬ StrictlyOrientedBy (TwoWayPairAdm a b) R := by
  intro horient
  exact reversalClosed_no_nontrivial_strict_orientation
    (twoWayPair_reversalClosed a b)
    horient
    (twoWayPair_nontrivial hne)

/-- Diagonal edges plus one distinguished direction. -/
def OneWayPairAdm {α : Type} (a b : α) (x y : α) : Prop :=
  x = y ∨ (x = a ∧ y = b)

theorem oneWayPair_strictlyOriented
    {α : Type} {a b : α} {R : α → α → Prop}
    (hstrict : StrictPart R a b) :
    StrictlyOrientedBy (OneWayPairAdm a b) R := by
  intro x y hxy hne
  rcases hxy with hdiag | hab
  · exact False.elim (hne hdiag)
  · rcases hab with ⟨rfl, rfl⟩
    exact hstrict

theorem oneWayPair_not_reversalClosed
    {α : Type} {a b : α} (hne : a ≠ b) :
    ¬ ReversalClosed (OneWayPairAdm a b) := by
  intro hrev
  have hforward : OneWayPairAdm a b a b := Or.inr ⟨rfl, rfl⟩
  have hback : OneWayPairAdm a b b a := hrev hforward
  rcases hback with hdiag | hba
  · exact hne hdiag.symm
  · exact hne hba.1.symm

/-- Explicit two-point relation containing only false -> true. -/
def BoolForward (x y : Bool) : Prop :=
  x = false ∧ y = true

theorem boolForward_strict :
    StrictPart BoolForward false true := by
  constructor
  · exact ⟨rfl, rfl⟩
  · intro h
    exact Bool.noConfusion h.1

/-- Positive control: once the admissibility surface is one-way, orientation works. -/
theorem bool_oneWay_oriented :
    StrictlyOrientedBy
      (OneWayPairAdm false true)
      BoolForward := by
  exact oneWayPair_strictlyOriented boolForward_strict

/-- The positive control explicitly breaks reversal closure. -/
theorem bool_oneWay_breaks_reversal :
    ¬ ReversalClosed (OneWayPairAdm false true) := by
  exact oneWayPair_not_reversalClosed (by decide)

/-- Negative control: the two-way fixture is reversal-closed and nontrivial. -/
theorem bool_twoWay_obstruction :
    ReversalClosed (TwoWayPairAdm false true) ∧
    NontrivialAdmissibility (TwoWayPairAdm false true) ∧
    ∀ R : Bool → Bool → Prop,
      ¬ StrictlyOrientedBy (TwoWayPairAdm false true) R := by
  refine ⟨twoWayPair_reversalClosed false true, ?_, ?_⟩
  · exact twoWayPair_nontrivial (by decide)
  · intro R
    exact twoWayPair_not_strictlyOriented (by decide) R

/--
Scoped acceptance bundle: reversal closure blocks strict orientation in the
negative control, while a one-way asymmetry permits it in the positive control.
-/
theorem temporal_orientation_asymmetry_bundle :
    (∀ R : Bool → Bool → Prop,
      ¬ StrictlyOrientedBy (TwoWayPairAdm false true) R) ∧
    StrictlyOrientedBy (OneWayPairAdm false true) BoolForward ∧
    ¬ ReversalClosed (OneWayPairAdm false true) := by
  exact ⟨bool_twoWay_obstruction.2.2,
    bool_oneWay_oriented,
    bool_oneWay_breaks_reversal⟩

end TemporalOrientationAsymmetry
end RelayTheory
