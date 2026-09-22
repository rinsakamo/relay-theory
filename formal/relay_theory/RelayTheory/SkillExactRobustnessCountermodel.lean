namespace RelayTheory

namespace SkillExactRobustnessCountermodel

abbrev Bit := Bool
abbrev Context := Bit
abbrev Variation := Bit
abbrev Response := Bit
abbrev Profile := Context → Variation → Response
abbrev SuccessCriterion := Context → Response → Prop

def nominalVariation : Variation := false

def robustProfile : Profile :=
  fun c _ => c

def brittleProfile : Profile :=
  fun c v => if v then false else c

def identitySuccess : SuccessCriterion :=
  fun c r => r = c

def NominalCompetent
    (success : SuccessCriterion)
    (profile : Profile) : Prop :=
  ∀ c : Context, success c (profile c nominalVariation)

def ExactRobust
    (success : SuccessCriterion)
    (profile : Profile) : Prop :=
  ∀ c : Context, ∀ v : Variation, success c (profile c v)

theorem sameNominalMapping :
    ∀ c : Context,
      robustProfile c nominalVariation =
      brittleProfile c nominalVariation := by
  intro c
  simp [robustProfile, brittleProfile, nominalVariation]

theorem robustProfile_nominalCompetent :
    NominalCompetent identitySuccess robustProfile := by
  intro c
  rfl

theorem brittleProfile_nominalCompetent :
    NominalCompetent identitySuccess brittleProfile := by
  intro c
  simp [identitySuccess, brittleProfile, nominalVariation]

theorem robustProfile_exactRobust :
    ExactRobust identitySuccess robustProfile := by
  intro c v
  rfl

theorem brittleProfile_not_exactRobust :
    ¬ ExactRobust identitySuccess brittleProfile := by
  intro h
  have bad := h true true
  exact Bool.noConfusion bad

theorem nominalCompetence_doesNotDetermineExactRobustness :
    NominalCompetent identitySuccess robustProfile ∧
    NominalCompetent identitySuccess brittleProfile ∧
    ExactRobust identitySuccess robustProfile ∧
    ¬ ExactRobust identitySuccess brittleProfile := by
  exact ⟨robustProfile_nominalCompetent,
    brittleProfile_nominalCompetent,
    robustProfile_exactRobust,
    brittleProfile_not_exactRobust⟩

abbrev ExpandedContext := Context × Variation
abbrev ExpandedPolicy := ExpandedContext → Response
abbrev ExpandedSuccessCriterion := ExpandedContext → Response → Prop

def asExpandedPolicy (profile : Profile) : ExpandedPolicy :=
  fun cv => profile cv.1 cv.2

def liftSuccess
    (success : SuccessCriterion) : ExpandedSuccessCriterion :=
  fun cv r => success cv.1 r

def ExpandedCompetent
    (success : ExpandedSuccessCriterion)
    (policy : ExpandedPolicy) : Prop :=
  ∀ k : ExpandedContext, success k (policy k)

theorem exactRobustness_iff_expandedCompetence
    (success : SuccessCriterion)
    (profile : Profile) :
    ExactRobust success profile ↔
      ExpandedCompetent
        (liftSuccess success)
        (asExpandedPolicy profile) := by
  constructor
  · intro h k
    exact h k.1 k.2
  · intro h c v
    exact h (c, v)

theorem extensionalProfilesPreserveExactRobustness
    (success : SuccessCriterion)
    (f g : Profile)
    (hEq : ∀ c : Context, ∀ v : Variation, f c v = g c v) :
    ExactRobust success f ↔ ExactRobust success g := by
  constructor
  · intro hf c v
    rw [← hEq c v]
    exact hf c v
  · intro hg c v
    rw [hEq c v]
    exact hg c v

structure DecoratedProfile where
  profile : Profile
  robustnessFlag : Bit

def decoratedTrue : DecoratedProfile where
  profile := robustProfile
  robustnessFlag := true

def decoratedFalse : DecoratedProfile where
  profile := robustProfile
  robustnessFlag := false

theorem robustnessLabelDeletionControl :
    ExactRobust identitySuccess decoratedTrue.profile ↔
    ExactRobust identitySuccess decoratedFalse.profile := by
  rfl

end SkillExactRobustnessCountermodel

end RelayTheory
