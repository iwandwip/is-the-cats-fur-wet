import firebase_admin
from utility.data import YAMLDataHandler
from firebase_admin import db, credentials, storage

if __name__ == "__main__":
    print("[INFO] Firebase Database Initialize")
    data = YAMLDataHandler("out/cats-output-data.yaml")
    cred = credentials.Certificate('cats-firebase-sdk.json')  # firebase configuration
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://is-the-cats-fur-wet-default-rtdb.firebaseio.com/',
        'storageBucket': 'is-the-cats-fur-wet.appspot.com'
    })
    bucket = storage.bucket()
    ref = db.reference('/')
    try:
        while True:
            try:
                dc_fan = [ref.child('dc-fan-a').get(),
                          ref.child('dc-fan-b').get(),
                          ref.child('dc-fan-c').get(),
                          ref.child('dc-fan-d').get()]
                ref.update({key: value for key, value in data.read().items() if not key.startswith('dc-fan')})
                data.update('dc-fan-a', dc_fan[0])
                data.update('dc-fan-b', dc_fan[1])
                data.update('dc-fan-c', dc_fan[2])
                data.update('dc-fan-d', dc_fan[3])
                bucket.blob('cats-output.png').upload_from_filename('out/cats-output.png')
                print(f"[INFO] FanA: {dc_fan[0]} | FanB: {dc_fan[1]} | FanC: {dc_fan[2]} | FanD: {dc_fan[3]} ")
            except Exception as err:
                print(err)
    except RuntimeError as e:
        print(f"[ERROR] Firebase Database Initialize Failed: \n{e}")
