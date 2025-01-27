# Smart Vision Safety System

## Overview

It is a real-time fatigue detection system powered by AI. It uses video feed to analyze key indicators of fatigue, including **Eye Aspect Ratio (EAR)** for drowsiness detection and **Mouth Aspect Ratio (MAR)** for yawning detection. If fatigue is detected, the system triggers both visual and audio alerts. Additionally, all events are logged to a CSV file for further analysis. EyesOn also adapts to day and night conditions to ensure accurate detection in varying lighting environments.

## Features

- **Real-Time Fatigue Detection**: Monitors eye (EAR) and mouth (MAR) movements to detect drowsiness and yawning.
- **Audio Feedback**: Provides real-time auditory feedback using **pyttsx3** for drowsiness and yawning alerts.
- **Event Logging**: All detected events (drowsiness, yawning) are logged with timestamps, EAR/MAR values, and event status in a CSV file.
- **Day/Night Mode**: Dynamically adjusts detection thresholds for varying light conditions to enhance accuracy.
- **Real-Time Feedback**: Displays the EAR, MAR, brightness, and fatigue index on the live video feed.
- **Customizable Parameters**: Adjust drowsiness and yawning detection thresholds based on personal needs.

## Requirements

To run this project, you'll need the following Python libraries:

- `face_recognition` (for detecting face landmarks and extracting facial features)
- `opencv-python` (for video capture and displaying frames)
- `numpy` (for numerical computations)
- `scipy` (for calculating the distances between facial points)
- `pyttsx3` (for text-to-speech alerts)
- `csv` (for logging events)
- `datetime` (for timestamp logging)

You can install all the required libraries using:

```bash
pip install -r requirements.txt
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/prantikm07/EyesOn-AI-Powered-Drowsiness-Detection.git
cd EyesOn-AI-Powered-Drowsiness-Detection
```

### 2. Set up a virtual environment (optional but recommended)

- **Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

- **macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

This will open a webcam window that detects drowsiness and yawning in real-time. Alerts will trigger both visually and audibly.

## Usage

### Drowsiness Detection

The **Eye Aspect Ratio (EAR)** is used to determine if a person is falling asleep. If the EAR drops below a predefined threshold, the system detects drowsiness and triggers an alert.

### Yawning Detection

The **Mouth Aspect Ratio (MAR)** is used to identify yawns. If the MAR exceeds a predefined threshold, the system detects yawning and provides an alert.

### Audio Feedback

Upon detecting drowsiness or yawning, the system will play a voice alert via **pyttsx3**. The feedback can be customized as needed.

### Event Logging

Every event (drowsiness or yawning detection) is logged in the `drowsiness_log.csv` file. The data recorded includes:

- **Timestamp**: When the event occurred
- **EAR Value**: Eye Aspect Ratio at the time of the event
- **MAR Value**: Mouth Aspect Ratio at the time of the event
- **Alert Status**: Whether the system triggered an alert ("Yes"/"No")

### Press `Q` to Quit

You can press the **Q key** to stop the application and close the video window.

## Mode Switching (Day/Night Mode)

- **Day Mode**: Uses higher EAR thresholds suitable for daylight conditions.
- **Night Mode**: Adjusts EAR thresholds for lower light levels during the night.

### Configuring Detection Parameters

- **EAR Thresholds**: Adjust `min_aer_day` (for day mode) and `min_aer_night` (for night mode) to optimize drowsiness detection based on testing and environmental factors.
- **MAR Thresholds**: Tweak `mar_threshold` to fine-tune the yawning detection sensitivity.
- **Detection Frames**: Adjust `eye_arc_frames` and `yawn_frames` to set how many frames are required before confirming an alert.

## Log Data Format

The `drowsiness_log.csv` file stores the following data:

| Timestamp           | EAR Value | MAR Value | Alert Status |
| ------------------- | --------- | --------- | ------------ |
| 2022-01-25 10:00:01 | 0.25      | 0.28      | Yes          |
| 2022-01-25 10:05:10 | 0.32      | 0.29      | No           |

## Contributing

Feel free to fork this repository and submit pull requests. I’m always open to suggestions and improvements. If you would like to contribute, you can:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Create a new Pull Request

### License

This project is open-source and available under the MIT License.

## Contact

If you have any questions, feel free to contact me via:
- Email: [suswagata05@gmail.com](mailto:suswagata05@gmail.com)
- LinkedIn: [Suswagata Ghosh](https://www.linkedin.com/in/suswagata-ghosh-318242252/)