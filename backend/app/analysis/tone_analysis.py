from transformers import pipeline
from app.processing.json_io import write_to_json
from app.processing.audio import split_audio
import tempfile
import torch
import logging
logger = logging.getLogger(__name__)
        

def analyze_tone(audio_chunks, transcript_chunks, threshold=0.1):
    
    try:
        
        # Detect available device (CUDA > CPU > fallback)
        if torch.backends.mps.is_available():
            device = -1  # Use CPU to avoid MPS limitations
        else:
            device = 0 if torch.cuda.is_available() else -1

        emotion_classifier = pipeline(
            "audio-classification", 
            model="superb/wav2vec2-base-superb-er", 
            device=device
        )
        
        results = []

        for i, chunk in enumerate(audio_chunks):
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                chunk.export(tmp.name, format="wav")
                result = emotion_classifier(tmp.name)
                results.append({
                    "start": transcript_chunks[i]['start'],
                    "end": transcript_chunks[i]['end'],
                    "tone": result[0]['label'],
                    "confidence": result[0]['score'],
                })
        return results

    except Exception as e:
        logger.error(f"error during tone analysis: {e}")
        raise


def emotion_from_tone(file_path, speaker_transcript_chunks, data_dir):
    try:
        
        logger.info("getting emotion from tone")

        chunks = split_audio(file_path, speaker_transcript_chunks)
        
        emotion_results = analyze_tone(chunks, speaker_transcript_chunks)

        file_prefix = data_dir + "/tone_analysis"
        output_file = write_to_json(emotion_results, file_prefix)
        
        return output_file, emotion_results
    
    except Exception as e:
        logger.error(f"error getting tone analysis: {e}")
        raise

