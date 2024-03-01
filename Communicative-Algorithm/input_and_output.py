from determine_move import find_best_move
import time

# Direct communication with Arduino
import serial.tools.list_ports

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

def update_pos():
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

def find_action():
    if end_position[1] == current_position[1]: # If the player is not hit (Transfer occured)
        # print(f"TRANSFER,{end_position[0][0]},{end_position[0][1]}")
        return f"TRANSFER,{end_position[0][0]},{end_position[0][1]}"
        
    if current_position[1][0] != end_position[1][0]: # If the players left hand isn't the same after the action (left hand got hit)
        if (current_position[0][0] + current_position[1][0] == end_position[1][0]) or (current_position[0][0] + current_position[1][0] >= 5 and end_position[1][0] == 0): # if bot's left hand and player's left hand add up to players final left hand (bot left hit player left)
            # print("LEFT,LEFT")
            return "LEFT,LEFT"
        elif (current_position[0][1] + current_position[1][0] == end_position[1][0]) or (current_position[0][1] + current_position[1][0] >= 5 and end_position[1][0] == 0): # if bot's right hand and player's left hand add up to players final left hand (bot right hit player left)
            # print("RIGHT,LEFT")
            return "RIGHT,LEFT"
    elif current_position[1][1] != end_position[1][1]: # If the players right hand isn't the same after the action (right hand got hit)
        if (current_position[0][0] + current_position[1][1] == end_position[1][1]) or (current_position[0][0] + current_position[1][1] >= 5 and end_position[1][1] == 0): # if bot's left hand and player's right hand add up to players final right hand (bot left hit player right)
            # print("LEFT,RIGHT")
            return"LEFT,RIGHT"
        elif (current_position[0][1] + current_position[1][1] == end_position[1][1]) or (current_position[0][1] + current_position[1][1] >= 5 and end_position[1][1] == 0): # if bot's right hand and player's right hand add up to players final right hand (bot right hit player right)
            # print("RIGHT,RIGHT")
            return "RIGHT,RIGHT"

bot = [1, 1]
player = [1, 1]

input = input("INPUT: ").split(",")
current_position = update_pos()
serialInst.write(str(current_position[0]).replace("[", "").replace(" ", "").replace("]", "").encode("utf-8"))
end_position = find_best_move(current_position)

command = find_action()
time.sleep(2) # this could change depending on the move, needs a certain time difference in inputs for the next input to be read
serialInst.write(command.encode("utf-8"))
