# TCP-implementation-using-UDP

Ahmed Hassan Falah 6737
Alaa Hossam Abu-hashima 6750
Kyrillos Gayed Ishak 6804

Project overview:
It is required to implement TCP over UDP connection to be able to make UDP reliable to send TCP packets over it such as HTTP which uses TCP protocol. So as known UDP is connectionless and not reliable so we may suffer from data loss and corruption. Now we need to implement:

1- Three-way handshaking.
2- Error detection algorithm (here we implement checksum).
3- Method to detect packet corruption.
4- Method to retransmit the lost or corrupted packets. (stop-and-wait algorithm)
5- Method to detect duplicate packets and ignore resending them.
6- HTTP server on top of the implemented TCP using UCP.

Problems we face:

We had a problem in stop-and-wait usage since there is a probability of deadlock occurrence but it occurs rarely when we use localhost server connection.

Assumptions:

We assume that we need to implement TCP over UDP so we implement some functions to make UDP reliable.

We assume we needn’t to implement congestion control method.

Explanation:

1) Firstly, we need start implementing the connection using sockets:

  ▪ Creating a socket from built-in socket library: socket (AF_INET, SOCK_DGRAM)
    AF_INET: using for IP Address family.
    SOCK_DGRAM: datagram service for UDP.
  
  ▪ Identifying a socket; in other words, we need to assign a transport address to the socket. Using system call bind.
  
  ▪ Waiting for incoming connection by implementing function called listen() to check for connections all the time.
  
  ▪ Sending and receiving data with functions send() and receive()
  
  ▪ Dividing data into packets with implementing functions:

    breakPackets(): split the packet information to be used into data, sequence number, acknowledge number, checksum, packet type, length and ID.

    createPacket(): creating single packet with information consists of all info resulted from breakPackets() function concatenated together.

    listPackets(): to list the chunks of data into list and send them in their order.
2) Now we need to make functions for error detection so we implement two functions:
  
  The first function is: calculatechecksum() for calculating the checksum of the packet given some info
  
  The second function is: validateChecksum() to compare the calculated checksum with the given checksum and if they are no equal, then there is an error detected. Else, there is no error detected.

3) Simulate packet loss and packet corruption with function packetcorruption() by randomly changing one byte in the packet with a certain probability and packet loss with function packetloss() by discarding the packet with a certain probability.

4) Check packet loss or corruption by cekPacket() function which checks whether the reply id in the server side is equivalent to packet id in the client or not , calculated checksum equals the given checksum or not and checks the reply type and packet type.

5) Send The packets from sender to receiver with checking the validation of the data packets transmitted.

6) Now we concern in how to use HTTP server in our implementation; we write the HTTP header in a file then:
  ▪ open this file and read data written in it.
  
  ▪ Parsing this header into request method (GET or POST), URL, payload and http version.
  
  ▪ Check the request method if it is GET, then the server will be sender and client will be receiver. If it is POST, then the client will be as a sender and server will be as a receiver.
  
  ▪ Check the URL if it is valid, create another output file and write “200 OK”.
      If it is not valid, write “404 NOT FOUND” in the output file.

This code is a Python class called ReliableUDP that implements a simple version of the User Datagram Protocol (UDP) that guarantees reliable delivery of data packets between two endpoints over an unreliable network. The class defines several methods that are responsible for various aspects of packet creation, transmission, and reception, as well as error checking and correction.
The class begins by defining four class-level constants that represent the types of packets that can be sent between the two endpoints: SYN , SYN_ACK, DATA, ACK, FIN, and FIN_ACK. It also defines several other constants that represent various packet and buffer sizes, as well as the default port number that the class listens on.

The ReliableUDP class defines several methods that are responsible for various aspects of packet creation, transmission, and reception, as well as error checking and correction. The createPacket() method is used to create a packet from its constituent parts, including the packet type, identifier, sequence number, length, checksum, and data payload. The breakPacket() method is used to extract the individual fields of a packet that has been received, while the validateChecksum() method checks whether the packet's checksum is correct.

The createListPacket() method is used to split a file into a list of packets, each of which can be transmitted independently. It first opens the specified file using the openFile() method and then iteratively creates packets from the file's contents, appending each one to the list until the entire file has been processed. The final packet in the list is a special FIN packet that indicates that the file has been completely transmitted.

The sendFile() method is used to send a file to a specified endpoint by transmitting each packet in the file one at a time and waiting for an acknowledgement (ACK) from the recipient after each transmission. If an ACK is not received within a specified timeout period, the packet is retransmitted. This process continues until all packets have been successfully transmitted and acknowledged, or until a maximum number of retries has been reached.

The receiveFile() method is used to receive a file from a specified endpoint by listening for incoming packets on the specified port number and assembling them into a list of packets until the FIN packet is received. The method then sends an acknowledgement (FIN_ACK) to the sender and returns the assembled packets as a single byte string.

The initialize() method is used to initialize an array of a given size with a specified value. The convertIntToNByte() method is used to convert an integer to a byte string of a specified length.
Finally, the cekPacket() method is used to check whether a received packet is valid and whether it corresponds to the expected packet, given the context of the current transmission. It checks the packet's type, identifier, sequence number, length, and checksum against the corresponding fields of the original packet to ensure that the packet has been received intact and that it corresponds to the expected packet in the current transmission context.

Testcases:
  Attached with the project file, you will see four test cases:
    • one for HTTP GET request and the result is 200 OK and the needed data.
    • one for HTTP POST request and the result is 200 OK.
    • One HTTP GET request and the result is 404 NOT FOUND.
    • One HTTP POST request and the result is 404 NOT FOUND.
