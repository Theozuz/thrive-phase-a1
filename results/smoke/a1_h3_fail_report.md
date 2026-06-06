# Phase A-1 Factorial Analysis — Results Report

Generated: 2026-06-06T17:42:49.693549+00:00
Git commit: `GIT_UNAVAILABLE`
Script SHA-256: `0bd6b2e4332061dcf13f36e19ad12226429403764de2a60558fd7a87c82b0792`
Include R_FM: `True`

## H1 (Claim C1) — Sheaf coherence is discriminative — **PASS**

```json
{
  "hypothesis": "H1 (Claim C1) \u2014 Sheaf coherence is discriminative",
  "test": "Paired BEST (S-TTSA vs S-rand at S0)",
  "n_subjects": 109,
  "mean_sttsa": 0.7141160590440859,
  "mean_srand": 0.5651833103395628,
  "cohens_d": 5.687839322247805,
  "BF10": 5.53e+80,
  "p_one_sided": 1.3542077738541737e-84,
  "ci_95": [
    0.14416866888589136,
    0.15392144437434763
  ],
  "threshold": 3.0,
  "passed": true,
  "halt_if_fail": true
}
```

## H2 (Claim C2) — Sheaf layer recovers information (vs R8) — **PASS**

```json
{
  "hypothesis": "H2 (Claim C2) \u2014 Sheaf layer recovers information (vs R8)",
  "test": "Paired one-sided t-test ((R8+S) vs R8 at S0)",
  "n_subjects": 109,
  "mean_r8s": 0.886421535173668,
  "mean_r8": 0.8513354938759339,
  "cohens_d": 2.1793489545142393,
  "p_one_sided": 2.657928046515146e-43,
  "BF10": 7.705908256880734e+39,
  "ci_95": [
    0.032164432232704744,
    0.038134315421596156
  ],
  "threshold_d": 0.2,
  "threshold_alpha": 0.05,
  "passed": true
}
```

## H3 (Claim C4) — Sheaf coherence degrades gracefully — **FAIL**

```json
{
  "hypothesis": "H3 (Claim C4) \u2014 Sheaf coherence degrades gracefully",
  "test": "rmANOVA: representation x stressor interaction + Holm pairwise",
  "F_interaction": 0.7699213755205171,
  "p_interaction": 0.7377730561447045,
  "pairwise_holm": [
    {
      "stressor": "S0",
      "n": 109,
      "d": -4.9322496569355385,
      "p_raw": 1.0,
      "p_holm": 1.0,
      "rejected": false
    },
    {
      "stressor": "S1",
      "n": 109,
      "d": -4.8521434701950215,
      "p_raw": 1.0,
      "p_holm": 1.0,
      "rejected": false
    },
    {
      "stressor": "S2",
      "n": 109,
      "d": -4.387432637508533,
      "p_raw": 1.0,
      "p_holm": 1.0,
      "rejected": false
    },
    {
      "stressor": "S3",
      "n": 109,
      "d": -4.135167830985991,
      "p_raw": 1.0,
      "p_holm": 1.0,
      "rejected": false
    }
  ],
  "threshold_alpha": 0.05,
  "passed": false
}
```

## H4 (§9.5) — Sheaf adds value over foundation model — **PASS**

```json
{
  "hypothesis": "H4 (\u00a79.5) \u2014 Sheaf adds value over foundation model",
  "test": "Paired one-sided t-test ((R_FM+S) vs R_FM at S0)",
  "n_subjects": 109,
  "mean_rfms": 0.9203402980142426,
  "mean_rfm": 0.8948137981090192,
  "cohens_d": 2.1130925087542165,
  "p_one_sided": 4.1546771895086034e-42,
  "BF10": 5.254e+38,
  "ci_95": [
    0.02336150145658586,
    0.027912260892278436
  ],
  "threshold_d": 0.2,
  "threshold_alpha": 0.05,
  "passed": true
}
```

## §9.6 Joint H2/H4 Interpretation

**Verdict:** STRONGEST: sheaf adds value over both R8 and R_FM baselines. Proceed with full v5.5 architecture.

**Action:** `proceed_full_architecture`
