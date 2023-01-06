#%%
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import skimage as sk
import numpy as np

image = sk.io.imread(r'Capture.PNG', as_gray = True)

# apply threshold
thresh = sk.filters.threshold_otsu(image)
bw = sk.morphology.closing(image > thresh, sk.morphology.square(3))
# %%

# label image regions
label_image = sk.measure.label(bw)

# to make the background transparent, pass the value of `bg_label`,
# and leave `bg_color` as `None` and `kind` as `overlay`
image_label_overlay = sk.color.label2rgb(label_image, image=image, bg_label=0)

fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(image_label_overlay)

for region in sk.measure.regionprops(label_image):
    # take regions with large enough areas
    # draw rectangle around segmented coins
    minr, minc, maxr, maxc = region.bbox
    rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                fill=False, edgecolor='red', linewidth=2)
    ax.add_patch(rect)

ax.set_axis_off()
plt.tight_layout()
plt.show()
# %%
