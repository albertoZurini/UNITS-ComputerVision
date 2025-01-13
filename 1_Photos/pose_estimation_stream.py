import cv2, queue, threading, time
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError

stream_address = "http://192.168.1.203:8081/video"
GRID_H = 9
GRID_W = 6
FRST_P = 0
SCND_P = 8
LENGTH = 22 * (SCND_P - FRST_P + 1) # mm

def draw(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1,2)
    # draw ground floor in green
    img = cv2.drawContours(img, [imgpts[:4]],-1,(0,255,0),15)
    # draw pillars in blue color
    for i,j in zip(range(4),range(4,8)):
        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),5)
    # draw top layer in red color
    img = cv2.drawContours(img, [imgpts[4:]],-1,(0,0,255),15)
    return img

axis = np.float32([[0,0,0], [0,3,0], [3,3,0], [3,0,0],
                   [0,0,-3],[0,3,-3],[3,3,-3],[3,0,-3] ])

def put_text(img, text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (1000, 500)
    fontScale = 5
    color = (255, 0, 0)
    thickness = 10
    img = cv2.putText(img, text, org, font, 
                    fontScale, color, thickness, cv2.LINE_AA)
    return img

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((GRID_H*GRID_W,3), np.float32)
objp[:,:2] = np.mgrid[0:GRID_H,0:GRID_W].T.reshape(-1,2)
def draw_cube(frame):
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (GRID_H,GRID_W),None)
    if ret == True:
        corners2 = cv2.cornerSubPix(gray,corners,(22,22),(-1,-1),criteria)
        cv2.drawChessboardCorners(frame, (GRID_H,GRID_W), corners2, ret)
        # Find the rotation and translation vectors.
        # ret,rvecs, tvecs = cv2.solvePnP(objp, corners2, mtx, dist)
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera([objp], [corners2], gray.shape[::-1], None, None)
        # project 3D points to image plane
        imgpts, jac = cv2.projectPoints(axis, rvecs[0], tvecs[0], mtx, dist)
        frame = draw(frame,corners2,imgpts)
    return frame

class VideoCapture:

  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    return True, self.q.get()

cap = VideoCapture(stream_address)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
 
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frame = draw_cube(frame)

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('c'):
        #filename = f"photos/{time.time()}.jpg"
        #print("saving image", filename)
        #cv2.imwrite(filename, frame)
        dst = input("Enter distance")

        ret, length = get_side_length(gray)
        if ret:
            FACTOR = int(dst) * length / LENGTH
            print("Calculated factor:", FACTOR)


 
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
