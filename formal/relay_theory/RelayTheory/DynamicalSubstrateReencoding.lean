import RelayTheory.InterventionCountermodel

namespace RelayTheory

namespace DynamicalSubstrateReencoding

open InterventionCountermodel

/--
A semantics-free two-channel response profile.  The tuple positions carry no
RelayTheory ontology by themselves; any interpretation of the channels is
supplied by the surrounding model/evaluation context.
-/
abbrev GenericResponseProfile :=
  (Bit → Observation) × (Bit → Observation)

/-- Forget the field names of the #22 mechanism model without forgetting data. -/
def forgetNames (m : BinaryMechanismModel) : GenericResponseProfile :=
  (m.observe, m.doXFalse)

/-- Re-assign the #22 field names to a generic two-channel response profile. -/
def assignNames (p : GenericResponseProfile) : BinaryMechanismModel where
  observe := p.1
  doXFalse := p.2

theorem assignNames_forgetNames (m : BinaryMechanismModel) :
    assignNames (forgetNames m) = m := by
  cases m
  rfl

theorem forgetNames_assignNames (p : GenericResponseProfile) :
    forgetNames (assignNames p) = p := by
  cases p
  rfl

/--
The named #22 presentation and a generic two-channel response profile are
losslessly interconvertible.
-/
theorem namedAndGenericAreMutualInverses :
    (∀ m : BinaryMechanismModel, assignNames (forgetNames m) = m) ∧
    (∀ p : GenericResponseProfile, forgetNames (assignNames p) = p) := by
  constructor
  · exact assignNames_forgetNames
  · exact forgetNames_assignNames

/--
The independent-information witness from #22 survives after the semantic field
names are erased: the first response channels agree, while the second channels
differ on the selected input.
-/
theorem interventionGapSurvivesGenericEncoding :
    (forgetNames modelA).1 = (forgetNames modelB).1 ∧
    (forgetNames modelA).2 true ≠ (forgetNames modelB).2 true := by
  constructor
  · rfl
  · exact differentInterventionResponse

/--
Any predicate stated over the named #22 model presentation can be transported
without loss to the generic response profile.
-/
def genericize (P : BinaryMechanismModel → Prop) :
    GenericResponseProfile → Prop :=
  fun p => P (assignNames p)

theorem predicateFactorsThroughGenericProfile
    (P : BinaryMechanismModel → Prop)
    (m : BinaryMechanismModel) :
    P m ↔ genericize P (forgetNames m) := by
  cases m
  rfl

end DynamicalSubstrateReencoding

end RelayTheory
