# Copyright (c) 2024 Julian Müller (ChaoticByte)

from io import BytesIO as _BytesIO
from pathlib import Path as _Path

from faster_whisper import WhisperModel as _WhisperModel

from .msg import ComponentLogger as _ComponentLogger


class STT:

    def __init__(self, model_path: _Path, n_threads: int = 4, use_int8: bool = True, logger: _ComponentLogger = _ComponentLogger("STT")):
        assert isinstance(model_path, _Path)
        assert type(n_threads) == int and n_threads >= 0
        assert type(use_int8) == bool
        assert isinstance(logger, _ComponentLogger)
        self.logger = logger
        self.model_path = model_path.expanduser().resolve()
        assert self.model_path.exists()
        self.n_threads = n_threads
        if use_int8:
            self.compute_type = "int8"
        else:
            self.compute_type = "default"
        self._model = None

    def init(self):
        if self._model is None:
            self.logger.debug("Initializing ...")
            self._model = _WhisperModel(
                self.model_path.__str__(),
                device="cpu",
                cpu_threads=self.n_threads,
                compute_type=self.compute_type,
                local_files_only=True)
            self.logger.debug("Initialized.")

    def transcribe(self, audio: bytes) -> str:
        '''Transcibes audio and yields the segment strings'''
        assert type(audio) == bytes
        with _BytesIO(audio) as bio:
            bio.seek(0)
            self.init()
            self.logger.debug("Transcribing audio ...")
            segments, _ = self._model.transcribe(
                bio,
                beam_size=5, # beam size -> performance/quality
                vad_filter=True) # remove silence
            for s in segments:
                self.logger.debug(f"... segment #{s.id}")
                if s.id == 1:
                    text = s.text.lstrip(" ")
                else:
                    text = s.text
                yield text
