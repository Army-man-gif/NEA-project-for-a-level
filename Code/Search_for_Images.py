from constants import *
  

def Find_Images(x):
    entry = ''
    special_characters = '!@#$%^&*()-_+=[]{}|;:,.<>?/\\'
    special_characters = string.punctuation + special_characters
    special_characters = [char for char in special_characters]
    for i in special_characters:
        if i in x:
          entry = x.replace(i,' ').replace(' ', '+')
    else:
        entry = x.replace(' ', '+')
    url = f'https://uk.images.search.yahoo.com/search/images;_ylt=AwrkPPD3O8Zkjaclgj8M34lQ;_ylu=Y29sbwNpcjIEcG9zAzEEdnRpZAMEc2VjA3BpdnM-?p={entry}+gym+exercises&fr2=piv-web&type=E210GB91082G0&fr=mcafee'
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    holder = soup.find('img')
    if holder is not None:
        if holder and 'src' in holder.attrs:
            img_url = holder['src']
        elif holder and 'data-src' in holder.attrs:
            img_url = holder['data-src']
        else:
                print(f"Image not found for {entry}")

        holder['alt'] = f'{x}'
        try:
            img_url = holder['data-src']
            name = holder['alt']+file_extension
            urllib.request.urlretrieve(img_url,f'{base_path}/{name}')
        except:
            try:
                img_url = holder['src']
                name = holder['alt']+'.jpg'
                urllib.request.urlretrieve(img_url,f'{base_path}/{name}')
            except Exception as e:
                print(e)

def Scrape_and_save_Images_Locally_Execution_Function(Fill,trial):  
  connection = sqlite3.connect("My database")
  c = connection.cursor()
  exer = c.execute('''
  SELECT name FROM Exercise
  ''').fetchall() 
  threads = []
  if Fill == True:
      for i in exer:
        t = threading.Thread(target=Find_Images,args=(i[0],))
        threads.append(t)
        t.start()

      for j in threads:
          j.join()
  else:
      for i in trial:
        t = threading.Thread(target=Find_Images,args=(i,))
        threads.append(t)
        t.start()

      for j in threads:
          j.join()
