import RelayTheory.ProbeFutureClosure

namespace RelayTheory
namespace GroundedPresentationDistinguishability

/-!
# Grounded presentation-safe distinguishability

This finite module separates presentation-sensitive differences from differences
that factor through an explicit grounding map into an ambient referent carrier.

The carrier identities used here are formal/modeling substrate. The module does
not interpret presentation constructors or referent values as primitive
individual identities.
-/

inductive Presentation where
  | encodedA
  | encodedB
  | encodedC
deriving DecidableEq

abbrev Referent := Bool
abbrev Outcome := Bool

inductive Probe where
  | constant
  | identity
deriving DecidableEq

inductive Interface where
  | coarse
  | fine
deriving DecidableEq

/-- Two different encodings may ground to the same formal ambient referent. -/
def ground : Presentation → Referent
  | .encodedA => false
  | .encodedB => false
  | .encodedC => true

/-- Grounded probes act on referents, not presentation metadata. -/
def response : Probe → Referent → Outcome
  | .constant, _ => false
  | .identity, referent => referent

def observeGrounded (presentation : Presentation) (probe : Probe) : Outcome :=
  response probe (ground presentation)

/-- A deliberately presentation-sensitive probe used only as a negative control. -/
def encodingProbe : Presentation → Bool
  | .encodedA => false
  | .encodedB => true
  | .encodedC => false

/-- The coarse interface admits only the constant grounded probe. -/
def accessible : Interface → Probe → Prop
  | .coarse, .constant => True
  | .coarse, .identity => False
  | .fine, _ => True

def GroundedIndistAt
    (interface : Interface)
    (left right : Presentation) : Prop :=
  ∀ probe, accessible interface probe →
    observeGrounded left probe = observeGrounded right probe

/-- Equal grounding forces equality under every grounded referent probe. -/
theorem sameGrounding_sameGroundedObservation
    {left right : Presentation}
    (hGround : ground left = ground right) :
    ∀ probe, observeGrounded left probe = observeGrounded right probe := by
  intro probe
  exact congrArg (response probe) hGround

/--
A grounded outcome difference entails a difference in the grounding result.
The referent inequality is concluded from the discriminator rather than assumed.
-/
theorem groundedOutcomeDifference_impliesGroundDifference
    {left right : Presentation}
    {probe : Probe}
    (hDifference :
      observeGrounded left probe ≠ observeGrounded right probe) :
    ground left ≠ ground right := by
  intro hGround
  apply hDifference
  exact congrArg (response probe) hGround

/-- Re-encoding that preserves grounding preserves the entire grounded profile. -/
theorem sameGrounding_sameGroundedProfile
    {left right : Presentation}
    (hGround : ground left = ground right) :
    (fun probe => observeGrounded left probe) =
      (fun probe => observeGrounded right probe) := by
  funext probe
  exact sameGrounding_sameGroundedObservation hGround probe

theorem encodedA_encodedB_sameGrounding :
    ground .encodedA = ground .encodedB := by
  rfl

/--
The two encodings are presentation-distinguishable even though they ground to
the same referent.
-/
theorem encodingProbe_separates_sameGrounding :
    encodingProbe .encodedA ≠ encodingProbe .encodedB ∧
    ground .encodedA = ground .encodedB := by
  constructor
  · intro h
    exact Bool.noConfusion h
  · rfl

/--
Presentation-sensitive separation does not survive the grounded observation
surface for two encodings of the same referent.
-/
theorem sameReferent_encodings_groundedlyIndistinguishable :
    GroundedIndistAt .fine .encodedA .encodedB := by
  intro probe _
  exact sameGrounding_sameGroundedObservation
    encodedA_encodedB_sameGrounding probe

/-- The coarse interface cannot separate encodedA from encodedC. -/
theorem coarse_indistinguishable :
    GroundedIndistAt .coarse .encodedA .encodedC := by
  intro probe hAccessible
  cases probe with
  | constant => rfl
  | identity => exact False.elim hAccessible

/-- The fine interface exposes one grounded probe that separates them. -/
theorem fine_distinguishable :
    ¬ GroundedIndistAt .fine .encodedA .encodedC := by
  intro hIndist
  have h := hIndist .identity trivial
  change false = true at h
  exact Bool.noConfusion h

/-- The positive-control grounded outcome difference. -/
theorem identityProbe_groundedDifference :
    observeGrounded .encodedA .identity ≠
      observeGrounded .encodedC .identity := by
  intro h
  exact Bool.noConfusion h

/--
The formal referent difference in the positive control is derived from the
grounded probe outcome difference.
-/
theorem derivedGroundDifference :
    ground .encodedA ≠ ground .encodedC :=
  groundedOutcomeDifference_impliesGroundDifference
    identityProbe_groundedDifference

/-- More accessible grounded probes induce a finer indistinguishability. -/
theorem groundedIndist_of_access_inclusion
    {coarseInterface fineInterface : Interface}
    {left right : Presentation}
    (hInclude :
      ∀ probe,
        accessible coarseInterface probe →
        accessible fineInterface probe)
    (hFine : GroundedIndistAt fineInterface left right) :
    GroundedIndistAt coarseInterface left right := by
  intro probe hProbe
  exact hFine probe (hInclude probe hProbe)

