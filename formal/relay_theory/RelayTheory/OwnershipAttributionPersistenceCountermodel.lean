namespace RelayTheory

namespace OwnershipAttributionPersistenceCountermodel

abbrev Time := Bool
abbrev Agent := Bool
abbrev State := Bool
abbrev Snapshot := Bool

def t0 : Time := false
def t1 : Time := true
def agentA : Agent := false
def agentB : Agent := true

/--
Finite time-indexed lower-level response profile.

No Ownership, persistent-owner, authorship, or controller classification field
is present.
-/
structure IndexedProfile where
  realized : Time → State
  generatedUnder : Time → Agent → Bool → State
  acceptsRevision : Time → Agent → State → Bool

def GenerationSensitiveAt
    (p : IndexedProfile)
    (t : Time)
    (a : Agent) : Prop :=
  p.generatedUnder t a false ≠ p.generatedUnder t a true

/--
For Boolean state, propose the opposite of the realized state and ask whether
that nontrivial successor is accepted in the declared revision context.
-/
def CanReviseAt
    (p : IndexedProfile)
    (t : Time)
    (a : Agent) : Prop :=
  p.acceptsRevision t a (Bool.not (p.realized t)) = true

/--
Control-transfer witness: realized state stays fixed and generation sensitivity
remains with A, while revision privilege transfers from A to B.
-/
def transferProfile : IndexedProfile where
  realized _ := true
  generatedUnder _ agent source :=
    match agent with
    | false => source
    | true => true
  acceptsRevision time agent proposal :=
    match time, agent, proposal with
    | false, false, false => true
    | true, true, false => true
    | _, _, _ => false

theorem transfer_realizedStateFixed :
    transferProfile.realized t0 = transferProfile.realized t1 := by
  rfl

theorem transfer_A_generationSensitive_t0 :
    GenerationSensitiveAt transferProfile t0 agentA := by
  intro h
  exact Bool.noConfusion h

theorem transfer_A_generationSensitive_t1 :
    GenerationSensitiveAt transferProfile t1 agentA := by
  intro h
  exact Bool.noConfusion h

theorem transfer_B_not_generationSensitive_t0 :
    ¬ GenerationSensitiveAt transferProfile t0 agentB := by
  intro h
  exact h rfl

theorem transfer_B_not_generationSensitive_t1 :
    ¬ GenerationSensitiveAt transferProfile t1 agentB := by
  intro h
  exact h rfl

theorem transfer_A_canRevise_t0 :
    CanReviseAt transferProfile t0 agentA := by
  rfl

theorem transfer_B_not_canRevise_t0 :
    ¬ CanReviseAt transferProfile t0 agentB := by
  intro h
  exact Bool.noConfusion h

theorem transfer_A_not_canRevise_t1 :
    ¬ CanReviseAt transferProfile t1 agentA := by
  intro h
  exact Bool.noConfusion h

theorem transfer_B_canRevise_t1 :
    CanReviseAt transferProfile t1 agentB := by
  rfl

/--
Revision privilege changes while the realized state and generation-side
attribution remain fixed.
-/
theorem revisionPrivilegeTransfersWithoutStateReplacement :
    transferProfile.realized t0 = transferProfile.realized t1 ∧
    GenerationSensitiveAt transferProfile t0 agentA ∧
    GenerationSensitiveAt transferProfile t1 agentA ∧
    CanReviseAt transferProfile t0 agentA ∧
    ¬ CanReviseAt transferProfile t0 agentB ∧
    ¬ CanReviseAt transferProfile t1 agentA ∧
    CanReviseAt transferProfile t1 agentB := by
  exact ⟨transfer_realizedStateFixed,
    transfer_A_generationSensitive_t0,
    transfer_A_generationSensitive_t1,
    transfer_A_canRevise_t0,
    transfer_B_not_canRevise_t0,
    transfer_A_not_canRevise_t1,
    transfer_B_canRevise_t1⟩

/--
Replacement witness: the realized Boolean value stays the same, but the
generation-sensitive source changes from A at t0 to B at t1.
-/
def replacementProfile : IndexedProfile where
  realized _ := true
  generatedUnder time agent source :=
    match time, agent with
    | false, false => source
    | true, true => source
    | _, _ => true
  acceptsRevision time agent proposal :=
    match time, agent, proposal with
    | false, false, false => true
    | true, true, false => true
    | _, _, _ => false

