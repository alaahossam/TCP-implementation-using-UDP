import random
import sys
import time
import socket
import click

cache = {}


class ReliableUDP:
    flag = 0

    def __init__(self):
        self.DATA = b'\x00'
        self.ACK = b'\x01'
        self.FIN = b'\x02'
        self.FIN_ACK = b'\x03'
        self.SYN = b'\x04'
        self.SYN_ACK = b'\x05'
        self.MAX_DATA = 32768
        self.LISTEN_PORT = 6789
        self.MAX_SENT = 33000
        self.MAX_PROGRESS = 40
        self.file = self.initialize(16, bytes(0))
        self.fileSequence = self.initialize(16, 1)

    def createListPacket(self, filename):
        data_byte = self.openFile(filename)
        identifier = (random.randint(0, 15)).to_bytes(1, byteorder='big')
        listPacket = []
        count_seq = 1
        with click.progressbar(length=int(len(data_byte) / self.MAX_DATA), label='Preprocessing files....') as bar:
            while len(data_byte) > self.MAX_DATA:
                bar.update(1)
                data = data_byte[0:self.MAX_DATA]
                data_byte = data_byte[self.MAX_DATA:]
                Type = self.DATA
                Seq = count_seq.to_bytes(2, byteorder="big")
                length = len(data).to_bytes(2, byteorder="big")
                checksum = self.calculateChecksum(Type, identifier, Seq, length, data)
                packet = self.createPacket(Type, identifier, Seq, length, checksum, data)
                count_seq += 1
                listPacket.append(packet)

        Type = self.FIN
        Seq = count_seq.to_bytes(2, byteorder="big")
        length = len(data_byte).to_bytes(2, byteorder="big")
        checksum = self.calculateChecksum(Type, identifier, Seq, length, data_byte)
        packet = self.createPacket(Type, identifier, Seq, length, checksum, data_byte)
        listPacket.append(packet)
        ReliableUDP().flag = 1
        return listPacket

    def createPacket(self, tipe, identifier, Seq, length, checksum, data):
        combine = (int.from_bytes(tipe, byteorder="big") << 4) | (int.from_bytes(identifier, byteorder="big"))
        Type_id = combine.to_bytes(1, byteorder="big")

        return Type_id + Seq + length + checksum + data

    def breakPacket(self, packet):
        Type = (packet[0] >> 4).to_bytes(1, byteorder='big')
        ID = (packet[0] & 15).to_bytes(1, byteorder='big')
        Seq = packet[1:3]
        length = packet[3:5]
        checksum = packet[5:7]
        data = packet[7:]
        return Type, ID, Seq, length, checksum, data

    def calculateChecksum(self, Type, ID, Seq, length, data):
        pppp = ((int.from_bytes(Type, byteorder='big') << 4) + int.from_bytes(ID, byteorder='big')).to_bytes(1,
                                                                                                             byteorder='big') + Seq + length + data

        piecePacket = pppp[0:2]
        pppp = pppp[2:]
        calculateCheck = int.from_bytes(piecePacket, byteorder='big')

        while len(pppp) > 2:
            satuanPiecePacket = pppp[0:2]
            pppp = pppp[2:]
            calculateCheck = calculateCheck ^ int.from_bytes(satuanPiecePacket, byteorder='big')

        calculateCheck = calculateCheck ^ int.from_bytes(pppp, byteorder='big')

        return calculateCheck.to_bytes(2, byteorder='big')

    def validateChecksum(self, packet):
        Type, ID, Seq, length, checksum, data = self.breakPacket(packet)
        calculateCheck = self.calculateChecksum(Type, ID, Seq, length, data)
        if int.from_bytes(calculateCheck, byteorder='big') == int.from_bytes(checksum, byteorder='big'):
            return True
        else:
            return False

    def convertIntToNByte(self, integer, n):
        return integer.to_bytes(n, byteorder='big')

    def openFile(self, filename):
        data = open(filename, "rb")
        dataByte = data.read()
        data.close()
        return dataByte

    def writeFile(self, byte, filename):
        f = open(filename, "wb+")
        f.write(byte)
        f.close()

    def initialize(self, size, element):
        array = [element] * size
        return array

    def cekPacket(self, totalPacket, packet, reply):
        if reply == bytes(0):
            return False

        sendtype, sendid, sendseq, sendlen, sendchksum, senddata = self.breakPacket(packet)
        replytype, replyid, replyseq, replylen, replychksum, replydata = self.breakPacket(reply)

        if (int.from_bytes(replyseq,
                           byteorder='big') < totalPacket) and replytype == self.ACK and sendtype == self.DATA:
            if self.validateChecksum(reply):
                if sendid == replyid and sendseq == replyseq:
                    return True
                else:
                    return False
            else:
                return False
        elif (int.from_bytes(replyseq, byteorder='big') == totalPacket) and (replytype == self.FIN_ACK) and (
                sendtype == self.FIN):
            if self.validateChecksum(reply):
                if sendid == replyid and sendseq == replyseq:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    # send a file to host
    def sendFile(self, host, listenPort, filename, senderSock):
        try:
            listPacket = self.createListPacket(filename)
        except IOError:
            print("File not found")
            return

        totalPacket = len(listPacket)
        i = 0
        with click.progressbar(length=totalPacket, label='Sending files..........') as bar:
            while i < totalPacket:

                packet = listPacket[i]
                bar.update(1)
                start = time.time()
                try:
                    senderSock.sendto(packet, (host, listenPort))
                except socket.error:
                    print("Error in sending packet")
                try:
                    reply, (addr, port) = senderSock.recvfrom(self.MAX_SENT)
                except socket.error:
                    pass
                end = time.time()
                timeout = end - start
                reply = bytes(0)
                while timeout <= 0.5 and not self.cekPacket(totalPacket, packet, reply):
                    try:
                        reply, (addr, port) = senderSock.recvfrom(self.MAX_SENT)
                    except socket.error:
                        pass
                    end = time.time()
                    timeout = end - start
                if self.cekPacket(totalPacket, packet, reply):
                    i += 1
            ReliableUDP().flag = 1

    def processPacket(self, packetReceived, addr, LISTEN_PORT, senderSock):
        if self.validateChecksum(packetReceived):
            valid = True
            tipe, identifier, sequence, length, checksum, data = self.breakPacket(packetReceived)
            if self.fileSequence[int.from_bytes(identifier, byteorder='big')] >= int.from_bytes(sequence,
                                                                                                byteorder='big'):
                if tipe == self.DATA:
                    replyType = self.ACK
                elif tipe == self.FIN:
                    replyType = self.FIN_ACK
                else:
                    valid = False
                    print("Packet data type is not valid, data type is " + str(tipe))

                if valid and self.fileSequence[int.from_bytes(identifier, byteorder='big')] == int.from_bytes(sequence,
                                                                                                              byteorder='big'):
                    self.file[int.from_bytes(identifier, byteorder='big')] += data
                    self.fileSequence[int.from_bytes(identifier, byteorder='big')] += 1

            else:
                valid = False

            if valid:
                if replyType == self.FIN_ACK:
                    print("Writing File...", "output")
                    self.writeFile(self.file[int.from_bytes(identifier, byteorder='big')],
                                   "output")
                replyChecksum = self.calculateChecksum(replyType, identifier, sequence,
                                                       self.convertIntToNByte(0, 2), bytes(0))
                replyPacket = self.createPacket(replyType, identifier, sequence, self.convertIntToNByte(0, 2),
                                                replyChecksum, bytes(0))
                senderSock.sendto(replyPacket, (addr, LISTEN_PORT))
                return self.file[int.from_bytes(identifier, byteorder='big')], replyType
        else:
            print("Packet checksum is not valid")


