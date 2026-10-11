import os
import glob
import re
import ollama

CARPETA_ORIGINAL_MD = "./bibliografiamarkdown"
CARPETA_TRADUCIDA_MD = "./bibliografiamarkdown_es"
MODELO_LLM = "gemma4"  # O llama3.1, qwen2.5, mistral-nemo

os.makedirs(CARPETA_TRADUCIDA_MD, exist_ok=True)

PROMPT_SISTEMA = """
Eres un traductor académico profesional y experto en Inteligencia Artificial, Computación y Privacidad.
Tu tarea es traducir el texto científico del inglés al español de forma fiel, rigurosa y formal.

REGLAS ESTRICTAS DE TRADUCCIÓN:
1. PRESERVACIÓN MATEMÁTICA TOTAL: NO modifiques, traduzcas ni alteres ninguna fórmula matemática, símbolo o notación LaTeX (ej. $...$, $$, \\begin{equation}, \\alpha, \\theta, \\mathcal{D}_{forget}, \\nabla). Déjalas exactamente idénticas al original.
2. PRESERVACIÓN DE TABLAS: Mantén intacta la estructura de tablas en formato Markdown (| --- |). Traduce el texto dentro de las celdas, pero no alteres los separadores ni los números.
3. ACRÓNIMOS Y CÓDIGO: Mantén acrónimos técnicos estándar (ej. MUSE, FUMA, TOFU, LLM, LoRA, GDPR, CCPA, MIA, RAG, ViT) y bloques de código o comandos intactos.
4. TONO: Usa un lenguaje formal en tercera persona propio de publicaciones de posgrado (Ph.D.).
5. FORMATO DE SALIDA: Devuelve ÚNICAMENTE el texto traducido. No agregues saludos, explicaciones, notas del traductor ni bloques de código adicionales alrededor de toda la respuesta.
"""

def segmentar_markdown_por_secciones(texto: str, max_caracteres: int = 3500) -> list:
    """
    Divide el documento en fragmentos respetando encabezados (#, ##, ###)
    y párrafos dobles para no cortar tablas o fórmulas por la mitad.
    """
    # Dividir preferentemente por encabezados o saltos de párrafo
    bloques_crudos = re.split(r'(\n#{1,4} [^\n]+\n|\n\n+)', texto)
    
    chunks = []
    chunk_actual = ""
    
    for bloque in bloques_crudos:
        if len(chunk_actual) + len(bloque) <= max_caracteres:
            chunk_actual += bloque
        else:
            if chunk_actual.strip():
                chunks.append(chunk_actual)
            chunk_actual = bloque
            
    if chunk_actual.strip():
        chunks.append(chunk_actual)
        
    return chunks

def traducir_bloque_con_llm(bloque_texto: str) -> str:
    """Envía el fragmento al LLM para su traducción estructurada."""
    if not bloque_texto.strip():
        return ""
    
    # Si el bloque es solo una imagen o separador, no gastar inferencia
    if re.match(r'^\s*<!--\s*image\s*-->\s*$', bloque_texto):
        return bloque_texto

    try:
        response = ollama.chat(
            model=MODELO_LLM,
            messages=[
                {"role": "system", "content": PROMPT_SISTEMA},
                {"role": "user", "content": f"Traduce el siguiente fragmento al español respetando estrictamente las tablas y fórmulas:\n\n{bloque_texto}"}
            ],
            options={"temperature": 0.1, "num_ctx": 8192}
        )
        
        if hasattr(response, 'message'):
            return response.message.content
        else:
            return response['message']['content']
    except Exception as e:
        print(f"   ❌ Error traduciendo bloque: {e}")
        return bloque_texto  # Fallback: retorna el original si hay error

def procesar_traduccion_masiva(directorio_entrada: str, directorio_salida: str):
    """Procesa todos los archivos .md por lotes y guarda los equivalentes en español."""
    archivos = glob.glob(os.path.join(directorio_entrada, "*.md"))
    total_archivos = len(archivos)
    
    print(f"Iniciando traducción masiva de {total_archivos} documentos científicos...")
    
    for idx, filepath in enumerate(archivos, start=1):
        nombre_archivo = os.path.basename(filepath)
        nombre_archivo_salida = nombre_archivo.replace(".md", "_ES.md")
        ruta_salida = os.path.join(directorio_salida, nombre_archivo_salida)
        
        # Checkpoint: Si ya se tradujo previamente, saltarlo
        if os.path.exists(ruta_salida):
            print(f"[{idx}/{total_archivos}] Saltando (ya traducido): {nombre_archivo}")
            continue
            
        print(f"[{idx}/{total_archivos}] Traduciendo: {nombre_archivo}...")
        
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            texto_completo = f.read()
            
        fragmentos = segmentar_markdown_por_secciones(texto_completo, max_caracteres=3500)
        print(f"   └─ Dividido en {len(fragmentos)} bloques seguros para traducción.")
        
        traducciones = []
        for b_idx, chunk in enumerate(fragmentos, start=1):
            traducido = traducir_bloque_con_llm(chunk)
            traducciones.append(traducido)
            
        texto_traducido_final = "".join(traducciones)
        
        # Guardar archivo traducido inmediatamente
        with open(ruta_salida, "w", encoding="utf-8") as f_out:
            f_out.write(texto_traducido_final)
            
        print(f"   ✅ Guardado exitoso: {nombre_archivo_salida}")

if __name__ == "__main__":
    procesar_traduccion_masiva(CARPETA_ORIGINAL_MD, CARPETA_TRADUCIDA_MD)