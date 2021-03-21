import h5py
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage  import transform, util
import scipy
import numpy as np



def read_img(img):    
    img = mpimg.imread(img)
    img = util.invert(img)
    img = scipy.sparse.csr_matrix(img)
    return img

#f = h5py.File('train_img/train_0.h5py','r')


#print keys
#keys = list(f.keys())
#img_0 = f[keys[0]]

#img = img_0['1100'][:]


#test = scipy.sparse.csr_matrix(util.invert(img))

#plt.imshow(util.invert(img))
#plt.show()


