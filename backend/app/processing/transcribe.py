import re
import whisper
from .json_io import write_to_json
import logging
logger = logging.getLogger(__name__)
    

def transcribe_audio(file_path, data_dir, model_size="small", language="en"):
    # Transcribes audio using OpenAI Whisper in Python.

    try: 
        logger.info("starting transcription")
        model = whisper.load_model(model_size)
        result = model.transcribe(file_path, language=language)

        output_file = data_dir + "/transcript_raw.txt"

        with open(output_file, "w", encoding="utf-8") as f:
            for segment in result["segments"]:
                start_timestamp = format_timestamp(segment["start"])
                end_timestamp = format_timestamp(segment["end"])
                f.write(f"{start_timestamp} {end_timestamp} {segment['text'].strip()}\n")
        
        if result["language"] != "en":
            logger.warning(f"detected Language: {result['language']}")
            
        logger.info(f"transcription saved to {output_file}")
        return output_file
    
    except Exception as e:
        logger.error(f"error during transcription: {e}")
        raise
        
        

def format_timestamp(seconds):
    """Convert seconds to [mm:ss.xx] format."""
    minutes = int(seconds // 60)
    seconds_remainder = seconds % 60
    return f"[{minutes:02d}:{seconds_remainder:05.2f}]"


def parse_txt(file_path, data_dir):
    segments = []
    time_pattern = re.compile(r"\[(\d+:\d+\.\d+)\] \[(\d+:\d+\.\d+)\] (.+)")

    with open(file_path, "r") as f:
        for line in f:
            match = time_pattern.match(line.strip())
            if match:
                start = timestamp_to_seconds(match.group(1))
                end = timestamp_to_seconds(match.group(2))
                text = match.group(3).strip()

                segments.append({
                    "start": start,
                    "end": end,
                    "text": text
                })

    file_prefix = data_dir + "/transcript"

    return write_to_json(segments, file_prefix), segments


def timestamp_to_seconds(hhmmss):
    minutes, seconds = hhmmss.split(":")
    return int(minutes) * 60 + float(seconds)