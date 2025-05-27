from flask import Flask, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

# Initialize the Flask application
app = Flask(__name__)

# --- Configuration ---
# Directory to store uploaded files
FILES_DIR = 'files'
# Create the files directory if it doesn't exist
os.makedirs(FILES_DIR, exist_ok=True)

# --- CORS Configuration (Optional but recommended for API access from different origins) ---
# Import CORS extension for Flask
from flask_cors import CORS
# Enable CORS for all routes (r"/*") allowing requests from any origin ("*").
# In a production environment, you might want to restrict 'origins' to specific domains.
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/files", methods=["GET"])
def list_files():
    """
    Endpoint to list all files stored in the FILES_DIR.
    Returns a JSON array of file objects, each containing the file's name and size.
    """
    files = []
    # Iterate through all items in the files directory
    for f in os.listdir(FILES_DIR):
        file_path = os.path.join(FILES_DIR, f)
        # Check if the item is a file (not a directory)
        if os.path.isfile(file_path):
            files.append({"name": f, "size": os.path.getsize(file_path)})
    # Return the list of files with a 200 OK status
    return jsonify(files), 200

@app.route("/files/<filename>", methods=["GET"])
def get_file(filename):
    """
    Endpoint to download a specific file.
    Securely handles the filename to prevent directory traversal attacks.
    """
    # Sanitize the filename to ensure it's safe for file system operations
    filename = secure_filename(filename)
    file_path = os.path.join(FILES_DIR, filename)

    # Check if the requested file exists in the designated directory
    if os.path.isfile(file_path):
        # Serve the file as an attachment, prompting download
        return send_from_directory(FILES_DIR, filename, as_attachment=True)
    # If the file does not exist, return a 404 Not Found error
    return jsonify({"error": "File not found."}), 404

@app.route("/files/<filename>", methods=["POST"])
def upload_file_post(filename):
    """
    Endpoint to upload a new file using the POST method.
    If a file with the same name already exists, it returns a 409 Conflict error.
    The file content is expected in the request body.
    """
    # Sanitize the filename
    filename = secure_filename(filename)
    file_path = os.path.join(FILES_DIR, filename)

    # Check if a file with the given name already exists to prevent overwriting with POST
    if os.path.exists(file_path):
        return jsonify({"error": "File already exists."}), 409

    # Get the raw binary data from the request body
    data = request.get_data()
    try:
        # Write the received data to the specified file in binary write mode
        with open(file_path, 'wb') as f:
            f.write(data)
        # Return a success message with a 201 Created status
        return jsonify({"message": f"File '{filename}' saved."}), 201
    except Exception as e:
        # Handle any potential errors during file writing
        return jsonify({"error": str(e)}), 500

@app.route("/files/<filename>", methods=["PUT"])
def upload_file_put(filename):
    """
    Endpoint to upload or overwrite a file using the PUT method.
    If the file exists, it will be overwritten; otherwise, a new file will be created.
    The file content is expected in the request body.
    """
    # Sanitize the filename
    filename = secure_filename(filename)
    file_path = os.path.join(FILES_DIR, filename)

    # Get the raw binary data from the request body
    data = request.get_data()
    try:
        # Open the file in binary write mode ('wb'). This will create the file if it doesn't exist
        # or truncate (clear) it if it does, then write the new data.
        with open(file_path, 'wb') as f:
            f.write(data)
        # Return a success message with a 200 OK status
        return jsonify({"message": f"File '{filename}' overwritten."}), 200
    except Exception as e:
        # Handle any potential errors during file writing
        return jsonify({"error": str(e)}), 500

@app.route("/files/<filename>", methods=["DELETE"])
def delete_file(filename):
    """
    Endpoint to delete a specific file.
    Securely handles the filename.
    """
    # Sanitize the filename
    filename = secure_filename(filename)
    file_path = os.path.join(FILES_DIR, filename)

    # Check if the file exists before attempting to delete
    if os.path.exists(file_path):
        try:
            # Remove the file from the file system
            os.remove(file_path)
            # Return a success message with a 200 OK status
            return jsonify({"message": f"File '{filename}' deleted."}), 200
        except Exception as e:
            # Handle any potential errors during file deletion (e.g., permissions)
            return jsonify({"error": str(e)}), 500
    # If the file does not exist, return a 404 Not Found error
    return jsonify({"error": "File does not exist."}), 404

@app.route("/files/<filename>/append_line", methods=["POST"])
def append_line_post(filename):
    """
    Endpoint to append a new line of text to an existing file using the POST method.
    The text to append is expected in the request body as plain text.
    Each appended text will start on a new line.
    """
    # Sanitize the filename
    filename = secure_filename(filename)
    file_path = os.path.join(FILES_DIR, filename)

    # Ensure the file exists before attempting to append
    if not os.path.exists(file_path):
        return jsonify({"error": "File does not exist."}), 404

    # Get the data to append from the request body, interpreted as text
    data_to_append = request.get_data(as_text=True)

    # Validate if any data was provided in the request body
    if not data_to_append:
        return jsonify({"error": "No data to append provided."}), 400

    try:
        # Open the file in append mode ('a'), which adds content to the end of the file.
        # 'encoding='utf-8'' ensures proper handling of various characters.
        with open(file_path, 'a', encoding='utf-8') as f:
            # Prepend a newline character before the received data to ensure it starts on a new line
            f.write('\n' + data_to_append)
        # Return a success message with a 200 OK status
        return jsonify({"message": f"Line appended to file '{filename}'."}), 200
    except Exception as e:
        # Handle any potential errors during file appending
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    """
    Root endpoint providing a welcome message for the API.
    """
    # Returns a simple JSON message indicating the API's technology stack
    return jsonify({"message": "REST API Flask + Gunicorn + NGINX + Docker"}), 200

if __name__ == "__main__":
    # Run the Flask app directly when the script is executed.
    # In a production environment, Gunicorn (or another WSGI server) would handle this.
    # debug=True: Enables debug mode, providing detailed error messages and auto-reloading.
    # host="0.0.0.0": Makes the server accessible from any IP address (important for Docker containers).
    # port=8000: Specifies the port the Flask app will listen on.
    app.run(debug=True, host="0.0.0.0", port=8000)