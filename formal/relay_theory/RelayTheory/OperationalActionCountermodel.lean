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
  decide

theorem fixedModel_not_sourceSensitive :
    ¬ SourceSensitive fixedModel := by
  decide

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

theorem matchedRealizedTrace_separatedByAttribution :
    realizedSignature sensitiveModel = realizedSignature fixedModel ∧
    Attributable sensitiveModel outwardView ∧
    ¬ Attributable fixedModel outwardView := by
  constructor
  · exact sameRealizedSignature
  constructor <;> decide

theorem focalReindexingChangesOutwardAttribution :
    Attributable sensitiveModel outwardView ∧
    ¬ Attributable sensitiveModel internalView := by
  constructor <;> decide

/-- Validation/acceptance remains an explicit context, separate from attribution. -/
def Accepted (ctx : Bit) : Prop :=
  ctx = true

theorem attributionAndAcceptanceAreOrthogonal :
    Attributable sensitiveModel outwardView ∧
    ¬ Accepted false ∧
    Accepted true := by
  constructor
  · decide
  constructor <;> decide

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
