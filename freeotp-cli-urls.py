#!/usr/bin/env python3

import pyotp
import base64
import sys
import json
import hashlib
import argparse
from urllib.parse import urlparse, parse_qs, unquote

parser = argparse.ArgumentParser(description='Read FreeOTP token.xml files and generate tokens')
parser.add_argument('--url', help='URL to create QRCode for', action="store_true")
parser.add_argument('file',  type=str, help='tokens.xml file to use')
parser.add_argument('token',  type=str, nargs='?', help='token name to generate TOTP value for')

args = parser.parse_args()

digests = {
    'SHA1': hashlib.sha1
        }

with open(args.file) as f:
    for i in f:
        i = i.strip()
        url = urlparse(i)
        qs = parse_qs(url.query)

        s_b32 = qs['secret'][0]
        period = int(qs['period'][0])
        digits = int(qs['digits'][0])
        algo = qs['algorithm'][0]

        name = unquote(url.path)
        if args.token is None:
            print(name)
        elif args.token == name:
            totp = pyotp.TOTP(s=s_b32, interval=period, digits=digits, digest=digests[algo])
            print(totp.now())
            break
