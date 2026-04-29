import math
from pathlib import Path
import random
from PIL import Image
import matplotlib.pyplot as plt

def get_subplot_dims(num_samples, max_cols=5, aspect_ratio=(4, 3)):
    """
    Calculate number of rows and columns for subplots
    and suggested figure size based on number of samples.

    Args:
        num_samples (int): Number of plots to display.
        max_cols (int): Maximum columns allowed.
        aspect_ratio (tuple): Width:Height ratio of each subplot.

    Returns:
        rows (int), cols (int), fig_size (tuple)
    """
    if num_samples <= 0:
        return 0, 0, (0, 0)

    cols = min(num_samples, max_cols)
    rows = math.ceil(num_samples / cols)

    # Width and height of figure
    width_per_ax, height_per_ax = aspect_ratio
    fig_width = cols * width_per_ax
    fig_height = rows * height_per_ax

    return rows, cols, (fig_width, fig_height)

def plot_image_samples(
        dataset_path,
        mode="random",              # "random" or "per_class"
        n_samples=20,               # used for random mode
        n_per_class=5,              # used for per_class mode
        get_subplot_dims=None       # pass your function here
):
    dataset_path = Path(dataset_path)

    # ---- Collect images ----
    if mode == "random":
        all_images = list(dataset_path.glob("*.ppm"))
        samples = random.sample(all_images, min(n_samples, len(all_images)))

    elif mode == "per_class":
        samples = []
        for class_dir in sorted(dataset_path.iterdir()):
            if class_dir.is_dir():
                images = list(class_dir.glob("*.ppm"))
                if images:
                    k = min(n_per_class, len(images))  # avoid errors
                    samples.extend(random.sample(images, k))
    else:
        raise ValueError("mode must be 'random' or 'per_class'")

    # ---- Plot ----
    if get_subplot_dims:
        nrows, ncols, figsize = get_subplot_dims(len(samples))
    else:
        ncols = 5
        nrows = (len(samples) + ncols - 1) // ncols
        figsize = (ncols * 3, nrows * 3)

    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    axes = axes.flatten()

    for ax, img_path in zip(axes, samples):
        img = Image.open(img_path)
        ax.imshow(img)
        ax.set_title(img_path.parent.name, fontsize=8)
        ax.axis("off")

    # Hide unused axes
    for ax in axes[len(samples):]:
        ax.axis("off")

    plt.tight_layout()
    plt.show()

def plot_data_grid(
        data_list,
        plotting_func,
        max_cols=5,
        aspect_ratio=(5, 4),
        **kwargs
):
    """
    Generic grid plotter for any type of matplotlib chart.

    Args:
        data_list (list): List of DataFrames, Series, or items to plot.
        plotting_func (callable): Function that takes (item, ax) and draws the plot.
        max_cols (int): Max columns in grid.
        aspect_ratio (tuple): Ratio for each individual subplot.
        **kwargs: Extra arguments passed to plotting_func.
    """
    num_samples = len(data_list)
    rows, cols, figsize = get_subplot_dims(num_samples, max_cols, aspect_ratio)

    fig, axes = plt.subplots(rows, cols, figsize=figsize)

    # Handle the case of a single plot (where subplots doesn't return an array)
    if num_samples == 1:
        axes = [axes]
    else:
        axes = axes.flatten()

    for i, item in enumerate(data_list):
        plotting_func(item, axes[i], **kwargs)

    # Hide unused axes
    for j in range(i + 1, len(axes)):
        axes[j].axis("off")

    plt.tight_layout()
    plt.show()
