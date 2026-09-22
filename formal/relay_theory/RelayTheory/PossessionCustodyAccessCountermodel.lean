import RelayTheory.OwnershipAuthorshipControlCountermodel
import RelayTheory.OwnershipInstitutionalTitleCountermodel

namespace RelayTheory

namespace PossessionCustodyAccessCountermodel

abbrev Bit := Bool
abbrev RealizedSnapshot := Bit × Bit × Bit × Bit

/--
A minimal lower-level physical/use response surface.

The realized snapshot is stored separately from the counterfactual response
families so that matched profiles can share the same observed state while
differing in unobserved response.
-/
structure PossessionResponseProfile where
  actualCarrier : Bit
  actualObjectLocation : Bit
  actualRequest : Bit
  actualUseOutcome : Bit
  objectLocationUnderCarrier : Bit → Bit
  useOutcomeUnderRequest : Bit → Bit

def neitherProfile : PossessionResponseProfile where
  actualCarrier := false
  actualObjectLocation := false
  actualRequest := false
  actualUseOutcome := false
  objectLocationUnderCarrier _ := false
  useOutcomeUnderRequest _ := false

def accessOnlyProfile : PossessionResponseProfile where
  actualCarrier := false
  actualObjectLocation := false
  actualRequest := false
  actualUseOutcome := false
  objectLocationUnderCarrier _ := false
  useOutcomeUnderRequest x := x

def custodyOnlyProfile : PossessionResponseProfile where
  actualCarrier := false
  actualObjectLocation := false
  actualRequest := false
  actualUseOutcome := false
  objectLocationUnderCarrier x := x
  useOutcomeUnderRequest _ := false

def bothProfile : PossessionResponseProfile where
  actualCarrier := false
  actualObjectLocation := false
  actualRequest := false
  actualUseOutcome := false
  objectLocationUnderCarrier x := x
  useOutcomeUnderRequest x := x

def realizedSnapshot (p : PossessionResponseProfile) : RealizedSnapshot :=
  (p.actualCarrier, p.actualObjectLocation, p.actualRequest, p.actualUseOutcome)

def Sensitive (f : Bit → Bit) : Prop :=
  f false ≠ f true

/--
Operational custody-like transport coupling: object location changes under the
declared claimant-associated carrier/location probe.
-/
def CustodyLike (p : PossessionResponseProfile) : Prop :=
  Sensitive p.objectLocationUnderCarrier

/--
Operational access-like capability: use outcome changes under the declared
claimant-associated request probe.
-/
def AccessLike (p : PossessionResponseProfile) : Prop :=
  Sensitive p.useOutcomeUnderRequest

theorem identitySensitive : Sensitive (fun x : Bit => x) := by
  intro h
  exact Bool.noConfusion h

theorem constantFalseNotSensitive : ¬ Sensitive (fun _ : Bit => false) := by
  intro h
  exact h rfl

theorem allProfiles_sameRealizedSnapshot :
    realizedSnapshot neitherProfile = realizedSnapshot accessOnlyProfile ∧
    realizedSnapshot neitherProfile = realizedSnapshot custodyOnlyProfile ∧
    realizedSnapshot neitherProfile = realizedSnapshot bothProfile := by
  exact ⟨rfl, rfl, rfl⟩

theorem neither_quadrant :
    ¬ CustodyLike neitherProfile ∧ ¬ AccessLike neitherProfile := by
  exact ⟨constantFalseNotSensitive, constantFalseNotSensitive⟩

theorem accessOnly_quadrant :
    ¬ CustodyLike accessOnlyProfile ∧ AccessLike accessOnlyProfile := by
  exact ⟨constantFalseNotSensitive, identitySensitive⟩

theorem custodyOnly_quadrant :
    CustodyLike custodyOnlyProfile ∧ ¬ AccessLike custodyOnlyProfile := by
  exact ⟨identitySensitive, constantFalseNotSensitive⟩

theorem both_quadrant :
    CustodyLike bothProfile ∧ AccessLike bothProfile := by
  exact ⟨identitySensitive, identitySensitive⟩

theorem custodyAndAccess_independentlyVariable :
    (¬ CustodyLike neitherProfile ∧ ¬ AccessLike neitherProfile) ∧
    (¬ CustodyLike accessOnlyProfile ∧ AccessLike accessOnlyProfile) ∧
    (CustodyLike custodyOnlyProfile ∧ ¬ AccessLike custodyOnlyProfile) ∧
    (CustodyLike bothProfile ∧ AccessLike bothProfile) := by
  exact ⟨neither_quadrant, accessOnly_quadrant, custodyOnly_quadrant, both_quadrant⟩

/--
Explicitly pair the possession response surface with #46 current revision
authority. The two response surfaces remain distinct.
-/
structure AccessRevisionCase where
  possession : PossessionResponseProfile
  revision :
    OwnershipAuthorshipControlCountermodel.ResponseProfile

def accessWithoutRevisionCase : AccessRevisionCase where
  possession := accessOnlyProfile
  revision := OwnershipAuthorshipControlCountermodel.generationOnlyProfile

def revisionWithoutAccessCase : AccessRevisionCase where
  possession := custodyOnlyProfile
  revision := OwnershipAuthorshipControlCountermodel.revisionOnlyProfile

