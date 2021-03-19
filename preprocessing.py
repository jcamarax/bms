import h5py
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage  import transform

f = h5py.File('train_img/train_0.h5py','r')


#print keys
keys = list(f.keys())
img_0 = f[keys[0]]

img = img_0['11800'][:]
plt.imshow(img[:])
plt.show()

img_trans = transform.rescale(img,0.5,anti_aliasing=True)
plt.imshow(img_trans)
plt.show()

def read_img(img):    
    img = mpimg.imread(img)
    img = transform.rescale(img,0.5,anti_aliasing=True)
    return img