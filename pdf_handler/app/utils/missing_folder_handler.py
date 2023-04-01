import os

def missing_folder_handler():
    folder_names = ["docs","output","temp"]
    dir_base=os.environ["PRIVATE_FOLDER"]
    for name in folder_names:
        path=f"{dir_base}/{name}"
        isExist = os.path.exists(path)
        if (not isExist):
            os.makedirs(path)
            print(f"{path} is created",flush=True)