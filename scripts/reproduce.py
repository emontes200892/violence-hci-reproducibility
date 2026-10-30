#!/usr/bin/env python3
"""Reproduce numerical summaries from archived author exports, without network access."""
from pathlib import Path
import argparse, csv, json
import numpy as np
from scipy.stats import wilcoxon
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]

def read_csv(path):
    with path.open(encoding='utf-8',newline='') as stream:
        return list(csv.DictReader(stream))

def write_csv(path,fields,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields)
        writer.writeheader();writer.writerows(rows)

def holm_adjust(p_values):
    p=np.asarray(p_values,dtype=float)
    order=np.argsort(p,kind='stable')
    sorted_adjusted=np.minimum(1.,np.maximum.accumulate(p[order]*(len(p)-np.arange(len(p)))))
    adjusted=np.empty_like(p);adjusted[order]=sorted_adjusted
    return adjusted

def validate_and_load():
    rows=read_csv(ROOT/'data/derived/prompt_transition_distances.csv')
    expected_ids=[f'P{i:02d}' for i in range(1,16)]
    expected_pairs=[(f'Prompt_{i}',f'Prompt_{i+1}') for i in range(1,5)]
    values={}
    for row in rows:
        key=(row['participant_id'],row['source_stage'],row['target_stage'])
        if key in values:raise ValueError(f'Duplicate transition observation: {key}')
        distance=float(row['cosine_distance']);similarity=float(row['cosine_similarity'])
        if not np.isfinite(distance) or not 0<=distance<=2:raise ValueError(f'Invalid cosine distance: {key}')
        if not np.isclose(distance+similarity,1,atol=1e-12):raise ValueError(f'Distance/similarity mismatch: {key}')
        values[key]=distance
    expected_keys={(pid,a,b) for pid in expected_ids for a,b in expected_pairs}
    if set(values)!=expected_keys:raise ValueError('Expected exactly 15 participants x four transitions')
    direct=np.array([[values[(pid,a,b)] for a,b in expected_pairs] for pid in expected_ids])

    centroid_rows=read_csv(ROOT/'data/derived/participant_centroid_distances.csv');centroid_values={}
    for row in centroid_rows:
        key=(row['participant_id'],row['stage'])
        if key in centroid_values:raise ValueError(f'Duplicate centroid-distance observation: {key}')
        value=float(row['cosine_distance'])
        if not np.isfinite(value) or not 0<=value<=2:raise ValueError(f'Invalid centroid distance: {key}')
        centroid_values[key]=value
    if set(centroid_values)!={(pid,f'Prompt_{i}') for pid in expected_ids for i in range(1,6)}:
        raise ValueError('Expected exactly 15 participants x five centroid-distance stages')
    centroid=np.array([[centroid_values[(pid,f'Prompt_{i}')] for i in range(1,6)] for pid in expected_ids])
    return expected_ids,direct,centroid

def describe(values):
    return [dict(transition=f'P{i+1}->P{i+2}',mean=float(values[:,i].mean()),
                 median=float(np.median(values[:,i])),sample_sd=float(values[:,i].std(ddof=1)),
                 minimum=float(values[:,i].min()),maximum=float(values[:,i].max()),
                 mean_similarity=float(1-values[:,i].mean())) for i in range(4)]

def analyze(centroid):
    results=[]
    for i in range(4):
        source,target=centroid[:,i],centroid[:,i+1]
        result=wilcoxon(source,target,zero_method='wilcox',alternative='two-sided',method='exact')
        results.append(dict(transition=f'P{i+1}->P{i+2}',n_pairs=len(source),
                            median_source=float(np.median(source)),median_target=float(np.median(target)),
                            median_paired_difference=float(np.median(target-source)),
                            difference_of_stage_medians=float(np.median(target)-np.median(source)),
                            wilcoxon_statistic=float(result.statistic),raw_p=float(result.pvalue)))
    adjusted=holm_adjust([x['raw_p'] for x in results])
    for row,p in zip(results,adjusted):row.update(holm_adjusted_p=float(p),significant_after_holm=bool(p<.05))
    return results

