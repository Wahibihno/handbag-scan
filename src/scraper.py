from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import cloudscraper
import time
import csv
import os 

#Setup browsers
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

#Cloudscaper to simulate java app 
scraper_img = cloudscraper.create_scraper()

#Setup file 
os.makedirs("data/images" , exist_ok= True)
csv_file = open('data/dataset_bag.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
writer.writerow(['brand', 'model', 'price', 'img_file'])

#Setup page numbering 
base_url = "https://fr.vestiairecollective.com/search/p-{}/?q=sac"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
} 

#Loop scraping
for page in range(1,5) :
    url = base_url.format(page)
    print(f"\nExtrect from {page} page : {url}")

    #Get request with Selenium
    driver.get(url)
    
    print("Défilement de la page pour charger les images...")
    for i in range(5):
        driver.execute_script("window.scrollBy(0, 1500);")
        time.sleep(1) 

    #Extract data from html using Selenium's page_source
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    box_handbag = soup.find_all('a', class_='product-card_productCard__sGjCz')

    if not box_handbag :
        print(f"Empty page : {page}")
        continue 

    #Extract the details for each bag in the current page
    for bag in box_handbag :
        brand_tag = bag.find('span', attrs={'data-cy': 'productCard__text__brand'})
        description_tag = bag.find('span', attrs={'data-cy': 'productCard__text__name'})
        price_tag = bag.find('span', attrs={'data-cy': 'productCard__text__price__discount'})
        img_tag = bag.find('img')

        if not brand_tag or not description_tag or not price_tag or not img_tag :
            continue

        #Clear the data -> from html to usable data 
        brand = brand_tag.text.strip()
        description = description_tag.text.strip()
        price = price_tag.text.strip()
        img_url = img_tag.get('src')
        
        # Security: ensure we don't grab a dummy image pixel
        if not img_url or "vestiairecollective" not in img_url:
            continue

        #Save the data
        img_name = f"{brand}_{description}.jpg".replace(" ", "_").replace("/", "_")
        img_path = f"data/images/{img_name}"
        
        # Download image using cloudscraper instead of requests
        img_response = scraper_img.get(img_url, headers=headers)

        if img_response.status_code == 200 :
            img_file = open(img_path, 'wb')
            img_file.write(img_response.content)
            img_file.close()
            print(f"Saved : {brand} {description}")
        else :
            print(f"Error {img_response.status_code} to save {description}")
            continue

        writer.writerow([brand, description, price, img_path])

driver.quit()
csv_file.close()
print("\nScraping done !")