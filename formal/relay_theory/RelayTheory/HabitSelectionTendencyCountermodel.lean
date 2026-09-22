namespace RelayTheory

namespace HabitSelectionTendencyCountermodel

abbrev Bit := Bool
abbrev Context := Bit
abbrev Response := Bit
abbrev Weight := Nat
abbrev SelectionWeight := Context → Response → Weight
abbrev SuccessCriterion := Context → Response → Prop

def identitySuccess : SuccessCriterion :=
  fun c r => r = c

/--
A response is operationally available when it has positive declared selection
weight. Capability asks only whether at least one task-successful response is
available in every context. It does not ask which response dominates.
-/
def Capable
    (success : SuccessCriterion)
    (weights : SelectionWeight) : Prop :=
  ∀ c : Context, ∃ r : Response, 0 < weights c r ∧ success c r

/--
A narrow default-tendency judgment: response `false` has greater declared
selection weight than response `true` in every context.
-/
def FalseDominant (weights : SelectionWeight) : Prop :=
  ∀ c : Context, weights c false > weights c true

def falseBiasedCapable : SelectionWeight :=
  fun _ r => if r then 1 else 2

def trueBiasedCapable : SelectionWeight :=
  fun _ r => if r then 2 else 1

def falseOnly : SelectionWeight :=
  fun _ r => if r then 0 else 2

def trueOnly : SelectionWeight :=
  fun _ r => if r then 2 else 0

theorem falseBiasedCapable_capable :
    Capable identitySuccess falseBiasedCapable := by
  intro c
  refine ⟨c, ?_, rfl⟩
  cases c <;> simp [falseBiasedCapable]

theorem trueBiasedCapable_capable :
    Capable identitySuccess trueBiasedCapable := by
  intro c
  refine ⟨c, ?_, rfl⟩
  cases c <;> simp [trueBiasedCapable]

theorem falseOnly_not_capable :
    ¬ Capable identitySuccess falseOnly := by
  intro h
  rcases h true with ⟨r, hpos, hsuccess⟩
  change r = true at hsuccess
  subst r
  simp [falseOnly] at hpos

theorem trueOnly_not_capable :
    ¬ Capable identitySuccess trueOnly := by
  intro h
  rcases h false with ⟨r, hpos, hsuccess⟩
  change r = false at hsuccess
  subst r
  simp [trueOnly] at hpos

theorem falseBiasedCapable_falseDominant :
    FalseDominant falseBiasedCapable := by
  intro c
  simp [falseBiasedCapable]

theorem falseOnly_falseDominant :
    FalseDominant falseOnly := by
  intro c
  simp [falseOnly]

theorem trueBiasedCapable_not_falseDominant :
    ¬ FalseDominant trueBiasedCapable := by
  intro h
  have bad := h false
  simp [trueBiasedCapable] at bad

theorem trueOnly_not_falseDominant :
    ¬ FalseDominant trueOnly := by
  intro h
  have bad := h false
  simp [trueOnly] at bad

theorem allFour_capabilityTendencyQuadrants :
    (Capable identitySuccess falseBiasedCapable ∧
      FalseDominant falseBiasedCapable) ∧
    (Capable identitySuccess trueBiasedCapable ∧
      ¬ FalseDominant trueBiasedCapable) ∧
    (¬ Capable identitySuccess falseOnly ∧
      FalseDominant falseOnly) ∧
    (¬ Capable identitySuccess trueOnly ∧
      ¬ FalseDominant trueOnly) := by
  exact ⟨
    ⟨falseBiasedCapable_capable, falseBiasedCapable_falseDominant⟩,
    ⟨trueBiasedCapable_capable, trueBiasedCapable_not_falseDominant⟩,
    ⟨falseOnly_not_capable, falseOnly_falseDominant⟩,
    ⟨trueOnly_not_capable, trueOnly_not_falseDominant⟩
  ⟩

