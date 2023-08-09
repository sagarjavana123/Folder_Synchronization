"""
@package Folder_Synch.py
@brief   Python script to synchronize two folders in one way manner.
@ToRun   python Folder_Synch.py Arg1 Arg2 Arg3 Arg4
          Arg1 : source_folder_path, Path to the source folder
          Arg2 : replica_folder_path, Path to the destination folder
          Arg3 : interval, Synchronization interval in minutes
          Arg4 : log_file_path, Path to the log file
"""

import os
import shutil
import argparse
import hashlib
import time
import logging
import sys


def calculate_md5(file_path):
    """
    Calculates the MD5 hash of a given file and returns the computed MD5 hash as a hexadecimal string.
    :param file_path: Path of file for which MD5 hash needs to be calculated
    :return: MD5 hash as a hexadecimal
    """
    with open(file_path, 'rb') as f:
        md5 = hashlib.md5()
        while chunk := f.read(8192):
            md5.update(chunk)
    return md5.hexdigest()


class FolderSync:
    """
    This class is created to have two folders synchronized in one way manner.
    """
    def __init__(self, source_folder, replica_folder, interval, log_file):
        self.source_folder = source_folder
        self.replica_folder = replica_folder
        self.interval = interval
        self.log_file = log_file

        # Set up logging
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    def validate_inputs(self):
        """
        This method validates the provided inputs.
        :return: None
        """
        # Validating the provided inputs
        if not os.path.exists(self.source_folder):
            logging.error("\n***** Argument Error *****\nSource folder does not exist!")
            exit(1)

        if not os.path.exists(self.replica_folder):
            print("\n***** Argument Error *****\nDestination folder does not exist!")
            logging.error("\n***** Argument Error *****\nDestination folder does not exist!")
            exit(1)

        if not os.path.exists(os.path.dirname(self.log_file)):
            logging.error("\n***** Argument Error *****\nLogfile directory folder does not exist!")
            exit(1)

        if self.interval.isdigit():
            self.interval = int(self.interval) * 60
        else:
            logging.error(f"\n***** Argument Error *****\n'{self.interval}' can not be converted into integer.")
            exit(1)

    def synch_folders(self):
        """
        This method synchronize two folders in one-way.
        :return: None
        """
        try:
            # If we use this part of code then we can avoid deletion code part
            # Remove existing files and folders from destination
            # shutil.rmtree(replica_folder)
            # os.makedirs(replica_folder)

            # Copy all the files to destination folder
            for root, _, files in os.walk(self.source_folder):
                for file in files:
                    source_file_path = os.path.join(root, file)
                    replica_file_path = source_file_path.replace(self.source_folder, self.replica_folder, 1)

                    if not os.path.exists(replica_file_path) or\
                            calculate_md5(source_file_path) != calculate_md5(replica_file_path):
                        os.makedirs(os.path.dirname(replica_file_path), exist_ok=True)
                        shutil.copy2(source_file_path, replica_file_path)
                        logging.info(f"File copied: {source_file_path} --> {replica_file_path}")

            # Delete the files and folders which are not present in source folder
            for root, dirs, files in os.walk(self.replica_folder):
                for file in files:
                    replica_file_path = os.path.join(root, file)
                    source_file_path = os.path.join(self.source_folder,
                                                    os.path.relpath(replica_file_path, self.replica_folder))

                    if not os.path.exists(source_file_path):
                        os.remove(replica_file_path)
                        logging.info(f"File Removed: {replica_file_path}")
                for dir_ in dirs:
                    replica_folder_path = os.path.join(root, dir_)
                    source_file_path = os.path.join(self.source_folder,
                                                    os.path.relpath(replica_folder_path, self.replica_folder))

                    if not os.path.exists(source_file_path):
                        shutil.rmtree(replica_folder_path)
                        logging.info(f"Folder Removed: {replica_folder_path}")

            logging.info(f"Synchronization completed at: {time.ctime()}")
        except Exception as synch_error:
            logging.info(f"Error occurred during synchronization: {synch_error}")

    def run(self):
        """
        This method defines sequence of the synchronization tool.
        :return: None
        """
        self.validate_inputs()
        while True:
            self.synch_folders()
            time.sleep(self.interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="One way folder Synchronization Program")
    parser.add_argument("source_folder_path", help="Path to the source folder")
    parser.add_argument("replica_folder_path", help="Path to the destination folder")
    parser.add_argument("interval", help="Synchronization interval in minutes")
    parser.add_argument("log_file_path", help="Path to the log file")
    args = parser.parse_args()

    sync_instance = FolderSync(args.source_folder_path, args.replica_folder_path,
                               args.interval, args.log_file_path)

    # Tool processing starts here
    sync_instance.run()
