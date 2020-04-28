import os
import requests
import pandas as pd
from tqdm import tqdm

folder = os.path.join(os.getcwd(), 'springer_pdfs')

if not os.path.exists(folder):
    os.mkdir(folder)
    
if not os.path.exists(os.path.join(folder, "table.xlsx")):
    books = pd.read_excel('https://resource-cms.springernature.com/springer-cms/rest/v1/content/17858272/data/v4')
    books.to_excel(os.path.join(folder, 'table.xlsx'))
else:
    books = pd.read_excel(os.path.join(folder, 'table.xlsx'), index_col=0, header=0)
print('Downloading . . .')

for url, title, author, pk_name in tqdm(books[['OpenURL', 'Book Title', 'Author', 'English Package Name']].values):
    new_folder = os.path.join(folder, pk_name)

    if not os.path.exists(new_folder):
        os.mkdir(new_folder)

    r = requests.get(url) 
    my_url = r.url
    my_url = my_url.replace('/book/','/content/pdf/')
    my_url = my_url.replace('%2F','/')
    my_url = my_url + '.pdf'

    final_url = my_url.split('/')[-1]
    final_url = title.replace(',','-').replace('.','').replace('/',' ').replace(':',' ')\
            + ' - ' + author.replace(',','-').replace('.','').replace('/',' ').replace(':',' ') + ' - ' + final_url
    output_file = os.path.join(new_folder, final_url)

    if not os.path.exists(output_file.encode('utf-8')):
        myfile = requests.get(my_url, allow_redirects=True)
        try:
            open(output_file.encode('utf-8'), 'wb').write(myfile.content)
        except OSError: 
            print("Error: PDF filename is appears incorrect.")

print('Download finished.')