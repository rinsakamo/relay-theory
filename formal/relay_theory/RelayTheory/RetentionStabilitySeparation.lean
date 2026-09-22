import RelayTheory.RetainedFormationSeparation

namespace RelayTheory
namespace RetentionStabilitySeparation

abbrev Experience := RetainedFormationSeparation.Experience
abbrev RetainedState := RetainedFormationSeparation.RetainedState
abbrev Formation := RetainedFormationSeparation.Formation
abbrev Readout := RetainedFormationSeparation.Readout
abbrev Perturbation := Bool
abbrev Evolution := RetainedState → Perturbation → RetainedState

def formation : Formation :=
  RetainedFormationSeparation.experienceSensitive

def actualExperience : Experience := true

def formedState : RetainedState :=
  formation actualExperience

def readout : Readout :=
  RetainedFormationSeparation.currentReadout

def normalPerturbation : Perturbation := false

def changedPerturbation : Perturbation := true

def preservingEvolution : Evolution :=
  fun state _ => state

def fragileEvolution : Evolution :=
  fun state perturbation =>
    if perturbation then !state else state

def OrdinarilyRetained
    (evolve : Evolution)
    (state : RetainedState) : Prop :=
  evolve state normalPerturbation = state

def ReadoutStable
    (evolve : Evolution)
    (state : RetainedState) : Prop :=
  ∀ perturbation : Perturbation,
    readout (evolve state perturbation) = readout state

theorem formedState_is_true :
    formedState = true := by
  rfl

theorem sameOrdinaryState :
    preservingEvolution formedState normalPerturbation =
      fragileEvolution formedState normalPerturbation := by
  rfl

theorem sameOrdinaryReadout :
    readout (preservingEvolution formedState normalPerturbation) =
      readout (fragileEvolution formedState normalPerturbation) := by
  rfl

theorem preserving_ordinarilyRetained :
    OrdinarilyRetained preservingEvolution formedState := by
  rfl

theorem fragile_ordinarilyRetained :
    OrdinarilyRetained fragileEvolution formedState := by
  rfl

theorem changedPerturbationSeparates :
    preservingEvolution formedState changedPerturbation ≠
      fragileEvolution formedState changedPerturbation := by
  decide

theorem preserving_readoutStable :
    ReadoutStable preservingEvolution formedState := by
  intro perturbation
  rfl

theorem fragile_not_readoutStable :
    ¬ ReadoutStable fragileEvolution formedState := by
  intro h
  have bad := h changedPerturbation
  change false = true at bad
  exact Bool.noConfusion bad

theorem ordinaryRetention_doesNotDetermine_readoutStability :
    OrdinarilyRetained preservingEvolution formedState ∧
    OrdinarilyRetained fragileEvolution formedState ∧
    ReadoutStable preservingEvolution formedState ∧
    ¬ ReadoutStable fragileEvolution formedState := by
  exact ⟨
    preserving_ordinarilyRetained,
    fragile_ordinarilyRetained,
    preserving_readoutStable,
    fragile_not_readoutStable
  ⟩

theorem pointwiseEqualEvolution_preserves_readoutStability
    (first second : Evolution)
    (state : RetainedState)
    (hEq : ∀ perturbation, first state perturbation = second state perturbation) :
    ReadoutStable first state ↔ ReadoutStable second state := by
  constructor
  · intro hStable perturbation
    rw [← hEq perturbation]
    exact hStable perturbation
  · intro hStable perturbation
    rw [hEq perturbation]
    exact hStable perturbation

end RetentionStabilitySeparation
end RelayTheory
