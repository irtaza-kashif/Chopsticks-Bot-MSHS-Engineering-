# import the opencv library
def video(input):
    import cv2
    import mediapipe as mp
    import opentelemetry
    # define a video capture object
    vid = cv2.VideoCapture(1)

    mpHands = mp.solutions.hands
    mpDrawing = mp.solutions.drawing_utils
    hand = mpHands.Hands()

    tipIds = [4, 8, 12, 16, 20]

    width = 650
    height = 500
    bueno = False
    start_point =(560, 386)
    end_point =(800, 595)
    handswapping = False
    while (input == "NA"):
        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hand.process(rgbFrame)

        # print(marks(result))

        leftLandmarks = []
        rightLandmarks = []
        leftFingers = []
        rightFingers = []

        if result.multi_hand_landmarks and len(result.multi_hand_landmarks) == 2:
            if (result.multi_handedness[0].classification[0].label == "Right"):
                leftHand = result.multi_hand_landmarks[0]
                rightHand = result.multi_hand_landmarks[1]
            else:
                leftHand = result.multi_hand_landmarks[1]
                rightHand = result.multi_hand_landmarks[0]
            for n in range(20):
                if (rightHand.landmark[n].x*width >= 225 and leftHand.landmark[n].x*width <= 475 and rightHand.landmark[n].y*height <= 325 and leftHand.landmark[n].y*height <= 325):
                    handswapping = True
                if (rightHand.landmark[n].x*width <= 200 and rightHand.landmark[n].y*height >= 375):
                    input = "RIGHT,RIGHT"
                    handswapping = False
                if (leftHand.landmark[n].x*width >= 500 and leftHand.landmark[n].y*height >= 375):
                    input = "LEFT,LEFT"
                    handswapping = False
                if (leftHand.landmark[n].x*width <= 200 and leftHand.landmark[n].y*height >= 375):
                    input = "LEFT,RIGHT"
                    handswapping = False
                if (rightHand.landmark[n].x*width >= 500 and rightHand.landmark[n].y*height >= 375):
                    input = "RIGHT,LEFT"
                    handswapping = False
                if (rightHand.landmark[n].x*width <= 225 and leftHand.landmark[n].x*width >= 475 and rightHand.landmark[n].y*height <= 325 and leftHand.landmark[n].y*height <= 325):
                    if (handswapping == True):
                        input = "TRANSFER," + str(leftCount) + "," + str(rightCount)
                    bueno = True
                
            
            # if (result.multi_handedness[1].classification[0].label == "Left"):
            #     leftHand = result.multi_hand_landmarks[1]
            # else:
            #     rightHand = result.multi_hand_landmarks[1]

            # if leftHand.landmark[9].x > 0.5 and leftHand.landmark[9].y < 0.5:
            #     # print("Top right of screen")
            #     pass

            for id, lm in enumerate(leftHand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                leftLandmarks.append([id, cx, cy])

            for id, lm in enumerate(rightHand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                rightLandmarks.append([id, cx, cy])

            for id in range(1, 5):
                if leftLandmarks[tipIds[id]][2] > leftLandmarks[tipIds[id] - 2][2]:
                    leftFingers.append(1)
                else:
                    leftFingers.append(0)
            for id in range(1, 5):
                if rightLandmarks[tipIds[id]][2] > rightLandmarks[tipIds[id] - 2][2]:
                    rightFingers.append(1)
                else:
                    rightFingers.append(0)

            # print(result.multi_hand_landmarks[0].landmark[0].x)  Keep this, useful reference
            # --------------------------------------------
            # Each object in the list multi_hand_landmarks is a hand. Each item in the landmark list
            # is a joint/point of interest. Then use .x .y and .z to retrieve pos data
            for hand_landmarks in result.multi_hand_landmarks:
                # print(hand_landmarks.landmark[0].x)
                mpDrawing.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

            leftCount = leftFingers.count(1)
            rightCount = rightFingers.count(1)
            # print("\n")
            # print("\n")
            # print("\n")
            # print("\n")
            # print("\n")
            # print("\n")
            # print("\n")
            # print("\n")
            # print("\n")
            # print(str(leftCount) + " left fingers")
            # print(str(rightCount) + " right fingers")

        if result.multi_hand_landmarks and len(result.multi_hand_landmarks) == 1:
            # print(result.multi_handedness[0].classification[0].label)
            pass

        # Display the resulting frame
        cv2.rectangle(frame, (0, 0), (200, 275), (0, 255, 255), thickness= 3, lineType=cv2.LINE_8) #yellow
        cv2.rectangle(frame, (450, 0), (650, 275), (255, 0, 255), thickness= 3, lineType=cv2.LINE_8)#purple 
        cv2.rectangle(frame, (225, 0), (425, 275), (0, 255, 0), thickness= 3, lineType=cv2.LINE_8)#green
        cv2.rectangle(frame, (0, 300), (175, 500), (0, 0, 255), thickness= 3, lineType=cv2.LINE_8)#red
        cv2.rectangle(frame, (475, 300), (650, 500), (255, 0, 0), thickness= 3, lineType=cv2.LINE_8)#blue
        cv2.imshow('frame', frame)
        path = 'C:/Users/irtaz/downloads/Hand Detection Code/Untitled.png'
        image = cv2.imread(path) 
        if (bueno == True):
                bueno = False
        else:
            input = "NA"
        # cv2.namedWindow("Display", cv2.WINDOW_AUTOSIZE
        # cv2.imshow('Display', image)
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            quit()
    
# After the loop release the cap object
    vid.release()
# Destroy all the windows
    cv2.destroyAllWindows()
    return(input)