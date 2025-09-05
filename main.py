import cv2
import mediapipe as mp
import pygame
import os
import time

# ─── Initialize Pygame Mixer ────────────────────────────────────────────────
pygame.mixer.init()

# ─── Load Audio File Paths ──────────────────────────────────────────────────
NUMBERED_FOLDER = "audio/numbered"

numbered_songs = {} 

for fname in os.listdir(NUMBERED_FOLDER):
    name, ext = os.path.splitext(fname)
    if ext.lower() in [".mp3", ".wav"]:
        try:
            num = int(name)
            if 1 <= num <= 10:
                numbered_songs[num] = os.path.join(NUMBERED_FOLDER, fname)
        except ValueError:
            pass

if len(numbered_songs) != 10:
    print("⚠️  Warning: You should have exactly 10 files named 1.mp3–10.mp3 in audio/numbered/")

# ─── Set up MediaPipe Hands ─────────────────────────────────────────────────
mp_hands = mp.solutions.hands
hands_detector = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8 
)

mp_draw = mp.solutions.drawing_utils

def count_raised_fingers(hand_landmarks):
    fingers_up = 0
    landmarks = hand_landmarks.landmark

    # Thumb
    if landmarks[4].x < landmarks[3].x:
        fingers_up += 1

    # Index, middle, ring, pinky
    tip_ids = [8, 12, 16, 20]
    for tip_id in tip_ids:
        if landmarks[tip_id].y < landmarks[tip_id - 2].y:
            fingers_up += 1

    return fingers_up

def play_audio_file(path):
    if not os.path.isfile(path):
        print(f"🔈 File not found: {path}")
        return
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
    except Exception as e:
        print("Error playing audio:", e)

# ─── MAIN ────────────────────────────────────────────────────────────────────
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌  Error: Cannot open webcam.")
    exit()

last_total = -1
last_play_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️  Warning: Failed to read frame.")
        break

    frame = cv2.flip(frame, 1)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands_detector.process(image_rgb)

    total_fingers = 0

    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_lms, mp_hands.HAND_CONNECTIONS)
            total_fingers += count_raised_fingers(hand_lms)

    # Display finger count
    cv2.putText(
        frame,
        f"Fingers: {total_fingers}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 255, 0) if total_fingers > 0 else (0, 0, 255),
        2
    )

    now = time.time()
    if total_fingers != last_total and (now - last_play_time) > 1.0:
        last_play_time = now
        last_total = total_fingers

        if 1 <= total_fingers <= 10:
            song_path = numbered_songs.get(total_fingers)
            if song_path:
                print(f"▶️  Playing song for {total_fingers} fingers.")
                play_audio_file(song_path)
            else:
                print(f"⚠️  No file for {total_fingers} fingers.")
        else:
            print("🛑 No fingers raised or invalid count. No song played.")

    cv2.imshow("Gesture-Controlled Yoto Player", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()
