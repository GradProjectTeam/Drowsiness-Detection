import cv2 as cv
import mediapipe as mp
import threading
import time
from pygame import mixer
from src.utils import draw_landmarks, get_aspect_ratio, run_speech
from src.config import *

def main():
    speech = pyttsx3.init()
    
    mixer.init()
    def play_alert_sound():
        mixer.Sound("drowsiness-detection/resources/forward.wav").play()
        
    sound_forward = mixer.Sound("drowsiness-detection/resources/forward.wav")
    
    face_mesh = mp.solutions.face_mesh
    draw_utils = mp.solutions.drawing_utils
    landmark_style = draw_utils.DrawingSpec((0, 255, 0), thickness=1, circle_radius=1)  # Set circle radius to 1
    connection_style = draw_utils.DrawingSpec((0, 0, 255), thickness=1, circle_radius=1)  # Set circle radius to 1

    face_model = mp.solutions.face_mesh.FaceMesh(static_image_mode=STATIC_IMAGE,
                                                max_num_faces=MAX_NO_FACES,
                                                min_detection_confidence=DETECTION_CONFIDENCE,
                                                min_tracking_confidence=TRACKING_CONFIDENCE)

    capture = cv.VideoCapture(0)

    frame_count = 0
    eye_closed_start_time = None
    eye_closed_1_sec_time = None
    alert_played = False
    forward_sound_played = False

    drowsy_icon_color = COLOR_GREEN
    yawn_icon_color = COLOR_GREEN

    while True:
        result, image = capture.read()
        if result:
            image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            outputs = face_model.process(image_rgb)

            if outputs.multi_face_landmarks:
                draw_landmarks(image, outputs, FACE, COLOR_GREEN)
                draw_landmarks(image, outputs, LEFT_EYE_TOP_BOTTOM, COLOR_RED)
                draw_landmarks(image, outputs, LEFT_EYE_LEFT_RIGHT, COLOR_RED)
                ratio_left = get_aspect_ratio(image, outputs, LEFT_EYE_TOP_BOTTOM, LEFT_EYE_LEFT_RIGHT)
                draw_landmarks(image, outputs, RIGHT_EYE_TOP_BOTTOM, COLOR_RED)
                draw_landmarks(image, outputs, RIGHT_EYE_LEFT_RIGHT, COLOR_RED)
                ratio_right = get_aspect_ratio(image, outputs, RIGHT_EYE_TOP_BOTTOM, RIGHT_EYE_LEFT_RIGHT)
                ratio = (ratio_left + ratio_right) / 2.0

                
                if ratio > MIN_TOLERANCE:  # Eyes are closed
                    frame_count += 1
                    drowsy_icon_color = COLOR_RED  # Drowsy icon turns red

                    if eye_closed_start_time is None:
                        eye_closed_start_time = time.time()
                    elif not forward_sound_played and time.time() - eye_closed_start_time >= 4:
                        forward_sound_played = True
                        sound_forward.play(loops=-1)  # Play forward sound continuously
                        #print("Forward sound started.")  # Debugging message

                    if eye_closed_1_sec_time is None:
                        eye_closed_1_sec_time = time.time()
                    elif not alert_played and time.time() - eye_closed_1_sec_time >= 2:
                        alert_played = True
                        threading.Thread(target=play_alert_sound).start()
                        #print("Alert sound played.")  

                else:  # Eyes are open
                    # Reset all flags and states when the driver wakes up
                    frame_count = 0
                    eye_closed_start_time = None
                    eye_closed_1_sec_time = None

                    # Stop forward sound if it is playing
                    if forward_sound_played:
                        forward_sound_played = False
                        sound_forward.stop()
                        #print("Forward sound stopped.") 

                    # Reset alert flag
                    alert_played = False
                    drowsy_icon_color = COLOR_GREEN  # Drowsy icon turns green
                    #print("Driver awake, alarms reset.")  # Debugging message


                if frame_count > MIN_FRAME:
                    message = 'Please wake up'
                    t = threading.Thread(target=run_speech, args=(speech, message))
                    t.start()

                draw_landmarks(image, outputs, UPPER_LOWER_LIPS, COLOR_BLUE)
                draw_landmarks(image, outputs, LEFT_RIGHT_LIPS, COLOR_BLUE)
                ratio_lips = get_aspect_ratio(image, outputs, UPPER_LOWER_LIPS, LEFT_RIGHT_LIPS)
                if ratio_lips < 1.8:
                    yawn_icon_color = COLOR_RED  # Yawn icon turns red
                    message = 'You look tired, please take a rest'
                    p = threading.Thread(target=run_speech, args=(speech, message))
                    p.start()
                else:
                    yawn_icon_color = COLOR_GREEN  # Yawn icon turns green

            # Draw the drowsy and yawn icons
            cv.circle(image, (50, 50), 20, drowsy_icon_color, -1)
            cv.putText(image, 'DROWSY', (80, 60), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

            cv.circle(image, (50, 100), 20, yawn_icon_color, -1)
            cv.putText(image, 'YAWN', (80, 110), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

            cv.imshow("FACE MESH", image)
            if cv.waitKey(1) & 255 == 27:
                break

    capture.release()
    cv.destroyAllWindows()
