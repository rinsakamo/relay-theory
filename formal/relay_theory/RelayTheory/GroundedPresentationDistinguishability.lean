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
A structural target-factorization condition for a presentation-level feature.
The value carrier is arbitrary. This object records only that the feature
factors through the grounding map; it does not provide empirical or epistemic
warrant for accepting that factorization in a scientific application.
-/
structure GroundingFactorization
    {Value : Type}
    (feature : Presentation → Value) where
  targetProperty : Referent → Value
  sound : ∀ presentation,
    feature presentation = targetProperty (ground presentation)

/--
Backward-compatible name for the structural factorization object. Manuscript
prose calls this a target-factorization condition rather than an evidential
warrant.
-/
abbrev GroundingBridge
    {Value : Type}
    (feature : Presentation → Value) :=
  GroundingFactorization feature

/--
If a presentation-level feature factors through grounding, equal grounding
forces equal feature values.
-/
theorem bridgedFeature_sameGrounding_sameValue
    {Value : Type}
    {feature : Presentation → Value}
    (bridge : GroundingFactorization feature)
    {left right : Presentation}
    (hGround : ground left = ground right) :
    feature left = feature right := by
  calc
    feature left = bridge.targetProperty (ground left) := bridge.sound left
    _ = bridge.targetProperty (ground right) :=
      congrArg bridge.targetProperty hGround
    _ = feature right := (bridge.sound right).symm

/--
A difference in a structurally factorized presentation feature entails a
difference in the grounding result.
-/
theorem bridgedFeatureDifference_impliesGroundDifference
    {Value : Type}
    {feature : Presentation → Value}
    (bridge : GroundingFactorization feature)
    {left right : Presentation}
    (hFeature : feature left ≠ feature right) :
    ground left ≠ ground right := by
  intro hGround
  exact hFeature (bridgedFeature_sameGrounding_sameValue bridge hGround)

/--
The deliberately presentation-sensitive encoding probe cannot satisfy target
factorization: it separates two presentations that have equal grounding.
-/
theorem encodingProbe_hasNoGroundingBridge :
    ¬ Nonempty (GroundingFactorization encodingProbe) := by
  intro hBridge
  rcases hBridge with ⟨bridge⟩
  have hSame : encodingProbe .encodedA = encodingProbe .encodedB :=
    bridgedFeature_sameGrounding_sameValue
      bridge encodedA_encodedB_sameGrounding
  exact encodingProbe_separates_sameGrounding.1 hSame

/-- A positive-control feature that exactly tracks the grounding result. -/
def groundFeature : Presentation → Referent := fun presentation =>
  ground presentation

/-- The positive-control ground-tracking feature satisfies target factorization. -/
theorem groundFeature_hasGroundingBridge :
    Nonempty (GroundingFactorization groundFeature) := by
  refine ⟨{ targetProperty := fun referent => referent, sound := ?_ }⟩
  intro presentation
  rfl

/--
A test-specific structural factorization between an observed presentation
surface and the target-level response function. This unifies the feature bridge
with the restricted-test layer: an observed outcome is target-factorized only
when it agrees with the response of the grounded referent.
-/
structure ObservationFactorization
    (observed : Presentation → Probe → Outcome) where
  sound : ∀ presentation probe,
    observed presentation probe =
      response probe (ground presentation)

/-- The built-in grounded observation surface satisfies test factorization. -/
theorem observeGrounded_hasObservationFactorization :
    Nonempty (ObservationFactorization observeGrounded) := by
  refine ⟨{ sound := ?_ }⟩
  intro presentation probe
  rfl

/--
For any observed presentation surface satisfying test factorization, a
difference under one probe entails a difference in the grounding result.
-/
theorem factorizedObservedDifference_impliesGroundDifference
    {observed : Presentation → Probe → Outcome}
    (bridge : ObservationFactorization observed)
    {left right : Presentation}
    {probe : Probe}
    (hDifference : observed left probe ≠ observed right probe) :
    ground left ≠ ground right := by
  intro hGround
  apply hDifference
  calc
    observed left probe = response probe (ground left) :=
      bridge.sound left probe
    _ = response probe (ground right) :=
      congrArg (response probe) hGround
    _ = observed right probe :=
      (bridge.sound right probe).symm

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
A presentation may carry arbitrary identity-like metadata. The token carrier is
fully polymorphic: no property of the token type is used by grounded semantics.
-/
structure TokenizedPresentation (Token : Type) where
  presentation : Presentation
  token : Token

/-- Grounded observation ignores identity-like metadata by construction. -/
def tokenizedObserveGrounded {Token : Type}
    (value : TokenizedPresentation Token)
    (probe : Probe) : Outcome :=
  observeGrounded value.presentation probe

def TokenizedGroundedIndistAt {Token : Type}
    (interface : Interface)
    (left right : TokenizedPresentation Token) : Prop :=
  ∀ probe, accessible interface probe →
    tokenizedObserveGrounded left probe =
      tokenizedObserveGrounded right probe

/--
For any token carrier, adding semantically inert identity-like metadata leaves
the base grounded classification unchanged.
-/
theorem tokenizedGroundedIndist_iff_base
    {Token : Type}
    (interface : Interface)
    (left right : TokenizedPresentation Token) :
    TokenizedGroundedIndistAt interface left right ↔
      GroundedIndistAt interface left.presentation right.presentation := by
  rfl

/--
For any token carrier, arbitrary reassignment of semantically inert tokens
preserves the grounded classification of fixed underlying presentations.
-/
theorem identityToken_variation_preserves_groundedClassification
    {Token : Type}
    (interface : Interface)
    (left right : Presentation)
    (leftToken rightToken leftToken' rightToken' : Token) :
    TokenizedGroundedIndistAt interface
        ⟨left, leftToken⟩ ⟨right, rightToken⟩ ↔
      TokenizedGroundedIndistAt interface
        ⟨left, leftToken'⟩ ⟨right, rightToken'⟩ := by
  rfl

/--
Concrete negative control: two different Boolean token values do not separate
the two same-reference encodings.
-/
theorem differentIdentityTokens_sameGroundedClassification :
    TokenizedGroundedIndistAt .fine
      (TokenizedPresentation.mk .encodedA false)
      (TokenizedPresentation.mk .encodedB true) := by
  exact
    (tokenizedGroundedIndist_iff_base .fine
      (TokenizedPresentation.mk .encodedA false)
      (TokenizedPresentation.mk .encodedB true)).2
      sameReferent_encodings_groundedlyIndistinguishable

/--
For any token carrier, assigning the same token cannot mask a grounded
difference that the admitted tests already expose.
-/
theorem identityTokenCannotMask_groundedDifference
    {Token : Type}
    (token : Token) :
    ¬ TokenizedGroundedIndistAt .fine
      (TokenizedPresentation.mk .encodedA token)
      (TokenizedPresentation.mk .encodedC token) := by
  intro hTokenized
  have hBase :
      GroundedIndistAt .fine .encodedA .encodedC :=
    (tokenizedGroundedIndist_iff_base .fine
      (TokenizedPresentation.mk .encodedA token)
      (TokenizedPresentation.mk .encodedC token)).1 hTokenized
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
