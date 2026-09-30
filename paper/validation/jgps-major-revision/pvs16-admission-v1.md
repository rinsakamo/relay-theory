# PVS-16 prospective admission v1

Status: **FROZEN BEFORE GRAMMAR MAPPING**

Authority: #365

The 16 validation sources are selected mechanically from the pre-Grammar
180-source candidate ledger. The ledger validator binds record order to the
frozen designed-corpus geometry and candidate rank.

Selection rule:

1. stay within each of the eight primary construct strata;
2. scan the frozen ledger in its validator-bound record order;
3. exclude identities already used in the activated 60-source manifest;
4. require a frozen `CANDIDATE` row with readable/non-`INACCESS` status;
5. admit the first two remaining rows.

This yields the rank-2 and rank-3 reserve candidates of slot 01 in each lane.
No diversification, source swapping, Grammar-fit inspection, ClaimIR creation,
or role mapping was performed before admission.

The admission JSON records `grammar_mapping_inspected=false` for every claim.

Important limitation: these sources were already present in the pre-Grammar
candidate ledger and had source-level screening metadata. They are prospective
with respect to ClaimIR/Grammar mapping and were not members of the original
60-claim induction corpus; they are not source-unseen to the research program.

Terminal:

`PVS16_ADMISSION_FROZEN_BEFORE_GRAMMAR_MAPPING`
