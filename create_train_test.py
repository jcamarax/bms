#Load packages
import pandas as pd 
import re
import numpy as np
import pickle5 as pickle
import os
import time
from dask import delayed,compute
#Load train_target
train_target = pd.read_csv('train_labels.csv')


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
    #Creating form colum
    train_target['form'] = train_target['InChI'].apply(text_processing)

    #Creating count columns 
    atoms = ['C','H', 'Br','Cl','F','B','I','N','O','S','P','Si' ]
    for atom in atoms:
        train_target[atom] =  train_target['form'].apply(lambda x: count_atom(atom, x))

    with open('train_target_processes.pkl', 'wb') as handle:
        pickle.dump(train_target, handle, protocol=pickle.HIGHEST_PROTOCOL)

#Unpickling train np arrays

def load_train(index):
    '''
    Function to load train data with index
    @index: ex train_0 has index 0
    '''
    path = "".join(['train_img/train_',str(index), '.pkl'])
    with open(path, 'rb') as handle:
        images = pickle.load(handle)

    return images

train = {}
for index in range(0,15):
    train.update(load_train(index))

with open('train_all_src.pkl','wb') as handle:
    pickle.load(train, handle, protocol=pickle.HIGHEST_PROTOCOL)

