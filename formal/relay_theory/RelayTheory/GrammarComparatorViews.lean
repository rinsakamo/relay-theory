import RelayTheory.UnifiedCognitiveStructuralGrammar

namespace RelayTheory

namespace UnifiedCognitiveStructuralGrammar

universe uTime uConfig uAction uObs uAlt

/--
A strict dynamical-system view of Grammar v0.

This view retains only:
- the temporal carrier / succession relation (T),
- the configuration carrier (X),
- a transition/dependence relation (K).

The inward interface operation is existentially forgotten. Pi, C, Q, P-out,
and rho/O do not appear in the resulting signature.

This is a comparator view for Paper 2 hostile validation, not a replacement
for `Grammar`.
-/
structure DynView where
  Time : Type uTime
  Config : Time → Type uConfig
  succession : Time → Time → Prop
  transition :
    {t t' : Time} →
    succession t t' →
    Config t →
    Config t' →
    Prop

/--
A POMDP-like action/transition/observation/criterion view.

This intentionally keeps the write/action side as `Action`, while the
query/read operation that produced an observation is existentially forgotten.
Pi-like individuation and C-like admissibility are not fields of the view.

`qLe` remains preorder-valued rather than being strengthened to scalar
reward; scalar reward is a possible specialization, not part of this formal
forgetful view.
-/
structure PomdpLikeView where
  Time : Type uTime
  State : Time → Type uConfig
  Action : Time → Type uAction
  Obs : Time → Type uObs
  Alternative : Time → Type uAlt

  succession : Time → Time → Prop

  transition :
    {t t' : Time} →
    succession t t' →
    State t →
    Action t →
    State t' →
    Prop

  observe :
    {t : Time} →
    State t →
    Obs t →
    Prop

  qLe :
    {t : Time} →
    Alternative t →
    Alternative t →
    Prop

  qRefl :
    ∀ {t : Time} (a : Alternative t),
      qLe a a

  qTrans :
    ∀ {t : Time} {a b c : Alternative t},
      qLe a b →
      qLe b c →
      qLe a c

namespace Grammar

/--
Forget Grammar v0 to the strict {X,K,T} comparator.

The K-like transition survives only after existentially forgetting which
P-in operation licensed the transition.
-/
def toDynView (G : Grammar) : DynView where
  Time := G.Time
  Config := G.Config
  succession := G.succession
  transition := by
    intro t t' h x x'
    exact ∃ p : G.Pin t, G.transition h x p x'

/--
The transition relation in the dynamical comparator is exactly the
existential image of Grammar-v0 transition after forgetting P-in identity.
-/
theorem toDynView_transition_iff
    (G : Grammar)
    {t t' : G.Time}
    (h : G.succession t t')
    (x : G.Config t)
    (x' : G.Config t') :
    (G.toDynView).transition h x x' ↔
      ∃ p : G.Pin t, G.transition h x p x' :=
  Iff.rfl

/--
Forget Grammar v0 to a POMDP-like action/transition/observation/criterion view.

The action side is retained as P-in. The identity of the P-out query that
generated an observation is existentially forgotten. Pi and C are absent from
the target signature.
-/
def toPomdpLikeView (G : Grammar) : PomdpLikeView where
  Time := G.Time
  State := G.Config
  Action := G.Pin
  Obs := G.Obs
  Alternative := G.Alternative
  succession := G.succession
  transition := G.transition
  observe := by
    intro t x o
    exact ∃ p : G.Pout t, G.observe x p o
  qLe := G.qLe
  qRefl := G.qRefl
  qTrans := G.qTrans

/--
The POMDP-like observation relation is exactly the existential image of
Grammar-v0 observation after forgetting P-out query identity.
-/
theorem toPomdpLikeView_observe_iff
    (G : Grammar)
    {t : G.Time}
    (x : G.Config t)
    (o : G.Obs t) :
    (G.toPomdpLikeView).observe x o ↔
      ∃ p : G.Pout t, G.observe x p o :=
  Iff.rfl

end Grammar

end UnifiedCognitiveStructuralGrammar

end RelayTheory
