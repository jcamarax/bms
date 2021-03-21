#Load packages
import os 
from functools import reduce
import itertools
import time
import pickle


#Xxtract all the pathname of the images

def extract_file(text):
    '''
    Function that returns the full path of the pictures contained in subfolders of folder @text
    '''
    list_all_png = []
    for path, subdirs, files in os.walk(text):
        for name in files:
            list_all_png.append(os.path.join(path, name))
    
    return list_all_png


#Creating train and test files
tic = time.time()
if os.path.exists('pickle/train_path.pickle') == False:
    train_path = extract_file('train')  

if os.path.exists('pickle/test_path.pickle') == False:   
    test_path = extract_file('test')
toc = time.time()
print("Duration for creating metadata files for test an train is {} s".format(toc-tic))


if os.path.exists('pickle/train_path.pickle') == False:
    #Saving research
    with open('pickle/train_path.pickle', 'wb') as handle:
        pickle.dump(train_path, handle,protocol=pickle.HIGHEST_PROTOCOL)

if os.path.exists('pickle/test_path.pickle') == False:
    with open('pickle/test_path.pickle', 'wb') as handle:
        pickle.dump(test_path, handle,protocol=pickle.HIGHEST_PROTOCOL)

def unload_paths():
    '''Function to load the pickled object'''

    with open('pickle/train_path.pickle', 'rb') as handle:
        train_path = pickle.load(handle)

    with open('pickle/test_path.pickle', 'rb') as handle:
        test_path = pickle.load(handle)
    
    return train_path, test_path
