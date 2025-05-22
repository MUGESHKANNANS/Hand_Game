import cv2
import numpy as np
import mediapipe as mp
import random
import time
import math

def football_game():
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands=1)
    cap = cv2.VideoCapture(0)

    # Game variables
    ball_pos = None
    ball_radius = 20
    ball_speed = 5
    goal_width = 100
    score = 0

    def generate_ball_position(width, height):
        return [random.randint(ball_radius, width - ball_radius), 
                random.randint(ball_radius, height - ball_radius)]

    def calculate_distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Initialize ball
        if ball_pos is None:
            ball_pos = generate_ball_position(width, height)

        # Draw elements
        cv2.rectangle(frame, (width//2 - goal_width//2, 0), 
                     (width//2 + goal_width//2, 50), (0, 255, 0), 2)
        cv2.circle(frame, tuple(ball_pos), ball_radius, (0, 0, 255), -1)

        # Hand interaction
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_x = int(index_tip.x * width)
                index_y = int(index_tip.y * height)

                distance = calculate_distance(index_x, index_y, *ball_pos)
                if distance < ball_radius:
                    ball_pos[0] += int((index_x - ball_pos[0]) * 0.2)
                    ball_pos[1] += int((index_y - ball_pos[1]) * 0.2)

        # Goal check
        if 0 < ball_pos[1] < 50 and (width//2 - goal_width//2 < ball_pos[0] < width//2 + goal_width//2):
            score += 1
            ball_pos = generate_ball_position(width, height)

        # Display score
        cv2.putText(frame, f'Score: {score}', (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Hand Football Game', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    football_game()