def verify(ids,direct,results):
    printed=read_csv(ROOT/'data/reference/proof_table4_printed.csv')
    if [x['participant_id'] for x in printed]!=ids:raise AssertionError('Printed-table ID order mismatch')
    expected=np.array([[float(x[f'p{i+1}_p{i+2}']) for i in range(4)] for x in printed])
    np.testing.assert_allclose(np.round(direct,4),expected,rtol=0,atol=1e-12)
    expected_stats=read_csv(ROOT/'data/reference/workbook_wilcoxon.csv')
    for row,expected_row in zip(results,expected_stats):
        for field in ['median_source','median_target','median_paired_difference','wilcoxon_statistic','raw_p']:
            np.testing.assert_allclose(row[field],float(expected_row[field]),rtol=0,atol=1e-12)
    table5=read_csv(ROOT/'data/reference/proof_table5_printed.csv')
    for row,expected_row in zip(describe(np.round(direct,4)),table5):
        for field in ['mean','median','sample_sd','minimum','maximum','mean_similarity']:
            if abs(row[field]-float(expected_row[field]))>5.000001e-5:raise AssertionError(f'Printed Table 5 mismatch: {field}')
    monthly=read_csv(ROOT/'data/derived/monthly_corpus_summary.csv')
    if len(monthly)!=10 or sum(int(x['news_items']) for x in monthly)!=105:raise AssertionError('Corpus-count mismatch')
    return dict(participants=len(ids),direct_distances=direct.size,centroid_distances=75,
                printed_table4_matches=True,printed_table5_matches=True,workbook_wilcoxon_matches=True,
                corpus_news_items=105,significant_transitions=[r['transition'] for r in results if r['significant_after_holm']])

def figures(direct,out):
    out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.size':10,'font.family':'DejaVu Sans','pdf.fonttype':42,'ps.fonttype':42})
    fig,ax=plt.subplots(figsize=(7.3,4.6));violin=ax.violinplot(direct,showextrema=False,widths=.68)
    for body in violin['bodies']:body.set_facecolor('#cddfe6');body.set_edgecolor('#24566c');body.set_alpha(1)
    for i in range(4):
        ax.scatter(i+1+np.linspace(-.14,.14,15),direct[:,i],s=20,color='#24566c',edgecolors='white',linewidths=.4,zorder=3)
        ax.plot([i+.78,i+1.22],[np.median(direct[:,i])]*2,color='#182c38',lw=2,zorder=4)
    ax.set_xticks(range(1,5),['P1 → P2','P2 → P3','P3 → P4','P4 → P5'])
    ax.set_xlabel('Consecutive prompt transition');ax.set_ylabel('Cosine distance (dimensionless)')
    ax.set_ylim(0,1.03);ax.set_yticks(np.arange(0,1.01,.2));ax.grid(axis='y',color='#dce2e5',lw=.7);ax.set_axisbelow(True)
    for spine in ['top','right']:ax.spines[spine].set_visible(False)
    fig.tight_layout(pad=1.5)
    for extension in ['pdf','png','eps']:fig.savefig(out/f'figure13.{extension}',dpi=350,bbox_inches='tight')
    plt.close(fig)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=ROOT/'results')
    parser.add_argument('--verify',action='store_true',help='Check archived reference values and input completeness')
    args=parser.parse_args();ids,direct,centroid=validate_and_load();results=analyze(centroid)
    out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
    fields=['transition','mean','median','sample_sd','minimum','maximum','mean_similarity']
    write_csv(out/'table5_full_precision.csv',fields,describe(direct))
    write_csv(out/'table5_from_printed_table4.csv',fields,describe(np.round(direct,4)))
    write_csv(out/'table6_centroid_tests.csv',list(results[0]),results)
    rounded=np.round(direct,4);means=rounded.mean(axis=1);q1,q2,q3=np.quantile(means,[.25,.5,.75])
    rows=[dict(participant_id=pid,**{f'p{i+1}_p{i+2}':rounded[j,i] for i in range(4)},mean=means[j],
               variance_population=float(rounded[j].var(ddof=0)),quartile=f'Q{1+int(means[j]>q1)+int(means[j]>q2)+int(means[j]>q3)}') for j,pid in enumerate(ids)]
    write_csv(out/'table4_participant_summaries.csv',list(rows[0]),rows)
    figures(direct,out/'figures')
    summary=verify(ids,direct,results) if args.verify else {'verification_requested':False}
    (out/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
