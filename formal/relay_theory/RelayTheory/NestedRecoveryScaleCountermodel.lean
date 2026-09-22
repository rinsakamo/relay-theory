import RelayTheory.NestedCandidateScaleCountermodel
import RelayTheory.HomeostaticRecoveryCountermodel

namespace RelayTheory

namespace NestedRecoveryScaleCountermodel

/-!
This finite module tests the #116 bridge from validated active recovery to
nested candidate-scale selection.

One ambient two-stage trajectory is projected onto the two properly nested
candidate loci already validated by #113. The outer projection genuinely
depends on an additional shell coordinate.

The tested result is only that active recovery plus functional integration and
final criterion-relative robustness do not force a unique nested candidate
scale.
-/

abbrev AmbientState := Bool × Bool
abbrev Perturbation := Bool

def projectCandidate :
    NestedCandidateScaleCountermodel.CandidateKey →
      AmbientState →
      Bool
  | .inner, state => state.1
  | .outer, state => state.1 && state.2

def ambientBaseline : AmbientState :=
  (true, true)

def ambientPostPerturb : Perturbation → AmbientState
  | false => (true, true)
  | true => (false, false)

def ambientPostResponse : Perturbation → AmbientState
  | _ => (true, true)

/--
Each candidate recovery profile is derived by projection from the same ambient
trajectory. No candidate-local recovery table is supplied.
-/
def projectedProfile
    (k : NestedCandidateScaleCountermodel.CandidateKey) :
    HomeostaticRecoveryCountermodel.RecoveryProfile where
  actualBaseline := projectCandidate k ambientBaseline
  postPerturb perturbation :=
    projectCandidate k (ambientPostPerturb perturbation)
  postResponse perturbation :=
    projectCandidate k (ambientPostResponse perturbation)

theorem innerShellInsensitive :
    projectCandidate .inner (true, false) =
      projectCandidate .inner (true, true) := by
  rfl

theorem outerShellSensitive :
    projectCandidate .outer (true, false) ≠
      projectCandidate .outer (true, true) := by
  intro h
  exact Bool.noConfusion h

theorem sharedAmbientRecoveryPath :
    ambientPostPerturb true = (false, false) ∧
    ambientPostResponse true = (true, true) := by
  exact ⟨rfl, rfl⟩

theorem innerFinalRobust :
    HomeostaticRecoveryCountermodel.FinalRobust
      HomeostaticRecoveryCountermodel.acceptTrue
      (projectedProfile .inner) := by
  intro perturbation
  cases perturbation <;> rfl

theorem outerFinalRobust :
    HomeostaticRecoveryCountermodel.FinalRobust
      HomeostaticRecoveryCountermodel.acceptTrue
      (projectedProfile .outer) := by
  intro perturbation
  cases perturbation <;> rfl

theorem innerActiveRecovery :
    HomeostaticRecoveryCountermodel.ActiveRecovery
      HomeostaticRecoveryCountermodel.acceptTrue
      (projectedProfile .inner) := by
  refine ⟨true, ?_, ?_⟩
  · intro h
    exact Bool.noConfusion h
  · rfl

theorem outerActiveRecovery :
    HomeostaticRecoveryCountermodel.ActiveRecovery
      HomeostaticRecoveryCountermodel.acceptTrue
      (projectedProfile .outer) := by
  refine ⟨true, ?_, ?_⟩
  · intro h
    exact Bool.noConfusion h
  · rfl

def RecoveryQualified
    (k : NestedCandidateScaleCountermodel.CandidateKey) : Prop :=
  NestedCandidateScaleCountermodel.Integrated k ∧
  HomeostaticRecoveryCountermodel.FinalRobust
    HomeostaticRecoveryCountermodel.acceptTrue
    (projectedProfile k) ∧
  HomeostaticRecoveryCountermodel.ActiveRecovery
    HomeostaticRecoveryCountermodel.acceptTrue
    (projectedProfile k)

theorem innerRecoveryQualified :
    RecoveryQualified .inner := by
  exact ⟨
    NestedCandidateScaleCountermodel.innerIntegrated,
    innerFinalRobust,
    innerActiveRecovery
  ⟩

theorem outerRecoveryQualified :
    RecoveryQualified .outer := by
  exact ⟨
    NestedCandidateScaleCountermodel.outerIntegrated,
    outerFinalRobust,
    outerActiveRecovery
  ⟩

def UniqueRecoveryQualifier : Prop :=
  ∃ winner : NestedCandidateScaleCountermodel.CandidateKey,
    RecoveryQualified winner ∧
    ∀ other : NestedCandidateScaleCountermodel.CandidateKey,
      RecoveryQualified other → other = winner

theorem noUniqueRecoveryQualifier :
    ¬ UniqueRecoveryQualifier := by
  intro h
  rcases h with ⟨winner, hwinner, hunique⟩
  have hInner : NestedCandidateScaleCountermodel.CandidateKey.inner = winner :=
    hunique .inner innerRecoveryQualified
  have hOuter : NestedCandidateScaleCountermodel.CandidateKey.outer = winner :=
    hunique .outer outerRecoveryQualified
  exact NestedCandidateScaleCountermodel.inner_ne_outer
    (hInner.trans hOuter.symm)

/--
Finite witness that one ambient recovery trajectory supports two distinct,
properly nested, recovery-qualified candidates.
-/
theorem nestedRecoveryQualifiers :
    ∃ k₁ k₂ : NestedCandidateScaleCountermodel.CandidateKey,
      k₁ ≠ k₂ ∧
      NestedCandidateScaleCountermodel.ProperlyNested
        (NestedCandidateScaleCountermodel.member k₁)
        (NestedCandidateScaleCountermodel.member k₂) ∧
      RecoveryQualified k₁ ∧
      RecoveryQualified k₂ := by
  exact ⟨
    .inner,
    .outer,
    NestedCandidateScaleCountermodel.inner_ne_outer,
    NestedCandidateScaleCountermodel.innerProperlyNestedOuter,
    innerRecoveryQualified,
    outerRecoveryQualified
  ⟩

theorem recoveryClassificationSelectionSplit :
    RecoveryQualified .inner ∧
    RecoveryQualified .outer ∧
    ¬ UniqueRecoveryQualifier := by
  exact ⟨
    innerRecoveryQualified,
    outerRecoveryQualified,
    noUniqueRecoveryQualifier
  ⟩

end NestedRecoveryScaleCountermodel

end RelayTheory
