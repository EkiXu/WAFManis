from generator.model import RequestSample
from mutator import Mutator


def serialize_test():
    sample = RequestSample()

    sample.build_tree("<start>")

    raw = sample.serialize()

    sample2 = RequestSample()

    sample2.unserialize(raw)
    print(sample2.dump2txt())

def mutate_test():
    sample = RequestSample()
    sample.build_tree("<start>")
    print(sample.dump2req("localhost:6000").decode())
    mutator = Mutator(sample,verbose=True)
    mutator.mutate_input()
    print("\r\nAfter mutating\r\n")
    print(mutator.input.dump2req("localhost:6000").decode())


#mutate_test()

# import copy

# sample = RequestSample()
# with open("./fuzzing/queue/corrput-16:24:00.312954","rb") as f:
#     data = f.read()
#     sample.unserialize(data)
#     print(sample.dump2req("localhost:6000"))
# sample.build_tree("<start>")
# sample2 = copy.deepcopy(sample)

#print(sample is sample2,sample == sample2,sample.dump2req() == sample2.dump2req())


# sample = RequestSample()
# sample.build_tree("<start>")
# print(sample.dump2req("localhost:6000").decode())

#serialize_test()

# from generator.model import HTTPResponse
# from utils import webapp_verfication,get_free_tcp_port
# from config import EXPECTED_TAINT

# # raw = b'HTTP/1.1 200 OK\r\nServer: Werkzeug/3.0.1 Python/3.10.12\r\nDate: Mon, 04 Mar 2024 15:31:36 GMT\r\nContent-Type: application/json\r\nContent-Length: 109\r\nConnection: close\r\n\r\n{"args": {}, "form": {"id": "1\' union select 1,group_concat(user,0x3a,password) from users #"}, "json": null}'

# # resp = HTTPResponse(raw)

# # print(webapp_verfication(resp,EXPECTED_TAINT))

# print(get_free_tcp_port())