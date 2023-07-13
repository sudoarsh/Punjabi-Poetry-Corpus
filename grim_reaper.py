import csv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
 
input_file = 'updated_urls.csv'
output_file = 'output.csv'

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(['Poet', 'Title', 'Poem'])

    with open(input_file, 'r', encoding='utf-8') as urlsfile:
        reader = csv.reader(urlsfile)

        total_urls = sum(1 for _ in reader)

        urlsfile.seek(0)

        progress_bar = tqdm(total=total_urls, desc='Scraping Progress', unit='URL')

        for row in reader:
            url = row[0] 

            response = requests.get(url)

            soup = BeautifulSoup(response.text, 'html.parser')

            h1_tag = soup.find('h1')
            poet = h1_tag.text.split(':')[1].strip() if h1_tag and len(h1_tag.text.split(':')) > 1 else None

            poem_sections = soup.find_all('div', class_='section')

            for section in poem_sections:
                h3_tag = section.find('h3')
                title = h3_tag.text if h3_tag else None

                p_tag = section.find('p')
                poem = p_tag.text if p_tag else None

                if poem is None:
                    continue

                print('Poet:', poet)
                print('Title:', title)
                print('Poem:', poem)
                print('---')

                writer.writerow([poet, title, poem])

            progress_bar.update(1)

        progress_bar.close()
