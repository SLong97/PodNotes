import io
import asyncio
import os
import subprocess
import bentoml
from bentoml.exceptions import BentoMLException
from bentoml.io import JSON, File
from runners.video_download import VideoDownload
from runners.podcast_download import PodcastDownload
from runners.transcribe_diarize import TranscribeDiarize
from runners.dialogue_summarize import DialogueSummarize


runner_video_download = bentoml.Runner(
    VideoDownload,
    name="video_download",
)
runner_podcast_download = bentoml.Runner(
    PodcastDownload,
    name="podcast_download",
)
runner_transcribe_diarize = bentoml.Runner(
    TranscribeDiarize,
    name="transcribe_diarize",
)
runner_dialogue_summarize = bentoml.Runner(
    DialogueSummarize,
    name="summarize_dialogue"
)

svc = bentoml.Service(
    "pod_notes_pipeline",
    runners=[
        runner_video_download,
        runner_podcast_download,
        runner_transcribe_diarize,
        runner_dialogue_summarize,
    ],
)


async def generate_dialogue_summary(text):
    metadata = await asyncio.gather(
        runner_dialogue_summarize.summarize_dialogue.async_run(text),
    )
    return metadata

async def diarization_alignment(dict):

    # aligned_dict = {}
        
    # for seg, spk, sent in dict:
    #     key = f'{seg.start:.2f}-{seg.end:.2f}, {spk}' #to seperate timestamp from speaker, strip ',' do the same with '-' for start/stop times.
    #     value = sent
    #     aligned_dict[key] = value

    conversation_str = ""
    for seg, spk, sent in dict:
        speaker = spk
        sentence = f"{speaker}: {sent}"
        conversation_str += sentence
    
    return conversation_str


@svc.api(input=JSON(), output=JSON())
async def process_video_audio(input_data):

    url = input_data.get("url", None)

    path = await runner_video_download.download_video.async_run(url)
    transcript, diarized_transcript = await asyncio.wait_for(runner_transcribe_diarize.transcribe_diarize.async_run(path), timeout=3600)
    
    transcript_text = transcript["text"]
    transcript_diarized = await diarization_alignment(diarized_transcript) 
    summary_text = await generate_dialogue_summary(transcript_text)
    #summary_text = await generate_summary(transcript_text)

    output = {}
    output["transcript"] = transcript_text
    output["diarization"] = transcript_diarized
    output["summary"] = summary_text

    return output

@svc.api(input=JSON(), output=JSON())
async def process_url_audio(input_data):

    url = input_data.get("url", None)

    path = await runner_podcast_download.download_podcast.async_run(url)
    transcript, diarized_transcript = await asyncio.wait_for(runner_transcribe_diarize.transcribe_diarize.async_run(path), timeout=3600)
    
    transcript_text = transcript["text"]
    transcript_diarized = await diarization_alignment(diarized_transcript) 
    summary_text = await generate_dialogue_summary(transcript_text)
    #summary_text = await generate_summary(transcript_text)

    output = {}
    output["transcript"] = transcript_text
    output["diarization"] = transcript_diarized
    output["summary"] = summary_text

    return output

@svc.api(input=File(), output=JSON())
async def process_uploaded_audio(input_file: io.BytesIO):

    path = f"/tmp/uploaded_audio"
    output_filename = '/tmp/podcast_audio.wav'

    try:

        with open(path, 'wb') as f:
            f.write(input_file.read())
            print("Audio file uploaded")

        # Use FFmpeg to convert MP3 to WAV
        subprocess.run(["ffmpeg", "-y", "-i", path, output_filename])
        print("Audio file converted to WAV")
    
    except:
            raise BentoMLException("Error uploading audio file.")

    transcript, diarized_transcript = await asyncio.wait_for(runner_transcribe_diarize.transcribe_diarize.async_run(output_filename), timeout=3600)
    
    transcript_text = transcript["text"]
    transcript_diarized = await diarization_alignment(diarized_transcript)
    summary_text = await generate_dialogue_summary(transcript_text)
    #summary_text = await generate_summary(transcript_text)

    output = {}
    output["transcript"] = transcript_text
    output["diarization"] = transcript_diarized
    output["summary"] = summary_text

    return output