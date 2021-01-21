import seaborn as sns
from matplotlib.colors import ListedColormap


def husl(n):
    return ListedColormap(sns.color_palette("husl", n).as_hex())