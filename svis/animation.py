import math
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import pdb
from IPython.display import HTML


def animated_video(vid, interval=25, figsize=(5,5), cmap='viridis'):
    def init():
        return (im,)

    def animate(frame):
        im.set_data(frame)
        return (im,)

    fig, ax = plt.subplots(figsize=figsize)
    im = ax.imshow(np.zeros(vid[0].shape), vmin=np.min(vid), vmax=np.max(vid), cmap=cmap);
    plt.axis('off')
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=vid, interval=interval, blit=True)
    plt.close()
    return HTML(anim.to_html5_video())



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


def animated_surface(frames, interval=100, figsize=(15, 10), cmap='viridis'):
    
    
    def update_plot(frame_number, frames, plot):
        plot[0].remove()
        plot[0] = ax.plot_surface(X, Y, frames[frame_number], cmap=cmap, vmin=frames.min(), vmax=frames.max())

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')

    X = np.arange(frames.shape[1])
    Y = np.arange(frames.shape[0])
    X, Y = np.meshgrid(X, Y)
    Z = frames[0]

    plot = [ax.plot_surface(X, Y, Z, cmap=cmap, vmin=frames.min(), vmax=frames.max())]
    ax.set_zlim(frames.min()-1, frames.max()+1)
    ax.view_init(30, 90)

    anim = animation.FuncAnimation(fig, update_plot, fargs=(frames, plot), blit=True)

    plt.close()

    return HTML(anim.to_html5_video())


def animated_flow(x, y, u, v, vid=None, interval=75, figsize=(10, 7)):
    
    U = u #u[:, y, x]
    V = v #v[:, y, x]

    def update_quiver(num, flow, U, V):
        ax.cla()

        if vid is not None:
            ax.imshow(vid[num])
        flow = ax.quiver(x, y, U[num], V[num])
        if vid is None:
            plt.gca().invert_yaxis()
        return flow,

    fig, ax = plt.subplots(figsize=figsize)
    
    if vid is not None:
        im = ax.imshow(vid[0])
        
    flow = ax.quiver(x, y, U[0], V[0], color='black');
    
    if vid is None:
        plt.gca().invert_yaxis()
    
    plt.axis('off')
    anim = animation.FuncAnimation(fig, update_quiver, fargs=(flow, U, V),
                                   interval=interval, blit=True, save_count=U.shape[0])
    plt.close()
    return HTML(anim.to_html5_video())




# def make_polar_movie(vid, interval=25, figsize=(10,10), cmap='viridis'):
#     from matplotlib.colors import Normalize
#     min_mag = np.abs(vid).min()
#     max_mag = np.abs(vid).max()
#     mag = np.abs(vid[0])
#     mag = Normalize(min_mag, max_mag, clip=True)(mag)
#     phase = np.angle(vid[0])    
#     cmap = plt.cm.rainbow
#     # Normalize the colors b/w 0 and 1, we'll then pass an MxNx4 array to imshow
#     colors = Normalize(-np.pi, np.pi)(phase)
#     colors = cmap(colors)

#     # Now set the alpha channel to the one we created above
#     colors[..., -1] = mag

#     def init():
#         return (im,)

#     def animate(frame):
#         mag = np.abs(frame)
#         mag = Normalize(min_mag, max_mag, clip=True)(mag)
#         phase = np.angle(frame)
#         colors = Normalize(-np.pi, np.pi)(phase)
#         colors = cmap(colors)
#         colors[..., -1] = mag
#         im.set_data(colors)
#         return (im,)

#     fig, ax = plt.subplots(figsize=figsize)
# #     ax.imshow(greys)
#     im =ax.imshow(colors)

# #     ax.imshow(colors, extent=(xmin, xmax, ymin, ymax))
# #     # Add contour lines to further highlight different levels.
# #     ax.contour(weights[::-1], levels=[-.1, .1], colors='k', linestyles='-')
# #     ax.set_axis_off()
# #     plt.show()

# #     im = ax.imshow(np.zeros(vid[0].shape), vmin=np.min(vid), vmax=np.max(vid), cmap=cmap);
# #     plt.axis('off')
#     anim = animation.FuncAnimation(fig, animate, init_func=init,
#                                    frames=vid, interval=interval, blit=True)
#     plt.close()
#     return HTML(anim.to_html5_video())


