#!/usr/bin/env python3
from my_custom_proto_pb2 import Move
import my_custom_proto_pb2_grpc
import grpc
import os
from queue import Queue


class Board:
    def __init__(self):
        self.data = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]

    def draw(self):
        for row in self.data:
            print(row[0], row[1], row[2])

    def set(self, pos, who):
        r, c = (pos - 1) // 3, (pos - 1) % 3
        self.data[r][c] = who

    def is_valid_move(self, move):
        if move < 1 or move > 9:
            return False
        r, c = (move - 1) // 3, (move - 1) % 3
        return self.data[r][c] not in ("X", "O")

    def is_winner(self, player):
        board = self.data
        # Check rows
        for r in range(0, 3):
            if all(board[r][c] == player for c in range(0, 3)):
                return True
        # Check columns
        for c in range(0, 3):
            if all(board[r][c] == player for r in range(0, 3)):
                return True
        # Check diagonals
        return (player == board[0][0] == board[1][1] == board[2][2]) or (
            player == board[2][0] == board[1][1] == board[0][2]
        )

    def is_full(self):
        for row in self.data:
            for elem in row:
                if elem not in ("X", "O"):
                    return False
        return True

    def is_game_over(self):
        return self.is_winner("X") or self.is_winner("O") or self.is_full()


def ask_move(board, player):
    move = int(input(f"Enter your move (1-9) {player}: "))

    while not board.is_valid_move(move):
        move = int(input(f"INVALID MOVE. Enter your move (1-9) {player}: "))

    return move


def choose_player():
    player = input("Choose your player (X/O): ").upper()
    while player not in ("X", "O"):
        player = input("Invalid choice. Choose your player (X/O): ").upper()
    return player


def _generate_moves(queue):
    while True:
        request = queue.get()
        if request is None:
            break
        yield request


def player_move(board, player):
    while True:
        board.draw()
        print("YOUR TURN")
        my_move = ask_move(board, player)
        board.set(my_move, player)
        return Move(position=my_move, player=player)


def main():
    host = os.environ.get("PYSROS_IP", "172.20.20.10")
    port = os.environ.get("PYSROS_GRPC_PORT", "57400")
    username = os.environ.get("PYSROS_NAME", "admin")
    password = os.environ.get("PYSROS_PASS", "NokiaSros1!")
    auth_metadata = [
        ("username", username),
        ("password", password),
    ]
    board = Board()
    me = choose_player()
    opponent = "O" if me == "X" else "X"
    queue = Queue()

    try:
        with grpc.insecure_channel(f"{host}:{port}") as channel:
            stub = my_custom_proto_pb2_grpc.myserviceStub(channel)

            # First message has to be send before we have response
            if me == "X":
                queue.put(player_move(board, me))
            else:
                # If player do not start, we have to tell server, that it should start
                queue.put(Move(player=me))

            for response in stub.NoughtsAndCrosses(
                _generate_moves(queue), metadata=auth_metadata
            ):
                if response.position:
                    print(f"{opponent} moves to {response.position}")
                    print()
                    assert board.is_valid_move(response.position)
                    board.set(response.position, opponent)
                    if board.is_game_over():
                        break
                    move = player_move(board, me)
                    if board.is_game_over():
                        break
                    queue.put(move)

        print("FINAL POSITION")
        board.draw()
        if board.is_winner(me):
            print(f"PLAYER {me} WINS!")
        elif board.is_winner(opponent):
            print(f"PLAYER {opponent} WINS!")
        else:
            print(f"DRAW!")
    except grpc.RpcError as e:
        # Handle RPC‑level errors (e.g., connection loss)
        print(f"[Client] RPC error: {e}")
    finally:
        queue.put(None)  # Ask generator to finish


if __name__ == "__main__":
    main()
