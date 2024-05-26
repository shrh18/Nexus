import socket
host = "localhost"
port = 12345
s = socket.socket()		# TCP socket object
s.bind((host,port))
s.listen(5)

print("Waiting for client...")
conn,addr = s.accept()	        # Accept connection when client connects
print("Connected by ", addr)

# while True:
data = conn.recv(100000)	    # Receive client data
print("---------------------------")
print(data)
	# if not data: break	        # exit from loop if no data
conn.sendall(data)	        # Send the received data back to client
conn.close() 