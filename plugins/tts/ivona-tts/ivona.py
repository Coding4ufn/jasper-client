import os
import json
import tempfile
import pyvona
from client import plugin


class IvonaTTSPlugin(plugin.TTSPlugin):
    """
    Uses the Ivona Speech Cloud Services.
    Ivona is a multilingual Text-to-Speech synthesis platform developed by
    Amazon.
    """

    def __init__(self, *args, **kwargs):
        plugin.TTSPlugin.__init__(self, *args, **kwargs)

        access_key = self.config.get('ivona-tts', 'access_key')
        if not access_key:
            raise ValueError("Ivona access key not configured!")

        secret_key = self.config.get('ivona-tts', 'secret_key')
        if not secret_key:
            raise ValueError("Ivona secret key not configured!")

        region = self.config.get('ivona-tts', 'region')
        voice = self.config.get('ivona-tts', 'voice')
        speech_rate = self.config.get('ivona-tts', 'speech_rate')
        sentence_break = self.config.get('ivona-tts', 'sentence_break')
        language = self.config.get('language')

        self._pyvonavoice = pyvona.Voice(access_key, secret_key)
        self._pyvonavoice.codec = "mp3"
        if region is not None:
            self._pyvonavoice.region = region

        # Use an appropriate voice for the chosen language
        all_voices = json.loads(self._pyvonavoice.list_voices())["Voices"]
        suitable_voices = [v for v in all_voices if v["Language"] == language]

        if len(suitable_voices) == 0:
            raise ValueError("Language '%s' not supported" % language)
        else:
            if voice is not None and len([v for v in suitable_voices
                                          if v["Name"] == voice]) > 0:
                # Use voice from config
                self._pyvonavoice.voice_name = voice
            else:
                # Use any voice for that language
                voice = suitable_voices[0]["Name"]
                self._pyvonavoice.voice_name = voice

        if speech_rate is not None:
            self._pyvonavoice.speech_rate = speech_rate
        if sentence_break is not None:
            self._pyvonavoice.sentence_break = sentence_break

    def say(self, phrase):
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            tmpfile = f.name
        self._pyvonavoice.fetch_voice(phrase, tmpfile)
        data = self.mp3_to_wave(tmpfile)
        os.remove(tmpfile)
        return data
