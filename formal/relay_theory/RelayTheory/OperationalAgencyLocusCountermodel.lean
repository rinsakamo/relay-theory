namespace RelayTheory

namespace OperationalAgencyLocusCountermodel

abbrev Bit := Bool

/--
Raw response families relative to an already supplied focal locus.
No Self, Action, Perception, or Cognition classification field is present.
-/
structure FocalResponseProfile where
  inwardUnderExterior : Bit → Bit
  internalUnderSource : Bit → Bit
  downstreamUnderIntermediate : Bit → Bit
  outwardUnderSource : Bit → Bit

def fullyResponsive : FocalResponseProfile where
  inwardUnderExterior x := x
  internalUnderSource x := x
  downstreamUnderIntermediate x := x
  outwardUnderSource x := x

def inertProfile : FocalResponseProfile where
  inwardUnderExterior _ := false
  internalUnderSource _ := false
  downstreamUnderIntermediate _ := false
  outwardUnderSource _ := false

def missingOutward : FocalResponseProfile where
  inwardUnderExterior x := x
  internalUnderSource x := x
  downstreamUnderIntermediate x := x
  outwardUnderSource _ := false

def Sensitive (f : Bit → Bit) : Prop :=
  f false ≠ f true

def OperationalAgencyLocus (p : FocalResponseProfile) : Prop :=
  Sensitive p.inwardUnderExterior ∧
  Sensitive p.internalUnderSource ∧
  Sensitive p.downstreamUnderIntermediate ∧
  Sensitive p.outwardUnderSource

theorem identitySensitive : Sensitive (fun x : Bit => x) := by
  intro h
  exact Bool.noConfusion h

theorem constantFalseNotSensitive : ¬ Sensitive (fun _ : Bit => false) := by
  intro h
  exact h rfl

theorem fullyResponsive_isOperationalAgencyLocus :
    OperationalAgencyLocus fullyResponsive := by
  exact ⟨identitySensitive, identitySensitive, identitySensitive, identitySensitive⟩

theorem inertProfile_notOperationalAgencyLocus :
    ¬ OperationalAgencyLocus inertProfile := by
  intro h
  exact constantFalseNotSensitive h.1

theorem missingOutward_notOperationalAgencyLocus :
    ¬ OperationalAgencyLocus missingOutward := by
  intro h
  exact constantFalseNotSensitive h.2.2.2

/--
A focal region can be evaluated without a prior eligibility gate. Missing raw
response structure makes the operational profile fail directly.
-/
theorem noPrequalificationNeededForInertControl :
    ¬ OperationalAgencyLocus inertProfile := by
  exact inertProfile_notOperationalAgencyLocus

structure DecoratedProfile where
  base : FocalResponseProfile
  selfFlag : Bit

def decoratedSelfTrue : DecoratedProfile where
  base := fullyResponsive
  selfFlag := true

def decoratedSelfFalse : DecoratedProfile where
  base := fullyResponsive
  selfFlag := false

theorem selfLabelDeletionControl :
    OperationalAgencyLocus decoratedSelfTrue.base ↔
    OperationalAgencyLocus decoratedSelfFalse.base := by
  rfl

/--
The operational profile is exactly a conjunction of raw response-sensitivity
facts; no high-level agency labels are required as ingredients.
-/
theorem operationalProfile_expandsToRawResponses
    (p : FocalResponseProfile) :
    OperationalAgencyLocus p ↔
      Sensitive p.inwardUnderExterior ∧
      Sensitive p.internalUnderSource ∧
      Sensitive p.downstreamUnderIntermediate ∧
      Sensitive p.outwardUnderSource := by
  rfl

end OperationalAgencyLocusCountermodel

end RelayTheory
