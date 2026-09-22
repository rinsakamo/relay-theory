namespace RelayTheory
namespace JointRecoveryCountermodel

abbrev Source := Bool
abbrev Mask := Bool
abbrev LocalOutput := Bool
abbrev JointOutput := Bool × Bool

/--
A minimal deterministic split-access encoding. The mask is ordinary input
structure, not an ontological hidden carrier.

For source `s` and mask `r`:

* first output = `r`;
* second output = `r` when `s=false`, and `not r` when `s=true`.

The pair therefore carries a parity distinction that neither coordinate alone
must determine.
-/
def encode (s : Source) (r : Mask) : JointOutput :=
  (r, if s = true then !r else r)

def firstAccess (s : Source) (r : Mask) : LocalOutput :=
  (encode s r).1

def secondAccess (s : Source) (r : Mask) : LocalOutput :=
  (encode s r).2

/-- A local decoder is exact only if it recovers every source for every mask. -/
def ExactLocalDecoder
    (observe : Source → Mask → LocalOutput)
    (decode : LocalOutput → Source) : Prop :=
  ∀ s r, decode (observe s r) = s

/-- Every first-coordinate output is compatible with every source value. -/
theorem firstAccess_every_output_compatible
    (s : Source) (out : LocalOutput) :
    ∃ r, firstAccess s r = out := by
  exact ⟨out, by simp [firstAccess, encode]⟩

/-- Every second-coordinate output is also compatible with every source value. -/
theorem secondAccess_every_output_compatible
    (s : Source) (out : LocalOutput) :
    ∃ r, secondAccess s r = out := by
  cases s <;> cases out
  · exact ⟨false, by simp [secondAccess, encode]⟩
  · exact ⟨true, by simp [secondAccess, encode]⟩
  · exact ⟨true, by simp [secondAccess, encode]⟩
  · exact ⟨false, by simp [secondAccess, encode]⟩

/--
The first marginal admits no decoder that exactly recovers the source across
all allowed source/mask pairs.
-/
theorem no_exact_first_marginal_decoder :
    ¬ ∃ decode : LocalOutput → Source,
      ExactLocalDecoder firstAccess decode := by
  rintro ⟨decode, hDecode⟩
  have hFalse := hDecode false false
  have hTrue := hDecode true false
  simp [ExactLocalDecoder, firstAccess, encode] at hFalse hTrue
  have hImpossible : (false : Bool) = true := hFalse.symm.trans hTrue
  cases hImpossible

/--
The second marginal likewise admits no universally exact source decoder.
-/
theorem no_exact_second_marginal_decoder :
    ¬ ∃ decode : LocalOutput → Source,
      ExactLocalDecoder secondAccess decode := by
  rintro ⟨decode, hDecode⟩
  have hFalse := hDecode false false
  have hTrue := hDecode true true
  simp [ExactLocalDecoder, secondAccess, encode] at hFalse hTrue
  have hImpossible : (false : Bool) = true := hFalse.symm.trans hTrue
  cases hImpossible

/-- Joint parity decoder. -/
def jointDecode (out : JointOutput) : Source :=
  if out.1 = out.2 then false else true

/-- The joint output exactly recovers the source for every mask. -/
theorem jointDecode_recovers_source
    (s : Source) (r : Mask) :
    jointDecode (encode s r) = s := by
  cases s <;> cases r <;> simp [jointDecode, encode]

/--
Same-support control for the first marginal: changing the source does not
remove or add any possible local output.
-/
theorem firstAccess_same_support
    (s₁ s₂ : Source) (out : LocalOutput) :
    (∃ r, firstAccess s₁ r = out) ↔
    (∃ r, firstAccess s₂ r = out) := by
  constructor
  · intro _
    exact firstAccess_every_output_compatible s₂ out
  · intro _
    exact firstAccess_every_output_compatible s₁ out

/-- Same-support control for the second marginal. -/
theorem secondAccess_same_support
    (s₁ s₂ : Source) (out : LocalOutput) :
    (∃ r, secondAccess s₁ r = out) ↔
    (∃ r, secondAccess s₂ r = out) := by
  constructor
  · intro _
    exact secondAccess_every_output_compatible s₂ out
  · intro _
    exact secondAccess_every_output_compatible s₁ out

/--
Level-B structural bundle: each marginal is individually insufficient for
universal exact recovery, while the joint pair remains exactly decodable.

This is a deterministic possibility/recoverability result. It does not assert
equality or independence of probability laws.
-/
theorem joint_recovery_without_recovering_marginal_bundle :
    (¬ ∃ decode : LocalOutput → Source,
      ExactLocalDecoder firstAccess decode) ∧
    (¬ ∃ decode : LocalOutput → Source,
      ExactLocalDecoder secondAccess decode) ∧
    (∀ s r, jointDecode (encode s r) = s) := by
  exact ⟨
    no_exact_first_marginal_decoder,
    no_exact_second_marginal_decoder,
    jointDecode_recovers_source
  ⟩

end JointRecoveryCountermodel
end RelayTheory
