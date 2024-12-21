import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the main directory and subdirectories
# main_dir = 'Sw'
# main_dir = 'Wt'
main_dir = 'Temperature'
subdirs = ['1Y_Data', '3Y_Data', '5Y_Data', '10Y_Data']
times = ['1Y', '3Y', '5Y', '10Y']

molecule_names = ['H2', 'H2SAQ']
x_axis_col = 'Fe(II)/Fe Total Mole Ratio'

# Define the columns to plot for each molecule type
columns_to_plot = {
    'H2': ['Hematite Per', 'Goethite Per'],
    'H2SAQ': ['Hem H2S(g)/H2(g) [ppm]', 'Goe H2S(g)/H2(g) [ppm]']
}

# Prepare data structure
data = {molecule: {col: {time: [] for time in times} for col in cols} for molecule, cols in columns_to_plot.items()}

# Custom colors for Hematite (reds) and Goethite (blues) with larger contrast
custom_palette = {
    '1Y Hematite Per': '#8b0000', '3Y Hematite Per': '#ff6347',
    '5Y Hematite Per': '#8b0000', '10Y Hematite Per': '#ff6347',
    '1Y Goethite Per': '#00008b', '3Y Goethite Per': '#87cefa',
    '5Y Goethite Per': '#00008b', '10Y Goethite Per': '#87cefa',
    '1Y Hem H2S(g)/H2(g) [ppm]': '#8b0000', '3Y Hem H2S(g)/H2(g) [ppm]': '#ff6347',
    '5Y Hem H2S(g)/H2(g) [ppm]': '#8b0000', '10Y Hem H2S(g)/H2(g) [ppm]': '#ff6347',
    '1Y Goe H2S(g)/H2(g) [ppm]': '#00008b', '3Y Goe H2S(g)/H2(g) [ppm]': '#87cefa',
    '5Y Goe H2S(g)/H2(g) [ppm]': '#00008b', '10Y Goe H2S(g)/H2(g) [ppm]': '#87cefa'
}

