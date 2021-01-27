import matplotlib.pyplot as plt
import numpy as np
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objects as go
import plotly


def pointcloud(X, Y, Z, height=500, width=600):
    init_notebook_mode(connected=True)         # initiate notebook for offline plot
    fig = go.Figure(data=[go.Scatter3d(x=X, y=Y, z=Z,
                                       mode='markers')])
    
    fig.update_layout(width=width, height=height)

    fig.show()
    
    
def surface(Z, X=None, Y=None, cmap='viridis', figsize=(10, 5)):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    if X is None:
        X = np.arange(Z.shape[1])
        Y = np.arange(Z.shape[0])
        X, Y = np.meshgrid(X, Y)

    plot = ax.plot_surface(X, Y, Z, cmap=cmap, vmin=Z.min(), vmax=Z.max())

    
def surface2(Z, X=None, Y=None, surfacecolor=None, show=True):
    init_notebook_mode(connected=True)         # initiate notebook for offline plot
    
    if X is None:
        X = np.arange(Z.shape[1])
        Y = np.arange(Z.shape[0])
        X, Y = np.meshgrid(X, Y)
        
    if surfacecolor is None:
        surfacecolor = Z
    
    data = go.Surface(x=X, y=Y, z=Z, surfacecolor=surfacecolor)
    fig = go.Figure(data=data)
    if show:
        fig.show()
    return fig



def volume(values, colorscale='Phase', cmin=None, cmax=None, show=True):
    init_notebook_mode(connected=True)         # initiate notebook for offline plot
    
    X, Y, Z = np.mgrid[0:values.shape[0], 0:values.shape[1], 0:values.shape[2]]

    cmin = values.min() if cmin is None else cmin
    cmax = values.max() if cmax is None else cmax
    
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
    if show:
        fig.show()
    return fig
    
    
def spherical(values, surfacecolor=None, show=True):
    init_notebook_mode(connected=True)         # initiate notebook for offline plot
    
    phi = np.linspace(0, np.pi, values.shape[0])
    theta = np.linspace(0, 2 * np.pi, values.shape[0])
    phi, theta = np.meshgrid(phi, theta)
    xyz = np.array([np.sin(theta) * np.sin(phi),
                    np.sin(theta) * np.cos(phi),
                    np.cos(theta)])
    
    Vx, Vy, Vz = values * xyz
    
    if surfacecolor is None:
        surfacecolor = values
    
    data = go.Surface(x=Vx, y=Vy, z=Vz, surfacecolor=surfacecolor)
    fig = go.Figure(data=data)
    if show:
        fig.show()
    return fig

