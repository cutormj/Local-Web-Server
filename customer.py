from flask import Flask, request, render_template
import os
import uuid
import json
import mimetypes


app = Flask(__name__)

def list_files(directory):
    # Get a list of all files in the specified directory
    return [filename for filename in os.listdir(directory)]

def save_file_with_unique_id(uploaded_file, save_directory, form_data):
    # Generate a unique folder name using UUID
    unique_id = str(uuid.uuid4().hex[:9].upper())
    folder_path = os.path.join(save_directory, unique_id)
    
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
    
    # Save the uploaded file inside the unique folder
    file_path = os.path.join(folder_path, uploaded_file.filename)
    uploaded_file.save(file_path)
    
    # Detect the file type (MIME type) based on the uploaded file's extension
    file_type, _ = mimetypes.guess_type(uploaded_file.filename)
    
    # Save the form data as a JSON file in the same folder
    json_data = {
        "id": unique_id,
        "file": file_path,
        "file_type": file_type,  # Add file type to JSON data
        "copies": form_data['copies'],
        "paper_size": form_data['paper_size'],
        "color_mode": form_data['color_mode'],
        "page_range": form_data['page_range'],
        "duplex": form_data['duplex'],
        "orientation": form_data['orientation'],
        "print_quality": form_data['print_quality'],
        "collate": form_data['collate']
    }
    
    json_file_path = os.path.join(folder_path, 'data.json')
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    
    # Return the folder name (or path) for reference
    return unique_id

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the uploaded file
        uploaded_file = request.files['file']
        
        # Collect the form data
        form_data = {
            'filename' : uploaded_file.filename,
            'copies': request.form['copies'],
            'paper_size': request.form['paper-size'],
            'color_mode': request.form['color-mode'],
            'page_range': request.form['page-range'],
            'duplex': 'Yes' if 'duplex' in request.form else 'No',
            'orientation': request.form['orientation'],
            'print_quality': request.form['print-quality'],
            'collate': 'Yes' if 'collate' in request.form else 'No'
        }

        # Directory to save the file
        save_directory = os.path.join('D:', 'uploads')

        # Save the uploaded file and form data
        unique_folder_name = save_file_with_unique_id(uploaded_file, save_directory, form_data)

        # Render a different HTML file with the success message and the folder path
        return render_template('upload_success.html', 
                               folder_name=unique_folder_name, 
                               **form_data)
    
    else:
        # Render the upload form
        return render_template('upload_form.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, ssl_context=('https.crt', 'https.key'))
