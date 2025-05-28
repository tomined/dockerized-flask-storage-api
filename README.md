# Flask File Storage API with Docker, Nginx, and Gunicorn

![Docker Compose Badge](https://img.shields.io/badge/Docker%20Compose-v3.9-blue?style=flat-square&logo=docker)
![Flask Badge](https://img.shields.io/badge/Flask-2.x-lightgray?style=flat-square&logo=flask)
![Nginx Badge](https://img.shields.io/badge/Nginx-latest-green?style=flat-square&logo=nginx)
![Gunicorn Badge](https://img.shields.io/badge/Gunicorn-latest-orange?style=flat-square&logo=gunicorn)
![Python Badge](https://img.shields.io/badge/Python-3.10%2B-blueviolet?style=flat-square&logo=python)
![License Badge](https://img.shields.io/badge/License-MIT-success?style=flat-square) 
A robust and secure RESTful API for file storage, built with Flask, served by Gunicorn, and reverse-proxied by Nginx with SSL/TLS, all containerized using Docker. This setup provides a scalable and production-ready environment for managing files.

## Table of Contents

1.  [Features](#features)
2.  [Project Structure](#project-structure)
3.  [Prerequisites](#prerequisites)
4.  [Getting Started](#getting-started)
    * [1. Generate Self-Signed SSL Certificates](#1-generate-self-signed-ssl-certificates)
    * [2. Build and Run Docker Containers](#2-build-and-run-docker-containers)
5.  [API Endpoints](#api-endpoints)
    * [Base URL](#base-url)
    * [Listing Files (GET /files)](#listing-files-get-files)
    * [Filtering Files (GET /files/filter)](#filtering-files-get-filesfilter)
    * [Downloading a File (GET /files/<filename>)](#downloading-a-file-get-filesfilename)
    * [Uploading a New File (POST /files/<filename>)](#uploading-a-new-file-post-filesfilename)
    * [Overwriting/Updating a File (PUT /files/<filename>)](#overwritingupdating-a-file-put-filesfilename)
    * [Appending a Line to a File (POST /files/<filename>/append_line)](#appending-a-line-to-a-file-post-filesfilenameappend_line)
    * [Deleting a File (DELETE /files/<filename>)](#deleting-a-file-delete-filesfilename)
    * [Root Endpoint (GET /)](#root-endpoint-get-)
6.  [Troubleshooting](#troubleshooting)
    * [`curl -k` not working in PowerShell](#curl--k-not-working-in-powershell)
7.  [License](#license)
8.  [Contributing](#contributing)

## Features

* **RESTful API:** Standard HTTP methods (GET, POST, PUT, DELETE) for file operations.
* **Secure File Storage:** Basic file management with `secure_filename` for safety.
* **Dockerized Environment:** Easy setup and consistent environment across different systems.
* **Gunicorn:** Production-ready WSGI HTTP server for Flask applications.
* **Nginx Reverse Proxy:** Handles incoming requests, provides SSL/TLS termination, and proxies requests to the Flask app.
* **HTTPS (SSL/TLS):** Configured with self-signed certificates for local development, ensuring secure communication.
* **CORS Enabled:** Allows cross-origin requests for easier development and integration.
* **Persistent Storage:** File uploads are stored in a Docker volume, mapping to a local directory for data persistence.

## Project Structure
```
.
├── app/
│   ├── app.py                   # Flask application logic
│   ├── Dockerfile               # Dockerfile for building the Flask app image
│   └── requirements.txt         # Python dependencies
├── nginx/
│   ├── certs/                   # Directory for SSL certificates (ignored by Git)
│   │   ├── server.crt           # Self-signed SSL certificate
│   │   └── server.key           # Self-signed SSL private key
│   └── nginx.conf               # Nginx configuration for reverse proxy and SSL
├── .gitignore                   # Specifies untracked files to be ignored by Git
├── docker-compose.yml           # Defines and configures the multi-container Docker application
├── README.md                    # Project README file
└── LICENSE                      # Project license file
```

## Prerequisites

Before you begin, ensure you have the following installed on your system:

* **Docker Desktop:** Includes Docker Engine and Docker Compose.
    * [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
* **OpenSSL:** For generating self-signed SSL certificates.
    * Usually pre-installed on Linux/macOS. For Windows, it's often included with Git Bash or can be downloaded separately (e.g., from [https://wiki.openssl.org/index.php/Binaries](https://wiki.openssl.org/index.php/Binaries)).
* **`curl` or Postman/Insomnia:** For testing the API endpoints.

## Getting Started

Follow these steps to get your Flask File Storage API up and running using Docker Compose.

### 1. Generate Self-Signed SSL Certificates

Nginx requires SSL certificates to enable HTTPS. For local development, we'll generate self-signed certificates.

1.  **Navigate to the `nginx/certs` directory:**
    ```bash
    cd nginx/certs
    ```

2.  **Generate the certificates using OpenSSL:**
    ```bash
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt -subj "/CN=localhost"
    ```
    * `openssl req`: Utility for creating and processing certificate requests.
    * `-x509`: Creates a self-signed certificate instead of a certificate request.
    * `-nodes`: No DES encryption for the private key (no passphrase needed).
    * `-days 365`: Certificate valid for 365 days.
    * `-newkey rsa:2048`: Generates a new 2048-bit RSA private key.
    * `-keyout server.key`: Outputs the private key to `server.key`.
    * `-out server.crt`: Outputs the certificate to `server.crt`.
    * `-subj "/CN=localhost"`: Sets the Common Name (CN) to `localhost`, which is crucial for local testing.

3.  **Return to the project root directory:**
    ```bash
    cd ../..
    ```

### 2. Build and Run Docker Containers

From the project root directory, use Docker Compose to build the images and start the services.

1.  **Build the Docker images and start the containers in detached mode:**
    ```bash
    docker compose up --build -d
    ```
    * `--build`: Forces Docker Compose to rebuild images (useful when Dockerfile or dependencies change).
    * `-d`: Runs containers in detached mode (in the background).

2.  **Verify that the containers are running:**
    ```bash
    docker compose ps
    ```
    You should see both `app` and `nginx` containers in a `running` state.

## API Endpoints

The API is accessible via HTTPS on `https://localhost`. When testing with `curl` or similar tools, you might need to use the `-k` or `--insecure` flag to bypass self-signed certificate warnings.

### Base URL

`https://localhost` (proxied by Nginx to the Flask app)

### Listing Files (GET /files)

Retrieves a list of all files currently stored on the server, including their names and sizes.

* **URL:** `https://localhost/files`
* **Method:** `GET`
* **Response:**
    ```json
    [
        {"name": "example.txt", "size": 123},
        {"name": "another_file.pdf", "size": 45678}
    ]
    ```
* **Example (using curl):**
    ```bash
    curl -k https://localhost/files
    ```

---

### Filtering Files (GET /files/filter)

Retrieves a list of files whose names contain a specific search string (case-insensitive).

* **URL:** `https://localhost/files/filter`
* **Method:** `GET`
* **Query Parameters:**
    * `search_string` (required): The string to search for within file names.
* **Response:**
    ```json
    [
        {"name": "document.txt", "size": 1234},
        {"name": "another_document.pdf", "size": 5678}
    ]
    ```
    (Returns an empty array `[]` if no matching files are found.)
* **Error Response:**
    ```json
    {"error": "Parameter 'search_string' is required."}
    ```
    (If `search_string` is not provided.)
* **Example (using curl):**
    ```bash
    curl -k https://localhost/files/filter?search_string=doc
    ```
    ```bash
    curl -k https://localhost/files/filter?search_string=report
    ```

---

### Downloading a File (GET /files/<filename>)

Downloads a specific file by its name.

* **URL:** `https://localhost/files/<filename>` (replace `<filename>` with the actual file name)
* **Method:** `GET`
* **Response:** The raw content of the file.
* **Example (using curl):**
    ```bash
    curl -k https://localhost/files/my_document.txt
    ```

### Uploading a New File (POST /files/<filename>)

Uploads a new file to the server. If a file with the same name already exists, it will return a `409 Conflict` error.

* **URL:** `https://localhost/files/<filename>`
* **Method:** `POST`
* **Request Body:** The raw content of the file.
* **Headers:** `Content-Type: text/plain` (or appropriate MIME type for binary files)
* **Response:**
    ```json
    {"message": "File 'your_file.txt' saved."}
    ```
* **Example (using curl):**
    ```bash
    curl -k -X POST -H "Content-Type: text/plain" --data "Hello, this is content for a new file." https://localhost/files/new_file.txt
    ```

### Overwriting/Updating a File (PUT /files/<filename>)

Uploads a file to the server, overwriting it if it already exists, or creating a new one if it doesn't.

* **URL:** `https://localhost/files/<filename>`
* **Method:** `PUT`
* **Request Body:** The raw content of the file.
* **Headers:** `Content-Type: text/plain` (or appropriate MIME type)
* **Response:**
    ```json
    {"message": "File 'your_file.txt' overwritten."}
    ```
* **Example (using curl):**
    ```bash
    curl -k -X PUT -H "Content-Type: application/octet-stream" --data-binary @path/to/local/image.jpg https://localhost/files/my_image.jpg
    # Or for text:
    curl -k -X PUT -H "Content-Type: text/plain" --data "This will overwrite existing content or create new." https://localhost/files/existing_file.txt
    ```

### Appending a Line to a File (POST /files/<filename>/append_line)

Appends a new line of text to an existing file. Each appended text will start on a new line.

* **URL:** `https://localhost/files/<filename>/append_line`
* **Method:** `POST`
* **Request Body:** The text string to append.
* **Headers:** `Content-Type: text/plain`
* **Response:**
    ```json
    {"message": "Line appended to file 'your_file.txt'."}
    ```
* **Example (using curl):**
    ```bash
    curl -k -X POST -H "Content-Type: text/plain" --data "This is a new line to add." https://localhost/files/my_log.txt/append_line
    ```

### Deleting a File (DELETE /files/<filename>)

Deletes a specific file from the server.

* **URL:** `https://localhost/files/<filename>`
* **Method:** `DELETE`
* **Response:**
    ```json
    {"message": "File 'your_file.txt' deleted."}
    ```
    or
    ```json
    {"error": "File does not exist."}
    ```
* **Example (using curl):**
    ```bash
    curl -k -X DELETE https://localhost/files/file_to_delete.txt
    ```

### Root Endpoint (GET /)

A simple endpoint to confirm the API is running.

* **URL:** `https://localhost/`
* **Method:** `GET`
* **Response:**
    ```json
    {"message": "REST API Flask + Gunicorn + NGINX + Docker"}
    ```
* **Example (using curl):**
    ```bash
    curl -k https://localhost/
    ```

## Troubleshooting

### `curl -k` not working in PowerShell

If you encounter an error like `"Invoke-WebRequest : A parameter cannot be found that matches parameter name 'k'"` when using `curl` in PowerShell, it's because `curl` in PowerShell is an alias to `Invoke-WebRequest`, which has a different syntax and the `-k` parameter is not available in older PowerShell versions.

**Solutions:**

1.  **Use Git Bash:** If you have Git for Windows installed, open "Git Bash" from your Start Menu. This terminal provides a true `curl` executable.
    ```bash
    # In Git Bash
    curl -k https://localhost/files
    ```
2.  **Use Command Prompt (CMD):** If you have a standalone `curl.exe` installed and added to your system's PATH, CMD will use it directly.
    ```cmd
    # In CMD
    curl -k https://localhost/files
    ```
3.  **Install true `curl` via Winget (for newer Windows):** Open PowerShell **as Administrator** and run `winget install curl.curl`. Then, restart your terminal and explicitly use `curl.exe`.
    ```powershell
    # In PowerShell after installing curl via winget
    curl.exe -k https://localhost/files
    ```
4.  **Use `Invoke-WebRequest` with `-SkipCertificateCheck` (for PowerShell 6.0+):** If you have PowerShell 6.0 (or newer) installed (check `$PSVersionTable`), you can use the correct parameter.
    ```powershell
    # In PowerShell 6.0+
    Invoke-WebRequest -Uri https://localhost/files -SkipCertificateCheck | Select-Object -ExpandProperty Content
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to fork this repository, open issues, and submit pull requests.