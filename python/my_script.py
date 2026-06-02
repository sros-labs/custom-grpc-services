import grpcserver
import time
from pysros.management import connect


def addNumbers(request, context):
    return {"result": request["number_one"] + request["number_two"]}


def addStreamingNumbers(request_iter, context):
    response_sum = 0
    for request in request_iter:
        response_sum += request["number"]
    return {"result": response_sum}


def streamCount(request, context):
    for i in range(0, 20):
        yield {"response": i}


def is_prime(n):
    thumbs_up_unicode = "\U0001f44d"
    thumbs_down_unicode = "\U0001f44e"

    if n == 1:
        return thumbs_down_unicode

    for i in range(2, 1 + int(n**0.5)):
        if int(n) % i == 0:
            return thumbs_down_unicode

    return thumbs_up_unicode


def streamFactors(request, context):
    n = request["starting_number"]
    for i in range(1, n + 1):
        if n % i == 0:
            yield {"factor": i, "prime": is_prime(i)}


def noughtsAndCrosses(message_iter, context):
    # The random module is not supported on SR OS so the time
    # module is used instead
    def randrange(n):
        return time.ticks_cpu() % n

    def opponent_of(player):
        return {"O": "X", "X": "O"}[player]

    me = None
    unused = [i for i in range(1, 10)]

    for message in message_iter:
        if me is None:
            me = opponent_of(message["player"])
        assert message["player"] == opponent_of(me)
        if "position" in message:
            try:
                unused.remove(message["position"])
            except ValueError:
                yield {"debug_message": "your move is not allowed"}
                continue

        if not unused:
            yield {"debug_message": "game is over, no place to move"}
            break

        # Select a random move from the available unused moves
        my_move = unused.pop(randrange(len(unused)))
        yield {"position": my_move, "player": me}


def main():
    grpcserver.add_handler(service="myservice", rpc="Add", handler=addNumbers)
    grpcserver.add_handler(
        service="myservice", rpc="StreamingAdd", handler=addStreamingNumbers
    )
    grpcserver.add_handler(
        service="myservice", rpc="Count", handler=streamCount
    )
    grpcserver.add_handler(
        service="myservice", rpc="PrimeFinder", handler=streamFactors
    )
    grpcserver.add_handler(
        service="myservice", rpc="NoughtsAndCrosses", handler=noughtsAndCrosses
    )
    grpcserver.handle_rpc()


if __name__ == "__main__":
    main()
