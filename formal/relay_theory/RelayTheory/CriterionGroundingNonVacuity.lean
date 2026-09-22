namespace RelayTheory

namespace CriterionGroundingNonVacuity

abbrev Context := Bool
abbrev Response := Bool
abbrev Behavior := Context → Response
abbrev Criterion := Context → Response → Bool

/--
A behavior is competent relative to a declared criterion when every context in
the finite Boolean scope is judged successful.
-/
def Competent
    (criterion : Criterion)
    (behavior : Behavior) : Prop :=
  ∀ context, criterion context (behavior context) = true

/--
Existential criterion attribution is the deliberately dangerous formulation:
the criterion may be chosen after the behavior is fixed.
-/
def ExistentialCriterionAttribution
    (behavior : Behavior) : Prop :=
  ∃ criterion : Criterion, Competent criterion behavior

/--
A maximally permissive criterion judges every context/response pair successful.
-/
def permissiveCriterion : Criterion :=
  fun _ _ => true

/--
Every behavior can be made competent when criterion choice is unconstrained.
-/
theorem arbitraryCriterionMakesAnyBehaviorCompetent
    (behavior : Behavior) :
    ∃ criterion : Criterion, Competent criterion behavior := by
  refine ⟨permissiveCriterion, ?_⟩
  intro context
  rfl

/--
Therefore existential criterion attribution is universal over behaviors and
cannot discriminate among them.
-/
theorem existentialCriterionAttributionIsUniversal
    (behavior : Behavior) :
    ExistentialCriterionAttribution behavior := by
  exact arbitraryCriterionMakesAnyBehaviorCompetent behavior

/--
An independently declared matched criterion: success requires response=context.
-/
def identityCriterion : Criterion :=
  fun context response =>
    if response = context then true else false

def identityBehavior : Behavior :=
  fun context => context

def constantFalseBehavior : Behavior :=
  fun _ => false

theorem groundedIdentityCriterionAcceptsIdentity :
    Competent identityCriterion identityBehavior := by
  intro context
  simp [identityCriterion, identityBehavior]

theorem groundedIdentityCriterionRejectsConstantFalse :
    ¬ Competent identityCriterion constantFalseBehavior := by
  intro h
  have htrue := h true
  simp [identityCriterion, constantFalseBehavior] at htrue

/--
The matched fixed criterion separates the two behaviors.
-/
theorem fixedGroundedCriterionDiscriminates :
    Competent identityCriterion identityBehavior ∧
    ¬ Competent identityCriterion constantFalseBehavior := by
  exact ⟨
    groundedIdentityCriterionAcceptsIdentity,
    groundedIdentityCriterionRejectsConstantFalse
  ⟩

/--
By contrast, existential criterion attribution accepts both matched behaviors.
-/
theorem existentialCriterionFailsToDiscriminate :
    ExistentialCriterionAttribution identityBehavior ∧
    ExistentialCriterionAttribution constantFalseBehavior := by
  exact ⟨
    existentialCriterionAttributionIsUniversal identityBehavior,
    existentialCriterionAttributionIsUniversal constantFalseBehavior
  ⟩

/--
Compact non-vacuity contrast: arbitrary existential Q is universal, while one
fixed independently declared Q retains a behavior distinction.
-/
theorem criterionGroundingRestoresDiscrimination :
    (ExistentialCriterionAttribution identityBehavior ∧
      ExistentialCriterionAttribution constantFalseBehavior) ∧
    (Competent identityCriterion identityBehavior ∧
      ¬ Competent identityCriterion constantFalseBehavior) := by
  exact ⟨
    existentialCriterionFailsToDiscriminate,
    fixedGroundedCriterionDiscriminates
  ⟩

end CriterionGroundingNonVacuity

end RelayTheory
