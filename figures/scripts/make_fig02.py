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
robots = ['gw','ngw','gal','ngal']

## Define palettes.
palette_1 = ['#234f81', '#8e9cb8', '#bf8a82', '#812623']
palette_2 = ['#234f81', '0.75', '0.75', '0.75']
palette_3 = ['#234f81', '#6d7b96', '#ababab']

## Define labels.
labels = ['Day 0', 'Day 3', 'Day 14', 'Day 28']

## Define axis styles.
labelcolor = '#737373'
tickcolor = '#8a8a8a'
axiscolor = '#d3d3d3'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Initialize canvas.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Initialize canvas.
fig = plt.figure(figsize=(9,9))

## Initialize gridspec.
gs = fig.add_gridspec(3, 4, left=0.07, right=0.98, top=0.92, bottom=0.04, 
                      hspace=0.55, wspace=0.16)

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

## Load data.
data = concat([read_csv(os.path.join(ROOT_DIR, 'study01', 'data', session, 'pgng.csv'))
               for session in ['s1','s2','s3','s4']])

## Restrict participants.
reject = read_csv(os.path.join(ROOT_DIR, 'study01', 'data', 's1', 'reject.csv'))
data = data[data.subject.isin(reject.query('reject==0').subject)].reset_index(drop=True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Panels 1a-d: Learning curves.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Main loop.
for i, session in enumerate(sessions):
    
    ## Initialize axis.
    ax = plt.subplot(gs[0,i])
    
    ## Plot learning curves.
    sns.lineplot(x='exposure', y='choice', hue='robot', data=data.query(f'session == {session}'), 
                 hue_order=robots, palette=palette_1, legend=False, errorbar=('ci', 95), lw=3, ax=ax)
    
    ## Add midway line.
    ax.axhline(0.5, color='k', alpha=0.05, zorder=-1)

    ## Adjust x-axis.
    ax.set(xlim=(0.75,30), xticks=[0.75, 5, 10, 15, 20, 25, 30])
    ax.set_xticklabels([1,5,10,15,20,25,30], color=tickcolor, fontsize=9)
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
        for color, label in zip(palette_1, robots): ax.plot([], [], color=color, label=label.upper(), lw=4)
        ax.legend(loc=2, bbox_to_anchor=(0, 1.21), ncol=4, frameon=False, labelcolor=labelcolor,
                  fontsize=10, borderpad=0, borderaxespad=0, handletextpad=0.5, handlelength=1.6,
                  columnspacing=1.2)
        
    ## Modify ax spines.
    ax.yaxis.set_tick_params(pad=1)
    ax.spines['bottom'].set(linewidth=1, color=axiscolor)
    ax.tick_params(bottom=True, left=True, color=axiscolor, length=4, width=1)
    if not i: sns.despine(ax=ax, left=False, right=True, top=True, bottom=False)
    else: sns.despine(ax=ax, left=True, right=True, top=True, bottom=False)
    
    ## Add annotation.
    if not i: ax.annotate('A. Trial-by-trial behavior by session', (0,0), (-0.16,1.24), 'axes fraction', 
                          ha='left', va='bottom', color=labelcolor, fontsize=16)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Panel 2a: Changes in accuracy.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
## Initialize axis.
ax = plt.subplot(gs[1,0])

## Compute accuracy by participant & session.
pivot = data.pivot_table('accuracy', 'subject', 'session')
gb = pivot.melt(ignore_index=False, value_name='accuracy')

## Plot changes.
sns.barplot(x='session', y='accuracy', data=gb, palette=palette_2, estimator=np.nanmedian,
            errorbar=('ci', 95), width=0.88, errwidth=1, capsize=0.15, zorder=5, ax=ax)

## Add percentages.
for i, v in enumerate(pivot.median()): 
    ax.text(i + 1e-3, v - 8e-3, '%0.1f%%' %(v*1e2), ha='center', va='top', 
            color='w' if not i else 'k', fontsize=9, zorder=10)    
    
## Add pairwise comparisons.
plot_comparison(0, 1, 0.98, tickwidth=1e-2, annot='**', ax=ax)
plot_comparison(0, 2, 1.02, tickwidth=1e-2, annot='**', ax=ax)
plot_comparison(0, 3, 1.06, tickwidth=1e-2, annot='**', ax=ax)
    
## Adjust x-axis.
ax.set(xlim=(-0.4,3.4), xticks=np.arange(len(labels)), xlabel='')
ax.set_xticklabels(labels, color=tickcolor, fontsize=9)

## Adjust y-axis.
ax.set(ylim=(0.5, 1.10), yticks=[], ylabel='')

## Adjust title.
ax.set_title('Correct responses', loc='left', color=tickcolor, fontsize=11)

## Modify ax spines.
ax.yaxis.set_tick_params(pad=1)
ax.spines['bottom'].set(linewidth=1, color=axiscolor)
ax.tick_params(bottom=False, left=False, color=axiscolor, length=4, width=1)
sns.despine(ax=ax, left=True, right=True, top=True, bottom=True)

## Add annotation.
ax.annotate('B. Systematic changes in behavior by session', (0,0), (-0.15,1.13), 'axes fraction', 
            ha='left', va='bottom', color=labelcolor, fontsize=16)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Panel 2b: Changes in go bias.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
## Initialize axis.
ax = plt.subplot(gs[1,1])

## Compute choice by participant & session.
pivot = data.pivot_table('accuracy', 'subject', ['action','session'])
pivot = pivot['go'] - pivot['no-go']
gb = pivot.melt(ignore_index=False, value_name='accuracy')

## Plot changes.
sns.barplot(x='session', y='accuracy', data=gb, palette=palette_2, estimator=np.nanmedian,
            errorbar=('ci', 95), width=0.88, errwidth=1, capsize=0.15, zorder=5, ax=ax)

## Add percentages.
for i, v in enumerate(pivot.median()): 
    ax.text(i + 1e-3, v - 4e-3, '%0.1f%%' %(v*1e2), ha='center', va='top', 
            color='w' if not i else 'k', fontsize=9, zorder=10) 

## Add pairwise comparisons.
plot_comparison(0, 1, 0.15, tickwidth=5e-3, annot='**', ax=ax)
plot_comparison(0, 2, 0.17, tickwidth=5e-3, annot='**', ax=ax)
plot_comparison(0, 3, 0.19, tickwidth=5e-3, annot='**', ax=ax)
plot_comparison(1, 3, 0.21, tickwidth=5e-3, annot='**', ax=ax)
    
## Adjust x-axis.
ax.set(xlim=(-0.4,3.4), xticks=np.arange(len(labels)), xlabel='')
ax.set_xticklabels(labels, color=tickcolor, fontsize=9)

## Adjust y-axis.
ax.set(ylim=(0.0, 0.30), yticks=[], ylabel='')

## Adjust title.
ax.set_title('Go bias', loc='left', color=tickcolor, fontsize=11)

## Modify ax spines.
ax.yaxis.set_tick_params(pad=1)
ax.spines['bottom'].set(linewidth=1, color=axiscolor)
ax.tick_params(bottom=False, left=False, color=axiscolor, length=4, width=1)
sns.despine(ax=ax, left=True, right=True, top=True, bottom=True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Panel 2c: Changes in congruency effect.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
## Initialize axis.
ax = plt.subplot(gs[1,2])

## Define congruency.
data['congruence'] = data.robot.replace({'gw': 'c', 'ngal': 'c', 'ngw': 'i', 'gal': 'i'})

## Compute accuracy by participant, session, and congruence.
pivot = data.pivot_table('accuracy', 'subject', ['congruence','session'])
pivot = pivot['c'] - pivot['i']
gb = pivot.melt(ignore_index=False, value_name='accuracy')

## Plot changes.
sns.barplot(x='session', y='accuracy', data=gb, palette=palette_2, estimator=np.nanmedian,
            errorbar=('ci', 95), width=0.88, errwidth=1, capsize=0.15, zorder=5, ax=ax)

## Add percentages.
for i, v in enumerate(pivot.median()):
    y = v - 4e-3 if v >= 2e-2 else (v - 3e-3 if v >= 1e-2 else 0.033)
    ax.text(i + 1e-3, y, '%0.1f%%' %(v*1e2), ha='center', va='top', 
            color='w' if not i else 'k', fontsize=9, zorder=10) 
    
## Add pairwise comparisons.
plot_comparison(0, 1, 0.13, tickwidth=5e-3, annot='**', ax=ax)
plot_comparison(0, 2, 0.15, tickwidth=5e-3, annot='**', ax=ax)
plot_comparison(0, 3, 0.17, tickwidth=5e-3, annot='**', ax=ax)
    
## Adjust x-axis.
ax.set(xlim=(-0.4,3.4), xticks=np.arange(len(labels)), xlabel='')
ax.set_xticklabels(labels, color=tickcolor, fontsize=9)

## Adjust y-axis.
ax.set(ylim=(0.0, 0.30), yticks=[], ylabel='')

## Adjust title.
ax.set_title('Pavlovian bias', loc='left', color=tickcolor, fontsize=11)

## Modify ax spines.
ax.yaxis.set_tick_params(pad=1)
ax.spines['bottom'].set(linewidth=1, color=axiscolor)
ax.tick_params(bottom=False, left=False, color=axiscolor, length=4, width=1)
sns.despine(ax=ax, left=True, right=True, top=True, bottom=True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Panel 2d: Changes in feedback response.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    
## Initialize axis.
ax = plt.subplot(gs[1,3])

## Define previous exposure.
data['prev_sham'] = data.groupby(['subject','session','stimulus']).sham.transform(np.roll, 1)
data.loc[data.exposure == 1, 'prev_sham'] = np.nan

## Compute accuracy by participant, session, and feedback type.
pivot = data.pivot_table('accuracy', 'subject', ['prev_sham','session'])
pivot = pivot[0] - pivot[1]
gb = pivot.melt(ignore_index=False, value_name='accuracy')

## Plot changes.
sns.barplot(x='session', y='accuracy', data=gb, palette=palette_2, estimator=np.nanmedian,
            errorbar=('ci', 95), width=0.88, errwidth=1, capsize=0.15, zorder=5, ax=ax)

## Add percentages.
for i, v in enumerate(pivot.median()):
    ax.text(i + 1e-3, v - 4e-3 if v >= 1e-2 else 0.031, '%0.1f%%' %(v*1e2), ha='center', va='top', 
            color='w' if not i else 'k', fontsize=9, zorder=10) 

## Add pairwise comparisons.
plot_comparison(0, 1, 0.13, tickwidth=5e-3, annot='**', ax=ax)
plot_comparison(0, 2, 0.15, tickwidth=5e-3, annot='**', ax=ax)
plot_comparison(0, 3, 0.17, tickwidth=5e-3, annot='**', ax=ax)
    
## Adjust x-axis.
ax.set(xlim=(-0.4,3.4), xticks=np.arange(len(labels)), xlabel='')
ax.set_xticklabels(labels, color=tickcolor, fontsize=9)

## Adjust y-axis.
ax.set(ylim=(0.0, 0.25), yticks=[], ylabel='')

## Adjust title.
ax.set_title('Feedback sensitivity', loc='left', color=tickcolor, fontsize=11)

## Modify ax spines.
ax.yaxis.set_tick_params(pad=1)
ax.spines['bottom'].set(linewidth=1, color=axiscolor)
ax.tick_params(bottom=False, left=False, color=axiscolor, length=4, width=1)
sns.despine(ax=ax, left=True, right=True, top=True, bottom=True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Panels 3a-d: Individual differences.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Compute accuracy by participant / session / condition.
gb = data.groupby(['subject','session','robot']).accuracy.mean().reset_index()

## Score performance into top five deciles.
gb['score'] = np.digitize(gb.accuracy, [0.6,0.9])

## Calculate proportion of participants in each bin.
gb = gb.groupby(['robot','session','score']).subject.count().reset_index()
gb['prop'] = gb.groupby(['robot','session']).subject.transform(lambda x: x / np.sum(x))
gb['cumprop'] = gb.groupby(['robot','session']).prop.transform(np.cumsum)

## Iteratively plot.
for i, robot in enumerate(robots):

    ## Initialize axis.
    ax = plt.subplot(gs[2,i])
    
    ## Iterative plot percent stacked barchart. 
    for score, color in zip(np.unique(gb.score)[::-1], palette_3):    
    
        ## Plot proportions.
        q = f'robot == "{robot}" and score == {score}'
        sns.barplot(x='session', y='cumprop', data=gb.query(q), order=sessions, 
                    palette=np.repeat(color, 4), width=0.8, linewidth=0, ax=ax)
    
    ## Add annotations.
    q = f'robot == "{robot}" and score == 2'
    for x, (y, z) in enumerate(zip(gb.query(q).prop, gb.query(q).cumprop)):
        ax.annotate('%0.1f%%' %(y*1e2), (0,0), (x + 1e-3, z - y/2 - 1e-2), ha='center', va='bottom',
                    color='w', fontsize=9)
    
    ## Adjust x-axis.
    ax.set(xlim=(-0.4,3.4), xticks=np.arange(len(labels)), xlabel='')
    ax.set_xticklabels(labels, color=tickcolor, fontsize=9)
    
    ## Adjust y-axis.
    ax.set(ylim=(0,1), yticks=np.linspace(0,1,6), yticklabels=[], ylabel='')
    if not i: 
        ax.spines['left'].set(linewidth=1, color=axiscolor, position=('axes', -0.04))
        ax.set_yticklabels(['%0.0f%%' %p for p in np.linspace(0,1e2,6)], fontsize=9, color=tickcolor)
        ax.set_ylabel('Percent of sample', fontsize=9, color=tickcolor, labelpad=0)
    
    ## Adjust title.
    ax.set_title(robot.upper(), loc='left', color=tickcolor, fontsize=11, pad=2)
    
    ## Adjust legend.
    if not i:
        scores = [r'$<60\%$', r'$\geq60\%$', r'$\geq90\%$ correct responses']
        for score, color in zip(scores, palette_3[::-1]): ax.bar(0, 0, color=color, label=score)
        ax.legend(loc=2, bbox_to_anchor=(0, 1.19), ncol=5, frameon=False, labelcolor=labelcolor, fontsize=10,
                  borderpad=0, borderaxespad=0, handletextpad=0.2, handlelength=1.6, columnspacing=1.1)
    
    ## Modify ax spines.
    if not i:
        ax.tick_params(bottom=False, left=True, color=axiscolor, length=4, width=1)
        sns.despine(ax=ax, left=False, right=True, top=True, bottom=True)
    else:
        ax.tick_params(bottom=False, left=False)
        sns.despine(ax=ax, left=True, right=True, top=True, bottom=True)
    
    ## Add annotation.
    if not i: ax.annotate('C. Distribution of correct responses across participants', 
                          (0,0), (-0.15,1.24), 'axes fraction', ha='left', va='bottom', 
                          color=labelcolor, fontsize=16)
    
## Save figure.
plt.savefig(os.path.join(ROOT_DIR, 'figures', 'fig02.svg'), dpi=100)