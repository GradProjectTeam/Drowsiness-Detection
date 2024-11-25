
# Drowsiness Detection

A Python-based project designed for real-time drowsiness detection using facial landmarks with MediaPipe and computer vision techniques. The system monitors a person's facial features to detect signs of drowsiness, such as eye closure and yawning, and provides audio alerts to warn the user.

## Features
- Real-time facial landmark detection using MediaPipe
- Eye aspect ratio and yawn detection to identify drowsiness
- Audio alerts using pyttsx3 and pygame
- Visual indicators for drowsiness and yawning on the screen
- Configurable alert thresholds for different levels of fatigue

## Requirements

Make sure you have Python 3.x installed on your machine, then install the necessary dependencies using pip.

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Dependencies:
- `opencv-python`
- `mediapipe`
- `pygame`
- `pyttsx3`
- `scipy`

## Project Structure

```
drowsiness-detection/
├── src/
│   ├── __init__.py                 # Marks the src folder as a package
│   ├── drowsiness_detection.py     # Main drowsiness detection logic
│   ├── utils.py                    # Utility functions
│   └── config.py                   # Configuration variables and constants
├── resources/
│   └── forward.wav                 # Alert sound file
├── demo.py                         # Entry point to run the program
├── requirements.txt                # List of dependencies
├── README.md                       # Project documentation
└── .gitignore                      # Files to ignore in version control
```

## How to Run

1. Clone the repository:

```bash
git clone <repository-url>
```

2. Navigate to the project directory:

```bash
cd drowsiness-detection
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Run the program:

```bash
python demo.py
```

This will start the drowsiness detection system using your webcam. If the system detects drowsiness or yawning, it will provide audio and visual alerts.

## How It Works

1. **Facial Landmark Detection**: The system uses MediaPipe to detect key facial landmarks, such as the eyes and mouth.
2. **Eye Aspect Ratio (EAR)**: It calculates the Eye Aspect Ratio (EAR) to detect if the eyes are closed for a prolonged period, a common sign of drowsiness.
3. **Yawning Detection**: The system also tracks the aspect ratio of the mouth to detect yawning, another sign of fatigue.
4. **Alerts**: If drowsiness or yawning is detected, an audio alert is played and visual indicators (icons) appear on the screen.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository, make changes, and submit a pull request. Contributions are always welcome!
