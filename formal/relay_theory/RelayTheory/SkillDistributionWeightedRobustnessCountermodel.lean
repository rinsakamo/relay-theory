import RelayTheory.SkillBoundedRobustnessCountermodel

namespace RelayTheory

namespace SkillDistributionWeightedRobustnessCountermodel

open SkillExactRobustnessCountermodel
open SkillBoundedRobustnessCountermodel

abbrev Weights := Nat × Nat

def failOnTrue : Profile :=
  fun c v => if v then false else c

def failOnFalse : Profile :=
  fun c v => if v then c else false

theorem failOnTrue_failureCount_one :
    FailureCount failOnTrue = 1 := by
  rfl

theorem failOnFalse_failureCount_one :
    FailureCount failOnFalse = 1 := by
  rfl

theorem equalUnweightedFailureCount :
    FailureCount failOnTrue = FailureCount failOnFalse := by
  rw [failOnTrue_failureCount_one, failOnFalse_failureCount_one]

def falseHeavy : Weights := (2, 1)

def trueHeavy : Weights := (1, 2)

def totalWeight (weights : Weights) : Nat :=
  weights.1 + weights.2

theorem equalWeightMass :
    totalWeight falseHeavy = totalWeight trueHeavy := by
  rfl

def WeightedFailure
    (weights : Weights)
    (profile : Profile) : Nat :=
  weights.1 * failureAtTrue profile false +
  weights.2 * failureAtTrue profile true

theorem falseHeavy_failOnTrue_exact :
    WeightedFailure falseHeavy failOnTrue = 1 := by
  rfl

theorem falseHeavy_failOnFalse_exact :
    WeightedFailure falseHeavy failOnFalse = 2 := by
  rfl

theorem trueHeavy_failOnTrue_exact :
    WeightedFailure trueHeavy failOnTrue = 2 := by
  rfl

theorem trueHeavy_failOnFalse_exact :
    WeightedFailure trueHeavy failOnFalse = 1 := by
  rfl

theorem falseHeavy_prefers_failOnTrue :
    WeightedFailure falseHeavy failOnTrue <
    WeightedFailure falseHeavy failOnFalse := by
  decide

theorem trueHeavy_prefers_failOnFalse :
    WeightedFailure trueHeavy failOnFalse <
    WeightedFailure trueHeavy failOnTrue := by
  decide

theorem rankingReversesUnderWeightSwap :
    (WeightedFailure falseHeavy failOnTrue <
      WeightedFailure falseHeavy failOnFalse) ∧
    (WeightedFailure trueHeavy failOnFalse <
      WeightedFailure trueHeavy failOnTrue) := by
  exact ⟨falseHeavy_prefers_failOnTrue,
    trueHeavy_prefers_failOnFalse⟩

theorem sameUnweightedCount_differentWeightedRisk :
    FailureCount failOnTrue = FailureCount failOnFalse ∧
    WeightedFailure falseHeavy failOnTrue ≠
      WeightedFailure falseHeavy failOnFalse := by
  exact ⟨equalUnweightedFailureCount, by decide⟩

theorem extensionalProfilesPreserveWeightedFailure
    (weights : Weights)
    (f g : Profile)
    (hEq : ∀ c : Context, ∀ v : Variation, f c v = g c v) :
    WeightedFailure weights f = WeightedFailure weights g := by
  unfold WeightedFailure failureAtTrue
  rw [hEq true false, hEq true true]

def WeightedQualified
    (weights : Weights)
    (profile : Profile)
    (budget : Nat) : Prop :=
  WeightedFailure weights profile ≤ budget

theorem falseHeavy_budgetOne_separates :
    WeightedQualified falseHeavy failOnTrue 1 ∧
    ¬ WeightedQualified falseHeavy failOnFalse 1 := by
  simp [WeightedQualified, WeightedFailure, failureAtTrue,
    falseHeavy, failOnTrue, failOnFalse]

theorem trueHeavy_budgetOne_separates :
    WeightedQualified trueHeavy failOnFalse 1 ∧
    ¬ WeightedQualified trueHeavy failOnTrue 1 := by
  simp [WeightedQualified, WeightedFailure, failureAtTrue,
    trueHeavy, failOnTrue, failOnFalse]

theorem extensionalProfilesPreserveWeightedQualification
    (weights : Weights)
    (f g : Profile)
    (budget : Nat)
    (hEq : ∀ c : Context, ∀ v : Variation, f c v = g c v) :
    WeightedQualified weights f budget ↔
    WeightedQualified weights g budget := by
  have hRisk := extensionalProfilesPreserveWeightedFailure weights f g hEq
  unfold WeightedQualified
  rw [hRisk]

structure DecoratedProfile where
  profile : Profile
  probabilisticRobustnessFlag : Bool

def decoratedTrue : DecoratedProfile where
  profile := failOnTrue
  probabilisticRobustnessFlag := true

def decoratedFalse : DecoratedProfile where
  profile := failOnTrue
  probabilisticRobustnessFlag := false

theorem probabilisticRobustnessLabelDeletionControl :
    WeightedQualified falseHeavy decoratedTrue.profile 1 ↔
    WeightedQualified falseHeavy decoratedFalse.profile 1 := by
  rfl

end SkillDistributionWeightedRobustnessCountermodel

end RelayTheory
