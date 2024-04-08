import os
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError
from pydub import AudioSegment

storage_client = storage.Client()


def upload_to_gcs(bucket_name: str, source_file_name: str, destination_blob_name: str | None = None,
                  sub_folder: str | None = None) -> str:
    try:
        bucket = storage_client.bucket(bucket_name)
        if not destination_blob_name:
            destination_blob_name = os.path.basename(source_file_name)

        if sub_folder:
            destination_blob_name = os.path.join(sub_folder, destination_blob_name)

        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)

        destination_name = f"gs://{bucket_name}/{destination_blob_name}"
        print(f"File {source_file_name} uploaded to {destination_name}.")

        return destination_name
    except GoogleCloudError as gcs_error:
        raise GoogleCloudError(f"Failed to upload to Google Cloud Storage due to: {gcs_error}") from gcs_error


def stereo_to_mono(audio_file_path):
    sound = AudioSegment.from_wav(audio_file_path)
    sound = sound.set_channels(1)
    sound.export(audio_file_path, format="wav")


