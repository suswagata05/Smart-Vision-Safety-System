import face_recognition
import cv2
import numpy as np
from scipy.spatial import distance as dist
import pyttsx3
import csv
from datetime import datetime

# Thresholds and counters
min_aer_day = 0.20
min_aer_night = 0.17
mar_threshold = 0.12
eye_arc_frames = 10
yawn_frames = 2

counter = 0
yawn_counter = 0
fatigue_index = 0

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Open the CSV file for logging
log_file = 'drowsiness_log.csv'
with open(log_file, 'a', newline='') as file:
    writer = csv.writer(file)
    # Write the header if the file is empty
    if file.tell() == 0:
        writer.writerow(['Timestamp', 'EAR', 'MAR', 'Event'])

def audio_feedback(message):
    """Provides audio feedback using text-to-speech."""
    engine.say(message)
    engine.runAndWait()

def eye_ar(eye):
    """Calculates the Eye Aspect Ratio (EAR)."""
    a = dist.euclidean(eye[1], eye[5])
    b = dist.euclidean(eye[2], eye[4])
    c = dist.euclidean(eye[0], eye[3])
    ear = (a + b) / (2 * c)
    return ear

def mouth_aspect_ratio(mouth):
    """Calculates the Mouth Aspect Ratio (MAR)."""
    a = dist.euclidean(mouth[2], mouth[10])  # 51, 59
    b = dist.euclidean(mouth[4], mouth[8])   # 53, 57
    c = dist.euclidean(mouth[0], mouth[6])   # 49, 55
    mar = (a + b) / (2 * c)
    return mar

def main():
    global counter, yawn_counter, fatigue_index
    video_capture = cv2.VideoCapture(0)
    video_capture.set(8, 720)
    video_capture.set(9, 560)

    with open(log_file, 'a', newline='') as file:
        writer = csv.writer(file)

        while True:
            ret, frame = video_capture.read()
            face_landmarks_list = face_recognition.face_landmarks(frame)
            ear = None
            mar = None

            # Determine day or night mode
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)
            min_aer = min_aer_day if brightness >= 50 else min_aer_night

            for face_landmarks in face_landmarks_list:
                # Get EAR and draw eye landmarks
                left_eye = face_landmarks['left_eye']
                right_eye = face_landmarks['right_eye']
                mouth = face_landmarks['top_lip'] + face_landmarks['bottom_lip']

                left_ear = eye_ar(left_eye)
                right_ear = eye_ar(right_eye)
                ear = (left_ear + right_ear) / 2

                mar = mouth_aspect_ratio(mouth)

                lpts = np.array(left_eye)
                rpts = np.array(right_eye)
                mouth_pts = np.array(mouth)

                cv2.polylines(frame, [lpts], True, (255, 255, 0), 1)
                cv2.polylines(frame, [rpts], True, (255, 255, 0), 1)
                cv2.polylines(frame, [mouth_pts], True, (0, 255, 255), 1)

                # Drowsiness detection
                if ear < min_aer:
                    counter += 1
                    if counter >= eye_arc_frames:
                        fatigue_index += 1
                        audio_feedback("You look drowsy. Please take a break.")
                        cv2.putText(frame, 'Drowsiness Alert!', (5, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
                        
                        # Log drowsiness event
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        writer.writerow([timestamp, ear, mar, 'Drowsiness Alert'])

                else:
                    counter = 0

                # Yawning detection
                if mar > mar_threshold:
                    yawn_counter += 1
                    if yawn_counter >= yawn_frames:
                        fatigue_index += 1
                        audio_feedback("Yawning detected. Please rest for a while.")
                        cv2.putText(frame, 'Yawning Detected!', (5, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
                        
                        # Log yawning event
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        writer.writerow([timestamp, ear, mar, 'Yawning Detected'])

                else:
                    yawn_counter = 0

            # Display real-time metrics
            cv2.putText(frame, f'EAr: {ear:.2f}' if ear else 'EAr: --', (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            cv2.putText(frame, f'MAR: {mar:.2f}' if mar else 'MAR: --', (5, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            cv2.putText(frame, f'Fatigue Index: {fatigue_index}', (5, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            cv2.putText(frame, f'Brightness: {brightness:.2f}', (5, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            cv2.putText(frame, f'Mode: {"Day" if min_aer == min_aer_day else "Night"}', (5, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            cv2.putText(frame, "Press 'Q' to quit", (5, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

            # Show the frame
            cv2.imshow('Fatigue Detection System', frame)

            # Quit on 'q' key press
            if cv2.waitKey(1) == ord('q'):
                break

    # Release resources and close windows
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
