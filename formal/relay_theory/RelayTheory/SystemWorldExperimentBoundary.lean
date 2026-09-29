import RelayTheory.UnifiedCognitiveStructuralGrammar

namespace RelayTheory

namespace UnifiedCognitiveStructuralGrammar

universe uWorld

/--
A World-side carrier coupled to an already-defined Grammar-v0 system.

This structure is deliberately outside `Grammar`.
It does not add World as a Grammar-v0 role and does not identify experimental
operations with system-internal dynamics.

`inCouples` relates a World-side state/event to a P-in operation directed
into the modeled system boundary.

`outCouples` relates a P-out configured system-relative observation/trace
to a World-side state/consequence.

No dynamics for World are assumed here.
-/
structure WorldCoupling (G : Grammar) where
  World : G.Time → Type uWorld

  inCouples :
    {t : G.Time} →
    World t →
    G.Pin t →
    Prop

  outCouples :
    {t : G.Time} →
    G.Pout t →
    G.Obs t →
    World t →
    Prop

/--
A finite-observation cut through a Grammar-v0 system history.

The cut selects an experiment-relative start position and an admissible
configuration at that position. It does not assert that `start` is the
absolute beginning of the system.
-/
structure RunCut (G : Grammar) where
  start : G.Time
  state : G.Config start
  admissible : G.stateAdmissible state

/--
A run cut has a witnessed system prehistory when an earlier configuration can
transition into the cut state through some P-in operation.

This is optional evidence. No theorem states that every run cut has prehistory.
-/
def RunCut.HasSystemPrehistory
    (G : Grammar)
    (c : RunCut G) : Prop :=
  ∃ (tPrev : G.Time)
    (h : G.succession tPrev c.start)
    (xPrev : G.Config tPrev)
    (p : G.Pin tPrev),
    G.transition h xPrev p c.state

/--
An experiment protocol is external to Grammar v0.

It selects which already-available system interface operations are scheduled
at which World/system positions. The protocol does not create new P-in/P-out
roles and does not become part of K.

`inSchedule` and `outSchedule` may be partial or relational.
-/
structure ExperimentProtocol
    (G : Grammar)
    (WC : WorldCoupling G) where
  inSchedule :
    {t : G.Time} →
    WC.World t →
    G.Pin t →
    Prop

  outSchedule :
    {t : G.Time} →
    WC.World t →
    G.Pout t →
    Prop

  inSchedule_respects_coupling :
    ∀ {t : G.Time}
      (w : WC.World t)
      (p : G.Pin t),
      inSchedule w p →
      WC.inCouples w p

/--
An experiment-start configuration pairs a system run cut with the World state
at the same experiment-relative position.

No equality, generation rule, or causal direction between the two is assumed
without an explicit coupling or preparation relation.
-/
structure ExperimentStart
    (G : Grammar)
    (WC : WorldCoupling G) where
  cut : RunCut G
  world : WC.World cut.start

end UnifiedCognitiveStructuralGrammar

end RelayTheory
