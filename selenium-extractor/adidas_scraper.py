from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import time
import os
from urllib.parse import urljoin
import requests

class AdidasScraper:
    def __init__(self, headless=False):
        self.setup_driver(headless)
        self.products = []
        self.images = []
        
    def setup_driver(self, headless):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
    def scroll_to_load_products(self, max_scrolls=10):
        """Scroll down to load more products (infinite scroll)"""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scrolls = 0
        
        while scrolls < max_scrolls:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            
            last_height = new_height
            scrolls += 1
            
    def accept_cookies(self):
        """Accept cookies if the banner appears"""
        try:
            cookie_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-auto-id='glass-gdpr-default-consent-accept-button']"))
            )
            cookie_button.click()
            time.sleep(2)
        except TimeoutException:
            print("No se encontró banner de cookies")
            
    def extract_product_data(self):
        """Extract product information and images"""
        try:
            # Esperar a que los productos carguen
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-auto-id='product-card']"))
            )
            
            # Obtener todos los productos
            products = self.driver.find_elements(By.CSS_SELECTOR, "[data-auto-id='product-card']")
            
            for product in products:
                try:
                    # Extraer información del producto
                    product_data = {}
                    
                    # Nombre del producto
                    try:
                        name_element = product.find_element(By.CSS_SELECTOR, "[data-auto-id='product-card-title']")
                        product_data['name'] = name_element.text.strip()
                    except NoSuchElementException:
                        product_data['name'] = "Sin nombre"
                    
                    # Precio
                    try:
                        price_element = product.find_element(By.CSS_SELECTOR, "[data-auto-id='product-card-price']")
                        product_data['price'] = price_element.text.strip()
                    except NoSuchElementException:
                        product_data['price'] = "Sin precio"
                    
                    # Enlace del producto
                    try:
                        link_element = product.find_element(By.TAG_NAME, "a")
                        product_data['url'] = urljoin("https://www.adidas.com", link_element.get_attribute("href"))
                    except NoSuchElementException:
                        product_data['url'] = ""
                    
                    # Imágenes
                    images = []
                    try:
                        # Buscar imágenes en diferentes selectores comunes de Adidas
                        img_selectors = [
                            "img[src*='adidas']",
                            "img[data-auto-id='product-card-image']",
                            "img[class*='image']",
                            "img"
                        ]
                        
                        for selector in img_selectors:
                            try:
                                imgs = product.find_elements(By.CSS_SELECTOR, selector)
                                for img in imgs:
                                    src = img.get_attribute("src") or img.get_attribute("data-src")
                                    if src and "adidas" in src:
                                        # Limpiar y obtener URL de alta calidad
                                        if "_" in src:
                                            # Intentar obtener versión de mayor calidad
                                            high_quality = src.split("_")[0] + "_500.jpg"
                                            images.append(high_quality)
                                        else:
                                            images.append(src)
                                break
                            except:
                                continue
                    except:
                        pass
                    
                    product_data['images'] = list(set(images))  # Eliminar duplicados
                    
                    if product_data['name'] != "Sin nombre":
                        self.products.append(product_data)
                        self.images.extend(images)
                        
                except Exception as e:
                    print(f"Error extrayendo producto: {e}")
                    continue
                    
        except TimeoutException:
            print("No se encontraron productos")
            
    def scrape_adidas_sale(self, url):
        """Scrape Adidas sale page"""
        print(f"Navegando a: {url}")
        self.driver.get(url)
        time.sleep(5)
        
        # Aceptar cookies
        self.accept_cookies()
        
        # Scroll para cargar más productos
        print("Cargando más productos...")
        self.scroll_to_load_products(max_scrolls=5)
        
        # Extraer datos
        print("Extrayendo información de productos...")
        self.extract_product_data()
        
        print(f"Se encontraron {len(self.products)} productos")
        print(f"Se encontraron {len(self.images)} imágenes")
        
    def save_data(self, output_dir="adidas_data"):
        """Save scraped data to files"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Guardar información de productos
        products_file = os.path.join(output_dir, "products.json")
        with open(products_file, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, ensure_ascii=False, indent=2)
        
        # Guardar lista de imágenes
        images_file = os.path.join(output_dir, "images.json")
        with open(images_file, 'w', encoding='utf-8') as f:
            json.dump(self.images, f, ensure_ascii=False, indent=2)
        
        # Crear archivo HTML con vista previa
        self.create_html_preview(output_dir)
        
        print(f"Datos guardados en: {output_dir}")
        
    def create_html_preview(self, output_dir):
        """Create HTML preview of scraped products"""
        html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Adidas Sale - Productos Extraídos</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }
        .header { background: #000; color: white; padding: 20px; text-align: center; margin-bottom: 30px; }
        .products-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .product-card { background: white; border-radius: 8px; padding: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .product-image { width: 100%; height: 200px; object-fit: cover; border-radius: 4px; margin-bottom: 10px; }
        .product-name { font-size: 16px; font-weight: bold; margin-bottom: 8px; color: #333; }
        .product-price { font-size: 18px; color: #e60023; font-weight: bold; margin-bottom: 10px; }
        .product-link { color: #0066cc; text-decoration: none; font-size: 14px; }
        .product-link:hover { text-decoration: underline; }
        .stats { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; text-align: center; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏃‍♂️ Adidas Sale - Productos Extraídos</h1>
        <p>Extractor de Selenium - Zapatillas en oferta</p>
    </div>
    
    <div class="stats">
        <h2>Estadísticas</h2>
        <p>Total de productos: {product_count}</p>
        <p>Total de imágenes: {image_count}</p>
    </div>
    
    <div class="products-grid">
"""
        
        for product in self.products:
            images_html = ""
            if product['images']:
                images_html = f'<img src="{product["images"][0]}" alt="{product["name"]}" class="product-image">'
            
            html_content += f"""
        <div class="product-card">
            {images_html}
            <div class="product-name">{product['name']}</div>
            <div class="product-price">{product['price']}</div>
            <a href="{product['url']}" target="_blank" class="product-link">Ver producto →</a>
        </div>
"""
        
        html_content += """
    </div>
</body>
</html>
"""
        
        html_content = html_content.format(
            product_count=len(self.products),
            image_count=len(self.images)
        )
        
        html_file = os.path.join(output_dir, "preview.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
    def download_images(self, output_dir="adidas_data/images"):
        """Download all product images"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print("Descargando imágenes...")
        for i, image_url in enumerate(set(self.images)):
            try:
                response = requests.get(image_url, timeout=10)
                if response.status_code == 200:
                    filename = f"adidas_product_{i+1}.jpg"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    print(f"Descargada: {filename}")
            except Exception as e:
                print(f"Error descargando imagen {image_url}: {e}")
                
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()

def main():
    # URL de Adidas - Hombre Zapatillas en Oferta
    url = "https://www.adidas.com/us/men-shoes-sale?sort=price-low-to-high"
    
    scraper = AdidasScraper(headless=False)
    
    try:
        # Extraer productos
        scraper.scrape_adidas_sale(url)
        
        # Guardar datos
        scraper.save_data()
        
        # Descargar imágenes (opcional)
        # scraper.download_images()
        
        print("✅ Extracción completada!")
        print("📁 Archivos creados:")
        print("  - adidas_data/products.json")
        print("  - adidas_data/images.json") 
        print("  - adidas_data/preview.html")
        
    except Exception as e:
        print(f"❌ Error durante la extracción: {e}")
        
    finally:
        scraper.close()

if __name__ == "__main__":
    main()