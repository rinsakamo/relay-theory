namespace RelayTheory

namespace PartitionGroundingNonVacuity

/--
A minimal case surface with one declared grounded observation and one external
target field.
-/
structure Case where
  observation : Bool
  target : Bool
deriving DecidableEq

/--
A finite partition is represented by its cell label.
-/
abbrev Partition := Case → Bool

/-- Two cases occupy the same cell under a partition. -/
def SameCell
    (partition : Partition)
    (a b : Case) : Prop :=
  partition a = partition b

/--
The finite control's provenance condition for an admissible grounded partition:
its cell assignment must factor through the declared observation surface.
-/
def FactorsThroughObservation
    (partition : Partition) : Prop :=
  ∃ classify : Bool → Bool,
    ∀ c : Case, partition c = classify c.observation

def matchedFalse : Case where
  observation := false
  target := false

def matchedTrue : Case where
  observation := false
  target := true

theorem matchedObservationsAgree :
    matchedFalse.observation = matchedTrue.observation := by
  rfl

/--
Any partition that factors through the declared observation surface must keep
observation-identical matched cases in the same cell.
-/
theorem groundedPartitionPreservesMatchedEquivalence
    (partition : Partition)
    (hfactor : FactorsThroughObservation partition) :
    SameCell partition matchedFalse matchedTrue := by
  rcases hfactor with ⟨classify, hclassify⟩
  unfold SameCell
  calc
    partition matchedFalse = classify matchedFalse.observation :=
      hclassify matchedFalse
    _ = classify matchedTrue.observation := by
      rw [matchedObservationsAgree]
    _ = partition matchedTrue := (hclassify matchedTrue).symm

/-- A canonical grounded partition that uses only the declared observation. -/
def observationPartition : Partition :=
  fun c => c.observation

theorem observationPartitionFactorsThroughObservation :
    FactorsThroughObservation observationPartition := by
  refine ⟨fun x => x, ?_⟩
  intro c
  rfl

theorem observationPartitionKeepsMatchedCasesTogether :
    SameCell observationPartition matchedFalse matchedTrue := by
  exact groundedPartitionPreservesMatchedEquivalence
    observationPartition
    observationPartitionFactorsThroughObservation

/--
An explicitly answer-bearing post-hoc partition.
-/
def targetPartition : Partition :=
  fun c => c.target

theorem targetPartitionSeparatesMatchedCases :
    ¬ SameCell targetPartition matchedFalse matchedTrue := by
  simp [SameCell, targetPartition, matchedFalse, matchedTrue]

/--
The answer-bearing target partition cannot satisfy the grounded factorization
condition, because any such factorization would force the matched cases back
into the same cell.
-/
theorem targetPartitionDoesNotFactorThroughObservation :
    ¬ FactorsThroughObservation targetPartition := by
  intro hfactor
  exact targetPartitionSeparatesMatchedCases
    (groundedPartitionPreservesMatchedEquivalence targetPartition hfactor)

/--
Compact non-vacuity contrast: grounded quotienting preserves the equivalence
forced by the declared observation, while a target-bearing post-hoc partition
creates a separation that cannot be grounded in that observation surface.
-/
theorem posthocPartitionSelectionCreatesSeparation :
    FactorsThroughObservation observationPartition ∧
    SameCell observationPartition matchedFalse matchedTrue ∧
    ¬ SameCell targetPartition matchedFalse matchedTrue ∧
    ¬ FactorsThroughObservation targetPartition := by
  exact ⟨
    observationPartitionFactorsThroughObservation,
    observationPartitionKeepsMatchedCasesTogether,
    targetPartitionSeparatesMatchedCases,
    targetPartitionDoesNotFactorThroughObservation
  ⟩

end PartitionGroundingNonVacuity

end RelayTheory
