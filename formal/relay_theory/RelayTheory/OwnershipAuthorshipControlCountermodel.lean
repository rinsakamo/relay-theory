namespace RelayTheory

namespace OwnershipAuthorshipControlCountermodel

abbrev Bit := Bool

/--
Finite lower-level profile for one candidate source relative to one current
state.  It contains only a current value, a counterfactual generation
response, and an explicit revision-acceptance response.
-/
structure ResponseProfile where
  current : Bit
  generatedUnder : Bit → Bit
  acceptsRevision : Bit → Bit

def realizedState (p : ResponseProfile) : Bit :=
  p.current

/--
The generated state changes when the explicit source/intervention bit changes.
This is the finite causal/provenance-side discriminator; it is not normative
authorship, intention, responsibility, or title.
-/
def GenerationSensitive (p : ResponseProfile) : Prop :=
  p.generatedUnder false ≠ p.generatedUnder true

/--
A fixed nontrivial successor probe is accepted: the current state is true and
the proposed successor false is admitted by the declared revision context.
This is only operational revision privilege.
-/
def CanRevise (p : ResponseProfile) : Prop :=
  p.current = true ∧ p.acceptsRevision false = true

def neitherProfile : ResponseProfile where
  current := true
  generatedUnder _ := true
  acceptsRevision _ := false

def revisionOnlyProfile : ResponseProfile where
  current := true
  generatedUnder _ := true
  acceptsRevision proposed := Bool.not proposed

def generationOnlyProfile : ResponseProfile where
  current := true
  generatedUnder source := source
  acceptsRevision _ := false

def bothProfile : ResponseProfile where
  current := true
  generatedUnder source := source
  acceptsRevision proposed := Bool.not proposed

theorem allProfilesShareRealizedState :
    realizedState neitherProfile = realizedState revisionOnlyProfile ∧
    realizedState revisionOnlyProfile = realizedState generationOnlyProfile ∧
    realizedState generationOnlyProfile = realizedState bothProfile := by
  exact ⟨rfl, rfl, rfl⟩

theorem neither_not_generationSensitive :
    ¬ GenerationSensitive neitherProfile := by
  intro h
  exact h rfl

theorem neither_not_canRevise :
    ¬ CanRevise neitherProfile := by
  intro h
  exact Bool.noConfusion h.2

theorem revisionOnly_not_generationSensitive :
    ¬ GenerationSensitive revisionOnlyProfile := by
  intro h
  exact h rfl

theorem revisionOnly_canRevise :
    CanRevise revisionOnlyProfile := by
  exact ⟨rfl, rfl⟩

theorem generationOnly_generationSensitive :
    GenerationSensitive generationOnlyProfile := by
  intro h
  exact Bool.noConfusion h

theorem generationOnly_not_canRevise :
    ¬ CanRevise generationOnlyProfile := by
  intro h
  exact Bool.noConfusion h.2

theorem both_generationSensitive :
    GenerationSensitive bothProfile := by
  intro h
  exact Bool.noConfusion h

theorem both_canRevise :
    CanRevise bothProfile := by
  exact ⟨rfl, rfl⟩

/--
The selected finite lower-level model class realizes every Boolean combination
of generation sensitivity and revision privilege while holding the realized
current state fixed.
-/
theorem fourQuadrants :
    (¬ GenerationSensitive neitherProfile ∧ ¬ CanRevise neitherProfile) ∧
    (¬ GenerationSensitive revisionOnlyProfile ∧ CanRevise revisionOnlyProfile) ∧
    (GenerationSensitive generationOnlyProfile ∧ ¬ CanRevise generationOnlyProfile) ∧
    (GenerationSensitive bothProfile ∧ CanRevise bothProfile) := by
  constructor
  · exact ⟨neither_not_generationSensitive, neither_not_canRevise⟩
  constructor
  · exact ⟨revisionOnly_not_generationSensitive, revisionOnly_canRevise⟩
  constructor
  · exact ⟨generationOnly_generationSensitive, generationOnly_not_canRevise⟩
  · exact ⟨both_generationSensitive, both_canRevise⟩

/--
Direct destructive witnesses for the local Grand Null.
-/
theorem creatorWithoutCurrentRevision :
    GenerationSensitive generationOnlyProfile ∧
    ¬ CanRevise generationOnlyProfile := by
  exact ⟨generationOnly_generationSensitive, generationOnly_not_canRevise⟩

theorem reviserWithoutGeneration :
    ¬ GenerationSensitive revisionOnlyProfile ∧
    CanRevise revisionOnlyProfile := by
  exact ⟨revisionOnly_not_generationSensitive, revisionOnly_canRevise⟩

/--
A decorative high-level flag may vary while both lower-level derived judgments
remain fixed.  The flag is consulted by neither predicate.
-/
structure DecoratedProfile where
  base : ResponseProfile
  decorativeFlag : Bit

def decoratedGenerationTrue : DecoratedProfile where
  base := generationOnlyProfile
  decorativeFlag := true

def decoratedGenerationFalse : DecoratedProfile where
  base := generationOnlyProfile
  decorativeFlag := false

theorem decorativeLabelDeletion_generation :
    GenerationSensitive decoratedGenerationTrue.base ↔
    GenerationSensitive decoratedGenerationFalse.base := by
  rfl

theorem decorativeLabelDeletion_revision :
    CanRevise decoratedGenerationTrue.base ↔
    CanRevise decoratedGenerationFalse.base := by
  rfl

end OwnershipAuthorshipControlCountermodel

end RelayTheory