theorem replacement_realizedStateFixed :
    replacementProfile.realized t0 = replacementProfile.realized t1 := by
  rfl

theorem replacement_A_generationSensitive_t0 :
    GenerationSensitiveAt replacementProfile t0 agentA := by
  intro h
  exact Bool.noConfusion h

theorem replacement_A_not_generationSensitive_t1 :
    ¬ GenerationSensitiveAt replacementProfile t1 agentA := by
  intro h
  exact h rfl

theorem replacement_B_not_generationSensitive_t0 :
    ¬ GenerationSensitiveAt replacementProfile t0 agentB := by
  intro h
  exact h rfl

theorem replacement_B_generationSensitive_t1 :
    GenerationSensitiveAt replacementProfile t1 agentB := by
  intro h
  exact Bool.noConfusion h

theorem currentGenerationAttributionCanChangeAcrossReplacement :
    replacementProfile.realized t0 = replacementProfile.realized t1 ∧
    GenerationSensitiveAt replacementProfile t0 agentA ∧
    ¬ GenerationSensitiveAt replacementProfile t1 agentA ∧
    ¬ GenerationSensitiveAt replacementProfile t0 agentB ∧
    GenerationSensitiveAt replacementProfile t1 agentB := by
  exact ⟨replacement_realizedStateFixed,
    replacement_A_generationSensitive_t0,
    replacement_A_not_generationSensitive_t1,
    replacement_B_not_generationSensitive_t0,
    replacement_B_generationSensitive_t1⟩

/--
Cross-snapshot continuity is evaluated under an explicit criterion rather than
stored as an intrinsic persistent-Ownership bit.
-/
def StrictSnapshotIdentity (x y : Snapshot) : Prop :=
  x = y

def DeclaredSuccessorLineage (x y : Snapshot) : Prop :=
  x = y ∨ (x = false ∧ y = true)

def ContinuesUnder
    (criterion : Snapshot → Snapshot → Prop) : Prop :=
  criterion false true

theorem strictCriterionRejectsReplacement :
    ¬ ContinuesUnder StrictSnapshotIdentity := by
  intro h
  exact Bool.noConfusion h

theorem declaredLineageAcceptsReplacement :
    ContinuesUnder DeclaredSuccessorLineage := by
  exact Or.inr ⟨rfl, rfl⟩

/--
The same replacement pair is non-continuous under strict snapshot identity and
continuous under the declared successor-lineage criterion.
-/
theorem persistenceDependsOnExplicitCriterion :
    ¬ ContinuesUnder StrictSnapshotIdentity ∧
    ContinuesUnder DeclaredSuccessorLineage := by
  exact ⟨strictCriterionRejectsReplacement, declaredLineageAcceptsReplacement⟩

/--
Declared lineage continuity does not force current generation-side attribution
to remain with the earlier source.
-/
theorem lineageDoesNotPreserveCurrentGenerationAttribution :
    ContinuesUnder DeclaredSuccessorLineage ∧
    GenerationSensitiveAt replacementProfile t0 agentA ∧
    ¬ GenerationSensitiveAt replacementProfile t1 agentA ∧
    ¬ GenerationSensitiveAt replacementProfile t0 agentB ∧
    GenerationSensitiveAt replacementProfile t1 agentB := by
  exact ⟨declaredLineageAcceptsReplacement,
    replacement_A_generationSensitive_t0,
    replacement_A_not_generationSensitive_t1,
    replacement_B_not_generationSensitive_t0,
    replacement_B_generationSensitive_t1⟩

/--
A decorative continuity label may vary while all lower-level time-indexed
judgments remain fixed.
-/
structure DecoratedHistory where
  base : IndexedProfile
  decorativeContinuityFlag : Bool

def decoratedTransferTrue : DecoratedHistory where
  base := transferProfile
  decorativeContinuityFlag := true

def decoratedTransferFalse : DecoratedHistory where
  base := transferProfile
  decorativeContinuityFlag := false

theorem decorativeLabelDeletion_generation :
    GenerationSensitiveAt decoratedTransferTrue.base t1 agentA ↔
    GenerationSensitiveAt decoratedTransferFalse.base t1 agentA := by
  rfl

theorem decorativeLabelDeletion_revision :
    CanReviseAt decoratedTransferTrue.base t1 agentB ↔
    CanReviseAt decoratedTransferFalse.base t1 agentB := by
  rfl

end OwnershipAttributionPersistenceCountermodel

end RelayTheory
