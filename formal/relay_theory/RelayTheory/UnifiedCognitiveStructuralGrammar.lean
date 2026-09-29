namespace RelayTheory

namespace UnifiedCognitiveStructuralGrammar

universe uTime uPart uConfig uPin uPout uObs uAlt

/--
A type-checked Discussion-level carrier for Paper 2's Unified Cognitive
Structural Grammar v0.

This is deliberately weaker than any particular cognitive theory:
- `succession` supplies T-like ordering without forcing a transition law;
- `partOf` supplies Pi-like individuation;
- C-like admissibility is represented by predicates;
- K-like transition and rho-like observation are relations, so deterministic
  functions and stochastic/relational refinements can be added later;
- Q-like orientation is only required to be a preorder;
- P is split into inward actions (`Pin`) and outward queries (`Pout`).

The structure is validation infrastructure for #321. It is not a claim that
every frozen Paper 2 claim instantiates every field.
-/
structure Grammar where
  /-- T carrier: temporal / succession positions. -/
  Time : Type uTime

  /-- S/X carrier at each temporal position. -/
  Config : Time → Type uConfig

  /-- Pi index at each temporal position. -/
  Part : Time → Type uPart

  /-- Pi-like assignment of a configuration to an individuation cell. -/
  partOf : {t : Time} → Config t → Part t

  /-- P-in: intervention / write-side interface operations. -/
  Pin : Time → Type uPin

  /-- P-out: probe / read-side interface operations. -/
  Pout : Time → Type uPout

  /-- O carrier: boundary-relative observations / traces. -/
  Obs : Time → Type uObs

  /-- Q carrier: alternatives to which a criterion-relative orientation applies. -/
  Alternative : Time → Type uAlt

  /--
  T-like succession relation. This is intentionally separate from K:
  successive positions need not have a retained transformation law.
  -/
  succession : Time → Time → Prop

  /-- C-like admissibility of a configuration at a temporal position. -/
  stateAdmissible : {t : Time} → Config t → Prop

  /--
  C-like admissibility of a possible transition. It is separate from the
  retained K-like transition relation so that realizability constraints can be
  stronger than mere logical definability.
  -/
  transitionAdmissible :
    {t t' : Time} →
    succession t t' →
    Config t →
    Pin t →
    Config t' →
    Prop

  /--
  K-like typed transition/dependence relation. A function-valued update is a
  specialization, not assumed by the grammar.
  -/
  transition :
    {t t' : Time} →
    succession t t' →
    Config t →
    Pin t →
    Config t' →
    Prop

  /-- Every retained transition lies inside the C-admissible transition region. -/
  transition_respects_C :
    ∀ {t t' : Time}
      (h : succession t t')
      (x : Config t)
      (p : Pin t)
      (x' : Config t'),
      transition h x p x' →
      transitionAdmissible h x p x'

  /-- C-like admissibility of a boundary exposure / observation. -/
  observationAdmissible :
    {t : Time} →
    Config t →
    Pout t →
    Obs t →
    Prop

  /--
  rho-like boundary trace / projection relation configured by P-out.
  It is relational to permit partial or non-functional readout.
  -/
  observe :
    {t : Time} →
    Config t →
    Pout t →
    Obs t →
    Prop

  /-- Every retained observation lies inside the C-admissible exposure region. -/
  observe_respects_C :
    ∀ {t : Time}
      (x : Config t)
      (p : Pout t)
      (o : Obs t),
      observe x p o →
      observationAdmissible x p o

  /-- Q-like criterion-relative comparison on alternatives. -/
  qLe :
    {t : Time} →
    Alternative t →
    Alternative t →
    Prop

  /-- Q is at least preorder-like; scalar objectives are optional refinements. -/
  qRefl :
    ∀ {t : Time} (a : Alternative t),
      qLe a a

  /-- Q orientation composes transitively. -/
  qTrans :
    ∀ {t : Time} {a b c : Alternative t},
      qLe a b →
      qLe b c →
      qLe a c

namespace Grammar

/-- The Pi fiber containing configurations assigned to index `i`. -/
def Fiber (G : Grammar)
    (t : G.Time)
    (i : G.Part t) : Type uConfig :=
  {x : G.Config t // G.partOf x = i}

/-- Every configuration canonically inhabits its own Pi fiber. -/
def toFiber (G : Grammar)
    {t : G.Time}
    (x : G.Config t) :
    G.Fiber t (G.partOf x) :=
  ⟨x, rfl⟩

/-- Kernel-visible witness that K is constrained by C in the grammar. -/
theorem transition_is_admissible
    (G : Grammar)
    {t t' : G.Time}
    (h : G.succession t t')
    (x : G.Config t)
    (p : G.Pin t)
    (x' : G.Config t')
    (hk : G.transition h x p x') :
    G.transitionAdmissible h x p x' :=
  G.transition_respects_C h x p x' hk

/-- Kernel-visible witness that rho/O exposure is constrained by C. -/
theorem observation_is_admissible
    (G : Grammar)
    {t : G.Time}
    (x : G.Config t)
    (p : G.Pout t)
    (o : G.Obs t)
    (ho : G.observe x p o) :
    G.observationAdmissible x p o :=
  G.observe_respects_C x p o ho

/-- Kernel-visible witness that Q's comparison is reflexive. -/
theorem q_reflexive
    (G : Grammar)
    {t : G.Time}
    (a : G.Alternative t) :
    G.qLe a a :=
  G.qRefl a

/--
A deterministic K-like update is a refinement of the relational grammar, not
part of the base definition.
-/
structure DeterministicTransition (G : Grammar) where
  step :
    {t t' : G.Time} →
    (h : G.succession t t') →
    G.Config t →
    G.Pin t →
    G.Config t'

  realizes :
    ∀ {t t' : G.Time}
      (h : G.succession t t')
      (x : G.Config t)
      (p : G.Pin t),
      G.transition h x p (step h x p)

/--
A deterministic rho-like readout is likewise a refinement of the relational
observation layer.
-/
structure DeterministicObservation (G : Grammar) where
  read :
    {t : G.Time} →
    G.Config t →
    G.Pout t →
    G.Obs t

  realizes :
    ∀ {t : G.Time}
      (x : G.Config t)
      (p : G.Pout t),
      G.observe x p (read x p)

/--
Successive time fibers need not be definitionally the same type. Therefore
"persistence = K = identity" is not well-typed in the general grammar without
an explicit identification / transport between the fibers.

A carry map makes that extra structure explicit.
-/
structure CarryMap
    (G : Grammar)
    {t t' : G.Time}
    (h : G.succession t t') where
  carry : G.Config t → G.Config t'

/--
For a fixed inward interface operation, a K-like transition realizes a chosen
carry map when every source configuration is related to its carried image.

Identity persistence is a special case only when the relevant fibers have
already been identified.
-/
def TransitionRealizesCarry
    (G : Grammar)
    {t t' : G.Time}
    (h : G.succession t t')
    (p : G.Pin t)
    (c : CarryMap G h) : Prop :=
  ∀ x : G.Config t, G.transition h x p (c.carry x)

end Grammar

end UnifiedCognitiveStructuralGrammar

end RelayTheory
