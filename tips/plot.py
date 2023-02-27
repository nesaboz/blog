import matplotlib.pyplot as plt
import numpy as np
import torch

# plt.rcParams["savefig.bbox"] = 'tight'
# if you change the seed, make sure that the randomly-applied transforms
# properly show that the image can be both transformed and *not* transformed!
torch.manual_seed(0)


def plot_pil_images(imgs, labels=None, max_num_cols=5, row_title=None, **imshow_kwargs):
    N = len(imgs)

    if N == 0:
        raise ValueError('imgs is empty.')

    img = imgs[0]
    w, h = img.size

    num_cols = min(max_num_cols, N)
    num_rows = (N - 1) // num_cols + 1

    fig, axs = plt.subplots(nrows=num_rows, ncols=num_cols, squeeze=False)

    for row_idx in range(num_rows):
        for col_idx in range(num_cols):
            idx = row_idx * num_cols + col_idx
            ax = axs[row_idx][col_idx]
            if idx >= N:
                fig.delaxes(ax)
                continue

            img = imgs[idx]
            ax.imshow(np.asarray(img), **imshow_kwargs)
            ax.set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])
            if labels:
                ax.set(title=labels[idx])
                ax.title.set_size(8)

    # sets the size of the canvas to 10 inch width and height that is proportional, so it minimizes empty space
    ratio = (num_rows * h) / (w * num_cols)
    fig.set_size_inches(10, 10*ratio)

    # sets row titles if needed
    if row_title is not None:
        for row_idx in range(num_rows):
            axs[row_idx][0].set(ylabel=row_title[row_idx])

    plt.tight_layout()

    return axs