theorem coarse_access_included_in_fine :
    ∀ probe, accessible .coarse probe → accessible .fine probe := by
  intro probe _
  trivial

theorem fine_indist_implies_coarse_indist
    {left right : Presentation}
    (hFine : GroundedIndistAt .fine left right) :
    GroundedIndistAt .coarse left right :=
  groundedIndist_of_access_inclusion coarse_access_included_in_fine hFine

/--
Decorative interface metadata does not alter the underlying grounded access
profile when the actual interface is fixed.
-/
abbrev DecoratedInterface := Interface × Bool

def decoratedAccessible
    (decorated : DecoratedInterface)
    (probe : Probe) : Prop :=
  accessible decorated.1 probe

theorem decorativeInterfaceTag_irrelevant
    (interface : Interface)
    (leftTag rightTag : Bool) :
    ∀ probe,
      decoratedAccessible (interface, leftTag) probe ↔
      decoratedAccessible (interface, rightTag) probe := by
  intro probe
  rfl

/--
An explicit identity-like token carried by a presentation. The token is
deliberately absent from grounding and grounded response semantics so that the
formalization can test whether such a field can do hidden classification work.
-/
abbrev IdentityToken := Bool

structure TokenizedPresentation where
  presentation : Presentation
  identityToken : IdentityToken
deriving DecidableEq

def tokenizedGround (tokenized : TokenizedPresentation) : Referent :=
  ground tokenized.presentation

def observeTokenizedGrounded
    (tokenized : TokenizedPresentation)
    (probe : Probe) : Outcome :=
  response probe (tokenizedGround tokenized)

def TokenizedGroundedIndistAt
    (interface : Interface)
    (left right : TokenizedPresentation) : Prop :=
  ∀ probe, accessible interface probe →
    observeTokenizedGrounded left probe =
      observeTokenizedGrounded right probe

/--
Adding an explicit identity token does not change the grounded classification:
for fixed presentations, the tokenized relation is definitionally the same as
the original grounded indistinguishability relation.
-/
theorem tokenizedGroundedIndist_iff_base
    (interface : Interface)
    (left right : Presentation)
    (leftToken rightToken : IdentityToken) :
    TokenizedGroundedIndistAt
      interface
      ⟨left, leftToken⟩
      ⟨right, rightToken⟩ ↔
    GroundedIndistAt interface left right := by
  rfl

/--
Arbitrary reassignment of explicit identity tokens cannot change the grounded
operational classification when the presentations, grounding, admitted probes,
and grounded response semantics are fixed.
-/
theorem identityToken_variation_preserves_groundedClassification
    (interface : Interface)
    (left right : Presentation)
    (leftToken₁ leftToken₂ rightToken₁ rightToken₂ : IdentityToken) :
    TokenizedGroundedIndistAt
      interface
      ⟨left, leftToken₁⟩
      ⟨right, rightToken₁⟩ ↔
    TokenizedGroundedIndistAt
      interface
      ⟨left, leftToken₂⟩
      ⟨right, rightToken₂⟩ := by
  rfl

/--
Concrete negative control: different explicit identity tokens do not separate
two encodings that share the same grounding.
-/
theorem differentIdentityTokens_sameGroundedClassification :
    TokenizedGroundedIndistAt
      .fine
      ⟨.encodedA, false⟩
      ⟨.encodedB, true⟩ := by
  exact
    (tokenizedGroundedIndist_iff_base
      .fine .encodedA .encodedB false true).2
      sameReferent_encodings_groundedlyIndistinguishable

/--
Positive contrast: an identity token cannot mask a target-sensitive grounded
difference already exposed by the admitted probes.
-/
theorem identityTokenCannotMask_groundedDifference :
    ¬ TokenizedGroundedIndistAt
      .fine
      ⟨.encodedA, true⟩
      ⟨.encodedC, true⟩ := by
  intro hTokenized
  have hBase :
      GroundedIndistAt .fine .encodedA .encodedC :=
    (tokenizedGroundedIndist_iff_base
      .fine .encodedA .encodedC true true).1 hTokenized
  exact fine_distinguishable hBase

/--
Scoped bundle: presentation metadata can differ without grounded separation;
coarse access can fail to distinguish; richer grounded access can distinguish;
and the positive-control referent difference is derived from a grounded
response difference.
-/
theorem groundedPresentationSafeBundle :
    encodingProbe .encodedA ≠ encodingProbe .encodedB ∧
    GroundedIndistAt .fine .encodedA .encodedB ∧
    GroundedIndistAt .coarse .encodedA .encodedC ∧
    ¬ GroundedIndistAt .fine .encodedA .encodedC ∧
    ground .encodedA ≠ ground .encodedC := by
  exact ⟨
    encodingProbe_separates_sameGrounding.1,
    sameReferent_encodings_groundedlyIndistinguishable,
    coarse_indistinguishable,
    fine_distinguishable,
    derivedGroundDifference
  ⟩

end GroundedPresentationDistinguishability
end RelayTheory
