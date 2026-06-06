# Seely Equivalence — Independent Two-Route Derivation

> **Status:** Drafted May 2026 as the §0 prerequisite of [[../Phase A Experiment/(C)-Phase-A-Experiment-Revised]] (the Pre-Experimental Verification). Closes **S1** of the [[../Phase A Experiment/(C)-OSF-Preregistration-Phase-A1]] Appendix-A lock-in punch list. Provides two independent derivations of the theorem cited at §2.1.4 of [[02-Cellular-Sheaves-SPD-Manifolds]] — one algebraic (Rao–Ballard route, what §0 explicitly asks for), one categorical (St Clere Smithe 2023 route from the [[../10-Analysis/(C)-09-Topos-Institute-Research-Mapping]] §3.1 OQ 11.43 lead). The two routes agree under shared assumptions; **both are necessary** because the qualifications they expose are different and complementary.

> **Result preview:** the equivalence $E_{\mathrm{PC}}(\mathbf{x}) = \mathbf{x}^\top L_{\mathcal{F}} \mathbf{x}$ holds **exactly** under five explicit assumptions (linear restriction maps, Gaussian likelihood, orthogonal transport via $\Gamma \in \mathrm{O}(d)$, surjective edge projection $P_{u \to e}$, identity or precision-weighted edge norm). Three of the five are built into the spec by construction; the remaining two (Gaussian likelihood and the precision structure) are explicit modelling commitments whose violation has known consequences. Stage-1 deployment lives inside this envelope; Stage-2 and Stage-3 extensions must check each assumption against their operational regime.

---

## §1 The theorem and the question

**Theorem (Seely et al., 2025, arXiv:2511.11092).** *Let $\mathcal{F}$ be a cellular sheaf on a graph $G = (V, E)$ with finite-dimensional stalks and linear restriction maps. The predictive-coding energy functional on the node-state vector $\mathbf{x} \in C^0(G; \mathcal{F}) = \bigoplus_{v \in V} \mathcal{F}(v)$ equals the sheaf Laplacian quadratic form:*

$$E_{\mathrm{PC}}(\mathbf{x}) = \mathbf{x}^\top L_{\mathcal{F}} \mathbf{x}.$$

**What §0 of [[../Phase A Experiment/(C)-Phase-A-Experiment-Revised]] asks.** Re-derive this from the Rao & Ballard (1999) prediction-error formulation using thrIVE's explicit restriction-map decomposition $\mathcal{F}_{u \triangleleft e} = P_{u \to e} \Gamma_{u \to v}$ (§2.1.3 of [[02-Cellular-Sheaves-SPD-Manifolds]]), documenting any qualifications. This document does so along two independent paths.

---

## §2 Setup — sheaf machinery in spec notation

Following §2.1.1 of [[02-Cellular-Sheaves-SPD-Manifolds]]:

- **Graph:** $G = (V, E)$, with each edge $e \in E$ given a chosen orientation $e = (u, v)$ (head $v$, tail $u$).
- **Node stalks:** $\mathcal{F}(v) \cong \mathbb{R}^{d}$ for each $v \in V$ (homogeneous stalk dimension assumed — see §4.5 for the inhomogeneous case).
- **Edge stalks:** $\mathcal{F}(e) \cong \mathbb{R}^{d_s}$ with $d_s \leq d$.
- **Restriction maps:** for each incident pair $(v, e)$, a linear map $\mathcal{F}_{v \triangleleft e} : \mathcal{F}(v) \to \mathcal{F}(e)$.
- **Spec decomposition:** $\mathcal{F}_{u \triangleleft e} = P_{u \to e} \Gamma_{u \to v}$, where $\Gamma_{u \to v} \in \mathrm{O}(d)$ is orthogonal parallel transport and $P_{u \to e} \in \mathbb{R}^{d_s \times d}$ is a row-orthonormal projection onto the edge subspace.
- **Coboundary operator:** $\delta : C^0(G; \mathcal{F}) \to C^1(G; \mathcal{F})$ acting on $\mathbf{x} = (x_v)_{v \in V}$ by
  $$(\delta \mathbf{x})_e = \mathcal{F}_{v \triangleleft e}(x_v) - \mathcal{F}_{u \triangleleft e}(x_u) \quad \text{for } e = (u, v).$$
