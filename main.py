from flask import Flask, request, render_template
import os

app = Flask(__name__)

def list_files(directory):
    # Get a list of all files in the specified directory
    return [filename for filename in os.listdir(directory)]

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the uploaded file
        uploaded_file = request.files['file']

        # Save the file to D:\uploads
        save_path = os.path.join('D:', 'uploads', uploaded_file.filename)
        uploaded_file.save(save_path)

        return f"File '{uploaded_file.filename}' uploaded successfully!"
    else:
        # Render an HTML form for file upload
        return render_template('upload_form.html')

@app.route('/files')
def display_files():
    target_directory = r'D:\uploads'  # Change this to your actual directory
    files = list_files(target_directory)
    return render_template('list_files.html', files=files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
