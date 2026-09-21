namespace RelayTheory

namespace OperationalPerceptionCountermodel

abbrev Bit := Bool
abbrev RealizedSignature := Bit × Bit

/--
Minimal lower-level response model for an exterior source and an internal
response. No Perception-classification field is present.
-/
structure InwardResponseModel where
  actualExterior : Bit
  actualInternal : Bit
  internalUnderExterior : Bit → Bit

def sensitiveModel : InwardResponseModel where
  actualExterior := true
  actualInternal := true
  internalUnderExterior w := w

def replayModel : InwardResponseModel where
  actualExterior := true
  actualInternal := true
  internalUnderExterior _ := true

def invertedModel : InwardResponseModel where
  actualExterior := true
  actualInternal := false
  internalUnderExterior w := Bool.not w

def realizedSignature (m : InwardResponseModel) : RealizedSignature :=
  (m.actualExterior, m.actualInternal)

theorem sameRealizedSignature :
    realizedSignature sensitiveModel = realizedSignature replayModel := by
  rfl

/-- Counterfactual response of the internal target depends on the exterior source. -/
def ExteriorSensitive (m : InwardResponseModel) : Prop :=
  m.internalUnderExterior false ≠ m.internalUnderExterior true

theorem sensitiveModel_exteriorSensitive :
    ExteriorSensitive sensitiveModel := by
  intro h
  exact Bool.noConfusion h

theorem replayModel_not_exteriorSensitive :
    ¬ ExteriorSensitive replayModel := by
  intro h
  exact h rfl

theorem invertedModel_exteriorSensitive :
    ExteriorSensitive invertedModel := by
  intro h
  exact Bool.noConfusion h

/--
Only focal membership is supplied. The view does not say that Perception
occurred.
-/
structure FocalView where
  sourceInside : Bit
  targetInside : Bit

def inwardView : FocalView where
  sourceInside := false
  targetInside := true

def internalView : FocalView where
  sourceInside := true
  targetInside := true

def InwardRelativeTo (view : FocalView) : Prop :=
  view.sourceInside = false ∧ view.targetInside = true

/--
Operational perception-like attribution candidate: counterfactual exterior
sensitivity crossing the supplied focal partition inward.
-/
def PerceptionLike
    (m : InwardResponseModel)
    (view : FocalView) : Prop :=
  ExteriorSensitive m ∧ InwardRelativeTo view

theorem sensitive_inward_perceptionLike :
    PerceptionLike sensitiveModel inwardView := by
  exact ⟨sensitiveModel_exteriorSensitive, ⟨rfl, rfl⟩⟩

theorem replay_inward_not_perceptionLike :
    ¬ PerceptionLike replayModel inwardView := by
  intro h
  exact replayModel_not_exteriorSensitive h.1

theorem matchedRealizedTrace_separatedByPerceptionLike :
    realizedSignature sensitiveModel = realizedSignature replayModel ∧
    PerceptionLike sensitiveModel inwardView ∧
    ¬ PerceptionLike replayModel inwardView := by
  exact ⟨sameRealizedSignature,
    sensitive_inward_perceptionLike,
    replay_inward_not_perceptionLike⟩

theorem focalReindexingChangesPerceptionLike :
    PerceptionLike sensitiveModel inwardView ∧
    ¬ PerceptionLike sensitiveModel internalView := by
  constructor
  · exact sensitive_inward_perceptionLike
  · intro h
    exact Bool.noConfusion h.2.1

/--
Exterior sensitivity does not imply veridical identity between source and
internal response: the inverted channel is still perception-like operationally.
-/
theorem invertedChannelShowsVeridicalityIsSeparate :
    PerceptionLike invertedModel inwardView ∧
    invertedModel.actualExterior ≠ invertedModel.actualInternal := by
  constructor
  · exact ⟨invertedModel_exteriorSensitive, ⟨rfl, rfl⟩⟩
  · intro h
    exact Bool.noConfusion h

/--
A decorative Perception flag can vary while the lower-level classification is
unchanged. The flag is not consulted by PerceptionLike.
-/
structure DecoratedModel where
  base : InwardResponseModel
  perceptionFlag : Bit

def decoratedTrue : DecoratedModel where
  base := sensitiveModel
  perceptionFlag := true

def decoratedFalse : DecoratedModel where
  base := sensitiveModel
  perceptionFlag := false

theorem perceptionLabelDeletionControl :
    PerceptionLike decoratedTrue.base inwardView ↔
    PerceptionLike decoratedFalse.base inwardView := by
  rfl

end OperationalPerceptionCountermodel

end RelayTheory