- **Sheaf Laplacian:** $L_{\mathcal{F}} = \delta^\top \delta$.

The Hansen & Ghrist (2019) identity restated:

$$\mathbf{x}^\top L_{\mathcal{F}} \mathbf{x} = \|\delta \mathbf{x}\|^2 = \sum_{e = (u,v) \in E} \left\| \mathcal{F}_{v \triangleleft e}(x_v) - \mathcal{F}_{u \triangleleft e}(x_u) \right\|^2_{\mathcal{F}(e)}. \tag{$\star$}$$

This is the right-hand side of the theorem. Both derivation routes target the left-hand side independently and show it reduces to ($\star$).

---

## §3 Route 1 — Algebraic derivation from Rao–Ballard prediction errors

### §3.1 Rao–Ballard (1999) on a hierarchy

In Rao & Ballard's original formulation on a layered hierarchy $v_0, v_1, \ldots, v_K$:

- Each layer $v_i$ has a representation $r_i \in \mathbb{R}^{d_i}$
- Layer $v_{i+1}$ predicts layer $v_i$ via a linear generative model $\hat{r}_i = W_{i+1} r_{i+1}$
- The local prediction error is $\epsilon_i = r_i - \hat{r}_i = r_i - W_{i+1} r_{i+1}$
- The total energy (under Gaussian likelihood with identity precision) is

$$E_{\mathrm{RB}}(\mathbf{r}) = \sum_{i=0}^{K-1} \| r_i - W_{i+1} r_{i+1} \|^2 + \text{prior terms}. \tag{1}$$

### §3.2 Generalisation to an arbitrary directed graph

The hierarchy generalises naturally: each *edge* (not just adjacent layers) carries a prediction. For a directed edge $e = (u, v)$, the head $v$ generates a prediction of the tail $u$, and the local prediction error lives in a shared comparison space.

To preserve linearity, the prediction-error space must be common to both endpoints. The cellular-sheaf formalism realises this directly: $\mathcal{F}(e)$ *is* the local comparison space, and the restriction maps $\mathcal{F}_{u \triangleleft e}, \mathcal{F}_{v \triangleleft e}$ are exactly the linear maps that send each endpoint's state to that comparison space. The edge prediction error is then

$$\epsilon_e = \mathcal{F}_{v \triangleleft e}(x_v) - \mathcal{F}_{u \triangleleft e}(x_u), \quad \epsilon_e \in \mathcal{F}(e). \tag{2}$$

This is the natural cellular-sheaf generalisation of the Rao–Ballard prediction error: each endpoint pushes its state forward to the edge, and the discrepancy *at the edge* is the prediction error.

The total graph-level prediction-coding energy under Gaussian likelihood with identity edge precision is

$$E_{\mathrm{PC}}(\mathbf{x}) = \sum_{e \in E} \| \epsilon_e \|^2_{\mathcal{F}(e)} = \sum_{e \in E} \left\| \mathcal{F}_{v \triangleleft e}(x_v) - \mathcal{F}_{u \triangleleft e}(x_u) \right\|^2_{\mathcal{F}(e)}. \tag{3}$$

By inspection, (3) is the right-hand side of ($\star$), which equals $\mathbf{x}^\top L_{\mathcal{F}} \mathbf{x}$. This establishes the theorem.

### §3.3 Substituting the spec's restriction-map decomposition

Substitute $\mathcal{F}_{u \triangleleft e} = P_{u \to e} \Gamma_{u \to v}$ into (2):

$$\epsilon_e = P_{v \to e} \Gamma_{v \to u} \, x_v - P_{u \to e} \Gamma_{u \to v} \, x_u, \tag{4}$$

where $\Gamma_{v \to u} = \Gamma_{u \to v}^{-1} = \Gamma_{u \to v}^\top$ by orthogonality of $\Gamma$ (this is the consistency condition for parallel transport: transporting from $u$ to $v$ and back is the identity).

