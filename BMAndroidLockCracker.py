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
import hashlib
import argparse
from itertools import product

SHA1_LEN = 40
MD5_LEN = 32

class PasswordGestureGenerate:
    """Generates SHA-1 hash from Android gesture pattern."""

    def __init__(self, gesture=None):
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

    def generate_self_hash(self):
        if not self.salted:
            self._update_salted()
        sha1 = hashlib.sha1(self.salted.encode()).hexdigest()
        md5 = hashlib.md5(self.salted.encode()).hexdigest()
        return (sha1 + md5).upper()

    def generate_hash(self, passwd):
        salted = passwd + self.salt
        sha1 = hashlib.sha1(salted.encode()).hexdigest()
        md5 = hashlib.md5(salted.encode()).hexdigest()
        return (sha1 + md5).upper()


class AndroidPasswordCracker:
    """Cracker for Android passwords (PIN or gesture)."""

    def __init__(self, hash_value, salt=None, hash_type=None, verbose=False):
        self.hash_value = hash_value.upper()
        self.salt = salt
        self.hash_type = hash_type
        self.verbose = verbose

    def crack_pin(self, charset, length):
        if not self.salt:
            raise ValueError("Salt required for PIN cracking.")

        print(f"[+] Starting PIN cracking: length={length}, charset={charset}")
        for pin in product(charset, repeat=length):
            candidate = ''.join(pin)
            generator = PasswordPinGenerate(candidate, self.salt)
            candidate_hash = generator.generate_self_hash()
            if self.verbose:
                print(f"[*] Trying: {candidate} -> {candidate_hash}")
            if candidate_hash == self.hash_value:
                print(f"[+] Match found! PIN: {candidate}")
                return candidate
        print("[-] PIN not found.")
        return None

    def crack_gesture(self, length):
        print(f"[+] Starting gesture cracking: length={length}")
        max_dot = 9  # Android gestures use 0-8

        def recursive_search(path, used):
            if len(path) == length:
                generator = PasswordGestureGenerate(path)
                candidate_hash = generator.generate_self_hash()
                if self.verbose:
                    print(f"[*] Trying: {path} -> {candidate_hash}")
                if candidate_hash == self.hash_value:
                    print(f"[+] Match found! Gesture: {path}")
                    return path
                return None
            for i in range(max_dot):
                if i not in used:
                    result = recursive_search(path + [i], used | {i})
                    if result:
                        return result
            return None

        return recursive_search([], set())


def main():
    parser = argparse.ArgumentParser(description="AndroidLockCracker by Benjamin Hunter Miller")
    parser.add_argument('--hash', required=True, help="Target hash value to crack")
    parser.add_argument('--salt', help="Salt value (for PIN cracking)")
    parser.add_argument('--mode', choices=['pin', 'gesture'], required=True, help="Mode: pin or gesture")
    parser.add_argument('--length', type=int, required=True, help="Length of PIN or gesture")
    parser.add_argument('--charset', default="0123456789", help="Charset for PIN cracking")
    parser.add_argument('--verbose', action='store_true', help="Verbose output")
    args = parser.parse_args()

    cracker = AndroidPasswordCracker(args.hash, args.salt, args.mode, args.verbose)

    if args.mode == 'pin':
        cracker.crack_pin(args.charset, args.length)
    elif args.mode == 'gesture':
        cracker.crack_gesture(args.length)

if __name__ == "__main__":
    main()
