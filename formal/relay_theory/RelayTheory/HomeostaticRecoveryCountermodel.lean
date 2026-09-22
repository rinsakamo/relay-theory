namespace RelayTheory

namespace HomeostaticRecoveryCountermodel

abbrev Bit := Bool
abbrev State := Bool
abbrev Perturbation := Bool
abbrev Criterion := State → Prop

def acceptTrue : Criterion :=
  fun state => state = true

def acceptAny : Criterion :=
  fun _ => True

/--
Two explicitly ordered response stages:
1. state immediately after the perturbation;
2. state after a later response.
No Homeostasis/Recovery classification field is present.
-/
structure RecoveryProfile where
  actualBaseline : State
  postPerturb : Perturbation → State
  postResponse : Perturbation → State

/-- Never leaves the acceptable region in the tested surface. -/
def preventiveProfile : RecoveryProfile where
  actualBaseline := true
  postPerturb _ := true
  postResponse _ := true

/--
Leaves the acceptable region under the non-baseline perturbation and later
returns to it.
-/
def recoveryProfile : RecoveryProfile where
  actualBaseline := true
  postPerturb perturbation := if perturbation then false else true
  postResponse _ := true

/--
Leaves the acceptable region under the non-baseline perturbation and remains
outside it after the later response.
-/
def failingProfile : RecoveryProfile where
  actualBaseline := true
  postPerturb perturbation := if perturbation then false else true
  postResponse perturbation := if perturbation then false else true

def ImmediateRobust
    (acceptable : Criterion)
    (profile : RecoveryProfile) : Prop :=
  ∀ perturbation : Perturbation,
    acceptable (profile.postPerturb perturbation)

def FinalRobust
    (acceptable : Criterion)
    (profile : RecoveryProfile) : Prop :=
  ∀ perturbation : Perturbation,
    acceptable (profile.postResponse perturbation)

/--
Operational active recovery:
for at least one perturbation, the ordered path goes from outside the declared
acceptable region immediately after perturbation to inside it after response.
-/
def ActiveRecovery
    (acceptable : Criterion)
    (profile : RecoveryProfile) : Prop :=
  ∃ perturbation : Perturbation,
    ¬ acceptable (profile.postPerturb perturbation) ∧
    acceptable (profile.postResponse perturbation)

theorem allProfiles_sameActualBaseline :
    preventiveProfile.actualBaseline = recoveryProfile.actualBaseline ∧
    preventiveProfile.actualBaseline = failingProfile.actualBaseline := by
  exact ⟨rfl, rfl⟩

theorem preventive_immediateRobust :
    ImmediateRobust acceptTrue preventiveProfile := by
  intro perturbation
  rfl

theorem preventive_finalRobust :
    FinalRobust acceptTrue preventiveProfile := by
  intro perturbation
  rfl

theorem preventive_not_activeRecovery :
    ¬ ActiveRecovery acceptTrue preventiveProfile := by
  intro h
  rcases h with ⟨perturbation, outside, inside⟩
  exact outside rfl

theorem recovery_not_immediateRobust :
    ¬ ImmediateRobust acceptTrue recoveryProfile := by
  intro h
  have bad := h true
  exact Bool.noConfusion bad

theorem recovery_finalRobust :
    FinalRobust acceptTrue recoveryProfile := by
  intro perturbation
  rfl

theorem recovery_activeRecovery :
    ActiveRecovery acceptTrue recoveryProfile := by
  refine ⟨true, ?_, ?_⟩
  · intro h
    exact Bool.noConfusion h
  · rfl

theorem failing_not_immediateRobust :
    ¬ ImmediateRobust acceptTrue failingProfile := by
  intro h
  have bad := h true
  exact Bool.noConfusion bad

theorem failing_not_finalRobust :
    ¬ FinalRobust acceptTrue failingProfile := by
  intro h
  have bad := h true
  exact Bool.noConfusion bad

theorem failing_not_activeRecovery :
    ¬ ActiveRecovery acceptTrue failingProfile := by
  intro h
  rcases h with ⟨perturbation, outside, inside⟩
  cases perturbation with
  | false =>
      exact outside rfl
  | true =>
      exact Bool.noConfusion inside

