# M9-A — Categorical least-lift foundation for A0/A1/A2

Status: PROPOSED_FROZEN_M9A_FOUNDATION
Base authority: M8 exact HEAD `3e0c82fb090bc0fc2f66ed3c4e65df282779f4eb`

## 1. Question

The hostile review identified a precise threat to MAIN40: if the A0/A1/A2 adjudication procedure is structurally attracted to A0, then `40/40 A0` is not informative even if every paper-level adjudication is internally consistent. M9-A therefore asks a narrower question than MAIN40 itself:

> Are A0, A1, and A2 mutually discriminable least-reconstruction outcomes, and are A1 and A2 demonstrably reachable under matched source contracts?

M9-A does **not** re-adjudicate MAIN40 and does not alter any M1--M8 scientific artifact.

## 2. Reconstruction tower

Let \(\mathcal S\) be a category of source-fidelity contracts. Let

\[
\mathcal R_0 \xhookrightarrow{J_{01}} \mathcal R_1
\xhookrightarrow{J_{12}} \mathcal R_2
\]

be nested reconstruction categories:

- \(\mathcal R_0\): Grammar v0 roles plus mechanisms already defined by the source; no reconstruction-added mechanism.
- \(\mathcal R_1\): \(\mathcal R_0\) plus reconstruction-added **stateless typed interface / sequencing / translation** structure.
- \(\mathcal R_2\): \(\mathcal R_1\) plus reconstruction-added **persistent/stateful coordination** structure.

Let fidelity-forgetting functors

\[
U_i:\mathcal R_i\to\mathcal S
\]

return the source contract realized by a reconstruction. The inclusions must commute with fidelity forgetting up to the declared source-equivalence relation:

\[
U_1J_{01}\cong U_0,
\qquad
U_2J_{12}\cong U_1.
\]

Therefore their essential images are nested:

\[
\operatorname{EssIm}(U_0)
\subseteq
\operatorname{EssIm}(U_1)
\subseteq
\operatorname{EssIm}(U_2).
\]

For an eligible, sufficiently specified source contract \(s\):

\[
A0(s) \iff s\in\operatorname{EssIm}(U_0),
\]

\[
A1(s) \iff s\in\operatorname{EssIm}(U_1)
\setminus\operatorname{EssIm}(U_0),
\]

\[
A2(s) \iff s\in\operatorname{EssIm}(U_2)
\setminus\operatorname{EssIm}(U_1).
\]

If \(s\notin\operatorname{EssIm}(U_2)\), the reconstruction attempt has no faithful A0/A1/A2 lift under the frozen contract. This mathematical non-lift must not be conflated with `UNDERDETERMINED` or `SOURCE_INELIGIBLE`, which are epistemic/admission states decided before a scientific A-state can be certified.

### Proposition 1 — least-lift well-definedness

Under the commuting nested-reconstruction assumptions above, A0, A1 and A2 are pairwise disjoint. Every eligible source contract in \(\operatorname{EssIm}(U_2)\) has exactly one least reconstruction level among A0/A1/A2.

**Proof.** Nested essential images give \(E_0\subseteq E_1\subseteq E_2\). The three outcome classes are the disjoint shells \(E_0\), \(E_1\setminus E_0\), and \(E_2\setminus E_1\). Their union is \(E_2\). QED.

This theorem is the formal reason that A0/A1/A2 are an ordered reconstruction requirement, rather than three informal labels.

## 3. Why source-defined state does not imply A2

The tower is indexed by **reconstruction-added** structure, not by the intrinsic complexity of a source model. An object of \(\mathcal R_0\) may contain arbitrary source-defined memory, belief state, recurrent state, gating, hierarchy, planners, accumulators, or other persistent mechanisms. Such mechanisms are inside the source-native object before the inclusion tower is traversed. A2 is entered only when no faithful object exists in \(\mathcal R_1\) and a new persistent mechanism must be introduced by the reconstruction.

Thus:

> source-defined persistent state is compatible with A0; reconstruction-added persistent state is the defining positive witness for A2.

This preserves the M7 rule rather than weakening it.

## 4. Positive witness for A1

Consider two source-defined component ports. The upstream component emits a value of type `bit`; the downstream component accepts a value of type `tagged-bit`. Under the direct-composition contract, a connection is permitted only when the declared port types coincide. They do not, so no A0 direct connection exists.

A stateless typed map

\[
\alpha:\mathrm{bit}\to\mathrm{tagged\mbox{-}bit},
\qquad
\alpha(b)=\mathrm{Some}(b)
\]

restores fidelity without retaining history. This is an A1 witness: A0 fails, A1 succeeds, and no persistent state is needed.

The Lean module proves both the direct-type mismatch and existence of the stateless adapter.

## 5. Positive witness for A2

Let a bridge receive only the current binary input \(x_t\), while the source contract requires its output to equal the immediately preceding input \(x_{t-1}\). A stateless bridge is a function

\[
f:\{0,1\}\to\{0,1\}.
\]

