from pydub import AudioSegment
import logging
logger = logging.getLogger(__name__)

def extract_audio_from_video(file_path):
    try:
        _, ext = str.split(file_path, ".")
        audio_format = "wav"
        
        if ext != audio_format:
            audio_file_path = convert_to_wav(file_path)
            logger.info(f"file converted from {ext} to {audio_format}")
            return audio_file_path
        
        logger.info(f"file already in {audio_format} format")
        return file_path
    
    except Exception as e:
        logger.error(f"error during extraction: {e}")
        raise
    
def convert_to_wav(file_path):
    try: 
        file_prefix, ext = str.split(file_path, ".")
        audio = AudioSegment.from_file(file_path, format=ext)
        wav_format = "wav"
        wav_file = file_prefix + "." + wav_format
        audio.export(wav_file, format=wav_format)
        return wav_file
    except Exception as e:
        logger.error(f"error during conversion to wav fail: {e}")
        raise
    
def split_audio(audio_file_path, segments):
    try:
        audio = AudioSegment.from_wav(audio_file_path)
        audio_chunks = []
        
        for _, seg in enumerate(segments):
            start_ms = int(seg["start"] * 1000)
            end_ms = int(seg["end"] * 1000)
            chunk = audio[start_ms:end_ms]
            
            audio_chunks.append(chunk)

        return audio_chunks
    except Exception as e:
        logger.error(f"error splitting audio: {e}")
        raise
    