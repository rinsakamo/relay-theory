namespace RelayTheory
namespace ProbeFutureClosure

/--
Two values are indistinguishable relative to every probe admitted by `P`.
The definition is intentionally neutral: it carries no observer, information,
time, or ontology interpretation.
-/
def ProbeEq
    {α β : Type}
    (P : (α → β) → Prop)
    (x y : α) : Prop :=
  ∀ probe, P probe → probe x = probe y

/-- A probe family containing exactly one declared probe. -/
def SingletonFamily
    {α β : Type}
    (probe : α → β) : (α → β) → Prop :=
  fun candidate => candidate = probe

/--
Compatibility sufficient to transport a probe-relative equivalence through
a future map: every downstream probe, pulled back through the future map,
was already admitted by the current family.
-/
def PullbackClosedAlong
    {α β : Type}
    (current downstream : (α → β) → Prop)
    (future : α → α) : Prop :=
  ∀ probe, downstream probe →
    current (fun x => probe (future x))

/--
Explicit pullback closure is sufficient to preserve the declared equivalence
through the future map.
-/
theorem probeEq_future_of_pullbackClosed
    {α β : Type}
    {current downstream : (α → β) → Prop}
    {future : α → α}
    {x y : α}
    (hEq : ProbeEq current x y)
    (hClosed : PullbackClosedAlong current downstream future) :
    ProbeEq downstream (future x) (future y) := by
  intro probe hProbe
  exact hEq (fun z => probe (future z)) (hClosed probe hProbe)

/-- Identity evolution preserves every probe-relative equivalence. -/
theorem probeEq_identity
    {α β : Type}
    {P : (α → β) → Prop}
    {x y : α}
    (hEq : ProbeEq P x y) :
    ProbeEq P (id x) (id y) := by
  simpa using hEq

/-- More admitted probes induce a finer equivalence. -/
theorem probeEq_of_family_inclusion
    {α β : Type}
    {coarse fine : (α → β) → Prop}
    {x y : α}
    (hInclude : ∀ probe, coarse probe → fine probe)
    (hFine : ProbeEq fine x y) :
    ProbeEq coarse x y := by
  intro probe hProbe
  exact hFine probe (hInclude probe hProbe)

abbrev History := Bool × Bool

/-- The current probe sees only the first coordinate. -/
def firstProbe (h : History) : Bool := h.1

/-- Ordinary deterministic future transformation exchanging the coordinates. -/
def swapFuture (h : History) : History := (h.2, h.1)

def leftHistory : History := (false, false)
def rightHistory : History := (false, true)

/-- The two histories are indistinguishable under the declared current probe. -/
theorem current_singleton_probe_equivalent :
    ProbeEq (SingletonFamily firstProbe) leftHistory rightHistory := by
  intro probe hProbe
  subst probe
  rfl

/--
After an ordinary future map, the same declared probe separates the histories.
Thus arbitrary current probe-equivalence is not intrinsically future-stable.
-/
theorem future_map_breaks_current_probe_equivalence :
    ¬ ProbeEq
      (SingletonFamily firstProbe)
      (swapFuture leftHistory)
      (swapFuture rightHistory) := by
  intro hEq
  have h := hEq firstProbe rfl
  simp [firstProbe, swapFuture, leftHistory, rightHistory] at h

/--
The counterexample fails its own pullback-closure condition: the pulled-back
first-coordinate probe is the second-coordinate probe, which is not the
declared singleton current family.
-/
theorem counterexample_not_pullbackClosed :
    ¬ PullbackClosedAlong
      (SingletonFamily firstProbe)
      (SingletonFamily firstProbe)
      swapFuture := by
  intro hClosed
  have hMember := hClosed firstProbe rfl
  have hEqFun : (fun x => firstProbe (swapFuture x)) = firstProbe := hMember
  have hAtRight := congrArg (fun f => f rightHistory) hEqFun
  simp [firstProbe, swapFuture, rightHistory] at hAtRight

/--
Scoped bundle: current equivalence holds, arbitrary future stability fails,
while explicit pullback closure remains sufficient for transport.
-/
theorem probe_future_closure_bundle :
    ProbeEq (SingletonFamily firstProbe) leftHistory rightHistory ∧
    ¬ ProbeEq
      (SingletonFamily firstProbe)
      (swapFuture leftHistory)
      (swapFuture rightHistory) ∧
    ¬ PullbackClosedAlong
      (SingletonFamily firstProbe)
      (SingletonFamily firstProbe)
      swapFuture := by
  exact ⟨
    current_singleton_probe_equivalent,
    future_map_breaks_current_probe_equivalence,
    counterexample_not_pullbackClosed
  ⟩

end ProbeFutureClosure
end RelayTheory
