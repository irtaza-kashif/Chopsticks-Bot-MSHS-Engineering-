from determine_move import find_best_move
import serial.tools.list_ports
import time
import tkinter as tk
from cameraInputTestUpdated import video
bot = [1, 1]
player = [1, 1]

# Direct communication with Arduino
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portsList = []

for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))


val = input("Select port: COM")

for x in range(0, len(portsList)):
    if portsList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portVar)

serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()

# Input players move. ex. (LEFT,RIGHT), (RIGHT,LEFT), (TRANSFER,2,0) in the order of (PLAYER,BOT) with the exception of TRANSFER
# Return bots updated hand. ex. [4, 0], [3, 2]
# Output bots next move. ex. (LEFT,RIGHT), (RIGHT,LEFT), (TRANSFER,2,0) in the order of (BOT,PLAYER) with the exception of TRANSFER

def update_pos(input):
    input = input.split(",")
    
    if input[0] == "LEFT":
        if input[1] == "LEFT":
            bot[0] += player[0]
        if input[1] == "RIGHT":
            bot[1] += player[0]
    elif input[0] == "RIGHT":
        if input[1] == "LEFT":
            bot[0] += player[1]
        if input[1] == "RIGHT":
            bot[1] += player[1]
    elif input[0] == "TRANSFER":
        player[0] = int(input[1])
        player[1] = int(input[2])
        
    for i in range(2):
        if bot[i] >= 5:
            bot[i] = 0
        if player[i] >= 5:
            player[i] = 0
    
    return([bot, player])

def update_final_pos(input):
    input = input.split(",")
    
    if input[0] == "LEFT":
        if input[1] == "LEFT":
            player[0] += bot[0]
        if input[1] == "RIGHT":
            player[1] += bot[0]
    elif input[0] == "RIGHT":
        if input[1] == "LEFT":
            player[0] += bot[1]
        if input[1] == "RIGHT":
            player[1] += bot[1]
    elif input[0] == "TRANSFER":
        bot[0] = int(input[1])
        bot[1] = int(input[2])
        
    for i in range(2):
        if bot[i] >= 5:
            bot[i] = 0
        if player[i] >= 5:
            player[i] = 0
    
    return([bot, player])

def find_action(current_position, end_position):
    if end_position[1] == current_position[1]: # If the player is not hit (Transfer occured)
        return f"TRANSFER,{end_position[0][0]},{end_position[0][1]}"
        
    if current_position[1][0] != end_position[1][0]: # If the players left hand isn't the same after the action (left hand got hit)
        if (current_position[0][0] + current_position[1][0] == end_position[1][0]) or (current_position[0][0] + current_position[1][0] >= 5 and end_position[1][0] == 0): # if bot's left hand and player's left hand add up to players final left hand (bot left hit player left)
            return "LEFT,LEFT"
        elif (current_position[0][1] + current_position[1][0] == end_position[1][0]) or (current_position[0][1] + current_position[1][0] >= 5 and end_position[1][0] == 0): # if bot's right hand and player's left hand add up to players final left hand (bot right hit player left)
            return "RIGHT,LEFT"
    elif current_position[1][1] != end_position[1][1]: # If the players right hand isn't the same after the action (right hand got hit)
        if (current_position[0][0] + current_position[1][1] == end_position[1][1]) or (current_position[0][0] + current_position[1][1] >= 5 and end_position[1][1] == 0): # if bot's left hand and player's right hand add up to players final right hand (bot left hit player right)
            return"LEFT,RIGHT"
        elif (current_position[0][1] + current_position[1][1] == end_position[1][1]) or (current_position[0][1] + current_position[1][1] >= 5 and end_position[1][1] == 0): # if bot's right hand and player's right hand add up to players final right hand (bot right hit player right)
            return "RIGHT,RIGHT"

def main(input):
    current_position = update_pos(input)
    serialInst.write(str(current_position[0]).replace("[", "").replace(" ", "").replace("]", "").encode("utf-8"))
    print(current_position)
    end_position = find_best_move(current_position)

    time.sleep(2) # this could change depending on the move, needs a certain time difference in inputs for the next input to be read

    command = find_action(current_position, end_position)
    serialInst.write(command.encode("utf-8"))
    print(command)
    print(update_final_pos(command))
    print("i did that shit")
while (True):
    user_input = "NA"
    main(video(user_input))
# # User interface set-up
# root = tk.Tk()
# root.title("Chopsticks Interface")
# root.geometry("600x450")
# root.resizable(False, False)
# root.configure(bg = "gray")

# def printInput():
#     main("TRANSFER," + transferInput.get(1.0, "end-1c"))
#     transferInput.delete("1.0", tk.END)

# def printll():
#     main("LEFT,LEFT")

# def printlr():
#     main("RIGHT,LEFT")

# def printrl():
#     main("LEFT,RIGHT")

# def printrr():
#     main("RIGHT,RIGHT")

# transferInput = tk.Text(root, height = 1, width = 3, font = ("Ariel", 40, "bold"))
# transferInput.place(x = 253, y = 336)

# transfer_lbl = tk.Label(root, text = "Type Transfering Moves Here. ex. \"2,0\", \"3,2\"", font = ("Ariel", 10, "bold"), background = "gray")
# transfer_lbl.place(x = 160, y = 310)
# left_lbl = tk.Label(root, text = "Hit Bot's Left Hand", font = ("Ariel", 10, "bold"), background = "gray")
# left_lbl.place(x = 10, y = 150)
# right_lbl = tk.Label(root, text = "Hit Bot's Right Hand", font = ("Ariel", 10, "bold"), background = "gray")
# right_lbl.place(x = 452, y = 150)

# transfer_btn = tk.Button(root, text = "Transfer", command = printInput, height = 2, width = 10)
# transfer_btn.place(x = 260, y = 408)

# ll_btn = tk.Button(root, text = "LEFT", command = printll, height = 4, width = 20)
# lr_btn = tk.Button(root, text = "RIGHT", command = printlr, height = 4, width = 20)
# rl_btn = tk.Button(root, text = "LEFT", command = printrl, height = 4, width = 20)
# rr_btn = tk.Button(root, text = "RIGHT", command = printrr, height = 4, width = 20)
# ll_btn.place(x = 10, y = 10)
# lr_btn.place(x = 10, y = 81)
# rl_btn.place(x = 435, y = 10)
# rr_btn.place(x = 435, y = 81)
# root.mainloop()
