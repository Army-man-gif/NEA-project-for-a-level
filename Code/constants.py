from basics import *
import json
import sqlite3
import os
import re
import babel
from babel import numbers
import tkinter as tk
from tkinter import ttk,filedialog as fd,messagebox

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib.request

from PIL import Image,ImageTk, Image, ImageSequence
import math
import random
from collections import Counter


import threading
import gspread
import time

import imageio.v2 as imageio
import numpy as np
from datetime import datetime, timedelta

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build

import string
import shutil

import tkcalendar
from tkcalendar import *

import mplcursors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
# Formatting

root = tk.Tk()
root.attributes('-fullscreen', True)
H = 600
W=600
geo = f"{W}x{H}"
root.geometry(geo)
root.title("Gym") 
root['background']='white'

# Constants
add = 0
border = 0
tabs = {}
Buttons = {}
frames = []
file_extension = '.jpg'

texts = ["Profile","Workouts display","Display database in treeview","History","Workout graph summaries","Caloric stuff","Calendar"]
tab_strings = [f'tab{i+1}' for i in range(len(texts))]
colours = [f'#{random.randint(0,255):02X}{random.randint(0,255):02X}{random.randint(0,255):02X}' for i in range(len(texts))]



def tab_search(search):
  index = texts.index(search)
  value = tab_strings[index]
  return tabs[value]



