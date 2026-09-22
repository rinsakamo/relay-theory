import RelayTheory.OperationalSkillCountermodel

namespace RelayTheory

namespace SkillCompetenceResourceOrthogonality

abbrev Policy := OperationalSkillCountermodel.Policy
abbrev SuccessCriterion := OperationalSkillCountermodel.SuccessCriterion

structure ResourceAnnotatedPolicy where
  policy : Policy
  cost : Nat
  decorativeCrystallized : Bool

def compactGeneral : ResourceAnnotatedPolicy where
  policy := OperationalSkillCountermodel.generalPolicy
  cost := 1
  decorativeCrystallized := false

def expensiveGeneral : ResourceAnnotatedPolicy where
  policy := OperationalSkillCountermodel.generalPolicy
  cost := 2
  decorativeCrystallized := false

def compactReplay : ResourceAnnotatedPolicy where
  policy := OperationalSkillCountermodel.replayPolicy
  cost := 1
  decorativeCrystallized := false

def compactGeneralDecorated : ResourceAnnotatedPolicy where
  policy := OperationalSkillCountermodel.generalPolicy
  cost := 1
  decorativeCrystallized := true

def FitsBudget (budget : Nat) (candidate : ResourceAnnotatedPolicy) : Prop :=
  candidate.cost ≤ budget

def ResourceQualified
    (success : SuccessCriterion)
    (budget : Nat)
    (candidate : ResourceAnnotatedPolicy) : Prop :=
  OperationalSkillCountermodel.Competent success candidate.policy ∧
  FitsBudget budget candidate

theorem sameCompetence_differentCost :
    OperationalSkillCountermodel.Competent
      OperationalSkillCountermodel.identitySuccess
      compactGeneral.policy ∧
    OperationalSkillCountermodel.Competent
      OperationalSkillCountermodel.identitySuccess
      expensiveGeneral.policy ∧
    compactGeneral.cost < expensiveGeneral.cost := by
  exact ⟨
    OperationalSkillCountermodel.generalPolicy_competent_identityTask,
    OperationalSkillCountermodel.generalPolicy_competent_identityTask,
    by decide
  ⟩

theorem sameCost_differentCompetence :
    compactGeneral.cost = compactReplay.cost ∧
    OperationalSkillCountermodel.Competent
      OperationalSkillCountermodel.identitySuccess
      compactGeneral.policy ∧
    ¬ OperationalSkillCountermodel.Competent
      OperationalSkillCountermodel.identitySuccess
      compactReplay.policy := by
  exact ⟨
    rfl,
    OperationalSkillCountermodel.generalPolicy_competent_identityTask,
    OperationalSkillCountermodel.replayPolicy_not_competent_identityTask
  ⟩

theorem budgetSeparatesEqualCompetence :
    FitsBudget 1 compactGeneral ∧
    ¬ FitsBudget 1 expensiveGeneral := by
  simp [FitsBudget, compactGeneral, expensiveGeneral]

theorem equalBudgetDoesNotDetermineCompetence :
    FitsBudget 1 compactGeneral ∧
    FitsBudget 1 compactReplay ∧
    OperationalSkillCountermodel.Competent
      OperationalSkillCountermodel.identitySuccess
      compactGeneral.policy ∧
    ¬ OperationalSkillCountermodel.Competent
      OperationalSkillCountermodel.identitySuccess
      compactReplay.policy := by
  exact ⟨
    by simp [FitsBudget, compactGeneral],
    by simp [FitsBudget, compactReplay],
    OperationalSkillCountermodel.generalPolicy_competent_identityTask,
    OperationalSkillCountermodel.replayPolicy_not_competent_identityTask
  ⟩

theorem combinedJudgmentReconstructed :
    ResourceQualified
      OperationalSkillCountermodel.identitySuccess
      1
      compactGeneral ∧
    ¬ ResourceQualified
      OperationalSkillCountermodel.identitySuccess
      1
      expensiveGeneral ∧
    ¬ ResourceQualified
      OperationalSkillCountermodel.identitySuccess
      1
      compactReplay := by
  constructor
  · exact ⟨
      OperationalSkillCountermodel.generalPolicy_competent_identityTask,
      by simp [FitsBudget, compactGeneral]
    ⟩
  constructor
  · intro h
    exact (by
      simp [FitsBudget, expensiveGeneral] : ¬ FitsBudget 1 expensiveGeneral) h.2
  · intro h
    exact OperationalSkillCountermodel.replayPolicy_not_competent_identityTask h.1

theorem decorativeCrystallizationLabelDeletion_competence :
    OperationalSkillCountermodel.Competent
      OperationalSkillCountermodel.identitySuccess
      compactGeneral.policy ↔
    OperationalSkillCountermodel.Competent
      OperationalSkillCountermodel.identitySuccess
      compactGeneralDecorated.policy := by
  rfl

theorem decorativeCrystallizationLabelDeletion_resource :
    FitsBudget 1 compactGeneral ↔
    FitsBudget 1 compactGeneralDecorated := by
  rfl

theorem decorativeCrystallizationLabelDeletion_combined :
    ResourceQualified
      OperationalSkillCountermodel.identitySuccess
      1
      compactGeneral ↔
    ResourceQualified
      OperationalSkillCountermodel.identitySuccess
      1
      compactGeneralDecorated := by
  rfl

end SkillCompetenceResourceOrthogonality

end RelayTheory
