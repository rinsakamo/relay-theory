import RelayTheory.PossessionCustodyAccessCountermodel

namespace RelayTheory

namespace FocalMembershipIntegrationCountermodel

/-!
This finite module tests the scoped operational split recorded by #71.
It does not identify bidirectional functional integration with phenomenal or biological Selfhood.
-/

abbrev Bit := Bool
abbrev RealizedSnapshot := Bit × Bit

/--
A candidate component relative to a supplied focal partition.

`insideFocal` is analytic evaluation membership only. It is not a Selfhood,
body-ownership, or incorporation predicate.
-/
structure CandidateComponent where
  insideFocal : Bit
  actualComponent : Bit
  actualFocalTarget : Bit
  componentUnderFocalSource : Bit → Bit
  focalTargetUnderComponent : Bit → Bit

def realizedSnapshot (c : CandidateComponent) : RealizedSnapshot :=
  (c.actualComponent, c.actualFocalTarget)

def Sensitive (f : Bit → Bit) : Prop :=
  f false ≠ f true

def OutboundIntegrated (c : CandidateComponent) : Prop :=
  Sensitive c.componentUnderFocalSource

def InboundIntegrated (c : CandidateComponent) : Prop :=
  Sensitive c.focalTargetUnderComponent

def FunctionallyIntegrated (c : CandidateComponent) : Prop :=
  OutboundIntegrated c ∧ InboundIntegrated c

def outsideUnintegrated : CandidateComponent where
  insideFocal := false
  actualComponent := false
  actualFocalTarget := false
  componentUnderFocalSource _ := false
  focalTargetUnderComponent _ := false

def outsideIntegrated : CandidateComponent where
  insideFocal := false
  actualComponent := false
  actualFocalTarget := false
  componentUnderFocalSource x := x
  focalTargetUnderComponent x := x

def insideUnintegrated : CandidateComponent where
  insideFocal := true
  actualComponent := false
  actualFocalTarget := false
  componentUnderFocalSource _ := false
  focalTargetUnderComponent _ := false

def insideIntegrated : CandidateComponent where
  insideFocal := true
  actualComponent := false
  actualFocalTarget := false
  componentUnderFocalSource x := x
  focalTargetUnderComponent x := x

def outboundOnly : CandidateComponent where
  insideFocal := false
  actualComponent := false
  actualFocalTarget := false
  componentUnderFocalSource x := x
  focalTargetUnderComponent _ := false

def inboundOnly : CandidateComponent where
  insideFocal := false
  actualComponent := false
  actualFocalTarget := false
  componentUnderFocalSource _ := false
  focalTargetUnderComponent x := x

theorem identitySensitive : Sensitive (fun x : Bit => x) := by
  intro h
  exact Bool.noConfusion h

theorem constantFalseNotSensitive : ¬ Sensitive (fun _ : Bit => false) := by
  intro h
  exact h rfl

theorem allQuadrants_sameRealizedSnapshot :
    realizedSnapshot outsideUnintegrated = realizedSnapshot outsideIntegrated ∧
    realizedSnapshot outsideUnintegrated = realizedSnapshot insideUnintegrated ∧
    realizedSnapshot outsideUnintegrated = realizedSnapshot insideIntegrated := by
  exact ⟨rfl, rfl, rfl⟩

theorem outsideUnintegrated_quadrant :
    outsideUnintegrated.insideFocal = false ∧
    ¬ FunctionallyIntegrated outsideUnintegrated := by
  constructor
  · rfl
  · intro h
    exact constantFalseNotSensitive h.1

theorem outsideIntegrated_quadrant :
    outsideIntegrated.insideFocal = false ∧
    FunctionallyIntegrated outsideIntegrated := by
  exact ⟨rfl, identitySensitive, identitySensitive⟩

theorem insideUnintegrated_quadrant :
    insideUnintegrated.insideFocal = true ∧
    ¬ FunctionallyIntegrated insideUnintegrated := by
  constructor
  · rfl
  · intro h
    exact constantFalseNotSensitive h.1

theorem insideIntegrated_quadrant :
    insideIntegrated.insideFocal = true ∧
    FunctionallyIntegrated insideIntegrated := by
  exact ⟨rfl, identitySensitive, identitySensitive⟩

theorem membershipAndIntegration_independentlyVariable :
    (outsideUnintegrated.insideFocal = false ∧
      ¬ FunctionallyIntegrated outsideUnintegrated) ∧
    (outsideIntegrated.insideFocal = false ∧
      FunctionallyIntegrated outsideIntegrated) ∧
    (insideUnintegrated.insideFocal = true ∧
      ¬ FunctionallyIntegrated insideUnintegrated) ∧
    (insideIntegrated.insideFocal = true ∧
      FunctionallyIntegrated insideIntegrated) := by
  exact ⟨
    outsideUnintegrated_quadrant,
    outsideIntegrated_quadrant,
    insideUnintegrated_quadrant,
    insideIntegrated_quadrant
  ⟩

