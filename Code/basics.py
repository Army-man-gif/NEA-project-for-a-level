import sqlite3
import requests
import os
import subprocess
import gspread
import ast
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
def find_folder(target_folder_name):
    parent_folder_path = os.getcwd()
    if "Code" in parent_folder_path:

        # Check the OneDrive Desktop path
        #print(f"Checking {parent_folder_path_onedrive}")
        if os.path.exists(parent_folder_path) and os.path.isdir(parent_folder_path):
            for item in os.listdir(parent_folder_path):
                item_path = os.path.join(parent_folder_path, item)

                if os.path.isdir(item_path) and item == target_folder_name:
                    return item_path
        
        return None
    else:


        # Check the OneDrive Desktop path
        parent_folder_path = os.path.join(os.getcwd(), "Code")
        #print(f"Checking {parent_folder_path_onedrive}")
        if os.path.exists(parent_folder_path) and os.path.isdir(parent_folder_path):
            for item in os.listdir(parent_folder_path):
                item_path = os.path.join(parent_folder_path, item)
                if os.path.isdir(item_path) and item == target_folder_name:
                    return item_path
        else:
            return None
def find_file(file_name):
    
    parent_folder_path = os.getcwd()
    if "Code" not in parent_folder_path:
        parent_folder_path = os.path.join(os.getcwd(),"Code")
    if os.path.exists(parent_folder_path) and os.path.isdir(parent_folder_path):
        for item in os.listdir(parent_folder_path):
            item_path = os.path.join(parent_folder_path, item)
            if item == file_name:
                return item_path
    else:
        return None

project_pictures_folder = find_folder("Project pictures")
base_path = rf'{project_pictures_folder}/Images'
print(base_path)
def main(search):

  # List all files and directories in the specified directory
  global contents
  contents = os.listdir(base_path)
  # Iterate over the contents and do something with each item (file or directory)
  for filename in contents:
    if filename == search:
      file_path = os.path.join(base_path, filename)
      return file_path
    else:
      pass

Database_path = str(find_file('My database'))
connection = sqlite3.connect(Database_path)
c = connection.cursor()
