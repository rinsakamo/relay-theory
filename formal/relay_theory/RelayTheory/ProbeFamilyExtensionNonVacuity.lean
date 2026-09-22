namespace RelayTheory

namespace ProbeFamilyExtensionNonVacuity

/--
A minimal case surface with one source-grounded observation and one external
target field. The target is deliberately unavailable to the grounded probe
family below.
-/
structure Case where
  observation : Bool
  target : Bool
deriving DecidableEq

/--
The original declared probe family contains only the source-grounded
observation probe.
-/
inductive GroundedProbe
  | observe
deriving DecidableEq

def runGrounded
    (probe : GroundedProbe)
    (c : Case) : Bool :=
  match probe with
  | .observe => c.observation

def GroundedDistinguishable
    (a b : Case) : Prop :=
  ∃ probe : GroundedProbe,
    runGrounded probe a ≠ runGrounded probe b

/--
An extended probe family used only for the post-hoc control.

The revealTarget probe is explicitly synthetic: it exposes information that was
not available on the original declared probe surface.
-/
inductive ExtendedProbe
  | observe
  | revealTarget
deriving DecidableEq

def runExtended
    (probe : ExtendedProbe)
    (c : Case) : Bool :=
  match probe with
  | .observe => c.observation
  | .revealTarget => c.target

def ExtendedDistinguishable
    (a b : Case) : Prop :=
  ∃ probe : ExtendedProbe,
    runExtended probe a ≠ runExtended probe b

/--
Matched cases: identical grounded observation, opposite external targets.
-/
def matchedFalse : Case where
  observation := false
  target := false

def matchedTrue : Case where
  observation := false
  target := true

theorem groundedObservationsAgree :
    matchedFalse.observation = matchedTrue.observation := by
  rfl

/--
The original source-grounded probe family cannot distinguish the matched cases.
-/
theorem fixedGroundedProbeFamilyDoesNotDistinguish :
    ¬ GroundedDistinguishable matchedFalse matchedTrue := by
  intro h
  rcases h with ⟨probe, hprobe⟩
  cases probe
  exact hprobe rfl

/--
A synthetic target-revealing probe makes the same matched cases distinguishable
under the explicitly extended family.
-/
theorem extendedProbeFamilyDistinguishes :
    ExtendedDistinguishable matchedFalse matchedTrue := by
  refine ⟨ExtendedProbe.revealTarget, ?_⟩
  decide

/--
Compact contrast: the distinction is absent under the original declared probe
family and present only after a synthetic extension.
-/
theorem posthocProbeExtensionCreatesDistinction :
    (¬ GroundedDistinguishable matchedFalse matchedTrue) ∧
      ExtendedDistinguishable matchedFalse matchedTrue := by
  exact ⟨
    fixedGroundedProbeFamilyDoesNotDistinguish,
    extendedProbeFamilyDistinguishes
  ⟩

/--
The grounded observation remains non-discriminating even when represented
inside the extended family. The new distinction comes specifically from the new
probe, not from reinterpretation of the old observation.
-/
theorem extendedObserveStillAgrees :
    runExtended ExtendedProbe.observe matchedFalse =
      runExtended ExtendedProbe.observe matchedTrue := by
  rfl

end ProbeFamilyExtensionNonVacuity

end RelayTheory
