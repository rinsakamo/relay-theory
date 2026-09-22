import RelayTheory.RetainedFormationSeparation

namespace RelayTheory
namespace ReconstructionProvenanceSeparation

abbrev Experience := RetainedFormationSeparation.Experience
abbrev RetainedState := RetainedFormationSeparation.RetainedState
abbrev Formation := RetainedFormationSeparation.Formation
abbrev Readout := RetainedFormationSeparation.Readout

def actualExperience : Experience :=
  RetainedFormationSeparation.actualExperience

def identityReadout : Readout :=
  RetainedFormationSeparation.currentReadout

def constantFormation : Formation :=
  RetainedFormationSeparation.experienceInsensitive

def identityFormation : Formation :=
  RetainedFormationSeparation.experienceSensitive

def invertedFormation : Formation :=
  fun experience => !experience

def ReconstructsActual
    (formation : Formation)
    (readout : Readout) : Prop :=
  readout (formation actualExperience) = actualExperience

def SensitiveAtActual (formation : Formation) : Prop :=
  ∃ alternative : Experience,
    alternative ≠ actualExperience ∧
    formation alternative ≠ formation actualExperience

theorem sensitiveAtActual_implies_experienceDependent
    (formation : Formation)
    (h : SensitiveAtActual formation) :
    RetainedFormationSeparation.ExperienceDependent formation := by
  rcases h with ⟨alternative, _, hdiff⟩
  exact ⟨alternative, actualExperience, hdiff⟩

theorem constant_reconstructsActual :
    ReconstructsActual constantFormation identityReadout := by
  rfl

theorem constant_not_sensitiveAtActual :
    ¬ SensitiveAtActual constantFormation := by
  intro h
  rcases h with ⟨alternative, _, hdiff⟩
  exact hdiff rfl

theorem inverted_sensitiveAtActual :
    SensitiveAtActual invertedFormation := by
  exact ⟨true, by decide, by decide⟩

theorem inverted_not_reconstructsActual :
    ¬ ReconstructsActual invertedFormation identityReadout := by
  intro h
  change true = false at h
  exact Bool.noConfusion h

theorem identity_reconstructsActual :
    ReconstructsActual identityFormation identityReadout := by
  rfl

theorem identity_sensitiveAtActual :
    SensitiveAtActual identityFormation := by
  exact ⟨true, by decide, by decide⟩

theorem reconstruction_without_formationSensitivity :
    ReconstructsActual constantFormation identityReadout ∧
    ¬ SensitiveAtActual constantFormation := by
  exact ⟨constant_reconstructsActual, constant_not_sensitiveAtActual⟩

theorem formationSensitivity_without_reconstruction :
    SensitiveAtActual invertedFormation ∧
    ¬ ReconstructsActual invertedFormation identityReadout := by
  exact ⟨inverted_sensitiveAtActual, inverted_not_reconstructsActual⟩

theorem reconstruction_provenance_separation_bundle :
    (ReconstructsActual constantFormation identityReadout ∧
      ¬ SensitiveAtActual constantFormation) ∧
    (SensitiveAtActual invertedFormation ∧
      ¬ ReconstructsActual invertedFormation identityReadout) ∧
    (ReconstructsActual identityFormation identityReadout ∧
      SensitiveAtActual identityFormation) := by
  exact ⟨
    reconstruction_without_formationSensitivity,
    formationSensitivity_without_reconstruction,
    identity_reconstructsActual,
    identity_sensitiveAtActual
  ⟩

end ReconstructionProvenanceSeparation
end RelayTheory
