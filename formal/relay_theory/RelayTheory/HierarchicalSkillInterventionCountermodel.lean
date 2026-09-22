namespace RelayTheory

namespace HierarchicalSkillInterventionCountermodel

abbrev Bit := Bool
abbrev Context := Bit
abbrev Probe := Bit
abbrev Response := Bit
abbrev Policy := Context → Response
abbrev Profile := Context → Probe → Response
abbrev SuccessCriterion := Context → Response → Prop

def normalProbe : Probe := false

def changedProbe : Probe := true

def probeSensitive : Profile :=
  fun c p => if p then false else c

def probeInsensitive : Profile :=
  fun c _ => c

def ordinaryPolicy (profile : Profile) : Policy :=
  fun c => profile c normalProbe

def identitySuccess : SuccessCriterion :=
  fun c r => r = c

def Competent (success : SuccessCriterion) (policy : Policy) : Prop :=
  ∀ c : Context, success c (policy c)

def PerturbationSensitive (profile : Profile) : Prop :=
  profile true normalProbe ≠ profile true changedProbe

theorem sameOrdinaryMapping :
    ∀ c : Context,
      ordinaryPolicy probeSensitive c =
      ordinaryPolicy probeInsensitive c := by
  intro c
  simp [ordinaryPolicy, probeSensitive, probeInsensitive, normalProbe]

theorem probeSensitive_ordinaryCompetent :
    Competent identitySuccess (ordinaryPolicy probeSensitive) := by
  intro c
  simp [identitySuccess, ordinaryPolicy, probeSensitive, normalProbe]

theorem probeInsensitive_ordinaryCompetent :
    Competent identitySuccess (ordinaryPolicy probeInsensitive) := by
  intro c
  rfl

theorem sameOrdinaryCompetence :
    Competent identitySuccess (ordinaryPolicy probeSensitive) ∧
    Competent identitySuccess (ordinaryPolicy probeInsensitive) := by
  exact ⟨probeSensitive_ordinaryCompetent,
    probeInsensitive_ordinaryCompetent⟩

theorem changedProbeSeparates :
    probeSensitive true changedProbe ≠
    probeInsensitive true changedProbe := by
  simp [probeSensitive, probeInsensitive, changedProbe]

theorem probeSensitive_isPerturbationSensitive :
    PerturbationSensitive probeSensitive := by
  simp [PerturbationSensitive, probeSensitive, normalProbe, changedProbe]

theorem probeInsensitive_notPerturbationSensitive :
    ¬ PerturbationSensitive probeInsensitive := by
  simp [PerturbationSensitive, probeInsensitive, normalProbe, changedProbe]

theorem ordinaryEquality_doesNotDetermineFullProfileEquality :
    (∀ c : Context,
      ordinaryPolicy probeSensitive c =
      ordinaryPolicy probeInsensitive c) ∧
    ¬ (∀ c : Context, ∀ p : Probe,
      probeSensitive c p = probeInsensitive c p) := by
  constructor
  · exact sameOrdinaryMapping
  · intro h
    exact changedProbeSeparates (h true changedProbe)

theorem ordinaryCompetence_separatedByPerturbationResponse :
    Competent identitySuccess (ordinaryPolicy probeSensitive) ∧
    Competent identitySuccess (ordinaryPolicy probeInsensitive) ∧
    PerturbationSensitive probeSensitive ∧
    ¬ PerturbationSensitive probeInsensitive := by
  exact ⟨probeSensitive_ordinaryCompetent,
    probeInsensitive_ordinaryCompetent,
    probeSensitive_isPerturbationSensitive,
    probeInsensitive_notPerturbationSensitive⟩

theorem extensionalProfilesPreservePerturbationSensitivity
    (f g : Profile)
    (hEq : ∀ c : Context, ∀ p : Probe, f c p = g c p) :
    PerturbationSensitive f ↔ PerturbationSensitive g := by
  simp [PerturbationSensitive, hEq]

structure DecoratedProfile where
  profile : Profile
  hierarchyFlag : Bit

def decoratedHierarchy : DecoratedProfile where
  profile := probeSensitive
  hierarchyFlag := true

def decoratedFlat : DecoratedProfile where
  profile := probeSensitive
  hierarchyFlag := false

theorem hierarchyLabelDeletionControl :
    PerturbationSensitive decoratedHierarchy.profile ↔
    PerturbationSensitive decoratedFlat.profile := by
  rfl

end HierarchicalSkillInterventionCountermodel

end RelayTheory
