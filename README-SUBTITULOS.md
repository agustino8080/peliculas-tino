# 🎬 Sistema de Subtítulos para PELIS TINO

## 📋 Descripción

Este sistema añade funcionalidad de subtítulos al reproductor PELIS TINO sin modificar el archivo HTML original. Es completamente independiente y se puede integrar fácilmente.

## ✨ Características

- ✅ **Sin modificaciones al HTML original** - Solo añade una línea de código
- ✅ **Soporta formatos SRT y VTT** - Los formatos más comunes de subtítulos
- ✅ **Controles intuitivos** - Botón CC para activar/desactivar
- ✅ **Carga por arrastrar y soltar** - Interfaz moderna y fácil de usar
- ✅ **Carga desde URL** - Puedes cargar subtítulos desde internet
- ✅ **Sincronización automática** - Se sincroniza perfectamente con el video
- ✅ **Diseño responsive** - Se adapta a cualquier tamaño de pantalla
- ✅ **Estilos personalizables** - Fácil de personalizar los colores y tamaños

## 🚀 Instalación

### Paso 1: Copiar el archivo
Copia el archivo `subtitles.js` a la misma carpeta donde está tu `pelis.html`

### Paso 2: Añadir la referencia
Abre `pelis.html` y añade esta línea **justo antes del cierre de `</body>`**:

```html
<script src="subtitles.js"></script>
</body>
```

### Paso 3: Listo 🎉
¡Eso es todo! Los subtítulos estarán disponibles automáticamente.

## 📖 Cómo usar

### 1. Controles del reproductor
- Pasa el mouse sobre el reproductor de video
- Verás los controles de subtítulos en la esquina superior derecha
- **Botón CC**: Activa/desactiva los subtítulos
- **Botón Cargar**: Abre el selector de archivos

### 2. Cargar subtítulos

#### Opción A: Archivo local
1. Haz clic en el botón "Cargar" o arrastra un archivo `.srt` o `.vtt` al área del reproductor
2. Selecciona tu archivo de subtítulos
3. ¡Los subtítulos aparecerán automáticamente!

#### Opción B: Desde URL
```javascript
// Cargar subtítulos desde una URL
loadSubtitlesFromUrl('https://tudominio.com/subtitulos.srt');
```

#### Opción C: Desde JavaScript
```javascript
// Cargar subtítulos desde una cadena SRT
const srtContent = `1
00:00:01,000 --> 00:00:04,000
Este es un subtítulo de ejemplo`;

// El sistema los parseará automáticamente
```

## 🎨 Personalización

### Cambiar estilos de los subtítulos
```javascript
// Ejemplo de cómo cambiar los estilos
const customStyles = {
    fontSize: '20px',
    color: '#ffff00',
    backgroundColor: 'rgba(0, 0, 0, 0.9)',
    padding: '10px 20px'
};
```

### Verificar estado
```javascript
// Obtener información sobre los subtítulos
const status = getSubtitleStatus();
console.log(status);
// Devuelve: { enabled: true, loaded: true, count: 45 }
```

## 📁 Estructura de archivos

```
peliculas/
├── pelis.html              # Archivo original (no modificar)
├── transcode_fanta_hls.php # Script PHP original
├── subtitles.js            # ✅ Sistema de subtítulos (nuevo)
├── demo-subtitulos.html    # Demo interactivo (nuevo)
└── README.md              # Este archivo (nuevo)
```

## 🧪 Demo

Abre `demo-subtitulos.html` en tu navegador para ver una demostración completa de todas las funcionalidades.

## 📝 Ejemplos de archivos SRT

### Ejemplo básico
```
1
00:00:01,000 --> 00:00:04,000
Bienvenido a PELIS TINO

2
00:00:05,000 --> 00:00:08,000
Este es un ejemplo de subtítulos
```

### Ejemplo con múltiples líneas
```
1
00:00:01,000 --> 00:00:04,000
Primera línea del subtítulo
Segunda línea del mismo subtítulo

2
00:00:05,000 --> 00:00:08,000
Otro subtítulo
```

## 🔧 Solución de problemas

### Los subtítulos no aparecen
1. Verifica que el archivo `subtitles.js` esté en la misma carpeta que `pelis.html`
2. Asegúrate de que la línea `<script src="subtitles.js"></script>` esté antes de `</body>`
3. Comprueba que el video se esté reproduciendo

### Los subtítulos están desincronizados
- Asegúrate de que el archivo SRT tenga el formato correcto de tiempo
- Verifica que los timestamps estén en formato `HH:MM:SS,MMM`

### No puedo cargar archivos
- Asegúrate de que el archivo tenga extensión `.srt` o `.vtt`
- Verifica que el archivo no esté dañado

## 📞 Soporte

Si tienes problemas o preguntas:
1. Abre el demo (`demo-subtitulos.html`) para verificar que funciona
2. Revisa la consola del navegador (F12 → Consola)
3. Verifica que estés siguiendo los pasos de instalación

## ⚖️ Licencia

Este sistema de subtítulos es software libre y puede ser usado, modificado y distribuido libremente.

---

**¡Disfruta de tus películas con subtítulos! 🍿**