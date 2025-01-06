def modules():
  names = '''
    import sqlite3
    import os
    import tkinter as tk
    from tkinter import ttk
    import requests
    from requests.adapters import HTTPAdapter, Retry
    from bs4 import BeautifulSoup
    import urllib.request
    from PIL import Image, ImageTk
    import random
    from collections import Counter
    import re
    import time
    import threading
    import gspread
    from PIL import ImageTk, Image, ImageSequence
    import time
    from tkinter import filedialog as fd
    from tkinter import messagebox
    from urllib.parse import urljoin
    from difflib import SequenceMatcher
    from skimage.metrics import structural_similarity as compare_ssim
    import imageio.v2 as imageio
    import numpy as np
    from datetime import datetime
    from oauth2client.service_account import ServiceAccountCredentials
    from googleapiclient.http import MediaIoBaseDownload
    from googleapiclient.discovery import build
    import warnings
    import tkcalendar
    from tkcalendar import *
    import webbrowser
  '''
  lines = names.split('\n')
  import_names = []
  for line in lines:
      line = line.strip() 
      if line.startswith('import '):
          import_name = line.split(' ')[1]
          import_names.append(import_name)



modules()













