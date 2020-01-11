# USAGE
# python recognize_faces_video_file.py --encodings encodings.pickle --input videos/lunch_scene.mp4
# python recognize_faces_video_file.py --encodings encodings.pickle --input videos/lunch_scene.mp4 --output output/lunch_scene_output.avi --display 0

# import the necessary packages
import face_recognition
import cv2
from typing import Tuple
import argparse
import pickle
import time
import json
from cdptool import CDPInstance, configs
from pathlib import Path


# Test case event
event = 37f0be31-c075-4701-be70-a41323ea8a1a


#construct the argument parser and parse the arguments

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
                help="event id for council video")
args = vars(ap.parse_args())

# Jackson code for pulling transcript and video from database
def get_video_and_transcript_for_event_id(event_id: str) -> Tuple[Path]:
    seattle = CDPInstance(configs.SEATTLE)
    event = seattle.database.select_row_by_id("event", event_id)
    transcript = seattle.database.select_rows_as_list(
        "transcript",
        filters=[("event_id", event_id)]
    )[0]
    file = seattle.database.select_row_by_id("file", transcript["file_id"])
    transcript_save_path = seattle.file_store.download_file(file["filename"], overwrite=True)
    video_save_path = seattle.file_store._external_resource_copy(event["video_uri"], overwrite=True)
    return transcript_save_path, video_save_path

# initialize the pointer to the video file and the video writer
if not args["input"]:
    args["input"] = event
    
transcript_save_path, video_save_path = get_video_and_transcript_for_event_id(args["input"])
print(transcript_save_path)
stream = cv2.VideoCapture(video_save_path)

# close the video file pointers
stream.release()


writer = None
pass


# def frame_capture():
#     cap = cv2.VideoCapture("./council_010620_2022001V.mp4")
#     face_frame = False
#     count = 60
#     while not face_frame and count <150:
#         cap.set(1, count)
#         ret, frame = cap.read()
#         cv2.imwrite("frame.jpg", frame)
#         print(f'Frame {count} extracted')
#         count += 60
#     pass

# loop over frames from the video file stream
# 

