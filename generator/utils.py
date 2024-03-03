import binascii
import base64

def modified_base64(s):
    s = s.encode('utf-16be')
    return binascii.b2a_base64(s).rstrip(b'\n=').replace(b'/', b',')

def doB64(_in, r):
    if _in:
        r.append('+%s-' % modified_base64(''.join(_in)).decode())
        del _in[:]

def utf7encode(s):
    r = []
    _in = []
    for c in s:
        ordC = ord(c)
        if c == b'&':
            doB64(_in, r)
            r.append(b'&-')
        else:
            _in.append(c)
    doB64(_in, r)
    return str(''.join(r))

def utf7decode(s):
    r = []
    _in = []
    for c in s:
        ordC = ord(c)
        if c == b'&':
            doB64(_in, r)
            r.append(b'&-')
        else:
            _in.append(c)
    doB64(_in, r)
    return str(''.join(r))

def base64encode(s:str):
    return base64.b64encode(s.encode()).decode()