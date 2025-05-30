from transformers import pipeline
from app.processing.json_io import write_to_json
from textblob import TextBlob
from flair.data import Sentence
from flair.nn import Classifier

import logging
logger = logging.getLogger(__name__)
        

def analyze_text_sentiment(chunks, threshold=0.1):
    
    try:
        
        results = []

        for chunk in chunks:
            text = chunk["text"]

            # value, score = textblob_analysis(text)
            value, score = flair_analysis(text)

            results.append({
                "speaker": chunk["speaker"],
                "start": chunk["start"],
                "end": chunk["end"],
                "text": chunk["text"],
                "text_sentiment": value,
                "confidence": score
            })

        return results
    
    except Exception as e:
        logger.error(f"error during text sentiment analysis: {e}")
        raise

def textblob_analysis(text):
    blob = TextBlob(text[:512])
    text_sentiment = blob.sentiment
    return text_sentiment.polarity, text_sentiment.subjectivity
 
def flair_analysis(text):
    tagger = Classifier.load('sentiment')
    chunk = Sentence(text)
    tagger.predict(chunk)
    return chunk.labels[0].value, chunk.labels[0].score

def sentiment_from_text(text_chunks, data_dir):
    try: 
        
        logger.info("getting sentiment from text")
        
        emotion_results = analyze_text_sentiment(text_chunks)

        file_prefix = data_dir + "/text_sentiment"
        output_file = write_to_json(emotion_results, file_prefix)
        
        return output_file, emotion_results

    except Exception as e:
        logger.error(f"error getting text sentiment analysis: {e}")
        raise
