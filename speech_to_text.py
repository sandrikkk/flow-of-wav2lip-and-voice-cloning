"""Module for batch transcribing multiple audio files using Google Cloud Speech-to-Text API V2."""

from google.cloud import speech


def transcribe_gcs(gcs_uri: str) -> str:
    """Asynchronously transcribes the audio file specified by the gcs_uri.

    Args:
        gcs_uri: The Google Cloud Storage path to an audio file.

    Returns:
        The generated transcript from the audio file provided.
    """
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="es-ES"
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=120)

    transcript_builder = []
    for result in response.results:
        # Append only the transcript text to the string
        transcript_builder.append(result.alternatives[0].transcript)

    # Join the transcripts into one long string
    transcript = " ".join(transcript_builder)
    print(transcript)

    return transcript


if __name__ == "__main__":
    # Replace 'your_project_id' with your actual project ID.
    # List your GCS URIs and specify the GCS output path for the transcribed text.
    PROJECT_ID = "ms--gcp-gpt-ai--sandbox--c746"
    LOCATION = "europe-west4"
    GCS_URI = "gs://voice-cloning-bucket/denoise_wav_files/enhanced_trimmed_Descubre cómo colocar la jarra y los accesorios de la Mambo Cooking.wav"
    OUTPUT_BUCKET = "voice-cloning-bucket"

    transcript_uri = transcribe_gcs(GCS_URI)
