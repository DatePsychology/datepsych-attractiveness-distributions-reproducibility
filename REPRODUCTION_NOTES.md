# Reproduction notes and claim-to-evidence map

This is an **aggregate-statistic reconstruction**, not a rerun of the original surveys, matching models, individual-level face-rating studies, or the 2026 meta-analysis. It does not establish causal mechanisms.

| Claim in companion article | Published input | Script output | Limits |
|---|---|---|---|
| The 2026 synthesis reports a positive overall difference | 52 studies, 59 estimates; pooled 0.36 [0.29, 0.42]; I² = 89.86% | Figure 3 and numeric summary | Replot of published aggregate; no new meta-analysis or prediction interval |
| Same faces receive different mean scores from different observer groups | Wood & Brumbaugh (2009), Table 4, mean POMP: 40.9, 31.1, 38.9, 25.8 | Figure 2 and paired-face-set mean differences | Group sex and sexual orientation vary together; no identification of a pure sex effect |
| Newlywed couples do not demonstrate a female advantage in mean ratings | McNulty (2008) rounded 4.5 vs 4.3; Meltzer (2014) 4 studies, published sex comparisons nonsignificant | Figure 5 and four husband−wife differences | Non-significance is a reported finding, NOT reestimated from subject data; Study 1 overlaps McNulty 2008 |
| Jokela does not show monotonic increase in female fertility across attractiveness quartiles | Adjusted means and CIs from Table 3 Model A | Figure 4 and illustrative percent contrasts | The article's 16%/6% comparison uses a combined reference group; baseline weighting and unrounded estimates can differ; those are child counts, not birth probabilities |
| Jokela does not support offspring-sex claim | Published female trend p = .89; pooled OR = .97, p = .28 | Printed provenance checks only | Cannot recompute p-values without underlying data |
| Shape mediation has same rounded absolute reduction for both rater sexes | Published total/adjusted values .336/.224 and .260/.148; 33.25%/42.98% reported | Printed reductions and proportions | Percentages based on rounded coefficients will differ slightly from reported percentages; does not resolve model specification or identify causal mediation |
| CLT and Gaussian-overlap arguments are conceptual | Hypothetical normal densities with means 0 and 0.85 | Figure 6 | Schematic only: **not** observed attractiveness data |

## Figure 1 from the Substack article

The article also reproduces a historical OKCupid histogram/ratings graphic as **Figure 1**. This public repository intentionally does **not** redistribute that third-party figure or claim it can be regenerated from individual OKCupid ratings. The rating-level data, sampling/aggregation process, and original plotting code are not supplied. Consult the original Date Psychology post and the archived Rudder/OkTrends analysis.

## Why the mediation percentages are not independent mechanisms

- Female observers: 0.336 − 0.224 = **0.112**; 0.112 / 0.336 = 33.3% (vs published 33.25% using unrounded values).
- Male observers: 0.260 − 0.148 = **0.112**; 0.112 / 0.260 = 43.1% (vs published 42.98% using unrounded values).
- Thus the *absolute* attenuation is identical at the printed precision. The distinct *percentages* principally reflect unequal denominators.
- The independently printed reported paths (1.363 and −0.157) multiply to about −0.214. That does not straightforwardly equal the printed coefficient attenuation 0.112. This is a **reporting/specification reconciliation question**, **not** proof of a computational error or invalid statistical mediation; different models or scales may be involved. The script shows arithmetic only.

## What is and is not verified

**Reproducible here:** CSV transcription, CSV-to-figure transformations, simple percentage/difference checks, and conceptual normal curves.

**Not independently reproduced:** underlying rater-level records, estimate-level forest plot, the original meta-analysis weights and moderator models, exact mediation model, original platform rating distributions, significance tests from raw participant records, and causal inference. Some source authors make fuller data/code available online; this compact companion repository does not download or mirror them.

**No confidence intervals on Wood rater-group comparisons** are calculated: the published SDs are observer-level SDs, targets overlap across groups, and a naive independence assumption would not account for the actual design. No t-tests are inferred from the plot.
