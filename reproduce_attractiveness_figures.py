#!/usr/bin/env python3
"""Recompute published-summary checks and regenerate five original charts.

This is an aggregate-summary reconstruction, not a rerun of source analyses.
Python >=3.10. Charts use numpy and matplotlib. No web requests.
"""
import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def data(name):
    with (ROOT / name).open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def check_close(actual, expected, tol=1e-7):
    if abs(actual - expected) > tol:
        raise AssertionError(f"Expected {expected}, got {actual}")


def report():
    meta = data('meta_analysis_reported.csv')
    assert len(meta) == 1
    m = meta[0]
    assert int(m['studies']) == 52 and int(m['effect_estimates']) == 59
    check_close(float(m['pooled_standardized_difference']), .36)
    check_close(float(m['ci_95_low']), .29)
    check_close(float(m['ci_95_high']), .42)
    assert 89 < float(m['i_squared_percent']) < 91

    woods = data('wood_brumbaugh_2009_ratings.csv')
    assert len(woods) == 4
    w = {(r['face_sex'], r['observer_group']): float(r['mean_pomp']) for r in woods}
    wd = w['female', 'Heterosexual men'] - w['female', 'Lesbian women']
    md = w['male', 'Gay men'] - w['male', 'Heterosexual women']
    check_close(wd, 9.8)
    check_close(md, 13.1)

    couples = sorted(data('meltzer_2014_couples.csv'), key=lambda r:int(r['study']))
    assert len(couples) == 4
    assert sum(int(r['couples']) for r in couples) == 454
    couples_diffs = [float(r['husband_mean']) - float(r['wife_mean']) for r in couples]
    for a,b in zip(couples_diffs, [.14,-.15,.08,-.07]): check_close(a,b)

    children = sorted(data('jokela_2009_women.csv'),key=lambda r:int(r['ordinal']))
    assert [r['quartile'] for r in children] == ['Lowest','Second','Third','Highest']
    x = [float(r['adjusted_mean_children']) for r in children]
    for a,b in zip(x,[2.67,2.59,3.05,2.80]): check_close(a,b)
    baseline = (x[0] + x[1]) / 2.0 # illustrative equal-weight baseline, NOT source model contrast
    third_pct = 100 * (x[2] / baseline - 1)
    top_pct = 100 * (x[3] / baseline - 1)
    assert 15.5 < third_pct < 16.5 and 6 < top_pct < 7

    med = {r['observer_sex']: r for r in data('facial_shape_mediation_reported.csv')}
    def attenuation(sex):
        r=med[sex]
        total=float(r['total_sex_difference'])
        direct=float(r['after_shape_adjustment'])
        return total-direct,100*(total-direct)/total
    fd,fp=attenuation('female'); mdif,mp=attenuation('male')
    check_close(fd,.112); check_close(mdif,.112)

    extra = {(r['source_id'],r['measure']):float(r['value']) for r in data('other_reported_checks.csv')}
    assert extra['mcnulty_2008','husband_attractiveness_mean'] > extra['mcnulty_2008','wife_attractiveness_mean']
    check_close(extra['jokela_2009','female_attractiveness_offspring_sex_trend_p'],.89)
    check_close(extra['jokela_2009','combined_offspring_sex_ratio_p'],.28)
    ab=extra['wassiliwizky_2026','reported_shape_path_a']*extra['wassiliwizky_2026','reported_shape_path_b']

    lines=[
     'Physical attractiveness distributions — published-summary reconstruction',
     '=====================================================================',
     'IMPORTANT: Source-level summary statistics, not reanalysis of original records.',
     '',
     '2026 meta-analysis (directly transcribed):',
     f"  {m['studies']} studies; {m['effect_estimates']} effect estimates",
     f"  Mean standardized difference = {float(m['pooled_standardized_difference']):.2f}",
     f"  Published 95% CI = [{float(m['ci_95_low']):.2f}, {float(m['ci_95_high']):.2f}]",
     f"  Published I squared = {float(m['i_squared_percent']):.2f}%",
     '  These values are not independently reestimated here.',
     '',
     'Wood & Brumbaugh (2009), Table 4:',
     f'  Female-face photo set: heterosexual men minus lesbian women = {wd:.1f} POMP points',
     f'  Male-face photo set: gay men minus heterosexual women = {md:.1f} POMP points',
     '  Confounds sex of rater and sexual orientation; not a causal rater-sex effect.',
     '',
     'Meltzer et al. (2014), four newlywed samples:',
     '  Sample sizes (couples): '+ ', '.join(str(r['couples']) for r in couples),
     '  Husband minus wife means: '+', '.join(f'{v:+.2f}' for v in couples_diffs),
     '  The reported within-sample sex comparisons were nonsignificant.',
     '  Note: Study 1 includes the McNulty et al. (2008) cohort.',
     '',
     'Jokela (2009), Table 3, Model A:',
     '  Adjusted mean biological children by female attractiveness quartile: '+', '.join(f'{v:.2f}' for v in x),
     f'  Equal-weight mean of bottom two quartiles = {baseline:.3f}',
     f'  Third vs. this mean = {third_pct:+.1f}% (rounded; published prose ~16%)',
     f'  Top vs. this mean = {top_pct:+.1f}% (rounded; published prose ~6%)',
     '  These percentages compare CHILD COUNTS, not probability of any birth.',
     '  Equal weighting is illustrative: original regression reference may differ.',
     '  Female offspring-sex trend p = 0.89 (transcribed; not recalculated).',
     '',
     '2026 facial-shape statistical adjustment:',
     f'  Female raters: absolute change = {fd:.3f}, percent = {fp:.2f}% (reported 33.25%)',
     f'  Male raters:   absolute change = {mdif:.3f}, percent = {mp:.2f}% (reported 42.98%)',
     f'  Product of separately reported a*b paths = {ab:.3f}',
     '  Published pathways cannot be reconciled from the printed coefficients alone.',
     '  Do not infer a causal mediation effect from these arithmetic checks.',
     '',
     'Conceptual chart: two hypothetical Gaussian densities, NOT observed ratings.',
     'All validation assertions passed.',
    ]
    return '\n'.join(lines)+'\n'


