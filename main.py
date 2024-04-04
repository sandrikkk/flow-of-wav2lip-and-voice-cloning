from converter import mp4_to_wav
from download_from_youtube import download
from remove_backgroud_noise import reduce_noise

if __name__ == '__main__':
    base_link = 'https://www.youtube.com/watch?v'
    ids = ('ClUzITJywZQ', 'zwSgRPFomaw', 'snSJrg30bU8', 'TloRPbt5C5E')
    print("Started...")
    for yt_id in ids:
        trimmed_video_name_path = download(f"{base_link}={yt_id}")
        wav_file_path = mp4_to_wav(trimmed_video_name_path)
        reduce_noise(wav_file_path)
