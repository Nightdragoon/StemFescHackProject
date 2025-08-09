from typing import Any
from dataclasses import dataclass
import json
@dataclass
class HumanDto:
    generation_id: str
    snippet_id: str
    text: str
    transcribed_text: str
    chunk_index: int
    audio: str
    audio_format: str
    is_last_chunk: bool
    utterance_index: int

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _generation_id = str(obj.get("generation_id"))
        _snippet_id = str(obj.get("snippet_id"))
        _text = str(obj.get("text"))
        _transcribed_text = str(obj.get("transcribed_text"))
        _chunk_index = int(obj.get("chunk_index"))
        _audio = str(obj.get("audio"))
        _audio_format = str(obj.get("audio_format"))
        _is_last_chunk = False
        _utterance_index = int(obj.get("utterance_index"))
        return HumanDto(_generation_id, _snippet_id, _text, _transcribed_text, _chunk_index, _audio, _audio_format, _is_last_chunk, _utterance_index)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)