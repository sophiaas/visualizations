import svis
import numpy as np


def spherical_harmonic(l, m):
    #TODO: Remove axes
    phi = np.linspace(0, np.pi, 100)
    theta = np.linspace(0, 2 * np.pi, 100)
    phi, theta = np.meshgrid(phi, theta)
    xyz = np.array([np.sin(theta) * np.sin(phi),
                    np.sin(theta) * np.cos(phi),
                    np.cos(theta)])
    
    Y = sph_harm(m, l, phi, theta)
    if m < 0:
        Y = np.sqrt(2) * (-1) ** m * Y.imag
    elif m > 0:
        Y = np.sqrt(2) * (-1) ** m * Y.real

    p = svis.spherical(abs(Y), surfacecolor=Y.real)


def spherical_harmonics(l_max):
    #TODO: Remove axes
    from plotly.offline import init_notebook_mode, iplot
    import plotly.graph_objects as go
    import plotly
    from scipy.special import sph_harm
    from plotly.subplots import make_subplots

    
    phi = np.linspace(0, np.pi, 100)
    theta = np.linspace(0, 2 * np.pi, 100)
    phi, theta = np.meshgrid(phi, theta)
    xyz = np.array([np.sin(theta) * np.sin(phi),
                    np.sin(theta) * np.cos(phi),
                    np.cos(theta)])
    
    n_rows = l_max
    n_cols = 2 * l_max + 1
    plot_type = [[{'type': 'surface'}] * n_cols] * n_rows
    fig = make_subplots(rows=n_rows, 
                        cols=n_cols,
                        specs=plot_type,
                        subplot_titles = [' '] * n_cols * n_rows
                        )
    
    for l in range(l_max):
        for i, m in enumerate(range(-l, l+1)):
            Y = sph_harm(m, l, phi, theta)
            if m < 0:
                Y = np.sqrt(2) * (-1) ** m * Y.imag
            elif m > 0:
                Y = np.sqrt(2) * (-1) ** m * Y.real

            p = svis.spherical(abs(Y), surfacecolor=Y.real, show=False)
            r = l + 1
            c = l_max +m  + 1
            fig.add_trace(p.data[0], row=l+1, col=l_max+m+1)
            idx = np.ravel_multi_index((r-1, c-1), (n_rows, n_cols))
            str_m = '{' + str(m) + '}'
            fig.layout.annotations[idx]['text'] = "$Y^{}_{}$".format(l, str_m)
            

    fig.update_traces(showscale=False)
    fig.update_layout(height=300*l_max, width=600*l_max, title_text="Spherical Harmonics")
    fig.show()
