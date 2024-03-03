from generator import Generator

Generator = Generator

def generatorPacket(base=None,host=None,path=None,taint_key=None,taint_param=None):
    if base == None:
        base = f'''POST /{path} HTTP/1.1\r
User-Agent: Chrome/104.0.5112.102\r
Accept: */*\r
Host: {host}\r
'''
    content_type_header = Generator("<content_type_header>").build_tree()

    body = Generator("<body>").build_tree()

    content_len = len(body)

    content_len_header = "Content-Length: %d" % content_len

    packet = base+content_type_header+"\r\n"+content_len_header+"\r\n\r\n"+body
    return packet

# def outputPacket(base,body_tree:Generator):
#     body = body_tree.output()
#     body_begin = body.find("\r\n\r\n") + len("\r\n\r\n")
#     content_length = len(body) - body_begin
#     content_length_header = "Content-Length: %d" % content_length

#     packet = base + content_length_header +"\r\n" + body
