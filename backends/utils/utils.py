import os


def create_folder(upload_path):
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
