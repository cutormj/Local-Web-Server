from flask import Flask, request, render_template
import os

app = Flask(__name__)

def list_files(directory):
    # Get a list of all files in the specified directory
    return [filename for filename in os.listdir(directory)]

@app.route('/files')
def display_files():
    target_directory = r'D:\uploads'  # Change this to your actual directory
    files = list_files(target_directory)
    return render_template('list_files.html', files=files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, ssl_context=('https.crt', 'https.key'))

