# Copyright (c) 2024 Julian Müller (ChaoticByte)

from os import getpid as _getpid

from sanic import Sanic as _Sanic
from sanic import empty as _empty
from sanic import Request as _Request

from . import env as _env

from .msg import ComponentLogger as _ComponentLogger
from .stt import STT as _STT


def get_app() -> _Sanic:
    app = _Sanic("TranscriptAPI")

    @app.get("/ping")
    async def ping(_):
        return _empty(status=200)

    @app.post('/')
    async def transcribe(request: _Request):
        audio = request.files.get("audio").body
        if len(audio) < 1:
            return _empty(400)
        resp = await request.respond(content_type="text/plain")
        for s in app.ctx.stt.transcribe(audio):
            await resp.send(s)
        await resp.eof()

    @app.before_server_start
    async def setup_stt(app):
        app.ctx.stt = _STT(_env.API_STT_MODEL, logger=_ComponentLogger(f"{_getpid()}/STT"))
    
    @app.after_server_start
    async def init_stt(app):
        app.ctx.stt.init()

    @app.on_response
    async def middleware(_, response):
        response.headers["Access-Control-Allow-Origin"] = _env.ACCESS_CONTROL_ALLOW_ORIGIN

    return app
