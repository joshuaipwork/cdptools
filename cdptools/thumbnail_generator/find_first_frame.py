# import the necessary packages
import face_recognition
import cv2
from typing import Tuple
import argparse
import pickle
import time
import json
from cdptools import CDPInstance, configs
from pathlib import Path
from os import path

# Test case event
event = "37f0be31-c075-4701-be70-a41323ea8a1a"


# construct the argument parser and parse the arguments

# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--input", required=True,
#                 help="event id for council video")
# args = vars(ap.parse_args())
# args["input"] = event


# Jackson code for pulling transcript and video from database
def get_video_and_transcript_for_event_id(event_id: str) -> Tuple[Path]:
    seattle = CDPInstance(configs.SEATTLE)
    event = seattle.database.select_row_by_id("event", event_id)
    transcript = seattle.database.select_rows_as_list(
        "transcript",
        filters=[("event_id", event_id)]
    )[0]
    file = seattle.database.select_row_by_id("file", transcript["file_id"])
    try:
        transcript_save_path = seattle.file_store.download_file(file["filename"])
    except FileExistsError:
        transcript_save_path = file["filename"]

    try:
        video_save_path = seattle.file_store._external_resource_copy(event["video_uri"])
        video_save_path = path.absolute(video_save_path);
    except FileExistsError:
        video_save_path = event["video_uri"].split("/")[-1]

    return transcript_save_path, video_save_path


# initialize the pointer to the video file and the video writer
transcript_save_path, video_save_path = get_video_and_transcript_for_event_id(event)
print(transcript_save_path)
print(video_save_path)
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


#         while not cap.isOpened():
#                 cap = cv2.VideoCapture("video.mp4")
#                 cv2.waitKey(1000)
#                 print "Wait for the header"

# pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
#     flag, frame = cap.read()
#     if flag:
#             # The frame is ready and already captured
#             cv2.imshow('video', frame)
#             pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
#             print str(pos_frame)+" frames"
#     else:
#             # The next frame is not ready, so we try to read it again
#             cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos_frame-1)
#             print "frame is not ready"
#             # It is better to wait for a while for the next frame to be ready
#             cv2.waitKey(1000)

#     if cv2.waitKey(10) == 27:
#             break
#     if cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):
#             # If the number of captured frames is equal to the total number of frames,
#             # we stop
#             break

#         cap = cv2.VideoCapture("video.mp4")
# total_frames = cap.get(7)

# Here 7 is the prop-Id. You can find more here http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html

# After that you can set the frame number, suppose i want to extract 100th frame

# cap.set(1, 100)
# ret, frame = cap.read()
# cv2.imwrite("path_where_to_save_image", frame)
