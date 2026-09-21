namespace RelayTheory

namespace OperationalActionCountermodel

abbrev Bit := Bool
abbrev RealizedSignature := Bit × Bit

/--
Minimal lower-level response model for an internal source and an exterior
response.  No Action-classification field is present.
-/
structure OutwardResponseModel where
  actualSource : Bit
  actualExterior : Bit
  exteriorUnderSource : Bit → Bit

def sensitiveModel : OutwardResponseModel where
  actualSource := true
  actualExterior := true
  exteriorUnderSource s := s

def fixedModel : OutwardResponseModel where
  actualSource := true
  actualExterior := true
  exteriorUnderSource _ := true

def realizedSignature (m : OutwardResponseModel) : RealizedSignature :=
  (m.actualSource, m.actualExterior)

theorem sameRealizedSignature :
    realizedSignature sensitiveModel = realizedSignature fixedModel := by
  rfl

/-- Counterfactual response of the exterior target depends on the source. -/
def SourceSensitive (m : OutwardResponseModel) : Prop :=
  m.exteriorUnderSource false ≠ m.exteriorUnderSource true

theorem sensitiveModel_sourceSensitive :
    SourceSensitive sensitiveModel := by
  intro h
  exact Bool.noConfusion h

theorem fixedModel_not_sourceSensitive :
    ¬ SourceSensitive fixedModel := by
  intro h
  exact h rfl

/--
Only focal membership is supplied.  The view does not say that an Action
occurred.
-/
structure FocalView where
  sourceInside : Bit
  targetInside : Bit

def outwardView : FocalView where
  sourceInside := true
  targetInside := false

def internalView : FocalView where
  sourceInside := true
  targetInside := true

def OutwardRelativeTo (view : FocalView) : Prop :=
  view.sourceInside = true ∧ view.targetInside = false

/--
Operational attribution candidate: counterfactual source sensitivity crossing
the supplied focal partition.
-/
def Attributable
    (m : OutwardResponseModel)
    (view : FocalView) : Prop :=
  SourceSensitive m ∧ OutwardRelativeTo view

theorem sensitive_outward_attributable :
    Attributable sensitiveModel outwardView := by
  exact ⟨sensitiveModel_sourceSensitive, ⟨rfl, rfl⟩⟩

theorem fixed_outward_not_attributable :
    ¬ Attributable fixedModel outwardView := by
  intro h
  exact fixedModel_not_sourceSensitive h.1

theorem matchedRealizedTrace_separatedByAttribution :
    realizedSignature sensitiveModel = realizedSignature fixedModel ∧
    Attributable sensitiveModel outwardView ∧
    ¬ Attributable fixedModel outwardView := by
  exact ⟨sameRealizedSignature,
    sensitive_outward_attributable,
    fixed_outward_not_attributable⟩

theorem focalReindexingChangesOutwardAttribution :
    Attributable sensitiveModel outwardView ∧
    ¬ Attributable sensitiveModel internalView := by
  constructor
  · exact sensitive_outward_attributable
  · intro h
    exact Bool.noConfusion h.2.2

/-- Validation/acceptance remains an explicit context, separate from attribution. -/
def Accepted (ctx : Bit) : Prop :=
  ctx = true

theorem false_not_accepted : ¬ Accepted false := by
  intro h
  exact Bool.noConfusion h

theorem true_accepted : Accepted true := by
  rfl

theorem attributionAndAcceptanceAreOrthogonal :
    Attributable sensitiveModel outwardView ∧
    ¬ Accepted false ∧
    Accepted true := by
  exact ⟨sensitive_outward_attributable,
    false_not_accepted,
    true_accepted⟩

/--
A decorative Action flag can vary while the lower-level attribution result is
unchanged.  The flag is not consulted by Attributable.
-/
structure DecoratedModel where
  base : OutwardResponseModel
  actionFlag : Bit

def decoratedTrue : DecoratedModel where
  base := sensitiveModel
  actionFlag := true

def decoratedFalse : DecoratedModel where
  base := sensitiveModel
  actionFlag := false

theorem actionLabelDeletionControl :
    Attributable decoratedTrue.base outwardView ↔
    Attributable decoratedFalse.base outwardView := by
  rfl

end OperationalActionCountermodel

end RelayTheory
