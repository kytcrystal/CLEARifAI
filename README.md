# agile-communicAItion

## Models Used

### Sentiment Analysis

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
