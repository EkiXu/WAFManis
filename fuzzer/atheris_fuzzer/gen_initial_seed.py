from generator.model import RequestSample
import sys


if __name__ == "__main__":
    seed_num = 10
    if len(sys.argv) > 1:
        seed_num = int(sys.argv[1])
    for i in range(seed_num):
        with open(f"./initial_seed/{i}.input","w") as f:
            case = RequestSample()
            case.build_tree("<start>")
            f.write(case.serialize())

