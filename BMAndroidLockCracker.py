"""
LEGAL DISCLAIMER:
This script is intended strictly for ethical hacking, Android bug bounty research, and authorized security testing purposes.
It must only be used on devices you own or have explicit permission to test. Unauthorized use of this tool against third-party
devices, systems, or networks may violate local, national, and international laws. The author, Benjamin Hunter Miller, assumes
no liability for misuse or damage resulting from use of this script.

USE RESPONSIBLY AND LEGALLY.
"""


python
Copy
Edit
#!/usr/bin/env python3
"""
AndroidLockCracker - Cracking and generating Android lock hashes
Updated for modern Android systems
Made by Benjamin Hunter Miller
GNU General Public License v3.0

LEGAL DISCLAIMER:
This script is intended strictly for ethical hacking, Android bug bounty research, and authorized security testing purposes.
It must only be used on devices you own or have explicit permission to test. Unauthorized use of this tool against third-party
devices, systems, or networks may violate local, national, and international laws. The author, Benjamin Hunter Miller, assumes
no liability for misuse or damage resulting from use of this script.

USE RESPONSIBLY AND LEGALLY.
"""

import sys
import string
import hashlib
import argparse
from itertools import product

SHA1_LEN = 40
MD5_LEN = 32

class PasswordGestureGenerate:
    """Generates SHA-1 hash from Android gesture pattern."""

    def __init__(self, sizeX=3, sizeY=3, gesture=None):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.gesture = gesture

    def generate_gesture_string(self, gesture):
        return ''.join(chr(point) for point in gesture)

    def generate_self_hash(self):
        if self.gesture is None:
            raise ValueError("Gesture pattern not provided.")
        return self.generate_hash(self.generate_gesture_string(self.gesture))

    def generate_hash(self, gesture_string):
        return hashlib.sha1(gesture_string.encode()).hexdigest().upper()


class PasswordPinGenerate:
    """Generates combined SHA-1 + MD5 hash for PIN/passwords."""

    def __init__(self, passwd=None, salt=None):
        self.passwd = passwd
        self.salt = salt
        self._update_salted()

    def _update_salted(self):
        if self.passwd and self.salt:
            self.salted = self.passwd + self.salt
        else:
            self.salted = None

    def set_salt(self, salt):
        if not salt:
            raise ValueError("Salt cannot be empty.")
        self.salt = salt
        self._update_salted()

    def generate_self_hash_sha1(self):
        if not self.salted:
            self._update_salted()
        return hashlib.sha1(self.salted.encode()).hexdigest()

    def generate_hash_sha1(self, passwd):
        salted = passwd + self.salt
        return hashlib.sha1(salted.encode()).hexdigest()

    def generate_self_hash(self):
        salted = self.passwd + self.salt
        return (hashlib.sha1(salted.encode()).hexdigest() +
                hashlib.md5(salted.encode()).hexdigest()).upper()

    def generate_hash(self, passwd):
        salted = passwd + self.salt
        return (hashlib.sha1(salted.encode()).hexdigest() +
                hashlib.md5(salted.encode()).hexdigest()).upper()
