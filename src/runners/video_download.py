import bentoml
from bentoml.exceptions import BentoMLException
import yt_dlp


class VideoDownload(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("cpu",)
    SUPPORTS_CPU_MULTI_THREADING = True

    @bentoml.Runnable.method(batchable=False)
    def download_video(self, url):
        
        output_file_path = '/tmp/video_audio'

        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'outtmpl': output_file_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }]
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                video_download = ydl.download(url)
        except yt_dlp.utils.DownloadError as e:
            raise BentoMLException(f"Error downloading video: {e}")

        print("Audio Download Completed")
        path = '/tmp/video_audio.wav'
        return path