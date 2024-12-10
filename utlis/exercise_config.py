# exercise_config.py
# squat ,deadlift almost the same angles (of course the same keypoints)

exercise_config = {
    "pushups": {
        "left_kpts": [5, 7, 9],  # Left arm: Shoulder, Elbow, Wrist
        "right_kpts": [6, 8, 10],  # Right arm: Shoulder, Elbow, Wrist
        "up_angle": 130.0,
        "down_angle": 120.0,
    },
    "pullups": {
        "left_kpts": [5, 7, 9],  # Left arm
        "right_kpts": [6, 8, 10],  # Right arm
        "up_angle": 140.0,
        "down_angle": 80.0,
    },
    "deadlift": {
        "left_kpts": [11, 13, 15],  # Left leg: Hip, Knee, Ankle
        "right_kpts": [12, 14, 16],  # Right leg: Hip, Knee, Ankle
        "up_angle": 170.0,
        "down_angle": 110.0,
    },
    "squat": {
        "left_kpts": [11, 13, 15],  # Left leg
        "right_kpts": [12, 14, 16],  # Right leg
        "up_angle": 170.0,
        "down_angle":110.0,
    },
}


