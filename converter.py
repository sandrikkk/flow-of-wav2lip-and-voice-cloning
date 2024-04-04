import os

from moviepy.editor import VideoFileClip


def mp4_to_wav(input_file):
    # Load the video file
    video_clip = VideoFileClip(input_file)

    # Extract the audio from the video
    audio_clip = video_clip.audio

    # Write the audio to a WAV file
    converter = 'mp4_to_wav/'
    os.makedirs(converter, exist_ok=True)
    filename_without_extension = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(converter, f"{filename_without_extension}.wav")
    audio_clip.write_audiofile(output_file)

    # Close the clips
    video_clip.close()
    audio_clip.close()

    return output_file
