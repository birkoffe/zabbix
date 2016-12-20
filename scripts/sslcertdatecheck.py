#!/usr/bin/python

from datetime import datetime
import socket
import ssl

def main():
    """ Print days to cert expire """
    host = "google.com"
    port = 443

    ctx = ssl.create_default_context()
    sock = ctx.wrap_socket(socket.socket(), server_hostname=host)
    sock.connect((host, port))
    cert = sock.getpeercert()

    print (datetime.fromtimestamp(ssl.cert_time_to_seconds(cert['notAfter']))-datetime.now()).days

if __name__ == '__main__':
    main()
