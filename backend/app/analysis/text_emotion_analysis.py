from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from app.processing.json_io import write_to_json

import logging
logger = logging.getLogger(__name__)
        

def analyze_text_emotion(chunks, threshold=0.1):
    
    try:
        
        # emotion_classifier = pipeline("text-classification", 
        #                         model = "j-hartmann/emotion-english-distilroberta-base",
        #                         # "bhadresh-savani/bert-base-go-emotion",
        #                         return_all_scores=True)
        
        
        results = []

        for chunk in chunks:
            text = chunk["text"]

            # Get emotion scores
            # emotion_scores = emotion_classifier(text[:512])[0] 
            # top_emotion = max(emotion_scores, key=lambda x: x['score'])
            # emotion = top_emotion['label']
            # confidence = top_emotion['score']
             
            emotions = get_goemotion(text)  


            results.append({
                "speaker": chunk["speaker"],
                "start": chunk["start"],
                "end": chunk["end"],
                "text": chunk["text"],
                "text_emotions": emotions
            })

        return results
    
    except Exception as e:
        logger.error(f"error during text emotion analysis: {e}")
        raise
        

def emotion_from_text(text_chunks, data_dir):
    try: 
        
        logger.info("getting emotion from text")
        
        emotion_results = analyze_text_emotion(text_chunks)

        file_prefix = data_dir + "/text_emotion"
        output_file = write_to_json(emotion_results, file_prefix)
        
        return output_file, emotion_results

    except Exception as e:
        logger.error(f"error getting text emotion analysis: {e}")
        raise


def get_goemotion(text, threshold=0.01, model_name = "monologg/bert-base-cased-goemotions-original"):
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        inputs = tokenizer(text, return_tensors="pt", truncation=True)
        with torch.no_grad():
            logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=1).numpy()[0]

        emotion_dict = {
            model.config.id2label[i]: float(probs[i])
            for i in range(len(probs)) if probs[i] >= threshold
        }

        # Sort by confidence
        sorted_emotions = sorted(emotion_dict.items(), key=lambda x: x[1], reverse=True)
        return sorted_emotions
    except Exception as e:
        logger.error(f"error during goemotion analysis: {e}")
        raise