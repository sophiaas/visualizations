import matplotlib.pyplot as plt
import numpy as np


def surface(values, cmap='viridis', figsize=(10, 5)):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')

    X = np.arange(Z.shape[1])
    Y = np.arange(Z.shape[0])
    X, Y = np.meshgrid(X, Y)

    plot = ax.plot_surface(X, Y, values, cmap=cmap, vmin=frames.min(), vmax=frames.max())

    
def volume(values, colorscale='Phase', cmin=None, cmax=None)
    from plotly.offline import init_notebook_mode, iplot
    from plotly.graph_objs import *
    import plotly.graph_objects as go
    import plotly

    init_notebook_mode(connected=True)         # initiate notebook for offline plot
    X, Y, Z = np.mgrid[0:100, 0:values.shape[1], 0:values.shape[2]]

    cmin = values.min() if cmin is None
    cmax = values.max() if cmax is None
    
    fig = go.Figure(data=go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=values.flatten(),
        opacity=0.1, # needs to be small to see through all surfaces
        surface_count=17, # needs to be a large number for good volume rendering,
        colorscale=colorscale,
        cmin=cmin,
        cmax=cmax
        ))

    fig.show()
