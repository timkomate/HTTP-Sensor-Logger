import http.server
import datetime
import socketserver
import mariadb
import json
import logging

class DataReceiverHandler(http.server.SimpleHTTPRequestHandler):
    @staticmethod
    def load_json(filename):
        with open(filename, "r") as json_file:
            return json.load(json_file)

    def __init__(self, *args, **kwargs):
        self.config = self.load_json("config.json")
        self.secret_data = self.load_json("secret.json")
        super().__init__(*args, **kwargs)

    def do_POST(self):
        try:
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")
            logging.info("Received POST data: %s", post_data)

            data = json.loads(post_data)
            humidity = data.get("humidity")
            temperature = data.get("temperature")

            if humidity is None or temperature is None:
                self.send_response(400)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write("Missing or invalid data".encode("utf-8"))
                return

            now = datetime.datetime.utcnow()

            insert_data_into_database(now, humidity, temperature)

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            response = "Thanks for the POST request!"
            self.wfile.write(response.encode("utf-8"))
        except Exception as e:
            logging.error("Error processing POST request: %s", e)
            self.send_error(500, "Internal Server Error")

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = """
            <html>
            <head><title>Post Data to Database</title></head>
            <body>
            <h1>Post Data to Database</h1>
            <p>To post data to the database, send a POST request to this URL with the data in JSON format:</p>
            <pre>curl -X POST -H "Content-Type: application/json" -d '{{"humidity": 50, "temperature": 20}}' http://{}/</pre>
            </body>
            </html>
            """.format(self.server.server_address[0])
            self.wfile.write(html.encode("utf-8"))
        else:
            super().do_GET()

def insert_data_into_database(timestamp, humidity, temperature):
    try:
        with mariadb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_DATABASE,
        ) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO Data_ESP8266 (date, humidity, temperature) VALUES (?, ?, ?)",
                (timestamp, humidity, temperature),
            )
            conn.commit()
    except mariadb.Error as e:
        logging.error("Error connecting to MariaDB: %s", e)

def main():
    logging.basicConfig(level=logging.INFO)
    with socketserver.TCPServer(("", PORT), DataReceiverHandler) as httpd:
        logging.info("Serving at port %s", PORT)
        httpd.serve_forever()

if __name__ == "__main__":
    main()

