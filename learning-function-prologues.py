#importing our libraries
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

#create a list of all our binaries from symbull
file_list = os.listdir("symbull_output")

df_list = []
ID = 1

for file in file_list:
    file = "symbull_output/" + file
    with open(file, mode = 'rb') as file: #open the binary file. 'rb' specifies that we will (r)ead a (b)inary file
        #here we will get two pieces of data: the name of the function and its prologue(in bytes)
        while True:
            functionNameLength = file.read(2) #first 2 bytes of the data tells us how long the function name is
            if not functionNameLength:
                #EOF
                break
            functionNameLength = functionNameLength.decode('utf-8')
            if functionNameLength.isdigit():
                functionNameLength = int(functionNameLength)
                functionName = file.read(functionNameLength)
            else: #this means that the function length is single digit, so we also captured the first char of the name
                extraPart = functionNameLength[1] #this is the first char of the name. save it so we can add it back later
                functionNameLength = functionNameLength[0:1] #slicing the var to get only the first character (length of function)
                functionNameLength = int(functionNameLength)
                functionName = file.read(functionNameLength - 1) #since we incorrectly moved forward 2 chars, we need to realign ourselves
                functionName = extraPart + functionName.decode('utf-8')
            
            functionPrologue = bytearray()
            functionPrologue+=file.read(30) #put 30 bytes of the file into an array of bytes
            functionPrologue = bytes(functionPrologue)
            functionPrologue = str(functionPrologue)
            functionPrologue = functionPrologue[2:-1] #bytearray prepends b' and appends ' so lets remove that
    
            #add our function name and prologue to a dataframe. we will feed this to our model for training
            #this dataframe is a 2D object. think of it as a spreadsheet or a SQL table
            df = pd.DataFrame(np.array([[ID, functionName, functionPrologue]]), columns=['ID', 'Function Name', 'Function Prologue'])
            df_list.append(df) #add current dataframe to a list that we will compile into a big dataframe later
            ID = ID + 1
            
        file.close()

#merge our list of dataframes
df = pd.concat(df_list, axis = 0)

#training goes here