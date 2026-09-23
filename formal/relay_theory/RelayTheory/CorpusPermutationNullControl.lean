namespace RelayTheory

namespace CorpusPermutationNullControl

/--
A four-row deterministic fixture. The second component makes the carrier contain
two rows for each grounded Boolean value.
-/
abbrev Row := Bool × Bool

/-- The only grounded discriminator exposed to the frozen reconstruction. -/
def grounded (row : Row) : Bool :=
  row.1

/-- Real aligned target for the fixture. -/
def realTarget (row : Row) : Bool :=
  row.1

/--
A fixed row permutation used to construct the null target assignment.
It flips the first coordinate and leaves the second coordinate unchanged.
-/
def swapFirst (row : Row) : Row :=
  (!row.1, row.2)

/--
The null target is obtained only by permuting which row supplies the target.
The reconstruction function below is not changed.
-/
def permutedTarget (row : Row) : Bool :=
  realTarget (swapFirst row)

/-- Frozen reconstruction used for both real and null evaluation. -/
def derive (input : Bool) : Bool :=
  input

def FullCoverage
    (target : Row → Bool) : Prop :=
  ∀ row, derive (grounded row) = target row

def ZeroCoverage
    (target : Row → Bool) : Prop :=
  ∀ row, derive (grounded row) ≠ target row

/-- Local conjunction form because Lean core exposes Injective/Surjective separately. -/
def Bijective
    {α β : Type}
    (f : α → β) : Prop :=
  Function.Injective f ∧ Function.Surjective f

/-- The declared row permutation is an involution. -/
theorem swapFirstInvolutive
    (row : Row) :
    swapFirst (swapFirst row) = row := by
  cases row with
  | mk a b =>
      cases a <;> rfl

/-- Hence the null-control row map is injective. -/
theorem swapFirstInjective :
    Function.Injective swapFirst := by
  intro a b h
  calc
    a = swapFirst (swapFirst a) := (swapFirstInvolutive a).symm
    _ = swapFirst (swapFirst b) := congrArg swapFirst h
    _ = b := swapFirstInvolutive b

/-- And every fixture row is reached by the same involution. -/
theorem swapFirstSurjective :
    Function.Surjective swapFirst := by
  intro row
  exact ⟨swapFirst row, swapFirstInvolutive row⟩

theorem swapFirstBijective :
    Bijective swapFirst := by
  exact ⟨swapFirstInjective, swapFirstSurjective⟩

/--
The frozen reconstruction has full pointwise coverage on the aligned target.
-/
theorem realTargetFullCoverage :
    FullCoverage realTarget := by
  intro row
  rfl

/--
The same frozen reconstruction fails on every row after the target permutation.
No basis, criterion, probe, partition, or derive function is changed.
-/
theorem permutedTargetZeroCoverage :
    ZeroCoverage permutedTarget := by
  intro row
  cases row with
  | mk a b =>
      cases a <;>
        simp [derive, grounded, permutedTarget, realTarget, swapFirst]

/--
The null assignment is literally the real target transported along the declared
bijective row permutation.
-/
theorem permutedTargetIsTransportedRealTarget
    (row : Row) :
    permutedTarget row = realTarget (swapFirst row) := by
  rfl

/--
Compact corpus-level control semantics for the deterministic fixture:
the real alignment is fully reconstructed, whereas the target-permuted alignment
has zero pointwise coverage under exactly the same frozen derive function.
-/
theorem realVsPermutedCoverageContrast :
    FullCoverage realTarget ∧
    ZeroCoverage permutedTarget ∧
    Bijective swapFirst := by
  exact ⟨
    realTargetFullCoverage,
    permutedTargetZeroCoverage,
    swapFirstBijective
  ⟩

end CorpusPermutationNullControl

end RelayTheory
