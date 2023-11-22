# Sensor Data Receiver and Database Storage

This project implements an HTTP server that receives sensor data through POST requests and stores it in a MariaDB database. It provides a simple way to send sensor readings and store them for later analysis.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Example](#example)
- [Contributing](#contributing)

## Overview

The project consists of an HTTP server and a data handler module. The HTTP server listens for incoming POST requests containing JSON sensor data. The data is processed and stored in a MariaDB database. Additionally, the server provides a basic HTML page for information on how to send POST requests.

## Installation

1. Clone this repository:

```git clone https://github.com/timkomate/HTTP-Sensor-Logger.git```

2. Install the required dependencies (Python 3.9+):

```pip install mariadb```

## Usage
Set up your MariaDB database and update the config.json and secrets.json files with your database configuration and credentials.

Start the HTTP server:

```python main.py --port 8080```

Replace 8080 with the desired port number.

To post data to the database, use the following command:

```curl -X POST -H "Content-Type: application/json" -d '{"table:" "test_data" "humidity": 50, "temperature": 20}' http://localhost:8080/```

## Configuration
`config.json`: Configuration settings for the HTTP server and database connection.
`secrets.json`: Secret configuration settings, including database credentials.
`configs/`: Example configuration files for reference.

## Example
Example POST request to send sensor data:

```
{
  "table": "test_data"
  "humidity": 50,
  "temperature": 20
}
```

## Contributing

Contributions are welcome! Feel free to open issues or pull requests for bug fixes, improvements, or new features.
