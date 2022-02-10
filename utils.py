import sys

def validate_argv():
    if len(sys.argv) != 2:
        exit("Error: 2 arguments espected, " + str(len(sys.argv)) + " were given")

    host_port = str(sys.argv[1]).split(":")
    if len(host_port) != 2:
        exit("Error: Invalid IP and port\n\tExample: localhost:8000")

    if not host_port[1].isnumeric():
        exit("Error: The port must be numeric")

    return (host_port[0], int(host_port[1]))