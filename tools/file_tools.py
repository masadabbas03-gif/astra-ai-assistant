from pathlib import Path


def list_files(folder_path):

    try:

        folder = Path(folder_path)

        files = []

        for item in folder.iterdir():

            files.append(item.name)

        return files

    except Exception as e:

        return str(e)


def create_folder(folder_name):

    try:

        folder = Path(folder_name)

        folder.mkdir(exist_ok=True)

        return f"Folder '{folder_name}' created successfully."

    except Exception as e:

        return str(e)
