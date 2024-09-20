import os

def list_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_list.append(os.path.join(root, filename))
    return file_list

if __name__ == '__main__':
    target_directory = r'D:\uploads'  # Change this to your actual directory
    files = list_files(target_directory)
    for file_path in files:
        print(file_path)
