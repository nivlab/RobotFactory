import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from os.path import dirname
from pandas import read_csv, concat
from scipy.stats import spearmanr
sns.set_theme(style='ticks', context='notebook', font_scale=1.2, rc={'font.family': 'Arial'})
ROOT_DIR = dirname(dirname(dirname(os.path.realpath(__file__))))
np.random.seed(47404)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define plot parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define I/O parameters.
stan_model = 'pgng_m7'

## Define variable ordering.
sessions = [1,2,3]
robots = ['gw','ngw','gal','ngal']

## Define palettes.
palette = ['#234f81', '#8e9cb8', '#bf8a82', '#812623']

## Define labels.
labels = ['Day 0', 'Day 3', 'Day 14']

## Define axis styles.
labelcolor = '#505050'
tickcolor = '#606060'
axiscolor = '#d3d3d3'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Initialize canvas.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Initialize canvas.
fig = plt.figure(figsize=(9,6))

## Initialize gridspec.
gs = fig.add_gridspec(2, 4, left=0.07, right=0.98, top=0.88, bottom=0.07, 
                      hspace=0.60, wspace=0.16)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Load and prepare data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Load data.
data = concat([read_csv(os.path.join(ROOT_DIR, 'study02', 'stan_results', session, f'{stan_model}_ppc.csv'))
               for session in ['s1','s2','s3']])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Panels 1a-d: Learning curves.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Main loop.
for i, session in enumerate(sessions):
    
    ## Initialize axis.
    ax = plt.subplot(gs[0,i])
    
    ## Plot observed learning curves.
    sns.lineplot(x='exposure', y='choice', hue='robot', data=data.query(f'session == {session}'), 
                 hue_order=robots, palette=palette, legend=False, errorbar=None, lw=3, ax=ax)
    
    ## Plot predicted learning curves.
    sns.lineplot(x='exposure', y='Y_hat', hue='robot', data=data.query(f'session == {session}'), 
                 hue_order=robots, palette=['0.1']*4, legend=False, errorbar=None, lw=2,  ax=ax,
                 linestyle=(0, (1, 1)))
    
    ## Add midway line.
    ax.axhline(0.5, color='k', alpha=0.05, zorder=-1)

    ## Adjust x-axis.
    ax.set(xlim=(0.7,12), xticks=[0.7,6,12])
    ax.set_xticklabels([1,6,12], color=tickcolor, fontsize=9)
    ax.set_xlabel('Trial', color=tickcolor, fontsize=9)
    
    ## Adjust y-axis.
    ax.set(ylim=(0,1), yticks=[], yticklabels=[], ylabel='')
    if not i:
        ax.spines['left'].set(linewidth=1, color=axiscolor, position=('axes', -0.04))
        ax.set_yticks(np.linspace(0,1,6))
        ax.set_yticklabels(ax.get_yticks().round(1), color=tickcolor, fontsize=9)
        ax.set_ylabel('p(Go)', color=tickcolor, fontsize=11)
        
    ## Adjust title.
    ax.set_title(labels[i], loc='left', color=tickcolor, fontsize=11)
        
    ## Adjust legend.
    if not i: 
        for color, label in zip(palette, robots): ax.plot([], [], color=color, label=label.upper(), lw=4)
        ax.legend(loc=2, bbox_to_anchor=(0, 1.21), ncol=4, frameon=False, labelcolor=labelcolor, fontsize=10,
                  borderpad=0, borderaxespad=0, handletextpad=0.5, handlelength=1.6, columnspacing=1.2)
        
    ## Modify ax spines.
    ax.yaxis.set_tick_params(pad=1)
    ax.spines['bottom'].set(linewidth=1, color=axiscolor)
    ax.tick_params(bottom=True, left=True, color=axiscolor, length=4, width=1)
    if not i: sns.despine(ax=ax, left=False, right=True, top=True, bottom=False)
    else: sns.despine(ax=ax, left=True, right=True, top=True, bottom=False)
    
    ## Add annotation.
    if not i: ax.annotate('A. Observed & model-predicted learning curves', (0,0), (-0.16,1.24), 'axes fraction', 
                          ha='left', va='bottom', color=labelcolor, fontsize=16)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Panels 2a-d: Individual differences.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define convenience functions.
RMSE = lambda x: np.sqrt(np.mean(np.square(x)))

## Main loop.
for i, session in enumerate(sessions):
    
    ## Initialize axis.
    ax = plt.subplot(gs[1,i])
    
    ## Compute average performance.
    agg = {'choice':'mean', 'Y_hat':'mean'}
    gb = data.query(f'session == {session}').groupby(['subject','robot']).agg(agg).reset_index()
    
    ## Compute correlation.
    rmse = RMSE(gb.choice - gb.Y_hat)
    corr = gb[['choice','Y_hat']].corr(method='spearman').values[0,1]
    
    ## Plot performance.
    sns.scatterplot(x='choice', y='Y_hat', hue='robot', data=gb, hue_order=robots, 
                    palette=palette, legend=False, ax=ax)
    
    ## Add diagonal line.
    ax.plot([-1,2], [-1,2], color='k', zorder=-1)
    
    ## Add annotation.
    annot = 'RMSE = %0.3f\n' %rmse + r'$\rho$ = %0.3f' %corr
    ax.annotate(annot, (0,0), (0.0, 0.98), 'axes fraction', ha='left', va='top', 
                color=labelcolor, fontsize=10)
    
    ## Adjust x-axis.
    ax.set(xlim=(-0.02,1.02), xticks=[-0.02, 0.2, 0.4, 0.6, 0.8, 1.02])
    ax.set_xticklabels(ax.get_xticks().round(1), color=tickcolor, fontsize=9)
    ax.set_xlabel('Observed', color=tickcolor, fontsize=9)
    
    ## Adjust y-axis.
    ax.set(ylim=(-0.02,1.02), yticks=[], yticklabels=[], ylabel='')
    if not i:
        ax.spines['left'].set(linewidth=1, color=axiscolor, position=('axes', -0.04))
        ax.set_yticks([-0.02, 0.2, 0.4, 0.6, 0.8, 1.02])
        ax.set_yticklabels(ax.get_yticks().round(1), color=tickcolor, fontsize=9)
        ax.set_ylabel('Predicted', color=tickcolor, fontsize=11)
    
    ## Adjust title.
    ax.set_title(labels[i], loc='left', color=tickcolor, fontsize=11)
    
    ## Adjust legend.
    if not i:
        for color, label in zip(palette, robots): ax.scatter([], [], color=color, label=label.upper())
        ax.legend(loc=2, bbox_to_anchor=(0, 1.21), ncol=4, frameon=False, labelcolor=labelcolor, fontsize=10, 
                  borderpad=0, borderaxespad=0, handletextpad=0.5, handlelength=1.6, columnspacing=1.2)
    
    ## Modify ax spines.
    ax.yaxis.set_tick_params(pad=1)
    ax.spines['bottom'].set(linewidth=1, color=axiscolor)
    ax.tick_params(bottom=True, left=True, color=axiscolor, length=4, width=1)
    if not i: sns.despine(ax=ax, left=False, right=True, top=True, bottom=False)
    else: sns.despine(ax=ax, left=True, right=True, top=True, bottom=False)
    
    ## Add annotation.
    if not i: ax.annotate('B. Observed & model-predicted choice behavior', (0,0), (-0.16,1.24), 'axes fraction', 
                          ha='left', va='bottom', color=labelcolor, fontsize=16)
    
## Save figure.
plt.savefig(os.path.join(ROOT_DIR, 'figures', 'figS03.svg'), dpi=100)