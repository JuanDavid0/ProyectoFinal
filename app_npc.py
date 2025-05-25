from flask import Flask, request, jsonify, render_template
from npc_generator_logic import NPCGenerator 
from parse_grammar import parse_grammar # Asumiendo que está en la misma carpeta
import os
import sys

app = Flask(__name__)

# Actualizar al nuevo nombre del archivo de gramática
GRAMMAR_FILE = "npc_grammar.gr" 
# GRAMMAR_FILE = "npc_grammar_avanzada.gr" # o el nombre que hayas decidido finalmente

# --- Comprobación de la ruta del archivo de gramática ---
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
grammar_full_path = os.path.join(base_path, GRAMMAR_FILE)

if not os.path.exists(grammar_full_path):
    print(f"ERROR CRÍTICO: El archivo de gramática '{GRAMMAR_FILE}' no se encontró en la ruta: {grammar_full_path}")
    # sys.exit(f"Saliendo debido a la falta del archivo de gramática: {GRAMMAR_FILE}") # Puedes salir si es crítico
    grammar_rules = {} # Iniciar con reglas vacías para evitar error al instanciar NPCGenerator
else:
    print(f"Cargando gramática desde: {grammar_full_path}")
    grammar_rules = parse_grammar(grammar_full_path)

if not grammar_rules:
    print(f"ADVERTENCIA: No se pudieron cargar reglas de la gramática desde '{GRAMMAR_FILE}'. El generador puede no funcionar como se espera.")

npc_generator = NPCGenerator(grammar_rules)
current_npc_description = None

@app.route("/")
def home():
    return render_template("npc_index.html") # Asumiendo que no cambiaste el nombre del HTML

@app.route("/generate_npc", methods=["POST"])
def generate_npc_route():
    global current_npc_description
    if not npc_generator.rules:
        return jsonify({"success": False, "error": "Error: Las reglas de gramática no están cargadas en el generador."})
    try:
        current_npc_description = npc_generator.generate_npc_description()
        return jsonify({"success": True, "description": current_npc_description})
    except Exception as e:
        app.logger.error(f"Error generando descripción de NPC: {str(e)}", exc_info=True)
        return jsonify({"success": False, "error": f"Error generando descripción de NPC: {str(e)}"})

if __name__ == "__main__":
    if not grammar_rules and os.path.exists(grammar_full_path): # Si el archivo existe pero no se cargaron reglas
        print("El archivo de gramática existe pero no se cargaron reglas. Revise el formato del archivo o errores de parseo.")
        # sys.exit("Saliendo debido a error en la carga de gramática.")
    
    app.run(debug=True)