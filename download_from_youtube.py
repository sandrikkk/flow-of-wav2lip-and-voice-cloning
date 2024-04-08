import os
import logging
from pytube import YouTube
from moviepy.editor import VideoFileClip

from utils import upload_to_gcs

# Set up logging
logging.basicConfig(level=logging.INFO)


def download_video(video_url, output_path):
    """Download a video from a URL using pytube."""
    logging.info(f"Downloading video from {video_url}")
    yt = YouTube(video_url)
    stream = yt.streams.get_highest_resolution()
    stream.download(output_path=output_path)
    return os.path.join(output_path, f"{yt.title}.{stream.subtype}")


def extract_subclip(video_path, start_time, end_time):
    """Extract a subclip from a video."""
    logging.info(f"Extracting subclip from {video_path}")
    video_clip = VideoFileClip(video_path)
    subclip = video_clip.subclip(start_time, end_time)
    return subclip


def save_subclip(subclip, output_path):
    """Save a subclip to a file."""
    logging.info(f"Saving subclip to {output_path}")
    subclip.write_videofile(output_path)


def upload_video(bucket_name, source_file_name, sub_folder):
    """Upload a video to Google Cloud Storage."""
    logging.info(f"Uploading {source_file_name} to {bucket_name}/{sub_folder}")
    upload_to_gcs(bucket_name=bucket_name, source_file_name=source_file_name, sub_folder=sub_folder)


def download_and_trim_video(video_url, start_time=5.2, end_time=21):
    """Download a video, extract a subclip, and upload both to GCS."""
    try:
        # Download the video
        original_videos_folder = 'original_videos/'
        os.makedirs(original_videos_folder, exist_ok=True)
        video_path = download_video(video_url, original_videos_folder)

        # Upload the original video to GCS
        upload_video(bucket_name=os.getenv('BUCKET_NAME'), source_file_name=video_path,
                     sub_folder=original_videos_folder)

        # Load the downloaded video file
        video_clip = VideoFileClip(video_path)
        full_video_duration = video_clip.duration

        # Extract the subclip
        subclip = extract_subclip(video_path, float(start_time), float(full_video_duration - end_time))

        # Save the subclip
        trimmed_videos_folder = 'trimmed_videos/'
        os.makedirs(trimmed_videos_folder, exist_ok=True)
        subclip_filename = os.path.join(trimmed_videos_folder, f"trimmed_{os.path.basename(video_path)}")
        save_subclip(subclip, subclip_filename)

        # Upload the trimmed video to GCS
        upload_video(bucket_name=os.getenv('BUCKET_NAME'), source_file_name=subclip_filename,
                     sub_folder=trimmed_videos_folder)

        # Close the video file
        video_clip.close()

        return subclip_filename
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise
