import os
from generator.model import HTTPResponse,RequestSample
import socket
from urllib.parse import urlparse
from config import WEBAPP_VALIDATE_CODE,WAF_VALIDATE_CODE
import hashlib
import base64



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
  if isinstance(port,str):
    port = int(port)
  response = b''
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
    except (KeyError,TypeError):
        return False
    return False


def md5(poc:bytes) -> bytes:
    if isinstance(poc,str):
        poc = poc.encode()
    md5helper = hashlib.md5()
    md5helper.update(poc)
    return md5helper.hexdigest()

