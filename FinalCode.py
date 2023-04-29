import time 
import sys
sys.path.append('.../')

from Common_Libraries.p2_lib import *

import random
from random import shuffle

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print(error_update_sim)
        
arm = qarm()

update_thread = repeating_timer(2, update_sim)

# Drop off locations
smallR = [-0.6121, 0.2411, 0.3704]
bigR = [-0.3587, 0.1449, 0.2973]
smallG = [0.0, -0.6465, 0.3700]
bigG = [0.0, -0.399, 0.31]
smallB = [0.0, 0.6450, 0.3700]
bigB = [0.0, 0.388, 0.31]

pick_up = [0.5055, 0.0, 0.0277]
home = [0.4064, 0.0, 0.4826]
drop_off_L = [smallR, smallG, smallB, bigR, bigG, bigB] #Create a drop off list that has six different lists for each container drop off location
L_th = 0.9
s_th = 0.1 #Variables for my differnt thresholds, Use L_th and S_th for most of my functions. 
# The small threshold is not 0 because the muscle sensor moves randomly sometimes which can cause some error. Having a threshold below 0.1 can make it more efficient

#Global
openarm = True
opendrawer = False

def identify_bin(ID):
    if ID == 1:
        ID = (drop_off_L[0])
    elif ID == 2:
        ID = (drop_off_L[1])
    elif ID == 3:
        ID = (drop_off_L[2])
    elif ID == 4:
        ID = (drop_off_L[3])
    elif ID == 5:
        ID = (drop_off_L[4])
    elif ID == 6:
        ID = (drop_off_L[5])
    return ID
    
def pickup():
    while True:
        if arm.emg_left() > L_th and arm.emg_right() < S_th:
            arm.move_arm(pick_up[0], pick_up[1], pick_up[2])
            break #Break functions is used throughout our code to stop the infinite looop.
    return None #Return None is used throughout the code to return a value that we can use later on
    
def move_end_effector(ID):
    while True:
        if arm.emg_left() > L_th and arm.emg_right() < S_th:
            home()
            time.sleep(1)
            arm.move_arm(identify_bin(ID)[0], identify_bin(ID)[1], identify_bin(ID)[2]) #Use drop off list and the randomized container ID to find the drop off location. the -1 is because the ID numbers are indexed by 1
            break
        return None
        
def gripper():
    global openarm
    time.sleep(1)
    while True:
        if arm.emg_left() > L_th and arm.emg_right() > L_th:
            if openarm == True:
                arm.control_gripper(45)
                openarm == False
                break                 
        elif arm.emg_left() < S_th and arm.emg_right() < S_th and openarm ==  False:  #Set boundaries to release the container (ungrip)
            arm.control_gripper(-45)
            openarm = True
            break
    return None
    
def autoclave(ID):      #Define function and pass container as a parameter.
    global opendrawer   #Define a global opendrawer variable that stores data that can be used throughout the code
    while True:  
        if arm.emg_left() < S_th and arm.emg_right() > L_th and opendrawer == False:  #Set boundaries for which the autoclave will open its drawer for the large containers
            if ID == 4:
                arm.open_red_autoclave(True)
                opendrawer == True                          #Set the global variable to true when the autovlave drawer closes
                break
            elif ID == 5:
                arm.open_green_autoclave(True)
                opendrawer == True
                break
            elif ID == 6:
                arm.open_blue_autoclave(True)
                opendrawer == True
                break
            
        elif arm.emg_left() < S_th and arm.emg_right() > L_th and opendrawer == True:  #If autoclave is open, use the elif to close the autoclave drawers
            if ID == 4:
                arm.open_red_autoclave(False)
                opendrawer == False     #Set the global variable to false when the autoclave drawer closes
                break
            elif ID == 5:
                arm.open_green_autoclave(False)
                opendrawer == False
                break
            elif ID == 6:
                arm.open_blue_autoclave(False)
                opendrawer == False
                break
            
    return None
            
def home():
    arm.move_arm(0.04064, 0.0, 0.4026)
    return none
    
def main():
    ID_spawn = []                 #Create an empty list
    while len(ID_spawn) < 6:      #The function can run as long as the list has a length that is less than 6
        time.sleep(1)
        ID = random.randint(1,6)  #Random integer is picked which is the ID of the container
        if ID in ID_spawn:        #Checks if the ID that is generated is in the list
            continue              #If the ID is already int he list, it will go back to the top. If it isn't, it will continue
        else:
            ID_spawn.append(ID)
            identify_bin(ID)
            arm.spawn_cage(ID)
            pickup()
            gripper()
            time.sleep(1)
            
            if ID == 4 or ID == 5 or ID == 6:
                move.end_effector(ID)
                autoclave(ID)
                gripper()
                time.sleep(1)
                autoclave(ID)
                time.sleep(1)
                home()
                
            else:
                move_end_effector(ID)
                time.sleep(1)
                gripper()
                time.sleep(2)
                home()
        return None
        
if __name__ == "__main__":
    main()

    
        