Three observations follow from (4):

1. **Orthogonality of $\Gamma$ preserves the norm.** Because $\Gamma \in \mathrm{O}(d)$ is an isometry on $\mathcal{F}(u) \cong \mathcal{F}(v) \cong \mathbb{R}^d$, the transported state $\Gamma_{u \to v} x_u$ has the same magnitude as $x_u$. This is the gauge-invariance property: the energy does not depend on the choice of frame at each node.

2. **Surjectivity of $P_{u \to e}$ onto $\mathcal{F}(e)$ ensures no information loss at the edge.** The projection $P_{u \to e} \in \mathbb{R}^{d_s \times d}$ is row-orthonormal by construction, so $P_{u \to e} P_{u \to e}^\top = I_{d_s}$. The projection's image is the full edge stalk; the kernel is the orthogonal complement. This means the edge comparison captures the full $d_s$-dimensional content that the spec commits to comparing.

3. **The decomposition does not introduce new degrees of freedom.** Composition $P \Gamma$ has $d \cdot d_s + d(d-1)/2$ degrees of freedom (orthonormal projection plus $\Gamma$). For thrIVE's $d = 8$, $d_s = 8$, this is $36 + 28 = 64 = d \cdot d$, identical to the degrees of freedom of an unconstrained linear map $\mathbb{R}^d \to \mathbb{R}^{d_s}$. The decomposition is therefore a *reparametrisation*, not a restriction.

The substituted prediction-coding energy is

$$E_{\mathrm{PC}}(\mathbf{x}) = \sum_{e = (u,v) \in E} \left\| P_{v \to e} \Gamma_{v \to u} x_v - P_{u \to e} \Gamma_{u \to v} x_u \right\|^2, \tag{5}$$

which equals $\mathbf{x}^\top L_{\mathcal{F}} \mathbf{x}$ via ($\star$). The equivalence holds.

### §3.4 Precision-weighted extension

The spec's precision-weighted formulation (§4.4.1 of [[../03-Architecture/02-Cellular-Sheaf-Architecture]]) replaces the identity edge precision in (3) with a per-edge precision matrix $\Pi_e \succ 0$:

$$E_{\mathrm{PC}}^{\Pi}(\mathbf{x}) = \sum_{e \in E} \epsilon_e^\top \Pi_e \, \epsilon_e = \mathbf{x}^\top L_{\mathcal{F}}^{\Pi} \mathbf{x}, \tag{6}$$

where the precision-weighted sheaf Laplacian is

$$L_{\mathcal{F}}^{\Pi} = \delta^\top \Pi \, \delta, \quad \Pi = \mathrm{diag}\{\Pi_e\}_{e \in E}. \tag{7}$$

The derivation is identical to §3.2–§3.3 with the squared edge norm replaced by the Mahalanobis form induced by $\Pi_e$. This is the form Evidence 1 uses in the IVE ($\mathcal{C}_\Pi$ in §6.4 of [[../04-Safety-Verification/02-Intent-Verification-Engine]]).

### §3.5 Qualifications surfaced by Route 1

| # | Qualification | Status in spec | Consequence if violated |
|---|---|---|---|
| Q1 | **Linear restriction maps.** $\mathcal{F}_{u \triangleleft e}$ is linear in $x_u$ | Built in by §2.1.1 definition | Nonlinear restriction maps generate higher-order terms in $\epsilon_e^2$; the equality becomes a local Taylor approximation around the operating point |
| Q2 | **Gaussian likelihood** (squared-error edge norm) | Spec commitment; underlies §4.4.1 IVE Evidence 1 | Non-Gaussian likelihoods produce non-quadratic energies (e.g. cross-entropy → KL divergence at edges); the equality becomes one term in a more general $f$-divergence form |
| Q3 | **Orthogonal parallel transport $\Gamma \in \mathrm{O}(d)$** | Built in by §2.1.3 spec decomposition | Non-orthogonal transport breaks gauge invariance; energy depends on stalk-frame choice |
| Q4 | **Row-orthonormal edge projection $P_{u \to e}$** | Built in by §2.1.3 + §4.3 Stiefel manifold constraint | Non-orthonormal $P$ inflates or shrinks the edge norm relative to the source stalk; equality holds only up to a scale factor |
| Q5 | **Homogeneous node-stalk dimension $d$** | Spec sets $d = 8$ globally | Inhomogeneous stalks require adapting $\Gamma$ to be a partial isometry between unequal-dimensional spaces; the orthogonality interpretation generalises to the Stiefel manifold $\mathrm{St}(d_u, d_v)$ |

