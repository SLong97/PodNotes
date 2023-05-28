# PodNotes

Podcasts are a popular and convenient way for people to access information and entertainment. However, their audio-only format can make them difficult for listeners to fully absorb and retain. 
To address these challenges, my research aimed to develop a system that uses automatic speech recognition (ASR) and natural language processing (NLP) to create transcripts and summaries of podcasts. 
By providing a written version of the audio content, listeners would be able to refer back to specific points in the podcast and more easily retain the information presented.

## Main Objectives

The Objective of this project was to create an application that makes the consumption of podcasts more accessible for the user. 

This was to be achieved through the use of automatic speech recognition technology that when provided an audio file can generate an accurate transcription that would then undergo summarization and diarization and be available for saving, exporting, and editing via a friendly easy to use interface.

### 1. Automatic Speech Recognition
### 2. Summarization
### 3. Diarization
### 4. Useability

## Tools & Technologies Used

PodNotes was built using Streamlit and deployed on a GPU-powered AWS EC2 instance, integrating a transcription (Whisper), summarization (BART), and diarization (Pyannote) API through BentoML. This architecture facilitates GPU-based processing, accessibility, scalability, platform independence, and easier updates. The storage strategy used was an AWS S3 Bucket, providing better scalability and reliability. AWS Cognito was introduced for secure user authentication, allowing users to easily manage their podcast transcriptions and summaries. This strategy resulted in an efficient, secure, and user-friendly ASR system that aligned closely with project's objectives from the research phase.

![Blank board](https://github.com/SLong97/PodNotes/assets/91565384/5d3d65dc-1ea5-4eff-90b4-8344fb221b54)
