import os

CircleBin = "CircleBin.txt"

def get_CircleBin():
    """Reads a variable stored in a .txt file

    Returns:
        The variable in the .txt file
    """
    # Checks if the txt file exists
    if os.path.exists(CircleBin):

        # Opens the txt file in read-only mode
        with open(CircleBin, "r") as file:
            
            # Turns the variable into an int
            Circle = int(file.read())

    # If there is no variable in the file, return the variable as 0
    else:
        Circle = 0
    return Circle

# Function to update and save the the variable to the file
def update_Circle(amount):
    # uses the get circlebin function to update it with "amount", amount could be -ve or +ve
    Circle = get_CircleBin() + amount

    # opens the texts file and writes in the new variable value, that is what "w" means "write"
    with open(CircleBin, "w") as file:
        # writes it as a string version of the variable
        file.write(str(Circle))

# Using the function like this will make the variable permantantly 1
Circle = get_CircleBin()

# using the update function like this will make the circle value always 0
update_Circle(-Circle)

update_Circle(1)
Circle = get_CircleBin()
  
print(Circle)