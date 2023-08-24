import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define paths
DOWNLOAD_DIR = os.path.expanduser("~\Downloads")
BRAIN_DIR = os.path.join(DOWNLOAD_DIR, "Brain")
BODY_DIR = os.path.join(DOWNLOAD_DIR, "Body")

def get_folder_name_from_extension(extension):
    # Strip the dot and capitalize
    return extension[1:].upper() + " Files"

def organize_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1]
            folder_name = get_folder_name_from_extension(file_ext)
            
            dest_folder = os.path.join(BODY_DIR, folder_name)
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)

            dest_path = os.path.join(dest_folder, filename)
            os.rename(file_path, dest_path)
            safe_string = f"Moved {filename} to {folder_name}".encode('cp1252', 'replace').decode('cp1252')
            print(safe_string)


class WatcherHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory or event.src_path.startswith(BRAIN_DIR):
            # Do not process directory changes or files in BRAIN_DIR
            return 
        organize_files(DOWNLOAD_DIR)

def main():
    # Ensure BODY_DIR exists
    if not os.path.exists(BODY_DIR):
        os.makedirs(BODY_DIR)

    # Organize existing files
    organize_files(DOWNLOAD_DIR)

    # Setup the watcher
    event_handler = WatcherHandler()
    observer = Observer()
    observer.schedule(event_handler, DOWNLOAD_DIR, recursive=False)  # No recursive, we only monitor DOWNLOAD_DIR
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
