import os

from df.enhance import enhance, init_df, load_audio, save_audio


def reduce_noise(input_file):
    model, df_state, _ = init_df()
    audio, _ = load_audio(input_file,
                          sr=df_state.sr())
    enhanced = enhance(model, df_state, audio)
    enhanced_folder = 'denoise_wav_files/'
    os.makedirs(enhanced_folder, exist_ok=True)
    wav_file_path = os.path.basename(input_file)
    output_file = os.path.join(enhanced_folder, f"enhanced_{wav_file_path}")
    save_audio(output_file, enhanced, df_state.sr())
