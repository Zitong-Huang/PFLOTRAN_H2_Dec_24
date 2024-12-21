import matplotlib.pyplot as plt

# Data from the table
temperature = [0, 25, 60, 100, 150, 200]
dis = [-0.900773344, -0.996773344, -1.031173344, -0.988973344, -0.868373344, -0.701973344]
#case_1 = [-0.901208947, -0.998425241, -1.038815791, -1.019564708, -0.983569695, -1.003503627]
case_1_dash = [-6.00071875, -5.63424375, -5.16175625, -4.685625, -4.18691875, -3.795175]
case_2 = [-6.341416667, -5.953516667, -5.45585, -4.955733333, -4.430483333, -4.011966667]
case_2_dash = [-6.236586538, -5.855278846, -5.365359615, -4.872623077, -4.355540385, -3.945261538]
case_3 = [-6.64455, -6.27365, -5.82845, -5.415333333, -5.023016667, -4.752866667]
case_3_dash = [-6.341570588, -5.972752941, -5.514711765, -5.071941176, -4.629558824, -4.302188235]

temp_dot = [25, 37.5, 50, 62.5, 75]
case_1_dot = [-1.068542129, -1.086716098, -1.09420412, -1.091514981, -1.080921908]
case_2_dot = [-1.07007044, -1.090443971, -1.101274818, -1.104025268, -1.105130343]
case_3_dot = [-1.073143291, -1.095825632, -1.110138279, -1.116338565, -1.12090412]

plt.figure(figsize=(8, 5))

# Plot solid lines with different markers for each case
plt.plot(temperature, dis, label='Dissolution', color='black', marker='s', markersize=5)
plt.plot(temperature, case_2, label='PPH Equilibrium', color='orange', marker='o', markersize=5)  # Triangle markers
plt.plot(temperature, case_3, label='PPG Equilibrium', color='green', marker='^', markersize=5)  # Diamond markers

# Plot dashed lines with the same markers for each corresponding case
plt.plot(temperature, case_1_dash, linestyle='--', color='blue', marker='d', label='PPM Equilibrium', markersize=5)
plt.plot(temperature, case_2_dash, linestyle='--', color='orange', marker='o',label='PPMH Equilibrium', markersize=5)
plt.plot(temperature, case_3_dash, linestyle='--', color='green', marker='^', label='PPMG Equilibrium', markersize=5)

# Plot experimental data points as individual markers with no connecting lines
plt.plot(temp_dot, case_1_dot, linestyle='--', color='blue', marker='d', markersize=7, markerfacecolor='none', label='Case 1 (1 year)')
plt.plot(temp_dot, case_2_dot, linestyle='--', color='orange', marker='o', markersize=7, markerfacecolor='none', label='Case 2 (1 year)')
plt.plot(temp_dot, case_3_dot, linestyle='--', color='green', marker='^', markersize=7, markerfacecolor='none', label='Case 3 (1 year)')


# Labels and legend
plt.xlabel(r'$\mathbf{Temperature\ [°C]}$', fontsize=16)
plt.ylabel(r'$\mathbf{log_{10}(\mathrm{{H}_{2} molality })}$', fontsize=16)
plt.legend(loc='center left', bbox_to_anchor=(-0.01, 0.58), fontsize=11)
plt.xticks(fontsize=12)  # Increased tick label font size
plt.yticks(fontsize=12)  # Increased tick label font size
# Save and show the plot
plt.savefig('./h2_molal_equili.png', dpi=300)
plt.show()