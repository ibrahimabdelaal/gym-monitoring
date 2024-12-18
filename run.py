import cv2
from GYM import AIGym
from utlis.exercise_config import exercise_config
from utlis.exercise_config_with_error import exercise_config_error

# Prompt the user to select an exercise
print("Select an exercise:")
print("1. Pushups")
print("2. Pullups")
print("3. Deadlift")
print("4. Squat")   #Dumbbell Bicep Curls
print("5. Dumbbell Bicep Curls") 

try:
    #flag to decide with error or not 
    wiht_error=False
    exercise_choice = int(input("Enter the number of the exercise: "))
    exercise_map = {1: "pushups", 2: "pullups", 3: "deadlift", 4: "squat" ,5:"Dumbbell Bicep Curls"}

    # Validate the choice
    if exercise_choice not in exercise_map:
        raise ValueError("Invalid choice. Please select a valid exercise number.")

    # Get the selected exercise settings
    selected_exercise = exercise_map[exercise_choice]
    
    # Ask user if they want error detection on or off
    error_detection_choice = input("Do you want to enable error detection? (y/n): ").strip().lower() == 'y'
    
    if error_detection_choice:
        settings = exercise_config_error[selected_exercise]
        wiht_error=True
    else:
        settings = exercise_config[selected_exercise]

    print("Here are the settings used for your exercise (feel free to change them in utils.exercise_config):", settings)

    # Prompt the user to select a model
    print("\nSelect a YOLO pose model:")
    print("1. Nano ")
    print("2. Small ")
    print("3. Medium ")
    print("4. Large ")

    model_choice = int(input("Enter the number of the model: "))
    model_map = {1: "weights\yolo11n-pose.pt", 2: "weights\yolo11s-pose.pt", 3: "weights\yolo11m-pose.pt", 4: "weights\yolo11l-pose.pt"}

    # Validate the model choice
    if model_choice not in model_map:
        raise ValueError("Invalid model choice. Please select a valid number.")

    # Get the selected model
    selected_model = model_map[model_choice]
    print(f"Using model: {selected_model}")

    # Prompt the user for a video file path
    video_file = input(f"Enter the path of the video for {selected_exercise} (default: 'workout/{selected_exercise}.mp4'): ")

    # If no input is provided, use the default path
    if not video_file:
        video_file = f"workout/{selected_exercise}.mp4"
        print(f"Using default video path: {video_file}")

    # Open the video file
    cap = cv2.VideoCapture(video_file)
    assert cap.isOpened(), f"Error reading video file: {video_file}"

    # Get video properties
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

    # Initialize the video writer
    output_file = f"output/{selected_exercise}_out.mp4"
    video_writer = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

    # Initialize the AIGym instance with exercise-specific settings
    gym = AIGym(
        model=selected_model,  # Pass the selected model here
        exercise=selected_exercise,
        line_width=2,
        show=True,
        left_kpts=settings["left_kpts"],
        right_kpts=settings["right_kpts"],
        conf=0.5,
        up_angle=settings["up_angle"],
        down_angle=settings["down_angle"],
        save=True,
        max_det=1,
        with_error=wiht_error
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
