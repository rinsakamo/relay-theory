import RelayTheory.FocalMembershipIntegrationCountermodel

namespace RelayTheory

namespace NestedCandidateScaleCountermodel

/-!
This finite module tests the #113 nested-candidate scale discriminator.

It deliberately avoids organismic, Selfhood, maintenance, recovery, and
persistence semantics. The only qualification surface is:

* bidirectional functional integration reconstructed by #71 from response
  sensitivity; and
* criterion-relative robustness using the #108 response-under-perturbation
  shape.

The target is classification-versus-selection: two properly nested candidate
loci can both satisfy the same qualification predicate.
-/

abbrev Bit := Bool
abbrev Candidate := Bit → Prop
abbrev Perturbation := Bool
abbrev State := Bool

inductive CandidateKey
  | inner
  | outer
deriving DecidableEq

/-- Two explicit candidate loci over the same finite carrier. -/
def member : CandidateKey → Candidate
  | .inner => fun x => x = false
  | .outer => fun _ => True

/-- Proper nesting is inclusion plus at least one outer-only carrier point. -/
def ProperlyNested (inner outer : Candidate) : Prop :=
  (∀ x, inner x → outer x) ∧
  ∃ x, outer x ∧ ¬ inner x

theorem innerProperlyNestedOuter :
    ProperlyNested (member .inner) (member .outer) := by
  constructor
  · intro x hx
    trivial
  · refine ⟨true, ?_, ?_⟩
    · trivial
    · intro h
      cases h

theorem inner_ne_outer : CandidateKey.inner ≠ CandidateKey.outer := by
  intro h
  cases h

/--
Both candidate loci are assigned the same lower-level bidirectional response
profile from #71. No scale preference is encoded in this surface.
-/
def integrationSurface :
    CandidateKey →
      FocalMembershipIntegrationCountermodel.CandidateComponent
  | .inner => FocalMembershipIntegrationCountermodel.outsideIntegrated
  | .outer => FocalMembershipIntegrationCountermodel.outsideIntegrated

def Integrated (k : CandidateKey) : Prop :=
  FocalMembershipIntegrationCountermodel.FunctionallyIntegrated
    (integrationSurface k)

theorem sameIntegrationSurface :
    integrationSurface .inner = integrationSurface .outer := by
  rfl

theorem innerIntegrated : Integrated .inner := by
  exact FocalMembershipIntegrationCountermodel.outsideIntegrated_quadrant.2

theorem outerIntegrated : Integrated .outer := by
  exact FocalMembershipIntegrationCountermodel.outsideIntegrated_quadrant.2

/--
The explicit evaluation criterion and response-under-perturbation surface use
the same operational robustness shape recorded by #108.
-/
def acceptable (s : State) : Prop :=
  s = true

def responseUnder : CandidateKey → Perturbation → State
  | .inner, _ => true
  | .outer, _ => true

def CriterionRobust (k : CandidateKey) : Prop :=
  ∀ p, acceptable (responseUnder k p)

theorem sameCriterionSurface :
    ∀ p, responseUnder .inner p = responseUnder .outer p := by
  intro p
  rfl

theorem innerCriterionRobust : CriterionRobust .inner := by
  intro p
  rfl

theorem outerCriterionRobust : CriterionRobust .outer := by
  intro p
  rfl

def Qualifies (k : CandidateKey) : Prop :=
  Integrated k ∧ CriterionRobust k

theorem innerQualifies : Qualifies .inner := by
  exact ⟨innerIntegrated, innerCriterionRobust⟩

theorem outerQualifies : Qualifies .outer := by
  exact ⟨outerIntegrated, outerCriterionRobust⟩

/--
Finite counterexample to unique candidate-scale selection from the tested
integration-plus-criterion-robustness qualification surface.
-/
theorem nestedDistinctQualifiers :
    ∃ k₁ k₂ : CandidateKey,
      k₁ ≠ k₂ ∧
      ProperlyNested (member k₁) (member k₂) ∧
      Qualifies k₁ ∧
      Qualifies k₂ := by
  exact ⟨
    .inner,
    .outer,
    inner_ne_outer,
    innerProperlyNestedOuter,
    innerQualifies,
    outerQualifies
  ⟩

theorem noUniqueQualifier :
    ¬ (∃! k : CandidateKey, Qualifies k) := by
  intro h
  rcases h with ⟨winner, hwinner, hunique⟩
  have hInner : CandidateKey.inner = winner :=
    hunique .inner innerQualifies
  have hOuter : CandidateKey.outer = winner :=
    hunique .outer outerQualifies
  exact inner_ne_outer (hInner.trans hOuter.symm)

/--
The scoped discriminator: candidate classification is available for both
nested loci, while unique selection is not supplied by the same qualification
surface.
-/
theorem classificationSelectionSplit :
    Qualifies .inner ∧
    Qualifies .outer ∧
    ¬ (∃! k : CandidateKey, Qualifies k) := by
  exact ⟨innerQualifies, outerQualifies, noUniqueQualifier⟩

end NestedCandidateScaleCountermodel

end RelayTheory
