namespace RelayTheory
namespace TemporalOrderMetricIndependence

/--
Three-event strict chain used only as a finite discriminator:

  a < b < c
-/
inductive Event where
  | a
  | b
  | c
  deriving DecidableEq, Repr

/-- Fixed strict source order. -/
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

/-- A finite scalar clock. -/
abbrev Clock := Event → Nat

/--
The clock carries exactly the same strict ordering information as the source
when it preserves and reflects every strict comparison.
-/
def OrderEquivalentClock (clock : Clock) : Prop :=
  ∀ x y, StrictPrecedes x y ↔ clock x < clock y

/-- Unit-spaced clock. -/
def clockUnit : Clock
  | .a => 0
  | .b => 1
  | .c => 2

/-- Same event order, but the final interval is stretched. -/
def clockStretched : Clock
  | .a => 0
  | .b => 1
  | .c => 3

theorem clockUnit_injective :
    Function.Injective clockUnit := by
  intro x y hxy
  cases x <;> cases y <;>
    simp_all [clockUnit]

theorem clockStretched_injective :
    Function.Injective clockStretched := by
  intro x y hxy
  cases x <;> cases y <;>
    simp_all [clockStretched]

theorem clockUnit_order_equivalent :
    OrderEquivalentClock clockUnit := by
  intro x y
  cases x <;> cases y <;>
    simp [OrderEquivalentClock, StrictPrecedes, clockUnit]

theorem clockStretched_order_equivalent :
    OrderEquivalentClock clockStretched := by
  intro x y
  cases x <;> cases y <;>
    simp [OrderEquivalentClock, StrictPrecedes, clockStretched]

/--
Duration-like interval induced by a supplied scalar clock.

Only ordered pairs matter to the current discriminator.  The use of Nat here
is a finite witness choice, not a physical claim about temporal codomain.
-/
def DurationFromClock (clock : Clock) (x y : Event) : Nat :=
  clock y - clock x

def durationUnit : Event → Event → Nat :=
  DurationFromClock clockUnit

def durationStretched : Event → Event → Nat :=
  DurationFromClock clockStretched

theorem durations_agree_on_first_interval :
    durationUnit .a .b = durationStretched .a .b := by
  simp [durationUnit, durationStretched, DurationFromClock,
    clockUnit, clockStretched]

theorem durations_disagree_on_second_interval :
    durationUnit .b .c ≠ durationStretched .b .c := by
  simp [durationUnit, durationStretched, DurationFromClock,
    clockUnit, clockStretched]

theorem durations_disagree_on_total_interval :
    durationUnit .a .c ≠ durationStretched .a .c := by
  simp [durationUnit, durationStretched, DurationFromClock,
    clockUnit, clockStretched]

/--
Both witness duration assignments satisfy the same finite chain additivity
condition.
-/
def ChainAdditive (duration : Event → Event → Nat) : Prop :=
  duration .a .c = duration .a .b + duration .b .c

theorem durationUnit_chain_additive :
    ChainAdditive durationUnit := by
  simp [ChainAdditive, durationUnit, DurationFromClock, clockUnit]

theorem durationStretched_chain_additive :
    ChainAdditive durationStretched := by
  simp [ChainAdditive, durationStretched, DurationFromClock, clockStretched]

/--
Both duration assignments are positive on every strict source comparison.
-/
def PositiveOnStrictOrder (duration : Event → Event → Nat) : Prop :=
  ∀ x y, StrictPrecedes x y → 0 < duration x y

theorem durationUnit_positive :
    PositiveOnStrictOrder durationUnit := by
  intro x y hxy
  cases x <;> cases y <;>
    simp_all [PositiveOnStrictOrder, StrictPrecedes,
      durationUnit, DurationFromClock, clockUnit]

theorem durationStretched_positive :
    PositiveOnStrictOrder durationStretched := by
  intro x y hxy
  cases x <;> cases y <;>
    simp_all [PositiveOnStrictOrder, StrictPrecedes,
      durationStretched, DurationFromClock, clockStretched]

/--
Exact order-only reconstruction obstruction.

A deterministic recovery function supplied with exactly the same source order
cannot return two extensionally different duration assignments for that same
input.
-/
theorem no_order_only_reconstruction_of_both_durations :
    ¬ ∃ recover :
      (Event → Event → Prop) → Event → Event → Nat,
      recover StrictPrecedes = durationUnit ∧
      recover StrictPrecedes = durationStretched := by
  rintro ⟨recover, hUnit, hStretched⟩
  have hDurations : durationUnit = durationStretched :=
    hUnit.symm.trans hStretched
  have hbc :
      durationUnit .b .c = durationStretched .b .c :=
    congrArg (fun duration => duration .b .c) hDurations
  exact durations_disagree_on_second_interval hbc

/--
Primary finite discriminator.

The event carrier and complete strict order are identical.  Two injective
scalar clocks both preserve and reflect that same order and both induce
positive, chain-additive duration assignments, yet they disagree on interval
magnitude.

Thus order information alone does not determine the metric-like spacing used
by these witnesses.
-/
theorem temporal_order_does_not_determine_metric_duration :
    Function.Injective clockUnit ∧
    Function.Injective clockStretched ∧
    OrderEquivalentClock clockUnit ∧
    OrderEquivalentClock clockStretched ∧
    ChainAdditive durationUnit ∧
    ChainAdditive durationStretched ∧
    PositiveOnStrictOrder durationUnit ∧
    PositiveOnStrictOrder durationStretched ∧
    durationUnit .b .c ≠ durationStretched .b .c ∧
    durationUnit .a .c ≠ durationStretched .a .c ∧
    (¬ ∃ recover :
      (Event → Event → Prop) → Event → Event → Nat,
      recover StrictPrecedes = durationUnit ∧
      recover StrictPrecedes = durationStretched) := by
  exact ⟨
    clockUnit_injective,
    clockStretched_injective,
    clockUnit_order_equivalent,
    clockStretched_order_equivalent,
    durationUnit_chain_additive,
    durationStretched_chain_additive,
    durationUnit_positive,
    durationStretched_positive,
    durations_disagree_on_second_interval,
    durations_disagree_on_total_interval,
    no_order_only_reconstruction_of_both_durations
  ⟩

end TemporalOrderMetricIndependence
end RelayTheory
