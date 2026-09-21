namespace RelayTheory

namespace InterventionCountermodel

abbrev Bit := Bool
abbrev Observation := Bit × Bit
abbrev ObservationalSignature := Observation × Observation

structure BinaryMechanismModel where
  observe : Bit → Observation
  doXFalse : Bit → Observation

def modelA : BinaryMechanismModel where
  observe u := (u, u)
  doXFalse _ := (false, false)

def modelB : BinaryMechanismModel where
  observe u := (u, u)
  doXFalse u := (false, u)

def observationalSignature (m : BinaryMechanismModel) : ObservationalSignature :=
  (m.observe false, m.observe true)

theorem sameObservationalSignature :
    observationalSignature modelA = observationalSignature modelB := by
  rfl

theorem differentInterventionResponse :
    modelA.doXFalse true ≠ modelB.doXFalse true := by
  decide

theorem observationalSignatureDoesNotDetermineIntervention :
    ∃ a b : BinaryMechanismModel,
      observationalSignature a = observationalSignature b ∧
      a.doXFalse true ≠ b.doXFalse true := by
  exact ⟨modelA, modelB, sameObservationalSignature, differentInterventionResponse⟩

theorem noRecoveryFromObservationalSignature
    (recover : ObservationalSignature → Observation)
    (hA : recover (observationalSignature modelA) = modelA.doXFalse true)
    (hB : recover (observationalSignature modelB) = modelB.doXFalse true) :
    False := by
  have h : modelA.doXFalse true = modelB.doXFalse true := by
    calc
      modelA.doXFalse true = recover (observationalSignature modelA) := hA.symm
      _ = recover (observationalSignature modelB) := by
        rw [sameObservationalSignature]
      _ = modelB.doXFalse true := hB
  exact differentInterventionResponse h

end InterventionCountermodel

end RelayTheory