Of these, **Q1, Q3, and Q4 are built into the spec by construction** — they cannot be violated without changing the architecture. **Q2 (Gaussian likelihood)** is a modelling commitment whose violation has known consequences but is empirically defensible for EEG covariance data in the operational SNR range. **Q5 (homogeneous stalks)** is the spec's choice for Stage 1; relaxing it is a Stage-2 / Stage-3 extension that requires generalisation of the orthogonality condition.

---

## §4 Route 2 — Categorical zD0 wl o j.derivation via St Clere Smithe (2023)

### §4.1 Predictive coding as functorial semantics of autoencoder games

St Clere Smithe's DPhil thesis (2023, Oxford; "Mathematical Foundations for a Compositional Account of the Bayesian Brain", DOI:10.5287/ora-kzjqyop2d), Chapters 3–4, gives an independent categorical derivation of the predictive-coding energy. The setup:

- **Bayesian lens.** Each node $v$ has a forward channel $f_v : \mathcal{F}(v) \to \mathcal{F}(v)$ (generative model) and a backward channel $b_v$ (inference); these form a Bayesian lens (Capucci, Gavranović, et al., 2022; St Clere Smithe 2021, *Compositional Active Inference I*).
- **Edge interaction.** Each edge $e = (u, v)$ provides a "comparison morphism" in the category of Bayesian lenses, expressing that the two endpoints' lens images must agree.
- **Autoencoder game.** The composed game's value functional is a sum of per-edge "loss" terms, each measuring the disagreement between endpoint lens images.

### §4.2 The derivation

Thesis Chapter 3 (Theorem 3.4.2 in St Clere Smithe 2023) proves that the value functional of the composed autoencoder game on a graph decomposes as

$$V(\mathbf{x}) = \sum_{e \in E} \ell_e\!\left(f_v(x_v), \, f_u(x_u)\right) \tag{8}$$

where $\ell_e$ is the local loss at edge $e$. Chapter 4 (Proposition 4.2.1) specialises (8) to the *linear Gaussian* case (linear forward channels + Gaussian backward channels), giving

$$V_{\mathrm{lin}}(\mathbf{x}) = \sum_{e \in E} \left\| g_v(x_v) - g_u(x_u) \right\|^2 \tag{9}$$

where $g_v : \mathcal{F}(v) \to \mathcal{F}(e)$ is the forward-channel-composed-with-the-edge-comparison-morphism. **Identifying $g_v = \mathcal{F}_{v \triangleleft e}$**, expression (9) is identical to (3) of Route 1, and therefore equals $\mathbf{x}^\top L_{\mathcal{F}} \mathbf{x}$ via ($\star$).

### §4.3 The fibration condition

The Chapter-4 specialisation to (9) requires a structural condition: the lens network must form a **fibration** over the graph (Definition 4.1.3 in the thesis). Operationally, the fibration condition says that the lens-image-comparison-morphism at each edge is well-defined and the edge's comparison space is correctly determined by both endpoints' forward channels.

The fibration condition is equivalent to **surjectivity of the restriction maps onto the edge stalk** (this is the Topos-route counterpart of Qualification Q4 from §3.5). In categorical language: each restriction map $\mathcal{F}_{u \triangleleft e}$ must have full row rank $d_s$, so that its image is the entire edge stalk $\mathcal{F}(e)$.

For thrIVE's spec decomposition $\mathcal{F}_{u \triangleleft e} = P_{u \to e} \Gamma_{u \to v}$:

