# 🏃‍♂️ Adidas Selenium Scraper

Extractor avanzado de productos Adidas usando Selenium WebDriver con interfaz web moderna.

## 🚀 Características

- **Selenium Automation**: Control completo del navegador Chrome
- **Scroll Inteligente**: Carga automática de productos infinitos
- **Extracción de Imágenes**: Obtiene todas las imágenes de alta calidad
- **Datos Estructurados**: JSON, CSV y HTML para análisis
- **Interfaz Web Moderna**: Control desde tu navegador
- **Anti-Detección**: Evita bloqueos de bots
- **Reintentos Automáticos**: Manejo de errores robusto

## 📋 Requisitos

```bash
# Instalar Python 3.8+
# Instalar Chrome/Chromium
# Instalar dependencias
pip install -r requirements.txt
```

## 🛠️ Instalación

1. **Clonar o descargar el proyecto**
```bash
cd selenium-extractor
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Descargar ChromeDriver** (automático con webdriver-manager)

## 🎯 Uso Rápido

### Opción 1: Interfaz Web (Recomendado)
```bash
# Iniciar servidor Flask
python app.py

# Abrir en navegador
http://localhost:5000
```

### Opción 2: Script Directo
```bash
# Scraping básico
python adidas_scraper.py

# Scraping avanzado
python adidas_advanced_scraper.py
```

## 🔧 Configuración

### URLs Soportadas
- `https://www.adidas.com/us/men-shoes-sale`
- `https://www.adidas.com/us/women-shoes-sale`
- `https://www.adidas.com/us/kids-shoes-sale`
- Cualquier página de categoría de Adidas

### Opciones de Scraping
```python
# Modo invisible (sin abrir navegador)
headless = True

# Descargar imágenes
download_images = True

# Límite de productos
max_products = 30

# Tiempo de espera
implicit_wait = 10
```

## 📊 Datos Extraídos

### Información de Productos
- ✅ **Nombre completo**
- ✅ **Precio actual**
- ✅ **Precio original** (si hay descuento)
- ✅ **Categoría**
- ✅ **Disponibilidad**
- ✅ **URL del producto**
- ✅ **Todas las imágenes** (varias resoluciones)
- ✅ **Metadata** (fecha, categorías, estadísticas)

### Formatos de Salida
- `products_detailed.json` - Datos completos con metadata
- `products.csv` - Datos para Excel/análisis
- `images.json` - Lista de URLs de imágenes
- `advanced_preview.html` - Vista previa interactiva

## 🎨 Interfaz Web

### Panel de Control
- 🔄 **URL personalizable**
- 👻 **Modo invisible**
- 🖼️ **Descarga de imágenes**
- 📊 **Progreso en tiempo real**
- 📝 **Logs detallados**
- ⏱️ **Estadísticas**

### Monitoreo
- Barra de progreso en vivo
- Contador de productos
- Contador de imágenes
- Tiempo transcurrido
- Mensajes de estado

## 🔍 Ejemplos de Uso

### Scraping Básico
```python
from adidas_scraper import AdidasScraper

scraper = AdidasScraper(headless=True)
scraper.scrape_adidas_sale("https://www.adidas.com/us/men-shoes-sale")
scraper.save_data()
scraper.close()
```

### Scraping Avanzado
```python
from adidas_advanced_scraper import AdidasAdvancedScraper

scraper = AdidasAdvancedScraper(headless=False)
scraper.scrape_adidas_sale_advanced("https://www.adidas.com/us/men-shoes-sale")
scraper.save_comprehensive_data()
scraper.download_images()
scraper.close()
```

## 🛡️ Anti-Detección

### Técnicas Implementadas
- **User-Agent realista**: Simula Chrome real
- **Ventana tamaño humano**: 1920x1080
- **Scroll natural**: Movimientos suaves
- **Tiempo de espera**: Pausas realistas
- **JavaScript habilitado**: Como usuario real
- **Cookies aceptadas**: Evita bloqueos

### Selectores Robusto
```python
# Múltiples selectores por elemento
name_selectors = [
    "[data-auto-id='product-card-title']",
    "h3[class*='title']",
    "a[class*='title']",
    "[class*='product-name']"
]
```

## 🚨 Manejo de Errores

### Reintentos Automáticos
- **Máximo 3 intentos** por producto
- **Timeouts configurables** (10-15 segundos)
- **Elementos stale**: Detección y recuperación
- **Popups dinámicos**: Manejo automático

### Logs Detallados
```
[10:30:45] 🚀 Iniciando scraping avanzado
[10:30:47] 🌐 Navegando a Adidas.com...
[10:30:52] 🍪 Cookies aceptadas
[10:30:55] 📜 Scroll #1: 12 productos encontrados
[10:31:02] 📜 Scroll #2: 24 productos encontrados
[10:31:08] ✅ Extracción exitosa: 30 productos
```

## 📁 Estructura de Archivos

```
selenium-extractor/
├── 📄 app.py                      # Servidor Flask
├── 📄 adidas_scraper.py          # Scraping básico
├── 📄 adidas_advanced_scraper.py # Scraping avanzado
├── 📄 requirements.txt           # Dependencias
├── 📄 index.html                 # Interfaz web
├── 📄 README.md                  # Documentación
└── 📁 adidas_data/               # Salida de datos
    ├── 📄 products_detailed.json
    ├── 📄 products.csv
    ├── 📄 images.json
    ├── 📄 advanced_preview.html
    └── 📁 images/                # Imágenes descargadas
```

## 🔧 Solución de Problemas

### ChromeDriver no encontrado
```bash
# Se instala automáticamente con webdriver-manager
# Si hay problemas, instalar manualmente:
# Windows: Descargar de https://chromedriver.chromium.org/
# Linux: sudo apt-get install chromium-chromedriver
```

### Timeout errors
```python
# Aumentar tiempo de espera
implicit_wait = 20  # segundos
wait = WebDriverWait(driver, 30)
```

### Elementos no encontrados
```python
# Verificar selectores en la página
# Usar Chrome DevTools para inspeccionar
# Actualizar selectores en el código
```

## 📈 Próximas Mejoras

- [ ] **Multithreading**: Más velocidad
- [ ] **Proxy rotation**: Evitar bloqueos IP
- [ ] **API REST**: Integración completa
- [ ] **Base de datos**: Almacenamiento persistente
- [ ] **Machine Learning**: Detección de cambios
- [ ] **Notificaciones**: Alertas por email
- [ ] **Programación**: Scraping automático

## 📞 Soporte

### Problemas Comunes
1. **¿Chrome no abre?** → Instala Chrome/Chromium
2. **¿Timeout errors?** → Aumenta `implicit_wait`
3. **¿No encuentra productos?** → Verifica la URL
4. **¿Imágenes rotas?** → Usa modo visible (headless=False)

### Debug Mode
```python
# Activar modo debug
scraper = AdidasAdvancedScraper(headless=False, debug=True)
```

---

**⭐ ¿Te gusta este proyecto?** ¡Dale una estrella y comparte!

**🔧 ¿Problemas?** Abre un issue en GitHub

**💡 ¿Sugerencias?** ¡Envía un pull request!