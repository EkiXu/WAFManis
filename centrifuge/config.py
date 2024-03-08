WAF = {
    "safeline": {
        "name": "safeline",
        "url": "http://safeline.waf.server-config.zip:31080/"
    },
    "aliyun": {
        "name": "aliyun",
        "url": "http://aliyun.waf.jianjunchen.com:80/"
    }
}

WEBAPP_VALIDATOR = {
    # "flask": {
    #     "name": "flask",
    #     "host":"localhost",
    #     "port": "15001",
    #     "path": "/",
    #     "expected_taint": {
    #         "loc": "form",
    #         "taint_key":"taint",
    #         "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
    #     }
    # },
    "webpy": {
        "name": "webpy",
        "host":"localhost",
        "port": "15002",
        "path": "/",
        "expected_taint": {
            "loc": "form",
            "taint_key":"taint",
            "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
        }
    },
    "fastapi": {
        "name": "fastapi",
        "host":"localhost",
        "port": "15003",
        "path": "/",
        "expected_taint": {
            "loc": "form",
            "taint_key":"taint",
            "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
        }
    },
    "django": {
        "name": "django",
        "host":"localhost",
        "port": "15004",
        "path": "/",
        "expected_taint": {
            "loc": "form",
            "taint_key":"taint",
            "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
        }
    },
    "gin" : {
        "name": "gin",
        "host":"localhost",
        "port": "15005",
        "path": "/",
        "expected_taint": {
            "loc": "form",
            "taint_key":"taint",
            "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
        }
    },
    "echo": {
        "name": "echo",
        "host":"localhost",
        "port": "15006",
        "path": "/",
        "expected_taint": {
            "loc": "form",
            "taint_key":"taint",
            "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
        }
    },
    "beego": {
        "name": "beego",
        "host":"localhost",
        "port": "15007",
        "path": "/echo/post",
        "expected_taint": {
            "loc": "form",
            "taint_key":"taint",
            "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
        }
    },
    "laravel": {
        "name": "laravel",
        "host":"localhost",
        "port": "15008",
        "path": "/",
        "expected_taint": {
            "loc": "form",
            "taint_key":"taint",
            "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
        }
    },
    "codeigniter":{
        "name": "codeigniter",
        "host":"localhost",
        "port": "15009",
        "path": "/",
        "expected_taint": {
            "loc": "form",
            "taint_key":"taint",
            "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
        }
    },
    "symfony":{
        "name": "symfony",
        "host":"localhost",
        "port": "15010",
        "path": "/",
        "expected_taint": {
            "loc": "form",
            "taint_key":"taint",
            "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
        }
    },
    "express":{
        "name": "express",
        "host":"localhost",
        "port": "15011",
        "path": "/",
        "expected_taint": {
            "loc": "form",
            "taint_key":"taint",
            "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
        }
    },
    "fastify":{
        "name": "fastify",
        "host":"localhost",
        "port": "15012",
        "path": "/",
        "expected_taint": {
            "loc": "form",
            "taint_key":"taint",
            "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
        }
    },
    "koa": {
        "name": "koa",
        "host":"localhost",
        "port": "15013",
        "path": "/",
        "expected_taint": {
            "loc": "form",
            "taint_key":"taint",
            "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
        }
    },
    "nestjs":{
        "name": "nestjs",
        "host":"localhost",
        "port": "15014",
        "path": "/",
        "expected_taint": {
            "loc": "form",
            "taint_key":"taint",
            "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
        }
    },
    "sails":{
        "name": "sails",
        "host":"localhost",
        "port": "15015",
        "path": "/post",
        "expected_taint": {
            "loc": "form",
            "taint_key":"taint",
            "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
        }
    },
    "rocket":{
        "name": "rocket",
        "host":"localhost",
        "port": "15016",
        "path": "/",
        "expected_taint": {
            "loc": "form",
            "taint_key":"taint",
            "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
        }
    },
    "rails":{
        "name": "rails",
        "host":"localhost",
        "port": "15017",
        "path": "/echo/post",
        "expected_taint": {
            "loc": "form",
            "taint_key":"taint",
            "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
        }
    },
    "aspnetcore":{
        "name": "aspnetcore",
        "host":"localhost",
        "port": "15018",
        "path": "/echo/post",
        "expected_taint": {
            "loc": "form",
            "taint_key":"taint",
            "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
        }
    },
    "springboot":{
        "name": "springboot",
        "host":"localhost",
        "port": "15019",
        "path": "/post2",
        "expected_taint": {
            "loc": "form",
            "taint_key":"taint",
            "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #",
        }
    },
}

INPUT_EVASION_DIR = "./evasion_03_21"
MINI_EVASION_DIR = "./mini_evasion_simple_03_21"
MINI_SAMPLE_DIR = "./mini_sample_simple_03_21"


WEBAPP_VALIDATE_CODE,WAF_VALIDATE_CODE = 299,299

FROZEN_SYMBOL = ["<start>","<request_line>","<request_headers>","<host_header>","<content_length_header>","<taint_key>","<taint_token>","<body>"]
