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