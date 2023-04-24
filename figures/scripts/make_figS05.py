import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from os.path import dirname
from pandas import read_csv, concat
sns.set_theme(style='ticks', context='notebook', font_scale=1.2, rc={'font.family': 'Arial'})
ROOT_DIR = dirname(dirname(dirname(os.path.realpath(__file__))))
np.random.seed(47404)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define plot parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define axis styles.
labelcolor = '#505050'
tickcolor = '#606060'
axiscolor = '#d3d3d3'

## Define row 1 styling.
r1_titles = ['Mood (Slider)', 'Anxiety (GAD-7)', 'Depression (DASS)']
r1_xticks = [-0.3, -0.1, 0.1, 0.3, 0.7, 0.9, 1.1]
r1_xticklabels = [0, 3, 14, 28, 0, 3, 14]
r1_ylims = [(0,1), (0,1), (0,1)]
r1_yticks = [np.linspace(0,1,3), np.linspace(0,1,3), np.linspace(0,1,3)]
r1_palette = np.repeat(['#000000', '#f5970a'], 4)
r1_comparisons = {
    'mood': [],
    'gad7': [(-0.3,0.3,0.36,'**'), (-0.1,0.3,0.42,'**'), (0.7,1.1,0.36,'**')],
    'dass': []
}

## Define row 2 styling.
r2_titles = ['Mood (Slider)', 'Anxiety (GAD-7)', 'Depression (DASS)']
r2_xticks = np.concatenate([np.linspace(-0.25,0.25,3) + i for i in range(2)])
r2_xticklabels = np.tile(['0{0}3'.format(u'\u2013'), '0{0}14'.format(u'\u2013'), '3{0}14'.format(u'\u2013')], 2)
r2_palette = np.repeat(['#000000', '#f5970a'], 3)
r2_markers = np.tile(['o', 'o', 'o'], 2)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Initialize canvas.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Initialize canvas.
fig = plt.figure(figsize=(9,6))

## Initialize gridspec.
gs = fig.add_gridspec(2, 3, left=0.06, right=0.98, top=0.88, bottom=0.07,
                      hspace=0.70, wspace=0.20)

## Define convenience functions.
def plot_comparison(x1, x2, y, color=labelcolor, lw=0.8, tickwidth=1e-2, annot=None, ax=None):
    ax.plot([x1,x2], [y,y], color=color, lw=lw)
    ax.plot([x1,x1], [y-tickwidth, y], color=color, lw=lw)
    ax.plot([x2,x2], [y-tickwidth, y], color=color, lw=lw)
    ax.text(x1 + (x2-x1)/2., y, annot,  ha='center', va='center', color=labelcolor, fontsize=10)
    return ax

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Load and prepare data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Load and prepare self-report data (experiment 1).
s1 = concat([read_csv(os.path.join(ROOT_DIR, 'study01', 'data', s, 'surveys.csv')) for s in ['s1','s2','s3','s4']])
reject = read_csv(os.path.join(ROOT_DIR, 'study01', 'data', 's1', 'reject.csv'))
s1 = s1[s1.subject.isin(reject.query('reject==0').subject)].reset_index(drop=True)
s1 = s1.rename(columns={'slider':'mood'})
s1['gad7'] = s1.filter(regex='gad7-q0[1-7]').sum(axis=1) / 21.
s1['dass'] = np.nan

## Load and prepare self-report data (experiment 2).
s2 = concat([read_csv(os.path.join(ROOT_DIR, 'study02', 'data', s, 'surveys.csv')) for s in ['s1','s2','s3']])
reject = read_csv(os.path.join(ROOT_DIR, 'study02', 'data', 's1', 'reject.csv'))
s2 = s2[s2.subject.isin(reject.query('reject==0').subject)].reset_index(drop=True)
s2['gad7'] = s2.filter(regex='gad7_q0[1-7]').sum(axis=1) / 21.
s2['dass'] = s2.filter(regex='dass_q0[1-7]').sum(axis=1) / 21.

## Merge DataFrames.
cols = ['subject','session','mood','gad7','dass']
scores = concat([s1[cols].assign(study=1), s2[cols].assign(study=2)])

## Compute observed statistics.
summary = scores.groupby(['study','session'])[['mood','gad7','dass']].mean()
summary = summary.reset_index().melt(id_vars=['study','session'], var_name='scale', value_name='Mean')

