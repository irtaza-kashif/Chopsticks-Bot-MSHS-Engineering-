# import the opencv library
import cv2
import mediapipe as mp
import opentelemetry

# define a video capture object
vid = cv2.VideoCapture(1)

mpHands = mp.solutions.hands
mpDrawing = mp.solutions.drawing_utils
hand = mpHands.Hands()

tipIds = [4, 8, 12, 16, 20]

while(True):
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
        print(leftHand.landmark[0].y)
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
    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()