import RelayTheory.GrammarComparatorViews

namespace RelayTheory

namespace UnifiedCognitiveStructuralGrammar

namespace PomdpLikeView

/-- Forget the POMDP-like comparator further to the strict dynamical comparator. -/
def toDynView (P : PomdpLikeView) : DynView where
  Time := P.Time
  Config := P.State
  succession := P.succession
  transition := by
    intro t t' h x x'
    exact ∃ a : P.Action t, P.transition h x a x'

end PomdpLikeView

namespace Grammar

/--
On the X/K/T transition backbone, direct Grammar-to-Dynamic forgetting agrees
with Grammar-to-POMDP-like-to-Dynamic forgetting.
-/
theorem toDynView_viaPomdp_transition_iff
    (G : Grammar)
    {t t' : G.Time}
    (h : G.succession t t')
    (x : G.Config t)
    (x' : G.Config t') :
    ((G.toPomdpLikeView).toDynView).transition h x x' ↔
      (G.toDynView).transition h x x' :=
  Iff.rfl

end Grammar

end UnifiedCognitiveStructuralGrammar

namespace ReconstructionLiftHierarchy

inductive Family where
  | dynamic
  | pomdp
  deriving DecidableEq, Repr

inductive Requirement where
  | direct
  | stateless
  | stateful
  deriving DecidableEq, Repr

structure Contract where
  family : Family
  requirement : Requirement
  deriving DecidableEq, Repr

/--
Object-level formal shadow of nested reconstruction categories R0 -> R1 -> R2.
U0/U1/U2 forget a reconstruction back to the source-fidelity contract.
-/
structure LiftTower (Source R0 R1 R2 : Type) where
  U0 : R0 → Source
  U1 : R1 → Source
  U2 : R2 → Source
  include01 : R0 → R1
  include12 : R1 → R2
  commute01 : ∀ r, U1 (include01 r) = U0 r
  commute12 : ∀ r, U2 (include12 r) = U1 r

namespace LiftTower

variable {Source R0 R1 R2 : Type}

def HasLift0 (T : LiftTower Source R0 R1 R2) (s : Source) : Prop :=
  ∃ r : R0, T.U0 r = s

def HasLift1 (T : LiftTower Source R0 R1 R2) (s : Source) : Prop :=
  ∃ r : R1, T.U1 r = s

def HasLift2 (T : LiftTower Source R0 R1 R2) (s : Source) : Prop :=
  ∃ r : R2, T.U2 r = s

def A0 (T : LiftTower Source R0 R1 R2) (s : Source) : Prop :=
  T.HasLift0 s

def A1 (T : LiftTower Source R0 R1 R2) (s : Source) : Prop :=
  ¬ T.HasLift0 s ∧ T.HasLift1 s

def A2 (T : LiftTower Source R0 R1 R2) (s : Source) : Prop :=
  ¬ T.HasLift1 s ∧ T.HasLift2 s

def NoLift (T : LiftTower Source R0 R1 R2) (s : Source) : Prop :=
  ¬ T.HasLift2 s

theorem lift0_implies_lift1
    (T : LiftTower Source R0 R1 R2)
    (s : Source)
    (h : T.HasLift0 s) :
    T.HasLift1 s := by
  rcases h with ⟨r, hr⟩
  refine ⟨T.include01 r, ?_⟩
  calc
    T.U1 (T.include01 r) = T.U0 r := T.commute01 r
    _ = s := hr

theorem lift1_implies_lift2
    (T : LiftTower Source R0 R1 R2)
    (s : Source)
    (h : T.HasLift1 s) :
    T.HasLift2 s := by
  rcases h with ⟨r, hr⟩
  refine ⟨T.include12 r, ?_⟩
  calc
    T.U2 (T.include12 r) = T.U1 r := T.commute12 r
    _ = s := hr

theorem a0_not_a1
    (T : LiftTower Source R0 R1 R2)
    (s : Source)
    (h0 : T.A0 s) :
    ¬ T.A1 s := by
  intro h1
  exact h1.1 h0

theorem a0_not_a2
    (T : LiftTower Source R0 R1 R2)
    (s : Source)
    (h0 : T.A0 s) :
    ¬ T.A2 s := by
  intro h2
  exact h2.1 (T.lift0_implies_lift1 s h0)

theorem a1_not_a2
    (T : LiftTower Source R0 R1 R2)
    (s : Source)
    (h1 : T.A1 s) :
    ¬ T.A2 s := by
  intro h2
  exact h2.1 h1.2

/-- Any source with an R2 lift has one of the three least-lift shells. -/
theorem least_lift_exhaustive
    (T : LiftTower Source R0 R1 R2)
    (s : Source)
    (h2 : T.HasLift2 s) :
    T.A0 s ∨ T.A1 s ∨ T.A2 s := by
  classical
  by_cases h0 : T.HasLift0 s
  · exact Or.inl h0
  · by_cases h1 : T.HasLift1 s
    · exact Or.inr (Or.inl ⟨h0, h1⟩)
    · exact Or.inr (Or.inr ⟨h1, h2⟩)

end LiftTower

structure R0Obj where
  family : Family

inductive R1Kind where
  | direct
  | stateless
  deriving DecidableEq, Repr

structure R1Obj where
  family : Family
  kind : R1Kind

structure R2Obj where
  family : Family
  requirement : Requirement

private def U0Matched (r : R0Obj) : Contract :=
  ⟨r.family, Requirement.direct⟩

private def U1Matched (r : R1Obj) : Contract :=
  match r.kind with
  | R1Kind.direct => ⟨r.family, Requirement.direct⟩
  | R1Kind.stateless => ⟨r.family, Requirement.stateless⟩

private def U2Matched (r : R2Obj) : Contract :=
  ⟨r.family, r.requirement⟩

private def include01Matched (r : R0Obj) : R1Obj :=
  ⟨r.family, R1Kind.direct⟩

private def include12Matched (r : R1Obj) : R2Obj :=
  match r.kind with
  | R1Kind.direct => ⟨r.family, Requirement.direct⟩
  | R1Kind.stateless => ⟨r.family, Requirement.stateless⟩

def matchedTower : LiftTower Contract R0Obj R1Obj R2Obj where
  U0 := U0Matched
  U1 := U1Matched
  U2 := U2Matched
  include01 := include01Matched
  include12 := include12Matched
  commute01 := by
    intro r
    rfl
  commute12 := by
    intro r
    rcases r with ⟨family, kind⟩
    cases kind <;> rfl

private def directContract (f : Family) : Contract :=
  ⟨f, Requirement.direct⟩

private def statelessContract (f : Family) : Contract :=
  ⟨f, Requirement.stateless⟩

private def statefulContract (f : Family) : Contract :=
  ⟨f, Requirement.stateful⟩

theorem direct_reaches_A0 (f : Family) :
    matchedTower.A0 (directContract f) := by
  exact ⟨⟨f⟩, rfl⟩

private theorem stateless_has_no_R0_lift (f : Family) :
    ¬ matchedTower.HasLift0 (statelessContract f) := by
  intro h
  rcases h with ⟨r, hr⟩
  have hreq := congrArg Contract.requirement hr
  cases hreq

private theorem stateless_has_R1_lift (f : Family) :
    matchedTower.HasLift1 (statelessContract f) := by
  exact ⟨⟨f, R1Kind.stateless⟩, rfl⟩

theorem stateless_reaches_A1 (f : Family) :
    matchedTower.A1 (statelessContract f) := by
  exact ⟨stateless_has_no_R0_lift f, stateless_has_R1_lift f⟩

private theorem stateful_has_no_R1_lift (f : Family) :
    ¬ matchedTower.HasLift1 (statefulContract f) := by
  intro h
  rcases h with ⟨r, hr⟩
  rcases r with ⟨family, kind⟩
  cases kind with
  | direct =>
      have hreq := congrArg Contract.requirement hr
      cases hreq
  | stateless =>
      have hreq := congrArg Contract.requirement hr
      cases hreq

private theorem stateful_has_R2_lift (f : Family) :
    matchedTower.HasLift2 (statefulContract f) := by
  exact ⟨⟨f, Requirement.stateful⟩, rfl⟩

theorem stateful_reaches_A2 (f : Family) :
    matchedTower.A2 (statefulContract f) := by
  exact ⟨stateful_has_no_R1_lift f, stateful_has_R2_lift f⟩

/-- Both matched families reach every A-state. -/
theorem six_case_reachability :
    matchedTower.A0 (directContract Family.dynamic) ∧
    matchedTower.A1 (statelessContract Family.dynamic) ∧
    matchedTower.A2 (statefulContract Family.dynamic) ∧
    matchedTower.A0 (directContract Family.pomdp) ∧
    matchedTower.A1 (statelessContract Family.pomdp) ∧
    matchedTower.A2 (statefulContract Family.pomdp) := by
  exact ⟨
    direct_reaches_A0 Family.dynamic,
    stateless_reaches_A1 Family.dynamic,
    stateful_reaches_A2 Family.dynamic,
    direct_reaches_A0 Family.pomdp,
    stateless_reaches_A1 Family.pomdp,
    stateful_reaches_A2 Family.pomdp
  ⟩

inductive PortType where
  | bit
  | taggedBit
  deriving DecidableEq, Repr

private def PortCarrier : PortType → Type
  | PortType.bit => Bool
  | PortType.taggedBit => Option Bool

structure PortContract where
  source : PortType
  target : PortType

private def DirectPortComposition (c : PortContract) : Prop :=
  c.source = c.target

private def HasStatelessPortAdapter (c : PortContract) : Prop :=
  Nonempty (PortCarrier c.source → PortCarrier c.target)

private def A1PortWitness : PortContract :=
  ⟨PortType.bit, PortType.taggedBit⟩

theorem a1_port_not_direct :
    ¬ DirectPortComposition A1PortWitness := by
  intro h
  cases h

theorem a1_port_stateless_adapter_exists :
    HasStatelessPortAdapter A1PortWitness := by
  exact ⟨fun b => some b⟩

/-- No current-input-only map can output the previous bit for all histories. -/
def StatelessHistoryRealizer (f : Bool → Bool) : Prop :=
  ∀ previous current : Bool, f current = previous

theorem no_stateless_history_realizer :
    ¬ ∃ f : Bool → Bool, StatelessHistoryRealizer f := by
  intro h
  rcases h with ⟨f, hf⟩
  have h0 : f false = false := hf false false
  have h1 : f false = true := hf true false
  have hbad : false = true := h0.symm.trans h1
  exact Bool.noConfusion hbad

/-- A one-bit persistent bridge can output stored previous input and store current input. -/
def StatefulHistoryRealizer (step : Bool → Bool → Bool × Bool) : Prop :=
  ∀ previous current : Bool,
    (step previous current).1 = previous ∧
    (step previous current).2 = current

theorem stateful_history_realizer_exists :
    ∃ step : Bool → Bool → Bool × Bool, StatefulHistoryRealizer step := by
  refine ⟨fun previous current => (previous, current), ?_⟩
  intro previous current
  exact ⟨rfl, rfl⟩

end ReconstructionLiftHierarchy

end RelayTheory
