import sys
import os

def parse_grammar(file_path: str) -> dict:
    """
    Lee un archivo de gramática y lo convierte en un diccionario de reglas.
    """
    grammar = {}
    
    # Si estamos dentro de un ejecutable empaquetado, usa la ruta correcta
    if getattr(sys, 'frozen', False):
        # sys._MEIPASS es el directorio temporal donde PyInstaller extrae los archivos
        file_path = os.path.join(sys._MEIPASS, file_path)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Filtra las líneas vacías o comentarios
                if not line.strip() or line.strip().startswith('#'):
                    continue

                if "->" in line:
                    try:
                        key, values_str = line.strip().split("->", 1) # Divide la línea en clave y valores 
                        key = key.strip() # Limpia la clave de espacios

                        # Divide las expansiones posibles por |
                        possible_expansions = values_str.split("|")
                        
                        processed_expansions = []
                        for expansion_str in possible_expansions:
                            expansion_str = expansion_str.strip()
                            if not expansion_str: # Maneja producciones verdaderamente vacías como "RULE -> | something" o "RULE -> #EMPTY# | "
                                processed_expansions.append([]) # Representa una producción vacía
                            else:
                                processed_expansions.append(expansion_str.split())  # Divide la expansión en símbolos individuales

                        # Agrega las expansiones de las reglas a la gramática
                        grammar.setdefault(key, []).extend(processed_expansions)
                    except ValueError:
                        print(f"Error en la línea de gramática: {line.strip()}")
                        continue
        return grammar

    except FileNotFoundError:
        print(f"El archivo de gramática no se encontró: {file_path}")
        return {}
    except Exception as e:
        print(f"Error al procesar el archivo de gramática: {e}")
        return {}