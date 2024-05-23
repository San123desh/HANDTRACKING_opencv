import cv2
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            # for id, lm in enumerate(handLms.landmark):
            #     h, w, c = img.shape
            #     cx, cy = int(lm.x * w), int(lm.y * h)
            #     if id == 4:
            #         cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            #         cv2.putText(img, str(id), (cx - 20, cy - 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 2)
            #         if id == 4:
            #             print(id)
            #             print(cx)
            #             print(cy)
            #             print(time.time())

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