## Compute bootstrap confidence interval.
f = lambda x: np.mean(np.random.choice(x, x.size, replace=True))
null = np.zeros((1000, 3, len(summary) // 3))
for n in range(len(null)):
    for m, col in enumerate(['mood','gad7','dass']):
        null[n,m] = scores.groupby(['study','session'])[col].apply(f).values
        
summary['2.5%'] = np.percentile(null, 2.5, 0).flatten()
summary['97.5%'] = np.percentile(null, 97.5, 0).flatten()
summary = summary.set_index('scale')

## Compute test-retest reliability.
f = lambda x: x.corr().values[np.tril_indices(3, k=-1)]
reliability = np.stack([
    np.concatenate(scores.pivot_table(col,['study','subject'],'session',dropna=False).groupby('study').apply(f).values)
    for col in ['mood','gad7','dass']
])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Row 1: Group-level parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
## Iteratively plot.
for i, (scale, yticks, ylim, title) in enumerate(zip(['mood','gad7','dass'], r1_yticks, r1_ylims, r1_titles)):
    
    ## Initialize axis.
    ax = plt.subplot(gs[0,i])
    
    ## Iteratively plot.
    for j, (y, lb, ub, x, color) in enumerate(zip(summary.loc[scale,'Mean'],
                                                  summary.loc[scale,'2.5%'],
                                                  summary.loc[scale,'97.5%'],
                                                  r1_xticks, r1_palette)):
        ax.errorbar(x=x, y=y, yerr=np.vstack([y-lb,ub-y]), fmt='o', color=color, elinewidth=1.5)
        
    ## Add pairwise comparisons.
    tickwidth = float(np.diff(ylim)) * 2e-2
    for x1, x2, y, annot in r1_comparisons[scale]:
        plot_comparison(x1, x2, y, tickwidth=tickwidth, annot=annot, ax=ax)
        
    ## Adjust x-axis.
    ax.set(xlim=(-0.35, 1.15), xticks=r1_xticks, xticklabels=[])
    ax.set_xticklabels(r1_xticklabels, color=tickcolor, fontsize=9)
    ax.set_xlabel('Day', color=tickcolor, fontsize=9)
    
    ## Adjust y-axis.
    ax.set(ylim=ylim, yticks=yticks, yticklabels=[])
    if not i:
        ax.spines['left'].set(linewidth=1, color=axiscolor, position=('axes', -0.0))
        ax.set_yticklabels([0, 50, 100], color=tickcolor, fontsize=9)
        ax.set_ylabel('Score (% of max)', color=labelcolor, fontsize=10)
    
    ## Adjust title.
    ax.set_title(title, loc='left', color=tickcolor, fontsize=11, pad=4)
    
    ## Adjust legend.
    if not i:
        ax.errorbar([], [], fmt='o', color='#000000', label='Experiment 1')
        ax.errorbar([], [], fmt='o', color='#f5970a', label='Experiment 2')
        ax.legend(loc=2, bbox_to_anchor=(0, 1.20), ncol=2, frameon=False, labelcolor=labelcolor, fontsize=10,
                  borderpad=0, borderaxespad=0, handletextpad=0.5, handlelength=1.6, columnspacing=1.2)
    
    ## Modify ax spines.
    ax.spines['left'].set(linewidth=1, color=axiscolor)
    ax.tick_params(bottom=False, left=True, color=axiscolor, length=4, width=1)
    sns.despine(ax=ax, left=False, right=True, top=True, bottom=True)
    
    ## Add annotation.
    if not i: ax.annotate('A. Systematic changes in self-report measures', (0,0), (-0.11,1.24), 
                          'axes fraction', ha='left', va='bottom', color=labelcolor, fontsize=16)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Row 2: Test-retest reliability.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Iteratively plot.
for i, title in enumerate(r2_titles):
    
    ## Initialize axis.
    ax = plt.subplot(gs[1,i])

    ## Iteratively plot.
    for j, (y, x, fmt, color) in enumerate(zip(reliability[i], r2_xticks, r2_markers, r2_palette)):        
        ax.errorbar(x=x, y=y, fmt=fmt, color=color, elinewidth=1.5)
        
    ## Plot averages.
    ax.hlines(reliability[i,:3].mean(), -0.25, 0.25, color='0.2', lw=1.2,
              linestyle=(0, (1, 1)), zorder=-1)
    ax.hlines(reliability[i,3:].mean(),  0.75, 1.25, color='0.2', lw=1.2,
              linestyle=(0, (1, 1)), zorder=-1)
    
    ## Add zero-line.
    ax.axhline(0, linewidth=1, color=axiscolor, linestyle='--')
    
    ## Add fill.
    x1, x2 = [-0.31, 1.31]
    ax.fill_betweenx([0.7,1.05], x1, x2, color=axiscolor, edgecolor='none', alpha=0.18)
    
    ## Adjust x-axis.
    ax.set(xlim=(x1, x2), xticks=r2_xticks, xticklabels=[])
    ax.set_xticklabels(r2_xticklabels, color=tickcolor, fontsize=9)
    ax.set_xlabel('Days', color=tickcolor, fontsize=9)

    ## Adjust y-axis.
    ax.set(ylim=(-0.08,1.05), yticks=np.linspace(0.0,1.0,6), yticklabels=[])
    if not i:
        ax.spines['left'].set(linewidth=1, color=axiscolor, position=('axes', -0.0))
        ax.set_yticklabels(ax.get_yticks().round(1), color=tickcolor, fontsize=9)
        ax.set_ylabel('Reliability', color=tickcolor, fontsize=9)
    
    ## Adjust title.
    ax.set_title(title, loc='left', color=tickcolor, fontsize=11, pad=4)

    ## Adjust legend.
    if not i:
        ax.errorbar([], [], fmt='o', color='#000000', label='Experiment 1')
        ax.errorbar([], [], fmt='o', color='#f5970a', label='Experiment 2')
        ax.errorbar([], [], color='0.2', label='Average', linestyle=(0, (1, 1)))
        ax.legend(loc=2, bbox_to_anchor=(0, 1.21), ncol=3, frameon=False, labelcolor=labelcolor, fontsize=10,
                  borderpad=0, borderaxespad=0, handletextpad=0.5, handlelength=1.6, columnspacing=1.2)
        
    ## Modify ax spines.
    ax.yaxis.set_tick_params(pad=1)
    ax.spines['left'].set(linewidth=1, color=axiscolor)
    if not i: 
        sns.despine(ax=ax, left=False, right=True, top=True, bottom=True)
        ax.tick_params(bottom=False, left=True, color=axiscolor, length=4, width=1)
    else: 
        sns.despine(ax=ax, left=True, right=True, top=True, bottom=True)
        ax.tick_params(bottom=False, left=False, color=axiscolor, length=4, width=1)
            
    ## Add annotation.
    if not i: ax.annotate('B. Test-retest reliability of self-report measures', (0,0), (-0.11,1.24), 
                          'axes fraction', ha='left', va='bottom', color=labelcolor, fontsize=16)
    
## Save figure.
plt.savefig(os.path.join(ROOT_DIR, 'figures', 'figS05.svg'), dpi=100, transparent=True)