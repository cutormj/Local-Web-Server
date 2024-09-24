from flask import Flask, request, render_template
import os
import json
import win32print
import win32api
import win32con
import urllib.parse
import win32ui


app = Flask(__name__)

def list_json_files(directory):
    json_data_list = []
    
    # Traverse the directories in the specified directory
    for folder in os.listdir(directory):
        folder_path = os.path.join(directory, folder)
        
        # Check if it is a directory
        if os.path.isdir(folder_path):
            json_file_path = os.path.join(folder_path, 'data.json')
            
            # Check if 'data.json' exists in the directory
            if os.path.exists(json_file_path):
                # Open and read the JSON file
                with open(json_file_path, 'r') as json_file:
                    json_data = json.load(json_file)
                    json_data_list.append(json_data)
    
    return json_data_list

def print_document(file_path, printer_name=None, page_range=None):
    # If printer_name is not provided, use the default printer
    if not printer_name:
        printer_name = win32print.GetDefaultPrinter()
    
    try:
        # Ensure the file exists before trying to print
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Prepare Bullzip-specific arguments for page range
        if page_range:
            # Convert the page range list into a string, e.g., "1,3,5"
            page_range_str = ",".join(map(str, page_range))
            additional_args = f'/pagenumbers:"{page_range_str}"'
        else:
            additional_args = ""

        # Use ShellExecute to print the document with Bullzip PDF Printer's page range
        win32api.ShellExecute(
            0,
            "print",          # Print command
            file_path,        # File to print
            additional_args,  # Additional arguments for Bullzip (page range)
            ".",              # Directory
            0                 # Show window flag
        )
        print(f"Sent '{file_path}' to printer '{printer_name}' with page range '{page_range_str}'.")

    except Exception as e:
        print(f"Failed to print document: {e}")

        
def get_printer_names():
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    printer_names = [printer[2] for printer in printers]
    return json.dumps(printer_names)  # Convert the list to a JSON string

@app.route('/files')
def display_files():
    target_directory = r'D:\uploads'  # Path to the uploads directory
    json_files = list_json_files(target_directory)
    printer_names_json = get_printer_names()  # Get printer names as a JSON string
    printer_names = json.loads(printer_names_json)  # Convert JSON string to Python list
    
    # Render a template that displays the JSON data
    return render_template('list_files.html', json_files=json_files, printer_names=printer_names)

@app.route('/display/<path:encoded_parameter>')
def display_parameter(encoded_parameter):

    print("HELLOW!!: " + encoded_parameter)
    print_document(encoded_parameter, "Bullzip PDF Printer", [1,2])
    # Decode the URL-encoded parameter back to its original form
    decoded_parameter = urllib.parse.unquote(encoded_parameter)
    
    # Render a template that displays the decoded parameter (original file path)
    return render_template('display_parameter.html', param=decoded_parameter)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, ssl_context=('https.crt', 'https.key'))
