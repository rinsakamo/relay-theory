namespace RelayTheory
namespace PresentSliceCountermodel

abbrev Event := Fin 3
abbrev Slice := Event → Bool

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

def inSlice (s : Slice) (x : Event) : Prop :=
  s x = true

def PairwiseIncomparable (s : Slice) : Prop :=
  ∀ x y,
    inSlice s x →
    inSlice s y →
    x ≠ y →
    Incomparable x y

/--
A slice is maximal around the focal event when it contains the focal event,
its members are pairwise incomparable, and every excluded event conflicts
with at least one included event.
-/
def MaximalAroundFocal (s : Slice) : Prop :=
  inSlice s focal ∧
  PairwiseIncomparable s ∧
  ∀ z, ¬ inSlice s z →
    ∃ x, inSlice s x ∧ ¬ Incomparable x z

def sliceA (x : Event) : Bool :=
  decide (x = (0 : Event) ∨ x = focal)

def sliceB (x : Event) : Bool :=
  decide (x = (1 : Event) ∨ x = focal)

theorem precedence_refl :
    ∀ x : Event, Precedes x x := by
  intro x
  exact Or.inl rfl

theorem precedence_antisymm :
    ∀ x y : Event, Precedes x y → Precedes y x → x = y := by
  decide

theorem precedence_trans :
    ∀ x y z : Event, Precedes x y → Precedes y z → Precedes x z := by
  decide

theorem focal_incomparable_with_zero :
    Incomparable focal (0 : Event) := by
  decide

theorem focal_incomparable_with_one :
    Incomparable focal (1 : Event) := by
  decide

theorem sliceA_maximal :
    MaximalAroundFocal sliceA := by
  decide

theorem sliceB_maximal :
    MaximalAroundFocal sliceB := by
  decide

theorem slices_disagree_on_zero :
    sliceA (0 : Event) ≠ sliceB (0 : Event) := by
  decide

/--
The same finite partial order and the same focal event support two different
maximal incomparable slices through that focal event. Therefore those lower
level data do not select one unique global slice.
-/
theorem same_order_and_focal_do_not_select_unique_slice :
    ∃ s t : Slice,
      MaximalAroundFocal s ∧
      MaximalAroundFocal t ∧
      s (0 : Event) ≠ t (0 : Event) := by
  exact ⟨sliceA, sliceB, sliceA_maximal, sliceB_maximal,
    slices_disagree_on_zero⟩

end PresentSliceCountermodel
end RelayTheory
