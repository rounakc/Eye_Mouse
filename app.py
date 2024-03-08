import cv2
import mediapipe as mp
import pyautogui
import streamlit as st

# Initialize MediaPipe FaceMesh
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# Function to control mouse with eye movement
def control_mouse():
    cam = cv2.VideoCapture(0)
    screen_w, screen_h = pyautogui.size()
    while True:
        _, frame = cam.read()
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape
        if landmark_points:
            landmarks = landmark_points[0].landmark
            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0))
                if id == 1:
                    screen_x = screen_w * landmark.x
                    screen_y = screen_h * landmark.y
                    pyautogui.moveTo(screen_x, screen_y)
            left = [landmarks[145], landmarks[159]]
            for landmark in left:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 255))
            if (left[0].y - left[1].y) < 0.004:
                pyautogui.click()
                pyautogui.sleep(1)
        cv2.imshow('Eye Controlled Mouse', frame)
        # Check if any key is pressed
        key = cv2.waitKey(1) & 0xFF  # Masking to ensure compatibility with 64-bit systems
        if key != 255:  # Check if any key is pressed
            break

    # Release the camera and close OpenCV windows
    cam.release()
    cv2.destroyAllWindows()

# Streamlit UI
st.title('Eye Controlled Mouse')
st.write("Click the button below to activate eye-controlled mouse functionality.")

# Button to activate functionality
if st.button("Activate Eye Control"):
    control_mouse()
