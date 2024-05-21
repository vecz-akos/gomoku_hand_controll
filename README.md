# Gomoku with hand control

Current progress: __done__

This Python project allows you to play Gomoku by placing X's and O's using an initialized template image captured by your webcam. It utilizes OpenCV for position tracking.

## Run

 1. Start script:

```bash
# clone repository
cd gomoku_hand_controll
pip install -r requirements.txt
python main.py
```

 2. Focus on Gomoku window.

 3. Press `Space` to take a picture about the template image (red bordered rectangle).

 4. You can move the game cursor.

## Todo list

 - [x] Implement game logic and state tracking
 - [x] Create a user interface for displaying the game board
 - [x] Read and process the webcam stream
 - [x] Develop template recognition for piece placement
