import RelayTheory.ProbeFutureClosure

namespace RelayTheory
namespace ConceptProbeQuotient

abbrev Carrier := Bool × Bool
abbrev Output := Bool
abbrev Family := (Carrier → Output) → Prop

def firstProbe (value : Carrier) : Output := value.1
def secondProbe (value : Carrier) : Output := value.2

def FirstFamily : Family :=
  ProbeFutureClosure.SingletonFamily firstProbe

def SecondFamily : Family :=
  ProbeFutureClosure.SingletonFamily secondProbe

def x : Carrier := (false, false)
def y : Carrier := (false, true)
def z : Carrier := (true, false)

def ClassOf
    (family : Family)
    (anchor candidate : Carrier) : Prop :=
  ProbeFutureClosure.ProbeEq family anchor candidate

theorem first_xy_equivalent :
    ClassOf FirstFamily x y := by
  intro probe hProbe
  change probe = firstProbe at hProbe
  subst probe
  rfl

theorem second_xy_not_equivalent :
    ¬ ClassOf SecondFamily x y := by
  intro hEq
  have h := hEq secondProbe (by rfl)
  change false = true at h
  exact Bool.noConfusion h

theorem second_xz_equivalent :
    ClassOf SecondFamily x z := by
  intro probe hProbe
  change probe = secondProbe at hProbe
  subst probe
  rfl

theorem first_xz_not_equivalent :
    ¬ ClassOf FirstFamily x z := by
  intro hEq
  have h := hEq firstProbe (by rfl)
  change false = true at h
  exact Bool.noConfusion h

theorem sameCarrier_differentFamilies_differentClasses :
    ClassOf FirstFamily x y ∧
    ¬ ClassOf SecondFamily x y ∧
    ClassOf SecondFamily x z ∧
    ¬ ClassOf FirstFamily x z := by
  exact ⟨
    first_xy_equivalent,
    second_xy_not_equivalent,
    second_xz_equivalent,
    first_xz_not_equivalent
  ⟩

theorem classOf_is_probeEq
    (family : Family)
    (anchor candidate : Carrier) :
    ClassOf family anchor candidate ↔
      ProbeFutureClosure.ProbeEq family anchor candidate := by
  rfl

theorem probeEq_congr_family
    (first second : Family)
    (hFamily : ∀ probe, first probe ↔ second probe)
    (left right : Carrier) :
    ProbeFutureClosure.ProbeEq first left right ↔
      ProbeFutureClosure.ProbeEq second left right := by
  constructor
  · intro hEq probe hSecond
    exact hEq probe ((hFamily probe).mpr hSecond)
  · intro hEq probe hFirst
    exact hEq probe ((hFamily probe).mp hFirst)

theorem classOf_congr_family
    (first second : Family)
    (hFamily : ∀ probe, first probe ↔ second probe)
    (anchor candidate : Carrier) :
    ClassOf first anchor candidate ↔
      ClassOf second anchor candidate := by
  exact probeEq_congr_family first second hFamily anchor candidate

theorem concept_like_quotient_bundle :
    ClassOf FirstFamily x y ∧
    ¬ ClassOf SecondFamily x y ∧
    ClassOf SecondFamily x z ∧
    ¬ ClassOf FirstFamily x z ∧
    (∀ family anchor candidate,
      ClassOf family anchor candidate ↔
        ProbeFutureClosure.ProbeEq family anchor candidate) := by
  refine ⟨
    first_xy_equivalent,
    second_xy_not_equivalent,
    second_xz_equivalent,
    first_xz_not_equivalent,
    ?_
  ⟩
  intro family anchor candidate
  rfl

end ConceptProbeQuotient
end RelayTheory
