import numpy as np
import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt

from sklearn.manifold import MDS

# Reference:
# Perzan, Z., Babey, T., Caers, J., Bargar, J.R. and Maher, K., 2021, Local and global sensitivity analysis of a
# reactive transport model simulating floodplain redox cycling, Water Resources Research, doi: 10.1029/2021WR029723

def plot_cdf(parameters, labels, parameter, cluster_names=None, colors=None,
             figsize=(5, 5), parameter_names=None, legend_names=None,
             plot_prior=False, fontsize=12):
    """Plot the class-conditional cdf for a single parameter.

    params:
        parameters [array(float)]: array of shape (n_parameters, n_simulations)
                containing the parameter sets used for each model run
        labels [array(int)]: array of length n_simulations where each value
                represents the cluster to which that model belongs
        parameter [int]: index of the parameter to plot, corresponding to a
                column within `parameters`
        cluster_names [list(str)]: ordered list of cluster names corresponding
                to the label array, ie the 0th element of cluster_names is the
                name of the cluster where labels==0. Optional, default is
                ['Cluster 0', 'Cluster 1', ...]
        colors [list]: colors to plot
        figsize [tuple(float)]: matplotlib figure size in inches. Optional,
                default: (5,5)
        parameter_name [str]: name of the parameter as listed on the x-axis
                label. Optional, defaults to 'Parameter #'
        legend_names [list(str)]: ordered list of names to display in the
                legend. Optional, but must be a permuted version of
                cluster_names.
        fontsize [int]: font size for labels and legend. Optional, default: 12

    returns:
        fig: matplotlib figure handle
        ax: matplotlib axis handle
    """

    # Check input
    n_clusters = labels.max() + 1
    n_parameters = parameters.shape[1]

    if colors is None:
        colors = []
        cmap = matplotlib.cm.get_cmap('Set1')
        for i in range(n_clusters):
            colors.append(cmap(i))

    if cluster_names is None:
        cluster_names = ['Cluster %s' % i for i in range(n_clusters)]

    # If parameter is given as string, look for it in parameter_names
    if isinstance(parameter, str):
        if parameter_names is None:
            raise ValueError('Must provide list of parameter names if providing \
                parameter to plot as a string.')
        elif parameter not in parameter_names:
            raise ValueError('Could not find %s in parameter_names' % parameter)
        else:
            param_idx = parameter_names.index(parameter)

    elif isinstance(parameter, int):
        if parameter > (n_parameters - 1):
            raise ValueError('Parameter index passed (%s) is greater than the \
                             length of parameter_names' % parameter)
        else:
            param_idx = parameter

    if parameter_names is None:
        parameter_names = ['Parameter %s' % i for i in range(n_parameters)]

    # Get list of parameters (used for labeling with full col name)
    percentiles = np.arange(1, 100)

    fig, ax = plt.subplots(figsize=figsize, tight_layout=True)

    if plot_prior:
        ax.plot(np.percentile(parameters[:, param_idx], percentiles),
                percentiles, color='k', linestyle='--', label='$F$ ($X_i$)')

    for i in range(n_clusters):
        x = np.percentile(parameters[np.where(labels == i), param_idx], percentiles)
        ax.plot(x, percentiles, color=colors[i],
                label='$F$ ($X_i$ | %s)' % cluster_names[i])

    ax.set(xlabel=parameter_names[param_idx], ylabel='% of simulations')

    # Set font sizes
    ax.xaxis.label.set_fontsize(fontsize)
    ax.yaxis.label.set_fontsize(fontsize)
    ax.tick_params(axis='both', which='major', labelsize=fontsize)

    # If legend_names is provided, sort the handles before adding legend
    if legend_names is None:
        ax.legend(fontsize=fontsize)
    else:
        handles, legend_labels = ax.get_legend_handles_labels()
        reordered_handles = []
        for name in legend_names:
            idx = legend_labels.index('$F$ ($X_i$ | %s)' % name)
            reordered_handles.append(handles[idx])

        ax.legend(reordered_handles, legend_names, fontsize=fontsize)

    return fig, ax


folder_path = '.'
dfexp = pd.read_excel(os.path.join(folder_path, 'LHS_Parameters_Goe_Rate.xlsx'))
titles = ['Temperature', 'Water saturation', 'Fe(III)/Fe(II) ratio', 'Pyrite Mass', 'Goethite Mass', 'Pyrite rate coefficient', 'Goethite rate coefficient']
dfexp.columns.values[:7] = titles
parameters = dfexp.values[:,0:7]

