namespace RelayTheory

namespace SkillCrossWorldTransferCountermodel

abbrev SourceContext := Bool
abbrev TargetContext := Bool
abbrev SourceResponse := Bool
abbrev TargetResponse := Bool

abbrev SourcePolicy := SourceContext → SourceResponse
abbrev TargetPolicy := TargetContext → TargetResponse
abbrev ContextBridge := TargetContext → SourceContext
abbrev ResponseBridge := SourceResponse → TargetResponse
abbrev SourceSuccessCriterion := SourceContext → SourceResponse → Prop
abbrev TargetSuccessCriterion := TargetContext → TargetResponse → Prop

def sourceIdentityPolicy : SourcePolicy :=
  fun c => c

def identityBridge : Bool → Bool :=
  fun x => x

def flipBridge : Bool → Bool :=
  fun x => !x

def sourceIdentitySuccess : SourceSuccessCriterion :=
  fun c r => r = c

def targetIdentitySuccess : TargetSuccessCriterion :=
  fun c r => r = c

def SourceCompetent
    (success : SourceSuccessCriterion)
    (policy : SourcePolicy) : Prop :=
  ∀ c : SourceContext, success c (policy c)

def TargetCompetent
    (success : TargetSuccessCriterion)
    (policy : TargetPolicy) : Prop :=
  ∀ c : TargetContext, success c (policy c)

def Transport
    (policy : SourcePolicy)
    (contextBridge : ContextBridge)
    (responseBridge : ResponseBridge) : TargetPolicy :=
  fun c => responseBridge (policy (contextBridge c))

def Transfers
    (policy : SourcePolicy)
    (contextBridge : ContextBridge)
    (responseBridge : ResponseBridge)
    (success : TargetSuccessCriterion) : Prop :=
  TargetCompetent success (Transport policy contextBridge responseBridge)

theorem sourceIdentity_competent :
    SourceCompetent sourceIdentitySuccess sourceIdentityPolicy := by
  intro c
  rfl

theorem identityIdentity_transfers :
    Transfers sourceIdentityPolicy identityBridge identityBridge
      targetIdentitySuccess := by
  intro c
  rfl

theorem identityFlip_not_transfers :
    ¬ Transfers sourceIdentityPolicy identityBridge flipBridge
      targetIdentitySuccess := by
  intro h
  have bad := h false
  exact Bool.noConfusion bad

theorem flipIdentity_not_transfers :
    ¬ Transfers sourceIdentityPolicy flipBridge identityBridge
      targetIdentitySuccess := by
  intro h
  have bad := h false
  exact Bool.noConfusion bad

theorem flipFlip_transfers :
    Transfers sourceIdentityPolicy flipBridge flipBridge
      targetIdentitySuccess := by
  intro c
  cases c <;> rfl

theorem bridgeAlignmentControlsTransfer :
    Transfers sourceIdentityPolicy identityBridge identityBridge
      targetIdentitySuccess ∧
    ¬ Transfers sourceIdentityPolicy identityBridge flipBridge
      targetIdentitySuccess ∧
    ¬ Transfers sourceIdentityPolicy flipBridge identityBridge
      targetIdentitySuccess ∧
    Transfers sourceIdentityPolicy flipBridge flipBridge
      targetIdentitySuccess := by
  exact ⟨identityIdentity_transfers,
    identityFlip_not_transfers,
    flipIdentity_not_transfers,
    flipFlip_transfers⟩

theorem sourceCompetence_doesNotDetermineTargetTransfer :
    SourceCompetent sourceIdentitySuccess sourceIdentityPolicy ∧
    ¬ Transfers sourceIdentityPolicy identityBridge flipBridge
      targetIdentitySuccess := by
  exact ⟨sourceIdentity_competent, identityFlip_not_transfers⟩

def SelfInverse (bridge : Bool → Bool) : Prop :=
  ∀ x : Bool, bridge (bridge x) = x

theorem identityBridge_selfInverse :
    SelfInverse identityBridge := by
  intro x
  rfl

theorem flipBridge_selfInverse :
    SelfInverse flipBridge := by
  intro x
  cases x <;> rfl

theorem reversibleBridges_areNotUnique :
    SelfInverse identityBridge ∧
    SelfInverse flipBridge ∧
    identityBridge false ≠ flipBridge false := by
  exact ⟨identityBridge_selfInverse,
    flipBridge_selfInverse,
    by intro h; exact Bool.noConfusion h⟩

theorem extensionalSourceAndBridgesPreserveTransfer
    (p q : SourcePolicy)
    (contextA contextB : ContextBridge)
    (responseA responseB : ResponseBridge)
    (success : TargetSuccessCriterion)
    (hPolicy : ∀ c : SourceContext, p c = q c)
    (hContext : ∀ c : TargetContext, contextA c = contextB c)
    (hResponse : ∀ r : SourceResponse, responseA r = responseB r) :
    Transfers p contextA responseA success ↔
    Transfers q contextB responseB success := by
  have hTransport :
      ∀ c : TargetContext,
        Transport p contextA responseA c =
        Transport q contextB responseB c := by
    intro c
    unfold Transport
    rw [hContext c, hPolicy (contextB c), hResponse (q (contextB c))]
  constructor
  · intro h c
    rw [← hTransport c]
    exact h c
  · intro h c
    rw [hTransport c]
    exact h c

structure DecoratedTransferCase where
  policy : SourcePolicy
  contextBridge : ContextBridge
  responseBridge : ResponseBridge
  transferableSkillFlag : Bool

def decoratedTransferTrue : DecoratedTransferCase where
  policy := sourceIdentityPolicy
  contextBridge := identityBridge
  responseBridge := identityBridge
  transferableSkillFlag := true

def decoratedTransferFalse : DecoratedTransferCase where
  policy := sourceIdentityPolicy
  contextBridge := identityBridge
  responseBridge := identityBridge
  transferableSkillFlag := false

theorem transferableSkillLabelDeletionControl :
    Transfers
      decoratedTransferTrue.policy
      decoratedTransferTrue.contextBridge
      decoratedTransferTrue.responseBridge
      targetIdentitySuccess ↔
    Transfers
      decoratedTransferFalse.policy
      decoratedTransferFalse.contextBridge
      decoratedTransferFalse.responseBridge
      targetIdentitySuccess := by
  rfl

end SkillCrossWorldTransferCountermodel

end RelayTheory
