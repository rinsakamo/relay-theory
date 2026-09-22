import RelayTheory.OwnershipAuthorshipControlCountermodel

namespace RelayTheory

namespace OwnershipInstitutionalTitleCountermodel

abbrev Claimant := Bool

/--
A minimal institutional surface. The initial assignment and transfer rule are
declared institutional inputs, not physical facts and not an Ownership bit.
-/
structure Institution where
  initialAssignment : Claimant
  acceptsTransfer : Claimant → Claimant → Bool

structure TransferProposal where
  from : Claimant
  to : Claimant

/--
Replay one proposed transfer against the declared institutional rule.
-/
def currentRecognized
    (institution : Institution)
    (proposal : TransferProposal) : Claimant :=
  if institution.acceptsTransfer proposal.from proposal.to
  then proposal.to
  else institution.initialAssignment

/--
Scoped registry-mediated title judgment. This is a derived equality against the
current recognized claimant, not an input relation.
-/
def RegistryTitle
    (institution : Institution)
    (proposal : TransferProposal)
    (claimant : Claimant) : Prop :=
  currentRecognized institution proposal = claimant

def transferFalseToTrue : TransferProposal where
  from := false
  to := true

def acceptingInstitution : Institution where
  initialAssignment := false
  acceptsTransfer _ _ := true

def rejectingInstitution : Institution where
  initialAssignment := false
  acceptsTransfer _ _ := false

theorem admittedTransferChangesRecognizedClaimant :
    currentRecognized acceptingInstitution transferFalseToTrue = true := by
  rfl

theorem rejectedTransferPreservesInitialAssignment :
    currentRecognized rejectingInstitution transferFalseToTrue = false := by
  rfl

theorem sameProposalDifferentRuleSurfaceChangesRecognition :
    currentRecognized acceptingInstitution transferFalseToTrue ≠
      currentRecognized rejectingInstitution transferFalseToTrue := by
  intro h
  exact Bool.noConfusion h

theorem accepted_true_hasRegistryTitle :
    RegistryTitle acceptingInstitution transferFalseToTrue true := by
  rfl

theorem rejected_true_notRegistryTitle :
    ¬ RegistryTitle rejectingInstitution transferFalseToTrue true := by
  intro h
  exact Bool.noConfusion h

/--
Pair the institutional surface with the already-forged physical/control profile
from #46. The institutional component is deliberately independent of that
physical response profile.
-/
structure PhysicalInstitutionalCase where
  physical :
    OwnershipAuthorshipControlCountermodel.ResponseProfile
  institution : Institution
  proposal : TransferProposal

def samePhysicalAcceptedCase : PhysicalInstitutionalCase where
  physical := OwnershipAuthorshipControlCountermodel.revisionOnlyProfile
  institution := acceptingInstitution
  proposal := transferFalseToTrue

def samePhysicalRejectedCase : PhysicalInstitutionalCase where
  physical := OwnershipAuthorshipControlCountermodel.revisionOnlyProfile
  institution := rejectingInstitution
  proposal := transferFalseToTrue

theorem samePhysicalProfile_differentRegistryRecognition :
    samePhysicalAcceptedCase.physical = samePhysicalRejectedCase.physical ∧
    RegistryTitle
      samePhysicalAcceptedCase.institution
      samePhysicalAcceptedCase.proposal
      true ∧
    ¬ RegistryTitle
      samePhysicalRejectedCase.institution
      samePhysicalRejectedCase.proposal
      true := by
  exact ⟨rfl, accepted_true_hasRegistryTitle, rejected_true_notRegistryTitle⟩

/--
The candidate source can have current revision privilege while lacking the
registry-mediated title under the rejecting institution.
-/
theorem controllerWithoutRegistryTitle :
    OwnershipAuthorshipControlCountermodel.CanRevise
      OwnershipAuthorshipControlCountermodel.revisionOnlyProfile ∧
    ¬ RegistryTitle rejectingInstitution transferFalseToTrue true := by
  exact ⟨
    OwnershipAuthorshipControlCountermodel.revisionOnly_canRevise,
    rejected_true_notRegistryTitle
  ⟩

/--
The candidate source can hold registry-mediated title while lacking current
revision privilege.
-/
theorem registryTitleWithoutCurrentControl :
    RegistryTitle acceptingInstitution transferFalseToTrue true ∧
    ¬ OwnershipAuthorshipControlCountermodel.CanRevise
      OwnershipAuthorshipControlCountermodel.generationOnlyProfile := by
  exact ⟨
    accepted_true_hasRegistryTitle,
    OwnershipAuthorshipControlCountermodel.generationOnly_not_canRevise
  ⟩

/--
A high-level decorative label may vary while the institutional replay result
remains fixed.
-/
structure DecoratedInstitutionalCase where
  institution : Institution
  proposal : TransferProposal
  decorativeOwnershipFlag : Bool

def decoratedTrue : DecoratedInstitutionalCase where
  institution := acceptingInstitution
  proposal := transferFalseToTrue
  decorativeOwnershipFlag := true

def decoratedFalse : DecoratedInstitutionalCase where
  institution := acceptingInstitution
  proposal := transferFalseToTrue
  decorativeOwnershipFlag := false

theorem ownershipLabelDeletion_registryTitle :
    RegistryTitle decoratedTrue.institution decoratedTrue.proposal true ↔
    RegistryTitle decoratedFalse.institution decoratedFalse.proposal true := by
  rfl

/--
Scoped bundle:
- one and the same physical/control profile admits different registry-title
  outcomes under different institutional rule surfaces;
- registry title and current control vary independently in both directions.
-/
theorem physicalControlDoesNotDetermineRegistryTitle_bundle :
    samePhysicalAcceptedCase.physical = samePhysicalRejectedCase.physical ∧
    RegistryTitle
      samePhysicalAcceptedCase.institution
      samePhysicalAcceptedCase.proposal
      true ∧
    ¬ RegistryTitle
      samePhysicalRejectedCase.institution
      samePhysicalRejectedCase.proposal
      true ∧
    OwnershipAuthorshipControlCountermodel.CanRevise
      OwnershipAuthorshipControlCountermodel.revisionOnlyProfile ∧
    ¬ OwnershipAuthorshipControlCountermodel.CanRevise
      OwnershipAuthorshipControlCountermodel.generationOnlyProfile := by
  exact ⟨
    rfl,
    accepted_true_hasRegistryTitle,
    rejected_true_notRegistryTitle,
    OwnershipAuthorshipControlCountermodel.revisionOnly_canRevise,
    OwnershipAuthorshipControlCountermodel.generationOnly_not_canRevise
  ⟩

end OwnershipInstitutionalTitleCountermodel

end RelayTheory
