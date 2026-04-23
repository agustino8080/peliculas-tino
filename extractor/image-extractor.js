/**
 * Extractor de Imágenes de Páginas Web
 * Este script permite extraer imágenes de páginas web como eBay
 */

class ImageExtractor {
    constructor() {
        this.images = [];
        this.currentUrl = '';
        this.isLoading = false;
        this.proxyUrl = 'https://api.allorigins.win/get?url='; // Proxy para evitar CORS
        
        this.init();
    }
    
    init() {
        this.createUI();
        this.setupEventListeners();
    }
    
    createUI() {
        // Crear contenedor principal
        const container = document.createElement('div');
        container.id = 'imageExtractor';
        container.innerHTML = `
            <style>
                #imageExtractor {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    width: 400px;
                    max-height: 80vh;
                    background: #1a1a1a;
                    border: 2px solid #f97316;
                    border-radius: 10px;
                    padding: 15px;
                    z-index: 10000;
                    font-family: Arial, sans-serif;
                    color: #ffffff;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.8);
                    overflow: hidden;
                }
                
                .extractor-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 15px;
                    padding-bottom: 10px;
                    border-bottom: 1px solid #444;
                }
                
                .extractor-title {
                    color: #f97316;
                    font-size: 16px;
                    font-weight: bold;
                    margin: 0;
                }
                
                .extractor-close {
                    background: #ff4444;
                    color: white;
                    border: none;
                    border-radius: 50%;
                    width: 25px;
                    height: 25px;
                    cursor: pointer;
                    font-size: 14px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                
                .extractor-input {
                    width: 100%;
                    padding: 8px;
                    background: #2a2a2a;
                    border: 1px solid #444;
                    border-radius: 5px;
                    color: white;
                    margin-bottom: 10px;
                    font-size: 14px;
                }
                
                .extractor-button {
                    width: 100%;
                    padding: 10px;
                    background: #f97316;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 14px;
                    font-weight: bold;
                    margin-bottom: 10px;
                    transition: background 0.3s;
                }
                
                .extractor-button:hover {
                    background: #fb923c;
                }
                
                .extractor-button:disabled {
                    background: #666;
                    cursor: not-allowed;
                }
                
                .extractor-loading {
                    text-align: center;
                    color: #f97316;
                    padding: 10px;
                    font-style: italic;
                }
                
                .extractor-results {
                    max-height: 300px;
                    overflow-y: auto;
                    margin-top: 10px;
                }
                
                .extractor-image-item {
                    display: flex;
                    align-items: center;
                    margin-bottom: 10px;
                    padding: 8px;
                    background: #2a2a2a;
                    border-radius: 5px;
                    border: 1px solid #444;
                }
                
                .extractor-image-thumb {
                    width: 60px;
                    height: 60px;
                    object-fit: cover;
                    border-radius: 5px;
                    margin-right: 10px;
                    cursor: pointer;
                    transition: transform 0.2s;
                }
                
                .extractor-image-thumb:hover {
                    transform: scale(1.1);
                }
                
                .extractor-image-info {
                    flex: 1;
                    font-size: 12px;
                }
                
                .extractor-image-name {
                    color: #f97316;
                    font-weight: bold;
                    margin-bottom: 5px;
                    word-break: break-all;
                }
                
                .extractor-image-size {
                    color: #888;
                    font-size: 11px;
                }
                
                .extractor-download-btn {
                    background: #22c55e;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    padding: 5px 10px;
                    cursor: pointer;
                    font-size: 11px;
                    transition: background 0.3s;
                }
                
                .extractor-download-btn:hover {
                    background: #16a34a;
                }
                
                .extractor-stats {
                    background: rgba(249, 115, 22, 0.1);
                    border: 1px solid #f97316;
                    border-radius: 5px;
                    padding: 10px;
                    margin-bottom: 10px;
                    font-size: 12px;
                    text-align: center;
                }
                
                .extractor-error {
                    background: rgba(255, 68, 68, 0.1);
                    border: 1px solid #ff4444;
                    color: #ff4444;
                    border-radius: 5px;
                    padding: 10px;
                    margin-bottom: 10px;
                    font-size: 12px;
                    text-align: center;
                }
                
                .extractor-success {
                    background: rgba(34, 197, 94, 0.1);
                    border: 1px solid #22c55e;
                    color: #22c55e;
                    border-radius: 5px;
                    padding: 10px;
                    margin-bottom: 10px;
                    font-size: 12px;
                    text-align: center;
                }
                
                .extractor-toggle {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    background: #f97316;
                    color: white;
                    border: none;
                    border-radius: 50%;
                    width: 50px;
                    height: 50px;
                    cursor: pointer;
                    font-size: 20px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
                    z-index: 9999;
                    transition: all 0.3s;
                }
                
                .extractor-toggle:hover {
                    background: #fb923c;
                    transform: scale(1.1);
                }
                
                .extractor-hidden {
                    display: none;
                }
                
                .extractor-preview {
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    max-width: 80vw;
                    max-height: 80vh;
                    z-index: 10001;
                    border: 3px solid #f97316;
                    border-radius: 10px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.9);
                }
                
                .extractor-preview-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0,0,0,0.8);
                    z-index: 10000;
                    cursor: pointer;
                }
            </style>
                    
            <div class="extractor-header">
                <h3 class="extractor-title">🖼️ Extractor de Imágenes</h3>
                <button class="extractor-close" onclick="imageExtractor.toggle()">×</button>
            </div>
                    
            <input type="text" class="extractor-input" id="extractorUrl" placeholder="Ingresa la URL de la página web (ej: eBay, Amazon, etc.)">
                    
            <button class="extractor-button" id="extractButton" onclick="imageExtractor.extractImages()">
                🔍 Extraer Imágenes
            </button>
                    
            <div id="extractorContent"></div>
        `;
        
        // Botón flotante para mostrar/ocultar
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'extractor-toggle';
        toggleBtn.innerHTML = '🖼️';
        toggleBtn.onclick = () => this.toggle();
        
        document.body.appendChild(container);
        document.body.appendChild(toggleBtn);
        
        this.container = container;
        this.toggleBtn = toggleBtn;
        this.contentDiv = container.querySelector('#extractorContent');
        this.urlInput = container.querySelector('#extractorUrl');
        this.extractButton = container.querySelector('#extractButton');
        
        // Establecer la URL del ejemplo
        this.urlInput.value = 'https://www.ebay.com/str/bluehaze?_trksid=p4429486.m3561.l161211';
    }
    
