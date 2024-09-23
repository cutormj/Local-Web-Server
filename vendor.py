from flask import Flask, request, render_template
import os
import json
import win32print
import win32api
import win32con
import urllib.parse

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

def print_document(file_path):
    # Get the default printer
    printer_name = "Microsoft Print to PDF"
    
    try:
        # Check if the printer is available
        printer_info = win32print.GetPrinter(win32print.OpenPrinter(printer_name), 2)
        
        # Print the file
        win32api.ShellExecute(
            0,
            "print",
            file_path,
            f'/d:"{printer_name}"',
            ".",
            0
        )
        
        print("Print job submitted successfully.")
        
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
    print_document(encoded_parameter)
    # Decode the URL-encoded parameter back to its original form
    decoded_parameter = urllib.parse.unquote(encoded_parameter)
    
    # Render a template that displays the decoded parameter (original file path)
    return render_template('display_parameter.html', param=decoded_parameter)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, ssl_context=('https.crt', 'https.key'))
