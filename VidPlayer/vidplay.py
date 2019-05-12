import cv2, numpy as np
import sys
from time import sleep
from gettime import Time

def flick(x):
    pass

cv2.namedWindow('image')
cv2.moveWindow('image', 150, 250)
#cv2.namedWindow('controls')
#cv2.moveWindow('controls',250,50)

#controls = np.zeros((50,750),np.uint8)
#cv2.putText(controls, "W/w: Play, S/s: Stay, A/a: Prev, D/d: Next, E/e: Fast, Q/q: Slow, Esc: Exit", (40,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

video = sys.argv[1]
cap = cv2.VideoCapture(video)

tots = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = int(cap.get(cv2.CAP_PROP_FPS))
i = 0
step=1
cv2.createTrackbar('S','image', 0,int(tots)-1, flick)
cv2.setTrackbarPos('S','image',10)

cv2.createTrackbar('Speed','image', 1, 100, flick)
frame_rate = fps
cv2.setTrackbarPos('Speed','image',1 )

def process(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

status = 'stay'

clock = Time()

thiscfr = 0

print(fps)

while True:
  #cv2.imshow("controls",controls)
  try:
    if i==tots-1:
      i=0
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, im = cap.read()
    r = 750.0 / im.shape[1]
    dim = (750, int(im.shape[0] * r))
    im = cv2.resize(im, dim, interpolation = cv2.INTER_AREA)
    if im.shape[0]>600:
        im = cv2.resize(im, (500,500))
        controls = cv2.resize(controls, (im.shape[1],25))
    #cv2.putText(im, status, )
    timelist = clock.get_time(i, fps)
    thlist = clock.get_time(thiscfr, fps)
    time = "{}:{}:{}:{}".format(timelist[0], timelist[1], timelist[2], timelist[3])
    thtime = "{}:{}:{}:{}".format(thlist[0], thlist[1], thlist[2], thlist[3])
    cv2.putText(im, time, (250, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255))
    cv2.putText(im, time, (253, 53), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))
    cv2.putText(im, thtime, (250, 80), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255))
    cv2.putText(im, thtime, (253, 83), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))
    cv2.imshow('image', im)
    status = { ord('s'):'stay', ord('S'):'stay',
                ord('w'):'play', ord('W'):'play',
                ord('a'):'prev_frame', ord('A'):'prev_frame',
                ord('d'):'next_frame', ord('D'):'next_frame',
                ord('q'):'slow', ord('Q'):'slow',
                ord('e'):'fast', ord('E'):'fast',
                ord('r'):'restart', ord('R'):'restart',
                ord('c'):'snap', ord('C'):'snap',
                -1: status,
                27: 'exit'}[cv2.waitKey(1)]


    if status == 'play':
      frame_rate = cv2.getTrackbarPos('F','image')
      #sleep((0.1-frame_rate/1000.0)**21021)
      i+=step
      thiscfr+=step
      cv2.setTrackbarPos('S','image',i)
      continue
    if status == 'stay':
      i = cv2.getTrackbarPos('S','image')
    if status == 'exit':
        break
    if status=='prev_frame':
        i-=1
        thiscfr-=1
        cv2.setTrackbarPos('S','image',i)
        status='stay'
    if status=='next_frame':
        i+=1
        thiscfr+=1
        cv2.setTrackbarPos('S','image',i)
        status='stay'
    if status=='slow':
        step = max(1, step - 1)
        frame_rate = step * 10
        cv2.setTrackbarPos('Speed', 'image', frame_rate)
        status='play'
    if status=='fast':
        step = min(10, step + 1)
        frame_rate = step * 10
        cv2.setTrackbarPos('Speed', 'image', frame_rate)
        status='play'
    if status=='snap':
        cv2.imwrite("./"+"Snap_"+str(i)+".jpg",im)
        print("Snap of Frame",i,"Taken!")
        status='stay'
    if status=='restart':
        thiscfr = 0

  except KeyError:
      print("Invalid Key was pressed")


cv2.destroyAllWindows()
cv2.waitKey(1)
