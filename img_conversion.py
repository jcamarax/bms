#Load packages and train, test path data
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from find_path_data import unload_paths
from dask import delayed, compute
import h5py
import psutil, time, os,signal
import memory
from skimage  import transform
from preprocessing import read_img
import pickle5 as pickle
from collections import namedtuple
import re

#Load path files
train_path, test_path = unload_paths()

def extract_name(path):
    '''
    Function that extract the identifier of the image
    @path of the image
    '''
    match = re.match(".+/(.+)\\.png",path)

    return match.group(1)


def img_to_array_delayed(path):
    '''
    Function to convert images from their path to arrays. Useful for big datasets.
    @path: a list of path names of the images to be converted into arrays
    '''

    #Initialisation 
    tic = time.time()
    
    result = {}
    for img in path:
        try:
            #preproprocessing 
            id = extract_name(img)
            result[id] = delayed(read_img)(img) 
            
        except:
            print("There was an error at step" + img)
    
    toc = time.time()

    print("The  parrallism task instructions took {} s".format(toc-tic))
    tic = time.time()
    result =compute(result)
    toc = time.time()
    print("The  computation took  took {} s".format(toc-tic))
    return result[0]


def create_save_imgs_h5py(path, chunks, type_set ="train"):
    '''
    
    '''
    #Creating chunks
    chunk = list(range(0,len(path), int(len(path)/chunks)))
    chunk.append(len(path)) 

    #Sequence
    index = list(range(len(chunk)))


    #Save list of file
    print('##################')
    print('Starting conversion')
    print('##################')

    memory.memory_footprint()
    for i in  index:
        if os.path.exists(type_set+"_img/"+type_set+"_"+str(i)+".h5py") == False:
            print('creating file'+'/'+type_set+'_img/train_'+str(i))
            train_img = img_to_array_delayed(train_path[slice(chunk[i],chunk[i+1],1)])


            print('starting serialisation with h5py ')
            
            #Serialisation with h5py
            tic = time.time()

            f = h5py.File(type_set+"_img/"+type_set+"_"+str(i)+".h5py", 'w')
            dset = f.create_group(type_set+"_"+str(i))
            for pos,array in enumerate(train_img):
                dset[str(pos)] = array
            

            toc = time.time()
            print('finished serialisation after {} mins'.format((toc-tic)/60)) 

            memory.memory_footprint()
            break
    print('##################')
    print('End conversion')
    print('##################')


def create_save_imgs_scipy(path, chunks, type_set ="train"):
    '''
    
    '''
    #Creating chunks
    chunk = list(range(0,len(path), int(len(path)/chunks)))
    chunk.append(len(path)) 

    #Sequence
    index = list(range(len(chunk)))


    #Save list of file
    print('##################')
    print('Starting conversion')
    print('##################')

    memory.memory_footprint()
    for i in  index:
        if os.path.exists(type_set+"_img/"+type_set+"_"+str(i)+".pkl") == False:
            print('creating file'+'/'+type_set+'_img/'+type_set+'_'+str(i))
            train_img = img_to_array_delayed(path[slice(chunk[i],chunk[i+1],1)])


            print('starting serialisation with scipy ')
            
            #Serialisation with h5py
            tic = time.time()

            with open(type_set+"_img/"+type_set+"_"+str(i)+".pkl",'wb') as handle:
                pickle.dump(train_img, handle,protocol=pickle.HIGHEST_PROTOCOL)

            toc = time.time()
            print('finished serialisation after {} mins'.format((toc-tic)/60)) 

            memory.memory_footprint()
            break
    print('##################')
    print('End conversion')
    print('##################')

create_save_imgs_scipy(train_path, 15)
create_save_imgs_scipy(test_path, 15, type_set = "test")
