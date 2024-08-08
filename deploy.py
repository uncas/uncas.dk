import os

from dotenv import load_dotenv
from ftplib import FTP

load_dotenv(override = True)

user = os.getenv("ftp_user")
password = os.getenv("ftp_password")
host = os.getenv("ftp_host")
remote_root = os.getenv("ftp_remote_root")
local_root = "build"

ftp = FTP(host)
ftp.login(user, password)

def upload_file(file_name, file_path):
	with open(file_path, "rb") as f:
		ftp.storbinary(f"STOR {file_name}", f)

def upload_files_recursively(local_folder = local_root, remote_folder = remote_root, child_folder = ""):
	local_folder_path = local_folder
	remote_folder_path = remote_folder
	if len(child_folder) > 0:
		local_folder_path = local_folder + "/" + child_folder
		remote_folder_path = remote_folder + "/" + child_folder
		if not remote_folder_path in ftp.nlst(remote_folder):
			print(f"Creating folder {child_folder} in {remote_folder}")
			ftp.cwd(remote_folder)
			ftp.mkd(child_folder)
	print(f"Uploading {local_folder_path} to {remote_folder_path}")
	for name in os.listdir(local_folder_path):
		ftp.cwd(remote_folder_path)
		path = os.path.join(local_folder_path, name)
		if os.path.isdir(path):
			upload_files_recursively(local_folder_path, remote_folder_path, name)
		else:
			upload_file(name, path)

upload_files_recursively()
