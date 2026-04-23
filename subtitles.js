/**
 * Sistema de subtítulos para el reproductor de video
 * Este archivo añade funcionalidad de subtítulos sin modificar el HTML original
 */

class SubtitleManager {
    constructor() {
        this.currentVideo = null;
        this.subtitles = [];
        this.currentSubtitleIndex = -1;
        this.isEnabled = true;
        this.subtitleElement = null;
        this.container = null;
        this.trackElement = null;
        
        // Configuración de estilos
        this.subtitleStyles = {
            fontSize: '18px',
            fontFamily: 'Arial, sans-serif',
            color: '#ffffff',
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            padding: '8px 16px',
            borderRadius: '4px',
            textAlign: 'center',
            position: 'absolute',
            bottom: '60px',
            left: '50%',
            transform: 'translateX(-50%)',
            zIndex: '1000',
            maxWidth: '80%',
            wordWrap: 'break-word'
        };
        
        this.init();
    }
    
    init() {
        this.injectStyles();
        this.waitForVideo();
    }
    
    injectStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .subtitle-container {
                position: absolute;
                bottom: 60px;
                left: 50%;
                transform: translateX(-50%);
                z-index: 1000;
                max-width: 80%;
                pointer-events: none;
            }
            
            .subtitle-text {
                font-size: 18px;
                font-family: Arial, sans-serif;
                color: #ffffff;
                background-color: rgba(0, 0, 0, 0.8);
                padding: 8px 16px;
                border-radius: 4px;
                text-align: center;
                word-wrap: break-word;
                line-height: 1.4;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
            }
            
            .subtitle-controls {
                position: absolute;
                top: 10px;
                right: 10px;
                z-index: 1001;
                background: rgba(0, 0, 0, 0.7);
                border-radius: 4px;
                padding: 5px;
                display: none;
            }
            
            .subtitle-controls.active {
                display: flex;
                gap: 5px;
            }
            
            .subtitle-btn {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 5px 10px;
                border-radius: 3px;
                cursor: pointer;
                font-size: 12px;
                transition: all 0.2s ease;
            }
            
            .subtitle-btn:hover {
                background: rgba(255, 255, 255, 0.3);
            }
            
            .subtitle-btn.active {
                background: #f97316;
                border-color: #f97316;
            }
            
