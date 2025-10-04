"""
This module contains the core calculation logic for the Flask backend.
"""

def perform_calculation(num1_str, num2_str, operator):
    """
    Performs a single arithmetic calculation based on two numbers and an operator.

    Args:
        num1_str (str): The first operand as a string.
        num2_str (str): The second operand as a string.
        operator (str): The arithmetic operator (+, -, *, /).

    Returns:
        float or str: The result of the calculation or an error message.
    """
    try:
        # Attempt to convert input strings to floats
        num1 = float(num1_str)
        num2 = float(num2_str)
    except ValueError:
        # Handle cases where input strings are not valid numbers
        return "Error: Invalid number input"

    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        if num2 == 0:
            return "Error: Division by zero"
        return num1 / num2
    else:
        return "Error: Invalid operator"
