import logging
from converter import mp4_to_wav
from download_from_youtube import download_and_trim_video
from remove_backgroud_noise import reduce_noise
from speech_to_text import transcribe_gcs
from translate import translate_text
from utils import stereo_to_mono

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define the base URL as a global constant
YOUTUBE_BASE_URL = 'https://www.youtube.com/watch?v'


def process_video(yt_id):
    """Download a YouTube video, convert it to WAV, reduce noise, transcribe it, and translate the transcription."""
    try:
        # Download and trim the video
        logging.info(f"Downloading and trimming video {yt_id}")
        trimmed_video_name_path = download_and_trim_video(f"{YOUTUBE_BASE_URL}={yt_id}")

        # Convert the video to WAV
        logging.info("Converting video to WAV")
        wav_file_path = mp4_to_wav(trimmed_video_name_path)

        # Convert stereo audio to mono
        logging.info("Converting stereo to mono")
        stereo_to_mono(wav_file_path)

        # Reduce noise in the audio
        logging.info("Reducing noise")
        reduced_noise_path = reduce_noise(wav_file_path)

        # Transcribe the audio
        logging.info("Transcribing audio")
        speech_to_text = transcribe_gcs(reduced_noise_path)

        # Translate the transcription
        logging.info("Translating text")
        text = translate_text('en', speech_to_text)

        return text
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise


if __name__ == '__main__':
    ids = ('ClUzITJywZQ', 'zwSgRPFomaw', 'snSJrg30bU8', 'TloRPbt5C5E')
    print("Started...")
    for yt_id in ids:
        text = process_video(yt_id)