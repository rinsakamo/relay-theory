namespace RelayTheory
namespace LocalLineageGlobalOrderCountermodel

/--
Three-event merge fixture.  The names are deliberately structural only:
two incomparable sources `a` and `b` both precede `c`.
-/
inductive Event where
  | a
  | b
  | c
  deriving DecidableEq, Repr

/--
Ambient reflexive precedence relation for the finite merge fixture.

The only non-reflexive comparisons are:

  a <= c
  b <= c

In particular, a and b are incomparable.
-/
def Precedes : Event → Event → Prop
  | .a, .a => True
  | .b, .b => True
  | .c, .c => True
  | .a, .c => True
  | .b, .c => True
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

/-- Neither ambient direction compares the two source events. -/
def Incomparable (x y : Event) : Prop :=
  ¬ Precedes x y ∧ ¬ Precedes y x

theorem sources_incomparable :
    Incomparable .a .b := by
  simp [Incomparable, Precedes]

/-- First selected local lineage: a -> c. -/
def lineageA (x : Event) : Prop :=
  x = .a ∨ x = .c

/-- Second selected local lineage: b -> c. -/
def lineageB (x : Event) : Prop :=
  x = .b ∨ x = .c

/-- Ambient precedence is total when restricted to a selected predicate. -/
def TotalOn (s : Event → Prop) : Prop :=
  ∀ x y, s x → s y → Precedes x y ∨ Precedes y x

theorem lineageA_total :
    TotalOn lineageA := by
  intro x y hx hy
  cases x <;> cases y <;> simp_all [lineageA, Precedes]

theorem lineageB_total :
    TotalOn lineageB := by
  intro x y hx hy
  cases x <;> cases y <;> simp_all [lineageB, Precedes]

/-- Every event occurs in at least one of the two selected local lineages. -/
def CoveredBySelectedLineages : Prop :=
  ∀ x, lineageA x ∨ lineageB x

theorem selected_lineages_cover :
    CoveredBySelectedLineages := by
  intro x
  cases x <;> simp [lineageA, lineageB]

/-- Ambient totality would require every event pair to be comparable. -/
def AmbientTotal : Prop :=
  ∀ x y, Precedes x y ∨ Precedes y x

/--
Covered locally total lineages do not force ambient totality:
the pair a,b remains incomparable.
-/
theorem covered_local_totality_does_not_force_ambient_totality :
    TotalOn lineageA ∧
    TotalOn lineageB ∧
    CoveredBySelectedLineages ∧
    ¬ AmbientTotal := by
  refine ⟨lineageA_total, lineageB_total, selected_lineages_cover, ?_⟩
  intro htotal
  have hab := htotal .a .b
  simpa [Precedes] using hab

/-- First scalar serialization: a < b < c. -/
def rankAB : Event → Nat
  | .a => 0
  | .b => 1
  | .c => 2

/-- Second scalar serialization: b < a < c. -/
def rankBA : Event → Nat
  | .a => 1
  | .b => 0
  | .c => 2

/-- A scalar ranking preserves every comparison already present in the ambient order. -/
def OrderPreserving (rank : Event → Nat) : Prop :=
  ∀ x y, Precedes x y → rank x ≤ rank y

/--
A finite scalar linearization is an injective scalar ranking that preserves
ambient precedence.  Injectivity makes the scalar presentation a total order
of distinct events; no order-reflection assumption is included.
-/
def ScalarLinearization (rank : Event → Nat) : Prop :=
  OrderPreserving rank ∧ Function.Injective rank

theorem rankAB_order_preserving :
    OrderPreserving rankAB := by
  intro x y hxy
  cases x <;> cases y <;> simp_all [Precedes, rankAB]

theorem rankBA_order_preserving :
    OrderPreserving rankBA := by
  intro x y hxy
  cases x <;> cases y <;> simp_all [Precedes, rankBA]

theorem rankAB_injective :
    Function.Injective rankAB := by
  intro x y hxy
  cases x <;> cases y <;> simp_all [rankAB]

theorem rankBA_injective :
    Function.Injective rankBA := by
  intro x y hxy
  cases x <;> cases y <;> simp_all [rankBA]

theorem rankAB_linearization :
    ScalarLinearization rankAB :=
  ⟨rankAB_order_preserving, rankAB_injective⟩

theorem rankBA_linearization :
    ScalarLinearization rankBA :=
  ⟨rankBA_order_preserving, rankBA_injective⟩