            .subtitle-file-input {
                display: none;
            }
        `;
        document.head.appendChild(style);
    }
    
    waitForVideo() {
        // Esperar a que el video esté disponible
        const checkVideo = () => {
            const video = document.querySelector('video');
            if (video) {
                this.setupVideo(video);
            } else {
                setTimeout(checkVideo, 1000);
            }
        };
        checkVideo();
    }
    
    setupVideo(video) {
        this.currentVideo = video;
        this.createSubtitleElements();
        this.setupControls();
        this.setupEventListeners();
    }
    
    createSubtitleElements() {
        // Crear contenedor de subtítulos
        this.container = document.querySelector('.player-inner');
        if (!this.container) return;
        
        // Crear elemento de subtítulos
        this.subtitleElement = document.createElement('div');
        this.subtitleElement.className = 'subtitle-container';
        this.subtitleElement.style.display = 'none';
        
        const subtitleText = document.createElement('div');
        subtitleText.className = 'subtitle-text';
        this.subtitleElement.appendChild(subtitleText);
        
        this.container.appendChild(this.subtitleElement);
        
        // Crear controles de subtítulos
        this.createControls();
    }
    
    createControls() {
        const controlsDiv = document.createElement('div');
        controlsDiv.className = 'subtitle-controls';
        
        // Botón de activar/desactivar subtítulos
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'subtitle-btn';
        toggleBtn.textContent = 'CC';
        toggleBtn.title = 'Activar/Desactivar subtítulos';
        toggleBtn.addEventListener('click', () => this.toggleSubtitles());
        
        // Botón de cargar subtítulos
        const loadBtn = document.createElement('button');
        loadBtn.className = 'subtitle-btn';
        loadBtn.textContent = 'Cargar';
        loadBtn.title = 'Cargar archivo de subtítulos';
        loadBtn.addEventListener('click', () => this.loadSubtitleFile());
        
        // Input file oculto
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.className = 'subtitle-file-input';
        fileInput.accept = '.srt,.vtt,.txt';
        fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        
        controlsDiv.appendChild(toggleBtn);
        controlsDiv.appendChild(loadBtn);
        controlsDiv.appendChild(fileInput);
        
        this.container.appendChild(controlsDiv);
        
        // Mostrar controles cuando el mouse esté sobre el video
        this.container.addEventListener('mouseenter', () => {
            controlsDiv.classList.add('active');
        });
        
        this.container.addEventListener('mouseleave', () => {
            controlsDiv.classList.remove('active');
        });
        
        this.controlsDiv = controlsDiv;
        this.toggleBtn = toggleBtn;
        this.fileInput = fileInput;
    }
    
    setupEventListeners() {
        if (!this.currentVideo) return;
        
        this.currentVideo.addEventListener('timeupdate', () => {
            if (this.isEnabled && this.subtitles.length > 0) {
                this.updateSubtitle();
            }
        });
        
        this.currentVideo.addEventListener('loadedmetadata', () => {
            this.hideSubtitle();
        });
        
        this.currentVideo.addEventListener('seeked', () => {
            if (this.isEnabled && this.subtitles.length > 0) {
                this.updateSubtitle();
            }
        });
    }
    
    setupControls() {
        // No necesario, ya configurado en createControls
    }
    
    toggleSubtitles() {
        this.isEnabled = !this.isEnabled;
        
        if (this.toggleBtn) {
            this.toggleBtn.classList.toggle('active', this.isEnabled);
        }
        
        if (!this.isEnabled) {
            this.hideSubtitle();
        } else {
            this.updateSubtitle();
        }
    }
    
    loadSubtitleFile() {
        if (this.fileInput) {
            this.fileInput.click();
        }
    }
    
    handleFileSelect(event) {
        const file = event.target.files[0];
        if (!file) return;
        
        const reader = new FileReader();
        reader.onload = (e) => {
            const content = e.target.result;
            this.parseSubtitles(content, file.name);
        };
        reader.readAsText(file);
    }
    
    parseSubtitles(content, filename) {
        const extension = filename.split('.').pop().toLowerCase();
        
        switch (extension) {
            case 'srt':
                this.parseSRT(content);
                break;
            case 'vtt':
                this.parseVTT(content);
                break;
            default:
                this.parseSRT(content); // Por defecto intentar SRT
        }
    }
    
    parseSRT(content) {
        this.subtitles = [];
        const lines = content.split(/\r?\n/);
        let currentSubtitle = null;
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();
            
            if (line === '') {
                if (currentSubtitle && currentSubtitle.text) {
                    this.subtitles.push(currentSubtitle);
                    currentSubtitle = null;
                }
                continue;
            }
            
            // Si la línea es un número de secuencia
            if (/^\d+$/.test(line)) {
                if (currentSubtitle && currentSubtitle.text) {
                    this.subtitles.push(currentSubtitle);
                }
                currentSubtitle = { start: 0, end: 0, text: '' };
                continue;
            }
            
            // Si la línea contiene timestamps
            if (line.includes('-->')) {
                const times = line.split('-->');
                if (times.length === 2 && currentSubtitle) {
                    currentSubtitle.start = this.parseTime(times[0].trim());
                    currentSubtitle.end = this.parseTime(times[1].trim());
                }
                continue;
            }
            
            // Si es texto de subtítulo
            if (currentSubtitle && line) {
                currentSubtitle.text += (currentSubtitle.text ? '\n' : '') + line;
            }
        }
        
        // Agregar el último subtítulo si existe
        if (currentSubtitle && currentSubtitle.text) {
            this.subtitles.push(currentSubtitle);
        }
        
        console.log(`Subtítulos cargados: ${this.subtitles.length}`);
        this.showNotification(`Subtítulos cargados: ${this.subtitles.length}`);
    }
    
    parseVTT(content) {
        // Implementación básica de VTT (similar a SRT pero con formato diferente)
        this.subtitles = [];
        const lines = content.split(/\r?\n/);
        let currentSubtitle = null;
        
        // Saltar la línea WEBVTT
        let startIndex = 0;
        if (lines[0] && lines[0].includes('WEBVTT')) {
            startIndex = 1;
        }
        
        for (let i = startIndex; i < lines.length; i++) {
            const line = lines[i].trim();
            
            if (line === '') {
                if (currentSubtitle && currentSubtitle.text) {
                    this.subtitles.push(currentSubtitle);
                    currentSubtitle = null;
                }
                continue;
            }
            
            // Si la línea contiene timestamps
            if (line.includes('-->')) {
                const times = line.split('-->');
                if (times.length === 2) {
                    if (currentSubtitle && currentSubtitle.text) {
                        this.subtitles.push(currentSubtitle);
                    }
                    currentSubtitle = {
                        start: this.parseTime(times[0].trim()),
                        end: this.parseTime(times[1].trim()),
                        text: ''
                    };
                }
                continue;
            }
            
            // Si es texto de subtítulo
            if (currentSubtitle && line) {
                currentSubtitle.text += (currentSubtitle.text ? '\n' : '') + line;
            }
        }
        
        // Agregar el último subtítulo si existe
        if (currentSubtitle && currentSubtitle.text) {
            this.subtitles.push(currentSubtitle);
        }
        
        console.log(`Subtítulos VTT cargados: ${this.subtitles.length}`);
        this.showNotification(`Subtítulos VTT cargados: ${this.subtitles.length}`);
    }
    
    parseTime(timeString) {
        // Convertir tiempo en formato "00:00:00,000" o "00:00:00.000" a segundos
        const parts = timeString.replace(',', '.').split(':');
        if (parts.length === 3) {
            const hours = parseInt(parts[0]) || 0;
            const minutes = parseInt(parts[1]) || 0;
            const seconds = parseFloat(parts[2]) || 0;
            return hours * 3600 + minutes * 60 + seconds;
        }
        return 0;
    }
    
    updateSubtitle() {
        if (!this.currentVideo || this.subtitles.length === 0) return;
        
        const currentTime = this.currentVideo.currentTime;
        let foundSubtitle = null;
        
        // Buscar subtítulo actual
        for (const subtitle of this.subtitles) {
            if (currentTime >= subtitle.start && currentTime <= subtitle.end) {
                foundSubtitle = subtitle;
                break;
            }
        }
        
        if (foundSubtitle) {
            this.showSubtitle(foundSubtitle.text);
        } else {
            this.hideSubtitle();
        }
    }
    
    showSubtitle(text) {
        if (!this.subtitleElement) return;
        
        const subtitleText = this.subtitleElement.querySelector('.subtitle-text');
        if (subtitleText) {
            subtitleText.textContent = text;
            this.subtitleElement.style.display = 'block';
        }
    }
    
    hideSubtitle() {
        if (this.subtitleElement) {
            this.subtitleElement.style.display = 'none';
        }
    }
    
    showNotification(message) {
        // Crear notificación temporal
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #f97316;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            z-index: 10000;
            font-size: 14px;
            animation: slideIn 0.3s ease;
        `;
        notification.textContent = message;
        
