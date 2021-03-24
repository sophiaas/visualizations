from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.pyplot as plt


def image_grid(data, shape=(10,10), figsize=(10,10), cmap='viridis', share_range=True):

    fig = plt.figure(figsize=figsize)
    grid = ImageGrid(fig, 111,  # similar to subplot(111)
                     nrows_ncols=shape,  # creates 10x10 grid of axes
                     axes_pad=0.1,  # pad between axes in inch.
                     )

    if share_range:
        vmin = data.min()
        vmax = data.max()
        
    for ax, im in zip(grid, data):
        # Iterating over the grid returns the Axes.
        if share_range:
            ax.imshow(im, vmin=vmin, vmax=vmax, cmap=cmap)
        else:
            ax.imshow(im, cmap=cmap)
        ax.set_axis_off()

    plt.show()