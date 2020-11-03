import math
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import pdb
from IPython.display import HTML


def animated_polar(curves, 
                   interval=50, 
                   plot_mean=False,
                   max_cols=4,
                   figsize=(15, 15),
                   title=None,
                   ax_titles=None):
    
    colors = [x['color'] for x in plt.rcParams['axes.prop_cycle']]
    
    curves = np.array(curves)
    n_curves = len(curves)
    if n_curves < 4:
        n_cols = n_curves
    else:
        n_cols = max_cols
        
    n_rows = math.ceil(n_curves / n_cols)
 
    if plot_mean:
        n_lines = 2
        mean_curves = curves.mean(axis=1)
    else:
        n_lines = 1
        
    fig, axes = plt.subplots(figsize=figsize, nrows=n_rows, ncols=n_cols, subplot_kw=dict(polar=True))
    plt.tight_layout()
    if title is not None:
        fig.suptitle(title, fontsize=22)
    
    if type(axes) != np.ndarray:
        axes = [axes]
        
    lines = []
    for i, ax in enumerate(axes):
        line, = ax.plot([], [], color=colors[1], linewidth=3)
        ax.set_ylim(0, max(abs(curves[i]))+1)
        if plot_mean:
            ax.plot([0, np.angle(mean_curves[i])], [0, abs(mean_curves[i])], colors[0], linewidth=3)
        if ax_titles is not None:
            ax.set_title(ax_titles[i])
        lines.append(line)
    
    def update(idx):
        for i, ax in enumerate(axes):
            if len(ax.lines) > n_lines:
                ax.lines.pop()
            lines[i].set_xdata(np.angle(curves[i][:idx]))
            lines[i].set_ydata(abs(curves[i][:idx]))
            ax.plot([0, np.angle(curves[i][idx])], [0, abs(curves[i][idx])], colors[3], linewidth=3)

    anim = animation.FuncAnimation(fig, update, blit=True, interval=interval, save_count=curves.shape[1])
    plt.close()
    return HTML(anim.to_html5_video())