from fastapi import APIRouter, UploadFile, BackgroundTasks, HTTPException, Query
from uuid import uuid4
from .processing.audio import extract_audio_from_video
from .processing.transcribe import transcribe_audio, parse_txt
from .processing.diarize import diarize_audio, parse_rttm
from .processing.merging import merge_transcript_speaker_segments_to_json, assign_speakers_to_transcript_to_json, merge_transcript_with_tone_to_json
from .analysis.text_emotion_analysis import emotion_from_text
from .analysis.tone_analysis import emotion_from_tone
from .analysis.text_sentiment_analysis import sentiment_from_text
from .evaluate.create_prompt import create_prompt
from .evaluate.create_multi_turn_prompt import create_multi_turn_prompt
from .evaluate.prompt_llm import evaluate_communication_with_prompt
from .evaluate.prompt_local_llm import evaluate_communication_with_prompt_os
from .utils.file_manager import JobFileManager
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
manager = JobFileManager()
results = {}
evaluate_with_LLM = True  # change this flag to False if not evaluating 

@router.post("/upload")
async def upload_video(file: UploadFile):
    try:
        job_id = str(uuid4())
        results[job_id] = {"status": "processing"}
        file_path = manager.save_uploaded_file(file, job_id)
        process_file(file_path, job_id)
        return {"job_id": job_id}
    except Exception as e:
        logger.error(f"error: {e}")
        raise


def process_file(path: str, job_id: str):
    try:
        logger.info(path)
        data_dir = "data/" + job_id
        
        audio_path = extract_audio_from_video(path)

        results[job_id] = {
            "status": "uploaded",
            "video_file": path,
            "audio_file": audio_path,
            "folder": data_dir,
        }
        
    except Exception as e:
        results[job_id] = {"status": "error", "error": str(e)}
        raise

@router.post("/load/{job_id}")
async def load(job_id: str):
    try:
        job = results.get(job_id)
        if not job:
            return check_job_exists_and_load_job(job_id)                
        else:
            raise HTTPException(status_code=404, detail="Job ID not found.")
    except Exception as e:
        logger.error(f"error: {e}")
        raise

def check_job_exists_and_load_job(job_id):
    manager.folder_exists(job_id)
    if manager.folder_exists(job_id):
        results[job_id] = manager.load_job_data(job_id)
        return {"loaded": list(results[job_id].keys())}
    else: 
        raise HTTPException(status_code=404, detail="here Job ID not found.")


@router.post("/transcribe/{job_id}")
def transcribe(job_id: str):
    job = results.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID not found.")
    if "transcript" not in job:
        step_transcribe(job)
    return {"transcript": job["transcript"]}


@router.post("/diarize/{job_id}")
def diarize(job_id: str, min_speakers: int = Query(0), max_speakers: int = Query(0)):
    job = results.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID not found.")
    if "speakers" not in job:
        step_diarize(min_speakers, max_speakers, job)
    return {"speakers": job["speakers"]}


@router.post("/speaker_transcript/{job_id}")
def speaker_transcript(
    job_id: str, min_speakers: int = Query(0), max_speakers: int = Query(0)
):
    job = results.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID not found.")

    if "speaker_transcript" not in job:
        step_speaker_transcript(min_speakers, max_speakers, job)

    return {"speaker_transcript": job["speaker_transcript"]}


@router.post("/text_emotion_analysis/{job_id}")
def text_emotion_analysis(job_id: str, min_speakers: int = Query(0), max_speakers: int = Query(0)):
    job = results.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID not found.")
    
    if "text_emotion_analysis" not in job:
        step_text_emotion_analysis(min_speakers, max_speakers, job)
        
    return {
        "text_emotion_analysis": job["text_emotion_analysis"]
    }
    

@router.post("/sentiment_analysis/{job_id}")
def sentiment_analysis(job_id: str, min_speakers: int = Query(0), max_speakers: int = Query(0)):
    job = results.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID not found.")
    
    if "sentiment_analysis" not in job:
        step_sentiment_analysis(min_speakers, max_speakers, job)
        
    return {
        "sentiment_analysis": job["sentiment_analysis"]
    }
    
@router.post("/tone_analysis/{job_id}")
def tone_analysis(job_id: str, min_speakers: int = Query(0), max_speakers: int = Query(0)):
    job = results.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID not found.")
    
    if "tone_analysis" not in job:
        step_tone_analysis(min_speakers, max_speakers, job)
        
    return {
        "tone_analysis": job["tone_analysis"]
    }
    
