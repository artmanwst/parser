import requests
from bs4 import BeautifulSoup
import csv

csv_file_path = 'results1.csv'
count = 0

with open(csv_file_path, mode='w', encoding='utf-8', newline='') as csv_file:
    fieldnames = ['ID товара', 'Наименование', 'Ссылка на товар', 'Регулярная цена', 'Промо цена', 'Бренд']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    writer.writeheader()

    for i in range(1, 14):
        url = f'https://online.metro-cc.ru/category/chaj-kofe-kakao/kofe?page={i}'
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            product_blocks = soup.find_all('div', class_='catalog-2-level-product-card')

            for product_block in product_blocks:
                if count < 100:
                    product_id = product_block.get('data-sku')
                    count += 1
                    availability_button = soup.find('button', {'class': 'product-availability-status'})
                    product_name_element = product_block.find('a', class_='product-card-name__text')
                    product_name = product_name_element.text.strip() if product_name_element else None
                    
                    product_link_element = product_block.find('a', class_='product-card-photo__link')
                    product_link = product_link_element['href'] if product_link_element else None

                    regular_price_element = product_block.find('span', class_='product-price__sum-rubles')
                    regular_price = regular_price_element.text.strip() if regular_price_element else None
                    
                    promo_price_element = product_block.find('span', class_='product-range-prices__item-price-actual')
                    promo_price = promo_price_element.find('span', class_='product-price__sum-rubles').text.strip() if promo_price_element else None
                    
                    brand_element = product_block.find('span', class_='product-unit-prices__actual-wrapper')
                    brand = brand_element.find('span', class_='product-unit-prices__actual').text.strip() if brand_element else None
                    url_next = f'https://online.metro-cc.ru{product_link}'
                    response_2 = requests.get(url_next)
                    soup = BeautifulSoup(response_2.text, 'html.parser')
                    name = soup.find('h1', class_='product-page-content__product-name')
                    
                    brand_label = soup.find_all('a', class_='product-attributes__list-item-link')
                    brand_value = brand_label[0].text.strip()
                    product_name = name.text.strip().split(',')[0]
                    
                    if regular_price is not None:
                        in_stock = True
                    
                    if in_stock is True:
                        writer.writerow({
                            'ID товара': product_id,
                            'Наименование': product_name,
                            'Ссылка на товар': url_next,
                            'Регулярная цена': regular_price,
                            'Промо цена': promo_price,
                            'Бренд': brand_value
                        })
                else:
                    break
            else:
                print(f"Ошибка при запросе: {response.status_code}")
