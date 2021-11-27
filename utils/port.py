import socket


def detectPort(port=6666) :

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", port))
        s.shutdown(2)
        sign =  True
    except Exception :
        sign = False
    s.close()

    return sign