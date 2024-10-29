import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.ticker import ScalarFormatter


# Define your custom formatter function
def custom_formatter(x, pos):
    return f"{x * 1e-8:.1f}e7"


# Load the Excel file
df1 = pd.read_excel('Case3_Res.xlsx')

# Use the first column as x-axis values and the rest as y-axis values
y1 = df1.iloc[:, 1:]

plt.figure(figsize=(10, 5))
plt.plot(y1['Mon'], y1['Dpyr']*1e7, label="Pyrite")
plt.plot(y1['Mon'], y1['Dpyrr']*1e7, label="Pyrrhotite")
#plt.plot(y1['Mon'], y1['Dhem']*1e7, label="Hematite")
plt.plot(y1['Mon'], y1['Dgoe']*1e7, label="Goethite")
plt.xlabel('Storage Time [month]', fontsize=16)
plt.ylabel('Amount Change [mol]', fontsize=16)
plt.gca().tick_params(axis='x', labelsize=15)
plt.gca().tick_params(axis='y', labelsize=15)
plt.legend(fontsize=16, loc='upper left', bbox_to_anchor=(0.0, 0.5, 0.5, 0.5))
plt.grid(True)
plt.savefig('./Case3_Min1.png', dpi=300)
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(y1['Mon'], y1['Dcal'] * 1e7, label="Calcite")
plt.xlabel('Storage Time [month]', fontsize=16)
plt.ylabel('Amount Change [mol]', fontsize=16)
# Get current axis
ax = plt.gca()

# Force scientific notation on y-axis
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.get_offset_text().set_fontsize(15)  # Adjust font size for the exponent
ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))  # Force scientific notation regardless of data scale

# Set tick parameters
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
plt.legend(fontsize=16, loc='best', bbox_to_anchor=(0.5, 0., 0.5, 0.5))
plt.grid(True)
plt.savefig('./Case3_Min2.png', dpi=300)
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(y1['Mon'], y1['PH2']*100, label="H$_2$(g) Loss")
plt.xlabel('Storage Time [month]', fontsize=16)
plt.ylabel('Percentage H$_2$(g) Loss [%]', fontsize=16)
plt.gca().tick_params(axis='x', labelsize=15)
plt.gca().tick_params(axis='y', labelsize=15)
plt.legend(fontsize=16, loc='best', bbox_to_anchor=(0.5, 0., 0.5, 0.5))
plt.grid(True)
plt.savefig('./Case3_H2.png', dpi=300)
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(y1['Mon'], y1['MHS-'], label="HS$^-$ Molality")
plt.xlabel('Storage Time [month]', fontsize=16)
plt.ylabel('Molality [mole/L]', fontsize=16)
plt.gca().tick_params(axis='x', labelsize=15)
plt.gca().tick_params(axis='y', labelsize=15)
plt.legend(fontsize=16, loc='best', bbox_to_anchor=(0.5, 0., 0.5, 0.5))
plt.grid(True)
plt.savefig('./Case3_HS.png', dpi=300)
plt.show()