        // Agregar animación
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(notification);
        
        // Eliminar después de 3 segundos
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
            if (style.parentNode) {
                style.parentNode.removeChild(style);
            }
        }, 3000);
    }
    
    // Método para cargar subtítulos desde URL
    loadSubtitlesFromUrl(url) {
        fetch(url)
            .then(response => response.text())
            .then(content => {
                const filename = url.split('/').pop() || 'subtitles.srt';
                this.parseSubtitles(content, filename);
            })
            .catch(error => {
                console.error('Error al cargar subtítulos desde URL:', error);
                this.showNotification('Error al cargar subtítulos desde URL');
            });
    }
    
    // Método para obtener el estado actual
    getStatus() {
        return {
            enabled: this.isEnabled,
            loaded: this.subtitles.length > 0,
            count: this.subtitles.length
        };
    }
}

// Inicializar el gestor de subtítulos cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.subtitleManager = new SubtitleManager();
    });
} else {
    window.subtitleManager = new SubtitleManager();
}

// Función global para cargar subtítulos desde URL
window.loadSubtitlesFromUrl = function(url) {
    if (window.subtitleManager) {
        window.subtitleManager.loadSubtitlesFromUrl(url);
    }
};

// Función global para obtener el estado de los subtítulos
window.getSubtitleStatus = function() {
    if (window.subtitleManager) {
        return window.subtitleManager.getStatus();
    }
    return { enabled: false, loaded: false, count: 0 };
};