def simulate_packet_loss(packet, loss_probability):
    """
    Simulates packet loss by randomly discarding the packet with a certain probability.
    """
    if random.random() < loss_probability:
        return None  # packet is lost
    else:
        return packet


def simulate_packet_corruption(packet, corruption_probability):
    """
    Simulates packet corruption by randomly changing one byte in the packet with a certain probability.
    """
    packet = bytearray(packet)
    for i in range(len(packet)):
        if random.random() < corruption_probability:
            packet[i] = random.randint(0, 255)
    return bytes(packet)


def send(filename):
    myhost = "127.0.0.1"
    host = '127.0.0.1'
    UDP = ReliableUDP()
    try:
        listenPort = 12345

    except:
        print("Invalid port")
        sys.exit()

    try:
        senderSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # print("Socket sender opened")
    except socket.error:
        print('Failed to create socket. Error Code : ' + socket.error)
        sys.exit()

    try:

        senderSock.bind((myhost, listenPort))
        # print('Socket bind to port :' + str(listenPort))
    except socket.error:
        print('Bind failed. Error Code : ' + str(socket.error))
        sys.exit()
    # 3 way HandShake
    time.sleep(0.000000000000002)
    senderSock.sendto(UDP.SYN, (host, UDP.LISTEN_PORT))
    reply, (addr, port) = senderSock.recvfrom(UDP.MAX_SENT)
    senderSock.setblocking(False)
    if reply == UDP.SYN_ACK:
        print("Three way Handshake Succeeded.")
        print()
        UDP.sendFile(host, UDP.LISTEN_PORT, filename, senderSock)
        senderSock.close()
    else:
        print("Three way Handshake Failed.")