Take two histories with the same current input \(x_t=0\) but different previous inputs. Fidelity would require simultaneously

\[
f(0)=0
\quad\text{and}\quad
f(0)=1,
\]

which is impossible. Therefore no stateless realization exists.

A one-bit persistent bridge state suffices:

\[
z_{t+1}=x_t,
\qquad
y_t=z_t.
\]

The Lean module proves nonexistence of a stateless history realizer and constructs a stateful realizer. This is a positive A2 witness independent of MAIN40.

## 6. Matched Dynamic / POMDP-like benchmark

The same three reconstruction obligations are instantiated in two matched families. Family identity changes; the A-level-generating obstruction does not.

| Case | Family | Frozen obstruction | Least faithful level |
|---|---|---|---|
| DYN-0 | Dynamic | none; source-native typed composition closes | A0 |
| DYN-1 | Dynamic | typed port mismatch; stateless bridge suffices | A1 |
| DYN-2 | Dynamic | history-sensitive bridge; no current-input stateless map can satisfy fidelity | A2 |
| POM-0 | POMDP-like | source-defined latent/belief state and interfaces already close composition | A0 |
| POM-1 | POMDP-like | observation/action coding mismatch; stateless translation suffices | A1 |
| POM-2 | POMDP-like | two histories collapse to the same current exposed view but require different bridge output | A2 |

The benchmark is **matched** in the sense that A0/A1/A2 are generated by the same reconstruction obligations in each family. Model complexity is not used as a class cue.

The expected result is therefore exactly two A0, two A1, and two A2 cases. A classifier that returns A0 for all six fails M9-A even if it reproduces MAIN40.

## 7. Relationship to the existing Dynamic and POMDP-like comparators

Paper 2 already freezes two strict direct-preservation comparators:

\[
G_{\mathrm{dyn}}=\{X,K,T\},
\qquad
G_{\mathrm{pomdp}}=\{X,P,K,\rho/O,Q,T\}.
\]

The existing comparator result is not a non-encodability theorem. It asks whether frozen source distinctions remain **first-class and directly distinguishable** without retyping them into generic state or transition variables.

The frozen evidence is:

- `G_dyn`: 59/60 claims require at least one Grammar-v0 role beyond `{X,K,T}`; strict full direct preservation = 0.
- POMDP-like view: explicit `Pi` and `C` are absent; `P_in/P_out` directionality is collapsed; 44/60 claims are hit by these three direct-preservation tests.
- the POMDP-like formal view retains a generalized preorder-valued `Q`; the result therefore does not depend on reducing Q to scalar reward.

M9-A adds a formal factorization of the transition backbone:

\[
G_{v0}\to G_{\mathrm{pomdp\mbox{-}like}}\to G_{\mathrm{dyn}},
\]

where the second map existentially forgets action identity. On the K/T/X transition backbone, this agrees with the already frozen direct Grammar-to-Dynamic view.

This clarifies why Paper 2 moved beyond a POMDP-like comparison basis:

> the objection is not that POMDPs cannot encode cognitive models; it is that the POMDP-like projection is too forgetful for the source distinctions that Paper 2 chose to preserve directly.

Encoding power and distinction preservation are different criteria.

## 8. What M9-A would establish if all checks pass

M9-A supports the following bounded claims:

1. A0/A1/A2 have a mathematically explicit least-lift semantics under a nested reconstruction tower.
2. A1 and A2 are reachable positive outcomes; A0 is not forced by the outcome vocabulary.
3. A stateful A2 obligation can be proven by an obstruction to every stateless current-input realizer.
4. The Dynamic and POMDP-like matched families each contain A0/A1/A2 witnesses.
5. The existing comparator story and the new A-state story are complementary: comparator forgetting tests distinction loss; least-lift classification tests reconstruction-added coordination.
6. A POMDP-like basis was not rejected for lack of expressive encoding power, but because it failed the stricter direct-preservation contract for distinctions already frozen from the source corpus.

M9-A does **not** establish that MAIN40 papers are independent, that Grammar v0 is universal/minimal in an absolute sense, or that 40/40 A0 has a population frequency interpretation.

## 9. Formalization boundary

The repository does not currently depend on a category-theory library. The Lean module therefore kernel-checks the **object-level consequences** of the categorical construction: a commuting nested lift tower, monotonic lift existence, pairwise-disjoint least-lift outcomes, six matched A-state witnesses, the A1 typed-adapter witness, the A2 stateless-obstruction/stateful-realizer witness, and the POMDP-like-to-Dynamic transition factorization.

The category-theoretic statement above is the mathematical presentation; the Lean object-level theorem is a conservative formal shadow of its essential-image logic, not a claim that the repository has formalized general category theory.

## 10. Validation boundary

This matched synthetic reachability result does **not** replace independent human re-adjudication of a stratified MAIN40 subset. It addresses a different hostile-review question: whether the frozen A-state outcome vocabulary and reconstruction hierarchy can, in principle and in executable matched witnesses, return A1 and A2 rather than collapsing every admissible case to A0.

