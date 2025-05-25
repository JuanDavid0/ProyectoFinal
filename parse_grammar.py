import sys
import os

def is_terminal(symbols):
    """
    Determina si un conjunto de símbolos es terminal o no.
    Los símbolos terminales no comienzan con mayúscula.
    """
    return not any(symbol[0].isupper() for symbol in symbols.split())

def parse_grammar(file_path: str) -> dict:
    """
    Lee un archivo de gramática y lo convierte en un diccionario de reglas.
    """
    grammar = {}
    
    # Si estamos dentro de un ejecutable empaquetado, usa la ruta correcta
    if getattr(sys, 'frozen', False):
        # noinspection PyProtectedMember
        file_path = os.path.join(sys._MEIPASS, file_path)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Filtra las líneas vacías o comentarios
                if not line.strip() or line.strip().startswith('#'):
                    continue

                if "->" in line:
                    try:
                        key, values_str = line.strip().split("->", 1) # Split only on the first "->"
                        key = key.strip()

                        # Divide las expansiones posibles por |
                        possible_expansions = values_str.split("|")
                        
                        processed_expansions = []
                        for expansion_str in possible_expansions:
                            expansion_str = expansion_str.strip()
                            if not expansion_str: # Handles truly empty productions like "RULE -> | something" or "RULE -> #EMPTY# | "
                                processed_expansions.append([]) # Represents an empty production
                            else:
                                processed_expansions.append(expansion_str.split())

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