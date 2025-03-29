import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.ticker import FuncFormatter
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


def custom_formatter(x, pos):
    return f"{x * 1e-8:.1f}e7"

# Load the Excel file
df1 = pd.read_excel('Case1_001.xlsx')
df2 = pd.read_excel('Case1_002.xlsx')
df3 = pd.read_excel('Case1_003.xlsx')
df4 = pd.read_excel('Case1_004.xlsx')
df5 = pd.read_excel('Case1_005.xlsx')
# df1 = pd.read_excel('Case2_001.xlsx')
# df2 = pd.read_excel('Case2_002.xlsx')
# df3 = pd.read_excel('Case2_003.xlsx')
# df4 = pd.read_excel('Case2_004.xlsx')
# df5 = pd.read_excel('Case2_005.xlsx')
# df1 = pd.read_excel('Case3_001.xlsx')
# df2 = pd.read_excel('Case3_002.xlsx')
# df3 = pd.read_excel('Case3_003.xlsx')
# df4 = pd.read_excel('Case3_004.xlsx')
# df5 = pd.read_excel('Case3_005.xlsx')

sm = 4  # subaxis start month

# Use the first column as x-axis values and the rest as y-axis values
x = df1.iloc[:, 0]
y1 = df1.iloc[:, 1:]
y2 = df2.iloc[:, 1:]
y3 = df3.iloc[:, 1:]
y4 = df4.iloc[:, 1:]
y5 = df5.iloc[:, 1:]

Special_Mineral = "Calcite"  # case 1
# Special_Mineral = "Hematite"  # case 2
# Special_Mineral = "Goethite"  # case 3

# Create the main figure and axis
fig, ax = plt.subplots(figsize=(10, 6.5))

ax.semilogy(x, y1['H2(aq)'], color='orange')
ax.semilogy(x, y5['H2(aq)'], color='orange')
ax.fill_between(x, y1['H2(aq)'], y5['H2(aq)'], color='orange', alpha=0.3, label="H2(aq)")
ax.semilogy(x, y1['H2(g)'], color='blue')
ax.semilogy(x, y5['H2(g)'], color='blue')
ax.fill_between(x, y1['H2(g)'], y5['H2(g)'], color='blue', alpha=0.3, label="H2(g)")
ax.set_xlabel(df1.columns[0], fontsize=21)
ax.set_ylabel('Amount [mol]', fontsize=21)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.legend(loc=(0.7, 0.5), fontsize=20)
ax.grid(True)

ax_inset = inset_axes(ax, width='40%', height='40%', loc=3, bbox_to_anchor=(0.62, 0.05, 0.9, 0.9),
                      bbox_transform=ax.transAxes)
ax_inset.plot(x[sm:], y3['H2(aq)'][sm:], color='orange')
ax_inset.fill_between(x[sm:], y1['H2(aq)'][sm:], y5['H2(aq)'][sm:], color='orange', alpha=0.3, label="H2(aq)")
ax_inset.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
ax_inset.tick_params(axis='x', labelsize=15)
ax_inset.tick_params(axis='y', labelsize=15)
ax_inset.patch.set_edgecolor('black')

ax_inset2 = inset_axes(ax, width='40%', height='40%', loc=3, bbox_to_anchor=(0.18, 0.05, 0.9, 0.9),
                       bbox_transform=ax.transAxes)
ax_inset2.plot(x[sm:], y3['H2(g)'][sm:], color='blue')
ax_inset2.fill_between(x[sm:], y1['H2(g)'][sm:], y5['H2(g)'][sm:], color='blue', alpha=0.3, label="H2(g)")
ax_inset2.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
ax_inset2.tick_params(axis='x', labelsize=15)
ax_inset2.tick_params(axis='y', labelsize=15)
ax_inset2.patch.set_edgecolor('black')

ax.text(-0.15, 1.05, 'a)', transform=ax.transAxes, fontsize=25, fontweight='bold', va='top')
plt.savefig('./h2.png', dpi=300)
plt.show()

# Plot lost amount of each mineral
minerals = [Special_Mineral, "Pyrite", "Pyrrhotite"]
labels_char = ['b)', 'c)', 'd)']
dataframes = [y1, y2, y3, y4, y5]
i = 0

for mineral in minerals:
    fig, ax2 = plt.subplots(figsize=(10, 6.5))

    # Calculate the amount lost for each dataframe
    lost_amounts = [df[mineral] - df[mineral].iloc[0] for df in dataframes]

    # Plot the central dataframe (y3) in solid line
    ax2.plot(x[1:], lost_amounts[2][1:], label=f'{mineral} (3wt% Iron)', color='blue')

    # Fill between the minimum and maximum lost amounts
    min_loss = pd.concat(lost_amounts, axis=1).min(axis=1)
    max_loss = pd.concat(lost_amounts, axis=1).max(axis=1)

    ax2.fill_between(x[1:], min_loss[1:], max_loss[1:], color='blue', alpha=0.3, label=f'{mineral} (Range)')

    ax2.set_xlabel(df1.columns[0], fontsize=21)
    ax2.set_ylabel('Amount Change [mol]', fontsize=21)
    ax2.tick_params(axis='x', labelsize=20)
    ax2.tick_params(axis='y', labelsize=20)
    ax2.legend(fontsize=20)
    ax2.grid(True)
    ax2.text(-0.15, 1.05, labels_char[i], transform=ax2.transAxes, fontsize=25, fontweight='bold', va='top')
    plt.savefig(f'./{mineral}_change_amount.png', dpi=300)
    plt.show()

    i = i+1