def receive():
    host = "127.0.0.1"
    UDP = ReliableUDP()
    listenPort = 12345

    file = UDP.initialize(16, bytes(0))
    fileSequence = UDP.initialize(16, 1)

    try:
        receiverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # print('Socket created')
    except socket.error:
        print('Failed to create socket. Error Code : ' + socket.error)
        sys.exit()

    try:
        receiverSock.bind((host, UDP.LISTEN_PORT))
        # print('Socket bind to port:' + str(UDP.LISTEN_PORT))
    except socket.error:
        print('Bind failed. Error Code : ' + str(socket.error))
    count = 0
    reply, (addr, port) = receiverSock.recvfrom(UDP.MAX_SENT)
    if reply == UDP.SYN:
        print("Three way Handshake Succeeded.")
        receiverSock.sendto(UDP.SYN_ACK, (host, listenPort))
    else:
        print("Three way handshake failed.")
    while True:
        packetReceived, (addr, port) = receiverSock.recvfrom(UDP.MAX_SENT)
        # loss_probability = 0.1  # 10% probability of packet loss
        # packet = self.simulate_packet_loss(packet, loss_probability)
        # if packet is None:
        #     print("Packet lost!")
        # else:
        #     print("Packet not lost.")

        data, tipe = UDP.processPacket(packetReceived, addr, listenPort, receiverSock)
        count += 1
        if tipe == UDP.FIN_ACK:
            break
        print()

    receiverSock.close()
    return data



def send1(filename, port, binding):
    myhost = "127.0.0.1"
    host = '127.0.0.1'
    UDP = ReliableUDP()
    UDP.LISTEN_PORT = port
    try:
        listenPort = 12345

    except:
        print("Invalid port")
        sys.exit()

    try:
        senderSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # print("Socket sender opened")
    except socket.error:
        print('Failed to create socket. Error Code : ' + socket.error)
        sys.exit()

    try:

        senderSock.bind((myhost, binding))
        # print('Socket bind to port :' + str(listenPort))
    except socket.error:
        print('Bind failed. Error Code : ' + str(socket.error))
        sys.exit()
    # 3 way HandShake
    time.sleep(0.000000000000002)
    senderSock.sendto(UDP.SYN, (host, UDP.LISTEN_PORT))
    reply, (addr, port) = senderSock.recvfrom(UDP.MAX_SENT)
    senderSock.setblocking(False)
    if reply == UDP.SYN_ACK:
        print("Three way Handshake Succeeded.")
        print()
        UDP.sendFile(host, UDP.LISTEN_PORT, filename, senderSock)
        senderSock.close()
    else:
        print("Three way Handshake Failed.")


def receive1(listenPort, binding):
    host = "127.0.0.1"
    UDP = ReliableUDP()

    file = UDP.initialize(16, bytes(0))
    fileSequence = UDP.initialize(16, 1)

    try:
        receiverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # print('Socket created')
    except socket.error:
        print('Failed to create socket. Error Code : ' + socket.error)
        sys.exit()

    try:
        receiverSock.bind((host, binding))
        # print('Socket bind to port:' + str(UDP.LISTEN_PORT))
    except socket.error:
        print('Bind failed. Error Code : ' + str(socket.error))
    count = 0
    reply, (addr, port) = receiverSock.recvfrom(UDP.MAX_SENT)
    if reply == UDP.SYN:
        print("Three way Handshake Succeeded.")
        receiverSock.sendto(UDP.SYN_ACK, (host, listenPort))
    else:
        print("Three way handshake failed.")
    while True:
        packetReceived, (addr, port) = receiverSock.recvfrom(UDP.MAX_SENT)
        # loss_probability = 0.1  # 10% probability of packet loss
        # packet = self.simulate_packet_loss(packet, loss_probability)
        # if packet is None:
        #     print("Packet lost!")
        # else:
        #     print("Packet not lost.")

        data, tipe = UDP.processPacket(packetReceived, addr, listenPort, receiverSock)
        count += 1
        if tipe == UDP.FIN_ACK:
            break
        print()

    receiverSock.close()
    return data
