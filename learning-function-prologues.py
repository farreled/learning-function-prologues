#importing our libraries
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#open the raw data file that symbull created
#file = open("secretSearcher.out", mode = 'rb') # 'rb' specifies that we are (r)eading a (b)inary file
df_list = []

with open("secretSearcher.out", mode = 'rb') as file:
    #here we will get two pieces of data: the name of the function and its prologue(in bytes)
    #this is awful code 😥
    ID = 1
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

"""
df = pd.read_csv("training_data.csv")

#take all data except the last column
X = df.iloc[:, :-1]##we may not want to do this!
y = df.iloc[:, -1]

#get data that is and isnt a function
functions = df.loc[y == 1]
non_functions = df.loc[y == 0]

#plots for our data
plt.scatter(functions.iloc[:, 0], functions.iloc[:, 1], s=10, label='Functions')
plt.scatter(non_functions.iloc[:, 0], non_functions.iloc[:, 1], s=10, label="Not Functions")
plt.legend()
plt.show()
"""