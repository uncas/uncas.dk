import os

from dotenv import load_dotenv
from ftplib import FTP

load_dotenv(override = True)

user = os.getenv("ftp_user")
password = os.getenv("ftp_password")
host = os.getenv("ftp_host")
remote_root = os.getenv("ftp_remote_root")
local = "build"

ftp = FTP(host)
ftp.login(user, password)

def upload_file(file_name, file_path):
	with open(file_path, "rb") as f:
		ftp.storbinary(f"STOR {file_name}", f)

def upload_files_recursively(root_folder, sub_folder = ""):
	folder = root_folder + sub_folder
	remote_folder = remote_root + sub_folder
	print(f"Uploading {folder} to {remote_folder}")
	if len(sub_folder) > 0 and not remote_folder in ftp.nlst(remote_root):
		ftp.mkd(remote_folder)
	ftp.cwd(remote_folder)
	for name in os.listdir(folder):
		path = os.path.join(folder, name)
		if os.path.isdir(path):
			new_sub_folder = sub_folder + "/" + name
			upload_files_recursively(root_folder, new_sub_folder)
		else:
			upload_file(name, path)

upload_files_recursively(local)
