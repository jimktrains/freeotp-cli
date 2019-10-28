#!/usr/bin/env python3

import pyotp
import base64
import sys
import xml.etree.ElementTree as ET
import json
import hashlib
import argparse

parser = argparse.ArgumentParser(description='Read FreeOTP token.xml files and generate tokens')
parser.add_argument('--url', help='URL to create QRCode for', action="store_true")
parser.add_argument('file',  type=str, help='tokens.xml file to use')
parser.add_argument('token',  type=str, nargs='?', help='token name to generate TOTP value for')

args = parser.parse_args()

root = ET.parse(args.file)

digests = {
    'SHA1': hashlib.sha1
        }

for i in root.findall('./string'):
    if i.attrib['name'] == 'tokenOrder':
        continue
    params = json.loads(i.text)
    params.update(i.attrib)

    # Convert the list of signed integers into a hex string.
    s_hex = b''
    for j in params['secret']:
        # Prepend a 0 if hex() would only return a single character.
        prefix = b''
        if j >= 0 and j < 16:
            prefix = b'0'
        b =  prefix + bytes(hex(j & 255)[2:], 'ascii')
        s_hex += b

    # Convert the hex string to base32 encoding.
    s_bytes = base64.b16decode(s_hex, True)
    s_b32 = base64.b32encode(s_bytes)
    str_s_b32 = s_b32.decode('ascii')

    if args.token is None:
        if args.url:
            print(f"otpauth://totp/{params['name']}?secret={str_s_b32}")
        else:
            print(params['name'])
    elif args.token == name:
        if args.url:
            print(f"otpauth://totp/{params['name']}?secret={str_s_b32}")
        else:
            totp = pyotp.TOTP(s=s_b32, interval=params['period'], digits=params['digits'], digest=digests[params['algo']])
            print(totp.now())
        break
