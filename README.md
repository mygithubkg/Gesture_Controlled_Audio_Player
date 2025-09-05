# Gesture-Controlled Music Player

This Python script uses OpenCV and MediaPipe to create a gesture-controlled music player. It detects the number of fingers held up to a webcam and plays a corresponding audio file.

## Features

-   **Real-time Hand Tracking**: Utilizes Google's MediaPipe library to detect and track hands in the webcam feed.
-   **Finger Counting**: Accurately counts the number of raised fingers on one or two hands.
-   **Gesture-based Playback**: Plays a specific audio file based on the number of fingers detected (1 through 10).
-   **Visual Feedback**: Displays the live camera feed with hand landmarks and the current finger count overlaid.

## Project Structure

For the script to work correctly, your project must have the following directory structure:

```
.
├── main.py
├── audio/
│   └── numbered/
│       ├── 1.mp3
│       ├── 2.mp3
│       ├── ...
│       └── 10.mp3
└── README.md
```

You must place exactly 10 audio files (e.g., `.mp3` or `.wav`) inside the `audio/numbered/` directory, named from `1` to `10`.

## Setup and Installation

1.  **Prerequisites**:
    *   Python 3.x
    *   A webcam connected to your computer.

2.  **Install Dependencies**:
    Install the required Python libraries using pip.

    ```sh
    pip install opencv-python mediapipe pygame
    ```

3.  **Add Audio Files**:
    Create the `audio/numbered` directory and add your 10 audio files, naming them `1.mp3`, `2.mp3`, and so on.

## How to Use

1.  Run the main script from your terminal:

    ```sh
    python main.py
    ```

2.  A window will open showing your webcam feed.
3.  Hold up your hand(s) to the camera. The script will count your raised fingers.
4.  Based on the count (1-10), the corresponding song from the `audio/numbered` folder will play.
5.  To stop the program, press the 'q' key while the webcam window is active.