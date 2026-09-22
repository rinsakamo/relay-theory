namespace RelayTheory
namespace GlobalOrderSymmetryObstruction

/--
Three-event symmetric merge fixture inherited from the scoped Time question.

The constructor names are only finite proof handles.  The candidate preferred
order below is universally quantified and is not defined from constructor
position or event identifiers.
-/
inductive Event where
  | a
  | b
  | c
  deriving DecidableEq, Repr

/--
Ambient reflexive precedence:

  a <= c
  b <= c

with a and b incomparable.
-/
def Precedes : Event → Event → Prop
  | .a, .a => True
  | .b, .b => True
  | .c, .c => True
  | .a, .c => True
  | .b, .c => True
  | _, _ => False

/-- Nontrivial source automorphism exchanging the two incomparable events. -/
def swapAB : Event → Event
  | .a => .b
  | .b => .a
  | .c => .c

theorem swapAB_involutive :
    ∀ x, swapAB (swapAB x) = x := by
  intro x
  cases x <;> rfl

theorem swapAB_nontrivial :
    swapAB .a = .b ∧ swapAB .b = .a ∧ swapAB .c = .c := by
  exact ⟨rfl, rfl, rfl⟩

/-- The swap preserves every ambient precedence fact in both directions. -/
def PreservesPrecedence (f : Event → Event) : Prop :=
  ∀ x y, Precedes x y ↔ Precedes (f x) (f y)

theorem swapAB_preserves_precedence :
    PreservesPrecedence swapAB := by
  intro x y
  cases x <;> cases y <;> simp [Precedes, swapAB]

/-- Strict part of the ambient precedence relation. -/
def StrictPrecedes (x y : Event) : Prop :=
  Precedes x y ∧ x ≠ y

/-- Basic strict-order conditions, stated explicitly to avoid semantic imports. -/
def IsIrreflexive (R : Event → Event → Prop) : Prop :=
  ∀ x, ¬ R x x

def IsAsymmetric (R : Event → Event → Prop) : Prop :=
  ∀ x y, R x y → ¬ R y x

def IsTransitive (R : Event → Event → Prop) : Prop :=
  ∀ x y z, R x y → R y z → R x z

def IsTotalOnDistinct (R : Event → Event → Prop) : Prop :=
  ∀ x y, x ≠ y → R x y ∨ R y x

def IsStrictTotalOrder (R : Event → Event → Prop) : Prop :=
  IsIrreflexive R ∧
  IsAsymmetric R ∧
  IsTransitive R ∧
  IsTotalOnDistinct R

/-- Candidate global order preserves every strict ambient precedence fact. -/
def ExtendsAmbient (R : Event → Event → Prop) : Prop :=
  ∀ x y, StrictPrecedes x y → R x y

/--
A candidate preferred relation is source-symmetry-invariant when applying the
source automorphism changes no ordering judgment.
-/
def SwapInvariant (R : Event → Event → Prop) : Prop :=
  ∀ x y, R x y ↔ R (swapAB x) (swapAB y)

/--
Core obstruction.

No strict total order can remain invariant under the source automorphism that
exchanges a and b.  Totality must choose one direction for the pair; invariance
then forces the opposite direction as well, contradicting asymmetry.
-/
theorem no_swap_invariant_strict_total_order :
    ¬ ∃ R : Event → Event → Prop,
      IsStrictTotalOrder R ∧ SwapInvariant R := by
  rintro ⟨R, htotal, hinv⟩
  rcases htotal with ⟨_, hasym, _, hcompare⟩
  have hab_or_hba : R .a .b ∨ R .b .a :=
    hcompare .a .b (by decide)
  cases hab_or_hba with
  | inl hab =>
      have hswapped : R (swapAB .a) (swapAB .b) :=
        (hinv .a .b).mp hab
      have hba : R .b .a := by
        simpa [swapAB] using hswapped
      exact (hasym .a .b hab) hba
  | inr hba =>
      have hswapped : R (swapAB .b) (swapAB .a) :=
        (hinv .b .a).mp hba
      have hab : R .a .b := by
        simpa [swapAB] using hswapped
      exact (hasym .b .a hba) hab

