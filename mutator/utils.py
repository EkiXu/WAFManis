import binascii
import base64
import codecs

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
    return str(''.join(r)).encode()

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
    return base64.b64encode(s.encode())

def encode(msg:str|bytes,charset) -> bytes:
    if isinstance(msg,bytes):
        msg:str = msg.decode()

    if charset == "utf-7":
        return utf7encode(msg)
    elif charset == "base64":
        return base64encode(msg)
    else:
        try:
            encode_msg = codecs.encode(msg,charset)
        except Exception:
            encode_msg = msg.encode()

    # real_taint = taint
    # print(taint,"taint_type",type(taint),"real_taint_type",type(real_taint),real_taint)
    # raise Exception("end")
    return encode_msg
