# 🔬 Academic Markdown Translator (Local LLM & Ollama)

Herramienta en Python diseñada para automatizar la **traducción masiva de artículos científicos y documentos técnicos en formato Markdown (`.md`)** del inglés al español, utilizando modelos locales a través de **Ollama**. 

El script está optimizado para preservar fórmulas matemáticas (LaTeX), tablas, bloques de código y la estructura de encabezados, aplicando un tono formal y académico.

---

## 🚀 Características Principales

* **100% Local y Privado:** Sin dependencias de APIs de pago (como OpenAI o DeepL). Todo se ejecuta en tu equipo usando Ollama.
* **Preservación Estructural Estricta:** 
  * Respeta fórmulas matemáticas en notación LaTeX ($...$,$$, ecuaciones).
  * Mantiene intactas las tablas en Markdown (`| --- |`) y bloques de código.
* **Segmentación Inteligente:** Divide los documentos largos por secciones lógicas y párrafos para evitar cortes abruptos y asegurar que el modelo no exceda el contexto.
* **Sistema de Checkpoint (Reanudación):** Si el proceso se interrumpe, el script detecta automáticamente los archivos ya traducidos en la carpeta de salida y los salta para no repetir trabajo.
* **Control por Prompt de Sistema:** Configurado mediante un rol de traductor académico experto en IA, computación y privacidad con un tono formal de posgrado.

---

## 🛠️ Requisitos Previos

1. **Python 3.10 o superior** instalado.
2. **Ollama** instalado y ejecutándose en tu sistema. Puedes descargarlo desde [ollama.com](https://ollama.com/).

### Modelo de Ollama recomendado
Descarga el modelo que prefieras utilizar en el script (por ejemplo, `gemma4`, `qwen2.5`, o `llama3.1`):

```bash
ollama pull gemma4
```

### 📦 Instalación
Clona este repositorio o guarda el script en tu proyecto.

Instala la biblioteca oficial de Python para Ollama:
```bash
pip install ollama
```

### 📂 Estructura del Proyecto
Crea o organiza tus carpetas de la siguiente manera antes de ejecutar el script:
```
traductor-markdown/
│
├── traductorarticulomd.py              # Script principal de Python
├── bibliografiamarkdown/     # Carpeta con tus archivos .md originales (Inglés)
│   ├── paper_1.md
│   └── paper_2.md
└── bibliografiamarkdown_es/  # Carpeta de salida (se crea sola con los archivos _ES.md)
```

### ⚙️ Uso
1. Coloca tus archivos Markdown originales en la carpeta ./bibliografiamarkdown.

2. (Opcional) Modifica las variables globales en el script si deseas cambiar las rutas o el modelo LLM:
```
CARPETA_ORIGINAL_MD = "./bibliografiamarkdown"
CARPETA_TRADUCIDA_MD = "./bibliografiamarkdown_es"
MODELO_LLM = "gemma4"
```
3. Ejecuta el script:
```
python traductorarticulomd.py
```
Durante la ejecución verás el progreso detallado en la consola:
```
Iniciando traducción masiva de 2 documentos científicos...
[1/2] Traduciendo: paper_1.md...
   └─ Dividido en 14 bloques seguros para traducción.
   ✅ Guardado exitoso: paper_1_ES.md
[2/2] Saltando (ya traducido): paper_2.md
```

### 🔧 Personalización del Prompt
Si necesitas ajustar el comportamiento de la traducción (por ejemplo, permitir notas del traductor o cambiar el dominio técnico), puedes editar directamente la constante PROMPT_SISTEMA al inicio del código.

### 📄 Licencia
Este proyecto se distribuye bajo la licencia MIT. Siéntete libre de adaptarlo para tus investigaciones, tesis o proyectos personales.
