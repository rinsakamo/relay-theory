import Lean.Elab.Tactic

namespace RelayTheory
namespace PredictiveCapacity

/--
Two histories are equivalent for a declared response surface when every
declared probe produces the same output.
-/
def ResponseEquivalent
    {History Probe Output : Type}
    (response : History → Probe → Output)
    (h₁ h₂ : History) : Prop :=
  ∀ probe, response h₁ probe = response h₂ probe

/--
An encoding is exactly sufficient when it merges only histories that are
equivalent for the declared response surface.
-/
def ExactlySufficient
    {History Probe Output Representation : Type}
    (response : History → Probe → Output)
    (encode : History → Representation) : Prop :=
  ∀ h₁ h₂, encode h₁ = encode h₂ →
    ResponseEquivalent response h₁ h₂

/--
A finite sample is pairwise separated when every two different sample indices
can be distinguished by the declared response surface.
-/
def PairwiseSeparated
    {History Probe Output : Type}
    (response : History → Probe → Output)
    {k : Nat}
    (sample : Fin k → History) : Prop :=
  ∀ i j, i ≠ j →
    ¬ ResponseEquivalent response (sample i) (sample j)

/--
Exact sufficiency forces injectivity on every pairwise separated sample.
This is the representation-independent core of the capacity bound.
-/
theorem exactlySufficient_injective_on_pairwiseSeparated
    {History Probe Output Representation : Type}
    {response : History → Probe → Output}
    {encode : History → Representation}
    {k : Nat}
    {sample : Fin k → History}
    (hsufficient : ExactlySufficient response encode)
    (hseparated : PairwiseSeparated response sample) :
    Function.Injective (fun i => encode (sample i)) := by
  intro i j hij
  apply Classical.byContradiction
  intro hne
  exact hseparated i j hne
    (hsufficient (sample i) (sample j) hij)

/--
Delete one distinguished element from Fin (n+1), shifting larger values down.
-/
def eraseFin {n : Nat}
    (pivot value : Fin (n + 1))
    (hne : value ≠ pivot) : Fin n :=
  if hlt : value.val < pivot.val then
    ⟨value.val, by omega⟩
  else
    ⟨value.val - 1, by
      have hle : pivot.val ≤ value.val := Nat.le_of_not_gt hlt
      have hvalne : value.val ≠ pivot.val := by
        intro h
        exact hne (Fin.ext h)
      omega⟩

theorem eraseFin_injective
    {n : Nat}
    (pivot : Fin (n + 1))
    {y z : Fin (n + 1)}
    (hy : y ≠ pivot)
    (hz : z ≠ pivot)
    (h : eraseFin pivot y hy = eraseFin pivot z hz) :
    y = z := by
  apply Fin.ext
  have hv := congrArg Fin.val h
  by_cases hyp : y.val < pivot.val
  · by_cases hzp : z.val < pivot.val
    · simp [eraseFin, hyp, hzp] at hv
      exact hv
    · simp [eraseFin, hyp, hzp] at hv
      have hzle : pivot.val ≤ z.val := Nat.le_of_not_gt hzp
      have hzneq : z.val ≠ pivot.val := by
        intro hzv
        exact hz (Fin.ext hzv)
      omega
  · by_cases hzp : z.val < pivot.val
    · simp [eraseFin, hyp, hzp] at hv
      have hyle : pivot.val ≤ y.val := Nat.le_of_not_gt hyp
      have hyneq : y.val ≠ pivot.val := by
        intro hyv
        exact hy (Fin.ext hyv)
      omega
    · simp [eraseFin, hyp, hzp] at hv
      have hyle : pivot.val ≤ y.val := Nat.le_of_not_gt hyp
      have hzle : pivot.val ≤ z.val := Nat.le_of_not_gt hzp
      have hyneq : y.val ≠ pivot.val := by
        intro hyv
        exact hy (Fin.ext hyv)
      have hzneq : z.val ≠ pivot.val := by
        intro hzv
        exact hz (Fin.ext hzv)
      omega

/-- There is no injective map from Fin (n+1) into Fin n. -/
theorem finSucc_not_injective :
    ∀ n : Nat, ∀ f : Fin (n + 1) → Fin n,
      ¬ Function.Injective f
  | 0, f => by
      intro _
      exact Fin.elim0 (f 0)
  | n + 1, f => by
      intro hf
      let last : Fin (n + 2) := Fin.last (n + 1)
      let pivot : Fin (n + 1) := f last
      have hneq (i : Fin (n + 1)) :
          f (Fin.castSucc i) ≠ pivot := by
        intro h
        have heq : Fin.castSucc i = last := hf h
        have hv := congrArg Fin.val heq
        have hi := i.isLt
        simp [last] at hv
        omega
      let g : Fin (n + 1) → Fin n :=
        fun i => eraseFin pivot (f (Fin.castSucc i)) (hneq i)
      have hg : Function.Injective g := by
        intro i j hij
        have hfij :
            f (Fin.castSucc i) = f (Fin.castSucc j) := by
          exact eraseFin_injective pivot (hneq i) (hneq j) hij
        have hijCast : Fin.castSucc i = Fin.castSucc j := hf hfij
        have hv : i.val = j.val := by
          change (Fin.castSucc i).val = (Fin.castSucc j).val
          exact congrArg (fun x : Fin (n + 2) => x.val) hijCast
        exact Fin.ext hv
      exact finSucc_not_injective n g hg

/--
If a declared response surface contains n+1 pairwise separated sampled
histories, no encoding into Fin n can be exactly sufficient.

This theorem is about representation capacity relative to a declared response
surface. It contains no claim about physical finitude, memory, time, cognition,
or a privileged Present.
-/
theorem no_exactFinEncoding_of_succ_pairwiseSeparated
    {History Probe Output : Type}
    {response : History → Probe → Output}
    {n : Nat}
    {sample : Fin (n + 1) → History}
    (hseparated : PairwiseSeparated response sample)
    (encode : History → Fin n) :
    ¬ ExactlySufficient response encode := by
  intro hsufficient
  have hinjective : Function.Injective (fun i => encode (sample i)) :=
    exactlySufficient_injective_on_pairwiseSeparated
      hsufficient hseparated
  exact finSucc_not_injective n
    (fun i => encode (sample i)) hinjective

end PredictiveCapacity
end RelayTheory
