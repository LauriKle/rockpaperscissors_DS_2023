import socket

HOST = 'localhost'
PORT = 8888

def play_game():
    print("=Rock-Paper-Scissors Client=")
    print('Type "help" to get a list of the commands you can use.')
    while True:
        choice = input("Give your input: ")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if choice == "q":
                print("Quitting")
                s.close()
                break
            if choice == "help":
                print('To get the current status of a game, use "status GAME_ID_HERE". Example: status 0')
                print('To play a move, use "play GAME_ID_HERE r/p/s" for rock, paper or scissors. Example: play 0 r')
                print('To quit this client, use "q"')
            else:
                try:
                    s.connect((HOST, PORT))
                    s.sendall(choice.encode('utf-8'))
                    s.settimeout(60.0)
                    data = s.recv(1024).decode('utf-8')
                    print(data)
                except (socket.timeout):
                    print("Something went wrong. Please try again.")


if __name__ == '__main__':
    play_game()