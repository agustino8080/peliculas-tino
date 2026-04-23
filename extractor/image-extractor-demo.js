/**
 * Extractor de Imágenes - Versión Demo
 * Este script permite extraer imágenes de páginas web como eBay
 */

class ImageExtractorDemo {
    constructor() {
        this.images = [];
        this.currentUrl = '';
        this.isLoading = false;
        this.proxyUrl = 'https://api.allorigins.win/get?url='; // Proxy para evitar CORS
        
        // No crear UI automáticamente en el demo
        // La UI será manejada por el HTML del demo
    }
    
    async extractImagesFromUrl(url) {
        if (!url) {
            throw new Error('Por favor ingresa una URL válida');
        }
        
        this.isLoading = true;
        this.currentUrl = url;
        
        try {
            // Usar proxy para evitar CORS
            const proxyUrl = this.proxyUrl + encodeURIComponent(url);
            const response = await fetch(proxyUrl);
            const data = await response.json();
            
            if (data.contents) {
                const html = data.contents;
                this.parseImages(html, url);
                return {
                    success: true,
                    count: this.images.length,
                    images: this.images
                };
            } else {
                throw new Error('No se pudo obtener el contenido de la página');
            }
            
        } catch (error) {
            console.error('Error al extraer imágenes:', error);
            throw new Error('Error al cargar la página: ' + error.message);
        } finally {
            this.isLoading = false;
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
        
        return this.images;
    }
    
    isValidImageUrl(url) {
        // Filtrar por extensiones válidas
        const validExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp'];
        const lowerUrl = url.toLowerCase();
        
        return validExtensions.some(ext => lowerUrl.includes(ext)) &&
               !url.includes('data:image') && // Excluir data URLs
               url.length > 10; // Evitar URLs muy cortas
    }
    
    downloadImage(src, filename = null) {
        // Crear enlace de descarga temporal
        const link = document.createElement('a');
        link.href = src;
        link.download = filename || `imagen_${Date.now()}.jpg`;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        
        // Forzar descarga
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        return true;
    }
    
    getImageInfo() {
        return {
            total: this.images.length,
            images: this.images.map((img, index) => ({
                id: index,
                src: img.src,
                alt: img.alt,
                title: img.title,
                dimensions: `${img.width} x ${img.height}`
            }))
        };
    }
}

// Función global para usar desde el demo
window.extractImagesFromUrl = async function(url) {
    if (!window.imageExtractorDemo) {
        window.imageExtractorDemo = new ImageExtractorDemo();
    }
    
    return await window.imageExtractorDemo.extractImagesFromUrl(url);
};

// Función global para descargar imagen
window.downloadImage = function(src, filename = null) {
    if (!window.imageExtractorDemo) {
        window.imageExtractorDemo = new ImageExtractorDemo();
    }
    
    return window.imageExtractorDemo.downloadImage(src, filename);
};