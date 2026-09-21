namespace RelayTheory

namespace OperationalCognitionCountermodel

abbrev Bit := Bool
abbrev RealizedSignature := Bit × Bit × Bit

/--
Minimal lower-level model for an internal source, an internal intermediate, and
a later response. No Cognition-classification field is present.
-/
structure InternalProcessModel where
  actualSource : Bit
  actualIntermediate : Bit
  actualResponse : Bit
  intermediateUnderSource : Bit → Bit
  responseUnderIntermediate : Bit → Bit

def activeModel : InternalProcessModel where
  actualSource := true
  actualIntermediate := true
  actualResponse := true
  intermediateUnderSource s := s
  responseUnderIntermediate m := m

def replayModel : InternalProcessModel where
  actualSource := true
  actualIntermediate := true
  actualResponse := true
  intermediateUnderSource _ := true
  responseUnderIntermediate m := m

def inertModel : InternalProcessModel where
  actualSource := true
  actualIntermediate := true
  actualResponse := true
  intermediateUnderSource s := s
  responseUnderIntermediate _ := true

def realizedSignature (m : InternalProcessModel) : RealizedSignature :=
  (m.actualSource, m.actualIntermediate, m.actualResponse)

theorem sameRealizedSignature_active_replay :
    realizedSignature activeModel = realizedSignature replayModel := by
  rfl

theorem sameRealizedSignature_active_inert :
    realizedSignature activeModel = realizedSignature inertModel := by
  rfl

def InternalSensitive (m : InternalProcessModel) : Prop :=
  m.intermediateUnderSource false ≠ m.intermediateUnderSource true

def DownstreamRelevant (m : InternalProcessModel) : Prop :=
  m.responseUnderIntermediate false ≠ m.responseUnderIntermediate true

theorem active_internalSensitive : InternalSensitive activeModel := by
  intro h
  exact Bool.noConfusion h

theorem replay_not_internalSensitive : ¬ InternalSensitive replayModel := by
  intro h
  exact h rfl

theorem inert_internalSensitive : InternalSensitive inertModel := by
  intro h
  exact Bool.noConfusion h

theorem active_downstreamRelevant : DownstreamRelevant activeModel := by
  intro h
  exact Bool.noConfusion h

theorem replay_downstreamRelevant : DownstreamRelevant replayModel := by
  intro h
  exact Bool.noConfusion h

theorem inert_not_downstreamRelevant : ¬ DownstreamRelevant inertModel := by
  intro h
  exact h rfl

structure FocalView where
  sourceInside : Bit
  intermediateInside : Bit
  responseInside : Bit

def allInternalView : FocalView where
  sourceInside := true
  intermediateInside := true
  responseInside := true

def sourceExteriorView : FocalView where
  sourceInside := false
  intermediateInside := true
  responseInside := true

def InternalRelativeTo (view : FocalView) : Prop :=
  view.sourceInside = true ∧ view.intermediateInside = true

def CognitionLike
    (m : InternalProcessModel)
    (view : FocalView) : Prop :=
  InternalSensitive m ∧ DownstreamRelevant m ∧ InternalRelativeTo view

theorem active_allInternal_cognitionLike :
    CognitionLike activeModel allInternalView := by
  exact ⟨active_internalSensitive,
    active_downstreamRelevant,
    ⟨rfl, rfl⟩⟩

theorem replay_allInternal_not_cognitionLike :
    ¬ CognitionLike replayModel allInternalView := by
  intro h
  exact replay_not_internalSensitive h.1

theorem inert_allInternal_not_cognitionLike :
    ¬ CognitionLike inertModel allInternalView := by
  intro h
  exact inert_not_downstreamRelevant h.2.1

theorem matchedRealizedTrace_separatesSourceSensitivity :
    realizedSignature activeModel = realizedSignature replayModel ∧
    CognitionLike activeModel allInternalView ∧
    ¬ CognitionLike replayModel allInternalView := by
  exact ⟨sameRealizedSignature_active_replay,
    active_allInternal_cognitionLike,
    replay_allInternal_not_cognitionLike⟩

theorem matchedRealizedTrace_separatesDownstreamRelevance :
    realizedSignature activeModel = realizedSignature inertModel ∧
    CognitionLike activeModel allInternalView ∧
    ¬ CognitionLike inertModel allInternalView := by
  exact ⟨sameRealizedSignature_active_inert,
    active_allInternal_cognitionLike,
    inert_allInternal_not_cognitionLike⟩

/--
The later response can remain inside the focal locus. Operational cognition-like
classification therefore does not require an exterior Action-like response.
-/
theorem internalDownstreamResponseNeedsNoAction :
    CognitionLike activeModel allInternalView ∧
    allInternalView.responseInside = true := by
  exact ⟨active_allInternal_cognitionLike, rfl⟩

theorem focalReindexingChangesCognitionLike :
    CognitionLike activeModel allInternalView ∧
    ¬ CognitionLike activeModel sourceExteriorView := by
  constructor
  · exact active_allInternal_cognitionLike
  · intro h
    exact Bool.noConfusion h.2.2.1

structure DecoratedModel where
  base : InternalProcessModel
  cognitionFlag : Bit

def decoratedTrue : DecoratedModel where
  base := activeModel
  cognitionFlag := true

def decoratedFalse : DecoratedModel where
  base := activeModel
  cognitionFlag := false

theorem cognitionLabelDeletionControl :
    CognitionLike decoratedTrue.base allInternalView ↔
    CognitionLike decoratedFalse.base allInternalView := by
  rfl

end OperationalCognitionCountermodel

end RelayTheory
