#Load packages
import pandas as pd 
import re
import numpy as np
import pickle5 as pickle
import os
import time
import matplotlib.pyplot as plt
from dask import delayed,compute,visualize
import dask.array as da
import numba

#Function to count atoms
def count_atom(atom, formula):
    '''
    Function to count the number of atoms in the InChl formula
    @atom: atom to search in formula
    @formula
    '''

    pattern1 = "".join(['(?<=',atom,')\d{1,2}']) #Pattern to find atoms > 2 units
    pattern2 = "".join(['(?<=',atom,')(\w|)']) #Pattern to find atom = 1
    count1 = re.search(pattern1,formula)
    count2 = re.search(pattern2,formula)
    if count1 is not None:
        return int(count1.group(0))
    elif count2 is not None:
        return int(1)
    else:
        return int(0)
    
#Function to extract second segment of InChl
def text_processing(text):
    text = text.split('/')
    form = text[1]
    return form

#Run processing train target if not present
if os.path.exists('train_target_processes.pkl') is False:
    
    #Load train_target
    train_target = pd.read_csv('train_labels.csv')


    #Creating form colum
    train_target['form'] = train_target['InChI'].apply(text_processing)

    #Creating count columns 
    atoms = ['C','H', 'Br','Cl','F','B','I','N','O','S','P','Si' ]
    for atom in atoms:
        train_target[atom] =  train_target['form'].apply(lambda x: count_atom(atom, x))

    with open('train_target_processes.pkl', 'wb') as handle:
        pickle.dump(train_target, handle, protocol=pickle.HIGHEST_PROTOCOL)

#Unpickling train np arrays

def load_train_X(index):
    '''
    Function to load train data with index
    @index: ex train_0 has index 0
    '''
    path = "".join(['train_img/train_',str(index), '.pkl'])
    with open(path, 'rb') as handle:
        images = pickle.load(handle)

    return images

def load_train_y():
    with open('train_target_processes.pkl', 'rb') as handle:
        y_train = pickle.load(handle)
    
    return y_train





def return_ind(train_X,train_y,index):
    train_X = load_train_X(index)
    train_y = load_train_y()
    img_id_X = list(train_X.keys())
    img_id_Y = train_y['ainimage_id'].tolist()
    
    ind_Y = []

    print("##############")
    print("Starting search")

    tic = time.time()

    for i in range(len(img_id_X)): 
        ind_Y.append(img_id_Y.index(img_id_X[i]))

    toc = time.time()
    print("It took {} mins to find the indixes".format(()))
    
    return ind_Y

def generate_X_y_data(index):
    if os.path.exists('train0_indices.pkl') is False:
        ind_t = return_ind(train_X,train_y,index)
        with open('train0_indices.pkl', 'wb') as handle:
            pickle.dump(ind_t, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        with open('train0_indices.pkl', 'rb') as handle:
            ind0_X = pickle.load(handle)
    
    train_X = load_train_X(0)
    train_y = load_train_y()
    y_train = train_y.iloc[ind0_X,3:]    
    X_train = train_X

    return (X_train, y_train)


X,y = generate_X_y_data(0)