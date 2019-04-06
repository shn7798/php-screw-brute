import os
import sys
import binascii
from brute import decipher, header

def check_encrypted(bytes):
    return bytes.startswith(header)

def decrypt_file(key, filepath, bak_suffix='.bak'):
    bakpath = filepath + bak_suffix

    with open(filepath, 'rb') as fh:
        bytes = fh.read()


    if not check_encrypted(bytes):
        return

    # remove header
    bytes = bytes[len(header):]

    with open(bakpath, 'wb') as fh:
        fh.write(bytes)

    try:
        assert decipher(bytes, key, filepath)
    except Exception as e:
        print('[E] Error: %s' % filepath)


def find(root, exts=('.php', '.js', '.html')):
    result = []
    for root, dirs, files in os.walk(root):
        for file in files:
            ext = list(filter(lambda x: file.lower().endswith(x), exts))
            if ext:
                filepath = os.path.join(root, file)
                result.append(filepath)
        for dirname in dirs:
            result.extend(find(dirname, exts))

    return result



if __name__ == '__main__':
    key = sys.argv[1]
    key = binascii.a2b_hex(key.replace(' ', ''))
    print(repr(key))

    root = sys.argv[2]
    for filepath in find(root, exts=('.php', '.js', '.html')):
        print(filepath)
        decrypt_file(key, filepath)
    
