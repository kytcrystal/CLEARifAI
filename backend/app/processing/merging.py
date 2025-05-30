from pydub import AudioSegment
from .json_io import write_to_json, load_json
import logging
logger = logging.getLogger(__name__)


def assign_speakers_to_transcript(transcript_segments, speaker_segments):
    results = []

    for t in transcript_segments:
        # Find all speakers whose RTTM segments overlap with this transcript line
        matching_speakers = [
            s for s in speaker_segments
            if not (t["end"] < s["start_time"] or t["start"] > s["end_time"])
        ]

        # Assign the speaker with the most overlapping time (if multiple)
        if matching_speakers:
            overlap_durations = [
                min(t["end"], s["end_time"]) - max(t["start"], s["start_time"])
                for s in matching_speakers
            ]
            best_match_index = overlap_durations.index(max(overlap_durations))
            speaker = matching_speakers[best_match_index]["speaker"]
        else:
            speaker = "UNKNOWN"

        results.append({
            "speaker": speaker,
            "start": t["start"],
            "end": t["end"],
            "text": t["text"]
        })

    return results


def merge_by_speaker(segments, max_words=350):
    merged_chunks = []
    current = None

    for entry in segments:
        if current and entry["speaker"] == current["speaker"]:
            current["text"] += " " + entry["text"]
            current["end"] = entry["end"]
        else:
            if current:
                merged_chunks.extend(split_if_too_long(current, max_words))
            current = entry
    if current:
        merged_chunks.extend(split_if_too_long(current, max_words))

    return merged_chunks


def split_if_too_long(segment, max_words):
    words = segment["text"].split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunk_text = ' '.join(words[i:i + max_words])
        chunks.append({
            "speaker": segment["speaker"],
            "start": segment["start"],
            "end": segment["end"],
            "text": chunk_text
        })

    return chunks


def assign_speakers_to_transcript_to_json(transcript_segments, speaker_segments, data_dir):
    speaker_transcript_segments = assign_speakers_to_transcript(transcript_segments, speaker_segments)
    file_prefix = data_dir + "/speaker_transcript"
    return write_to_json(speaker_transcript_segments, file_prefix), speaker_transcript_segments


def merge_transcript_speaker_segments_to_json(speaker_transcript_segments, data_dir):
    merged_segments = merge_by_speaker(speaker_transcript_segments)
    file_prefix = data_dir + "/merged_speaker_transcript"
    return write_to_json(merged_segments, file_prefix), merged_segments


def split_audio(audio_file_path, json_path):
    audio = AudioSegment.from_wav(audio_file_path)
    segments = load_json(json_path)
    audio_chunks = []
    
    for i, seg in enumerate(segments):
        start_ms = int(seg["start"] * 1000)
        end_ms = int(seg["end"] * 1000)
        chunk = audio[start_ms:end_ms]
        
        audio_chunks.append(chunk)

    return audio_chunks
