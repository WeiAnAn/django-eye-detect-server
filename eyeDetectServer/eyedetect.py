import openface
import cv2
import numpy as np
from PIL import Image
from operator import itemgetter
from subprocess import check_output
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils


align = openface.AlignDlib("./eyeDetectServer/models/dlib/shape_predictor_68_face_landmarks.dat")


def findLandmarks(rgbImg, img):
     
    bb = align.getLargestFaceBoundingBox(rgbImg)
    if bb is not None:
        landmarks = align.findLandmarks(rgbImg, bb)
        leftEye = landmarks[36:42]
        rightEye = landmarks[42:48]
        lx,ly,lw,lh = findEyeScale(leftEye)
        rx,ry,rw,rh = findEyeScale(rightEye)

        lpupil = check_output(['./eyeDetectServer/eyeLike', "./eyeDetectServer/image/"+img, str(lx), str(ly), str(lw), str(lh)])
        rpupil = check_output(['./eyeDetectServer/eyeLike', "./eyeDetectServer/image/"+img, str(rx), str(ry), str(rw), str(rh)])
        lpupil = lpupil.split()
        rpupil = rpupil.split()
        lpupilXRatio = -1
        lpupilYRatio = -1
        rpupilXRatio = -1
        rpupilYRatio = -1

        if len(lpupil) == 2:
            lpupilXRatio = (float)(lpupil[0])/lw
            lpupilYRatio = (float)(lpupil[1])/lh

            rpupilXRatio = (float)(rpupil[0])/rw
            rpupilYRatio = (float)(rpupil[1])/rh

            lpupil = [ (int)(lpupil[0])+lx, (int)(lpupil[1])+ly]
            rpupil = [ (int)(rpupil[0])+lx, (int)(rpupil[1])+ly]

        return leftEye, rightEye, [lpupilXRatio, lpupilYRatio], [rpupilXRatio, rpupilYRatio]
    return [],[],[],[]

def findEyeScale(eye):
    minX = min(eye)[0]
    minY = min(eye,key=itemgetter(1))[1]
    maxX = max(eye)[0]
    maxY = max(eye,key=itemgetter(1))[1]
    width = maxX-minX
    height = maxY-minY
    return minX, minY, width, height

def getEAR(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])

    ear =  (2.0 * C) / (A + B)

    return ear

# def drawImg(img, eyes):
#     stream = open(img,'rb')
#     frame = np.fromfile(stream, dtype=np.uint8)
#     rgbImg = np.reshape(frame,(-1,320))
#     rgbImg = np.rot90(rgbImg,1)
#     rgbImg = rgbImg.copy()
#     for point in eyes[0]:
#         cv2.circle(rgbImg, (point[0],point[1]), 1, (255,255,255))
#     for point in eyes[1]:
#         cv2.circle(rgbImg, (point[0],point[1]), 1, (255,255,255))
#     cv2.imshow("im",rgbImg)
#     cv2.waitKey(0)

def openYUV(img):
    stream = open(img,'rb')
    frame = np.fromfile(stream, dtype=np.uint8)
    rgbImg = np.reshape(frame,(-1,320))
    rgbImg = np.rot90(rgbImg,1)
    return rgbImg

def openJPG(img):
    return cv2.imread(img)

# drawImg("pic0",findLandmarks("pic0"))
# findLandmarks("pic0")
# openYuv('pic0')