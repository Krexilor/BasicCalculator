# Libraries
import sys
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify

# Required Paths
# 1. Pathlib to determine the base directory of the application
BASE_DIR = Path(__file__).resolve().parent

# 2. Dynamically add the 'Backend' directory to the Python path 
sys.path.append(str(BASE_DIR / 'Backend'))

# Importing core calculation logic
try:
    from Backend.calculations import perform_calculation 
except ImportError:
    print("FATAL ERROR: Could not import calculations.py. Ensure it is in the 'Backend' directory.")
    sys.exit(1)

# Main
app = Flask(__name__, 
            template_folder=str(BASE_DIR / 'Frontend'),
            static_folder=str(BASE_DIR / 'Frontend'))


@app.route('/')
def index():
    """
    Route to read the index.html content using pathlib and render it.
    This simulates the Flask template system without needing a separate render_template call.
    """
    html_path = BASE_DIR / 'Frontend' / 'index.html'
    
    if not html_path.exists():
        return "Error: index.html not found in the Frontend directory.", 500
    
    html_content = html_path.read_text(encoding='utf-8')
    return render_template_string(html_content)


@app.route('/calculate', methods=['POST'])
def handle_calculate():
    """
    API endpoint to receive calculation requests and use the backend logic.
    """
    data = request.json
    
    num1 = data.get('num1')
    num2 = data.get('num2')
    operator = data.get('operator')

    if not all([num1, num2, operator]):
        return jsonify({"error": "Missing calculation parameters"}), 400

    result = perform_calculation(num1, num2, operator)
    
    if isinstance(result, str) and result.startswith("Error"):
        return jsonify({"error": result}), 400
    
    return jsonify({"result": result})


if __name__ == '__main__':
    # Flask application entry point
    app.run(debug=True)