/--
Stronger scoped statement for the Time query:
adding the requirement that a candidate order extend ambient precedence does
not remove the symmetry obstruction.
-/
theorem no_intrinsic_global_total_extension :
    ¬ ∃ R : Event → Event → Prop,
      IsStrictTotalOrder R ∧
      ExtendsAmbient R ∧
      SwapInvariant R := by
  rintro ⟨R, htotal, _, hinv⟩
  exact no_swap_invariant_strict_total_order ⟨R, htotal, hinv⟩

/--
Positive controls: total extensions do exist if one chooses a side of the
ambiently incomparable pair.
-/
def rankAB : Event → Nat
  | .a => 0
  | .b => 1
  | .c => 2

def rankBA : Event → Nat
  | .a => 1
  | .b => 0
  | .c => 2

def orderAB (x y : Event) : Prop :=
  rankAB x < rankAB y

def orderBA (x y : Event) : Prop :=
  rankBA x < rankBA y

theorem orderAB_strict_total :
    IsStrictTotalOrder orderAB := by
  constructor
  · intro x
    simp [orderAB]
  constructor
  · intro x y hxy
    simp [orderAB] at hxy ⊢
    omega
  constructor
  · intro x y z hxy hyz
    exact Nat.lt_trans hxy hyz
  · intro x y hne
    cases x <;> cases y <;>
      simp_all [orderAB, rankAB]

theorem orderBA_strict_total :
    IsStrictTotalOrder orderBA := by
  constructor
  · intro x
    simp [orderBA]
  constructor
  · intro x y hxy
    simp [orderBA] at hxy ⊢
    omega
  constructor
  · intro x y z hxy hyz
    exact Nat.lt_trans hxy hyz
  · intro x y hne
    cases x <;> cases y <;>
      simp_all [orderBA, rankBA]

theorem orderAB_extends_ambient :
    ExtendsAmbient orderAB := by
  intro x y hxy
  rcases hxy with ⟨hprec, hne⟩
  cases x <;> cases y <;>
    simp_all [Precedes, orderAB, rankAB]

theorem orderBA_extends_ambient :
    ExtendsAmbient orderBA := by
  intro x y hxy
  rcases hxy with ⟨hprec, hne⟩
  cases x <;> cases y <;>
    simp_all [Precedes, orderBA, rankBA]

theorem orderAB_breaks_swap_symmetry :
    ¬ SwapInvariant orderAB := by
  intro hinv
  have hab : orderAB .a .b := by
    simp [orderAB, rankAB]
  have hba : orderAB .b .a := by
    have h := (hinv .a .b).mp hab
    simpa [swapAB] using h
  simpa [orderAB, rankAB] using hba

theorem orderBA_breaks_swap_symmetry :
    ¬ SwapInvariant orderBA := by
  intro hinv
  have hba : orderBA .b .a := by
    simp [orderBA, rankBA]
  have hab : orderBA .a .b := by
    have h := (hinv .b .a).mp hba
    simpa [swapAB] using h
  simpa [orderBA, rankBA] using hab

/--
Combined discriminator.

The source symmetry is real and precedence-preserving.  Strict total extensions
exist, but every exhibited extension breaks that source symmetry, while the
generic theorem rules out any strict total extension that preserves it.

Thus a preferred total ordering of the symmetric incomparable pair cannot be
reconstructed invariantly from this source structure alone.
-/
theorem preferred_global_order_requires_symmetry_breaking :
    PreservesPrecedence swapAB ∧
    (IsStrictTotalOrder orderAB ∧ ExtendsAmbient orderAB) ∧
    (IsStrictTotalOrder orderBA ∧ ExtendsAmbient orderBA) ∧
    ¬ SwapInvariant orderAB ∧
    ¬ SwapInvariant orderBA ∧
    (¬ ∃ R : Event → Event → Prop,
      IsStrictTotalOrder R ∧ ExtendsAmbient R ∧ SwapInvariant R) := by
  exact ⟨
    swapAB_preserves_precedence,
    ⟨orderAB_strict_total, orderAB_extends_ambient⟩,
    ⟨orderBA_strict_total, orderBA_extends_ambient⟩,
    orderAB_breaks_swap_symmetry,
    orderBA_breaks_swap_symmetry,
    no_intrinsic_global_total_extension
  ⟩

end GlobalOrderSymmetryObstruction
end RelayTheory