theorem accessWithoutCurrentRevisionPrivilege :
    AccessLike accessWithoutRevisionCase.possession ∧
    ¬ OwnershipAuthorshipControlCountermodel.CanRevise
      accessWithoutRevisionCase.revision := by
  exact ⟨
    accessOnly_quadrant.2,
    OwnershipAuthorshipControlCountermodel.generationOnly_not_canRevise
  ⟩

theorem currentRevisionPrivilegeWithoutAccess :
    OwnershipAuthorshipControlCountermodel.CanRevise
      revisionWithoutAccessCase.revision ∧
    ¬ AccessLike revisionWithoutAccessCase.possession := by
  exact ⟨
    OwnershipAuthorshipControlCountermodel.revisionOnly_canRevise,
    custodyOnly_quadrant.2
  ⟩

/--
Pair one identical custody/access profile with two #58 institutional rule
surfaces. Registry title changes while the physical/use response profile is
fixed.
-/
structure PossessionInstitutionCase where
  possession : PossessionResponseProfile
  institution :
    OwnershipInstitutionalTitleCountermodel.Institution
  proposal :
    OwnershipInstitutionalTitleCountermodel.TransferProposal

def samePossessionAccepted : PossessionInstitutionCase where
  possession := bothProfile
  institution := OwnershipInstitutionalTitleCountermodel.acceptingInstitution
  proposal := OwnershipInstitutionalTitleCountermodel.transferFalseToTrue

def samePossessionRejected : PossessionInstitutionCase where
  possession := bothProfile
  institution := OwnershipInstitutionalTitleCountermodel.rejectingInstitution
  proposal := OwnershipInstitutionalTitleCountermodel.transferFalseToTrue

theorem sameCustodyAccess_differentRegistryTitle :
    samePossessionAccepted.possession = samePossessionRejected.possession ∧
    OwnershipInstitutionalTitleCountermodel.RegistryTitle
      samePossessionAccepted.institution
      samePossessionAccepted.proposal
      true ∧
    ¬ OwnershipInstitutionalTitleCountermodel.RegistryTitle
      samePossessionRejected.institution
      samePossessionRejected.proposal
      true := by
  exact ⟨
    rfl,
    OwnershipInstitutionalTitleCountermodel.accepted_true_hasRegistryTitle,
    OwnershipInstitutionalTitleCountermodel.rejected_true_notRegistryTitle
  ⟩

theorem sameRegistryTitle_differentCustodyAccess :
    OwnershipInstitutionalTitleCountermodel.RegistryTitle
      OwnershipInstitutionalTitleCountermodel.acceptingInstitution
      OwnershipInstitutionalTitleCountermodel.transferFalseToTrue
      true ∧
    CustodyLike custodyOnlyProfile ∧
    ¬ AccessLike custodyOnlyProfile ∧
    ¬ CustodyLike accessOnlyProfile ∧
    AccessLike accessOnlyProfile := by
  exact ⟨
    OwnershipInstitutionalTitleCountermodel.accepted_true_hasRegistryTitle,
    custodyOnly_quadrant.1,
    custodyOnly_quadrant.2,
    accessOnly_quadrant.1,
    accessOnly_quadrant.2
  ⟩

structure DecoratedProfile where
  base : PossessionResponseProfile
  possessionFlag : Bit

def decoratedTrue : DecoratedProfile where
  base := bothProfile
  possessionFlag := true

def decoratedFalse : DecoratedProfile where
  base := bothProfile
  possessionFlag := false

theorem possessionLabelDeletion_custody :
    CustodyLike decoratedTrue.base ↔ CustodyLike decoratedFalse.base := by
  rfl

theorem possessionLabelDeletion_access :
    AccessLike decoratedTrue.base ↔ AccessLike decoratedFalse.base := by
  rfl

/--
Combined scoped result:
- realized snapshots can be identical across all four custody/access quadrants;
- custody-like and access-like response roles are independently variable;
- access-like use capability and current revision privilege separate both ways;
- identical custody/access structure can coexist with different registry title.
-/
theorem possessionDecomposition_bundle :
    realizedSnapshot neitherProfile = realizedSnapshot accessOnlyProfile ∧
    realizedSnapshot neitherProfile = realizedSnapshot custodyOnlyProfile ∧
    realizedSnapshot neitherProfile = realizedSnapshot bothProfile ∧
    CustodyLike custodyOnlyProfile ∧
    ¬ AccessLike custodyOnlyProfile ∧
    ¬ CustodyLike accessOnlyProfile ∧
    AccessLike accessOnlyProfile ∧
    ¬ OwnershipAuthorshipControlCountermodel.CanRevise
      accessWithoutRevisionCase.revision ∧
    OwnershipAuthorshipControlCountermodel.CanRevise
      revisionWithoutAccessCase.revision ∧
    samePossessionAccepted.possession = samePossessionRejected.possession := by
  exact ⟨
    rfl,
    rfl,
    rfl,
    custodyOnly_quadrant.1,
    custodyOnly_quadrant.2,
    accessOnly_quadrant.1,
    accessOnly_quadrant.2,
    OwnershipAuthorshipControlCountermodel.generationOnly_not_canRevise,
    OwnershipAuthorshipControlCountermodel.revisionOnly_canRevise,
    rfl
  ⟩

end PossessionCustodyAccessCountermodel

end RelayTheory