theorem capability_doesNotDetermineDefaultTendency :
    Capable identitySuccess falseBiasedCapable ∧
    Capable identitySuccess trueBiasedCapable ∧
    FalseDominant falseBiasedCapable ∧
    ¬ FalseDominant trueBiasedCapable := by
  exact ⟨
    falseBiasedCapable_capable,
    trueBiasedCapable_capable,
    falseBiasedCapable_falseDominant,
    trueBiasedCapable_not_falseDominant
  ⟩

theorem defaultTendency_doesNotDetermineCapability :
    FalseDominant falseBiasedCapable ∧
    FalseDominant falseOnly ∧
    Capable identitySuccess falseBiasedCapable ∧
    ¬ Capable identitySuccess falseOnly := by
  exact ⟨
    falseBiasedCapable_falseDominant,
    falseOnly_falseDominant,
    falseBiasedCapable_capable,
    falseOnly_not_capable
  ⟩

theorem extensionalWeightsPreserveFalseDominant
    (f g : SelectionWeight)
    (hEq : ∀ c : Context, ∀ r : Response, f c r = g c r) :
    FalseDominant f ↔ FalseDominant g := by
  constructor
  · intro hf c
    have h := hf c
    simpa [hEq c false, hEq c true] using h
  · intro hg c
    have h := hg c
    simpa [← hEq c false, ← hEq c true] using h

def doubleWeights (weights : SelectionWeight) : SelectionWeight :=
  fun c r => 2 * weights c r

theorem finiteCommonRescale_preservesFalseBias :
    FalseDominant falseBiasedCapable ∧
    FalseDominant (doubleWeights falseBiasedCapable) := by
  constructor
  · exact falseBiasedCapable_falseDominant
  · intro c
    simp [doubleWeights, falseBiasedCapable]

theorem finiteCommonRescale_preservesAbsenceOfFalseBias :
    ¬ FalseDominant trueBiasedCapable ∧
    ¬ FalseDominant (doubleWeights trueBiasedCapable) := by
  constructor
  · exact trueBiasedCapable_not_falseDominant
  · intro h
    have bad := h false
    simp [doubleWeights, trueBiasedCapable] at bad

structure DecoratedWeights where
  base : SelectionWeight
  habitFlag : Bit

def decoratedHabitTrue : DecoratedWeights where
  base := falseBiasedCapable
  habitFlag := true

def decoratedHabitFalse : DecoratedWeights where
  base := falseBiasedCapable
  habitFlag := false

theorem habitLabelDeletion_capability :
    Capable identitySuccess decoratedHabitTrue.base ↔
    Capable identitySuccess decoratedHabitFalse.base := by
  rfl

theorem habitLabelDeletion_tendency :
    FalseDominant decoratedHabitTrue.base ↔
    FalseDominant decoratedHabitFalse.base := by
  rfl

/--
Combined scoped result:
- competence-like response availability and false-dominant default tendency
  realize all four Boolean combinations;
- neither judgment determines the other;
- the tendency judgment is extensional in the declared selection-weight surface;
- a finite common positive rescaling control preserves the tested dominance;
- a decorative Habit label adds no information.
-/
theorem competenceTendencySeparation_bundle :
    Capable identitySuccess falseBiasedCapable ∧
    FalseDominant falseBiasedCapable ∧
    Capable identitySuccess trueBiasedCapable ∧
    ¬ FalseDominant trueBiasedCapable ∧
    ¬ Capable identitySuccess falseOnly ∧
    FalseDominant falseOnly ∧
    ¬ Capable identitySuccess trueOnly ∧
    ¬ FalseDominant trueOnly := by
  exact ⟨
    falseBiasedCapable_capable,
    falseBiasedCapable_falseDominant,
    trueBiasedCapable_capable,
    trueBiasedCapable_not_falseDominant,
    falseOnly_not_capable,
    falseOnly_falseDominant,
    trueOnly_not_capable,
    trueOnly_not_falseDominant
  ⟩

end HabitSelectionTendencyCountermodel

end RelayTheory
