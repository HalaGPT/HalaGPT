import requests
from user_agent import generate_user_agent
from hashlib import md5
import random
from bs4 import BeautifulSoup
import pycountry
import time
from datetime import datetime
from secrets import token_hex
from uuid import uuid4
from mnemonic import Mnemonic

API_HalaGPT = "http://sii3.moayman.top"

VOICES = ["alloy", "coral", "echo", "shimmer", "verse", "onyx"]
STYLES = ["friendly", "calm", "noir_detective", "cowboy"]

MODELS_IMAGE = [
    "fluex-pro", "flux", "schnell", "imger-12", "deepseek",
    "gemini-2-5-pro", "blackbox", "redux", "halagpt-7-i",
    "r1", "gpt-4-1"
]

MODELS_BLACKBOX = [
    "blackbox", "gpt-4-1", "gpt-4-1-n", "gpt-4", "gpt-4o",
    "gpt-4o-m", "python", "html", "builder", "java", "js",
    "react", "android", "flutter", "nextjs", "angularjs",
    "swift", "mongodb", "pytorch", "xcode", "azure",
    "bitbucket", "digitalocean", "docker", "electron",
    "erlang", "fastapi", "firebase", "flask", "git",
    "gitlab", "go", "godot", "googlecloud", "heroku"
]

MODELS_DEEPINFRA = [
    "deepseekv3", "deepseekv3x", "deepseekr1", "deepseekr1base",
    "deepseekr1turbo", "deepseekr1llama", "deepseekr1qwen",
    "deepseekprover", "qwen235", "qwen30", "qwen32", "qwen14",
    "mav", "scout", "phi-plus", "guard", "qwq", "gemma27",
    "gemma12", "llama31", "llama332", "llama337", "mixtral24",
    "phi4", "phi-multi", "wizard822", "wizard27", "qwen2572",
    "qwen272", "dolphin26", "dolphin29", "airo70", "lzlv70",
    "mixtral822"
]

MODELS_GPT = [
    "gpt-4", "gpt-4o", "gpt-4-1", "gpt-voice",
    "llama8", "llamascout", "mistral", "mistralcf",
    "phi", "qwen", "bidara", "gpt-music", "o3"
]


class voice:
    @staticmethod
    def openai(text: str, voice: str = "alloy", style: str = None, method: str = "GET") -> dict:
        if voice not in VOICES:
            return {"status": "Error", "error": f"Voice '{voice}' not supported: {VOICES}"}
        if style and style not in STYLES:
            return {"status": "Error", "error": f"Style '{style}' not supported: {STYLES}"}
        params = {"text": text, "voice": voice}
        if style:
            params["style"] = style
        url = f"{API_HalaGPT}/DARK/voice.php"
        resp = requests.post(url, data=params) if method.upper() == "POST" else requests.get(url, params=params)
        return {"status": "ok" if "audio_url" in resp.text else "Bad", "result": resp.text}

    @staticmethod
    def models() -> list:
        return VOICES

    @staticmethod
    def styles() -> list:
        return STYLES


class image:
    @staticmethod
    def generate(prompt: str, model: str = "halagpt-7-i") -> dict:
        if model not in MODELS_IMAGE:
            return {"status": "Error", "error": f"Model '{model}' not supported: {MODELS_IMAGE}"}
        resp = requests.get(f"{API_HalaGPT}/api/img.php", params={model: prompt})
        try:
            return resp.json()
        except:
            return {"status": "OK", "result": resp.text}

    @staticmethod
    def models() -> list:
        return MODELS_IMAGE


class blackbox:
    @staticmethod
    def ask(text: str, model: str) -> dict:
        if model not in MODELS_BLACKBOX:
            return {"status": "Error", "error": f"Model '{model}' not supported: {MODELS_BLACKBOX}"}
        data = requests.get(f"{API_HalaGPT}/api/black.php", params={model: text}).json()
        return {"status": "OK", "result": data.get("response")}

    @staticmethod
    def models() -> list:
        return MODELS_BLACKBOX


class deepinfra:
    @staticmethod
    def ask(text: str, model: str) -> dict:
        if model not in MODELS_DEEPINFRA:
            return {"status": "Error", "error": f"Model '{model}' not supported: {MODELS_DEEPINFRA}"}
        try:
            resp = requests.get(f"{API_HalaGPT}/api/DeepInfra.php", params={model: text})
            res = resp.json()
            return {"status": "OK", "result": res.get("response", res)}
        except Exception as e:
            return {"status": "Error", "error": str(e)}

    @staticmethod
    def models() -> list:
        return MODELS_DEEPINFRA


class gpt:
    @staticmethod
    def ask(text: str, model: str) -> dict:
        if model not in MODELS_GPT:
            return {"status": "Error", "error": f"Model '{model}' not supported: {MODELS_GPT}"}
        try:
            return requests.get(f"{API_HalaGPT}/api/gpt.php", params={model: text}).json()
        except Exception as e:
            return {"status": "Error", "error": str(e)}

    @staticmethod
    def models() -> list:
        return MODELS_GPT


class wormgpt:
    @staticmethod
    def worm(text: str) -> dict:
        res = requests.get(f"{API_HalaGPT}/DARK/api/wormgpt.php", params={"text": text}).json()
        return {"status": "OK", "result": res.get("response")}

    @staticmethod
    def darkgpt(text: str) -> dict:
        res = requests.get(f"{API_HalaGPT}/DARK/api2/darkgpt.php", params={"text": text}).json()
        return {"status": "OK", "result": res.get("response")}


class gemini:
    @staticmethod
    def ask(prompt: str) -> dict:
        try:
            return requests.get(f"{API_HalaGPT}/DARK/gemini.php", params={"text": prompt}).json()
        except:
            return {"status": "Error", "result": ""}


class chat:
    @staticmethod
    def ask(prompt: str) -> dict:
        return requests.get(f"{API_HalaGPT}/api/chat/gpt-3.5.php", params={"ai": prompt}).json()


class deepseek:
    @staticmethod
    def codeify(text: str) -> dict:
        url = f"{API_HalaGPT}/api/DeepSeek/DeepSeek.php"
        resp = requests.get(url, params={"text": text})
        try:
            data = resp.json()
            if "result" in data:
                return {"status": "OK", "result": data["result"]}
            if "response" in data:
                return {"status": "OK", "result": data["response"]}
            return {"status": "OK", "result": str(data)}
        except ValueError:
            return {"status": "OK", "result": resp.text}