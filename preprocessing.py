import h5py
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage  import transform, util
import scipy
import numpy as np
import pickle5 as pickle


def read_img(img):    
    img = mpimg.imread(img)
    img = util.invert(img)
    img = scipy.sparse.csr_matrix(img)
    return img

with open('train_img/train_0.pkl', 'rb') as handle:
    images = pickle.load(handle)

img_id = list(images.keys())
img_test = images[img_id[10000]].toarray()
plt.imshow(img_test)
plt.show()


