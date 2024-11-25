import cv2 as cv
import mediapipe as mp
import threading
import time
from pygame import mixer
from src.utils import draw_landmarks, get_aspect_ratio, run_speech
from src.config import *

def main():
    mixer.init()
    speech = pyttsx3.init()
    sound_forward = mixer.Sound("resources/forward.wav")

    face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=STATIC_IMAGE,
                                                max_num_faces=MAX_NO_FACES,
                                                min_detection_confidence=DETECTION_CONFIDENCE,
                                                min_tracking_confidence=TRACKING_CONFIDENCE)

    capture = cv.VideoCapture(0)

    frame_count = 0
    eye_closed_start_time = None
    forward_sound_played = False

    while True:
        result, image = capture.read()
        if result:
            image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            outputs = face_mesh.process(image_rgb)

            if outputs.multi_face_landmarks:
                ratio_left = get_aspect_ratio(image, outputs, LEFT_EYE_TOP_BOTTOM, LEFT_EYE_LEFT_RIGHT)
                ratio_right = get_aspect_ratio(image, outputs, RIGHT_EYE_TOP_BOTTOM, RIGHT_EYE_LEFT_RIGHT)
                ratio = (ratio_left + ratio_right) / 2.0

                if ratio > MIN_TOLERANCE:
                    frame_count += 1
                    if eye_closed_start_time is None:
                        eye_closed_start_time = time.time()
                    elif not forward_sound_played and time.time() - eye_closed_start_time >= 2:
                        forward_sound_played = True
                        sound_forward.play(loops=-1)
                else:
                    frame_count = 0
                    forward_sound_played = False
                    sound_forward.stop()

                if frame_count > MIN_FRAME:
                    threading.Thread(target=run_speech, args=(speech, "Please wake up")).start()

            cv.imshow("Drowsiness Detection", image)
            if cv.waitKey(1) & 255 == 27:
                break

    capture.release()
    cv.destroyAllWindows()
