

if __name__ == "__main__":
    # This is the main function of the fuzzer. It is responsible for generating
    # and sending requests to the target server, and then checking the response
    # to see if the fuzzer has found a bypass.

    # The fuzzer is a simple grammar-based fuzzer. It uses a grammar to generate
    # a packet, sends the packet to the target server, and then checks the
    # response to see if the fuzzer has found a bypass.
    startApp()
    for seed in queue:
        cov , parsed = sendRequestToWebAppValidator(seed)
        if parsed:
            bypassed = sendRequestToWAFValidator()
            if bypassed:
                print("Bypassed")
                minimize(seed)
                break

