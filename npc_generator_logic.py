import random

class NPCGenerator:
    def __init__(self, rules: dict) -> None:
        self.rules = rules
        self.unprocessed_queue = []
        self.generated_npcs = []

    def reset_queue(self):
        self.unprocessed_queue = [['NPC']] # Símbolo inicial de la gramática

    def __expand_grammar(self, initial_symbols: list) -> str:
        current_symbols_to_process = list(initial_symbols)
        generated_parts = []

        while current_symbols_to_process:
            symbol = current_symbols_to_process.pop(0)
            
            expansion_rules = self.rules.get(symbol) # Obtener las reglas de expansión para el símbolo actual por ejemplo: "NPC" -> [["Un guerrero valiente", "Un mago sabio"], ["Una princesa noble"]]

            if expansion_rules:
                # Es un no-terminal, elegir una expansión aleatoria 
                chosen_expansion = random.choice(expansion_rules) # Por ejemplo: [["Un guerrero valiente", "Un mago sabio"], ["Una princesa noble"]]
                current_symbols_to_process = (chosen_expansion if isinstance(chosen_expansion, list) else [chosen_expansion]) + current_symbols_to_process # Añadir la expansión elegida al inicio de la cola de símbolos a procesar ejemplo: ["Un guerrero valiente", "Un mago sabio", "Una princesa noble", "Otro símbolo a procesar"]
            else:
                # Es un terminal (o un símbolo no definido en las reglas)
                if symbol == "#EMPTY#":
                    pass  # No añadir nada si es el símbolo especial de vacío
                elif symbol == "PUNTO":
                    generated_parts.append(".")
                elif symbol == "COMA":
                    generated_parts.append(",")
                else:
                    generated_parts.append(symbol)
        
        # --- Construcción y Limpieza de la Cadena ---
        # 1. Unir todas las partes con un espacio.
        raw_text = " ".join(filter(None, generated_parts)) # filter(None, ...) para eliminar strings vacíos si los hubiera

        # 2. Limpieza específica de puntuación y espacios múltiples.
        #    Quitar espacios antes de comas y puntos.
        text_cleaned = raw_text.replace(" .", ".").replace(" ,", ",")
        
        # 3. Normalizar espacios múltiples a uno solo.
        text_cleaned = ' '.join(text_cleaned.split())

        # 4. Asegurar que la primera letra sea mayúscula.
        if text_cleaned:
            text_cleaned = text_cleaned[0].upper() + text_cleaned[1:]
            
        return text_cleaned.strip()

    def generate_npc_description(self) -> str:
        self.reset_queue()
        if not self.unprocessed_queue:
            return "Error: La cola de procesamiento está vacía después de reset."
        
        initial_symbols_to_expand = self.unprocessed_queue.pop(0) # Símbolo inicial de la gramática
        description = self.__expand_grammar(initial_symbols_to_expand)
        
        self.generated_npcs.append(description)
        return description