// Función para cargar subtítulos desde archivo M3U
window.loadSubtitlesFromM3U = async function(m3uUrl) {
    try {
        const response = await fetch(m3uUrl);
        const content = await response.text();
        const movies = parseM3U(content);
        
        // Generar subtítulos automáticamente
        let subtitles = '';
        let time = 0;
        
        movies.forEach((movie, index) => {
            const translatedTitle = translateMovieTitle(movie.title);
            
            // Subtítulo de presentación
            subtitles += `${index * 2 + 1}\\n`;
            subtitles += `${formatTime(time)} --> ${formatTime(time + 3)}\\n`;
            subtitles += `Reproduciendo: ${translatedTitle}\\n\\n`;
            
            time += 5;
            
            // Subtítulo de información
            subtitles += `${index * 2 + 2}\\n`;
            subtitles += `${formatTime(time)} --> ${formatTime(time + 3)}\\n`;
            subtitles += `Título original: ${movie.title}\\n\\n`;
            
            time += 5;
        });
        
        if (window.subtitleManager) {
            window.subtitleManager.parseSubtitles(subtitles, 'm3u-generated.srt');
        }
        
        return {
            success: true,
            movieCount: movies.length,
            subtitleCount: movies.length * 2
        };
        
    } catch (error) {
        console.error('Error al cargar subtítulos desde M3U:', error);
        return {
            success: false,
            error: error.message
        };
    }
};

// Función auxiliar para parsear M3U
function parseM3U(content) {
    const lines = content.split('\\n');
    const movies = [];
    let currentTitle = '';
    
    lines.forEach(line => {
        line = line.trim();
        if (line.startsWith('#EXTINF:')) {
            // Extraer el título después de la última coma
            const lastCommaIndex = line.lastIndexOf(',');
            if (lastCommaIndex !== -1) {
                currentTitle = line.substring(lastCommaIndex + 1).trim();
            }
        } else if (line && !line.startsWith('#') && currentTitle && line.includes('http')) {
            // Es una URL de película
            movies.push({
                title: currentTitle,
                url: line,
                id: movies.length + 1
            });
            currentTitle = '';
        }
    });
    
    return movies;
}

// Función para traducir títulos de películas
function translateMovieTitle(title) {
    const translations = {
        'comedy': 'comedia',
        'movie': 'película',
        'action': 'acción',
        'adventure': 'aventura',
        'romance': 'romance',
        'horror': 'terror',
        'suspense': 'suspenso',
        'drama': 'drama',
        'fantasy': 'fantasía',
        'science fiction': 'ciencia ficción',
        'animation': 'animación',
        'family': 'familia',
        'music': 'música',
        'documentary': 'documental',
        'dubbed': 'doblado',
        'subtitled': 'subtitulado',
        'Latin': 'Latino',
        'HD': 'HD',
        '4K': '4K',
        '1080p': '1080p',
        '720p': '720p'
    };
    
    let translated = title;
    
    Object.keys(translations).forEach(english => {
        const spanish = translations[english];
        const regex = new RegExp(`\\b${english}\\b`, 'gi');
        translated = translated.replace(regex, spanish);
    });
    
    return translated;
}

// Función auxiliar para formatear tiempo
function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    const ms = Math.floor((seconds % 1) * 1000);
    
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')},${ms.toString().padStart(3, '0')}`;
}

