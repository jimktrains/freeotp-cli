#!/usr/bin/env python3

import pyotp
import base64
import sys
import xml.etree.ElementTree as ET
import json
import hashlib
import argparse

parser = argparse.ArgumentParser(description='Read FreeOTP token.xml files and generate tokens')
parser.add_argument('file',  type=str, help='tokens.xml file to use')

parser.add_argument('token',  type=str, nargs='?', help='token name to generate TOTP value for')

args = parser.parse_args()

root = ET.parse(sys.argv[1])

digests = {
    'SHA1': hashlib.sha1
        }

for i in root.findall('./string'):
    name = i.attrib['name']
    if args.token is None:
        print(name)
    elif args.token == name:
        params = json.loads(i.text)

        # Convert the list of signed integers into a hex string.
        s_hex = b''
        for j in params['secret']:
            # Prepend a 0 if hex() would only return a single character.
            prefix = b''
            if abs(j) < 16:
                prefix = b'0'
            s_hex += prefix + bytes(hex(j & 255)[2:], 'ascii')

        # Convert the hex string to base32 encoding.
        s_bytes = base64.b16decode(s_hex, True)
        s_b32 = base64.b32encode(s_bytes)
        totp = pyotp.TOTP(s=s_b32, interval=params['period'], digits=params['digits'], digest=digests[params['algo']])
        print(totp.now())
        break
