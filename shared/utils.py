from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["savefig.bbox"] = 'tight'


def plot_pil_images(imgs, titles, max_per_row=5, figsize=(5,5), 
                    save_path=None, remove=[], **imshow_kwargs):
    
    N = len(imgs)
    if titles:
        assert N == len(titles)
    else:
        titles = [''] * N
     
    if N <= max_per_row:
        imgs = [imgs]
        titles = [titles]
    else:
        # convert 1D imgs to 2D dimgs
        dimgs = []
        dtitles = []
        while len(imgs) > max_per_row:
            dimgs.append(imgs[:max_per_row])
            dtitles.append(titles[:max_per_row])
            imgs = imgs[max_per_row:]
            titles = titles[max_per_row:]
        dimgs.append(imgs)
        dtitles.append(titles)
        imgs = dimgs
        titles = dtitles
        
    num_rows = len(imgs)
    num_cols = len(imgs[0])
    fig, axs = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=figsize)

    for row_idx, row in enumerate(imgs):
        for col_idx, img in enumerate(row):
            if num_rows == 1:
                ax = axs[col_idx]
            else:
                ax = axs[row_idx, col_idx]
            ax.imshow(np.asarray(img), **imshow_kwargs)
            ax.set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])
            ax.set_title(titles[row_idx][col_idx])
     
    # delete unused axes
    for i in remove + list(range(N, num_rows*num_cols)):
        if num_rows == 1:
            ax = axs[i]
        else:
            ax = axs[i//num_cols, i%num_cols]
        ax.set_axis_off()
            
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path,
                    dpi=300,
                    bbox_inches='tight'
                    # bbox_inches=Bbox.from_extents(-0.2, -0.2, 8, 4)
        )
        print(f'Saved to {save_path}')
    
    plt.show()