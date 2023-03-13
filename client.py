import socket

HOST = 'localhost'
PORT = 8888

def play_game():
    while True:
        choice = input("Give your input: ")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if choice == "q":
                print("Quitting")
                s.close()
                break
            if choice == "help":
                print("To get the current status of a game, use the command 'status GAME_ID_HERE'.")
                print("To play a move, use the command 'play GAME_ID_HERE r/p/s' for rock, paper or scissors.")
            else:
                try:
                    s.connect((HOST, PORT))
                    s.sendall(choice.encode('utf-8'))
                    s.settimeout(60.0)
                    data = s.recv(1024).decode('utf-8')
                    print(data)
                except (socket.timeout):
                    print("Oops, something went wrong. Please try again.")


if __name__ == '__main__':
    play_game()