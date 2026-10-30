# Numerical corrections supported by the archived source

These corrections follow from recomputing the author-exported centroid distances.

1. In Table 6, replace **Difference in medians** with **Median paired difference**.
   Preserve the exported paired-difference values −0.1448, 0.0004, 0.0593 and
   0.0411. The corresponding differences of stage medians are different and are
   exported separately for transparency.
2. Define the descriptive statistic as
   `median_i(delta_i,t+1 - delta_i,t)`, not a subtraction of stage medians.
3. Calculate Holm adjustment before rounding raw p-values. The adjusted values
   rounded to four decimals are **0.0215, 0.7788, 0.7788, 0.1060**.
4. In the text and conclusions, replace adjusted p=0.0216 with 0.0215 and
   adjusted p=0.1059 with 0.1060. The raw p-values printed to four decimals
   remain 0.0054, 0.7197, 0.3894 and 0.0353. The significance conclusion is unchanged.
5. Describe −0.1448 as the median within-participant change in distance to the
   stage-specific centroid. It is not the difference between the two group medians.

The source workbook, exported CSV and executable analysis agree. These are
definition/precision corrections and do not introduce new observations or tests.
