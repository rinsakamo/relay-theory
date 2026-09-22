import RelayTheory.SkillExactRobustnessCountermodel

namespace RelayTheory

namespace SkillBoundedRobustnessCountermodel

open SkillExactRobustnessCountermodel

def failureAtTrue
    (profile : Profile)
    (variation : Variation) : Nat :=
  if profile true variation then 0 else 1

def FailureCount (profile : Profile) : Nat :=
  failureAtTrue profile false + failureAtTrue profile true

def BudgetQualified
    (profile : Profile)
    (budget : Nat) : Prop :=
  FailureCount profile ≤ budget

theorem robustProfile_failureCount_zero :
    FailureCount robustProfile = 0 := by
  rfl

theorem oneFailureProfile_failureCount_one :
    FailureCount brittleProfile = 1 := by
  rfl

theorem oneFailureProfile_not_exactRobust :
    ¬ ExactRobust identitySuccess brittleProfile :=
  brittleProfile_not_exactRobust

theorem robustProfile_budgetZero :
    BudgetQualified robustProfile 0 := by
  simp [BudgetQualified, FailureCount, failureAtTrue, robustProfile]

theorem oneFailureProfile_not_budgetZero :
    ¬ BudgetQualified brittleProfile 0 := by
  simp [BudgetQualified, FailureCount, failureAtTrue, brittleProfile]

theorem oneFailureProfile_budgetOne :
    BudgetQualified brittleProfile 1 := by
  simp [BudgetQualified, FailureCount, failureAtTrue, brittleProfile]

theorem thresholdRelativityControl :
    ¬ BudgetQualified brittleProfile 0 ∧
    BudgetQualified brittleProfile 1 := by
  exact ⟨oneFailureProfile_not_budgetZero,
    oneFailureProfile_budgetOne⟩

theorem boundedQualification_doesNotImplyExactRobustness :
    BudgetQualified brittleProfile 1 ∧
    ¬ ExactRobust identitySuccess brittleProfile := by
  exact ⟨oneFailureProfile_budgetOne,
    oneFailureProfile_not_exactRobust⟩

theorem sameBudgetSeparatesProfiles :
    BudgetQualified robustProfile 0 ∧
    ¬ BudgetQualified brittleProfile 0 := by
  exact ⟨robustProfile_budgetZero,
    oneFailureProfile_not_budgetZero⟩

theorem extensionalProfilesPreserveFailureCount
    (f g : Profile)
    (hEq : ∀ c : Context, ∀ v : Variation, f c v = g c v) :
    FailureCount f = FailureCount g := by
  unfold FailureCount failureAtTrue
  rw [hEq true false, hEq true true]

theorem extensionalProfilesPreserveBudgetQualification
    (f g : Profile)
    (budget : Nat)
    (hEq : ∀ c : Context, ∀ v : Variation, f c v = g c v) :
    BudgetQualified f budget ↔ BudgetQualified g budget := by
  have hCount := extensionalProfilesPreserveFailureCount f g hEq
  unfold BudgetQualified
  rw [hCount]

structure DecoratedProfile where
  profile : Profile
  approximateRobustnessFlag : Bool

def decoratedTrue : DecoratedProfile where
  profile := brittleProfile
  approximateRobustnessFlag := true

def decoratedFalse : DecoratedProfile where
  profile := brittleProfile
  approximateRobustnessFlag := false

theorem approximateRobustnessLabelDeletionControl :
    BudgetQualified decoratedTrue.profile 1 ↔
    BudgetQualified decoratedFalse.profile 1 := by
  rfl

end SkillBoundedRobustnessCountermodel

end RelayTheory
