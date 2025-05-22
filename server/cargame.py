import cv2
import numpy as np
import mediapipe as mp
import random
import time

# Setup MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(min_detection_confidence=0.2)

# Game setup
def car_game():
    cap = cv2.VideoCapture(0)
    frame_width, frame_height = 640, 480
    car_width, car_height = 50, 80
    lane_count = 3
    lane_width = frame_width // lane_count

    player_x = frame_width // 2
    player_y = frame_height - car_height - 10
    obstacles = []
    obstacle_speed = 7
    spawn_interval = 1.5
    last_spawn_time = time.time()
    score = 0
    game_over = False

    def generate_obstacle():
        lane = random.randint(0, lane_count - 1)
        return {"x": lane * lane_width + (lane_width - car_width) // 2, "y": -car_height}

    def draw_car(frame, x, y, color=(0, 255, 255)):
        cv2.rectangle(frame, (x, y), (x + car_width, y + car_height), color, -1)

    def check_collision(player_x, player_y, obs_x, obs_y):
        return (player_x < obs_x + car_width and
                player_x + car_width > obs_x and
                player_y < obs_y + car_height and
                player_y + car_height > obs_y)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (frame_width, frame_height))
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Hand detection
        hand_results = hands.process(rgb)
        if hand_results.multi_hand_landmarks and not game_over:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                player_x = int(index_tip.x * frame_width) - car_width // 2
                player_x = max(0, min(player_x, frame_width - car_width))

        # Obstacle management
        if time.time() - last_spawn_time > spawn_interval and not game_over:
            obstacles.append(generate_obstacle())
            last_spawn_time = time.time()

        for obs in obstacles:
            obs["y"] += obstacle_speed
            draw_car(frame, obs["x"], obs["y"], (0, 0, 255))

        obstacles = [obs for obs in obstacles if obs["y"] < frame_height]
        score += len([obs for obs in obstacles if obs["y"] + car_height > frame_height])

        if not game_over:
            draw_car(frame, player_x, player_y, (0, 255, 0))

        # Collision check
        game_over = any(check_collision(player_x, player_y, obs["x"], obs["y"]) for obs in obstacles)

        # Face detection
        face_results = face_detection.process(rgb)
        if face_results.detections:
            for detection in face_results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = frame.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # UI elements
        cv2.putText(frame, f"Score: {score}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        if game_over:
            cv2.putText(frame, "Game Over!", (180, frame_height // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

        cv2.imshow("Hand Car Game with Face Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    car_game()