/--
The two valid scalar linearizations preserve the same ambient precedence while
ordering the ambiently incomparable pair in opposite ways.
-/
theorem distinct_linearizations_add_opposite_comparisons :
    ScalarLinearization rankAB ∧
    ScalarLinearization rankBA ∧
    Incomparable .a .b ∧
    rankAB .a < rankAB .b ∧
    rankBA .b < rankBA .a := by
  exact ⟨rankAB_linearization, rankBA_linearization, sources_incomparable,
    by decide, by decide⟩

/--
Primary finite discriminator for #45.

Every event is covered by one of two locally total lineages, yet the ambient
partial order is non-total.  The same ambient order also admits two faithful
order-preserving scalar serializations that disagree on the incomparable pair.

Thus local one-dimensionality and serializability do not by themselves select
one intrinsic global total order in this fixture.
-/
theorem local_lineage_global_order_countermodel :
    TotalOn lineageA ∧
    TotalOn lineageB ∧
    CoveredBySelectedLineages ∧
    ¬ AmbientTotal ∧
    ScalarLinearization rankAB ∧
    ScalarLinearization rankBA ∧
    rankAB .a < rankAB .b ∧
    rankBA .b < rankBA .a := by
  exact ⟨
    lineageA_total,
    lineageB_total,
    selected_lineages_cover,
    covered_local_totality_does_not_force_ambient_totality.2.2.2,
    rankAB_linearization,
    rankBA_linearization,
    by decide,
    by decide
  ⟩

/-- Strict ambient precedence used by the deictic control below. -/
def StrictPrecedes (x y : Event) : Prop :=
  Precedes x y ∧ x ≠ y

instance strictPrecedesDecidable (x y : Event) :
    Decidable (StrictPrecedes x y) := by
  cases x <;> cases y <;>
    simp [StrictPrecedes, Precedes] <;>
    infer_instance

inductive DeicticClass where
  | here
  | past
  | future
  | elsewhere
  deriving DecidableEq, Repr

/--
Deictic classification from the ambient partial precedence relation.
An incomparable event remains explicitly `elsewhere`.
-/
def ambientClassify (focal x : Event) : DeicticClass :=
  if x = focal then
    .here
  else if StrictPrecedes x focal then
    .past
  else if StrictPrecedes focal x then
    .future
  else
    .elsewhere

/--
Deictic classification after replacing the ambient partial order by an
injective scalar serialization.  Every distinct pair becomes comparable.
-/
def scalarClassify (rank : Event → Nat) (focal x : Event) : DeicticClass :=
  if x = focal then
    .here
  else if rank x < rank focal then
    .past
  else
    .future

theorem ambient_b_elsewhere_from_a :
    ambientClassify .a .b = .elsewhere := by
  simp [ambientClassify, StrictPrecedes, Precedes]

theorem rankAB_b_future_from_a :
    scalarClassify rankAB .a .b = .future := by
  simp [scalarClassify, rankAB]

theorem rankBA_b_past_from_a :
    scalarClassify rankBA .a .b = .past := by
  simp [scalarClassify, rankBA]

/--
Positive control: on event pairs already comparable in the ambient order,
both scalar linearizations preserve the declared deictic relation.
-/
theorem scalar_classifiers_agree_on_ambient_comparisons :
    (∀ focal x,
      (Precedes focal x ∨ Precedes x focal) →
      scalarClassify rankAB focal x = ambientClassify focal x) ∧
    (∀ focal x,
      (Precedes focal x ∨ Precedes x focal) →
      scalarClassify rankBA focal x = ambientClassify focal x) := by
  constructor <;>
    intro focal x hcomp <;>
    cases focal <;> cases x <;>
    simp_all [scalarClassify, ambientClassify, StrictPrecedes, Precedes,
      rankAB, rankBA]

/--
Anti-smuggling discriminator.

The ambient partial order classifies b as ELSEWHERE relative to focal a.
Both valid scalar linearizations preserve every ambient precedence edge, yet
one turns b into FUTURE and the other turns b into PAST.

Therefore substituting a global serialization for the ambient order adds a
deictic temporal fact that is absent from the source partial structure.
-/
theorem linearization_can_invent_deictic_temporal_facts :
    ambientClassify .a .b = .elsewhere ∧
    scalarClassify rankAB .a .b = .future ∧
    scalarClassify rankBA .a .b = .past := by
  exact ⟨ambient_b_elsewhere_from_a,
    rankAB_b_future_from_a,
    rankBA_b_past_from_a⟩

end LocalLineageGlobalOrderCountermodel
end RelayTheory
