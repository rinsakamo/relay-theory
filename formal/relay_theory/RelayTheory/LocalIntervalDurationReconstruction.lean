namespace RelayTheory
namespace LocalIntervalDurationReconstruction

/--
Three-event finite chain used for the positive reconstruction test.

The constructor names are finite proof handles only.  No physical clock,
coordinate system, or preferred unit is encoded by the event identifiers.
-/
inductive Event where
  | a
  | b
  | c
  deriving DecidableEq, Repr

/-- Complete strict order on the finite chain: a < b < c. -/
def StrictPrecedes : Event → Event → Prop
  | .a, .b => True
  | .b, .c => True
  | .a, .c => True
  | _, _ => False

theorem strictPrecedes_irreflexive :
    ∀ x, ¬ StrictPrecedes x x := by
  intro x
  cases x <;> simp [StrictPrecedes]

theorem strictPrecedes_transitive :
    ∀ x y z,
      StrictPrecedes x y →
      StrictPrecedes y z →
      StrictPrecedes x z := by
  intro x y z hxy hyz
  cases x <;> cases y <;> cases z <;>
    simp_all [StrictPrecedes]

theorem strictPrecedes_total_on_distinct :
    ∀ x y, x ≠ y → StrictPrecedes x y ∨ StrictPrecedes y x := by
  intro x y hne
  cases x <;> cases y <;>
    simp_all [StrictPrecedes]

/--
Independent local interval magnitudes on the two immediate steps.

These values are supplied data.  They are not reconstructed from event order.
-/
structure LocalWeights where
  ab : Nat
  bc : Nat
  deriving DecidableEq, Repr

def PositiveWeights (w : LocalWeights) : Prop :=
  0 < w.ab ∧ 0 < w.bc

/--
Global finite duration table derived from only the two local interval weights
plus additive composition along the chain.

Pairs outside the forward strict-order surface are encoded as zero so that the
result can be represented as a total function.  This convention carries no
claim about negative duration.
-/
def DerivedDuration (w : LocalWeights) : Event → Event → Nat
  | .a, .b => w.ab
  | .b, .c => w.bc
  | .a, .c => w.ab + w.bc
  | _, _ => 0

/-- Encoding convention outside the declared forward interval surface. -/
def ZeroOutsideForward (D : Event → Event → Nat) : Prop :=
  ∀ x y, ¬ StrictPrecedes x y → D x y = 0

/--
A global duration assignment is admissible for the supplied local data when it
agrees on both immediate intervals, composes additively across a < b < c, and
uses the declared zero encoding outside forward intervals.
-/
def AdmissibleDuration
    (w : LocalWeights)
    (D : Event → Event → Nat) : Prop :=
  D .a .b = w.ab ∧
  D .b .c = w.bc ∧
  D .a .c = D .a .b + D .b .c ∧
  ZeroOutsideForward D

theorem derivedDuration_admissible (w : LocalWeights) :
    AdmissibleDuration w (DerivedDuration w) := by
  refine ⟨rfl, rfl, rfl, ?_⟩
  intro x y hnot
  cases x <;> cases y <;>
    simp_all [StrictPrecedes, DerivedDuration]

/--
Positive local weights induce positive duration on every forward interval in
the finite chain.
-/
theorem derivedDuration_positive
    (w : LocalWeights)
    (hw : PositiveWeights w) :
    ∀ x y, StrictPrecedes x y → 0 < DerivedDuration w x y := by
  intro x y hxy
  rcases hw with ⟨hab, hbc⟩
  cases x <;> cases y <;>
    simp_all [StrictPrecedes, DerivedDuration] <;>
    omega

/--
Uniqueness theorem.

Once the local interval weights, additive composition law, and outside-surface
encoding convention are fixed, every admissible global duration assignment is
extensionally equal to the derived table.
-/
theorem admissibleDuration_unique
    (w : LocalWeights)
    (D : Event → Event → Nat)
    (hD : AdmissibleDuration w D) :
    D = DerivedDuration w := by
  funext x y
  rcases hD with ⟨hab, hbc, hac, hzero⟩
  by_cases hxy : StrictPrecedes x y
  · cases x <;> cases y <;>
      simp_all [StrictPrecedes, DerivedDuration]
  · have hz : D x y = 0 := hzero x y hxy
    cases x <;> cases y <;>
      simp_all [StrictPrecedes, DerivedDuration]

/--
Existence plus uniqueness: the derived table is admissible, and every
admissible global duration assignment is extensionally equal to it.
-/
theorem admissible_duration_exists_and_is_unique (w : LocalWeights) :
    AdmissibleDuration w (DerivedDuration w) ∧
    ∀ D : Event → Event → Nat,
      AdmissibleDuration w D →
      D = DerivedDuration w := by
  exact ⟨
    derivedDuration_admissible w,
    fun D hD => admissibleDuration_unique w D hD
  ⟩

/--
The local-weight payload is recoverable from the derived global duration table.
Thus changing local metric information cannot leave the reconstructed duration
extensionally unchanged.
-/
theorem derivedDuration_injective :
    Function.Injective DerivedDuration := by
  intro w₁ w₂ h
  cases w₁ with
  | mk ab₁ bc₁ =>
      cases w₂ with
      | mk ab₂ bc₂ =>
          have hab : ab₁ = ab₂ := by
            have hpair := congrFun (congrFun h Event.a) Event.b
            simpa [DerivedDuration] using hpair
          have hbc : bc₁ = bc₂ := by
            have hpair := congrFun (congrFun h Event.b) Event.c
            simpa [DerivedDuration] using hpair
          simp [hab, hbc]

theorem different_local_weights_change_global_duration
    {w₁ w₂ : LocalWeights}
    (hneq : w₁ ≠ w₂) :
    DerivedDuration w₁ ≠ DerivedDuration w₂ := by
  intro hsame
  exact hneq (derivedDuration_injective hsame)

/--
Combined discriminator for #90.

The order remains fixed.  Independent local interval magnitudes plus additive
composition determine one and only one global duration assignment in this
finite chain, while changing those local magnitudes changes the reconstructed
global duration.

So the global duration table is derived here, but the local metric information
is not derived from order.
-/
theorem local_interval_weights_reconstruct_global_duration :
    (∀ w : LocalWeights,
      AdmissibleDuration w (DerivedDuration w)) ∧
    (∀ w D,
      AdmissibleDuration w D →
      D = DerivedDuration w) ∧
    Function.Injective DerivedDuration := by
  exact ⟨
    derivedDuration_admissible,
    admissibleDuration_unique,
    derivedDuration_injective
  ⟩

end LocalIntervalDurationReconstruction
end RelayTheory
