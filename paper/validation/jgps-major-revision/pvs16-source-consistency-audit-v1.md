# PVS-16 source-consistency audit v1

Status: **ASSISTANT AUDIT PASS — HUMAN REVIEW STILL REQUIRED**

This audit cross-checks the 16 frozen, unreviewed ClaimIR candidates against public source abstract/full-text surfaces. It does **not** change any candidate to `reviewed`, does not establish independent human agreement, and does not inspect Grammar-v0 mappings.

Admission authority: `0a4454887189730cf4b13d12061f4cab93fb8e4d8f0ec089a08f77bc088dc123`

| Claim | Assistant audit | Source-consistency finding |
|---|---|---|
| `PVS-MEM-01` | PASS | Candidate preserves the published abstract-level comparison: amnesic participants acquired the mirror-reading skill at a rate equivalent to matched controls and retained it for at least three months. |
| `PVS-MEM-02` | PASS | Candidate preserves the source distinction between conscious recollection and facilitation of test performance without conscious recollection, including dissociation across tasks/populations. |
| `PVS-LRN-01` | PASS | Candidate preserves the reported competition/differential engagement of medial-temporal and basal-ganglia systems under different task emphases and the training-related change in reliance. |
| `PVS-LRN-02` | PASS | Candidate preserves the distraction manipulation, comparatively preserved overall performance, reduced flexible/declarative knowledge, and the shift in neural-system association. |
| `PVS-SKL-01` | PASS | Candidate preserves the review-level claims linking acquisition, consolidation, retention, and functional/structural neural reorganization across timescales. |
| `PVS-SKL-02` | PASS | Candidate preserves the review-level stage progression from acquisition/planning through consolidation/automatization and associated changes in cortico-striatal organization. |
| `PVS-ATT-01` | PASS | Candidate preserves the biased-competition account: multiple visual representations compete and biasing signals favor behaviorally relevant objects. The candidate remains deliberately generic about mechanism beyond the reviewed source. |
| `PVS-ATT-02` | PASS | Candidate preserves the experiment: paired receptive-field stimuli produce competition, task relevance biases the neuronal response toward the selected stimulus, and the effect is smaller for a single stimulus. |
| `PVS-PRD-01` | PASS | Candidate preserves the Bayesian integration claim that estimates combine a prior with sensory evidence and that increasing sensory uncertainty increases reliance on the prior. |
| `PVS-PRD-02` | PASS | Candidate preserves the review claim that efficient perception/action requires representing uncertainty, with probabilistic distributions and population-level neural schemes proposed as coding implementations. |
| `PVS-CTL-01` | PASS | Candidate preserves the optimal-feedback-control description: state estimation from sensory feedback/efferent copy, goal-directed output adjustment, and selective correction of performance-relevant errors. |
| `PVS-CTL-02` | PASS | Candidate preserves task-dependent flexible control, late-target perturbation correction, and the experimentally supported stability-accuracy tradeoff. |
| `PVS-BLF-01` | PASS | Candidate preserves the dynamic-environment result: unexpected outcomes receive more weight when they indicate a change point; update gain varies with surprise/change probability and decays as evidence accumulates. |
| `PVS-BLF-02` | PASS | Candidate preserves the hierarchical Bayesian architecture: multiple uncertainty levels, higher-level control of lower-level evolution, cross-level coupling, and precision-weighted trial-wise updating. |
| `PVS-CNC-01` | PASS | Candidate preserves causal-model theory: probabilistic causal mechanisms link category features and categorization depends on how likely observed features are under those mechanisms. |
| `PVS-CNC-02` | PASS | Candidate preserves the causal-status result: feature importance depends on causal position, and experimental manipulation of causal position changes feature centrality/importance. |

Terminal:

`PVS16_ASSISTANT_SOURCE_CONSISTENCY_PASS_HUMAN_REVIEW_NOT_YET_SATISFIED`
