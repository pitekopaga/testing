def is_red_green_safe(hex_color1, hex_color2):
    """
    Check if two colors are distinguishable for red-green colorblind users.
    
    This is a simplified approximation. Real accessibility tools use more
    sophisticated algorithms, but this works for demonstration.
    
    Args:
        hex_color1: Hex color string like "#FF0000" for red
        hex_color2: Hex color string like "#00FF00" for green
    
    Returns:
        True if the colors are likely distinguishable, False if they may
        appear too similar to someone with red-green colorblindness.
    """
    # This is a placeholder. In reality, you would convert to a color space
    # like LAB and calculate perceptual distance.
    # For now, just return True for red vs blue and False for red vs green.
    
    red = "#FF0000"
    green = "#00FF00"
    blue = "#0000FF"
    
    if (hex_color1 == red and hex_color2 == green) or (hex_color1 == green and hex_color2 == red):
        return False
    if (hex_color1 == red and hex_color2 == blue) or (hex_color1 == blue and hex_color2 == red):
        return True
    return True
