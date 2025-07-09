# CLEARifAI

This is a thesis project to evaluate the quality of team communication in meetings using AI technologies.

Using the CLEAR Model in Modern Agile as a metric, team communication is evaluated using the following criteria:

- 7 statements of psychological safety
- 12 skills of active listening

## Evaluation Components

Team communication in meetings are evaluated only based on the audio recording. The process flowchart is shown below. 

![Process flowchart](/media/process-flowchart.png)

The steps involved are as follows:

1. Convert video meeting to audio (if needed).
2. From audio file, transcribe speech to text.
3. From audio file, identify speaker of each speech.
4. From audio file, classify emotions of each segment of speech.
5. Combine the above 3 components into a transcript with emotion labels.
6. Based on the transcript, evaluate quality of team communication using a chosen Large Language Model.
7. Generate score on each aspect of CLEAR, positive areas of team communication and recommendations for improvements.

The score on the 5 CLEAR aspects can be reflected in the CLEAR Radar Chart. An example is shown below.

![Radar Chart](/media/radar-chart.png)

## Technologies Used

- Audio conversion: [PyDub Library](https://pypi.org/project/pydub/)
- Transcription: [OpenAI Whisper](https://github.com/openai/whisper)
- Speaker Diarization: [PyAnnote](https://huggingface.co/pyannote/speaker-diarization-3.1)
- Speech Emotion Recognition: [SUPERB: Speech processing Universal PERformance Benchmark](https://huggingface.co/superb/wav2vec2-base-superb-er)
- Team Communication Evaluation: [Gemma 3 Models](https://ai.google.dev/gemma/docs/core) for open source models

## Backend

### Setting up

1. `cd backend`
2. `python3 -m venv .venv`
3. `source .venv/bin/activate`
4. `python3 -m pip install -r requirements.txt`
5. Duplicate `.env example` and rename it `.env`
6. Replace the placeholder <YOUR_HUGGING_FACE_TOKEN> and <YOUR_OPENROUTER_API_KEY> in `.env`

### Installing new packages

1. `pip install <package>`
2. `python3 -m pip freeze > requirements.txt`

### Running App

1. Run `uvicorn app.main:app --reload`
2. Navigate to `http://127.0.0.1:8000/docs`
  

## Frontend

1. `cd frontend`
2. `npm install`
3. `npm run dev`
4. Navigate to `http://localhost:5173/CLEARifAI/`

## Publishing Changes in Frontend

1. `npm run build`
2. `npm run deploy`
