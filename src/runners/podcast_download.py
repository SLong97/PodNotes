import requests
import os
import subprocess
import bentoml
from bentoml.exceptions import BentoMLException

class PodcastDownload(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("cpu",)
    SUPPORTS_CPU_MULTI_THREADING = True

    @bentoml.Runnable.method(batchable=False)
    def download_podcast(self, url):

        filename = '/tmp/podcast_audio'
        output_filename = '/tmp/podcast_audio.wav'

        response = requests.get(url)
        content_type = response.headers['Content-Type']

        try:
            # Save audio to file using urllib library
            if 'audio' in content_type:

                with open(filename, 'wb') as f:
                    f.write(response.content)
                    print("Audio file downloaded")

                # Use FFmpeg to convert MP3 to WAV
                subprocess.run(["ffmpeg", "-y", "-i", filename, output_filename])
                print("Audio file converted to WAV")

                os.remove(filename)

            else:
                print("URL does not contain audio file.")
        
        except:
            raise BentoMLException("Error downloading podcast audio.")

        print("Podcast Download Completed")
        return output_filename