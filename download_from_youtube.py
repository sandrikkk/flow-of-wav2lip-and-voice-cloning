from pytube import YouTube
from moviepy.editor import VideoFileClip
import os


def download(video_url, start_time=5.2, end_time=21.25):
    # Create a YouTube object
    yt = YouTube(video_url)

    # Get the highest resolution stream
    stream = yt.streams.get_highest_resolution()

    # Download the video
    original_videos_folder = 'original_videos'
    os.makedirs(original_videos_folder, exist_ok=True)
    stream.download(output_path=original_videos_folder)

    # Load the downloaded video file
    video_path = os.path.join("original_videos/", f"{yt.title}.{stream.subtype}")
    video_clip = VideoFileClip(video_path)
    full_video_duration = video_clip.duration

    # Extract the subclip from start time to end time
    subclip = video_clip.subclip(float(start_time), float(full_video_duration - end_time))

    # Save the subclip
    trimmed_videos_folder = 'trimmed_videos'
    os.makedirs(trimmed_videos_folder, exist_ok=True)
    subclip_filename = os.path.join("trimmed_videos/", f"{yt.title}_trimmed.{stream.subtype}")
    subclip.write_videofile(subclip_filename)

    # Close the video file
    video_clip.close()

    return subclip_filename