/--
Preventive robustness and active recovery are not the same operational role.
-/
theorem preventiveRobustness_withoutActiveRecovery :
    ImmediateRobust acceptTrue preventiveProfile ∧
    FinalRobust acceptTrue preventiveProfile ∧
    ¬ ActiveRecovery acceptTrue preventiveProfile := by
  exact ⟨
    preventive_immediateRobust,
    preventive_finalRobust,
    preventive_not_activeRecovery
  ⟩

/--
Active recovery can occur even when the immediate post-perturbation state is
not robust.
-/
theorem activeRecovery_withoutImmediateRobustness :
    ¬ ImmediateRobust acceptTrue recoveryProfile ∧
    FinalRobust acceptTrue recoveryProfile ∧
    ActiveRecovery acceptTrue recoveryProfile := by
  exact ⟨
    recovery_not_immediateRobust,
    recovery_finalRobust,
    recovery_activeRecovery
  ⟩

/--
Two systems can have the same final viability/robustness result while differing
in whether an outside-to-inside recovery path occurred.
-/
theorem sameFinalRobustness_differentRecoveryPath :
    FinalRobust acceptTrue preventiveProfile ∧
    FinalRobust acceptTrue recoveryProfile ∧
    ¬ ActiveRecovery acceptTrue preventiveProfile ∧
    ActiveRecovery acceptTrue recoveryProfile := by
  exact ⟨
    preventive_finalRobust,
    recovery_finalRobust,
    preventive_not_activeRecovery,
    recovery_activeRecovery
  ⟩

/--
The two relevant systems also share the same designated baseline path.
-/
theorem sameBaselinePath_preventive_recovery :
    preventiveProfile.actualBaseline = recoveryProfile.actualBaseline ∧
    preventiveProfile.postPerturb false = recoveryProfile.postPerturb false ∧
    preventiveProfile.postResponse false = recoveryProfile.postResponse false := by
  exact ⟨rfl, rfl, rfl⟩

/--
The exact same two-stage transition surface changes recovery classification when
the declared acceptable-state criterion changes.
-/
theorem activeRecovery_isCriterionRelative :
    ActiveRecovery acceptTrue recoveryProfile ∧
    ¬ ActiveRecovery acceptAny recoveryProfile := by
  constructor
  · exact recovery_activeRecovery
  · intro h
    rcases h with ⟨perturbation, outside, inside⟩
    exact outside True.intro

structure DecoratedProfile where
  base : RecoveryProfile
  homeostasisFlag : Bit

def decoratedTrue : DecoratedProfile where
  base := recoveryProfile
  homeostasisFlag := true

def decoratedFalse : DecoratedProfile where
  base := recoveryProfile
  homeostasisFlag := false

theorem homeostasisLabelDeletion_activeRecovery :
    ActiveRecovery acceptTrue decoratedTrue.base ↔
    ActiveRecovery acceptTrue decoratedFalse.base := by
  rfl

theorem homeostasisLabelDeletion_finalRobustness :
    FinalRobust acceptTrue decoratedTrue.base ↔
    FinalRobust acceptTrue decoratedFalse.base := by
  rfl

/--
Combined scoped result:
- preventive robustness does not imply active recovery;
- active recovery does not imply immediate robustness;
- equal final robustness does not identify path history;
- a failing path supplies no restoration witness;
- recovery classification is criterion-relative;
- a decorative Homeostasis label adds no information.
-/
theorem activeRecoverySeparation_bundle :
    ImmediateRobust acceptTrue preventiveProfile ∧
    ¬ ActiveRecovery acceptTrue preventiveProfile ∧
    ¬ ImmediateRobust acceptTrue recoveryProfile ∧
    FinalRobust acceptTrue recoveryProfile ∧
    ActiveRecovery acceptTrue recoveryProfile ∧
    ¬ FinalRobust acceptTrue failingProfile ∧
    ¬ ActiveRecovery acceptTrue failingProfile := by
  exact ⟨
    preventive_immediateRobust,
    preventive_not_activeRecovery,
    recovery_not_immediateRobust,
    recovery_finalRobust,
    recovery_activeRecovery,
    failing_not_finalRobust,
    failing_not_activeRecovery
  ⟩

end HomeostaticRecoveryCountermodel

end RelayTheory
