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
                ref.update({key: value for key, value in data.read().items() if not key.startswith('dc-fan')})
                data.update('dc-fan-a', ref.child('dc-fan-a').get())
                data.update('dc-fan-b', ref.child('dc-fan-b').get())
                data.update('dc-fan-c', ref.child('dc-fan-c').get())
                bucket.blob('cats-output.png').upload_from_filename('out/cats-output.png')
            except Exception as err:
                print(err)
    except RuntimeError as e:
        print(f"[ERROR] Firebase Database Initialize Failed: \n{e}")
