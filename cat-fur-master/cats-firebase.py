import firebase_admin
from utility.data import YAMLDataHandler
from firebase_admin import db, credentials, storage

if __name__ == "__main__":
    data = YAMLDataHandler("out/output.yaml")
    cred = credentials.Certificate('cats-firebase-sdk.json')  # firebase configuration
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://is-the-cats-fur-wet-default-rtdb.firebaseio.com/',
        'storageBucket': 'is-the-cats-fur-wet.appspot.com'
    })
    bucket = storage.bucket()
    ref = db.reference('/')
    print("[INFO] Firebase Database Initialize")
    try:
        while True:
            ref.set(data.read())
            firebaseData = [ref.child('temperature').get(), ref.child('humidity').get(), ref.child('condition').get()]
            photoPath = 'out/output.png'
            blob = bucket.blob('output.png')
            blob.upload_from_filename(photoPath)
    except RuntimeError as e:
        pass
