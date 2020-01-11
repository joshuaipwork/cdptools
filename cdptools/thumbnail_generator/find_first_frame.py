# USAGE
# python recognize_faces_video_file.py --encodings encodings.pickle --input videos/lunch_scene.mp4
# python recognize_faces_video_file.py --encodings encodings.pickle --input videos/lunch_scene.mp4 --output output/lunch_scene_output.avi --display 0

# import the necessary packages
import face_recognition
import cv2
import argparse
import pickle
import time

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
                help="path to input video")
args = vars(ap.parse_args())

# initialize the pointer to the video file and the video writer
print("[INFO] processing video...")
stream = cv2.VideoCapture(args["input"])
writer = None

# loop over frames from the video file stream
while True:
    # stream.read returns false if it was unable to get the next frame
    # frame is a pointer to the frame,
    (grabbed, frame) = (None, None)

    for i in range(30):
        (grabbed, frame) = stream.read()

    # if the frame was not grabbed, then we have reached the
    # end of the stream
    if not grabbed:
        break

    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input frame,
    # then, if there is only one face we want to use that as the thumbnail
    boxes = face_recognition.face_locations(frame, model=args["detection_method"])
    print(len(boxes))

    if len(boxes) == 1:
        cv2.imwrite("./thumbnail.png", frame)

        break

# close the video file pointers
stream.release()

# check to see if the video writer point needs to be released
if writer is not None:
    writer.release()
