def hello_rish():
    print("Hi there Rish!")
    
def calculate_pi(precision=5):
    """
    Calculate the value of pi to the specified decimal precision using the Nilakantha series.
    
    Args:
        precision: Number of decimal digits to calculate (default is 5)
        
    Returns:
        float: The value of pi calculated to the specified precision
    """
    # Start with the base value of pi according to the Nilakantha series
    pi = 3.0
    
    # The Nilakantha series converges relatively quickly
    # We'll use enough iterations to ensure at least 5 digits of precision
    sign = 1
    denominator = 2
    
    # Calculate number of iterations needed based on precision
    # More iterations for higher precision
    iterations = 1000 * precision
    
    for i in range(iterations):
        # Apply the Nilakantha series formula:
        # π = 3 + 4/(2*3*4) - 4/(4*5*6) + 4/(6*7*8) - ...
        term = 4.0 / (denominator * (denominator + 1) * (denominator + 2))
        pi += sign * term
        
        # Flip the sign for the next term
        sign *= -1
        
        # Move to the next term's denominator
        denominator += 2
    
    # Round to the specified precision
    return round(pi, precision)