    setupEventListeners() {
        // Presionar Enter en el input
        this.urlInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.extractImages();
            }
        });
    }
    
    toggle() {
        const isHidden = this.container.classList.contains('extractor-hidden');
        if (isHidden) {
            this.container.classList.remove('extractor-hidden');
            this.toggleBtn.style.display = 'none';
        } else {
            this.container.classList.add('extractor-hidden');
            this.toggleBtn.style.display = 'block';
        }
    }
    
    async extractImages() {
        const url = this.urlInput.value.trim();
        if (!url) {
            this.showError('Por favor ingresa una URL válida');
            return;
        }
        
        this.isLoading = true;
        this.extractButton.disabled = true;
        this.extractButton.textContent = '⏳ Extrayendo...';
        this.contentDiv.innerHTML = '<div class="extractor-loading">Cargando página web...</div>';
        
        try {
            // Usar proxy para evitar CORS
            const proxyUrl = this.proxyUrl + encodeURIComponent(url);
            const response = await fetch(proxyUrl);
            const data = await response.json();
            
            if (data.contents) {
                const html = data.contents;
                this.parseImages(html, url);
            } else {
                throw new Error('No se pudo obtener el contenido de la página');
            }
            
        } catch (error) {
            console.error('Error al extraer imágenes:', error);
            this.showError('Error al cargar la página: ' + error.message);
        } finally {
            this.isLoading = false;
            this.extractButton.disabled = false;
            this.extractButton.textContent = '🔍 Extraer Imágenes';
        }
    }
    
    parseImages(html, baseUrl) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        
        this.images = [];
        
        // Buscar imágenes en diferentes formatos
        const imageSelectors = [
            'img[src]',
            'img[data-src]',
            'img[data-original]',
            'img[data-lazy]',
            'img[data-image]'
        ];
        
        const foundImages = new Set();
        
        imageSelectors.forEach(selector => {
            const imgs = doc.querySelectorAll(selector);
            imgs.forEach(img => {
                let src = img.getAttribute('src') || 
                         img.getAttribute('data-src') || 
                         img.getAttribute('data-original') || 
                         img.getAttribute('data-lazy') || 
                         img.getAttribute('data-image');
                
                if (src && src.trim() && !foundImages.has(src)) {
                    foundImages.add(src);
                    
                    // Convertir URL relativa a absoluta
                    if (src.startsWith('//')) {
                        src = 'https:' + src;
                    } else if (src.startsWith('/')) {
                        const url = new URL(baseUrl);
                        src = url.origin + src;
                    } else if (!src.startsWith('http')) {
                        const url = new URL(baseUrl);
                        src = url.origin + '/' + src;
                    }
                    
                    // Filtrar imágenes válidas
                    if (this.isValidImageUrl(src)) {
                        this.images.push({
                            src: src,
                            alt: img.getAttribute('alt') || 'Sin descripción',
                            title: img.getAttribute('title') || '',
                            width: img.getAttribute('width') || 'Desconocido',
                            height: img.getAttribute('height') || 'Desconocido'
                        });
                    }
                }
            });
        });
        
        // Buscar imágenes en elementos con estilos background-image
        const elementsWithBg = doc.querySelectorAll('*');
        elementsWithBg.forEach(el => {
            const style = el.getAttribute('style');
            if (style && style.includes('background-image')) {
                const match = style.match(/url\(['"]?([^'"]+)['"]?\)/);
                if (match && match[1]) {
                    let src = match[1];
                    if (!foundImages.has(src)) {
                        foundImages.add(src);
                        
                        // Convertir URL relativa a absoluta
                        if (src.startsWith('//')) {
                            src = 'https:' + src;
                        } else if (src.startsWith('/')) {
                            const url = new URL(baseUrl);
                            src = url.origin + src;
                        } else if (!src.startsWith('http')) {
                            const url = new URL(baseUrl);
                            src = url.origin + '/' + src;
                        }
                        
                        if (this.isValidImageUrl(src)) {
                            this.images.push({
                                src: src,
                                alt: 'Background image',
                                title: '',
                                width: 'Desconocido',
                                height: 'Desconocido'
                            });
                        }
                    }
                }
            }
        });
        
        this.displayResults();
    }
    
    isValidImageUrl(url) {
        // Filtrar por extensiones válidas
        const validExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp'];
        const lowerUrl = url.toLowerCase();
        
        return validExtensions.some(ext => lowerUrl.includes(ext)) &&
               !url.includes('data:image') && // Excluir data URLs
               url.length > 10; // Evitar URLs muy cortas
    }
    
    displayResults() {
        if (this.images.length === 0) {
            this.contentDiv.innerHTML = '<div class="extractor-error">No se encontraron imágenes en esta página</div>';
            return;
        }
        
        let html = `
            <div class="extractor-stats">
                🖼️ Se encontraron ${this.images.length} imágenes
            </div>
        `;
        
        html += '<div class="extractor-results">';
        
        this.images.forEach((image, index) => {
            html += `
                <div class="extractor-image-item">
                    <img src="${image.src}" 
                         class="extractor-image-thumb" 
                         alt="${image.alt}"
                         onclick="imageExtractor.previewImage('${image.src}')"
                         title="${image.title || image.alt}">
                    <div class="extractor-image-info">
                        <div class="extractor-image-name">${this.truncateText(image.alt, 30)}</div>
                        <div class="extractor-image-size">Dimensión: ${image.width} x ${image.height}</div>
                    </div>
                    <button class="extractor-download-btn" 
                            onclick="imageExtractor.downloadImage('${image.src}', '${index}')">
                        💾 Descargar
                    </button>
                </div>
            `;
        });
        
        html += '</div>';
        this.contentDiv.innerHTML = html;
    }
    
    truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }
    
    previewImage(src) {
        // Crear overlay y preview
        const overlay = document.createElement('div');
        overlay.className = 'extractor-preview-overlay';
        overlay.onclick = () => {
            document.body.removeChild(overlay);
            document.body.removeChild(preview);
        };
        
        const preview = document.createElement('img');
        preview.className = 'extractor-preview';
        preview.src = src;
        preview.onclick = (e) => e.stopPropagation();
        
        document.body.appendChild(overlay);
        document.body.appendChild(preview);
    }
    
    downloadImage(src, filename) {
        // Crear enlace de descarga temporal
        const link = document.createElement('a');
        link.href = src;
        link.download = `imagen_${filename}_${Date.now()}.jpg`;
        link.target = '_blank';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        this.showSuccess('Imagen descargada correctamente');
    }
    
    showError(message) {
        this.contentDiv.innerHTML = `<div class="extractor-error">${message}</div>`;
    }
    
    showSuccess(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'extractor-success';
        successDiv.textContent = message;
        this.contentDiv.insertBefore(successDiv, this.contentDiv.firstChild);
        
        setTimeout(() => {
            if (successDiv.parentNode) {
                successDiv.parentNode.removeChild(successDiv);
            }
        }, 3000);
    }
}

// Inicializar el extractor cuando el DOM esté listo
let imageExtractor;

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        imageExtractor = new ImageExtractor();
    });
} else {
    imageExtractor = new ImageExtractor();
}

// Función global para usar desde la consola
window.extractImages = function(url) {
    if (!imageExtractor) {
        console.error('El extractor no está inicializado');
        return;
    }
    
    if (url) {
        imageExtractor.urlInput.value = url;
    }
    imageExtractor.extractImages();
};