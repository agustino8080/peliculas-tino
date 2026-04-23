from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import json
import time
import os
from urllib.parse import urljoin
import requests
from datetime import datetime

class AdidasAdvancedScraper:
    def __init__(self, headless=False, implicit_wait=10):
        self.setup_driver(headless, implicit_wait)
        self.products = []
        self.images = []
        self.scraped_urls = set()
        
    def setup_driver(self, headless, implicit_wait):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(implicit_wait)
        self.wait = WebDriverWait(self.driver, 15)
        
    def smart_scroll(self, max_products=50, scroll_pause=2):
        """Scroll inteligente que espera a que carguen los productos"""
        print("Iniciando scroll inteligente...")
        products_found = 0
        scrolls = 0
        max_scrolls = 20
        
        while products_found < max_products and scrolls < max_scrolls:
            # Scroll hacia abajo
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause)
            
            # Contar productos actuales
            current_products = len(self.driver.find_elements(By.CSS_SELECTOR, "[data-auto-id='product-card']"))
            
            if current_products > products_found:
                products_found = current_products
                print(f"Productos encontrados: {products_found}")
            else:
                # Si no hay nuevos productos, intentar scroll más lento
                self.driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(scroll_pause)
                
                # Verificar si hay botón de "Load More"
                try:
                    load_more = self.driver.find_element(By.CSS_SELECTOR, "[data-auto-id='load-more'], .load-more, button[aria-label*='load']")
                    if load_more.is_displayed():
                        self.driver.execute_script("arguments[0].click();", load_more)
                        time.sleep(scroll_pause * 2)
                        print("Botón 'Load More' clickeado")
                except:
                    pass
            
            scrolls += 1
            
        print(f"Scroll completado. Total productos: {products_found}")
        
    def handle_popups_and_cookies(self):
        """Manejar popups, cookies y banners"""
        try:
            # Cookies
            cookie_selectors = [
                "[data-auto-id='glass-gdpr-default-consent-accept-button']",
                "button[aria-label*='accept']",
                "button[data-testid*='cookie']",
                ".accept-cookies"
            ]
            
            for selector in cookie_selectors:
                try:
                    cookie_button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    cookie_button.click()
                    print("Cookies aceptadas")
                    time.sleep(2)
                    break
                except:
                    continue
                    
        except Exception as e:
            print(f"Error manejando popups: {e}")
            
    def extract_product_images(self, product_element):
        """Extraer todas las imágenes de un producto"""
        images = []
        
        # Selectores de imágenes comunes en Adidas
        image_selectors = [
            "img[src*='adidas']",
            "img[data-auto-id='product-card-image']",
            "img[class*='product-image']",
            "img[class*='image']",
            "img"
        ]
        
        for selector in image_selectors:
            try:
                imgs = product_element.find_elements(By.CSS_SELECTOR, selector)
                for img in imgs:
                    src = img.get_attribute("src") or img.get_attribute("data-src") or img.get_attribute("data-original")
                    if src and ("adidas" in src or "hbx" in src):
                        # Limpiar URL y obtener versión de alta calidad
                        if "_" in src:
                            # Adidas usa patrones como _200.jpg, _500.jpg, _1000.jpg
                            high_quality = src.split("_")[0] + "_1000.jpg"
                            if high_quality not in images:
                                images.append(high_quality)
                        else:
                            if src not in images:
                                images.append(src)
            except:
                continue
                
        return list(set(images))
    
    def extract_product_info(self, product_element):
        """Extraer información detallada del producto"""
        product_data = {}
        
        try:
            # Nombre del producto
            name_selectors = [
                "[data-auto-id='product-card-title']",
                "h3[class*='title']",
                "a[class*='title']",
                "[class*='product-name']",
                "h3"
            ]
            
            for selector in name_selectors:
                try:
                    name_elem = product_element.find_element(By.CSS_SELECTOR, selector)
                    product_data['name'] = name_elem.text.strip()
                    break
                except:
                    continue
            
            if 'name' not in product_data:
                product_data['name'] = "Sin nombre"
                
            # Precio
            price_selectors = [
                "[data-auto-id='product-card-price']",
                "[class*='price']",
                "[class*='cost']",
                ".price"
            ]
            
            for selector in price_selectors:
                try:
                    price_elem = product_element.find_element(By.CSS_SELECTOR, selector)
                    price_text = price_elem.text.strip()
                    if '$' in price_text or 'USD' in price_text or price_text.replace('$', '').replace('.', '').isdigit():
                        product_data['price'] = price_text
                        break
                except:
                    continue
                    
            if 'price' not in product_data:
                product_data['price'] = "Sin precio"
                
            # Precio original (si hay descuento)
            try:
                original_price_elem = product_element.find_element(By.CSS_SELECTOR, "[class*='original-price'], [class*='was-price']")
                product_data['original_price'] = original_price_elem.text.strip()
            except:
                product_data['original_price'] = None
                
            # Enlace
            try:
                link_elem = product_element.find_element(By.TAG_NAME, "a")
                href = link_elem.get_attribute("href")
                if href:
                    product_data['url'] = urljoin("https://www.adidas.com", href)
                else:
                    product_data['url'] = ""
            except:
                product_data['url'] = ""
                
            # Categoría/tipo
            try:
                category_elem = product_element.find_element(By.CSS_SELECTOR, "[class*='category'], [class*='type']")
                product_data['category'] = category_elem.text.strip()
            except:
                product_data['category'] = "Sin categoría"
                
            # Disponibilidad
            try:
                # Verificar si está agotado
                sold_out_indicators = [
                    "[class*='sold-out']",
                    "[class*='out-of-stock']",
                    "[data-auto-id*='sold']"
                ]
                
                product_data['available'] = True
                for selector in sold_out_indicators:
                    try:
                        product_element.find_element(By.CSS_SELECTOR, selector)
                        product_data['available'] = False
                        break
                    except:
                        continue
                        
            except:
                product_data['available'] = True
                
            # Extraer imágenes
            product_data['images'] = self.extract_product_images(product_element)
            
            # Marca de tiempo
            product_data['scraped_at'] = datetime.now().isoformat()
            
        except Exception as e:
            print(f"Error extrayendo info del producto: {e}")
            
        return product_data
    
    def scrape_with_retry(self, url, max_retries=3):
        """Scrape con reintentos en caso de fallo"""
        for attempt in range(max_retries):
            try:
                print(f"Intento {attempt + 1} de {max_retries}")
                self.driver.get(url)
                time.sleep(5)
                
                # Manejar popups
                self.handle_popups_and_cookies()
                
                # Scroll inteligente
                self.smart_scroll(max_products=30)
                
                # Extraer productos
                products = self.wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-auto-id='product-card']"))
                )
                
                print(f"Encontrados {len(products)} productos")
                
                for i, product in enumerate(products):
                    try:
                        # Hacer scroll al producto para asegurar que esté visible
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", product)
                        time.sleep(0.5)
                        
                        product_data = self.extract_product_info(product)
                        
                        # Evitar duplicados
                        if product_data['url'] and product_data['url'] not in self.scraped_urls:
                            self.products.append(product_data)
                            self.images.extend(product_data['images'])
                            self.scraped_urls.add(product_data['url'])
                            
                            print(f"Producto {i+1}: {product_data['name'][:50]}...")
                            
                    except StaleElementReferenceException:
                        print(f"Elemento stale en producto {i+1}, saltando...")
                        continue
                    except Exception as e:
                        print(f"Error en producto {i+1}: {e}")
                        continue
                
                print(f"✅ Extracción exitosa en intento {attempt + 1}")
                return True
                
            except Exception as e:
                print(f"❌ Error en intento {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                else:
                    print("❌ Máximo de reintentos alcanzado")
                    return False
                    
    def scrape_adidas_sale_advanced(self, url):
        """Scrape avanzado de Adidas con todas las funciones"""
        print(f"🚀 Iniciando scraping avanzado de Adidas")
        print(f"📍 URL: {url}")
        
        success = self.scrape_with_retry(url)
        
        if success:
            print(f"\n📊 Resumen de extracción:")
            print(f"   📦 Productos únicos: {len(self.products)}")
            print(f"   🖼️  Imágenes únicas: {len(set(self.images))}")
            print(f"   💰 Productos con precio: {len([p for p in self.products if p['price'] != 'Sin precio'])}")
            print(f"   ✅ Productos disponibles: {len([p for p in self.products if p['available']])}")
        else:
            print("❌ Falló la extracción")
            
    def save_comprehensive_data(self, output_dir="adidas_advanced_data"):
        """Guardar datos de forma comprensiva"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Guardar productos con metadata
        products_file = os.path.join(output_dir, "products_detailed.json")
        with open(products_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'total_products': len(self.products),
                    'scraped_at': datetime.now().isoformat(),
                    'source_url': 'https://www.adidas.com/us/men-shoes-sale',
                    'categories': list(set([p.get('category', 'Unknown') for p in self.products]))
                },
                'products': self.products
            }, f, ensure_ascii=False, indent=2)
        
        # Guardar imágenes únicas
        unique_images = list(set(self.images))
        images_file = os.path.join(output_dir, "images.json")
        with open(images_file, 'w', encoding='utf-8') as f:
            json.dump(unique_images, f, ensure_ascii=False, indent=2)
        
        # Crear CSV para análisis
        csv_file = os.path.join(output_dir, "products.csv")
        import csv
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            if self.products:
                fieldnames = ['name', 'price', 'original_price', 'category', 'available', 'url', 'image_count']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for product in self.products:
                    writer.writerow({
                        'name': product['name'],
                        'price': product['price'],
                        'original_price': product.get('original_price', ''),
                        'category': product.get('category', ''),
                        'available': product['available'],
                        'url': product['url'],
                        'image_count': len(product['images'])
                    })
        
        # Crear HTML avanzado
        self.create_advanced_html_preview(output_dir)
        
        print(f"✅ Datos guardados en: {output_dir}")
        
    def create_advanced_html_preview(self, output_dir):
        """Crear vista previa HTML avanzada"""
        html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏃‍♂️ Adidas Sale - Scraping Avanzado</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { 
            background: rgba(0, 0, 0, 0.9); 
            color: white; 
            padding: 30px; 
            text-align: center; 
            border-radius: 15px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px;
        }
        .stat-card { 
            background: rgba(255, 255, 255, 0.95); 
            padding: 20px; 
            border-radius: 10px; 
            text-align: center; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }
        .stat-number { font-size: 2em; font-weight: bold; color: #e60023; }
        .stat-label { color: #666; margin-top: 5px; }
        .products-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); 
            gap: 25px; 
        }
        .product-card { 
            background: rgba(255, 255, 255, 0.95); 
            border-radius: 15px; 
            padding: 20px; 
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            backdrop-filter: blur(10px);
        }
        .product-card:hover { 
            transform: translateY(-5px); 
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }
        .product-image-container { 
            position: relative; 
            width: 100%; 
            height: 200px; 
            border-radius: 10px; 
            overflow: hidden; 
            margin-bottom: 15px;
            background: #f8f9fa;
        }
        .product-image { 
            width: 100%; 
            height: 100%; 
            object-fit: cover; 
            transition: transform 0.3s ease;
        }
        .product-image:hover { transform: scale(1.05); }
        .product-badge { 
            position: absolute; 
            top: 10px; 
            right: 10px; 
            background: #e60023; 
            color: white; 
            padding: 5px 10px; 
            border-radius: 15px; 
            font-size: 12px; 
            font-weight: bold;
        }
        .product-name { 
            font-size: 16px; 
            font-weight: 600; 
            margin-bottom: 10px; 
            color: #333; 
            line-height: 1.4;
            height: 44px;
            overflow: hidden;
        }
        .product-price-container { margin-bottom: 10px; }
        .product-price { 
            font-size: 20px; 
            color: #e60023; 
            font-weight: bold; 
            display: inline-block;
        }
        .product-original-price { 
            font-size: 14px; 
            color: #999; 
            text-decoration: line-through; 
            margin-left: 10px;
        }
        .product-category { 
            color: #666; 
            font-size: 12px; 
            margin-bottom: 10px; 
            text-transform: uppercase; 
            letter-spacing: 0.5px;
        }
        .product-availability { 
            display: inline-block; 
            padding: 4px 8px; 
            border-radius: 12px; 
            font-size: 11px; 
            font-weight: bold;
            margin-bottom: 10px;
        }
        .available { background: #d4edda; color: #155724; }
        .unavailable { background: #f8d7da; color: #721c24; }
        .product-link { 
            display: inline-block; 
            background: #000; 
            color: white; 
            padding: 10px 15px; 
            border-radius: 8px; 
            text-decoration: none; 
            font-size: 14px; 
            transition: background 0.3s ease;
        }
        .product-link:hover { background: #333; }
        .no-image { 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            height: 100%; 
            background: #f8f9fa; 
            color: #999; 
            font-size: 14px;
        }
        .download-section { 
            text-align: center; 
            margin-top: 30px; 
            padding: 20px; 
            background: rgba(255, 255, 255, 0.95); 
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        .download-btn { 
            background: #28a745; 
            color: white; 
            padding: 12px 25px; 
            border: none; 
            border-radius: 8px; 
            font-size: 16px; 
            cursor: pointer; 
            text-decoration: none; 
            display: inline-block; 
            margin: 5px;
            transition: background 0.3s ease;
        }
        .download-btn:hover { background: #218838; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏃‍♂️ Adidas Sale - Scraping Avanzado</h1>
            <p>Extractor de Selenium con Inteligencia Artificial</p>
            <p>📅 Scraping realizado: {scraping_date}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_products}</div>
                <div class="stat-label">Productos Totales</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_images}</div>
                <div class="stat-label">Imágenes Únicas</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{available_products}</div>
                <div class="stat-label">Productos Disponibles</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{products_with_price}</div>
                <div class="stat-label">Con Precio</div>
            </div>
        </div>
        
        <div class="products-grid">
"""
        
        # Agregar productos
        for product in self.products:
            # Determinar disponibilidad
            availability_class = "available" if product['available'] else "unavailable"
            availability_text = "Disponible" if product['available'] else "Agotado"
            
            # Badge de descuento si hay precio original
            discount_badge = ""
            if product.get('original_price'):
                discount_badge = f'<div class="product-badge">OFERTA</div>'
            
            # Imagen o placeholder
            if product['images']:
                image_html = f'<img src="{product["images"][0]}" alt="{product["name"]}" class="product-image">'
            else:
                image_html = '<div class="no-image">Sin imagen</div>'
            
            # Precio original tachado
            original_price_html = ""
            if product.get('original_price'):
                original_price_html = f'<span class="product-original-price">{product["original_price"]}</span>'
            
            html_content += f"""
            <div class="product-card">
                <div class="product-image-container">
                    {image_html}
                    {discount_badge}
                </div>
                <div class="product-category">{product.get('category', 'Calzado')}</div>
                <div class="product-name">{product['name']}</div>
                <div class="product-price-container">
                    <span class="product-price">{product['price']}</span>
                    {original_price_html}
                </div>
                <div class="product-availability {availability_class}">{availability_text}</div>
                <a href="{product['url']}" target="_blank" class="product-link">Ver en Adidas →</a>
            </div>
"""
        
        html_content += """
        </div>
        
        <div class="download-section">
            <h3>📥 Descargar Datos</h3>
            <a href="products_detailed.json" class="download-btn" download>📄 JSON Detallado</a>
            <a href="products.csv" class="download-btn" download>📊 CSV para Excel</a>
            <a href="images.json" class="download-btn" download>🖼️ Lista de Imágenes</a>
        </div>
    </div>
</body>
</html>
"""
        
        # Formatear con datos reales
        html_content = html_content.format(
            scraping_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_products=len(self.products),
            total_images=len(set(self.images)),
            available_products=len([p for p in self.products if p['available']]),
            products_with_price=len([p for p in self.products if p['price'] != 'Sin precio'])
        )
        
        html_file = os.path.join(output_dir, "advanced_preview.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
    def close(self):
        """Cerrar navegador"""
        if self.driver:
            self.driver.quit()

def main():
    # URL de Adidas - Hombre Zapatillas en Oferta
    url = "https://www.adidas.com/us/men-shoes-sale?sort=price-low-to-high"
    
    scraper = AdidasAdvancedScraper(headless=False)
    
    try:
        # Ejecutar scraping avanzado
        scraper.scrape_adidas_sale_advanced(url)
        
        # Guardar datos completos
        scraper.save_comprehensive_data()
        
        print("\n🎉 ¡Scraping completado exitosamente!")
        print("\n📁 Archivos generados:")
        print("  📄 products_detailed.json - Datos completos con metadata")
        print("  📊 products.csv - Datos para Excel/análisis")
        print("  🖼️ images.json - Lista de URLs de imágenes")
        print("  🌐 advanced_preview.html - Vista previa interactiva")
        print("\n✨ Abre 'advanced_preview.html' en tu navegador para ver los resultados")
        
    except Exception as e:
        print(f"\n❌ Error durante el scraping: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        scraper.close()

if __name__ == "__main__":
    main()