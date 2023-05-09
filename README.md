# HTTP-Simulator

## First The function.py ((ReliableUDP))

A python implementation of Reliable UDP protocol that provides reliable data transmission between two processes over an unreliable network.

### Introduction

Reliable UDP is a transport protocol that adds reliability to the User Datagram Protocol (UDP) by providing reliable data transmission between two processes over an unreliable network. It is designed for use in situations where a reliable connection-oriented protocol such as TCP is too expensive.

### Usage
- Clone the repository.

```
$ git clone https://github.com/kyrillosishak/HTTP-Simulator.git
```

- Install the required dependencies.
```
$ pip install -r requirements.txt
```

- Import the ReliableUDP class into your code and initialize an object.
```
from function import ReliableUDP
udp = ReliableUDP()
```
- Sending Data
```
send("Name of the file")
```

- Reciving Data
```
data = recieve()
```
