#!usr/bin/python

##########################################################
#                                                     
#          #      #####   #####  #  #####
#          #     #     # #       # #
#          #     #     # #   ### # #
#          #     #     # #     # # #
#          #####  #####   #####  #  #####
#
#  ###   #  #   #  #   #  #     ###  #####  ###   ####
# #      #  ## ##  #   #  #    #   #   #   #   #  #   #
#  ###   #  # # #  #   #  #    #####   #   #   #  #### 
#     #  #  #   #  #   #  #    #   #   #   #   #  #   #
#  ###   #  #   #   ###   #### #   #   #    ###   #    #
#
# Description:
#  Provides digital circuit logic output based on given
# circuit and input vector. Circuits can be placed in 
# the same directory as this script in the standard text
# text file format for representing digital circuits. 
# 
# Usage: python3 main.py <circuit_name> <input_vector>
#  Eg:- python3 main.py s27 1101011
#
# Developer: Lakshmi S
# GitHub: lakshmi-sathi
# Email: lakshmi.sathi96@gmail.com
# 
##########################################################


import itertools
import sys

input_vector=[]
primary_input_pins=[]
primary_output_pins=[]

#Add .txt to input circuit name to get circuit file name
filename = sys.argv[1]+".txt"

input_vector_str = sys.argv[2]

#check if input vector is binary
for digit in input_vector_str:
    if (int(digit) > 1):
        print("Please enter a binary input vector")
        exit()
#converting input vector string to integer       
input_vector = [int(val) for val in input_vector_str]

#open required circuit file
f = open(filename,"r")

#Used to store index of last net.
last_net_index=0 

#To store count of lines in the circuit file.
no_of_lines = 0
for line in f:
    line = line.strip()
    word = line.split()
    func = word[0]
    net_indices_str = word[1:-1]
    if func =='INPUT':
        #n = list(map(int, net_indices_str))
        primary_input_pins = list(map(int, net_indices_str))
       
        #If input size of input vector doesn't match the size required for the given circuit, print and exit.
        if(len(primary_input_pins)!=len(input_vector_str)):
            print("Please input a",len(primary_input_pins),"element long vector")
            exit()
    if func == 'OUTPUT':
        primary_output_pins = list(map(int, net_indices_str))

    #Line by line search to find the last net index (largest net number)
    net_indices = list(map(int, net_indices_str))
    if(last_net_index < max(net_indices)):
            last_net_index = max(net_indices)
    #Count number of lines in the circuit file.
    no_of_lines = no_of_lines + 1
f.close()

#'wire' is a global binary list where each element corresponds to value of each net in the circuit in order,
#Initialising 'wire'
#Equivalent to multiplying 0 by total number of nets.
wire = [0]*(last_net_index)

#defining all logic gate functions
def INV(w):
    wire[w[1]-1] = int(not wire[w[0]-1])

def BUF(w):
    wire[w[1]-1] = int(wire[w[0]-1])

def NAND(w):
    wire[w[2]-1] = int(not (wire[w[0]-1] and wire[w[1]-1]))

def OR(w):
    wire[w[2]-1] = int( wire[w[0]-1] or wire[w[1]-1])

def AND(w):
    wire[w[2]-1] = int(wire[w[0]-1] and  wire[w[1]-1])

def NOR(w):
    wire[w[2]-1] = int(not ((wire[w[0]-1])or ( wire[w[1]-1])))

#returns output vector
def OUTPUT(w):
    output_vector = [wire[indx-1] for indx in w]
    return output_vector     

#assigns input vector to net
def INPUT(w):
    for i in range(len(w)):
        wire[w[i]-1] = input_vector[i]


f = open(filename,"r")
lines = f.readlines()
f.close()

nets_done = []
line_no = 0
completion = [0]*(no_of_lines)

#Corresponding input wires getting asssigned with the input values
INPUT(primary_input_pins)

#iterate endlessly through the circuit file lines until
#all net logic values get computed
for line in itertools.cycle(lines):
    word = line.split()
    func = word[0]
    net_indices = []
    net_indices_str = []

    if(func =='INPUT' or func =='OUTPUT'):
        net_indices_str = word[1:-1]
        net_indices = list(map(int, net_indices_str))
    else:
        net_indices_str = word[1:]
        net_indices = list(map(int, net_indices_str))

    #As primary input values already known
    
    nets_done = primary_input_pins

    if func=='INV':
        if (net_indices[0] in nets_done) and ( completion[line_no] == 0):
            INV(net_indices)
            completion[line_no]=1
            nets_done.append(net_indices[1])
            if (net_indices[0] not in nets_done):
                nets_done.append(net_indices[0])
            print("line",line_no+1, "-",func, "done")

    if func=='BUF':
        if(net_indices[0] in nets_done) and (completion[line_no]==0):
            BUF(net_indices)
            completion[line_no]=1
            print("line",line_no+1, "-",func, "done")
            nets_done.append(net_indices[1])
            if (net_indices[0] not in nets_done):
                nets_done.append(net_indices[0])
            

    if func=='AND':
        if(net_indices[0] in nets_done) and (net_indices[1] in nets_done) and (completion[line_no]==0):
            AND(net_indices)
            completion[line_no]=1
            print("line",line_no+1, "-",func, "done")
            nets_done.append(net_indices[2])
            if (net_indices[0] not in nets_done):
                nets_done.append(net_indices[0])
            if (net_indices[1] not in nets_done):
                nets_done.append(net_indices[1])

    if func=='NOR':
        if(net_indices[0] in nets_done) and (net_indices[1] in nets_done) and (completion[line_no]==0):
            NOR(net_indices)
            completion[line_no]=1
            print("line",line_no+1, "-",func, "done")
            nets_done.append(net_indices[2])
            if (net_indices[0] not in nets_done):
                nets_done.append(net_indices[0])
            if (net_indices[1] not in nets_done):
                nets_done.append(net_indices[1])
            
    if func=='NAND':
        if(net_indices[0] in nets_done) and (net_indices[1] in nets_done) and (completion[line_no]==0):
            completion[line_no]=1
            NAND(net_indices)
            print("line",line_no+1, "-",func, "done")
            nets_done.append(net_indices[2])
            if (net_indices[0] not in nets_done):
                nets_done.append(net_indices[0])
            if (net_indices[1] not in nets_done):
                nets_done.append(net_indices[1])

    if func=='OR':
        if(net_indices[0] in nets_done) and (net_indices[1] in nets_done) and (completion[line_no]==0):
            completion[line_no]=1
            OR(net_indices)
            print("line",line_no+1, "-",func, "done")
            nets_done.append(net_indices[2])
            if (net_indices[0] not in nets_done):
                nets_done.append(net_indices[0])
            if (net_indices[1] not in nets_done):
                nets_done.append(net_indices[1])

    if func=='INPUT':
        completion[line_no]=1

    if func=='OUTPUT':
        completion[line_no]=1
    
    line_no+=1

    if line_no == (no_of_lines):
        line_no=0

    #checking if all lines completed
    if completion.count(1)==(no_of_lines):
        print("|--------------------------------------------------")
        break

#printing the output
output = OUTPUT(primary_output_pins)
print("Output ( net indices", primary_output_pins,")","=", output)
