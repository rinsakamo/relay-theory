namespace RelayTheory

namespace OperationalSkillCountermodel

abbrev Bit := Bool
abbrev Context := Bit
abbrev Response := Bit
abbrev Policy := Context → Response
abbrev SuccessCriterion := Context → Response → Prop
abbrev ObservedSignature := Context × Response

def generalPolicy : Policy :=
  fun c => c

def replayPolicy : Policy :=
  fun _ => false

def identitySuccess : SuccessCriterion :=
  fun c r => r = c

def constantFalseSuccess : SuccessCriterion :=
  fun _ r => r = false

def observedContext : Context := false

def observedSignature (p : Policy) : ObservedSignature :=
  (observedContext, p observedContext)

theorem sameObservedTrainingSignature :
    observedSignature generalPolicy = observedSignature replayPolicy := by
  rfl

def Competent (success : SuccessCriterion) (policy : Policy) : Prop :=
  ∀ c : Context, success c (policy c)

theorem generalPolicy_competent_identityTask :
    Competent identitySuccess generalPolicy := by
  intro c
  rfl

theorem replayPolicy_not_competent_identityTask :
    ¬ Competent identitySuccess replayPolicy := by
  intro h
  have bad := h true
  exact Bool.noConfusion bad

theorem hiddenContextSeparatesPolicies :
    identitySuccess true (generalPolicy true) ∧
    ¬ identitySuccess true (replayPolicy true) := by
  constructor
  · rfl
  · intro h
    exact Bool.noConfusion h

theorem matchedObservedHistory_separatedByCompetence :
    observedSignature generalPolicy = observedSignature replayPolicy ∧
    Competent identitySuccess generalPolicy ∧
    ¬ Competent identitySuccess replayPolicy := by
  exact ⟨sameObservedTrainingSignature,
    generalPolicy_competent_identityTask,
    replayPolicy_not_competent_identityTask⟩

theorem replayPolicy_competent_constantFalseTask :
    Competent constantFalseSuccess replayPolicy := by
  intro c
  rfl

theorem generalPolicy_not_competent_constantFalseTask :
    ¬ Competent constantFalseSuccess generalPolicy := by
  intro h
  have bad := h true
  exact Bool.noConfusion bad

theorem taskRelativityControl :
    Competent constantFalseSuccess replayPolicy ∧
    ¬ Competent identitySuccess replayPolicy := by
  exact ⟨replayPolicy_competent_constantFalseTask,
    replayPolicy_not_competent_identityTask⟩

theorem extensionalPoliciesPreserveCompetence
    (success : SuccessCriterion)
    (p q : Policy)
    (hEq : ∀ c : Context, p c = q c) :
    Competent success p ↔ Competent success q := by
  constructor
  · intro hp c
    rw [← hEq c]
    exact hp c
  · intro hq c
    rw [hEq c]
    exact hq c

structure DecoratedPolicy where
  policy : Policy
  skillFlag : Bit

def decoratedTrue : DecoratedPolicy where
  policy := generalPolicy
  skillFlag := true

def decoratedFalse : DecoratedPolicy where
  policy := generalPolicy
  skillFlag := false

theorem skillLabelDeletionControl :
    Competent identitySuccess decoratedTrue.policy ↔
    Competent identitySuccess decoratedFalse.policy := by
  rfl

end OperationalSkillCountermodel

end RelayTheory
