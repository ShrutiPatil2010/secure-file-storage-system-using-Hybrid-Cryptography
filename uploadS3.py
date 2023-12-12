"""

Function for uploading file to AWS s3 bucket.
Required fields -> file_name, bucket, object_name





import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

# Set the paths for Firebase configuration
service_account_key_path = 'C:\\Users\\Ajay Patil\\Desktop\\ALL FOLDERS\\HYBRIDCRYPTO\\data-storage-9e045-firebase-adminsdk-f4zec-33e33a3976.json'
firebase_bucket = 'gs://data-storage-9e045.appspot.com'

def upload_file_to_firebase(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Initialize Firebase with your credentials and project configuration
    cred = credentials.Certificate(service_account_key_path)
    firebase_admin.initialize_app(cred, {
        'storageBucket': firebase_bucket
    })

    try:
        bucket = storage.bucket()
        blob = bucket.blob(object_name)
        blob.upload_from_filename(file_name)
        response = "Uploaded Successfully!!!"
    except Exception as e:
        response = f"Failed to upload to Firebase Storage: {str(e)}"

    return response

"""