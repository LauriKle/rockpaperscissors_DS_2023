import socket
import os
import sqlite3
import time
import sys

HOST = ''
PORT = 8000
DELAYTIME = 5

if not os.path.exists('game.db'):
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE games
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  first_move TEXT,
                  second_move TEXT,
                  result TEXT)''')
    conn.commit()
    conn.close()


def get_result(first_move, second_move):
    if first_move == second_move:
        return "It's a tie!"
    elif (first_move == 'r' and second_move == 's') or \
         (first_move == 'p' and second_move == 'r') or \
         (first_move == 's' and second_move == 'p'):
        return "The first move won!"
    else:
        return "The second move won!"

def save_result(id, first_move, second_move, result):
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM games WHERE id=?", (id,))
    count = c.fetchone()[0]
    if count == 0:
        c.execute("INSERT INTO games (id, first_move, second_move, result) VALUES (?, ?, ?, ?)", (id, first_move, second_move, result))
    else:
        c.execute("UPDATE games SET first_move=?, second_move=?, result=? WHERE id=?", (first_move, second_move, result, id))
    conn.commit()
    conn.close()

def get_game_data(id):
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute("SELECT id, first_move, second_move, result FROM games WHERE id=?", (id,))
    row = c.fetchone()
    conn.close()
    if row is None:
        return None
    else:
        return (row[0], row[1], row[2], row[3])

def attempt_to_play_move(id, move):
    data = get_game_data(id)
    if data is not None:
        if data[1] != "None" and data[2] == "None":
            res = get_result(data[1], move)
            save_result(id, data[1], move, res)
            outcome = res
        elif data[1] != "None" and data[2] != "None":
            outcome = "That game is already completed. Try another game Id."
        else:
            outcome = "Something weird happened. Couldn't play game."
    else:
        save_result(id, move, "None", "In progress")
        outcome = "Played your hand."
    return outcome

def send_data_back(conn, data):
    try:
        if DELAYTIME > 0:
            print(f"Sleeping for {DELAYTIME} seconds. Krooh pyyh...")
            time.sleep(DELAYTIME)
        conn.settimeout(5.0)
        conn.sendall(data.encode('utf-8'))
        print(f"Sent back data: {data}")
    except (socket.timeout):
        print("Connection timed out.")

def interpret_input(conn):
    try:
        input = conn.recv(1024).decode('utf-8')
        print(input)
        conn.settimeout(5.0)
        input = input.split(" ")
        if input[0] == "status":
            try:
                game_id = int(input[1])
                stat = get_game_data(game_id)
                if stat is not None:
                    answer = ' '.join([str(elem) for elem in stat])
                    send_data_back(conn, answer)
                else:
                    send_data_back(conn, "There is no game with that id yet.")
            except (IndexError, ValueError):
                send_data_back(conn, "Invalid status command syntax.")
        elif input[0] == "play":
            try:
                game_id = int(input[1])
                move = input[2].lower()
                if move not in ['r', 'p', 's']:
                    raise ValueError
                outcome = attempt_to_play_move(game_id, move)
                send_data_back(conn, outcome)

            except (IndexError, ValueError):
                send_data_back(conn, "Invalid play command syntax.")
        else:
            send_data_back(conn, ("Command not identified."))
    except Exception as exc:
        print(f"Got an exception: {exc}")
        conn.close()

def start():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            socket.setdefaulttimeout(5.0)
            s.bind((HOST, PORT))
            s.listen()
            while True:
                conn, address = s.accept()
                print(f"Got a connection from address {address}")
                interpret_input(conn)
    except Exception as exc:
        print(f"Got an exception. Goodbye. {exc}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
            print(f"Starting on port {PORT}.")
        except ValueError:
            print(f"Port Arg was not an integer. Starting on port {PORT}.")
        if len(sys.argv) > 2:
            try:
                DELAYTIME = int(sys.argv[2])
                print(f"Using an artificial delay of {DELAYTIME} seconds.")
            except ValueError:
                print(f"Arg 2 was not an integer. Setting delay time to 0.")
                DELAYTIME = 0
    else:
        print(f"No port given in args. Starting on port {PORT}.")
    start()