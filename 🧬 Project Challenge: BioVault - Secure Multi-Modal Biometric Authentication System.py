🎯 Objective:

Design and develop a Python-based multi-modal biometric authentication system that captures face and voice data, processes it securely using cryptographic hashing and encryption, and validates user identity using stored biometric profiles.
🔐 Project Title:

BioVault: A Cryptographically Secure Multi-Modal Biometric Authentication Platform
🧠 Learning Outcomes:

By completing this project, you’ll gain practical experience in:

    Capturing biometric data using Python (OpenCV, PyAudio)

    Implementing cryptographic hashing and symmetric encryption

    Creating secure multi-modal user profiles

    Authenticating users using a combination of biometric traits

    Ethical handling of biometric data

🧰 Requirements:
Component	Library/Tool
Face Capture	OpenCV
Voice Capture	PyAudio
Hashing	hashlib
Encryption	cryptography or Fernet
Data Handling	pickle, os, json
Optional GUI	Tkinter / PyQt (bonus)
🗂️ Project Structure:

biovault/
├── main.py
├── face_capture.py
├── voice_capture.py
├── crypto_utils.py
├── auth_engine.py
├── user_profiles/
│   ├── alice.json
│   └── bob.json
└── utils/
    └── audio_helpers.py

💻 Step-by-Step Breakdown:
1. face_capture.py – Capture face image & encode

import cv2
import numpy as np

def capture_face_image():
    cam = cv2.VideoCapture(0)
    print("📷 Capturing face. Look at the camera...")
    ret, frame = cam.read()
    cam.release()
    if not ret:
        raise Exception("Failed to capture face")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.resize(gray, (100, 100)).flatten()

2. voice_capture.py – Record 3 seconds of voice

import pyaudio
import wave

def capture_voice(filename="temp_voice.wav", duration=3):
    print("🎤 Recording voice...")
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    p = pyaudio.PyAudio()

    stream = p.open(format=format, channels=channels, rate=rate,
                    input=True, frames_per_buffer=chunk)

    frames = [stream.read(chunk) for _ in range(int(rate / chunk * duration))]
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    with open(filename, 'rb') as f:
        return f.read()

3. crypto_utils.py – Hashing & Encryption Functions

import hashlib
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def get_fernet(key):
    return Fernet(key)

def hash_data(data: bytes):
    return hashlib.sha256(data).hexdigest()

def encrypt_data(data: bytes, key: bytes):
    return get_fernet(key).encrypt(data)

def decrypt_data(data: bytes, key: bytes):
    return get_fernet(key).decrypt(data)

4. auth_engine.py – Authentication Logic

import json
from crypto_utils import hash_data

def authenticate_user(face_hash, voice_hash, username):
    try:
        with open(f"user_profiles/{username}.json", 'r') as f:
            profile = json.load(f)

        if face_hash == profile["face_hash"] and voice_hash == profile["voice_hash"]:
            print("✅ Authentication successful!")
        else:
            print("❌ Authentication failed.")
    except FileNotFoundError:
        print("⚠️ User profile not found.")

5. main.py – Pull It All Together

from face_capture import capture_face_image
from voice_capture import capture_voice
from crypto_utils import hash_data
from auth_engine import authenticate_user

def main():
    username = input("Enter username: ").lower()
    face = capture_face_image()
    voice = capture_voice()

    face_hash = hash_data(face.tobytes())
    voice_hash = hash_data(voice)

    authenticate_user(face_hash, voice_hash, username)

if __name__ == "__main__":
    main()

🧪 Optional: Enroll a New User

Create a small script to enroll a new user:

from face_capture import capture_face_image
from voice_capture import capture_voice
from crypto_utils import hash_data
import json
import os

def enroll_user():
    username = input("Enter new username: ").lower()
    face = capture_face_image()
    voice = capture_voice()

    user_data = {
        "face_hash": hash_data(face.tobytes()),
        "voice_hash": hash_data(voice)
    }

    with open(f"user_profiles/{username}.json", 'w') as f:
        json.dump(user_data, f)
    print(f"🧑‍💼 User '{username}' enrolled successfully.")

if __name__ == '__main__':
    enroll_user()

✅ Challenge Goals
Feature	Requirement
🎥 Face Capture	Using webcam and OpenCV
🎤 Voice Capture	Using PyAudio
🔒 Cryptographic Security	SHA-256 for hashing; Fernet for encryption (optional)
👤 Profile Management	Store biometric hashes per user
🔐 Authentication Engine	Match hashes and display result

🚨 Ethics & Disclaimer

Always remember:

    Only test this on devices you own

    Do not store real biometric data without consent

    Respect data privacy laws (like GDPR)
