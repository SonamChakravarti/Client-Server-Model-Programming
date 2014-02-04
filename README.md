About The Repository

This repository has python files to demonstrate client-server model for Go Back  and Selective N Automatic Repeat Requests protocols. The programs transfer files between a client and server with SFTP. The architecture involved is as follows:
The Simple-FTP server plays the role of the receiver in the reliable data transfer, and the Simple-FTP client plays the role of the sender. All data transfer is from sender (client) to receiver (server) only; only ACK packets travel from receiver to sender.