# responses = dfexp.values[:,-1].reshape(-1,1)     # Loss from dissolution
# responses = dfexp.values[:,-2].reshape(-1,1)     # Loss from reaction
responses = dfexp.values[:,-5].reshape(-1,1)     # Total Loss
# responses = dfexp.values[:,-3].reshape(-1,1)     # H2S generation

parameter_names = list(dfexp.columns[0:7])

from scipy.spatial.distance import pdist, squareform
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# responses = scaler.fit_transform(responses)
distances = pdist(responses, metric='euclidean')
distances = squareform(distances)

cluster_colors = ['red', 'blue', 'green']
cluster_labels = ['Cluster 1', 'Cluster 2', 'Cluster 3']

# Cluster the responses using KMedoids
from pyDGSA.cluster import KMedoids

n_clusters = 3
cluster_colors = ['orange', 'green', 'blue', 'red', 'black']
cluster_names = [f'Cluster{i+1}' for i in range(n_clusters)]

clusterer = KMedoids(n_clusters=n_clusters, max_iter=5000, tol=1e-6)
labels, medoids = clusterer.fit_predict(distances)

# Plotting clusters
fs = 14
mds = MDS(n_components=3, dissimilarity='precomputed', random_state=1, normalized_stress=False)
mds_dist = mds.fit_transform(distances)

fig = plt.figure(figsize=(15, 12))
ax = fig.add_subplot(111, projection='3d')
x = mds_dist[:, 0]
y = mds_dist[:, 1]
z = mds_dist[:, 2]
for i in range(n_clusters):
    sc = ax.scatter(x[labels == i], y[labels == i], z[labels == i],
                    c=cluster_colors[i], label=cluster_names[i])
ax.set(xlabel='Dim 1', ylabel='Dim 2', zlabel='Dim 3')
ax.set_xlabel(xlabel='Dim 1', fontsize=fs)
ax.set_ylabel(ylabel='Dim 2', fontsize=fs)
ax.set_zlabel(zlabel='Dim 3', fontsize=fs)
ax.tick_params(axis='both', labelsize=fs-4)

# Fix the angle of the 3D plot
# ax.view_init(elev=15, azim=199)
ax.view_init(elev=15, azim=75)

ax.legend()
plt.savefig('Tot_Cluster_Goe.png', dpi=300)
plt.show()

#==================
# Main Effects
#==================
from pyDGSA.dgsa import dgsa

mean_sensitivity = dgsa(parameters, labels, parameter_names=parameter_names, quantile=0.95,
                        n_boots=5000, confidence=True)
print(mean_sensitivity)

cluster_names = [f'Cluster{i+1}' for i in range(n_clusters)]

cluster_sensitivity = dgsa(parameters, labels, parameter_names=parameter_names,
                           output='cluster_avg', cluster_names=cluster_names)
print(cluster_sensitivity)

#=========================
# Interaction Effects
#=========================
from pyDGSA.dgsa import dgsa_interactions

mean_interact_sensitivity = dgsa_interactions(parameters, labels,
                                              parameter_names=parameter_names)
print(mean_interact_sensitivity)

sens = dgsa_interactions(parameters, labels,
                        #  cond_parameters=['depth','deviation','length', 'direction'],
                         cond_parameters=parameter_names,
                         parameter_names=parameter_names,
                         n_bins=16)
print(sens)

cluster_interact_sensitivity = dgsa_interactions(parameters, labels,
                                                 parameter_names=parameter_names,
                                                 cluster_names=cluster_names,
                                                 output='cluster_avg')
print(cluster_interact_sensitivity)

from pyDGSA.dgsa import dgsa_interactions
raw_interact_sensitivity = dgsa_interactions(parameters, labels,
                                             parameter_names=parameter_names,
                                             cluster_names=cluster_names,
                                             output='indiv')
print(raw_interact_sensitivity)

#===================
# Plot Main Effects
#===================
from pyDGSA.plot import vert_pareto_plot

