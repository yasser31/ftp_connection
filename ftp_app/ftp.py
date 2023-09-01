from ftplib import FTP
import os
import shutil
import schedule
import time
import logging

# Configure logging
logging.basicConfig(filename='ftp_download.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def download_files(ftp_server, remote_path, local_directory, internal_network_directory):
    """
    This function connects to the ftp server, downloads files and copies them to the internal network
    """
    try:
        # Connect to the FTP server
        ftp = FTP(ftp_server)
        ftp.login()
        ftp.cwd(remote_path)

        # List files in the FTP directory
        file_list = [f for f in ftp.nlst()]

        # Log local directory creation
        if not os.path.exists(local_directory):
            print("Creating local directory")
            logging.info("Creating local directory")
            os.makedirs(local_directory)
        else:
            print("Local directory already exists")
            logging.info("Local directory already exists")

        # Download files from FTP server
        if file_list:
            print(f"Files to be downloaded are {file_list}")
            logging.info(f"Files to be downloaded are {file_list}")
            for file_name in file_list:
                print(f"Downloading {file_name}")
                logging.info(f"Downloading {file_name}")
                local_file_path = os.path.join(local_directory, file_name)
                try:
                    with open(local_file_path, 'wb') as local_file:
                        ftp.retrbinary('RETR ' + file_name, local_file.write) # this line downloads the files
                    print(f"File '{file_name}' downloaded successfully.")
                    logging.info(f"File '{file_name}' downloaded successfully.")
                except Exception as download_err:
                    print(f"Error downloading '{file_name}': {download_err}")
                    logging.error(f"Error downloading '{file_name}': {download_err}")
        else:
            print("File list is empty")
            logging.info("File list is empty")

        # Close the FTP connection
        ftp.quit()

        # Log network directory creation
        if not os.path.exists(internal_network_directory):
            print("Creating network directory")
            logging.info("Creating network directory")
            os.makedirs(internal_network_directory)
        else:
            print("Network directory already exists")
            logging.info("Network directory already exists")

        try:
            for file_name in file_list:
                source_file_path = os.path.join(local_directory, file_name)
                destination_file_path = os.path.join(internal_network_directory, file_name)
                try:
                    shutil.copy(source_file_path, destination_file_path) # this line copies the files
                    print(f"File '{file_name}' copied to internal network successfully.")
                    logging.info(f"File '{file_name}' copied to internal network successfully.")
                except Exception as copy_err:
                    print(f"Error copying '{file_name}': {copy_err}")
                    logging.error(f"Error copying '{file_name}': {copy_err}")
        except Exception as copy_files_err:
            print(f"Error copying files to internal network: {copy_files_err}")
            logging.error(f"Error copying files to internal network: {copy_files_err}")

    except Exception as ftp_err:
        print(f"FTP connection error: {ftp_err}")
        logging.error(f"FTP connection error: {ftp_err}")

def download_and_copy():
    """
    This function calls the download_and_copy function we will use schedule on this function
    """
    ftp_server = 'ftp.us.debian.org'
    remote_path = 'debian'
    local_directory = 'ftp_test_storage'
    internal_network_directory = 'internal_network'

    download_files(ftp_server, remote_path, local_directory, internal_network_directory)


if __name__ == "__main__":
    # Schedule the task to run every day at a specific time (e.g., 2:00 PM)
    schedule.every().day.at("14:00").do(download_and_copy)

    # Keep the script running to allow the scheduled tasks to be executed
    while True:
        schedule.run_pending()
        time.sleep(1)