# Reproducibility and data dictionary

## Source and transformation

The research team supplied `textual_metrics_results.xlsx` and
`resumen_analisis_mensual.xlsx`. Their SHA-256 hashes are retained in
`data/provenance.json`; the original workbooks and private links are not redistributed.
Numeric and aggregate sheets were exported as UTF-8 CSV without changing numeric
precision. Workbook numeric row IDs 1–15 become P01–P15. No mapping to personal
names is distributed. Text response fields and identifiable submission filenames
are excluded.

## Data dictionary

| CSV | Rows | Meaning |
| --- | ---: | --- |
| `prompt_transition_distances.csv` | 60 | One direct cosine distance/similarity per participant and consecutive transition |
| `participant_centroid_distances.csv` | 75 | One participant-to-stage-centroid cosine distance at each of five stages |
| `stage_centroid_vectors.csv` | 5 | Archived 384-dimensional stage centroids; columns d000–d383 |
| `aggregate_term_weights.csv` | 30 | Aggregate term weights at each prompting stage |
| `monthly_corpus_summary.csv` | 10 | Monthly selected-corpus counts and exported mean polarity |

Cosine distances and term weights are dimensionless. Counts describe this selected
corpus and workshop, not the incidence of violence in the population. Mean polarity
is an exported descriptive output; the historical sentiment pipeline is not rerun.
The corpus count table does not substitute for a complete article-level source list.

## Direct distance summaries and precision

`table4_participant_summaries.csv` uses the distances rounded to four decimals,
matching the printed Table 4. Its within-participant variance uses denominator four.
Quartile boundaries are computed from participant mean distances.

`table5_from_printed_table4.csv` implements the proof's stated convention of
calculating summaries from the displayed Table 4 values. `table5_full_precision.csv`
uses the original exported values. Sample standard deviations use N−1. Tiny
differences in the fourth decimal can result from this explicit input-precision
choice; both outputs are named accordingly.

## Paired centroid tests

For participant i and stages t and t+1, define the paired difference as
`D_i = delta_i,t+1 - delta_i,t`.

The exported statistic `median_delta` is `median(D_i)`. It is not generally equal
to `median(delta_i,t+1) - median(delta_i,t)`. Both quantities are included as
separate columns in `table6_centroid_tests.csv`.

Each two-sided Wilcoxon signed-rank test uses the paired stage distances and
`zero_method="wilcox"`. The archived arrays have 15 nonzero paired differences;
`method="exact"` reproduces all four source-workbook W statistics and raw p-values.
Holm adjustment uses full-precision raw p-values, before formatting for display.

For P1→P2, W=13, raw p=0.00537109375 and Holm-adjusted p=0.021484375.
For P4→P5, raw p=0.03533935546875 and Holm-adjusted p=0.10601806640625.
Only P1→P2 meets the Holm-adjusted 0.05 threshold.

Stage-specific centroids are estimated from the same workshop participants, inducing
dependence through a shared reference. The tests remain exploratory and do not
establish causal learning, independent-pair inference or population generalizability.

## What is verified

`--verify` checks complete and unique observation keys, distance/similarity
complements, agreement of every rounded direct distance with printed Table 4,
Table 5 under its printed-input convention, exact reproduction of archived
Wilcoxon statistics/raw p-values/median paired differences, and the 105-item
monthly total. Input inconsistencies raise an error and fail the CI job.

## What is not regenerated

This release starts from archived numerical exports. It does not reconstruct the
historical sentence embeddings, recover missing questionnaire responses, generate
new images, collect the news corpus, or reproduce the infographic/video creation.
Original response texts, the complete article URL list, the historical pipeline
and the video are outside the distributed release. No replacement synthetic data
are supplied as if they were original observations.
