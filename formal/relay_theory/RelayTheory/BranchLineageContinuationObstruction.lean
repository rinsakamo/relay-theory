namespace RelayTheory
namespace BranchLineageContinuationObstruction

/--
Minimal finite fork used only as a structural countermodel.

The event constructors are finite proof handles.  No branch is assigned
intrinsic identity, ownership, observer, or Self semantics.
-/
inductive Event where
  | root
  | left
  | right
  deriving DecidableEq, Repr

/--
Ambient reflexive precedence for the fork:

  root <= left
  root <= right

The two branch events are incomparable.
-/
def Precedes : Event → Event → Prop
  | .root, .root => True
  | .left, .left => True
  | .right, .right => True
  | .root, .left => True
  | .root, .right => True
  | _, _ => False

theorem precedence_refl :
    ∀ x : Event, Precedes x x := by
  intro x
  cases x <;> simp [Precedes]

theorem precedence_antisymm :
    ∀ x y : Event, Precedes x y → Precedes y x → x = y := by
  intro x y hxy hyx
  cases x <;> cases y <;> simp_all [Precedes]

theorem precedence_trans :
    ∀ x y z : Event,
      Precedes x y → Precedes y z → Precedes x z := by
  intro x y z hxy hyz
  cases x <;> cases y <;> cases z <;> simp_all [Precedes]

def StrictPrecedes (x y : Event) : Prop :=
  Precedes x y ∧ x ≠ y

theorem branches_incomparable :
    (¬ Precedes .left .right) ∧ (¬ Precedes .right .left) := by
  simp [Precedes]

/-- Source automorphism exchanging the two symmetric branches. -/
def swapBranches : Event → Event
  | .root => .root
  | .left => .right
  | .right => .left

theorem swapBranches_involutive :
    ∀ x, swapBranches (swapBranches x) = x := by
  intro x
  cases x <;> rfl

def PreservesPrecedence (f : Event → Event) : Prop :=
  ∀ x y, Precedes x y ↔ Precedes (f x) (f y)

theorem swapBranches_preserves_precedence :
    PreservesPrecedence swapBranches := by
  intro x y
  cases x <;> cases y <;> simp [Precedes, swapBranches]

/--
A selected subset is chain-like when every pair of selected events is
comparable in the ambient precedence relation.
-/
def Chain (L : Event → Prop) : Prop :=
  ∀ x y, L x → L y → Precedes x y ∨ Precedes y x

/--
A branch continuation contains the root, remains chain-like, and contains at
least one proper ambient successor of the root.

This definition does not name either branch as preferred.
-/
def BranchContinuation (L : Event → Prop) : Prop :=
  L .root ∧
  Chain L ∧
  ∃ x, L x ∧ StrictPrecedes .root x

/-- Left-side positive control. -/
def leftContinuation : Event → Prop
  | .root => True
  | .left => True
  | .right => False

/-- Right-side positive control. -/
def rightContinuation : Event → Prop
  | .root => True
  | .left => False
  | .right => True

theorem leftContinuation_valid :
    BranchContinuation leftContinuation := by
  constructor
  · simp [leftContinuation]
  constructor
  · intro x y hx hy
    cases x <;> cases y <;>
      simp_all [leftContinuation, Precedes]
  · refine ⟨.left, ?_, ?_⟩
    · simp [leftContinuation]
    · simp [StrictPrecedes, Precedes]

theorem rightContinuation_valid :
    BranchContinuation rightContinuation := by
  constructor
  · simp [rightContinuation]
  constructor
  · intro x y hx hy
    cases x <;> cases y <;>
      simp_all [rightContinuation, Precedes]
  · refine ⟨.right, ?_, ?_⟩
    · simp [rightContinuation]
    · simp [StrictPrecedes, Precedes]

/--
The source automorphism sends the left continuation membership pattern to the
right continuation membership pattern.
-/
theorem swap_maps_left_to_right :
    ∀ x, leftContinuation x ↔ rightContinuation (swapBranches x) := by
  intro x
  cases x <;> simp [leftContinuation, rightContinuation, swapBranches]

/--
A selected lineage is source-symmetry-invariant when branch exchange changes
no membership judgment.
-/
def SwapInvariantSubset (L : Event → Prop) : Prop :=
  ∀ x, L x ↔ L (swapBranches x)

/--
No valid continuation chain through the fork can remain invariant under the
source branch-swap symmetry.

A valid continuation must contain a proper successor of root.  In this fixture
that successor is left or right.  Swap invariance then forces the opposite
branch into the same selected subset, while chainhood forbids selecting both
incomparable branches.
-/
theorem no_swap_invariant_branch_continuation :
    ¬ ∃ L : Event → Prop,
      BranchContinuation L ∧ SwapInvariantSubset L := by
  rintro ⟨L, hcont, hinv⟩
  rcases hcont with ⟨_, hchain, x, hx, hstrict⟩
  cases x with
  | root =>
      simp [StrictPrecedes, Precedes] at hstrict
  | left =>
      have hright : L .right := by
        have h := (hinv .left).mp hx
        simpa [swapBranches] using h
      have hcomp := hchain .left .right hx hright
      simpa [Precedes] using hcomp
  | right =>
      have hleft : L .left := by
        have h := (hinv .right).mp hx
        simpa [swapBranches] using h
      have hcomp := hchain .right .left hx hleft
      simpa [Precedes] using hcomp

/--
The two explicit continuations are genuinely distinct.
-/
theorem two_distinct_valid_continuations :
    BranchContinuation leftContinuation ∧
    BranchContinuation rightContinuation ∧
    leftContinuation .left ∧
    ¬ rightContinuation .left ∧
    rightContinuation .right ∧
    ¬ leftContinuation .right := by
  exact ⟨
    leftContinuation_valid,
    rightContinuation_valid,
    by simp [leftContinuation],
    by simp [rightContinuation],
    by simp [rightContinuation],
    by simp [leftContinuation]
  ⟩

/--
Combined finite discriminator for #81.

The source branching order admits two valid continuation chains exchanged by a
precedence-preserving automorphism, while no valid continuation chain is itself
invariant under that automorphism.

Thus the supplied branching order does not structurally select one intrinsic
continuation lineage in this symmetric fixture.
-/
theorem branching_order_does_not_select_intrinsic_continuation :
    PreservesPrecedence swapBranches ∧
    BranchContinuation leftContinuation ∧
    BranchContinuation rightContinuation ∧
    (∀ x, leftContinuation x ↔ rightContinuation (swapBranches x)) ∧
    (¬ ∃ L : Event → Prop,
      BranchContinuation L ∧ SwapInvariantSubset L) := by
  exact ⟨
    swapBranches_preserves_precedence,
    leftContinuation_valid,
    rightContinuation_valid,
    swap_maps_left_to_right,
    no_swap_invariant_branch_continuation
  ⟩

end BranchLineageContinuationObstruction
end RelayTheory
