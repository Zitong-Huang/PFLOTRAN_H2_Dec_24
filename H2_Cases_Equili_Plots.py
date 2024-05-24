import matplotlib.pyplot as plt

# Data from the table
temperature = [0, 25, 60, 100, 150, 200]
dis = [-0.900773344, -0.996773344, -1.031173344, -0.988973344, -0.868373344, -0.701973344]
case_1 = [-0.901208947, -0.998425241, -1.038815791, -1.019564708, -0.983569695, -1.003503627]
case_2 = [-6.341416667, -5.953516667, -5.45585, -4.955733333, -4.430483333, -4.011966667]
case_3 = [-6.64455, -6.27365, -5.82845, -5.415333333, -5.023016667, -4.752866667]

plt.figure(figsize=(8, 5))
plt.plot(temperature, dis, label='dissolution')
plt.plot(temperature, case_1, label='case 1')
plt.plot(temperature, case_2, label='case 2')
plt.plot(temperature, case_3, label='case 3')
plt.xlabel(r'$\mathbf{Temperature\ [°C]}$', fontsize=16)
plt.ylabel(r'$\mathbf{\log_{10}(\mathrm{{H}_{2} molality })}$', fontsize=16)
# plt.title('Temperature vs. Log10 Ratios')
plt.legend(loc='center left', fontsize=14)
plt.savefig('./h2_molal_equili.png', dpi=300)
plt.show()