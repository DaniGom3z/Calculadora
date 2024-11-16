from flask import Flask, render_template, request, jsonify
from lark import Lark, Transformer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Esto permite todas las solicitudes CORS desde cualquier origen

# Definir la gramática y crear el parser
grammar = """
    ?start: expr
    ?expr: term
         | expr "+" term   -> add
         | expr "-" term   -> sub
    ?term: factor
         | term "*" factor -> mul
         | term "/" factor -> div
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
        return {"type": "number", "value": n[0].value}

    def add(self, args):
        return {"type": "add", "left": args[0], "right": args[1]}
    
    def sub(self, args):
        return {"type": "sub", "left": args[0], "right": args[1]}

    def mul(self, args):
        return {"type": "mul", "left": args[0], "right": args[1]}

    def div(self, args):
        return {"type": "div", "left": args[0], "right": args[1]}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tree', methods=['POST'])
def tree():
    data = request.get_json()
    expression = data.get('expression')
    if not expression:
        return jsonify({'treeHTML': ''})

    try:
        # Parsear la expresión para construir el árbol
        tree = parser.parse(expression)
        transformed_tree = TreeBuilder().transform(tree)
        tree_html = render_tree(transformed_tree)
    except Exception as e:
        return jsonify({'treeHTML': f'<p>Error: {str(e)}</p>'})

    return jsonify({'treeHTML': tree_html})

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

if __name__ == '__main__':
    app.run(debug=True)
