# USAGE
# python videoWriter.py --video ball_tracking_example.mp4 --output output\ball_example.avi

"""
Created on Sun Apr 19 19:38:59 2020

@author: bessi
"""
import cv2
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
	help="path to input video file")
ap.add_argument("-o", "--output", required=True,
	help="path to output video file")
args = vars(ap.parse_args())

# initialize the video stream and output video writer
print("[INFO] starting video stream...")
vs = cv2.VideoCapture(args["video"])
writer = None

# loop over frames from the video file stream
while True:
	# grab the next frame from the video file
	(grabbed, frame) = vs.read()

	# check to see if we have reached the end of the video file
	if frame is None:
		break
    
	# if we are supposed to be writing a video to disk, initialize
	# the writer
	if args["output"] is not None and writer is None:
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 30,
			(frame.shape[1], frame.shape[0]), True)

	# check to see if we should write the frame to disk
	if writer is not None:
		writer.write(frame)

	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# check to see if we need to release the video writer pointer
if writer is not None:
	writer.release()

# do a bit of cleanup
cv2.destroyAllWindows()
vs.release()