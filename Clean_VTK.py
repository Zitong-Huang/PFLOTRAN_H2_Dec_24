import numpy as np

time_txt = '4M'

file_path = './H2_Inj/' + time_txt + '.vtk'
#file_path = './NH3_Inj/' + time_txt + '.vtk'
# Define a function to replace numbers below 1e-38 with 1e-38 in a line of text
def replace_numbers_in_line(line):
    # Split the line into words
    words = line.split()
    # Replace numbers below 1e-38 with 1e-38
    modified_words = []
    for word in words:
        try:
            number = float(word)
            if number != 0 and number < 1e-38:
                modified_words.append('1e-38')
            else:
                modified_words.append(word)
        except ValueError:
            # If the word is not a number, just append it to the modified words
            modified_words.append(word)
    # Join the modified words to create the modified line
    modified_line = ' '.join(modified_words)
    return modified_line

# Define the buffer size (number of characters to read at a time)
buffer_size = 1024 * 1024  # 1 MB
# Define the modified file path
modified_file_path = './H2_Inj/' + time_txt + '_mod.vtk'
#modified_file_path = './NH3_Inj/' + time_txt + '_mod.vtk'

# Open the input and output files
with open(file_path, 'r') as infile, open(modified_file_path, 'w') as outfile:
    # Read and write the file line by line
    for line in infile:
        # Replace numbers below 1e-38 with 1e-38 in the line
        modified_line = replace_numbers_in_line(line)
        # Write the modified line to the output file
        outfile.write(modified_line + '\n')

modified_file_path