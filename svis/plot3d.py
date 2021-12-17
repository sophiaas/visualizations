import matplotlib.pyplot as plt
import numpy as np
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objects as go
import plotly
from harmonics.spaces import s2


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
    
    
def spherical(values,
              b=None,
              theta=None, 
              phi=None, 
              show=True, 
              surface=False, 
              surfacecolor=None,
              grid_type='Clenshaw-Curtis',
              centered=False):
    
    init_notebook_mode(connected=True)         # initiate notebook for offline plot

    if theta is None:
        if b is None:
            raise ValueError('The value of b must be specified')
        theta, phi = s2.meshgrid(b, grid_type=grid_type, centered=centered)

    spherical = np.concatenate([np.expand_dims(np.ones(theta.shape).ravel(), -1), np.expand_dims(theta.ravel(), -1), np.expand_dims(phi.ravel(), -1)], axis=-1)
    
    xyz = s2.change_coordinates(spherical, to="cartesian", centered=centered)
    
    x, y, z = xyz.T
    
    x = x.reshape(theta.shape)
    y = y.reshape(theta.shape)
    z = z.reshape(theta.shape)

    Vx = values * x
    Vy = values * y
    Vz = values * z

    if surface:
        if surfacecolor is None:
            surfacecolor=values

                                                                                                   
                                          
        data = go.Surface(x=Vx, y=Vy, z=Vz, surfacecolor=surfacecolor, )
        
    else:
        data = go.Surface(x=x, y=y, z=z, surfacecolor=values)
        
    fig = go.Figure(data=data)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig

