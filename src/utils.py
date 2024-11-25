import cv2 as cv
from scipy.spatial import distance as dis

def run_speech(speech, speech_message):
    speech.say(speech_message)
    speech.runAndWait()

def draw_landmarks(image, outputs, landmarks, color):
    height, width = image.shape[:2]
    for face in landmarks:
        point = outputs.multi_face_landmarks[0].landmark[face]
        point_scale = (int(point.x * width), int(point.y * height))
        cv.circle(image, point_scale, 1, color, 1)

def euclidean_distance(image, point1, point2):
    height, width = image.shape[:2]
    point1 = int(point1.x * width), int(point1.y * height)
    point2 = int(point2.x * width), int(point2.y * height)
    return dis.euclidean(point1, point2)

def get_aspect_ratio(image, outputs, top_bottom, left_right):
    landmarks = outputs.multi_face_landmarks[0]
    top = landmarks.landmark[top_bottom[0]]
    bottom = landmarks.landmark[top_bottom[1]]
    left = landmarks.landmark[left_right[0]]
    right = landmarks.landmark[left_right[1]]
    return euclidean_distance(image, left, right) / euclidean_distance(image, top, bottom)

