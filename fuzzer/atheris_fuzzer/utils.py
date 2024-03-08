import os
from generator.model import HTTPResponse,RequestSample
import socket
from urllib.parse import urlparse
from config import WEBAPP_VALIDATE_CODE,WAF_VALIDATE_CODE
import base64
import hashlib
import socket

# def request(host:str,port:int,packet:bytes) ->HTTPResponse:
#     response = b''
#     s = socket.socket()
#     try:
#         s.connect((host, int(port)))
#         s.sendall(packet)
#         s.settimeout(0.05)
#         r = s.recv(2048)
#         while r:
#             response += r
#             r = s.recv(2048)
#     except socket.timeout:
#         pass

#     s.shutdown(socket.SHUT_RDWR)
#     s.close()

#     return HTTPResponse(response)


def request(host, port, data, timeout=1, retry=3):
  """
  Sends a TCP request to a server, receives a response, and retries on connection reset.

  Args:
      host (str): The hostname or IP address of the server.
      port (int): The port number of the server.
      data (bytes): The data to send to the server.
      timeout (int, optional): The timeout in seconds for socket operations. Defaults to 5.
      retry (int, optional): The number of times to retry on connection reset errors. Defaults to 3.

  Returns:
      bytes: The response data received from the server, or None if all retries fail.

  Raises:
      OSError: If an error occurs during socket creation or communication.
  """
  response = b''
  if isinstance(port,str):
    port = int(port)
  for attempt in range(retry + 1):
    try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.sendall(data)
        response = b''
        while True:
          chunk = sock.recv(1024)
          if not chunk:
            break
          response += chunk
        sock.shutdown(socket.SHUT_RDWR)
        return HTTPResponse(response)
    except socket.timeout:
       return HTTPResponse(response)
    except Exception as e:
      if attempt < retry:  # Check for connection reset
        print(f"{e} on attempt {attempt+1}/{retry}. Retrying...")
    except:
       pass

  # All retries failed
  print(f"Failed to connect to {host}:{port} after {retry} attempts.")
  return HTTPResponse(response)

def waf_verfication(resp:HTTPResponse):
    if resp.status_code == WAF_VALIDATE_CODE:
        #return True,resp.raw_packet[len("HTTP/1.1 299 OK\r\nX:"):]
        return True, base64.b64decode(resp.body_json["req"])
    return False, None

def webapp_verfication(resp:HTTPResponse,expected_taint,mode="strict"):
    if resp.status_code == WEBAPP_VALIDATE_CODE:
        return True
    try:
        # key and value must be the exact same as expected
        if mode == "strict":
            if resp.body_json[expected_taint["loc"]][expected_taint["taint_key"]] == expected_taint["taint_val"]:
                return True
        # value can be injected into the exact same key or some other key
        elif mode == "lax":
            if expected_taint["taint_val"] in resp.body_json[expected_taint["loc"]][expected_taint["taint_key"]] \
                or any(expected_taint["taint_val"] in v for v in resp.body_json[expected_taint["loc"]].values()):
                return True
    except KeyError:
        return False
    except TypeError:
       return False
    return False


def save_poc(poc:bytes):
    from hashlib import md5
    POC_DIR = "./fuzzing/poc"
    md5helper = md5()
    md5helper.update(poc)
    with open(os.path.join(POC_DIR,md5helper.hexdigest()),"wb") as f:
        f.write(poc)

def md5(poc:bytes) -> bytes:
    if isinstance(poc,str):
        poc = poc.encode()
    md5helper = hashlib.md5()
    md5helper.update(poc)
    return md5helper.hexdigest()



def get_free_tcp_port():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('localhost', 0))
            port = sock.getsockname()[1]
            return port
    except :
        return 0

# def local_request(udx_path:str,packet:bytes) ->HTTPResponse:
#     response = b''
#     s = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
#     try:
#         s.connect(udx_path)
#         s.sendall(packet)
#         s.settimeout(0.006)
#         r = s.recv(512)
#         # quick_check = HTTPResponse(r)
#         # if quick_check.status_code != 200:
#         #     response = r
#         #     raise socket.timeout
#         while r:
#             response += r
#             r = s.recv(512)
#     except socket.timeout:
#         pass

#     s.shutdown(socket.SHUT_RDWR)
#     s.close()

#     return HTTPResponse(response)# def local_request(udx_path:str,packet:bytes) ->HTTPResponse:
#     response = b''
#     s = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
#     try:
#         s.connect(udx_path)
#         s.sendall(packet)
#         s.settimeout(0.006)
#         r = s.recv(512)
#         # quick_check = HTTPResponse(r)
#         # if quick_check.status_code != 200:
#         #     response = r
#         #     raise socket.timeout
#         while r:
#             response += r
#             r = s.recv(512)
#     except socket.timeout:
#         pass

#     s.shutdown(socket.SHUT_RDWR)
#     s.close()

#     return HTTPResponse(response)