@router.post("/evaluate_communication/{job_id}")
def evaluation_communication(job_id: str, min_speakers: int = Query(0), max_speakers: int = Query(0), model: str = "deepseek-chat:free"):
    job = results.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job ID not found.")
    
    if not evaluate_with_LLM:
        text = '''
        ```json
        {
        "C": 0.7,
        "L": 0.5,
        "E": 0.8,
        "A": 0.6,
        "R": 0.6
        }
        ```
        '''
        return {
            "evaluate_communication": text
        }
    
    if "evaluate_communication" not in job:
        step_evaluate_communication(min_speakers, max_speakers, job, model)
        
    return {
        "evaluate_communication": job["evaluate_communication"]
    }
    
    
def job_exists_locally(job_id: str, base_dir="data") -> bool:
    job_path = os.path.join(base_dir, job_id)
    return os.path.exists(job_path) and os.path.isdir(job_path)


def step_transcribe(job):
    path = job["audio_file"]
    transcript_file = transcribe_audio(path, job["folder"])
    transcript = parse_txt(transcript_file)
    job["transcript"] = transcript
    
    
def step_diarize(min_speakers, max_speakers, job):
    path = job["audio_file"]
    rttm_file = diarize_audio(path, job["folder"], min_speakers, max_speakers)
    segments = parse_rttm(rttm_file)
    job["speakers"] = segments
    

def step_speaker_transcript(min_speakers, max_speakers, job):
    
    if "transcript" not in job:
        step_transcribe(job)
    if "speakers" not in job:
        step_diarize(min_speakers, max_speakers, job)
        
    _, speaker_transcript = assign_speakers_to_transcript_to_json(
        job["transcript"], job["speakers"], job["folder"]
    )
    job["speaker_transcript"] = speaker_transcript
    
    
def step_text_emotion_analysis(min_speakers, max_speakers, job):
    
    if "speaker_transcript" not in job:
        step_speaker_transcript(min_speakers, max_speakers, job)
        
    if "merged_speaker_transcript" not in job:
        _, job["merged_speaker_transcript"] = merge_transcript_speaker_segments_to_json(job["speaker_transcript"], job["folder"])
        
    _, text_emotion = emotion_from_text(job["merged_speaker_transcript"], job["folder"])
    job["text_emotion_analysis"] = text_emotion
    

def step_sentiment_analysis(min_speakers, max_speakers, job):
    
    if "speaker_transcript" not in job:
        step_speaker_transcript(min_speakers, max_speakers, job)
    
    if "merged_speaker_transcript" not in job:
        _, job["merged_speaker_transcript"] = merge_transcript_speaker_segments_to_json(job["speaker_transcript"], job["folder"])
        
    _, text_sentiment = sentiment_from_text(job["merged_speaker_transcript"], job["folder"])
    job["sentiment_analysis"] = text_sentiment
    
    
def step_tone_analysis(min_speakers, max_speakers, job):
    
    if "speaker_transcript" not in job:
        step_speaker_transcript(min_speakers, max_speakers, job)
    
    if "merged_speaker_transcript" not in job:
        _, job["merged_speaker_transcript"] = merge_transcript_speaker_segments_to_json(job["speaker_transcript"], job["folder"])
    
    audio_path = job["audio_file"]
    
    _, tone_analysis = emotion_from_tone(audio_path, job["merged_speaker_transcript"], job["folder"])
    job["tone_analysis"] = tone_analysis
    
    
def step_evaluate_communication(min_speakers, max_speakers, job, model):
    
    if "tone_analysis" not in job:
        step_tone_analysis(min_speakers, max_speakers, job)
        
    if "transcript_with_tone" not in job:
        _, job["transcript_with_tone"] = merge_transcript_with_tone_to_json(job["merged_speaker_transcript"], job["tone_analysis"], job["folder"])
    
    
    if "gemma3" in model:
        transcript, context = create_multi_turn_prompt(job["transcript_with_tone"], job["folder"])
        
        answer = evaluate_communication_with_prompt_os(transcript, context, job["folder"], model)     
    else:
        prompt = create_prompt(job["merged_speaker_transcript"], job["folder"])
        
        answer = evaluate_communication_with_prompt(prompt, job["folder"], model)     
    
    job["evaluate_communication"] = answer
    
    