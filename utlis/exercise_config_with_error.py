# exercise_config.py
# Squat and deadlift share similar angles and keypoints

exercise_config_error = {
    "pushups": {
        "left_kpts": [5, 7, 9],  # Left arm: Shoulder, Elbow, Wrist
        "right_kpts": [6, 8, 10],  # Right arm: Shoulder, Elbow, Wrist
        "back_kpts": [6, 12, 16],  # For back straightness
        "up_angle": 130.0,  # Arm angle for "up" position
        "down_angle": 120.0,  # Arm angle for "down" position
        "back_angle_threshold": 10.0,  # Max deviation for straight back
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
        "back_kpts": [6, 12, 16],  # For back straightness
        "up_angle": 170.0,  # Leg angle for "up" position
        "down_angle": 110.0,  # Leg angle for "down" position
        "back_angle_threshold": 10.0,  # Max deviation for straight back
    },
    "squat": {
        "left_kpts": [11, 13, 15],  # Left leg
        "right_kpts": [12, 14, 16],  # Right leg
        "back_kpts": [6, 12, 16],  # For back straightness
        "up_angle": 170.0,  # Leg angle for "up" position
        "down_angle": 110.0,  # Leg angle for "down" position
        "back_angle_threshold": 10.0,  # Max deviation for straight back
    },
}
