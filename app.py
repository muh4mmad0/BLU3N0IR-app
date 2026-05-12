"""
BLU3N0IR - Cyberpunk Calculator with DBMS Integration
Flask Backend + SQLite Database
"""

from flask import Flask, request, jsonify, render_template, send_file
from database import init_db, save_calculation, get_history, delete_record, delete_all, search_history, export_csv
import math, operator, re, io

app = Flask(__name__)

# ─── Safe Expression Evaluator ───────────────────────────────────────────────

SAFE_FUNCS = {
    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
    'sqrt': math.sqrt, 'log': math.log, 'log10': math.log10,
    'log2': math.log2, 'exp': math.exp, 'abs': abs,
    'ceil': math.ceil, 'floor': math.floor, 'factorial': math.factorial,
    'pi': math.pi, 'e': math.e, 'pow': math.pow,
    'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
    'degrees': math.degrees, 'radians': math.radians,
}

def safe_eval(expression: str):
    """Safely evaluate a mathematical expression."""
    # Clean the expression
    expr = expression.strip()
    expr = expr.replace('^', '**')
    expr = expr.replace('×', '*')
    expr = expr.replace('÷', '/')
    expr = expr.replace('π', str(math.pi))
    expr = expr.replace('√', 'sqrt')

    # Validate characters
    allowed = re.compile(r'^[\d\s\+\-\*\/\(\)\.\,\%\*\^a-zA-Z_]+$')
    if not allowed.match(expr):
        raise ValueError("Invalid characters in expression")

    # Block any dangerous builtins
    if any(word in expr for word in ['import', 'exec', 'eval', 'open', '__']):
        raise ValueError("Expression not allowed")

    result = eval(expr, {"__builtins__": {}}, SAFE_FUNCS)
    return result

# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data.get('expression', '').strip()
    if not expression:
        return jsonify({'error': 'Empty expression'}), 400
    try:
        result = safe_eval(expression)
        # Handle integer results cleanly
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        result_str = str(result)
        save_calculation(expression, result_str)
        return jsonify({'result': result_str, 'expression': expression})
    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Calculation error: {str(e)}'}), 400

@app.route('/api/history', methods=['GET'])
def history():
    limit = request.args.get('limit', 50, type=int)
    records = get_history(limit)
    return jsonify({'history': records})

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    records = search_history(query)
    return jsonify({'history': records})

@app.route('/api/delete/<int:record_id>', methods=['DELETE'])
def delete(record_id):
    delete_record(record_id)
    return jsonify({'success': True})

@app.route('/api/delete-all', methods=['DELETE'])
def clear_all():
    delete_all()
    return jsonify({'success': True})

@app.route('/api/export/csv', methods=['GET'])
def export_csv_route():
    csv_data = export_csv()
    return send_file(
        io.BytesIO(csv_data.encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='BLU3N0IR_history.csv'
    )

@app.route('/api/export/txt', methods=['GET'])
def export_txt_route():
    records = get_history(10000)
    lines = ["BLU3N0IR — Calculation History", "=" * 50, ""]
    for r in records:
        lines.append(f"[{r['timestamp']}]")
        lines.append(f"  Expression : {r['expression']}")
        lines.append(f"  Result     : {r['result']}")
        lines.append("")
    txt = "\n".join(lines)
    return send_file(
        io.BytesIO(txt.encode()),
        mimetype='text/plain',
        as_attachment=True,
        download_name='BLU3N0IR_history.txt'
    )

if __name__ == '__main__':
    init_db()
    print("\n  ██████╗ ██╗     ██╗   ██╗██████╗ ███╗   ██╗ ██████╗ ██╗██████╗ ")
    print("  ██╔══██╗██║     ██║   ██║╚════██╗████╗  ██║██╔═══██╗██║██╔══██╗")
    print("  ██████╔╝██║     ██║   ██║ █████╔╝██╔██╗ ██║██║   ██║██║██████╔╝")
    print("  ██╔══██╗██║     ██║   ██║ ╚═══██╗██║╚██╗██║██║   ██║██║██╔══██╗")
    print("  ██████╔╝███████╗╚██████╔╝██████╔╝██║ ╚████║╚██████╔╝██║██║  ██║")
    print("  ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═╝\n")
    print("  [SYSTEM] BLU3N0IR Calculator — DBMS Project")
    print("  [INFO]   Running at http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)
