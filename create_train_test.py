#Load packages
import pandas as pd 
import re


#Load train_target
train_target = pd.read_csv('train_labels.csv')

#find longest string
train_target['InChI'].apply(len).sort_values(ascending = False).head(1)

#Preprocessing the inchi
text = train_target.iloc[646416,1]
text_spl = text.split('/')

def text_processing(text):
    text = text.split('/')
    form = text[1]
    return form

train_target['form'] = train_target['InChI'].apply(text_processing)
train_target['form'].apply(len).sort_values(ascending = False).head(5)

#Finding the longest string
formula = train_target.iloc[1212419,2]


df = train_target.set_index("ainimage_id")
df.iloc[646416,:]

#Function to count atoms
def count_atom(atom, formula):
    '''
    Function to count the number of atoms in the InChl formula
    @atom: atom to search in formula
    '''

    pattern = "".join(['(?<=',atom,')\d{1,2}'])
    count = re.search(pattern,formula).group(0)
    return count


count_atom('Cl', formula)
list(map(lambda x: count_atom(x,formula),['C','H','O']))

