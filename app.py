import sys
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify

# 1. Use pathlib to determine the base directory of the application (where app.py is located)
BASE_DIR = Path(__file__).resolve().parent

# 2. Dynamically add the 'Backend' directory to the Python path 
# This allows us to import the calculation module.
sys.path.append(str(BASE_DIR / 'Backend'))

# 3. Import the core calculation logic
try:
    from Backend.calculations import perform_calculation 
except ImportError:
    # If the file is run incorrectly, this provides a helpful error
    print("FATAL ERROR: Could not import calculations.py. Ensure it is in the 'Backend' directory.")
    sys.exit(1)


# 4. Initialize Flask
# We explicitly set the template folder path using the pathlib Path object converted to string.
app = Flask(__name__, 
            template_folder=str(BASE_DIR / 'Frontend'),
            static_folder=str(BASE_DIR / 'Frontend'))


@app.route('/')
def index():
    """
    Route to read the index.html content using pathlib and render it.
    This simulates the Flask template system without needing a separate render_template call.
    """
    # Use pathlib to construct the exact path to the index.html file
    html_path = BASE_DIR / 'Frontend' / 'index.html'
    
    if not html_path.exists():
        return "Error: index.html not found in the Frontend directory.", 500
    
    # Read the content using pathlib's convenient .read_text() method
    html_content = html_path.read_text(encoding='utf-8')
    return render_template_string(html_content)


@app.route('/calculate', methods=['POST'])
def handle_calculate():
    """
    API endpoint to receive calculation requests and use the backend logic.
    """
    data = request.json
    
    # Extract the required parameters from the JSON request
    num1 = data.get('num1')
    num2 = data.get('num2')
    operator = data.get('operator')

    if not all([num1, num2, operator]):
        return jsonify({"error": "Missing calculation parameters"}), 400

    # Delegate the heavy lifting to the imported backend logic
    result = perform_calculation(num1, num2, operator)
    
    # Check if the result is an error string
    if isinstance(result, str) and result.startswith("Error"):
        # Return a 400 Bad Request status code for calculation errors
        return jsonify({"error": result}), 400
    
    # Return the successful result
    return jsonify({"result": result})


if __name__ == '__main__':
    # Flask application entry point
    app.run(debug=True)
