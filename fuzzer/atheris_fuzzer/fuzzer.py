import atheris
from multiprocessing import Process
import socket,sys,os,datetime
from json import dumps
from model import HTTPResponse
from datetime import datetime
import ssl
import time
# import flask
import coverage
coverage.process_startup()

global tot_cnt

with atheris.instrument_imports():
    import flask


app = flask.Flask(__name__)
@app.route("/", methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD', 'TRACE', 'CONNECT'])
def parse1():
    return (dumps({"args":flask.request.args,"form":flask.request.form,"json":flask.request.json if flask.request.content_type == 'application/json' else None}),200,[("Content-Type","application/json")])

@app.route("/<any>", methods=['GET', 'POST','PUT','DELETE','PATCH','OPTIONS','HEAD','TRACE','CONNECT'])
def parse2(any):
    return (dumps({"args":flask.request.args,"form":flask.request.form,"json":flask.request.json if flask.request.content_type == 'application/json' else None}),200,[("Content-Type","application/json")])



import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
log.disabled = True

host='127.0.0.1'
port=6000

target:Process

def CustomMutator(data, max_size, seed) -> bytes:
    from mutators.config import Config
    from mutators.mutator import Mutator
    from mutators.request import Request

    config = Config()
    try:
        req = Request(data)
        mut = Mutator(req,config)
        mut.mutate_input()
    except:
        return b""

    return req.generate_request()

queue_dir = './fuzzing/queue'
if not os.path.exists(queue_dir):
    os.makedirs(queue_dir)
else:
    if os.listdir(queue_dir):
        os.rename(queue_dir, '{}_{}_bkup'.format(queue_dir,datetime.now().strftime("%Y%m%d-%H%M%S")))
        os.makedirs(queue_dir)


def test():
    target = Process(target=app.run, kwargs={'debug': True, 'port': 6000})
    target.start()

def local_request(udx_path:str,packet:bytes) ->HTTPResponse:
    response = b''
    s = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
    try:
        s.connect(udx_path)
        s.sendall(packet)
        s.settimeout(0.006)
        r = s.recv(512)
        # quick_check = HTTPResponse(r)
        # if quick_check.status_code != 200:
        #     response = r
        #     raise socket.timeout
        while r:
            response += r
            r = s.recv(512)
    except socket.timeout:
        pass

    s.shutdown(socket.SHUT_RDWR)
    s.close()

    return HTTPResponse(response)

def request(host,port,packet:bytes,enable_ssl=False) ->HTTPResponse:
    response = b''
    s = socket.socket()
    if enable_ssl:
        #ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        s = ssl.wrap_socket(s)
    try:
        s.connect((host, int(port)))
        s.sendall(packet)
        s.settimeout(0.05)
        r = s.recv(2048)
        # quick_check = HTTPResponse(r)
        # if quick_check.status_code != 200:
        #     response = r
        #     raise socket.timeout
        while r:
            response += r
            r = s.recv(2048)
    except socket.timeout:
        pass

    s.shutdown(socket.SHUT_RDWR)
    s.close()

    return HTTPResponse(response)



def save_poc(poc:bytes):
    from hashlib import md5
    POC_DIR = "./fuzzing/poc"
    md5helper = md5()
    md5helper.update(poc)
    with open(os.path.join(POC_DIR,md5helper.hexdigest()),"wb") as f:
        f.write(poc)

chosen_charset:str = ""

def markup(raw_packet:bytes,taint:bytes,test_url:str) -> bytes:
    import copy
    from urllib.parse import urlparse
    import re
    import codecs
    packet = copy.deepcopy(raw_packet)

    regex = rb"(.)(_TAINT_)"
    global chosen_charset

    def encode_taint(match:re.Match):
        global chosen_charset
        #charsets = '''US-ASCII,ISO-8859-1,ISO_8859-1:1987,ISO-8859-2,ISO_8859-2:1987,ISO-8859-3,ISO_8859-3:1988,ISO-8859-4,ISO_8859-4:1988,ISO-8859-5,ISO_8859-5:1988,ISO-8859-6,ISO_8859-6:1987,ISO-8859-7,ISO_8859-7:1987,ISO-8859-8,ISO_8859-8:1988,ISO-8859-9,ISO_8859-9:1989,ISO-8859-10,ISO_6937-2-add,JIS_X0201,JIS_Encoding,Shift_JIS,EUC-JP,Extended_UNIX_Code_Packed_Format_for_Japanese,Extended_UNIX_Code_Fixed_Width_for_Japanese,BS_4730,SEN_850200_C,IT,ES,DIN_66003,NS_4551-1,NF_Z_62-010,ISO-10646-UTF-1,ISO_646.basic:1983,INVARIANT,ISO_646.irv:1983,NATS-SEFI,NATS-SEFI-ADD,NATS-DANO,NATS-DANO-ADD,SEN_850200_B,KS_C_5601-1987,ISO-2022-KR,EUC-KR,ISO-2022-JP,ISO-2022-JP-2,JIS_C6220-1969-jp,JIS_C6220-1969-ro,PT,greek7-old,latin-greek,NF_Z_62-010_(1973),Latin-greek-1,ISO_5427,JIS_C6226-1978,BS_viewdata,INIS,INIS-8,INIS-cyrillic,ISO_5427:1981,ISO_5428:1980,GB_1988-80,GB_2312-80,NS_4551-2,videotex-suppl,PT2,ES2,MSZ_7795.3,JIS_C6226-1983,greek7,ASMO_449,iso-ir-90,JIS_C6229-1984-a,JIS_C6229-1984-b,JIS_C6229-1984-b-add,JIS_C6229-1984-hand,JIS_C6229-1984-hand-add,JIS_C6229-1984-kana,ISO_2033-1983,ANSI_X3.110-1983,T.61-7bit,T.61-8bit,ECMA-cyrillic,CSA_Z243.4-1985-1,CSA_Z243.4-1985-2,CSA_Z243.4-1985-gr,ISO-8859-6-E,ISO_8859-6-E,ISO-8859-6-I,ISO_8859-6-I,T.101-G2,ISO-8859-8-E,ISO_8859-8-E,ISO-8859-8-I,ISO_8859-8-I,CSN_369103,JUS_I.B1.002,IEC_P27-1,JUS_I.B1.003-serb,JUS_I.B1.003-mac,greek-ccitt,NC_NC00-10:81,ISO_6937-2-25,GOST_19768-74,ISO_8859-supp,ISO_10367-box,latin-lap,JIS_X0212-1990,DS_2089,us-dk,dk-us,KSC5636,UNICODE-1-1-UTF-7,ISO-2022-CN,ISO-2022-CN-EXT,UTF-8,ISO-8859-13,ISO-8859-14,ISO-8859-15,ISO-8859-16,GBK,GB18030,OSD_EBCDIC_DF04_15,OSD_EBCDIC_DF03_IRV,OSD_EBCDIC_DF04_1,ISO-11548-1,KZ-1048,ISO-10646-UCS-2,ISO-10646-UCS-4,ISO-10646-UCS-Basic,ISO-10646-Unicode-Latin1,ISO-10646-J-1,ISO-Unicode-IBM-1261,ISO-Unicode-IBM-1268,ISO-Unicode-IBM-1276,ISO-Unicode-IBM-1264,ISO-Unicode-IBM-1265,UNICODE-1-1,SCSU,UTF-7,UTF-16BE,UTF-16LE,UTF-16,CESU-8,UTF-32,UTF-32BE,UTF-32LE,BOCU-1,UTF-7-IMAP,ISO-8859-1-Windows-3.0-Latin-1,ISO-8859-1-Windows-3.1-Latin-1,ISO-8859-2-Windows-Latin-2,ISO-8859-9-Windows-Latin-5,hp-roman8,Adobe-Standard-Encoding,Ventura-US,Ventura-International,DEC-MCS,IBM850,PC8-Danish-Norwegian,IBM862,PC8-Turkish,IBM-Symbols,IBM-Thai,HP-Legal,HP-Pi-font,HP-Math8,Adobe-Symbol-Encoding,HP-DeskTop,Ventura-Math,Microsoft-Publishing,Windows-31J,GB2312,Big5,macintosh,IBM037,IBM038,IBM273,IBM274,IBM275,IBM277,IBM278,IBM280,IBM281,IBM284,IBM285,IBM290,IBM297,IBM420,IBM423,IBM424,IBM437,IBM500,IBM851,IBM852,IBM855,IBM857,IBM860,IBM861,IBM863,IBM864,IBM865,IBM868,IBM869,IBM870,IBM871,IBM880,IBM891,IBM903,IBM904,IBM905,IBM918,IBM1026,EBCDIC-AT-DE,EBCDIC-AT-DE-A,EBCDIC-CA-FR,EBCDIC-DK-NO,EBCDIC-DK-NO-A,EBCDIC-FI-SE,EBCDIC-FI-SE-A,EBCDIC-FR,EBCDIC-IT,EBCDIC-PT,EBCDIC-ES,EBCDIC-ES-A,EBCDIC-ES-S,EBCDIC-UK,EBCDIC-US,UNKNOWN-8BIT,MNEMONIC,MNEM,VISCII,VIQR,KOI8-R,HZ-GB-2312,IBM866,IBM775,KOI8-U,IBM00858,IBM00924,IBM01140,IBM01141,IBM01142,IBM01143,IBM01144,IBM01145,IBM01146,IBM01147,IBM01148,IBM01149,Big5-HKSCS,IBM1047,PTCP154,Amiga-1251,KOI7-switched,BRF,TSCII,CP51932,windows-874,windows-1250,windows-1251,windows-1252,windows-1253,windows-1254,windows-1255,windows-1256,windows-1257,windows-1258,TIS-620,CP50220'''.split(",")
        charsets = ['ascii','base64','big5','big5hkscs','cp037','cp273','cp424','cp437','cp500','cp720','cp737','cp775','cp850','cp852','cp855','cp856','cp857','cp858','cp860','cp861','cp862','cp863','cp864','cp865','cp866','cp869','cp874','cp875','cp932','cp949','cp950','cp1006','cp1026','cp1125','cp1140','cp1250','cp1251','cp1252',
'cp1253','cp1254','cp1255','cp1256','cp1257','cp1258','euc_jp','euc_jis_2004','euc_jisx0213','euc_kr','gb2312',
'gbk',
'gb18030',
'hz',
'iso2022_jp',
'iso2022_jp_1',
'iso2022_jp_2',
'iso2022_jp_2004',
'iso2022_jp_3',
'iso2022_jp_ext',
'iso2022_kr',
'latin_1',
'iso8859_2',
'iso8859_3',
'iso8859_4',
'iso8859_5',
'iso8859_6',
'iso8859_7',
'iso8859_8',
'iso8859_9',
'iso8859_10',
'iso8859_11',
'iso8859_13',
'iso8859_14',
'iso8859_15',
'iso8859_16',
'johab',
'koi8_r',
'koi8_t',
'koi8_u',
'kz1048',
'mac_cyrillic',
'mac_greek',
'mac_iceland','mac_latin2','mac_roman','mac_turkish','ptcp154','shift_jis','shift_jis_2004','shift_jisx0213','utf_32','utf_32_be','utf_32_le','utf_16','utf_16_be','utf_16_le','utf_7','utf_8','utf_8_sig']
        chosen_charset = charsets[int(ord(match.groups()[0])) % len(charsets)]
        try:
            real_taint = codecs.encode(taint.decode(),chosen_charset)
        except TypeError:
            real_taint = codecs.encode(taint,chosen_charset)
        # real_taint = taint
        # print(taint,"taint_type",type(taint),"real_taint_type",type(real_taint),real_taint)
        # raise Exception("end")
        return real_taint

    # You can manually specify the number of replacements by changing the 4th argument
    packet = re.sub(regex, encode_taint, packet, 0, re.MULTILINE)
    packet = packet.replace(b"_CHAR_",chosen_charset.encode())

    #packet = packet.replace(b"_TAINT_",taint)
    body_begin = packet.find(b"\r\n\r\n")
    if body_begin !=-1:
        body_begin += len(b"\r\n\r\n")
        content_length = len(packet) - body_begin
        packet = packet.replace(b"_LEN_",str(content_length).encode())

    url = urlparse(test_url)
    packet = packet.replace(b"_HOST_",url.netloc.encode())
    return packet


def TestOneInput(data):
    TAINT = b"../../etc/passwd"
    global tot_cnt
    global target
    #print(data)

    if data==b'':
        return

    real_data = markup(data,TAINT,f"http://127.0.0.1:{port}")

    #target.start()
    if tot_cnt % 1000 == 0:
        try:
            target.kill()
        except:
            pass
        target = Process(target=app.run, kwargs={'host': 'unix://./tmp.socket'})
        target.start()
        time.sleep(1)

    res = local_request("./tmp.socket",real_data)

    # target.kill()
    #print(res.raw_packet)

    #print("response",res.raw_packet)
    valid_request = False
    try:
        # if any(TAINT in data.encode() for data in res.body_json["form"].values()):
        if res.body_json["form"]["id"].encode() == TAINT:
            valid_request = True
            waf_res:HTTPResponse = request("202.112.238.179","28280",markup(data,TAINT,"http://202.112.238.179:28280"))
            #print(waf_res.status_code)
            if waf_res.status_code == 200:
                print(waf_res.status_code)
                save_poc(real_data)
    except KeyError:
        pass

    #write data into file in queue_dir
    # with open('{}/{}-{}'.format(queue_dir, valid_request, datetime.now().strftime('%H:%M:%S.%f')), 'wb') as f:
    #     f.write(data)
    tot_cnt += 1

# target = Process(target=app.run, kwargs={'host': 'unix://./tmp.socket'})
#target.start()


if __name__ =='__main__':
    tot_cnt = 0
    atheris.Setup(sys.argv, TestOneInput)
    #atheris.Setup(sys.argv, TestOneInput,custom_mutator=CustomMutator)
    atheris.Fuzz()
