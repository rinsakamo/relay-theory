import RelayTheory.OperationalSkillCountermodel

namespace RelayTheory
namespace RetainedFormationSeparation

abbrev Experience := Bool
abbrev RetainedState := Bool
abbrev Formation := Experience → RetainedState
abbrev Readout := RetainedState → Bool

/--
A formation map whose retained state varies with the supplied experience.
No Memory / Skill / Crystal classification is encoded in this map.
-/
def experienceSensitive : Formation :=
  fun experience => experience

/--
A formation map whose retained state is constant across the supplied
experience coordinate.
-/
def experienceInsensitive : Formation :=
  fun _ => false

def actualExperience : Experience := false

def currentReadout : Readout :=
  fun state => state

/--
The actual final retained state is identical in the matched pair.
-/
theorem sameActualRetainedState :
    experienceSensitive actualExperience =
      experienceInsensitive actualExperience := by
  rfl

/--
The same current readout therefore also agrees in the matched pair.
-/
theorem sameActualCurrentReadout :
    currentReadout (experienceSensitive actualExperience) =
      currentReadout (experienceInsensitive actualExperience) := by
  rfl

/--
A counterfactual change of experience separates the formation maps.
-/
theorem counterfactualExperienceSeparatesFormation :
    experienceSensitive true ≠ experienceInsensitive true := by
  decide

/--
A neutral dependence predicate: some two experience values yield different
retained states.
-/
def ExperienceDependent (formation : Formation) : Prop :=
  ∃ e₁ e₂, formation e₁ ≠ formation e₂

theorem sensitive_isExperienceDependent :
    ExperienceDependent experienceSensitive := by
  exact ⟨false, true, by decide⟩

theorem insensitive_notExperienceDependent :
    ¬ ExperienceDependent experienceInsensitive := by
  intro h
  rcases h with ⟨e₁, e₂, hne⟩
  exact hne rfl

/--
Identical actual retained state and identical current readout do not determine
whether the retained state is counterfactually sensitive to prior experience.
-/
theorem sameFinalState_doesNotDetermineFormationDependence :
    experienceSensitive actualExperience =
        experienceInsensitive actualExperience ∧
    currentReadout (experienceSensitive actualExperience) =
        currentReadout (experienceInsensitive actualExperience) ∧
    ExperienceDependent experienceSensitive ∧
    ¬ ExperienceDependent experienceInsensitive := by
  exact ⟨
    sameActualRetainedState,
    sameActualCurrentReadout,
    sensitive_isExperienceDependent,
    insensitive_notExperienceDependent
  ⟩

/--
A minimal product system used only to test whether #41 task-relative
competence logically requires experience-sensitive retained-state formation.
-/
structure System where
  formation : Formation
  policy : OperationalSkillCountermodel.Policy

def competentWithoutExperienceDependentFormation : System where
  formation := experienceInsensitive
  policy := OperationalSkillCountermodel.generalPolicy

/--
The already-forged #41 competent policy can coexist with a formation map that
is not experience-dependent. Thus operational competence alone does not
establish experience-driven formation in this finite product model.
-/
theorem competenceDoesNotRequireExperienceDependentFormation :
    OperationalSkillCountermodel.Competent
        OperationalSkillCountermodel.identitySuccess
        competentWithoutExperienceDependentFormation.policy ∧
    ¬ ExperienceDependent
        competentWithoutExperienceDependentFormation.formation := by
  exact ⟨
    OperationalSkillCountermodel.generalPolicy_competent_identityTask,
    insensitive_notExperienceDependent
  ⟩

end RetainedFormationSeparation
end RelayTheory
