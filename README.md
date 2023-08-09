
# Folder Synchronization Tool

This Python script is a simple folder synchronization tool that helps you keep two folders synchronized in a one-way manner. It monitors the source folder for changes and updates the destination (replica) folder accordingly. The synchronization process compares files based on their content using MD5 checksums and updates only the modified or new files. It also deletes files and folders from the destination that are no longer present in the source.


## Features

- One-way synchronization from source to replica folder.
- Compares files based on MD5 checksums to detect changes.
- Deletes files and folders from the replica folder that are not present in the source.
- Provides synchronization logs for monitoring.


## Prerequisites
- Python 3.x
## Usage


1. Make sure you have Python 3.x installed on your system.

2. Save the provided Python script as folder_sync.py.

3. Open a terminal or command prompt.

4. Navigate to the directory containing the folder_sync.py script.

5. Run the script using the following command:

        python folder_sync.py source_folder_path replica_folder_path interval log_file_path




    Replace the placeholders with the actual values:
        
        'source_folder_path': Path to the source folder you want to synchronize from.
        'replica_folder_path': Path to the destination folder you want to synchronize to.
        'interval': Synchronization interval in minutes. The script will run at this interval to check for changes.
        'log_file_path': Path to the log file where synchronization activities will be recorded.



6. The script will start monitoring the source folder and perform synchronization based on the specified interval.

7. To stop the synchronization, you can terminate the script by pressing Ctrl + C in the terminal.
  



## Example
Suppose you have the following folder structure:

    /source_folder
        file1.txt
        folder1/
            file2.txt
            file3.txt


And you want to synchronize it with:

        /replica_folder


You can run the script with the following command:

        python folder_sync.py /source_folder /replica_folder 30 /var/log/folder_sync.log

This will synchronize the source_folder with the replica_folder every 30 minutes and log synchronization activities to /var/log/folder_sync.log.
## Note

The script assumes that you have the necessary permissions to read, write, and delete files and folders in both the source and replica folders.
## Author

- Sagar Tejaraj Javana

