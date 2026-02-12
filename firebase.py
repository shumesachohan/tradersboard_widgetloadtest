import logging
import time
import firebase_admin
from firebase_admin import credentials, storage
from utils import get_resource_path


def initialize_firebase(json_path):
    if not firebase_admin._apps:
        cred = credentials.Certificate(json_path)
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'restapipro-9a75a.appspot.com'
        })


def upload_to_firebase(local_path="chrome_test_run.avi", storage_path="chrome_test_run.avi"):
    try:
        json_path = r"restapipro-9a75a-firebase-adminsdk-vjilg-112bc9a6c4.json"
        initialize_firebase(json_path)

        bucket = storage.bucket()
        blob = bucket.blob(storage_path)
        blob.upload_from_filename(local_path)
        blob.make_public()

        public_url = blob.public_url
        logging.info(f"✅ Uploaded '{local_path}' to Firebase at: {public_url}")
        return public_url

    except Exception as e:
        logging.error(f"❌ Firebase upload failed: {e}")
        return None


def upload_to_firebase_file(local_path="test_log.log", storage_path="test_log.log"):
    try:
        json_path =  r'restapipro-9a75a-firebase-adminsdk-vjilg-112bc9a6c4.json'
        initialize_firebase(json_path)

        bucket = storage.bucket()
        blob = bucket.blob(storage_path)
        blob.upload_from_filename(local_path)
        blob.make_public()

        public_url = blob.public_url
        logging.info(f"✅ Uploaded '{local_path}' to Firebase at: {public_url}")
        return public_url

    except Exception as e:
        logging.error(f"❌ Firebase upload failed: {e}")
        return None
    
    
    

def upload_to_firebase_missing_elements(local_path="unfound_elements\missing_elements.csv", storage_path="unfound_elements\missing_elements.csv"):
    try:
        json_path =  r'restapipro-9a75a-firebase-adminsdk-vjilg-112bc9a6c4.json'
        initialize_firebase(json_path)

        bucket = storage.bucket()
        blob = bucket.blob(storage_path)
        blob.upload_from_filename(local_path)
        blob.make_public()

        public_url = blob.public_url
        logging.info(f"✅ Uploaded '{local_path}' to Firebase at: {public_url}")
        return public_url

    except Exception as e:
        logging.error(f"❌ Firebase upload failed: {e}")
        return None

    


def upload_to_firebase_networklogs(local_path="network_logs\login_end_with_requests_and_console.json", storage_path="network_logs\login_end_with_requests_and_console.json"):
    try:
        json_path =  r'restapipro-9a75a-firebase-adminsdk-vjilg-112bc9a6c4.json'
        initialize_firebase(json_path)

        bucket = storage.bucket()
        blob = bucket.blob(storage_path)
        blob.upload_from_filename(local_path)
        blob.make_public()

        public_url = blob.public_url
        logging.info(f"✅ Uploaded '{local_path}' to Firebase at: {public_url}")
        return public_url

    except Exception as e:
        logging.error(f"❌ Firebase upload failed: {e}")
        return None




def upload_to_firebase_with_retry(local_path="chrome_test_run.avi", storage_path="chrome_test_run.avi", retries=3):
    for attempt in range(retries):
        logging.info(f"📤 Attempting to upload file (Attempt {attempt + 1})...")
        result = upload_to_firebase(local_path, storage_path)
        if result:
            return result
        else:
            logging.warning(f"⚠️ Upload failed on attempt {attempt + 1}")
            if attempt < retries - 1:
                logging.info("🔁 Retrying...")
                time.sleep(2)
    logging.error("❌ Upload failed after all retries.")
    return None