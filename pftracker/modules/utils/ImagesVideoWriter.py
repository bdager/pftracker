
# USAGE
# python ImagesVideoWriter.py  --input cam3\. --output output\cam3_seq_000029.avi --initframe 29
# python ImagesVideoWriter.py  --input cam2\. --output output\cam2_seq_000012.avi --initframe 12


"""
Created on Sun Apr 19 19:38:59 2020

@author: bessi
"""
import cv2
import argparse
from imutils import paths

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to input images file")
ap.add_argument("-o", "--output", required=True,
	help="path to output video file")
ap.add_argument("-f", "--initframe", type=int, required=True,
	help="init frame for grabing the video")
args = vars(ap.parse_args())

# grab the paths to the input images
imagePaths = sorted(list(paths.list_images(args["input"])))

# initialize output video writer
writer = None

# loop over the input images
for p in imagePaths[args["initframe"]:]:
    	frame = cv2.imread(p)
        
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
