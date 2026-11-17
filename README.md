# Is Physical Attractiveness Normally Distributed? — Reproducibility Materials

Code, transcribed published summary statistics, numerical checks, and figures accompanying a [*methodological review*](https://datepsych.substack.com/p/does-physical-attractiveness-follow) of Date Psychology's **“Is Physical Attractiveness Normally Distributed?”** (2022).

The companion review evaluates the OKCupid rating distributions, the central limit theorem, comparison of attractiveness ratings across observer groups, a 2026 meta-analysis, spousal attractiveness, and fertility claims.

**Scope:** These are reconstructions from published, often rounded, **aggregate statistics**. This repository is **not** an independent replication of the underlying participant-level studies or a full rerun of the 2026 meta-analysis. It is designed to make the calculations and original charts in the companion critique inspectable and reproducible.

## Contents

| File | Purpose |
| --- | --- |
| `reproduce_attractiveness_figures.py` | Reads the input CSVs, checks arithmetic, prints results and regenerates five figures. |
| `wood_brumbaugh_2009_ratings.csv` | Means, SDs and sample sizes of rater groups (Table 4). |
| `meta_analysis_reported.csv` | The 2026 published pooled effect and interval; no underlying effect-size records. |
| `meltzer_2014_couples.csv` | Four newlywed sample means and reported t statistics. |
| `jokela_2009_women.csv` | Adjusted fertility means and published confidence intervals by quartile. |
| `facial_shape_mediation_reported.csv` | Published rounded total and adjusted estimates for each rater sex. |
| `other_reported_checks.csv` | Additional original-study values (McNulty 2008, Jokela offspring-sex tests, shape-path coefficients). |
| `reconstruction_results.txt` | Checked example console output from the script. |
| `figure_02_wood_raters.png` | Means of ratings of the same face sets, by observer group. |
| `figure_03_meta_analysis.png` | Published 2026 pooled difference and confidence interval. |
| `figure_04_jokela_fertility.png` | Published adjusted means and confidence intervals; female quartiles. |
| `figure_05_couples.png` | Published mean attractiveness for husbands and wives across four studies. |
| `figure_06_normal_illustration.png` | **Hypothetical** Gaussian curves with different means; not observed data. |
| `REPRODUCTION_NOTES.md` | Provenance, claim-to-evidence map, assumptions and non-reproducible claims. |
| `requirements.txt` | Python dependencies. |
| `.gitignore` | Common Python transient files. |

Figure numbers correspond to the Substack article. **Figure 1, the historical OKCupid graphic, is not included**: its underlying data and plotting process are not provided, and the third-party image is not redistributed.

## Reproduce the calculations and figures

Use Python 3.10 or later, in the directory containing these files:

```bash
python -m pip install -r requirements.txt
python reproduce_attractiveness_figures.py
```

The script reads the CSV files in the same directory, reports key results to the terminal, writes `reconstruction_results.txt`, and regenerates the five included PNGs. Run in a working copy if you want to preserve the checked-in images.

To run numerical validations **without rendering charts**, use:

```bash
python reproduce_attractiveness_figures.py --check-only
```

The script checks the input structure and the main reported arithmetic; it does not claim to reconstruct unreported original test statistics.

## Methods and interpretation

- **Wood & Brumbaugh:** Means are published percentages of maximum possible (POMP) attractiveness ratings. The plotted groups rate the **same face set within each face-sex category**, but observer sex and sexual orientation are not independently isolated by the design.
- **2026 meta-analysis:** The pooled effect, CI and I² are directly transcribed, **not reestimated**; no study-level forest plot or independent meta-analysis can be generated from the aggregate values alone.
- **Newlywed samples:** Means and nonsignificance statements come from Meltzer et al. (2014); Study 1 overlaps with the McNulty et al. (2008) cohort. The four samples are not four independent replications of the original sample.
- **Jokela:** The plotted quartile means are adjusted estimated **numbers of children**, not proportions of individuals who reproduced. The displayed 16% and 6% statements are relative child-count contrasts and depend on the reference category; the chart itself uses the reported adjusted means and CIs.
- **Mediation:** Rounded total and adjusted effects yield the same absolute reduction for male and female observers. Differences in *percentage* attenuation are not independent evidence of stronger causal mediation in one group.
- **Normality illustration:** The Gaussian curves are hypothetical and demonstrate only that different means are compatible with normally distributed variables.

For detailed caveats and numerical provenance, read [`REPRODUCTION_NOTES.md`](REPRODUCTION_NOTES.md).

## Principal sources

1. Date Psychology (2022), [“Is Physical Attractiveness Normally Distributed?”](https://datepsychology.com/is-physical-attractiveness-normally-distributed/)
2. Rudder (2009), [original OKCupid/OkTrends rating comparison (archived)](https://gwern.net/doc/psychology/okcupid/yourlooksandyourinbox.html); also *Dataclysm* (2014), cited in the companion critique.
3. Wood & Brumbaugh (2009), [*Using Revealed Mate Preferences to Evaluate Market Force and Differential Preference Explanations for Mate Selection*](https://doi.org/10.1037/a0015300), Table 4.
4. Wassiliwizky et al. (2026), [*The Gender Attractiveness Gap*](https://doi.org/10.1098/rspb.2026.0362), published meta-analysis and mediation results.
5. McNulty, Neff & Karney (2008), [study of partner attractiveness and marital behavior](https://doi.org/10.1037/0893-3200.22.1.135).
6. Meltzer, McNulty, Jackson & Karney (2014), [*Sex Differences in the Implications of Partner Physical Attractiveness for the Trajectory of Marital Satisfaction*](https://pmc.ncbi.nlm.nih.gov/articles/PMC4011637/), Table 1.
7. Jokela (2009), [*Physical Attractiveness and Reproductive Success in Humans*](https://pmc.ncbi.nlm.nih.gov/articles/PMC3000557/), Tables 2–3.

Other studies discussed in the critique are not recreated because the necessary input data or calculations are not available in this compact package.

**No copyrighted paper PDFs, third-party website copies, private data, or original OKCupid image are redistributed.** Only transcribed published numerical summaries and newly generated charts are included.


