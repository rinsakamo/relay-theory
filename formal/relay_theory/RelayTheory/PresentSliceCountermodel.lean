namespace RelayTheory
namespace PresentSliceCountermodel

abbrev Event := Fin 3
abbrev Slice := Event → Prop

/--
Finite precedence fixture:
0 precedes 1; event 2 is incomparable with both 0 and 1.
Reflexive edges are included for the partial-order presentation.
-/
def Precedes (x y : Event) : Prop :=
  x = y ∨ (x = (0 : Event) ∧ y = (1 : Event))

def StrictPrecedes (x y : Event) : Prop :=
  Precedes x y ∧ x ≠ y

def Incomparable (x y : Event) : Prop :=
  ¬ StrictPrecedes x y ∧ ¬ StrictPrecedes y x

def focal : Event := 2

def PairwiseIncomparable (s : Slice) : Prop :=
  ∀ x y, s x → s y → x ≠ y → Incomparable x y

/--
A slice is maximal around the focal event when it contains the focal event,
its members are pairwise incomparable, and every excluded event conflicts
with at least one included event.
-/
def MaximalAroundFocal (s : Slice) : Prop :=
  s focal ∧
  PairwiseIncomparable s ∧
  ∀ z, ¬ s z →
    ∃ x, s x ∧ ¬ Incomparable x z

def sliceA (x : Event) : Prop :=
  x = (0 : Event) ∨ x = focal

def sliceB (x : Event) : Prop :=
  x = (1 : Event) ∨ x = focal

theorem precedence_refl :
    ∀ x : Event, Precedes x x := by
  intro x
  exact Or.inl rfl

theorem precedence_antisymm :
    ∀ x y : Event, Precedes x y → Precedes y x → x = y := by
  intro x y hxy hyx
  rcases hxy with hEq | h01
  · exact hEq
  · rcases h01 with ⟨hx, hy⟩
    subst x
    subst y
    have hnot : ¬ Precedes (1 : Event) (0 : Event) := by
      simp [Precedes]
    exact False.elim (hnot hyx)

theorem precedence_trans :
    ∀ x y z : Event, Precedes x y → Precedes y z → Precedes x z := by
  intro x y z hxy hyz
  rcases hxy with hEq | h01
  · subst y
    exact hyz
  · rcases h01 with ⟨hx, hy⟩
    subst x
    subst y
    have hz : z = (1 : Event) := by
      rcases hyz with hyzEq | hbad
      · exact hyzEq.symm
      · have h10 : (1 : Event) ≠ (0 : Event) := by decide
        exact False.elim (h10 hbad.1)
    subst z
    exact Or.inr ⟨rfl, rfl⟩

theorem strict_zero_one :
    StrictPrecedes (0 : Event) (1 : Event) := by
  constructor
  · exact Or.inr ⟨rfl, rfl⟩
  · decide

theorem incomparable_zero_focal :
    Incomparable (0 : Event) focal := by
  constructor
  · intro h
    exact h.1.elim
      (fun h02 => by cases h02)
      (fun h => by
        have h21 : focal ≠ (1 : Event) := by decide
        exact h21 h.2)
  · intro h
    exact h.1.elim
      (fun h20 => by cases h20)
      (fun h => by
        have h20 : focal ≠ (0 : Event) := by decide
        exact h20 h.1)

theorem incomparable_one_focal :
    Incomparable (1 : Event) focal := by
  constructor
  · intro h
    exact h.1.elim
      (fun h12 => by cases h12)
      (fun h => by
        have h10 : (1 : Event) ≠ (0 : Event) := by decide
        exact h10 h.1)
  · intro h
    exact h.1.elim
      (fun h21 => by cases h21)
      (fun h => by
        have h20 : focal ≠ (0 : Event) := by decide
        exact h20 h.1)

theorem incomparable_symm {x y : Event}
    (h : Incomparable x y) : Incomparable y x := by
  exact ⟨h.2, h.1⟩

theorem sliceA_pairwise :
    PairwiseIncomparable sliceA := by
  intro x y hx hy hne
  rcases hx with rfl | rfl
  · rcases hy with rfl | rfl
    · exact False.elim (hne rfl)
    · exact incomparable_zero_focal
  · rcases hy with rfl | rfl
    · exact incomparable_symm incomparable_zero_focal
    · exact False.elim (hne rfl)

theorem sliceB_pairwise :
    PairwiseIncomparable sliceB := by
  intro x y hx hy hne
  rcases hx with rfl | rfl
  · rcases hy with rfl | rfl
    · exact False.elim (hne rfl)
    · exact incomparable_one_focal
  · rcases hy with rfl | rfl
    · exact incomparable_symm incomparable_one_focal
    · exact False.elim (hne rfl)

theorem sliceA_maximal :
    MaximalAroundFocal sliceA := by
  refine ⟨Or.inr rfl, sliceA_pairwise, ?_⟩
  intro z hz
  have hz0 : z ≠ (0 : Event) := by
    intro h
    exact hz (Or.inl h)
  have hzf : z ≠ focal := by
    intro h
    exact hz (Or.inr h)
  have hz0val : z.val ≠ 0 := by
    intro h
    exact hz0 (Fin.ext h)
  have hzfval : z.val ≠ 2 := by
    intro h
    apply hzf
    apply Fin.ext
    simpa [focal] using h
  have hz1val : z.val = 1 := by
    have hlt := z.isLt
    omega
  have hz1 : z = (1 : Event) := Fin.ext hz1val
  subst z
  refine ⟨(0 : Event), Or.inl rfl, ?_⟩
  intro hinc
  exact hinc.1 strict_zero_one

theorem sliceB_maximal :
    MaximalAroundFocal sliceB := by
  refine ⟨Or.inr rfl, sliceB_pairwise, ?_⟩
  intro z hz
  have hz1 : z ≠ (1 : Event) := by
    intro h
    exact hz (Or.inl h)
  have hzf : z ≠ focal := by
    intro h
    exact hz (Or.inr h)
  have hz1val : z.val ≠ 1 := by
    intro h
    exact hz1 (Fin.ext h)
  have hzfval : z.val ≠ 2 := by
    intro h
    apply hzf
    apply Fin.ext
    simpa [focal] using h
  have hz0val : z.val = 0 := by
    have hlt := z.isLt
    omega
  have hz0 : z = (0 : Event) := Fin.ext hz0val
  subst z
  refine ⟨(1 : Event), Or.inl rfl, ?_⟩
  intro hinc
  exact hinc.2 strict_zero_one

theorem slices_disagree_on_zero :
    sliceA (0 : Event) ∧ ¬ sliceB (0 : Event) := by
  constructor
  · exact Or.inl rfl
  · intro h
    rcases h with h01 | h02
    · have h : (0 : Event) ≠ (1 : Event) := by decide
      exact h h01
    · have h : (0 : Event) ≠ focal := by decide
      exact h h02

/--
The same finite partial order and the same focal event support two different
maximal incomparable slices through that focal event. Therefore those lower
level data do not select one unique global slice.
-/
theorem same_order_and_focal_do_not_select_unique_slice :
    ∃ s t : Slice,
      MaximalAroundFocal s ∧
      MaximalAroundFocal t ∧
      s (0 : Event) ∧
      ¬ t (0 : Event) := by
  exact ⟨sliceA, sliceB, sliceA_maximal, sliceB_maximal,
    slices_disagree_on_zero.1, slices_disagree_on_zero.2⟩

end PresentSliceCountermodel
end RelayTheory