// Función para cargar subtítulos desde el archivo comedia1tv.m3u de GitHub
window.loadGitHubSubtitles = function() {
    const githubUrl = 'https://raw.githubusercontent.com/agustino8080/listam3u/main/comedia1tv.m3u';
    
    fetch(githubUrl)
        .then(response => response.text())
        .then(content => {
            // Parsear el contenido M3U para extraer información de películas
            const lines = content.split('\n');
            const movies = [];
            let currentTitle = '';
            
            lines.forEach(line => {
                line = line.trim();
                if (line.startsWith('#EXTINF:')) {
                    // Extraer el título después de la última coma
                    const lastCommaIndex = line.lastIndexOf(',');
                    if (lastCommaIndex !== -1) {
                        currentTitle = line.substring(lastCommaIndex + 1).trim();
                    }
                } else if (line && !line.startsWith('#') && currentTitle) {
                    // Es una URL de película
                    movies.push({
                        title: currentTitle,
                        url: line,
                        originalLanguage: 'español'
                    });
                    currentTitle = '';
                }
            });
            
            // Crear subtítulos de muestra basados en las películas
            const sampleSubtitles = [];
            let currentTime = 0;
            
            movies.forEach((movie, index) => {
                // Crear subtítulos de muestra para cada película
                sampleSubtitles.push({
                    start: currentTime,
                    end: currentTime + 3,
                    text: `Ahora reproduciendo: ${movie.title}`
                });
                
                currentTime += 5;
                
                sampleSubtitles.push({
                    start: currentTime,
                    end: currentTime + 3,
                    text: `Idioma original: ${movie.originalLanguage}`
                });
                
                currentTime += 5;
            });
            
            // Cargar los subtítulos en el gestor
            if (window.subtitleManager) {
                window.subtitleManager.subtitles = sampleSubtitles;
                alert(`Se han cargado ${sampleSubtitles.length} subtítulos de muestra para ${movies.length} películas desde comedia1tv.m3u`);
            }
        })
        .catch(error => {
            console.error('Error al cargar desde GitHub:', error);
            alert('Error al cargar el archivo desde GitHub');
        });
};

// Función para traducir subtítulos de inglés a español
window.translateSubtitlesToSpanish = function() {
    if (!window.subtitleManager || window.subtitleManager.subtitles.length === 0) {
        alert('Primero debes cargar subtítulos para traducir');
        return;
    }
    
    // Traducción básica de inglés a español (diccionario simple)
    const translations = {
        'Now playing': 'Reproduciendo ahora',
        'Original language': 'Idioma original',
        'English': 'Inglés',
        'Spanish': 'Español',
        'Welcome to the subtitle demo': 'Bienvenido al demo de subtítulos',
        'This is an example of SRT subtitles': 'Este es un ejemplo de subtítulos SRT',
        'You can load your own subtitles': 'Puedes cargar tus propios subtítulos',
        'Drag a .srt or .vtt file': 'Arrastra un archivo .srt o .vtt',
        'And subtitles will appear automatically!': '¡Y los subtítulos aparecerán automáticamente!',
        'You can also load from a URL': 'También puedes cargar desde una URL',
        'The system is very easy to use': 'El sistema es muy fácil de usar',
        'Enjoy your content with subtitles': 'Disfruta de tu contenido con subtítulos',
        'comedy': 'comedia',
        'movie': 'película',
        'action': 'acción',
        'adventure': 'aventura',
        'romance': 'romance',
        'horror': 'terror',
        'suspense': 'suspenso',
        'drama': 'drama',
        'fantasy': 'fantasía',
        'science fiction': 'ciencia ficción',
        'animation': 'animación',
        'family': 'familia',
        'music': 'música',
        'documentary': 'documental',
        'dubbed': 'doblado',
        'subtitled': 'subtitulado',
        'Latin': 'Latino'
    };
    
    // Traducir los subtítulos actuales
    window.subtitleManager.subtitles.forEach(subtitle => {
        let translatedText = subtitle.text;
        
        // Reemplazar palabras y frases comunes
        Object.keys(translations).forEach(english => {
            const spanish = translations[english];
            translatedText = translatedText.replace(new RegExp(english, 'gi'), spanish);
        });
        
        subtitle.text = translatedText;
    });
    
    alert('Subtítulos traducidos al español');
};