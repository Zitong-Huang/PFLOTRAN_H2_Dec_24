import numpy as np
import pandas as pd

h2aq = np.zeros([13, 1])

for i in range(13):
    if i < 10:
        time_txt = '0' + str(i)
    else:
        time_txt = str(i)
    file_path = './H2_Inj/pflotran_h2-0' + time_txt + '.vtk'

    # Initialize an empty list to store the numbers
    numbers_list_h2 = []
    numbers_list_sat = []

    # Define a flag to identify when to start reading numbers
    start_reading_h2 = False
    start_reading_sat = False

    # Open the file and read line by line
    with open(file_path, 'r') as file:
        for line in file:
            # Check if the line contains the title indicating the start of numbers
            if 'SCALARS Total_H2(aq)' in line:
                start_reading_h2 = True
                # Skip the next line which is 'LOOKUP_TABLE default'
                next(file)
            elif start_reading_h2:
                # If the line is empty or a new section starts, stop reading
                if line.strip() == '' or 'SCALARS' in line or 'POINT_DATA' in line:
                    start_reading_h2 = False
                else:
                    # Split the line into individual numbers and extend the list
                    numbers_list_h2.extend([float(num) for num in line.split()])

            if 'SCALARS Liquid_Saturation' in line:
                start_reading_sat = True
                # Skip the next line which is 'LOOKUP_TABLE default'
                next(file)
            elif start_reading_sat:
                # If the line is empty or a new section starts, stop reading
                if line.strip() == '' or 'SCALARS' in line or 'POINT_DATA' in line:
                    start_reading_sat = False
                else:
                    # Split the line into individual numbers and extend the list
                    numbers_list_sat.extend([float(num) for num in line.split()])

    # Convert the list to a numpy array
    numbers_array_h2_all = np.array(numbers_list_h2)
    numbers_array_h2 = numbers_array_h2_all[numbers_array_h2_all <= 1.0]

    numbers_array_sat_all = np.array(numbers_list_sat)
    numbers_array_sat = numbers_array_sat_all[numbers_array_h2_all <= 1.0]

    # Determine the number of blocks that H2 has spreaded to
    plume_spread = numbers_array_h2_all[numbers_array_h2_all >= 1e-2]
    num_plume_blocks = np.shape(plume_spread)[-1]
    print(num_plume_blocks)

    cell_vol_gr = 16*16*20*0.2*1000

    # Display the first few numbers to verify
    cell_h2 = cell_vol_gr*numbers_array_sat*numbers_array_h2
    total_h2 = np.sum(cell_h2)

    print("Total H2(aq) in gr is " + str(total_h2) + "moles")

    h2aq[i, 0] = total_h2

# print(h2aq)
# df = pd.DataFrame(data=h2aq)
# df.to_excel("H2AQ.xlsx", index=False)
