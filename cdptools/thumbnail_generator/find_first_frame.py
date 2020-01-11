# import the necessary packages
import face_recognition
import cv2
import math
from typing import Tuple
import argparse
import pickle
import time
from imageio import imread, get_writer
import json
from cdptools import CDPInstance, configs
from pathlib import Path
from os import path

# Test case event
event = "37f0be31-c075-4701-be70-a41323ea8a1a"
gif_max_frames = 20

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


def create_gif_from_pngs(images):
    writer = get_writer("thumbnail.gif")
    current_frame = 0

    for image in images:
        writer.append_data(imread(image))
        current_frame = current_frame + 1
        if current_frame > gif_max_frames:
            break

    writer.close()


# initialize the pointer to the video file and the video writer
transcript_save_path, video_save_path = get_video_and_transcript_for_event_id(event)
print(transcript_save_path)
print(video_save_path)
stream = cv2.VideoCapture(video_save_path)
writer = None
file_names = []

# Get the times to collect thumbnails from
speakerTimes = json.load(open(transcript_save_path, 'r'))

# loop over frames from the video file stream
for speaker in speakerTimes['data']:
    # stream.read returns false if it was unable to get the next frame
    # frame is a pointer to the frame,
    (grabbed, frame) = (None, None)

    # Get the middle time of the speaker's first sentence
    timestamp = speaker['data'][0]['start_time'] + speaker['data'][0]['end_time'] / 2
    print(timestamp)

    # Convert the timestamp to the frame for cv2 to capture
    fps = stream.get(cv2.CAP_PROP_FPS)
    frame = math.floor(fps * timestamp)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame)

    # Get the frame
    (grabbed, frame) = stream.read()

    # if the frame was not grabbed, then something bad has happened
    # I might throw an error here in the future
    if not grabbed:
        break

    # detect the (x, y)-coordinates of the bounding boxes
    # corresponding to each face in the input frame,
    # then, if there is only one face we want to use that as the thumbnail
    boxes = face_recognition.face_locations(frame)
    print(len(boxes))

    file_name = "./thumbnail" + str(timestamp) + ".png"
    file_names.append("./thumbnail" + str(timestamp) + ".png")
    cv2.imwrite(file_name, frame)

# close the video file pointers
stream.release()

# check to see if the video writer point needs to be released
if writer is not None:
    writer.release()

# Create a gif from this
create_gif_from_pngs(file_names)
