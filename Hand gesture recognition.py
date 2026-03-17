import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
tip_ids =[4,8,12,16,20]

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    gesture="No Hand"
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers = []
            if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1,5):
                if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id]-2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total_fingers = fingers.count(1)
            if total_fingers >= 4:
                gesture = "Play"
            elif total_fingers == 0:
                gesture = "Pause"
            elif total_fingers == 2:
                gesture = "Volume Up"
        cv2.putText(frame, gesture, (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),3)
        cv2.imshow("Gesture Control",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()

