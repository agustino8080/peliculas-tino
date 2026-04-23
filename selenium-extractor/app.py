from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import json
import os
import subprocess
import threading
import time
from datetime import datetime
from adidas_advanced_scraper import AdidasAdvancedScraper

app = Flask(__name__)
CORS(app)

# Estado global del scraping
scraping_status = {
    'is_running': False,
    'progress': 0,
    'message': 'Listo para iniciar',
    'products_found': 0,
    'images_extracted': 0,
    'start_time': None,
    'results': [],
    'error': None
}

def run_scraping_task(url, headless=True, download_images=False):
    """Ejecutar el scraping en un hilo separado"""
    global scraping_status
    
    try:
        scraping_status.update({
            'is_running': True,
            'progress': 0,
            'message': '🚀 Iniciando scraping...',
            'error': None
        })
        
        # Crear scraper
        scraper = AdidasAdvancedScraper(headless=headless)
        
        # Actualizar progreso
        scraping_status.update({
            'progress': 10,
            'message': '🌐 Navegando a Adidas.com...'
        })
        
        # Ejecutar scraping
        scraper.scrape_adidas_sale_advanced(url)
        
        # Actualizar resultados
        scraping_status.update({
            'progress': 90,
            'message': '💾 Guardando datos...',
            'products_found': len(scraper.products),
            'images_extracted': len(set(scraper.images)),
            'results': scraper.products[:10]  # Primeros 10 resultados para preview
        })
        
        # Guardar datos
        scraper.save_comprehensive_data("adidas_data")
        
        # Descargar imágenes si se solicitó
        if download_images:
            scraping_status['message'] = '🖼️ Descargando imágenes...'
            scraper.download_images("adidas_data/images")
        
        scraping_status.update({
            'progress': 100,
            'message': '✅ Scraping completado exitosamente!',
            'is_running': False
        })
        
        scraper.close()
        
    except Exception as e:
        scraping_status.update({
            'is_running': False,
            'error': str(e),
            'message': f'❌ Error: {str(e)}'
        })

@app.route('/')
def index():
    """Servir la interfaz web"""
    return render_template('index.html')

@app.route('/api/start-scraping', methods=['POST'])
def start_scraping():
    """Iniciar el proceso de scraping"""
    global scraping_status
    
    if scraping_status['is_running']:
        return jsonify({'error': 'El scraping ya está en ejecución'}), 400
    
    try:
        data = request.get_json()
        url = data.get('url', 'https://www.adidas.com/us/men-shoes-sale?sort=price-low-to-high')
        headless = data.get('headless', True)
        download_images = data.get('downloadImages', False)
        
        # Reiniciar estado
        scraping_status = {
            'is_running': True,
            'progress': 0,
            'message': '🚀 Iniciando scraping...',
            'products_found': 0,
            'images_extracted': 0,
            'start_time': time.time(),
            'results': [],
            'error': None
        }
        
        # Iniciar scraping en hilo separado
        thread = threading.Thread(
            target=run_scraping_task,
            args=(url, headless, download_images)
        )
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Scraping iniciado',
            'status': scraping_status
        })
        
    except Exception as e:
        scraping_status['is_running'] = False
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop-scraping', methods=['POST'])
def stop_scraping():
    """Detener el proceso de scraping"""
    global scraping_status
    
    if not scraping_status['is_running']:
        return jsonify({'error': 'No hay scraping en ejecución'}), 400
    
    scraping_status.update({
        'is_running': False,
        'message': '🛑 Scraping detenido por el usuario'
    })
    
    return jsonify({
        'success': True,
        'message': 'Scraping detenido',
        'status': scraping_status
    })

@app.route('/api/status')
def get_status():
    """Obtener el estado actual del scraping"""
    global scraping_status
    
    # Calcular tiempo transcurrido
    if scraping_status['start_time']:
        elapsed = time.time() - scraping_status['start_time']
        scraping_status['elapsed_time'] = f"{int(elapsed // 60):02d}:{int(elapsed % 60):02d}"
    else:
        scraping_status['elapsed_time'] = "00:00"
    
    return jsonify(scraping_status)

@app.route('/api/results')
def get_results():
    """Obtener los resultados del scraping"""
    try:
        # Leer datos guardados
        data_dir = "adidas_data"
        products_file = os.path.join(data_dir, "products_detailed.json")
        
        if os.path.exists(products_file):
            with open(products_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return jsonify(data)
        else:
            return jsonify({'error': 'No hay resultados disponibles'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<file_type>')
def download_file(file_type):
    """Descargar archivos generados"""
    try:
        data_dir = "adidas_data"
        
        if file_type == 'json':
            file_path = os.path.join(data_dir, "products_detailed.json")
        elif file_type == 'csv':
            file_path = os.path.join(data_dir, "products.csv")
        elif file_type == 'images':
            file_path = os.path.join(data_dir, "images.json")
        else:
            return jsonify({'error': 'Tipo de archivo no válido'}), 400
        
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'Archivo no encontrado'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/preview')
def preview_results():
    """Servir la vista previa HTML"""
    try:
        preview_file = "adidas_data/advanced_preview.html"
        if os.path.exists(preview_file):
            return send_file(preview_file)
        else:
            return "<h1>No hay resultados para mostrar</h1><p>Execute el scraping primero.</p>", 404
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>", 500

# Crear directorio de templates si no existe
templates_dir = "templates"
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)

# Copiar el archivo index.html al directorio templates
import shutil
if os.path.exists("index.html"):
    shutil.copy("index.html", os.path.join(templates_dir, "index.html"))

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask para Adidas Selenium Scraper")
    print("📡 Servidor ejecutándose en: http://localhost:5000")
    print("🌐 Abre la URL en tu navegador para acceder a la interfaz")
    
    app.run(debug=True, host='0.0.0.0', port=5000)