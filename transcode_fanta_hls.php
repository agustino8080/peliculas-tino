<?php
// transcode_fanta_hls.php
// Requiere FFmpeg instalado en el servidor (accesible en la ruta del sistema)

header('Content-Type: application/json; charset=utf-8');

// 1) Validar parámetro
if (empty($_GET['url'])) {
    echo json_encode(['error' => 'Falta parámetro url']);
    exit;
}

$sourceUrl = $_GET['url'];

// Validación básica (solo permitir fanta.56k.es)
if (strpos($sourceUrl, 'https://fanta.56k.es/video/peliculas/2D/') !== 0) {
    echo json_encode(['error' => 'URL no permitida']);
    exit;
}

// 2) Configuración de rutas
$baseOutputDir = __DIR__ . '/hls_output';
if (!is_dir($baseOutputDir)) {
    mkdir($baseOutputDir, 0775, true);
}

// Nombre único por archivo (hash)
$hash = md5($sourceUrl);
$outDir = $baseOutputDir . '/' . $hash;
$playlistFile = $outDir . '/index.m3u8';

// Si ya existe una transcodificación reciente, reutiliza
if (file_exists($playlistFile)) {
    $publicBase = 'https://TU_DOMINIO/hls_output/' . $hash;
    echo json_encode([
        'status' => 'ok',
        'hls_url' => $publicBase . '/index.m3u8',
        'cached' => true
    ]);
    exit;
}

// 3) Crear carpeta salida
if (!is_dir($outDir)) {
    mkdir($outDir, 0775, true);
}

// 4) Ejecutar FFmpeg para generar HLS
// Ajusta la ruta a ffmpeg si es necesario
$ffmpegBin = '/usr/bin/ffmpeg';

// Opciones simples: HLS de bitrate fijo, códecs compatibles
$cmd = sprintf(
    '%s -y -i %s -c:v libx264 -preset veryfast -c:a aac -strict -2 -f hls ' .
    '-hls_time 6 -hls_playlist_type vod %s 2>&1',
    escapeshellcmd($ffmpegBin),
    escapeshellarg($sourceUrl),
    escapeshellarg($playlistFile)
);

exec($cmd, $output, $returnVar);

if ($returnVar !== 0 || !file_exists($playlistFile)) {
    echo json_encode([
        'error' => 'Error al transcodificar con FFmpeg',
        'ffmpeg_output' => $output
    ]);
    exit;
}

// 5) Devolver URL pública del HLS
$publicBase = 'https://TU_DOMINIO/hls_output/' . $hash;

echo json_encode([
    'status' => 'ok',
    'hls_url' => $publicBase . '/index.m3u8',
    'cached' => false
]);
