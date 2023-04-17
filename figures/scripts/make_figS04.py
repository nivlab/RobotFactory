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

## Define variable ordering.
sessions = [1,2,3,4]

## Define axis styles.
labelcolor = '#737373'
tickcolor = '#8a8a8a'
axiscolor = '#d3d3d3'

## Define row 1 styling.
r1_titles = [r'Outcome sensitivity ($\beta$)', r'Go bias ($\tau$)', r'Learning rates ($\eta$)']
r1_xticks = np.concatenate([np.linspace(-0.25,0.25,3) + i for i in range(2)])
r1_xticklabels = np.tile(['0', '3', '14'], 2)
r1_palette = np.repeat(['#234f81', '#812623'], 3)
r1_markers = np.tile(['o', 'o', 'o'], 2)

## Define row 2 styling.
r2_titles = [r'Outcome sensitivity ($\beta$)', r'Go bias ($\tau$)', r'Learning rates ($\eta$)']
r2_xticks = np.concatenate([np.linspace(-0.25,0.25,3) + i for i in range(2)])
r2_xticklabels = np.tile([0, 3, 14], 2)
r2_palette = np.repeat(['#234f81', '#812623'], 3)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Initialize canvas.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Initialize canvas.
fig = plt.figure(figsize=(9,6))

## Initialize gridspec.
gs = fig.add_gridspec(2, 3, left=0.06, right=0.98, top=0.88, bottom=0.07,
                      hspace=0.70, wspace=0.20)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Load and prepare data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Iteratively load Stan summaries.
summary = concat([
    read_csv(
        os.path.join(ROOT_DIR, 'study02', 'stan_results', s, f'pgng_m7_summary.tsv'), 
        sep='\t', index_col=0
    ).assign(Session=s)
    for s in ['s1', 's2', 's3']
])

## Restrict to group-level parameters.
summary = summary.T.filter(regex='_mu').T.reset_index().set_index(['index','Session']).sort_index()

## Load reliability.
rel1 = read_csv(os.path.join(ROOT_DIR, 'study01', 'stan_results', 'pgng_m7_reliability.csv'))
rel1 = rel1.query('Group > 0').set_index(['Type','Param']).sort_index()
rel2 = read_csv(os.path.join(ROOT_DIR, 'study02', 'stan_results', 'pgng_m7_reliability.csv'))
rel2 = rel2.query('Group > 0').set_index(['Type','Param']).sort_index()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Row 1: Experiment 1.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Iteratively plot.
for i, (p1, p2, title) in enumerate(zip(['b1','b3','a1'], ['b2','b4','a2'], r1_titles)):
    
    ## Initialize axis.
    ax = plt.subplot(gs[0,i])

    ## Iteratively plot.
    for y1, y2, x, color in zip(rel1.loc[('sh',[p1,p2]),'Mean'], 
                                rel2.loc[('sh',[p1,p2]),'Mean'], 
                                r1_xticks, r1_palette):        
        ax.scatter(x=x, y=y1, marker='o', color=color, edgecolor='none')
    
    ## Plot averages.
    ax.hlines(rel1.loc[('sh',p1),'Mean'].mean(), -0.25, 0.25, color='0.2', lw=1.5,
              linestyle=(0, (1, 1)), zorder=-1)
    ax.hlines(rel1.loc[('sh',p2),'Mean'].mean(),  0.75, 1.25, color='0.2', lw=1.5,
              linestyle=(0, (1, 1)), zorder=-1)
    
    ## Add zero-line.
    ax.axhline(0, linewidth=1, color=axiscolor, linestyle='--')
    
    ## Add fill.
    x1, x2 = [-0.31, 1.31]
    ax.fill_betweenx([0.7,1.05], x1, x2, color=axiscolor, edgecolor='none', alpha=0.18)
    
    ## Adjust x-axis.
    ax.set(xlim=(x1, x2), xticks=r1_xticks, xticklabels=[])
    ax.set_xticklabels(r1_xticklabels, color=tickcolor, fontsize=9)
    ax.set_xlabel('Day', color=tickcolor, fontsize=9)

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
        ax.errorbar([], [], fmt='o', color='#234f81', label='Rewarding')
        ax.errorbar([], [], fmt='o', color='#812623', label='Punishing')
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
    if not i: ax.annotate('A. Split-half reliability of model parameters (Experiment 1)', (0,0), (-0.11,1.24), 
                          'axes fraction', ha='left', va='bottom', color=labelcolor, fontsize=16)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Row 2: Experiment 2.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Iteratively plot.
for i, (p1, p2, title) in enumerate(zip(['b1','b3','a1'], ['b2','b4','a2'], r2_titles)):
    
    ## Initialize axis.
    ax = plt.subplot(gs[1,i])

    ## Iteratively plot.
    for y1, y2, x, color in zip(rel1.loc[('sh',[p1,p2]),'Mean'], 
                                rel2.loc[('sh',[p1,p2]),'Mean'], 
                                r2_xticks, r2_palette):        
        ax.scatter(x=x, y=y1, marker='o', color='none', edgecolor=color)
        ax.scatter(x=x, y=y2, marker='o', color=color, edgecolor='none')
        ax.vlines(x, y1, y2, color='0.9', lw=2, zorder=-1)
    
    ## Plot averages.
    ax.hlines(rel2.loc[('sh',p1),'Mean'].mean(), -0.25, 0.25, color='0.2', lw=1.5,
              linestyle=(0, (1, 1)), zorder=-1)
    ax.hlines(rel2.loc[('sh',p2),'Mean'].mean(),  0.75, 1.25, color='0.2', lw=1.5,
              linestyle=(0, (1, 1)), zorder=-1)
    
    ## Add zero-line.
    ax.axhline(0, linewidth=1, color=axiscolor, linestyle='--')
    
    ## Add fill.
    x1, x2 = [-0.31, 1.31]
    ax.fill_betweenx([0.7,1.05], x1, x2, color=axiscolor, edgecolor='none', alpha=0.18)
    
    ## Adjust x-axis.
    ax.set(xlim=(x1, x2), xticks=r2_xticks, xticklabels=[])
    ax.set_xticklabels(r2_xticklabels, color=tickcolor, fontsize=9)
    ax.set_xlabel('Day', color=tickcolor, fontsize=9)

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
        ax.errorbar([], [], fmt='o', color='#234f81', label='Rewarding')
        ax.errorbar([], [], fmt='o', color='#812623', label='Punishment')
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
    if not i: ax.annotate('B. Split-half reliability of model parameters (Experiment 2)', (0,0), (-0.11,1.24), 
                          'axes fraction', ha='left', va='bottom', color=labelcolor, fontsize=16)
    
## Save figure.
plt.savefig(os.path.join(ROOT_DIR, 'figures', 'figS04.svg'), dpi=100)