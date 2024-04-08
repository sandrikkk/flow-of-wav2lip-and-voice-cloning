import os
import logging
from dotenv import load_dotenv

from df.enhance import enhance, init_df, load_audio, save_audio

from utils import upload_to_gcs

load_dotenv()
# Set up logging
logging.basicConfig(level=logging.INFO)


def reduce_noise(input_file):
    """Reduce noise in an audio file and upload it to GCS."""
    try:
        # Initialize the deep filter
        logging.info("Initializing deep filter")
        model, df_state, _ = init_df()

        # Load the audio file
        logging.info(f"Loading audio file {input_file}")
        audio, _ = load_audio(input_file, sr=df_state.sr())

        # Enhance the audio
        logging.info("Enhancing audio")
        enhanced = enhance(model, df_state, audio)

        # Save the enhanced audio
        enhanced_folder = 'denoise_wav_files/'
        os.makedirs(enhanced_folder, exist_ok=True)
        wav_file_path = os.path.basename(input_file)
        output_file = os.path.join(enhanced_folder, f"enhanced_{wav_file_path}")
        logging.info(f"Saving enhanced audio to {output_file}")
        save_audio(output_file, enhanced, df_state.sr())

        # Upload the enhanced audio to GCS
        logging.info(f"Uploading {output_file} to GCS")
        path_of_gcs = upload_to_gcs(bucket_name=os.getenv('BUCKET_NAME'), source_file_name=output_file,
                                    sub_folder=enhanced_folder)

        return path_of_gcs
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise
