from skimage.segmentation import slic
from skimage.util import img_as_float
from skimage import io
from skimage import color
import numpy as np

def slic_apply(img_name):
    image = img_as_float(io.imread(img_name))
    image = image[:, :, :3]

    segments = slic(image, n_segments=250, compactness=10)
    segmented_image = color.label2rgb(segments, image, kind='avg')
    segmented_image *= 255/segmented_image.max() 
    # cast to 8bit
    segmented_image = np.array(segmented_image, np.uint8)

    io.imsave(img_name, segmented_image)




