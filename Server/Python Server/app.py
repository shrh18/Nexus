from flask import Flask, render_template
import socket

# Create a new Flask app
app = Flask(__name__)

# Set up a route to serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# Listen for data on port 12345
@app.route('/data')
def data():
    # Create a new socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to localhost port 12345
    sock.bind(('localhost', 12345))

    # Listen for incoming connections
    sock.listen()

    # Accept the connection and receive the data
    conn, addr = sock.accept()
    data = conn.recv(100000)
    conn.close()

    # Return the data to the client
    print(data)
    return data

# Start the server
if __name__ == '__main__':
    app.run(debug=True, port=3000)