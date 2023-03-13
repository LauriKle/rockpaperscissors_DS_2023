import socket
import time
import sys
import mysql.connector

HOST = '0.0.0.0'
PORT = 8000
DELAYTIME = 0

def connect_db():
    try:
        return mysql.connector.connect(
            host="sqlhost",
            port="3306",
            user="root",
            password="password",
            database="game"
        )
    except mysql.connector.Error as exc:
        print("DB connection failed: {}".format(exc))
        return None

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
    cnx = connect_db()
    if cnx == None:
        return "Something went wrong. Try again later."
    cursor = cnx.cursor()
    cursor.execute("INSERT INTO games (id, first_move, second_move, result) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE first_move=%s, second_move=%s, result=%s",
                            (id, first_move, second_move, result, first_move, second_move, result))
    cnx.commit()
    cursor.close()
    cnx.close()

def get_game_data(id):
    cnx = connect_db()
    if cnx == None:
        return None
    cursor = cnx.cursor()
    cursor.execute("SELECT id, first_move, second_move, result FROM games WHERE id=%s", (id,))
    row = cursor.fetchone()
    cursor.close()
    cnx.close()
    if row is None:
        return "That game doesn't exist yet."
    else:
        return (row[0], row[1], row[2], row[3])

def attempt_to_play_move(id, move):
    data = get_game_data(id)
    if data is None:
        return "Something went wrong. Try again later."
    elif data == "That game doesn't exist yet.":
        save_result(id, move, "None", "In progress")
        return "Played your hand."
    if type(data) == tuple:
        if data[2] != "None":
            return "That game is already completed. Try another game Id."
        else:
            result = get_result(data[1], move)
            save_result(id, data[1], move, result)
            return result
    else:
        print("Something went wrong.")
        return "Something went wrong. Try again later."

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
                   res = response = ' '.join(str(elem) for elem in stat)
                   send_data_back(conn, res)
                else:
                    send_data_back(conn, "Something went wrong. Try again later.")
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