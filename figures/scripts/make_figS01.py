import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from os.path import dirname
from pandas import read_csv
from matplotlib.markers import MarkerStyle
from matplotlib.patches import FancyArrowPatch
sns.set_theme(style='white', context='notebook', font_scale=1.2)
ROOT_DIR = dirname(dirname(dirname(os.path.realpath(__file__))))
np.random.seed(47404)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Define plot parameters.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Define axis styles.
labelcolor = '#666666'
tickcolor = '#8a8a8a'
axiscolor = '#d3d3d3'

## Define point styles.
fillstyles = ['full', 'bottom', 'full']
palette = ['#4f90a6', '#a9c6d2', '#d6a6af', '#a64f65']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Initialize canvas.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Initialize canvas.
fig, ax = plt.subplots(1, 1, figsize=(9,4.5))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Load and prepare data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Load sample data.
data = read_csv(os.path.join(ROOT_DIR, 'figures', 'support', 'example23.csv'))

## Format data.
f = lambda x: np.unique(x, return_inverse=True)[-1]
data['x'] = (data.trial - 1) % 20
data['y'] = (data.trial - 1) // 20
data['set'] = (data.stimulus - 1) // 4
data['robot'] = data.robot.replace({'GW': 0, 'NGW': 1, 'GAL': 2, 'NGAL': 3})
data['dup'] = data.groupby(['set','robot']).stimulus.transform(f)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
### Plotting.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## Iteratively add markers.
for i, (x, y, j, k, m) in enumerate(zip(data.x, data.y, data.set, data.robot, data.dup)):
    
    ## Plot marker.
    ax.plot(x, y, marker='o', markersize=15, markeredgewidth=1.8, fillstyle=fillstyles[j],
            markerfacecolor=palette[k] if j else 'w', markerfacecoloralt='w', 
            markeredgecolor=palette[k])
    if m: ax.plot(x, y, marker='o', markersize=2, color=palette[k] if not j else 'w')
    
    ## Add trial marker.
    ax.text(x, y + 0.2, i+1, ha='center', va='top', color=tickcolor, fontsize=8)
    
## Add annotation (first transition).
# ax.fill_between([11.5,19.5], 0.7, 1.4, color='0.965')
# ax.fill_between([-0.5, 6.5], 1.7, 2.4, color='0.965')
# ax.text(11.5, 1.45, 'Set 2 starts', ha='left', va='top', color=labelcolor, fontsize=9)
# ax.text(6.5, 2.45, 'Set 1 ends', ha='right', va='top', color=labelcolor, fontsize=9)
    
## Add annotation (second transition).
# ax.fill_between([11.5,19.5], 2.7, 3.4, color='0.965')
# ax.fill_between([-0.5, 6.5], 3.7, 4.4, color='0.965')
# ax.text(11.5, 3.45, 'Set 3 starts', ha='left', va='top', color=labelcolor, fontsize=9)
# ax.text(6.5, 4.45, 'Set 2 ends', ha='right', va='top', color=labelcolor, fontsize=9)

## Add annotation (set demarcations).
# ax.annotate('', xy=(1.0, 0.843), xytext=(1.0+1e-6, 0.843), xycoords='axes fraction', 
#             arrowprops=dict(arrowstyle='-[, widthB=3.0, lengthB=0.3', lw=2.0, color=axiscolor))
# ax.annotate('', xy=(1.0, 0.480), xytext=(1.0+1e-6, 0.480), xycoords='axes fraction', 
#             arrowprops=dict(arrowstyle='-[, widthB=3.0, lengthB=0.3', lw=2.0, color=axiscolor))
# ax.annotate('', xy=(1.0, 0.121), xytext=(1.0+1e-6, 0.121), xycoords='axes fraction', 
#             arrowprops=dict(arrowstyle='-[, widthB=3.0, lengthB=0.3', lw=2.0, color=axiscolor))