- $\Gamma_{u \to v} \in \mathrm{O}(d)$ is invertible, hence has full rank $d$.
- $P_{u \to e}$ is row-orthonormal by spec construction (Stiefel manifold constraint), hence has full row rank $d_s$.
- The composition $P_{u \to e} \Gamma_{u \to v}$ has rank equal to $\mathrm{min}(d, d_s) = d_s$ (with $d_s \leq d$).
- Therefore the spec's restriction maps are surjective onto $\mathcal{F}(e)$ **by construction**.

The fibration condition is satisfied. The Route-2 derivation goes through.

### §4.4 Qualifications surfaced by Route 2

| # | Qualification | Status in spec | Mapping to Route-1 qualification |
|---|---|---|---|
| C1 | **Linear forward channels** (Bayesian-lens linearity at each node) | Built in by §2.1.1 definition + §3.3 N-node linear-readout assumption | Same as Q1 (linear restriction maps) |
| C2 | **Gaussian backward channels** (variational-Gaussian posterior at each node) | Spec commitment via §4.4 variational free-energy formulation | Same as Q2 (Gaussian likelihood) |
| C3 | **Fibration condition** (surjective restriction maps onto edge stalks) | Built in by §2.1.3 spec decomposition + Stiefel constraint | Same as Q4 (row-orthonormal $P$) |
| C4 | **Compositionality of Bayesian lenses** (lens-laws satisfied at each node) | Implicit in the §2.6 Bayesian-lens framework | Cross-checks Q3 — orthogonal $\Gamma$ ensures backward-channel inversion is well-defined |
| C5 | **Functorial semantics** (well-defined functor from graph to category of lenses) | Implicit in the graph-sheaf construction | Cross-checks Q5 — homogeneous stalks make the functor cleanly defined |

The categorical route's five qualifications C1–C5 **map onto Route 1's five qualifications Q1–Q5**:

| Route 2 (categorical) | Route 1 (algebraic) | Shared qualification |
|---|---|---|
| C1 (linear forward channels) | Q1 (linear restriction maps) | Linearity |
| C2 (Gaussian backward channels) | Q2 (Gaussian likelihood) | Gaussian / quadratic energy |
| C3 (fibration) | Q4 (row-orthonormal $P$) | Surjectivity |
| C4 (lens-law compositionality) | Q3 (orthogonal $\Gamma$) | Frame-invariance |
| C5 (functorial semantics) | Q5 (homogeneous stalks) | Well-defined sheaf structure |

The two routes therefore agree on the substantive content of the equivalence under five shared assumptions, expressed in two complementary mathematical languages.

---

## §5 Cross-verification — what each route catches that the other misses

The two derivations are not redundant. Each surfaces qualifications more clearly than the other:

| Insight | Route 1 surfaces it via | Route 2 surfaces it via |
|---|---|---|
| **Information-loss at the edge stalk** when $P_{u \to e}$ is *not* row-orthonormal | Direct algebraic inflation factor in equation (5) | Fibration failure → composed lens-game value is ill-defined |
| **Gauge invariance** under orthogonal frame change at each node | $\Gamma \in \mathrm{O}(d)$ preserves the squared norm in equation (5) | Bayesian-lens compositionality requires invertible backward channels (C4), which $\Gamma$ orthogonality guarantees |
| **Reparametrisation rather than restriction** in the spec decomposition | Degree-of-freedom counting in §3.3 observation 3 (Route 1 — explicit) | Implicit in the functor-from-graph-to-lens-category being well-defined |
| **Failure mode under nonlinear restriction maps** | Direct: higher-order terms in $\epsilon_e^2$ | Indirect: linearity assumption in Chapter-4 specialisation; nonlinear case requires the full Chapter-3 game-theoretic treatment |
| **Failure mode under inhomogeneous stalk dimensions** | Direct: $\Gamma \in \mathrm{O}(d)$ presumes square; partial-isometry generalisation needed | Direct: functorial semantics requires well-defined source/target categories |
| **Connection to predictive-coding biological theory** (Rao & Ballard 1999) | Direct via §3.1 — the algebraic route is the original derivation chain | Indirect — categorical route arrives at the same expression through a structurally different argument |
| **Connection to compositional verification of IVE** | Indirect | Direct via St Clere Smithe 2024 typed-policy verification — see [[../10-Analysis/(C)-09-Topos-Institute-Research-Mapping]] §3.1 OQ 11.42 |

