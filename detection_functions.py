import os

CircleBin = "binary.txt"

# Function to update and save the the variable to the file
def update_Circle(bin_value):
    # uses the get circlebin function to update it with "amount", amount could be -ve or +ve
    if bin_value > 1:
        raise ValueError
    else:

        # Opens the texts file and writes in the new variable value
        with open(CircleBin, "w") as file:
            # Writes it as a string version of the variable
            file.write(str(bin_value))