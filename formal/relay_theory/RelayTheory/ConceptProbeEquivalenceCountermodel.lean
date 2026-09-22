namespace RelayTheory

namespace ConceptProbeEquivalenceCountermodel

abbrev Item := Bool
abbrev Probe := Bool
abbrev Response := Bool
abbrev Profile := Item → Probe → Response

def probeRelative : Profile :=
  fun item probe => if probe then item else false

def EquivalentUnder
    (profile : Profile)
    (probe : Probe)
    (a b : Item) : Prop :=
  profile a probe = profile b probe

theorem falseProbe_equivalent :
    EquivalentUnder probeRelative false false true := by
  rfl

theorem trueProbe_distinguishes :
    ¬ EquivalentUnder probeRelative true false true := by
  simp [EquivalentUnder, probeRelative]

theorem sameProfile_changesEquivalenceWithProbe :
    EquivalentUnder probeRelative false false true ∧
    ¬ EquivalentUnder probeRelative true false true := by
  exact ⟨falseProbe_equivalent, trueProbe_distinguishes⟩

theorem equivalentUnder_refl
    (profile : Profile)
    (probe : Probe)
    (a : Item) :
    EquivalentUnder profile probe a a := by
  rfl

theorem equivalentUnder_symm
    (profile : Profile)
    (probe : Probe)
    (a b : Item)
    (h : EquivalentUnder profile probe a b) :
    EquivalentUnder profile probe b a := by
  exact h.symm

theorem equivalentUnder_trans
    (profile : Profile)
    (probe : Probe)
    (a b c : Item)
    (hab : EquivalentUnder profile probe a b)
    (hbc : EquivalentUnder profile probe b c) :
    EquivalentUnder profile probe a c := by
  exact hab.trans hbc

theorem extensionalProfilesPreserveEquivalence
    (f g : Profile)
    (hEq : ∀ item : Item, ∀ probe : Probe, f item probe = g item probe)
    (probe : Probe)
    (a b : Item) :
    EquivalentUnder f probe a b ↔
    EquivalentUnder g probe a b := by
  unfold EquivalentUnder
  rw [hEq a probe, hEq b probe]

structure DecoratedProfile where
  profile : Profile
  conceptFlag : Bool

def decoratedConcept : DecoratedProfile where
  profile := probeRelative
  conceptFlag := true

def decoratedNonConcept : DecoratedProfile where
  profile := probeRelative
  conceptFlag := false

theorem conceptLabelDeletionControl
    (probe : Probe)
    (a b : Item) :
    EquivalentUnder decoratedConcept.profile probe a b ↔
    EquivalentUnder decoratedNonConcept.profile probe a b := by
  rfl

end ConceptProbeEquivalenceCountermodel

end RelayTheory