# Function to collect data from files
def collect_data():
    for subdir, time in zip(subdirs, times):
        path = os.path.join(main_dir, subdir)
        for molecule in molecule_names:
            # for i in [10, 20, 30, 40, 50]:
            for i in [25, 375, 50, 625, 75]:
            # for i in ['001', '002', '003', '004', '005']:
                # file_name = f"{molecule}_sw_{i}.xlsx"
                file_name = f"{molecule}_temp_{i}.xlsx"
                # file_name = f"{molecule}_wt_{i}.xlsx"

                file_path = os.path.join(path, file_name)
                try:
                    df = pd.read_excel(file_path)
                    if x_axis_col not in df.columns:
                        print(f"Column '{x_axis_col}' not found in {file_path}")
                        continue

                    for col in columns_to_plot[molecule]:
                        if col in df.columns:
                            data[molecule][col][time].append(df[[x_axis_col, col]])
                        else:
                            print(f"Column '{col}' not found in {file_path}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

collect_data()

# Function to create box-whisker plots
def create_combined_plots(selected_times, filename_suffix):
    # alpha
    a = 1
    for molecule, cols in columns_to_plot.items():
        plt.figure(figsize=(13, 7))
        all_x_vals = pd.concat(
            [df[x_axis_col] for time in selected_times for col in cols for df in data[molecule][col][time]]
        )
        unique_x_vals = sorted(all_x_vals.unique())

        plot_data = []

        for x_val in unique_x_vals:
            for time in selected_times:
                for col in cols:
                    for df in data[molecule][col][time]:
                        filtered_df = df[df[x_axis_col] == x_val]
                        if not filtered_df.empty:
                            for value in filtered_df[col].values:
                                plot_data.append({
                                    'Fe(II)/Fe Total Mole Ratio': x_val,
                                    'Value': value,
                                    'Time': time,
                                    'Type': 'Hematite' if 'Hematite' in col else 'Goethite',
                                    'TimeLabel': f'{time} {col}'
                                })

        df_plot = pd.DataFrame(plot_data)

        # Adjust the x-ticks for the unique x-values
        positions = []
        current_pos = 0
        for i in range(len(unique_x_vals)):
            positions.append(current_pos)
            current_pos += 4  # Leave space for two box positions

        # Create a new column for adjusted x positions
        def adjust_positions(row):
            base_pos = positions[unique_x_vals.index(row['Fe(II)/Fe Total Mole Ratio'])]
            if 'Hematite' in row['TimeLabel'] or 'Hem H2S(g)/H2(g)' in row['TimeLabel']:
                if '1Y' in row['TimeLabel']:
                    return base_pos - 0.3
                elif '3Y' in row['TimeLabel']:
                    return base_pos - 0.1
                elif '5Y' in row['TimeLabel']:
                    return base_pos + 0.1
                elif '10Y' in row['TimeLabel']:
                    return base_pos + 0.3
            else:
                if '1Y' in row['TimeLabel']:
                    return base_pos - 0.2
                elif '3Y' in row['TimeLabel']:
                    return base_pos
                elif '5Y' in row['TimeLabel']:
                    return base_pos + 0.2
                elif '10Y' in row['TimeLabel']:
                    return base_pos + 0.4

        df_plot['Adjusted Position'] = df_plot.apply(adjust_positions, axis=1)

        # Create the combined plot with adjusted positions for proper spacing
        boxplot = sns.boxplot(
            x='Adjusted Position',
            y='Value',
            hue='TimeLabel',
            data=df_plot,
            whis=[0, 100],
            palette=custom_palette,  # Use custom palette
            dodge=False,
            showfliers=False,
            legend=False  # Hide the default legend
        )

        # Set transparency for the boxes
        for patch in boxplot.patches:
            patch.set_alpha(a)

        # Draw middle lines
        middle_values = {f'{time} {col}': [] for time in selected_times for col in cols}
        for x_val in unique_x_vals:
            for time in selected_times:
                for col in cols:
                    values = df_plot[(df_plot['Fe(II)/Fe Total Mole Ratio'] == x_val) &
                                     (df_plot['TimeLabel'] == f'{time} {col}')]['Value'].values
                    if len(values) == 5:
                        middle_value = sorted(values)[2]  # Use the middle value directly
                        adjusted_pos = df_plot.loc[
                            (df_plot['Fe(II)/Fe Total Mole Ratio'] == x_val) &
                            (df_plot['TimeLabel'] == f'{time} {col}'),
                            'Adjusted Position'
                        ].iloc[0]
                        line_color = custom_palette[f'{time} {col}']

                        if time == '1Y' and col == 'Hematite Per':
                            adjp = adjusted_pos + 0.3
                            plt.plot([adjp, adjp], [middle_value, middle_value],
                                     color=line_color, linestyle='None')
                        elif time == '3Y' and col == 'Hematite Per':
                            adjp = adjusted_pos + 2.1
                            plt.plot([adjp, adjp], [middle_value, middle_value],
                                     color=line_color, linestyle='None')
                        elif time == '1Y' and col == 'Goethite Per':
                            adjp = adjusted_pos + 1.2
                            plt.plot([adjp, adjp], [middle_value, middle_value],
                                     color=line_color, linestyle='None')
                        elif time == '3Y' and col == 'Goethite Per':
                            adjp = adjusted_pos +3
                            plt.plot([adjp, adjp], [middle_value, middle_value],
                                     color=line_color, linestyle='None')

                        elif time == '5Y' and col == 'Hematite Per':
                            adjp = adjusted_pos -.1
                            plt.plot([adjp, adjp], [middle_value, middle_value],
                                     color=line_color, linestyle='None')
                        elif time == '10Y' and col == 'Hematite Per':
                            adjp = adjusted_pos + 1.7
                            plt.plot([adjp, adjp], [middle_value, middle_value],
                                     color=line_color, linestyle='None')
                        elif time == '5Y' and col == 'Goethite Per':
                            adjp = adjusted_pos + 0.8
                            plt.plot([adjp, adjp], [middle_value, middle_value],
                                     color=line_color, linestyle='None')
                        elif time == '10Y' and col == 'Goethite Per':
                            adjp = adjusted_pos +2.6
                            plt.plot([adjp, adjp], [middle_value, middle_value],
                                     color=line_color, linestyle='None')

                        elif time == '1Y' and col == 'Goe H2S(g)/H2(g) [ppm]':
                            adjp = adjusted_pos + 1.3
                            plt.plot([adjp, adjp], [middle_value, middle_value],
                                     color=line_color, linestyle='None')
                        elif time == '3Y' and col == 'Goe H2S(g)/H2(g) [ppm]':
                            adjp = adjusted_pos + 3.1
                            plt.plot([adjp, adjp], [middle_value, middle_value],
                                     color=line_color, linestyle='None')
                        elif time == '1Y' and col == 'Hem H2S(g)/H2(g) [ppm]':
                            adjp = adjusted_pos + 0.4
                            plt.plot([adjp, adjp], [middle_value, middle_value],
                                     color=line_color, linestyle='None')
                        elif time == '3Y' and col == 'Hem H2S(g)/H2(g) [ppm]':
                            adjp = adjusted_pos +2.2
                            plt.plot([adjp, adjp], [middle_value, middle_value],
                                     color=line_color, linestyle='None')

                        elif time == '5Y' and col == 'Goe H2S(g)/H2(g) [ppm]':
                            adjp = adjusted_pos + 0.9
                            plt.plot([adjp, adjp], [middle_value, middle_value],
                                     color=line_color, linestyle='None')
                        elif time == '10Y' and col == 'Goe H2S(g)/H2(g) [ppm]':
                            adjp = adjusted_pos + 2.7
                            plt.plot([adjp, adjp], [middle_value, middle_value],
                                     color=line_color, linestyle='None')
                        elif time == '5Y' and col == 'Hem H2S(g)/H2(g) [ppm]':
                            adjp = adjusted_pos
                            plt.plot([adjp, adjp], [middle_value, middle_value],
                                     color=line_color, linestyle='None')
                        elif time == '10Y' and col == 'Hem H2S(g)/H2(g) [ppm]':
                            adjp = adjusted_pos +1.8
                            plt.plot([adjp, adjp], [middle_value, middle_value],
                                     color=line_color, linestyle='None')

                        middle_values[f'{time} {col}'].append((adjp, middle_value))

        # Draw curves connecting middle values
        for key, vals in middle_values.items():
            if vals:
                x_vals, y_vals = zip(*vals)
                plt.plot(x_vals, y_vals, color=custom_palette[key], linestyle='-', linewidth=1)

        # Manually create the legend based on selected_times
        legend_elements = []
        if '1Y' in selected_times:
            legend_elements.append(plt.Line2D([0], [0], color='#8b0000', lw=4, label='Hematite 1Y', alpha=a))
            legend_elements.append(plt.Line2D([0], [0], color='#00008b', lw=4, label='Goethite 1Y', alpha=a))
        if '3Y' in selected_times:
            legend_elements.append(plt.Line2D([0], [0], color='#ff6347', lw=4, label='Hematite 3Y', alpha=a))
            legend_elements.append(plt.Line2D([0], [0], color='#87cefa', lw=4, label='Goethite 3Y', alpha=a))
        if '5Y' in selected_times:
            legend_elements.append(plt.Line2D([0], [0], color='#8b0000', lw=4, label='Hematite 5Y', alpha=a))
            legend_elements.append(plt.Line2D([0], [0], color='#00008b', lw=4, label='Goethite 5Y', alpha=a))
        if '10Y' in selected_times:
            legend_elements.append(plt.Line2D([0], [0], color='#ff6347', lw=4, label='Hematite 10Y', alpha=a))
            legend_elements.append(plt.Line2D([0], [0], color='#87cefa', lw=4, label='Goethite 10Y', alpha=a))

        # Set legend position based on molecule type
        legend_position = 'upper left' if molecule == 'H2SAQ' else 'upper right'
        plt.legend(handles=legend_elements, title='Mineral and Time', loc=legend_position, fontsize=16, title_fontsize=16)

        # Adjust x-ticks to be directly below their corresponding boxes
        new_xticks = [positions[i] for i in range(len(unique_x_vals))]
        plt.xticks(ticks=new_xticks, labels=[f"{x:.3f}" for x in unique_x_vals], rotation=45, fontsize=16)
        plt.yticks(fontsize=16)

        # Set x and y labels based on the molecule type
        plt.xlabel('Fe(II)/Fe(tot) Mole Ratio', fontsize=18)
        if molecule == 'H2':
            plt.ylabel('H$_2$(g) Fractional Loss', fontsize=18)
        else:
            plt.ylabel('H$_2$S Concentration [ppm]', fontsize=18)

        plt.tight_layout()
        plt.savefig(f'{molecule}_{filename_suffix}.png')
        plt.show()

# Create plots for the specified time groups
create_combined_plots(['1Y', '3Y'], '1Y_3Y')
create_combined_plots(['5Y', '10Y'], '5Y_10Y')
