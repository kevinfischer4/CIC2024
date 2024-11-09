import mediapipe as mp

def detectHands(frame):
    # Mediapipe Setup
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    # Hier wird die Hand erkannt
    results = pose.process(frame)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        return frame, True
    return frame, False