import os
from pyannote.audio import Pipeline
import logging
logger = logging.getLogger(__name__)

from dotenv import load_dotenv
load_dotenv()  
hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise EnvironmentError("HF_TOKEN is not set in environment variables.")



def diarize_audio(file_path, data_dir, min_speakers, max_speakers):
    try: 
    
        logger.info("starting speaker diarization")
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=hf_token)

        if min_speakers == 0 and max_speakers == 0:
            diarization = pipeline(file_path)
        else: 
            diarization = pipeline(file_path, min_speakers=min_speakers, max_speakers=max_speakers)
        
        rttm_file_path = data_dir + "/diarization.rttm"
        with open(rttm_file_path, "w") as rttm:
            diarization.write_rttm(rttm)
            
        logger.info(f"diarization saved to {rttm_file_path}")
        return rttm_file_path
    
    except Exception as e:
        logger.error(f"error during diarization: {e}")
        raise

def parse_rttm(file_path):
    segments = []

    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("SPEAKER"):
                parts = line.strip().split()
                segment = {
                    "file_id": parts[1],
                    "channel": parts[2],
                    "start_time": float(parts[3]),
                    "duration": float(parts[4]),
                    "end_time": float(parts[3]) + float(parts[4]),
                    "speaker": parts[7]
                }
                segments.append(segment)

    return segments