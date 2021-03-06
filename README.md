## Machine Learning On CoreUtils Binaries

1. [symbull output](https://github.com/farreled/learning-function-prologues/tree/main/symbull_output)
2. [binaries from coreutils](https://github.com/farreled/learning-function-prologues/tree/main/coreutils_binaries)
3. [Machine Learning Algorithm](https://github.com/farreled/learning-function-prologues/blob/main/learning-function-prologues.py)

## Documentation for Python file

### Overview

Function prologues are a few lines of code at the beginning of a function that prepare the stack and registers for use. Stripped binaries, however, do not contain function prologues, or rather have them removed in order to reduce the size of the executable. Because of this, identifying functions in stripped binaries can be challenging.
learning-function-prologues.py is meant to try and determine whether an inputted string looks like a function prologue or not. It ingests the raw data from a binary that is generated through [symbull](https://github.com/hawkinsw/symbull). Given an input and the list of prologues, it will try and determine whether it is a prologue or not based on string similarity.

### Input

The python file only requires two inputs:
1. file_list: A folder containing .out files generated by symbull. This is important because the algorithm needs to read from these files to learn what a prologue is supposed to look like
2. input_code: A string input of the code that you want to evaluate as a prologue or not.

### Output

Output generated will show a probability that the input is a prologue or not.

### Methodology

[RatCliff Obsershelp](https://en.wikipedia.org/wiki/Gestalt_Pattern_Matching) pattern matching is used to determine if the input is similar to any given prologue. Once given an input, it will loop through all of the ingested prologues and check their similarity, keeping the highest similarity score, which is used to determine whether the input is a prologue.



*By: Ned Farrell and Meg Jones*
