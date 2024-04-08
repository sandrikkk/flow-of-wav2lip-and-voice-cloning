import os
import logging
from moviepy.editor import VideoFileClip
from dotenv import load_dotenv

from utils import upload_to_gcs

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)


def load_video(input_file):
    """Load a video file."""
    logging.info(f"Loading video file {input_file}")
    return VideoFileClip(input_file)


def extract_audio(video_clip):
    """Extract the audio from a video clip."""
    logging.info("Extracting audio")
    return video_clip.audio


def save_audio(audio_clip, output_file):
    """Save an audio clip to a file."""
    logging.info(f"Saving audio to {output_file}")
    audio_clip.write_audiofile(output_file)


def upload_audio(bucket_name, source_file_name, sub_folder):
    """Upload an audio file to Google Cloud Storage."""
    logging.info(f"Uploading {source_file_name} to {bucket_name}/{sub_folder}")
    upload_to_gcs(bucket_name=bucket_name, source_file_name=source_file_name, sub_folder=sub_folder)


def mp4_to_wav(input_file):
    """Convert an MP4 video file to a WAV audio file and upload it to GCS."""
    try:
        # Load the video file
        video_clip = load_video(input_file)

        # Extract the audio
        audio_clip = extract_audio(video_clip)

        # Save the audio to a WAV file
        converter = 'mp4_to_wav/'
        os.makedirs(converter, exist_ok=True)
        filename_without_extension = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(converter, f"{filename_without_extension}.wav")
        save_audio(audio_clip, output_file)

        # Upload the WAV file to GCS
        upload_audio(bucket_name=os.getenv('BUCKET_NAME'), source_file_name=output_file, sub_folder=converter)

        # Close the clips
        audio_clip.close()

        return output_file
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise
