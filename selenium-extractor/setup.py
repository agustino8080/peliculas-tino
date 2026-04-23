#!/usr/bin/env python3
"""
🏃‍♂️ Adidas Selenium Scraper - Setup Script
Instalador automático para el extractor de Adidas
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def install_package(package):
    """Instalar un paquete pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado correctamente")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Error instalando {package}")
        return False

def check_chrome():
    """Verificar si Chrome está instalado"""
    system = platform.system()
    
    if system == "Windows":
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]
    elif system == "Darwin":  # macOS
        chrome_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        ]
    else:  # Linux
        chrome_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium"
        ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ Chrome encontrado: {path}")
            return True
    
    print("⚠️ Chrome no encontrado. Por favor instala Google Chrome:")
    print("📥 https://www.google.com/chrome/")
    return False

def setup_environment():
    """Configurar el entorno completo"""
    print("🚀 Iniciando configuración de Adidas Selenium Scraper")
    print("=" * 50)
    
    # Verificar Python
    print(f"📍 Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requerido")
        return False
    
    # Verificar Chrome
    print("🔍 Verificando Chrome...")
    if not check_chrome():
        return False
    
    # Instalar dependencias
    print("\n📦 Instalando dependencias...")
    requirements = [
        "selenium>=4.15.2",
        "requests>=2.31.0",
        "webdriver-manager>=4.0.1",
        "beautifulsoup4>=4.12.2",
        "flask>=2.3.0",
        "flask-cors>=4.0.0"
    ]
    
    success_count = 0
    for req in requirements:
        if install_package(req):
            success_count += 1
    
    print(f"\n📊 {success_count}/{len(requirements)} dependencias instaladas")
    
    if success_count < len(requirements):
        print("⚠️ Algunas dependencias fallaron. Intenta instalar manualmente:")
        print("pip install -r requirements.txt")
        return False
    
    # Crear directorios
    print("\n📁 Creando directorios...")
    directories = [
        "adidas_data",
        "adidas_data/images",
        "templates"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ {directory}")
    
    # Copiar archivos de plantillas
    print("\n📋 Configurando plantillas...")
    try:
        if os.path.exists("index.html") and not os.path.exists("templates/index.html"):
            import shutil
            shutil.copy("index.html", "templates/index.html")
            print("✅ Plantillas configuradas")
    except Exception as e:
        print(f"⚠️ Error configurando plantillas: {e}")
    
    print("\n🎉 ¡Configuración completada!")
    print("=" * 50)
    
    return True

def create_run_scripts():
    """Crear scripts de ejecución"""
    
    # Script para Windows
    windows_script = """@echo off
echo 🏃‍♂️ Adidas Selenium Scraper
echo ========================
echo.
echo 1. Interfaz Web (Recomendado)
echo 2. Scraping Directo
echo 3. Scraping Avanzado
echo 4. Salir
echo.
set /p choice="Selecciona una opción (1-4): "

if "%choice%"=="1" goto web
if "%choice%"=="2" goto basic
if "%choice%"=="3" goto advanced
if "%choice%"=="4" goto end

goto end

:web
echo 🌐 Iniciando interfaz web...
python app.py
goto end

:basic
echo 🔍 Ejecutando scraping básico...
python adidas_scraper.py
goto end

:advanced
echo 🚀 Ejecutando scraping avanzado...
python adidas_advanced_scraper.py
goto end

:end
echo 👋 ¡Hasta luego!
pause
"""
    
    # Script para Unix (Linux/Mac)
    unix_script = """#!/bin/bash

echo "🏃‍♂️ Adidas Selenium Scraper"
echo "========================"
echo ""
echo "1. Interfaz Web (Recomendado)"
echo "2. Scraping Directo"
echo "3. Scraping Avanzado"
echo "4. Salir"
echo ""
read -p "Selecciona una opción (1-4): " choice

case $choice in
    1)
        echo "🌐 Iniciando interfaz web..."
        python3 app.py
        ;;
    2)
        echo "🔍 Ejecutando scraping básico..."
        python3 adidas_scraper.py
        ;;
    3)
        echo "🚀 Ejecutando scraping avanzado..."
        python3 adidas_advanced_scraper.py
        ;;
    4)
        echo "👋 ¡Hasta luego!"
        exit 0
        ;;
    *)
        echo "❌ Opción no válida"
        ;;
esac
"""
    
    # Guardar scripts
    system = platform.system()
    
    if system == "Windows":
        with open("run.bat", "w") as f:
            f.write(windows_script)
        print("✅ Script de ejecución creado: run.bat")
    else:
        with open("run.sh", "w") as f:
            f.write(unix_script)
        os.chmod("run.sh", 0o755)
        print("✅ Script de ejecución creado: run.sh")

def main():
    """Función principal"""
    print("🏃‍♂️ Adidas Selenium Scraper - Instalador")
    print("=" * 50)
    
    try:
        # Configurar entorno
        if setup_environment():
            # Crear scripts de ejecución
            create_run_scripts()
            
            print("\n🚀 ¡Instalación exitosa!")
            print("\n📋 Próximos pasos:")
            
            if platform.system() == "Windows":
                print("1. Ejecuta: run.bat")
            else:
                print("1. Ejecuta: ./run.sh")
            
            print("2. O ejecuta directamente:")
            print("   python app.py              # Interfaz web")
            print("   python adidas_scraper.py   # Scraping básico")
            print("   python adidas_advanced_scraper.py  # Scraping avanzado")
            
            print("\n🌐 La interfaz web estará disponible en:")
            print("   http://localhost:5000")
            
            print("\n📖 Documentación completa en: README.md")
            
        else:
            print("\n❌ La instalación falló. Por favor verifica:")
            print("- Python 3.8+ está instalado")
            print("- Google Chrome está instalado")
            print("- Tienes permisos de escritura")
            print("- Tu conexión a internet funciona")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Instalación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("Por favor reporta este error con los detalles del error")

if __name__ == "__main__":
    main()