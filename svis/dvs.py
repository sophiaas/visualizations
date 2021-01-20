import numpy
from IPython.display import HTML
from matplotlib import animation


def plot_dvs(
    pos,
    pol,
    cmap="bwr_r", 
    figsize=(10,10),
    angle=(180, 60),
    depthshade=False,
    original=False,
    rotation=None):
        
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(angle[0], angle[1])
    
    if rotation is not None:
        pos = pos @ rotation

    color = pol
    ax.scatter(
        pos[:, 0],
        pos[:, 2],
        pos[:, 1], 
        c=color, 
        depthshade=depthshade, 
        cmap=cmap)
    
    
def project_image_numpy(pos, 
                        polarity, 
                        transformation, 
                        img_dims=(20, 20), 
                        normalized=True,
                        border=10,
                        sigma=1):
    
    from scipy.stats import multivariate_normal
    
    coords = pos[:, :2].copy()

    if normalized:
        coords = (coords + 1) / 2
        coords[:, 0] = coords[:, 0] * (img_dims[0] - 1)
        coords[:, 1] = coords[:, 1] * (img_dims[1] - 1)
        
    coords = coords + border

    img_dims = np.array(img_dims) + 2 * border
    img_dims = tuple(img_dims)
        
    transformed_image = np.zeros(img_dims[0] * img_dims[1])
    
    if pos.shape[0] == 0:
        return transformed_image.reshape(img_dims)
    
    else:
        all_coords = []

        for row in np.arange(img_dims[0]):
            for col in np.arange(img_dims[1]):
                all_coords.append((row, col))
        all_coords = np.array(all_coords, dtype=float)
                
        timesteps = pos[:, 2].copy()
        
        if pos.shape[0] == 1:
            timesteps[0] = 0
        else:
            timesteps -= timesteps.min()
            timesteps /= timesteps.max()
                

        for i, p in enumerate(polarity):  
            if tuple(transformation.shape[1:]) == img_dims:
                t = np.expand_dims(transformation[:, int(pos[i, 0]), int(pos[i, 1])], 0)
            else:
                t = transformation
            transformed = coords[i] - t * (1 - timesteps[i])

            dist = multivariate_normal(transformed, (np.eye(2) * sigma))
            probs = dist.pdf(all_coords).T * p

            transformed_image = transformed_image + probs
        
        return transformed_image.reshape(img_dims)
    

def project_timeslice(pos, pol, max_timestep=5000, sample_time=500, border=0):
    projections = []

    for j in tqdm(range(int(max_timestep // sample_time))):
        a = pos[:, 2] > j * sample_time
        b = pos[:, 2] <= (j + 1) * sample_time
        idx = a * b
        pos_crop = pos[idx]
        pol_crop = pol[idx]
        projection = project_image_numpy(pos_crop, 
                                         pol_crop, 
                                         transformation=np.array([0, 0]),
                                         border=border,
                                         sigma=1e-3)
        projections.append(projection)
    return projections