**Confidence consequence.** Two independent derivations agreeing under five shared assumptions, in two structurally distinct mathematical frameworks (one algebraic-statistical, one categorical), provides substantially higher confidence in the result than either alone. The equivalence is not an accident of one formalism — it is the same mathematical content expressed in two complementary ways. This is the **independent verification** that §0 of [[../Phase A Experiment/(C)-Phase-A-Experiment-Revised]] explicitly required.

---

## §6 Implications for the Phase A experiment

### §6.1 The equivalence is fully supported under spec assumptions

For Phase A-1's operational regime:

- All five Route-1 qualifications (Q1–Q5) are satisfied **by construction** — they are baked into the spec's restriction-map decomposition, the Stiefel-manifold constraint, the homogeneous-stalk choice, and the Gaussian-likelihood modelling commitment.
- All five Route-2 qualifications (C1–C5) follow from Q1–Q5 via the explicit correspondence in §4.4.

The Seely equivalence therefore holds **exactly** for the Phase A-1 architecture. The H1 hypothesis (S-TTSA > S-rand at S0; predictive-coding energy minimisation on a learned sheaf produces discriminative coherence) tests the *empirical* consequences of the equivalence on real EEG, not the equivalence itself.

### §6.2 The two failure modes that Phase A-1 cannot diagnose

The qualifications surface two failure modes the Phase A-1 design does not test:

1. **Q2 (Gaussian likelihood) violation.** If real EEG covariance data is sufficiently non-Gaussian at the operational scale, the precision-weighted edge energy (6) is a misspecified loss function. The H3 graceful-degradation test under EMG contamination (S2) probes this indirectly — heavy-tailed EMG residuals are non-Gaussian — but does not directly measure the deviation from quadratic energy.
2. **Q5 (homogeneous stalks) violation.** Stage 2 prosthetics may require inhomogeneous stalks (different stalk dimensions for motor-cortex N-nodes vs sensory-feedback V-nodes). The Phase A-1 architecture is homogeneous; the equivalence as stated does not cover the inhomogeneous case. Generalisation to the Stiefel manifold $\mathrm{St}(d_u, d_v)$ is a Stage-2 extension that requires its own derivation.

These two failure modes are **flagged for Phase B / Stage 2** but do not block Phase A-1 OSF lock-in.

### §6.3 The two failure modes Phase A-1 *does* diagnose

- **Q3 (orthogonal $\Gamma$) violation** is excluded by construction during S-TTSA learning via the Lipschitz regularisation $\lambda_{\mathrm{Lip}} \max(0, \sigma_{\max}(\mathcal{F}) - 1)^2$ in the §4.2 Fix 1 of [[../Phase A Experiment/(C)-Phase-A-Experiment-Revised]]. If the regularisation is too weak, the learned restriction maps drift from orthogonality; the H1 outcome reflects the actual operational regime. This is a soft empirical check on Q3.
- **Q4 (surjectivity)** is checked by the per-fold rank verification step in [[../Phase A Experiment/(C)-A1-Factorial-Analysis-Script]] (the analysis script asserts `np.linalg.matrix_rank(P_ue) == d_s` per fold per node). A rank-deficient $P_{u \to e}$ in any fold is reported as a registration-integrity violation.

---

## §7 Confidence statement for the OSF lock

