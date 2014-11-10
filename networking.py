import socket

def open_socket(port):
    """
    Opens a socket on the given port
    """
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sk.bind(("", port))
    sk.listen(1)
    return sk

def recv_msg(conn):
    """
    Receives a message from the socket.
    """
    try:
        # Unwrap message length header
        header = conn.recv(8).decode("UTF-8")
        length = int(header)
        body = conn.recv(length)
        return body
    except:
        raise IOError()
        return None
    
def recv_str(conn):
    """
    Convenience method for reading a string
    from the socket.
    """
    return recv_msg(conn).decode("UTF-8")

def send_msg(conn, msg):
    """
    Sends a message out the socket.
    """
    try:
        # Prepend message length header
        length = len(msg)
        msg = bytes(str(length).ljust(8), "UTF-8") + msg
        conn.send(msg)
    except:
        raise IOError()
        return None
    
def send_str(conn, msg, log = False):
    """
    Convenience method for sending a string
    out the socket.
    """
    length = len(msg)
    msg = bytes(str(length).ljust(8), "UTF-8") + bytes(msg, "UTF-8")
    conn.send(msg)
    if log:
        print(msg)
    
def broadcast_msg(conns, msg):
    """
    Sends a message out to all given connections
    """
    for conn in conns:
        send_msg(conn, msg)
        
def broadcast_str(conns, msg, log = False):
    """
    Convenience method for broadcasting a string
    out the given list of sockets.
    """
    for conn in conns:
        send_str(conn, msg)
    if log:
        print(msg)
    