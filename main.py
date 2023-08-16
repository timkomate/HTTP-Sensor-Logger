import argparse
import socketserver
import logging
from utils.DataReceiverHandler import DataReceiverHandler


def main():
    parser = argparse.ArgumentParser(
        description="HTTP server for receiving sensor data and storing in a database."
    )
    parser.add_argument(
        "--port", type=int, default=8080, help="Port number for the HTTP server"
    )
    args = parser.parse_args()

    PORT = args.port
    logging.basicConfig(level=logging.INFO)
    with socketserver.TCPServer(("", PORT), DataReceiverHandler) as httpd:
        logging.info("Serving at port %s", PORT)
        httpd.serve_forever()


if __name__ == "__main__":
    main()
