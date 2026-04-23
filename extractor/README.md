# 🖼️ Extractor de Imágenes Web

## 📋 Descripción

Un sistema completo para extraer imágenes de páginas web, incluyendo tiendas de eBay, Amazon, y cualquier sitio web. El extractor utiliza técnicas avanzadas para detectar imágenes en diferentes formatos y ubicaciones.

## ✨ Características

- ✅ **Extracción completa**: Detecta imágenes en `<img>`, `background-image`, y atributos data
- ✅ **Manejo de CORS**: Usa proxy para evitar restricciones de seguridad
- ✅ **Interfaz flotante**: Se integra en cualquier página web
- ✅ **Vista previa**: Muestra imágenes antes de descargar
- ✅ **Descarga individual**: Descarga imágenes seleccionadas
- ✅ **Detección inteligente**: Filtra por extensiones válidas
- ✅ **Responsive**: Funciona en dispositivos móviles
- ✅ **Fácil integración**: Solo incluir el script

## 🚀 Instalación

### Opción 1: Script separado
```html
<script src="image-extractor.js"></script>
```

### Opción 2: Integración directa
Copia el código de `image-extractor.js` en tu proyecto.

## 📖 Uso

### Desde la interfaz web
1. Abre `index.html` en tu navegador
2. Ingresa la URL de la página web
3. Haz clic en "Extraer Imágenes"
4. Visualiza y descarga las imágenes encontradas

### Desde la consola
```javascript
// Extraer imágenes de una página
extractImages('https://www.ebay.com/str/bluehaze');

// Usar el extractor directamente
imageExtractor.extractImages();
```

### Uso flotante (bookmarklet)
Crea un bookmarklet con este código:
```javascript
javascript:(function(){var s=document.createElement('script');s.src='https://tudominio.com/image-extractor.js';document.body.appendChild(s);})();
```

## 🎯 Ejemplos de uso

### eBay Store - BlueHaze
```
URL: https://www.ebay.com/str/bluehaze?_trksid=p4429486.m3561.l161211
Descripción: Tienda de eBay con productos de moda
```

### Amazon
```
URL: https://www.amazon.com
Descripción: Catálogo de productos
```

### Unsplash
```
URL: https://unsplash.com
Descripción: Fotografías de alta calidad
```

## 🔧 Cómo funciona

### 1. Extracción de imágenes
El extractor busca imágenes en múltiples formatos:
- **Etiquetas `<img>`**: src, data-src, data-original, data-lazy
- **Background images**: Estilos CSS con background-image
- **Data attributes**: Atributos personalizados con URLs

### 2. Procesamiento de URLs
- Convierte URLs relativas a absolutas
- Maneja diferentes protocolos (http, https, //)
- Filtra por extensiones válidas

### 3. Visualización
- Muestra miniaturas de las imágenes
- Información sobre dimensiones
- Vista previa en tamaño completo

## 📁 Estructura de archivos

```
extractor/
├── image-extractor.js      # Script principal del extractor
├── index.html             # Interfaz web demo
└── README.md              # Este archivo
```

## 🛠️ Personalización

### Cambiar el proxy CORS
```javascript
// En image-extractor.js
this.proxyUrl = 'https://api.allorigins.win/get?url=';
// Alternativas:
// - https://cors-anywhere.herokuapp.com/
// - https://api.codetabs.com/v1/proxy/
```

### Modificar filtros de imagen
```javascript
// Extensiones válidas
const validExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp'];

// Tamaño mínimo de URL
url.length > 10;
```

### Estilos personalizados
Modifica el CSS en la función `createUI()` para cambiar:
- Colores y temas
- Tamaños y posiciones
- Animaciones y efectos

## 🔍 Solución de problemas

### No se encuentran imágenes
- Verifica que la URL sea correcta
- Algunos sitios bloquean el acceso a robots
- Intenta usar un proxy diferente

### Error de CORS
- El proxy puede estar saturado
- Algunos sitios tienen protección estricta
- Intenta desde una extensión del navegador

### Imágenes sin cargar
- Las URLs pueden estar rotas
- El servidor puede bloquear hotlinking
- Verifica la conexión a internet

## 📄 Licencia

Este extractor es software libre y puede ser usado, modificado y distribuido libremente.

## 🤝 Contribuciones

Siéntete libre de:
- Reportar bugs
- Sugerir mejoras
- Añadir nuevas características
- Optimizar el código

---

**¡Disfruta extrayendo imágenes de la web! 🖼️**