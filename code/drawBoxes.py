import os

def drawBox(left, right, top, bottom):
    """Draw a 255x255 canvas and an inner box.

    Args:
        left (int): left face boundry 
        right (_type_): right face boundry 
        top (_type_): top face boundry 
        bottom (int): bottom face boundry 
    """
    for y in range(255):
        row = []
        for x in range(255):
            if (x == left or x == right) and (y >= top and y <= bottom):
                row.append("#")
            elif (y == top or y == bottom) and (x >= left and x <= right):
                row.append("#")
            else:
                row.append(".")
        print(''.join(row))

def clearScreen():
    """Clear the screen before drawing another frame.
    """
    os.system('cls' if os.name == 'nt' else 'clear')