from flask import Flask, render_template, request, jsonify
from lark import Lark, Transformer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Esto permite todas las solicitudes CORS desde cualquier origen

# Variable global para guardar el resultado de la última operación
last_result = None

# Definir la gramática y crear el parser
grammar = """
    ?start: expr
    ?expr: term
         | expr "+" term   -> add
         | expr "-" term   -> sub
    ?term: factor
         | term "*" factor -> mul
         | term "/" factor -> div
         | factor "(" expr ")" -> paren_expr
    ?factor: DECIMAL       -> number
           | "(" expr ")"
    DECIMAL: /-?\d+(\.\d+)?/
    %import common.WS
    %ignore WS
"""
parser = Lark(grammar, parser='lalr')

# Transformer para construir el árbol
class TreeBuilder(Transformer):
    def number(self, n):
        return {"type": "number", "value": float(n[0].value)}  # Convierte a float para operaciones

    def add(self, args):
        return {"type": "add", "left": args[0], "right": args[1]}
    
    def sub(self, args):
        return {"type": "sub", "left": args[0], "right": args[1]}

    def mul(self, args):
        return {"type": "mul", "left": args[0], "right": args[1]}

    def div(self, args):
        return {"type": "div", "left": args[0], "right": args[1]}

    def paren_expr(self, args):
        return args[0]  # Devuelve la expresión dentro de los paréntesis directamente

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tree', methods=['POST'])
def tree():
    global last_result
    data = request.get_json()
    expression = data.get('expression')

    # Reemplazar el marcador de resultado si se usa el último resultado
    if expression == "last_result":
        expression = str(last_result) if last_result is not None else "0"

    if not expression:
        return jsonify({'treeHTML': '', 'result': ''})

    try:
        # Parsear la expresión para construir el árbol
        tree = parser.parse(expression)
        transformed_tree = TreeBuilder().transform(tree)
        tree_html = render_tree(transformed_tree)
        result = evaluate_tree(transformed_tree)

        # Guardar el resultado para uso posterior
        last_result = result
    except Exception as e:
        return jsonify({'treeHTML': f'<p>Error: {str(e)}</p>', 'result': ''})

    return jsonify({'treeHTML': tree_html, 'result': result})

def render_tree(node):
    """Renderiza el árbol como HTML de manera recursiva."""
    if node['type'] == 'number':
        return f'<div class="node">{node["value"]}</div>'
    left = render_tree(node['left'])
    right = render_tree(node['right'])
    operator = "+" if node['type'] == 'add' else "-" if node['type'] == 'sub' else "*" if node['type'] == 'mul' else "/" 
    return f'''
        <div class="node operator">
            {operator}
        </div>

        <div class="operator">
            <div class="left">{left}</div>
            <div class="right">{right}</div>
        </div>
    '''

def evaluate_tree(node):
    """Evalúa el árbol y retorna el resultado."""
    if node['type'] == 'number':
        return node['value']
    left = evaluate_tree(node['left'])
    right = evaluate_tree(node['right'])
    if node['type'] == 'add':
        return left + right
    elif node['type'] == 'sub':
        return left - right
    elif node['type'] == 'mul':
        return left * right
    elif node['type'] == 'div':
        return left / right

if __name__ == '__main__':
    app.run(debug=True)