def plot_figures():
    # Import optional plotting dependencies only when needed.
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    NAVY='#24364A'; TEAL='#578B91'; BLUE='#9CAFB9'
    GRID='#E4E8EC'; INK='#283748'; MUTED='#607381'
    plt.rcParams.update({
      'font.family':'DejaVu Sans','font.size':11,'axes.titlesize':15,
      'axes.labelsize':11,'axes.edgecolor':GRID,'axes.labelcolor':INK,
      'text.color':INK,'xtick.color':INK,'ytick.color':INK,
      'axes.spines.top':False,'axes.spines.right':False,
      'savefig.facecolor':'white',
    })
    def save(fig,name):
        fig.savefig(ROOT/name,dpi=180,bbox_inches='tight',pad_inches=.28,facecolor='white')
        plt.close(fig)

    # Figure 2: same face sets, but observer orientation/sex both differ.
    rows=data('wood_brumbaugh_2009_ratings.csv')
    vals={(r['face_sex'],r['observer_sex']):float(r['mean_pomp']) for r in rows}
    fig,ax=plt.subplots(figsize=(10,5.2))
    xx=np.array([0,1],dtype=float); w=.34
    male=[vals['female','male'],vals['male','male']]
    female=[vals['female','female'],vals['male','female']]
    b1=ax.bar(xx-.19,male,width=w,color=NAVY,label='Male observers')
    b2=ax.bar(xx+.19,female,width=w,color=TEAL,label='Female observers')
    for bars in (b1,b2):
        for rect in bars:
            ax.text(rect.get_x()+rect.get_width()/2,rect.get_height()+1,
                    f'{rect.get_height():.1f}',ha='center',va='bottom',fontsize=11,fontweight='bold')
    ax.set_xticks(xx,['Female faces\nHeterosexual men / lesbian women',
                      'Male faces\nGay men / heterosexual women'])
    ax.set_ylim(0,53);ax.set_yticks([0,10,20,30,40,50]);ax.set_xlim(-.58,1.58)
    ax.set_ylabel('Mean attractiveness (0–100 POMP rating)')
    ax.set_title('The same photographs can receive different average ratings',loc='left',fontweight='bold',pad=16)
    ax.legend(loc='upper right',frameon=False,ncol=2)
    ax.grid(axis='y',color=GRID);ax.set_axisbelow(True)
    ax.tick_params(axis='x',pad=10)
    fig.subplots_adjust(bottom=.23)
    save(fig,'figure_02_wood_raters.png')

    # Figure 3: pooled point estimate, no invented distribution or forest plot.
    m=data('meta_analysis_reported.csv')[0]
    y=float(m['pooled_standardized_difference']);lo=float(m['ci_95_low']);hi=float(m['ci_95_high'])
    fig,ax=plt.subplots(figsize=(10,3.8))
    ax.axvline(0,color=INK,linewidth=1.25,alpha=.7)
    ax.plot([lo,hi],[0,0],lw=5,color=TEAL,solid_capstyle='round')
    ax.plot([lo,lo],[-.10,.10],lw=1.5,color=NAVY)
    ax.plot([hi,hi],[-.10,.10],lw=1.5,color=NAVY)
    ax.scatter([y],[0],color=NAVY,marker='D',s=155,zorder=3)
    ax.text(y,.25,f'{y:.2f} (95% CI {lo:.2f}–{hi:.2f})',ha='center',fontweight='bold',fontsize=12)
    ax.text(.61,-.53,'52 studies · 59 estimates · I² ≈ 90%',ha='right',color=MUTED,fontsize=10)
    ax.set_ylim(-.7,.7);ax.set_xlim(-.13,.64);ax.set_yticks([])
    ax.set_xticks([0,.1,.2,.3,.4,.5,.6])
    ax.set_xlabel('Difference in mean attractiveness ratings (female − male faces, standardized units)',labelpad=13)
    ax.set_title('Published 2026 meta-analysis: higher ratings for female faces',loc='left',fontweight='bold',pad=17)
    ax.grid(axis='x',color=GRID);ax.set_axisbelow(True)
    fig.subplots_adjust(bottom=.26)
    save(fig,'figure_03_meta_analysis.png')

    # Figure 4: CI bounds reported for adjusted model-based child-count means.
    rows=sorted(data('jokela_2009_women.csv'),key=lambda r:int(r['ordinal']))
    labels=[r['quartile'] for r in rows]
    vals=np.array([float(r['adjusted_mean_children']) for r in rows]);x=np.arange(4)
    low=np.array([float(r['ci_95_low']) for r in rows]);high=np.array([float(r['ci_95_high']) for r in rows])
    fig,ax=plt.subplots(figsize=(10,5))
    ax.bar(x,vals,width=.57,color=[BLUE,BLUE,TEAL,NAVY])
    ax.errorbar(x,vals,yerr=[vals-low,high-vals],fmt='none',ecolor=INK,capsize=5,lw=1.5)
    for i,v in enumerate(vals):
        ax.text(i,v+.22,f'{v:.2f}',ha='center',fontweight='bold')
    ax.set_xticks(x,labels);ax.set_xlim(-.6,3.6);ax.set_ylim(0,3.7)
    ax.set_title('Jokela: adjusted child counts do not rise steadily',loc='left',fontweight='bold',pad=18)
    ax.set_xlabel('Attractiveness quartile (women)',labelpad=13)
    ax.set_ylabel('Adjusted mean number of biological children')
    ax.grid(axis='y',color=GRID);ax.set_axisbelow(True)
    fig.subplots_adjust(bottom=.20)
    save(fig,'figure_04_jokela_fertility.png')

    # Figure 5: group sample means only; no inferred confidence intervals.
    rows=sorted(data('meltzer_2014_couples.csv'),key=lambda r:int(r['study']))
    x=np.arange(4);w=.34
    husbands=[float(r['husband_mean']) for r in rows];wives=[float(r['wife_mean']) for r in rows]
    fig,ax=plt.subplots(figsize=(10,4.9))
    bars1=ax.bar(x-.18,husbands,width=w,color=NAVY,label='Husbands')
    bars2=ax.bar(x+.18,wives,width=w,color=TEAL,label='Wives')
    for bars in (bars1,bars2):
        for rect in bars:
            ax.text(rect.get_x()+rect.get_width()/2,rect.get_height()+.1,
                f'{rect.get_height():.2f}',ha='center',fontsize=10)
    ax.set_xticks(x,[f'Study {r["study"]}\n(n={r["couples"]} couples)' for r in rows])
    ax.set_ylim(0,6.3);ax.set_ylabel('Mean observer-rated facial attractiveness')
    ax.set_title('Four newlywed samples: no significant mean sex difference',loc='left',fontweight='bold',pad=18)
    ax.legend(loc='upper right',frameon=False,ncol=2)
    ax.grid(axis='y',color=GRID);ax.set_axisbelow(True)
    fig.subplots_adjust(bottom=.19)
    save(fig,'figure_05_couples.png')

    # Figure 6: entirely illustrative Gaussian distributions.
    x=np.linspace(-3.5,4.5,600)
    def norm(mu):return np.exp(-.5*(x-mu)**2)/np.sqrt(2*np.pi)
    fig,ax=plt.subplots(figsize=(10,4))
    for mu,c,lab in [(0,NAVY,'Illustrative group A'),(.85,TEAL,'Illustrative group B')]:
        y=norm(mu);ax.plot(x,y,color=c,lw=3,label=lab)
        ax.fill_between(x,y,alpha=.09,color=c)
    ax.set_xlim(-3.5,4.5);ax.set_ylim(0,.46);ax.set_xticks([]);ax.set_yticks([])
    ax.set_title('Two normal distributions can have different means',loc='left',fontweight='bold',pad=17)
    ax.set_xlabel('Hypothetical shared measurement scale — not attractiveness data',labelpad=12)
    ax.legend(frameon=False,loc='upper right')
    save(fig,'figure_06_normal_illustration.png')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only',action='store_true',help='Validate inputs and report calculations; do not regenerate figures')
    args=parser.parse_args()
    results=report()
    if not args.check_only:
        plot_figures()
        (ROOT/'reconstruction_results.txt').write_text(results,encoding='utf-8')
    print(results,end='')

if __name__=='__main__':main()
