namespace RelayTheory

namespace NonVacuityBasisWitness

/--
A minimal source-grounded input surface.

The observation field is intentionally nondiscriminating in the matched examples.
The discriminator field represents one independently admitted distinction.
Neither field carries a cognitive construct label.
-/
structure GroundedInput where
  observation : Bool
  discriminator : Bool
deriving DecidableEq

/--
A target classification is kept outside the grounded input surface.

This separation is the point of the control: a reconstruction function may read
only GroundedInput. It may not inspect target directly.
-/
structure Case where
  grounded : GroundedInput
  target : Bool

/-- A reconstruction function correctly classifies one case. -/
def Reconstructs
    (derive : GroundedInput → Bool)
    (c : Case) : Prop :=
  derive c.grounded = c.target

/--
Any basis-derived classification is extensional in the admitted grounded input.
-/
theorem groundedExtensionality
    (derive : GroundedInput → Bool)
    (a b : GroundedInput)
    (h : a = b) :
    derive a = derive b := by
  exact congrArg derive h

/--
If two cases expose exactly the same grounded input but require different target
labels, no single reconstruction function over the grounded surface can recover
both labels.

The theorem forbids the reconstruction function from consulting target-only
information by type: its domain is GroundedInput, not Case.
-/
theorem sameGrounded_differentTarget_notReconstructible
    (a b : Case)
    (hground : a.grounded = b.grounded)
    (htarget : a.target ≠ b.target) :
    ¬ ∃ derive : GroundedInput → Bool,
        Reconstructs derive a ∧ Reconstructs derive b := by
  rintro ⟨derive, ha, hb⟩
  apply htarget
  calc
    a.target = derive a.grounded := ha.symm
    _ = derive b.grounded := by rw [hground]
    _ = b.target := hb

/-- Identical grounded evidence for the negative control. -/
def nullGrounded : GroundedInput where
  observation := false
  discriminator := false

/-- Negative-control row with target false. -/
def nullCaseFalse : Case where
  grounded := nullGrounded
  target := false

/-- Negative-control row with target true. -/
def nullCaseTrue : Case where
  grounded := nullGrounded
  target := true

theorem nullTargetsDiffer :
    nullCaseFalse.target ≠ nullCaseTrue.target := by
  decide

/--
Concrete random/decorative-target control: identical admitted grounded structure
cannot reconstruct opposite target labels.
-/
theorem nullControlNotReconstructible :
    ¬ ∃ derive : GroundedInput → Bool,
        Reconstructs derive nullCaseFalse ∧
        Reconstructs derive nullCaseTrue := by
  exact sameGrounded_differentTarget_notReconstructible
    nullCaseFalse
    nullCaseTrue
    rfl
    nullTargetsDiffer

/--
Positive-control cases keep the observation fixed and differ in exactly one
admitted grounded discriminator.
-/
def positiveCaseFalse : Case where
  grounded := {
    observation := false
    discriminator := false
  }
  target := false

def positiveCaseTrue : Case where
  grounded := {
    observation := false
    discriminator := true
  }
  target := true

/-- Reconstruction from the independently admitted discriminator. -/
def deriveFromDiscriminator (g : GroundedInput) : Bool :=
  g.discriminator

theorem groundedDiscriminatorReconstructs :
    Reconstructs deriveFromDiscriminator positiveCaseFalse ∧
    Reconstructs deriveFromDiscriminator positiveCaseTrue := by
  constructor <;> rfl

theorem positiveGroundedInputsDiffer :
    positiveCaseFalse.grounded ≠ positiveCaseTrue.grounded := by
  decide

/--
The positive control differs from the null control in the relevant respect:
one admitted grounded distinction is available and is sufficient for the two
target classifications.
-/
theorem matchedPositiveControl :
    ∃ derive : GroundedInput → Bool,
      Reconstructs derive positiveCaseFalse ∧
      Reconstructs derive positiveCaseTrue := by
  exact ⟨deriveFromDiscriminator, groundedDiscriminatorReconstructs⟩

end NonVacuityBasisWitness

end RelayTheory
