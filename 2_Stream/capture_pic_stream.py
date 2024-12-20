import cv2, queue, threading, time
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError

stream_address = "http://192.168.100.204:8080/video"
GRID_H = 9
GRID_W = 6
FRST_P = 0
SCND_P = 8
LENGTH = 22 * (SCND_P - FRST_P + 1) # mm
FACTOR = 119.48703402948802 #None

def get_length(p1, p2):
    return np.sqrt( (p1[0]-p2[0]) ** 2 + (p1[1]-p2[1]) ** 2)

def get_side_length(gray):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    ret, corners = cv2.findChessboardCorners(gray, (GRID_H,GRID_W), None)

    if ret:
        corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        length = get_length(corners2[FRST_P][0], corners2[SCND_P][0])
        return True, length
    else:
        print("ERROR!")
        return False, None

def put_text(img, text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (1000, 500)
    fontScale = 5
    color = (255, 0, 0)
    thickness = 10
    img = cv2.putText(img, text, org, font, 
                    fontScale, color, thickness, cv2.LINE_AA)
    return img


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

    if FACTOR is not None:
        ret, length = get_side_length(gray)
        if ret:
            frame = put_text(frame, str(FACTOR*LENGTH/length))

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
