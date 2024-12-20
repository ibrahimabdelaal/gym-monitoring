from solutions import BaseSolution
from utlis import Annotator  # Relative import for Annotator
from utlis.exercise_config import exercise_config
from utlis.exercise_config_with_error import exercise_config_error
import cv2
import random
class AIGym(BaseSolution):
    """
    A class to manage gym steps of people in a real-time video stream based on their poses.
    """

    def __init__(self, with_error: bool ,exercise: str = "pushups",**kwargs):
        """
        Initializes AIGym for workout monitoring using pose estimation and predefined angles.
        
        Args:
            exercise (str): The type of exercise to monitor. Default is "pushups".
        """
        if "model" in kwargs and "-pose" not in kwargs["model"]:
            kwargs["model"] = "yolo11n-pose.pt"
        elif "model" not in kwargs:
            kwargs["model"] = "yolo11n-pose.pt"
        print( 'the model used is :',kwargs["model"])
        super().__init__(**kwargs)

        # Load exercise-specific configurations
        print("**********************************exr")
        if with_error:
           print("**********************************exr")
           exr_config=exercise_config_error
        else:
            exr_config=exercise_config

        assert exercise in exr_config, f"Unknown exercise '{exercise}'. Check `exr_config.py`."
        cfg = exr_config[exercise]

        self.exercise = exercise
        self.count = []  # Repetition counts for each detected person
        self.angle = []  # Current angle of the tracked body part for each person
        self.stage = []  # Current exercise stage ('up', 'down', or '-') for each person
        self.selected_angle = {}  # Dictionary to store the selected angle for each person
        self.up_angle = cfg["up_angle"]  # Pose "up" angle threshold
        self.down_angle = cfg["down_angle"]  # Pose "down" angle threshold
        self.left_kpts = cfg["left_kpts"]  # Keypoints for the left side
        self.right_kpts = cfg["right_kpts"]  # Keypoints for the right side
        self.exr_config=exr_config
        

    def monitor(self, im0):
        """
        Monitors workouts using Ultralytics YOLO Pose Model, including error detection.

        Args:
            im0 (ndarray): Input image for processing.

        Returns:
            (ndarray): Processed image with annotations for workout monitoring.
        """
        # Extract tracks
        tracks = self.model.track(source=im0, persist=True, classes=self.CFG["classes"], **self.track_add_args)[0]

        if tracks.boxes.id is not None:
            # Initialize tracking for new detections
            if len(tracks) > len(self.count):
                new_human = len(tracks) - len(self.count)
                self.angle += [0] * new_human
                self.count += [0] * new_human
                self.stage += ["-"] * new_human

            # Initialize annotator
            self.annotator = Annotator(im0, line_width=self.line_width)

            # Process each detected person
            for ind, k in enumerate(reversed(tracks.keypoints.data)):
                left_kpts = [k[int(self.left_kpts[i])].cpu() for i in range(3)]
                right_kpts = [k[int(self.right_kpts[i])].cpu() for i in range(3)]

                # Back alignment keypoints and angle calculation
                if "back_kpts" in self.exr_config[self.exercise]:
                    print("#####################################################")

                    back_kpts = [
                        k[int(idx)].cpu() for idx in self.exr_config[self.exercise]["back_kpts"]
                    ]
                    if all(p.sum() > 0 for p in back_kpts):  # Ensure keypoints are valid
                        back_angle = self.annotator.estimate_pose_angle(*back_kpts)
                        back_angle_threshold = self.exr_config[self.exercise]["back_angle_threshold"]

                        # Check if back alignment is correct
                        if abs(180.0 - back_angle) > back_angle_threshold:
                                error_message = "Incorrect posture: Keep your back straight!"
                                # Use cv2.putText to display the error message
                                cv2.putText(
                                    im0,  # Image frame
                                    error_message,  # Text to display
                                    (50, 50),  # Position (x, y)
                                    cv2.FONT_HERSHEY_SIMPLEX,  # Font type
                                    1.0,  # Font scale
                                    (0, 0, 255),  # Color (Red for warnings)
                                    2,  # Thickness of the text
                                    cv2.LINE_AA  # Line type for smoother text
                                )


                # Calculate angles for left and right sides (if keypoints are valid)
                left_angle = (
                    self.annotator.estimate_pose_angle(*left_kpts)
                    if all(p.sum() > 0 for p in left_kpts)
                    else None
                )
                right_angle = (
                    self.annotator.estimate_pose_angle(*right_kpts)
                    if all(p.sum() > 0 for p in right_kpts)
                    else None
                )

                # Determine which side to use based on position (closer to the camera)
                if ind not in self.selected_angle:  # Select angle only once for each person
                    if left_angle and right_angle:
                        left_dist = left_kpts[1][0]  # Horizontal position of left keypoint
                        right_dist = right_kpts[1][0]  # Horizontal position of right keypoint
                        if abs(left_dist - im0.shape[1] / 2) < abs(right_dist - im0.shape[1] / 2):
                            self.selected_angle[ind] = 'right_angle'
                        else:
                            self.selected_angle[ind] = 'left_angle'
                    elif left_angle:
                        self.selected_angle[ind] = 'left_angle'
                    elif right_angle:
                        self.selected_angle[ind] = 'right_angle'
                    else:
                        self.selected_angle[ind] = 0  # No valid angles

                # After first time, stick with the selected angle
                if self.selected_angle[ind] == 'left_angle':
                    self.angle[ind] = left_angle
                else:
                    self.angle[ind] = right_angle

                # Annotate keypoints
                if left_angle:
                    im0 = self.annotator.draw_specific_points(k, self.left_kpts, radius=self.line_width * 3)
                if right_angle:
                    im0 = self.annotator.draw_specific_points(k, self.right_kpts, radius=self.line_width * 3)
                if "back_kpts" in self.exr_config[self.exercise]:
                    print("#####################################################")
    # Draw back keypoints using the annotator
                    im0 = self.annotator.draw_specific_points(k, self.exr_config[self.exercise]["back_kpts"], radius=self.line_width * 3)

                if self.selected_angle[ind] == 'left_angle':
                    right_angle = 0
                else:
                    left_angle = 0

                # Update stage and count based on thresholds
                if self.exercise=="Dumbbell Bicep Curls":
                    if self.angle[ind] > self.down_angle:
                        
                        self.stage[ind] = "down"
                    elif self.angle[ind] < self.up_angle:
                        if self.stage[ind] == "down":
                            self.count[ind] += 1
                        self.stage[ind] = "up"
                else:
                    if self.angle[ind] < self.down_angle:
                        if self.stage[ind] == "up":
                            self.count[ind] += 1
                        self.stage[ind] = "down"
                    elif self.angle[ind] > self.up_angle:
                        self.stage[ind] = "up"

                # Display angle, count, and stage
                self.annotator.plot_angle_and_count_and_stage(
                    angle_text=self.angle[ind],  # Angle text for display
                    count_text=self.count[ind],  # Repetition count
                    stage_text=self.stage[ind],  # Stage position text
                    center_kpt=k[int(self.left_kpts[1])]  # Use left center keypoint for display
                    if left_angle
                    else k[int(self.right_kpts[1])],  # Fallback to right center keypoint
                )

        self.display_output(im0)  # Display output (optional)
        return im0  # Return the processed image