theorem outboundOnly_notFunctionallyIntegrated :
    OutboundIntegrated outboundOnly ∧
    ¬ InboundIntegrated outboundOnly ∧
    ¬ FunctionallyIntegrated outboundOnly := by
  exact ⟨
    identitySensitive,
    constantFalseNotSensitive,
    by
      intro h
      exact constantFalseNotSensitive h.2
  ⟩

theorem inboundOnly_notFunctionallyIntegrated :
    ¬ OutboundIntegrated inboundOnly ∧
    InboundIntegrated inboundOnly ∧
    ¬ FunctionallyIntegrated inboundOnly := by
  exact ⟨
    constantFalseNotSensitive,
    identitySensitive,
    by
      intro h
      exact constantFalseNotSensitive h.1
  ⟩

/--
A #61 custody-like transport profile can coexist with no bidirectional focal
integration.
-/
theorem custodyLike_withoutFunctionalIntegration :
    PossessionCustodyAccessCountermodel.CustodyLike
      PossessionCustodyAccessCountermodel.custodyOnlyProfile ∧
    ¬ FunctionallyIntegrated outsideUnintegrated := by
  exact ⟨
    PossessionCustodyAccessCountermodel.custodyOnly_quadrant.1,
    outsideUnintegrated_quadrant.2
  ⟩

/--
Bidirectional focal integration can coexist with absence of the #61
custody-like transport role.
-/
theorem functionalIntegration_withoutCustodyLike :
    FunctionallyIntegrated outsideIntegrated ∧
    ¬ PossessionCustodyAccessCountermodel.CustodyLike
      PossessionCustodyAccessCountermodel.accessOnlyProfile := by
  exact ⟨
    outsideIntegrated_quadrant.2,
    PossessionCustodyAccessCountermodel.accessOnly_quadrant.1
  ⟩

/--
A #61 access-like use profile can likewise coexist with no bidirectional focal
integration.
-/
theorem accessLike_withoutFunctionalIntegration :
    PossessionCustodyAccessCountermodel.AccessLike
      PossessionCustodyAccessCountermodel.accessOnlyProfile ∧
    ¬ FunctionallyIntegrated outsideUnintegrated := by
  exact ⟨
    PossessionCustodyAccessCountermodel.accessOnly_quadrant.2,
    outsideUnintegrated_quadrant.2
  ⟩

structure DecoratedComponent where
  base : CandidateComponent
  incorporationFlag : Bit

def decoratedTrue : DecoratedComponent where
  base := insideIntegrated
  incorporationFlag := true

def decoratedFalse : DecoratedComponent where
  base := insideIntegrated
  incorporationFlag := false

theorem incorporationLabelDeletion_membership :
    decoratedTrue.base.insideFocal = decoratedFalse.base.insideFocal := by
  rfl

theorem incorporationLabelDeletion_functional :
    FunctionallyIntegrated decoratedTrue.base ↔
    FunctionallyIntegrated decoratedFalse.base := by
  rfl

/--
Combined scoped result: analytic focal membership and bidirectional functional
integration are independent, one-way coupling is insufficient for the declared
functional role, and #61 custody/access roles do not force functional
integration.
-/
theorem membershipIntegrationSplit_bundle :
    realizedSnapshot outsideUnintegrated = realizedSnapshot outsideIntegrated ∧
    realizedSnapshot outsideUnintegrated = realizedSnapshot insideUnintegrated ∧
    realizedSnapshot outsideUnintegrated = realizedSnapshot insideIntegrated ∧
    outsideIntegrated.insideFocal = false ∧
    FunctionallyIntegrated outsideIntegrated ∧
    insideUnintegrated.insideFocal = true ∧
    ¬ FunctionallyIntegrated insideUnintegrated ∧
    ¬ FunctionallyIntegrated outboundOnly ∧
    ¬ FunctionallyIntegrated inboundOnly := by
  exact ⟨
    rfl,
    rfl,
    rfl,
    rfl,
    outsideIntegrated_quadrant.2,
    rfl,
    insideUnintegrated_quadrant.2,
    outboundOnly_notFunctionallyIntegrated.2.2,
    inboundOnly_notFunctionallyIntegrated.2.2
  ⟩

end FocalMembershipIntegrationCountermodel

end RelayTheory
