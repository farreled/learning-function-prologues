#importing our libraries
import textdistance
import random
import pandas as pd
import numpy as np
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
            #functionPrologue = str(functionPrologue)
            functionPrologue = functionPrologue.decode("latin-1")
            functionPrologue = functionPrologue[2:-1] #bytearray prepends b' and appends ' so lets remove that
    
            #add our function name and prologue to a dataframe. we will feed this to our model for training
            #this dataframe is a 2D object. think of it as a spreadsheet or a SQL table
            df = pd.DataFrame(np.array([[ID, functionName, functionPrologue]]), columns=['ID', 'Function_Name', 'Function_Prologue'])
            df_list.append(df) #add current dataframe to a list that we will compile into a big dataframe later
            ID = ID + 1
            
        file.close()

#merge our list of dataframes
df = pd.concat(df_list, axis = 0)

X = df["Function_Prologue"]

#we can use different algorithms to determine how similar an input is to our known prologues
avg_similarity = 0
input_code = "UH\x89\xe5H\x83\xec H\x89}\xe8H\x89u\xe0H\x8bE\xe0H\x83\xc0\x01H\x89\xc7\xe8\x91\xfa"
for prologue in X:
    similarity_score = textdistance.ratcliff_obershelp(input_code, prologue)
    avg_similarity = avg_similarity + similarity_score
    
avg_similarity = avg_similarity / len(X)
print("The probability that the input is a prologue is : ", round(avg_similarity, 2))