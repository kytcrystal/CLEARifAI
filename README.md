# CLEARifAI

Evaluation of effective team communication using AI technologies.

Using the CLEAR Model in Modern Agile as a metric, team communication is evaluated using the following criteria:

- 7 statements of psychological safety
- 12 skills of active listening

This project is in the early stage, starting from the simplest case of audio-based technologies. As it progresses, more technologies and fine tuning will be integrated to enhanve the evaluation results.

## Models Used

### Text Sentiment/Emotion Analysis

- Model option 1: [j-hartmann/emotion-english-distilroberta-base](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base)
- Model option 2: [bhadresh-savani/bert-base-go-emotion](https://huggingface.co/bhadresh-savani/bert-base-go-emotion)
- Model option 3: [monologg/bert-base-cased-goemotions-original](https://huggingface.co/monologg/bert-base-cased-goemotions-original)

### Tone Analysis

- Model: [superb/wav2vec2-base-superb-er](https://huggingface.co/superb/wav2vec2-base-superb-er)
- Paper: [SUPERB: Speech processing Universal PERformance Benchmark](https://arxiv.org/abs/2105.01051)
- Emotion classes: neutral, happy, sad, angry


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
  
### Running Tests

In root folder, run `PYTHONPATH=backend pytest backend/tests`


## Frontend

1. `cd frontend`
2. `npm install`
3. `npm run dev`
4. Navigate to `http://localhost:5173/CLEARifAI/`

## Publishing Changes in Frontend

1. `npm run build`
2. `npm run deploy`
