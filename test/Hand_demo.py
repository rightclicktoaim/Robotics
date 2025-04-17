import cv2
# STEP 1: Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green

def draw_landmarks_on_image(rgb_image, detection_result):
  hand_landmarks_list = detection_result.hand_landmarks
  handedness_list = detection_result.handedness
  annotated_image = np.copy(rgb_image)
  right_fingers_count = 0
  left_fingers_count = 0

  # Loop through the detected hands to visualize.
  for idx in range(len(hand_landmarks_list)):
    hand_landmarks = hand_landmarks_list[idx]
    handedness = handedness_list[idx]

    # Draw the hand landmarks.
    hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    hand_landmarks_proto.landmark.extend([landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks])
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      hand_landmarks_proto,
      solutions.hands.HAND_CONNECTIONS,
      solutions.drawing_styles.get_default_hand_landmarks_style(),
      solutions.drawing_styles.get_default_hand_connections_style())

    # Get the top left corner of the detected hand's bounding box.
    height, width, _ = annotated_image.shape
    x_coordinates = [landmark.x for landmark in hand_landmarks]
    y_coordinates = [landmark.y for landmark in hand_landmarks]
    text_x = int(min(x_coordinates) * width)
    text_y = int(min(y_coordinates) * height) - MARGIN

    # Determine how many fingers are up for left hand
    if handedness[0].category_name == "Left":
      if x_coordinates[4] < x_coordinates[3]:
        left_fingers_count += 1
      if y_coordinates[8] < y_coordinates[6]:
        left_fingers_count += 1
      if y_coordinates[12] < y_coordinates[10]:
        left_fingers_count += 1
      if y_coordinates[16] < y_coordinates[14]:
        left_fingers_count += 1
      if y_coordinates[20] < y_coordinates[18]:
        left_fingers_count += 1

      # Draw caption (left handedness and finger count)
      cv2.putText(annotated_image, f"{left_fingers_count} Left Fingers",
                (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

    # Determine how many fingers are up for right hand
    if handedness[0].category_name == "Right":
      if x_coordinates[4] > x_coordinates[3]:
        right_fingers_count += 1
      if y_coordinates[8] < y_coordinates[6]:
        right_fingers_count += 1
      if y_coordinates[12] < y_coordinates[10]:
        right_fingers_count += 1
      if y_coordinates[16] < y_coordinates[14]:
        right_fingers_count += 1
      if y_coordinates[20] < y_coordinates[18]:
        right_fingers_count += 1

      # Draw caption (right handedness and finger count)
      cv2.putText(annotated_image, f"{right_fingers_count} Right Fingers",
                (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

  return annotated_image


def main():
    capture = cv2.VideoCapture(0)
    # STEP 2: Create an HandLandmarker object.
    base_options = python.BaseOptions(model_asset_path='models/hand_landmarker.task')
    options = vision.HandLandmarkerOptions(base_options=base_options,
                                           num_hands=2)
    detector = vision.HandLandmarker.create_from_options(options)

    while (capture.isOpened()):

        success, image = capture.read()
        if(success):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
            result = detector.detect(mp_image)

            anotated_image = draw_landmarks_on_image(image, result)

            cv2.imshow('Hand Landmarks', cv2.cvtColor(anotated_image, cv2.COLOR_BGR2RGB))

        if cv2.waitKey(1) == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()