# G2-D v10d: official INT08 source-native experimental caveat detector correction and final receipt (append only)

Authority issue #399, G2 frozen parent `69748673c80f421605f1c63607472903ac2ed68c`, independent INT-only draft PR #430. Original v10 Japanese review and all CI historical results are preserved, not overwritten.

## Actual primary publisher evidence

Published VOR eLife `10.7554/eLife.74445`, eLife 2022-04-11 v3 publisher PDF `https://cdn.elifesciences.org/articles/74445/elife-74445-v3.pdf` independently **HTTP200/4,476,771B/43 printed PDF pages**, raw SHA-256 **`89f8846ab34dbc5af0d4079423ff51e00c1873b6149c48217b547b1bdcb678da`**, exactly the original frozen G2 provenance byte identity. Timed firstparty HTTP 12s; browser fallback 18s not used because publisher's canonical VOR binary succeeded.

The original firstparty formal PDF on p6 says that for the human RM/DM/NM three-condition comparison **the experimenters imposed by hand an end-of-event episodic encoding policy**. Episodic retrieval is learned using EM-gate-modulated LCA within LSTM model; subsequent analyses compare selective encoding schedules and test mid-event encoding harms. It is not an end-to-end free joint learning experiment for *both* retrieval and encoding in *all* task regimes.

**Two source-extractor false negatives corrected without altering original bytes**:
- v10b independent CI `37206213517` obtained the correct VOR SHA and recorded exact firstparty p6 text, but a naive uninterrupted literal-string phrase check reported `false` for the true author-stated hand policy because of source PDF line breaks/punctuation.
- v10c independent CI `37206294340` tried regexp normalization but erroneously **double-escaped** `\\s` in a Python raw-regexp, again reported `false`. This was a testing-instrument false negative, NOT author science; retain both historical failed-witness runs and their evidence/assumptions.
- [Actual corrected v10d independently rerun `37206404322`](https://github.com/rinsakamo/relay-theory/actions/runs/37206404322) is **SUCCESS**. Same original raw SHA `89f8846ab34dbc5af0d4079423ff51e00c1873b6149c48217b547b1bdcb678da`, same 43p, same PDF 4,476,771B. Strict PDF-native proximity after whitespace normalization reports `human_comparison_hand_fixed_end_of_event_encoding_condition=true` and **exact original page witness [6]**. The correction was solely detector regex; no science evidence modified to satisfy test.

**Bounded source-native pair adjudication** remains `INT04_INT08_DIFFERENT_PRIMARY_OPERATIONS_WITH_SHARED_MEMORY_ANCESTRY`: INT04 one-shot MHN offline replay trains VAE latent schema, extended high-error feature residual; INT08 online LSTM state-needs-based LCA episodic retrieval gate with manually constrained encoding in human comparison task. Same high-level memory/hpc-neocortical theory vocabulary cannot by itself prove duplicated central model, while local distinct mechanisms cannot prove every central-mathematical ancestry/G1-40 family all-clear either.

INT04 original published main 20p+science supp9p+reporting2p had its 7/7 main figures, all 3 official supp figures, and supp equations(1)–(3) *physically reviewed* using independently original SHA-locked renders in v8–v9. INT08 43p source is independently exact original verified and selected primary main methods evidence extracted, **not all its figures/appendices or global central family qualified**.

No backup formally adopted; neither MAIN structure nor H0/H1/H2 computed; no author MAIN GO.
