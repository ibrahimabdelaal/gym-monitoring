import cv2
from GYM import AIGym
from utlis.exercise_config import exercise_config  # Import exercise configurations

# Prompt the user to select an exercise
print("Select an exercise:")
print("1. Pushups")
print("2. Pullups")
print("3. Deadlift")
print("4. Squat")

try:
    exercise_choice = int(input("Enter the number of the exercise: "))
    exercise_map = {1: "pushups", 2: "pullups", 3: "deadlift", 4: "squat"}

    # Validate the choice
    if exercise_choice not in exercise_map:
        raise ValueError("Invalid choice. Please select a valid exercise number.")

    # Get the selected exercise settings
    selected_exercise = exercise_map[exercise_choice]
    settings = exercise_config[selected_exercise]
    print("here is the settings",settings)

    # Open the video file (update path as needed)
    video_file = f"workout/{selected_exercise}.mp4"
    cap = cv2.VideoCapture(video_file)
    assert cap.isOpened(), f"Error reading video file: {video_file}"

    # Get video properties
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

    # Initialize the video writer
    output_file = f"output/{selected_exercise}_out.mp4"
    video_writer = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

    # Initialize the AIGym instance with exercise-specific settings
    gym = AIGym(
        exercise=selected_exercise,
        line_width=2,
        show=True,
        left_kpts=settings["left_kpts"],
        right_kpts=settings["right_kpts"],
        conf=0.3,
        up_angle=settings["up_angle"],
        down_angle=settings["down_angle"],
        save=True,
        max_det=1
    )

    # Process video frames
    while cap.isOpened():
        success, im0 = cap.read()
        if not success:
            print("Video frame is empty or video processing has been successfully completed.")
            break
        im0 = gym.monitor(im0)  # Process frame with AIGym
        video_writer.write(im0)  # Write the processed frame to output file

    # Release resources
    cap.release()
    video_writer.release()
    print(f"Processed video saved to {output_file}")

except Exception as e:
    print(f"An error occurred: {e}")