fig, ax = vert_pareto_plot(mean_sensitivity, np_plot='+5', confidence=True)
# ax.set_xlabel('Sensitivity for H$_2$ Loss from Dissolution')
# ax.set_xlabel('Sensitivity for H$_2$ Loss from Reaction')
ax.set_xlabel('Sensitivity for Total H$_2$ Loss', fontsize=15)
# ax.set_xlabel('Sensitivity for H$_2$S Formation', fontsize=15)
ax.tick_params(axis='both', which='major', labelsize=15)
ax.text(-0.2, 1.1, 'b)', transform=ax.transAxes, fontsize=20, fontweight='bold', va='top')
fig.savefig('./H2_Tot_Goe.png', bbox_inches='tight', pad_inches=0.1, dpi=300)
# fig.savefig('./H2_Dis_Goe.png', bbox_inches='tight', pad_inches=0.1, dpi=300)
# fig.savefig('./H2_Rea_Goe.png', bbox_inches='tight', pad_inches=0.1, dpi=300)
# fig.savefig('./H2S_Goe.png', bbox_inches='tight', pad_inches=0.1, dpi=300)

#====================
# Plot Clusters' DGSA
#====================
# Define the colors for each cluster
cluster_colors = ['orange', 'green', 'blue', 'red', 'yellow', 'black']

# Only plot 3 parameters total to save space (np_plot=3)
fig, ax = vert_pareto_plot(cluster_sensitivity, np_plot=4, fmt='cluster_avg',
                           colors=cluster_colors)
ax.set_xlabel('Sensitivity for H$_2$ Loss from Dissolution within Clusters')
ax.set_xlabel('Sensitivity for H$_2$ Loss from Geochemical Reaction within Clusters')
ax.set_xlabel('Sensitivity for Total H$_2$ Loss within Clusters')
ax.set_xlabel('Sensitivity for H$_2$S Generation within Clusters')

#==========
# CDF Plots
#==========
for item in parameter_names:
    fig, ax = plot_cdf(parameters, labels, item, parameter_names=parameter_names,
                    cluster_names=cluster_names, colors=cluster_colors, plot_prior=True)

#==============
# Plot scatters
#==============
import matplotlib.pyplot as plt
from sklearn.manifold import MDS

# Get MDS representation of distance matrix
mds = MDS(n_components=2, dissimilarity='precomputed', random_state=1, normalized_stress=False)
mds_dist = mds.fit_transform(distances)

# Plot mds distances as scatterplot
fig, ax = plt.subplots(figsize=(8, 5), facecolor='white')
x = mds_dist[:, 0]
y = mds_dist[:, 1]

# Plotting each cluster individually using a for loop,
# though it's possible to plot all clusters at once using
# ax.scatter(x, y, c=[cluster_colors[i] for i in labels])
for i in range(n_clusters):
    sc = ax.scatter(x[labels == i], y[labels == i],
                    c=cluster_colors[i], label=cluster_names[i])
ax.set(xlabel='Dim 1', ylabel='Dim 2')
ax.legend()

#=========================
# Plot Interaction Effects
#=========================
# Only show interactions with sensitivity >= 1 and the next 3 most
fig, ax = vert_pareto_plot(mean_interact_sensitivity, np_plot='+1')
# ax.set_xlabel('Interaction Sensitivity for H$_2$ Loss from Dissolution')
# ax.set_xlabel('Interaction Sensitivity for H$_2$ Loss from Reactions')
ax.set_xlabel('Interaction Sensitivity for Total H$_2$ Loss', fontsize=14)
# ax.set_xlabel('Interaction Sensitivity for H$_2$S Formation', fontsize=13)
ax.tick_params(axis='both', which='major', labelsize=13)
ax.text(-0.2, 1.1, 'b)', transform=ax.transAxes, fontsize=20, fontweight='bold', va='top')
fig.savefig('./H2_Tot_Interact_Goe.png', bbox_inches='tight', pad_inches=0.1, dpi=300)
# fig.savefig('./H2_Dis_Interact_Goe.png', bbox_inches='tight', pad_inches=0.1, dpi=300)
# fig.savefig('./H2_Rea_Interact_Goe.png', bbox_inches='tight', pad_inches=0.1, dpi=300)
# fig.savefig('./H2S_Interact_Goe.png', bbox_inches='tight', pad_inches=0.1, dpi=300)

# By default, np_plot = '+5'
fig, ax = vert_pareto_plot(cluster_interact_sensitivity,
                           fmt='cluster_avg',
                           colors=cluster_colors)
ax.set_xlabel('Interaction Sensitivity for H$_2$ Loss from Dissolution within Clusters')
ax.set_xlabel('Interaction Sensitivity for H$_2$ Loss from Geochemical Reactions within Clusters')
ax.set_xlabel('Interaction Sensitivity for Total H$_2$ Loss')
ax.set_xlabel('Interaction Sensitivity for H$_2$S Generation within Clusters')

plt.show()