## Demarcate second set.
ax.fill_between([-0.5, 19.5], 1.65, 3.50, color='0.965')

## Adjust x-axis.
ax.set(xlim=(-0.5, 19.5), xticks=[], xlabel='')

## Adjust y-axis.
ax.invert_yaxis()
ax.set(yticks=[], ylabel='')

## Adjust title.
ax.set_title('  One example block of the modified Pavlovian Go/No-go Task', 
             loc='left', color=labelcolor, fontsize=13)

## Adjust legends (set 1).
m11, = plt.plot([], [], marker='o', mfc='w', mec=palette[0], ms=15, mew=1.8, lw=0)
m12, = plt.plot([], [], marker='o', mfc='w', mec=palette[1], ms=15, mew=1.8, lw=0)
m13, = plt.plot([], [], marker='o', mfc='w', mec=palette[3], ms=15, mew=1.8, lw=0)
m14, = plt.plot([], [], marker='o', color=palette[3], ms=3, lw=0)
l1 = ax.legend([m11, m12, m13, (m13, m14)], ['GW','NGW','NGAL','NGAL'], ncol=2,
               loc=6, bbox_to_anchor=(0.995, 0.843), frameon=False, fontsize=9,
               markerscale=0.5, columnspacing=0, handletextpad=0,
               title='  Set 1', title_fontsize=10, labelcolor=labelcolor)
plt.setp(l1.get_title(), color=labelcolor, fontsize=10)
l1._legend_box.align = 'left'

## Adjust legends (set 1).
m11, = plt.plot([], [], marker='o', fillstyle='bottom', color=palette[0], ms=15, mew=1.8, lw=0)
m12, = plt.plot([], [], marker='o', fillstyle='bottom', color=palette[1], ms=15, mew=1.8, lw=0)
m13, = plt.plot([], [], marker='o', fillstyle='bottom', color=palette[2], ms=15, mew=1.8, lw=0)
m14, = plt.plot([], [], marker='o', color='w', ms=3, lw=0)
l2 = ax.legend([m11, m12, m13, (m13, m14)], ['GW','NGW','GAL','GAL'], ncol=2,
               loc=6, bbox_to_anchor=(0.995, 0.480), frameon=False, fontsize=9,
               markerscale=0.5, columnspacing=0, handletextpad=0,
               title='  Set 2', title_fontsize=10, labelcolor=labelcolor)
plt.setp(l2.get_title(), color=labelcolor, fontsize=10)
l2._legend_box.align = 'left'

## Adjust legends (set 3).
m31, = plt.plot([], [], marker='o', color=palette[0], ms=15, mew=1.8, lw=0)
m32, = plt.plot([], [], marker='o', color=palette[1], ms=15, mew=1.8, lw=0)
m33, = plt.plot([], [], marker='o', color=palette[2], ms=15, mew=1.8, lw=0)
m34, = plt.plot([], [], marker='o', color=palette[3], ms=15, mew=1.8, lw=0)
l3 = ax.legend([m31, m32, m33, m34], ['GW','NGW','GAL','NGAL'], ncol=2,
               loc=6, bbox_to_anchor=(0.995, 0.121), frameon=False, fontsize=9,
               markerscale=0.5, columnspacing=0, handletextpad=0,
               title='  Set 3', labelcolor=labelcolor)
plt.setp(l3.get_title(), color=labelcolor, fontsize=10)
l3._legend_box.align = 'left'

## Place legends.
plt.gca().add_artist(l1)
plt.gca().add_artist(l2)

## Modify ax spines.
ax.tick_params(bottom=False, left=False)
sns.despine(ax=ax, left=True, right=True, top=True, bottom=True)

## Save figure.
plt.subplots_adjust(left=0.01, right=0.86, bottom=0.04, top=0.93)
plt.savefig(os.path.join(ROOT_DIR, 'figures', 'figS01.svg'), dpi=100)