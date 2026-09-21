namespace RelayTheory
namespace LocalPresentReindexing

abbrev Event := Bool

inductive DeicticClass where
  | here
  | past
  | future
  | elsewhere
  deriving DecidableEq

/--
Fixed two-event oriented fixture. The underlying order does not depend on the
chosen focal event.
-/
def StrictPrecedes (x y : Event) : Prop :=
  x = false ∧ y = true

/--
Deictic classification relative to an explicitly supplied focal event.
No separate local-Present field appears in this query surface.
-/
def classify (focal x : Event) : DeicticClass :=
  if x = focal then
    .here
  else if StrictPrecedes x focal then
    .past
  else if StrictPrecedes focal x then
    .future
  else
    .elsewhere

theorem false_is_here_from_false_focal :
    classify false false = .here := by
  rfl

theorem true_is_future_from_false_focal :
    classify false true = .future := by
  rfl

theorem false_is_past_from_true_focal :
    classify true false = .past := by
  rfl

theorem true_is_here_from_true_focal :
    classify true true = .here := by
  rfl

/--
The same event changes deictic class when only the focal evaluation parameter
changes; the underlying event carrier and precedence relation remain fixed.
-/
theorem same_event_changes_class_under_focal_reindexing :
    classify false false = .here ∧
    classify true false = .past := by
  exact ⟨false_is_here_from_false_focal, false_is_past_from_true_focal⟩

/--
No focal-independent unary classifier can reproduce the declared deictic
classification for both focal choices on this fixed event/order fixture.
-/
theorem no_focal_independent_classifier
    (intrinsic : Event → DeicticClass)
    (hFalseFocal : ∀ x, intrinsic x = classify false x)
    (hTrueFocal : ∀ x, intrinsic x = classify true x) :
    False := by
  have hFalse := hFalseFocal false
  have hTrue := hTrueFocal false
  have hEq : DeicticClass.here = DeicticClass.past := by
    calc
      DeicticClass.here = intrinsic false := by
        simpa using hFalse.symm
      _ = DeicticClass.past := by
        simpa using hTrue
  have hNe : DeicticClass.here ≠ DeicticClass.past := by
    decide
  exact hNe hEq

end LocalPresentReindexing
end RelayTheory
