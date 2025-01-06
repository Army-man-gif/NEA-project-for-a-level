from constants import *

def Find_GIFs(x):
    entry = ''
    special_characters = '!@#$%^&*()-_+=[]{}|;:,.<>?/\\'
    special_characters = string.punctuation + special_characters
    special_characters = [char for char in special_characters]
    for i in special_characters:
        if i in x:
          entry = x.replace(i,' ').replace(' ', '+')
    else:
        entry = x.replace(' ', '+')
    url = f'https://tenor.com/en-GB/search/{entry.lower()}-gym-exercise-form-gifs'

    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    holder = soup.find_all('img')

    try:
        for h in holder:
            if h != None and h.get('alt') != ' ':
                if h.get('src').endswith('.gif') and 'ick' not in h.get('alt'):
                    img_url = urljoin(page.url, h.get('src'))
                    h['alt'] = f'{x}'
                    name = h.get('alt') + '.gif'
                    GIF_path = r"C:\Users\khait\OneDrive\Desktop\Project pictures\GIFs"
                    gif_filename = os.path.join(GIF_path, h.get('alt'))
                    gif_filename = gif_filename + '.gif'
                    urllib.request.urlretrieve(h.get('src'), gif_filename)
                    img_name = name.replace('.gif', '.jpg')
                    directory_path = r"C:\Users\khait\OneDrive\Desktop\Project pictures\Images"
                    img_path = os.path.join(directory_path, img_name)
                    # Load the reference image from a file path
                    if os.path.exists(img_path):
                      image = imageio.imread(img_path, mode='L')
                      image = np.array(image)
                    else:
                      Scrape_and_save_Images_Locally_Execution_Function(False,x)
                    # Load the GIF image from the URL

                    gif = Image.open(gif_filename).convert("L")
                    gif = np.array(gif)
                    height, width = image.shape
                    gif = Image.fromarray(gif)
                    gif = gif.resize((width, height), Image.LANCZOS)
                    gif = np.array(gif)
                    similarity = compare_ssim(image, gif)
                    if similarity < 0.5:
                        os.remove(gif_filename)
    except Exception as e:
        print("Exception: ",e)

def Scrape_and_save_GIFs_Locally_Execution_Function(Fill,trial):
  connection = sqlite3.connect("My database")
  c = connection.cursor()
  exer = c.execute('''
  SELECT name FROM Exercise
  ''').fetchall()
  threads = []
  if Fill == True:
    for i in exer:
        t = threading.Thread(target=Find_GIFs,args=(i[0],))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
  else:
      for i in trial:
        t = threading.Thread(target=Find_GIFs,args=(i,))
        threads.append(t)
        t.start()

      for j in threads:
          j.join()


