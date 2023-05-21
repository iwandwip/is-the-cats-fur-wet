import serial
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
from modules.utils import *
from modules.image import Vision
from modules.filters import KalmanFilter
from modules.routine import ImgBuster as Yolo

# constant macros
CAT_FUR_WET = '0'
CAT_FUR_DRY = '1'

DETECT_TIME = 50
SEND_TIME = 1000
RECEIVER_TIME = 1000
FB_TIME = 4000

if __name__ == "__main__":
    cam = Vision(isUsingCam=False, addr="core/wet-cat.mp4")
    pr = Yolo()
    pr.load("assets/class/cats.txt", "assets/data/best.pt")

    coms = serial.Serial('COM6', 9600, timeout=1)
    coms.reset_input_buffer()
    taskTimer = [0, 0, 0, 0, 0]
    catCondition = CAT_FUR_WET

    cred = credentials.Certificate('firebase-sdk.json')
    firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://is-the-cats-fur-wet-default-rtdb.firebaseio.com/'
    })
    ref = db.reference('/')
    nanoData = ['0', '0', '0', '0']
    fbData = ['0', '0', '0', '0']

    try:
        while True:
            frame = cam.read(480, True)
            if (Ticks() - taskTimer[0] >= DETECT_TIME): # detection
                detect = pr.predict(frame)
                for i, detect_info in enumerate(detect):
                    if detect[i]['class'] == 'kucing_basah':
                        catCondition = CAT_FUR_WET
                    elif detect[i]['class'] == 'kucing_kering':
                        catCondition = CAT_FUR_DRY
                taskTimer[0] = Ticks()
            if (Ticks() - taskTimer[1] >= SEND_TIME): # send to nano
                if catCondition:
                    coms.write(b"1\n")
                else:
                    coms.write(b"0\n")
                taskTimer[1] = Ticks()
            if (Ticks() - taskTimer[2] >= RECEIVER_TIME): # receive from nano
                if coms.in_waiting > 0:
                    nanoData = coms.readline().decode('utf-8', 'ignore').strip().split()
                    nanoData = [value.replace('C', '') for value in nanoData]
                    coms.reset_input_buffer()
                taskTimer[2] = Ticks()
            if (Ticks() - taskTimer[3] >= FB_TIME): # send to firebase
                if nanoData:
                    ref.set({
                        'temperature' : nanoData[0],
                        'humidity' : nanoData[1],
                        'distance' : nanoData[2],
                        'cat-condition' : str(catCondition)
                    })
                taskTimer[3] = Ticks()
            if (Ticks() - taskTimer[4] >= FB_TIME): # get from firebase
                fbData[0] = ref.child('temperature').get()
                fbData[1] = ref.child('humidity').get()
                fbData[2] = ref.child('distance').get()
                fbData[3] = ref.child('cat-condition').get()
                print(fbData)
                taskTimer[4] = Ticks()
            pr.draw(frame, detect) # frame debuging
            cam.show(frame, "frame")
            if cam.wait(1) == ord('q'):
                break
        cam.release()
        cam.destroy()
    except RuntimeError:
        pass