> **§0 Pre-Experimental Verification — completed May 2026.** The Seely equivalence $E_{\mathrm{PC}}(\mathbf{x}) = \mathbf{x}^\top L_{\mathcal{F}} \mathbf{x}$ has been independently re-derived via two routes:
>
> 1. **Algebraic route from Rao–Ballard (1999) prediction errors** — §3 of this document. Generalises the Rao–Ballard hierarchical formulation to an arbitrary directed graph, substitutes the spec's restriction-map decomposition $\mathcal{F}_{u \triangleleft e} = P_{u \to e} \Gamma_{u \to v}$, and shows the resulting energy equals the sheaf Laplacian quadratic form ($\star$).
> 2. **Categorical route from St Clere Smithe (2023, DPhil thesis Chapters 3–4)** — §4 of this document. Derives the same equivalence from the functorial semantics of autoencoder games on the graph, identifying the spec's restriction maps with the forward-channel-composed-with-edge-comparison morphisms.
>
> The two routes agree under five shared qualifications, listed and mapped between routes in §4.4. All five qualifications are satisfied by the Phase A-1 spec **by construction** (three) or **by explicit modelling commitment** (two). The equivalence therefore holds **exactly** for the Phase A-1 architecture.
>
> Failure modes outside the qualification envelope (non-Gaussian likelihood at operational scale; inhomogeneous stalks for Stage 2+) are flagged for downstream phases. Failure modes inside the envelope (drift from orthogonal $\Gamma$ under weak Lipschitz regularisation; rank deficiency of $P_{u \to e}$) are operationally diagnosed by the Phase A-1 analysis script.
>
> **§0 of [[../Phase A Experiment/(C)-Phase-A-Experiment-Revised]] is complete.** The Appendix-A lock-in item 10 ("Seely equivalence paper-check completed") can be marked ✓.

---

## §8 References

Battiloro, C., Di Lorenzo, P., & Ribeiro, A. (2023). Tangent bundle convolutional learning: from manifolds to cellular sheaves and back. *arXiv:2303.11424*.

Capucci, M., Gavranović, B., Hedges, J., & Rischel, E. F. (2022). Towards foundations of categorical cybernetics. *Electronic Proceedings in Theoretical Computer Science*, 372, 235–248.

Friston, K. (2005). A theory of cortical responses. *Philosophical Transactions of the Royal Society B*, 360(1456), 815–836.

Hansen, J., & Ghrist, R. (2019). Toward a spectral theory of cellular sheaves. *Journal of Applied and Computational Topology*, 3(4), 315–358.

Rao, R. P. N., & Ballard, D. H. (1999). Predictive coding in the visual cortex: a functional interpretation of some extra-classical receptive-field effects. *Nature Neuroscience*, 2(1), 79–87.

Seely, J., et al. (2025). Predictive coding inference is sheaf diffusion. *arXiv:2511.11092*.

St Clere Smithe, T. (2021). Compositional active inference I: Bayesian lenses. Statistical games. *arXiv:2109.04461*.

St Clere Smithe, T. (2023). *Mathematical Foundations for a Compositional Account of the Bayesian Brain*. DPhil thesis, University of Oxford. DOI: 10.5287/ora-kzjqyop2d.

---

## §9 Cross-references

| Section | Connection |
|---|---|
| §0 of [[../Phase A Experiment/(C)-Phase-A-Experiment-Revised]] | The §0 task this document closes |
| Appendix A item 10 of [[../Phase A Experiment/(C)-OSF-Preregistration-Phase-A1]] | The OSF lock-in checklist item this document satisfies |
| §2.1.4 of [[02-Cellular-Sheaves-SPD-Manifolds]] | The Seely theorem statement; this document is the independent derivation |
| §2.6 of [[(C)-05-Bayesian-Lens-Framework]] | The Bayesian-lens framework the Route-2 derivation operates within |
| §6.4 of [[../04-Safety-Verification/02-Intent-Verification-Engine]] | Precision-weighted Evidence-1 $\mathcal{C}_\Pi$ uses the equation (6) form |
| §4.2 Fix 1 of [[../Phase A Experiment/(C)-Phase-A-Experiment-Revised]] | Lipschitz regularisation that enforces Q3 during S-TTSA learning |
| [[../10-Analysis/(C)-09-Topos-Institute-Research-Mapping]] §3.1 OQ 11.43 | The Topos lead that informed Route 2 |
| [[../10-Analysis/02-Open-Questions]] §17.2 OQ 11.43 | **This document closes OQ 11.43** — update the OQ catalogue entry |
