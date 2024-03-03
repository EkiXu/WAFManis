import json
class HTTPResponse:
    raw_packet:bytes
    status_code: int
    headers:dict
    body_json:dict
    def __init__(self,raw_packet:bytes) -> None:
        self.raw_packet = raw_packet
        self.headers = {}
        self.body_json = {}
        try:
            self.parse_header()
            self.parse_body()
        except:
            self.http_version = ""
            self.status_code = "000"

    def parse_header(self):
        if len(self.raw_packet):
            raw_lines = self.raw_packet.splitlines()
            self.http_version = raw_lines[0].split(b" ")[0]
            self.status_code = int(raw_lines[0].split(b" ")[1])
            for header in raw_lines[1:]:
                if header == b"":
                    break
                #print(header)
                key,val = header[:header.index(b":")],header[header.index(b":")+1:]
                self.headers[key.strip().lower()] = val.strip().lower()
        else:
            self.http_version = ""
            self.status_code = "000"
    def parse_body(self):
        body_start = self.raw_packet.find(b"\r\n\r\n")+4
        if body_start > len(self.raw_packet):
            return
        if b"content-Length" in self.headers.keys():
            body_end = int(self.headers[b"content-Length"]) + body_start
        else:
            body_end = len(self.raw_packet)
        #print(self.raw_packet[body_start:body_end])
        content_type = b""
        transfer_encoding = b""
        if b"content-type" in self.headers.keys():
            content_type = self.headers[b"content-type"]

        if b"transfer-encoding" in self.headers.keys():
            transfer_encoding  = self.headers[b"transfer-encoding"]

        if b"application/json" in content_type:
            try:
                self.body_json = json.loads(self.raw_packet[body_start:body_end])
            except Exception as e:
                try:
                    raw_body = self.raw_packet[body_start:body_end]
                    #print("debug here",e,raw_body[raw_body.find(b"{"): raw_body.rfind(b"}")+1])
                    self.body_json = json.loads(raw_body[raw_body.find(b"{"): raw_body.rfind(b"}")+1])
                except Exception as e2:
                    print("body json parser error",e2)
        # else:
        #     print(self.headers)
