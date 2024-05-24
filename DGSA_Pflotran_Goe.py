import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

folder_path = '.'

dfexp = pd.read_excel(os.path.join(folder_path, 'LHS_Parameters_Goe_Rate.xlsx'))
# titles = ['Temperature', 'Water saturation', 'Fe(III)/Fe(II) ratio', 'Weight percent of iron', 'Specific surface area', 'Pyrite dissolution rate', 'Goethite dissolution rate']
# titles = ['Temperature', 'Water saturation', 'Fe(III)/Fe(II) ratio', 'Weight percent of iron', 'Pyrite surface area', 'Goethite surface area', 'Pyrite dissolution rate', 'Goethite dissolution rate']
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
from numpy.linalg import svd

distances = pdist(responses, metric='euclidean')
distances = squareform(distances)

T = np.dot(distances, distances.T)
cluster_colors = ['red', 'blue', 'green']
cluster_labels = ['Cluster 1', 'Cluster 2', 'Cluster 3']

# Cluster the responses using KMedoids
from pyDGSA.cluster import KMedoids

n_clusters = 3
clusterer = KMedoids(n_clusters=n_clusters, max_iter=5000, tol=1e-4)
labels, medoids = clusterer.fit_predict(distances)

scaler = StandardScaler()
scaled_T = scaler.fit_transform(T)
#
# from sklearn.manifold import TSNE
# # t-Distributed Stochastic Neighbor Embedding
# tsne = TSNE(n_components=2, perplexity=5, learning_rate=10, n_iter=1000)
# reduced_dim_tsne = tsne.fit_transform(distances)
#
# plt.figure(figsize=(10, 6))
# plt.scatter(reduced_dim_tsne[:, 0], reduced_dim_tsne[:, 1], c=labels, cmap='viridis')
# plt.xlabel('t-SNE Component 1')
# plt.ylabel('t-SNE Component 2')
# plt.title('t-SNE Projection')
# plt.grid(True)
# plt.show()
#
from sklearn.decomposition import KernelPCA

kpca = KernelPCA(n_components=2, kernel='sigmoid', gamma=0.5)
reduced_dim_kpca = kpca.fit_transform(scaled_T)

plt.figure(figsize=(10, 6))
plt.scatter(reduced_dim_kpca[:, 0], reduced_dim_kpca[:, 1], c=labels, cmap='viridis')
plt.xlabel('Kernel Principal Component 1')
plt.ylabel('Kernel Principal Component 2')
plt.title('Kernel PCA Projection')
plt.grid(True)
plt.show()
#
# # SVD
# U, S, VT = svd(distances)
# reduced_dim = U*np.sqrt(S)
#
# # Get variance of first two componentes
# singular_values = S
# squared_singular_values = singular_values ** 2
# total_variance = np.sum(squared_singular_values)
# variance_explained = squared_singular_values / total_variance
# variance_explained_first = np.sum(variance_explained[:1])
# variance_explained_first_two = np.sum(variance_explained[:2])
# print(variance_explained_first)
# print(variance_explained_first_two)
#
#
#
#
#
#
#
#
# plt.figure(figsize=(8, 6))
# scatter_objects = []
# for i in range(n_clusters):
#     # Select data for each cluster
#     cluster_indices = labels == i
#     # scatter = plt.scatter(reduced_dim[cluster_indices, 0], reduced_dim[cluster_indices, 1], color=cluster_colors[i])
#     scatter = plt.scatter(reduced_dim[cluster_indices, 0], reduced_dim[cluster_indices, 1], color=cluster_colors[i])
#     scatter_objects.append(scatter)
#
# plt.xlabel('Principal Component 1', fontsize=16)
# plt.ylabel('Principal Component 2', fontsize=16)
# plt.grid(True)
# plt.legend(scatter_objects, cluster_labels,fontsize=14)
# plt.savefig('./Cluster_H2S_Goe.png', dpi=300)
# plt.show()


# #==================
# # Main Effects
# #==================
# from pyDGSA.dgsa import dgsa
#
# mean_sensitivity = dgsa(parameters, labels, parameter_names=parameter_names, quantile=0.945,
#                         n_boots=5000, confidence=True)
# print(mean_sensitivity)
#
# cluster_names = [f'Cluster{i+1}' for i in range(n_clusters)]
#
# cluster_sensitivity = dgsa(parameters, labels, parameter_names=parameter_names,
#                            output='cluster_avg', cluster_names=cluster_names)
# print(cluster_sensitivity)
#
# #=========================
# # Interaction Effects
# #=========================
# from pyDGSA.dgsa import dgsa_interactions
#
# mean_interact_sensitivity = dgsa_interactions(parameters, labels,
#                                               parameter_names=parameter_names)
# print(mean_interact_sensitivity)
#
# sens = dgsa_interactions(parameters, labels,
#                         #  cond_parameters=['depth','deviation','length', 'direction'],
#                          cond_parameters=parameter_names,
#                          parameter_names=parameter_names,
#                          n_bins=24)
# print(sens)
#
# cluster_interact_sensitivity = dgsa_interactions(parameters, labels,
#                                                  parameter_names=parameter_names,
#                                                  cluster_names=cluster_names,
#                                                  output='cluster_avg')
# print(cluster_interact_sensitivity)
#
# from pyDGSA.dgsa import dgsa_interactions
# raw_interact_sensitivity = dgsa_interactions(parameters, labels,
#                                              parameter_names=parameter_names,
#                                              cluster_names=cluster_names,
#                                              output='indiv')
# print(raw_interact_sensitivity)
#
#
#
#
#
# #===================
# # Plot Main Effects
# #===================
# from pyDGSA.plot import vert_pareto_plot
#
# fig, ax = vert_pareto_plot(mean_sensitivity, np_plot='+5', confidence=True)
# # ax.set_xlabel('Sensitivity for H$_2$ Loss from Dissolution')
# # ax.set_xlabel('Sensitivity for H$_2$ Loss from Reaction')
# ax.set_xlabel('Sensitivity for Total H$_2$ Loss')
# # ax.set_xlabel('Sensitivity for H$_2$S Generation')
#
# fig.savefig('./H2_Tot_Goe.png', bbox_inches='tight', pad_inches=0.1, dpi=300)
# # fig.savefig('./H2_Dis_Goe.png', bbox_inches='tight', pad_inches=0.1, dpi=300)
# # fig.savefig('./H2_Rea_Goe.png', bbox_inches='tight', pad_inches=0.1, dpi=300)
# # fig.savefig('./H2S_Goe.png', bbox_inches='tight', pad_inches=0.1, dpi=300)
#
# # #====================
# # # Plot Clusters' DGSA
# # #====================
# # # Define the colors for each cluster
# # cluster_colors = ['orange', 'green', 'blue', 'red', 'yellow', 'black']
# #
# # # Only plot 3 parameters total to save space (np_plot=3)
# # fig, ax = vert_pareto_plot(cluster_sensitivity, np_plot=4, fmt='cluster_avg',
# #                            colors=cluster_colors)
# # ax.set_xlabel('Sensitivity for H$_2$ Loss from Dissolution within Clusters')
# # ax.set_xlabel('Sensitivity for H$_2$ Loss from Geochemical Reaction within Clusters')
# # ax.set_xlabel('Sensitivity for Total H$_2$ Loss within Clusters')
# # ax.set_xlabel('Sensitivity for H$_2$S Generation within Clusters')
#
# #==========
# # CDF Plots
# #==========
# from pyDGSA.plot import plot_cdf
#
# for item in parameter_names:
#     fig, ax = plot_cdf(parameters, labels, item, parameter_names=parameter_names,
#                     cluster_names=cluster_names, colors=cluster_colors, plot_prior=True)
#
#
# # #==============
# # # Plot scatters
# # #==============
# # import matplotlib.pyplot as plt
# # from sklearn.manifold import MDS
# #
# # # Get MDS representation of distance matrix
# # mds = MDS(n_components=2, dissimilarity='precomputed', random_state=1, normalized_stress=False)
# # mds_dist = mds.fit_transform(distances)
# #
# # ## Plot mds distances as scatterplot
# # fig, ax = plt.subplots(figsize=(8, 5), facecolor='white')
# # x = mds_dist[:, 0]
# # y = mds_dist[:, 1]
# #
# # # Plotting each cluster individually using a for loop,
# # # though it's possible to plot all clusters at once using
# # # ax.scatter(x, y, c=[cluster_colors[i] for i in labels])
# # for i in range(n_clusters):
# #     sc = ax.scatter(x[labels == i], y[labels == i],
# #                     c=cluster_colors[i], label=cluster_names[i])
# # ax.set(xlabel='Dim 1', ylabel='Dim 2')
# # ax.legend()
#
# #=========================
# # Plot Interaction Effects
# #=========================
# # Only show interactions with sensitivity >= 1 and the next 3 most
# fig, ax = vert_pareto_plot(mean_interact_sensitivity, np_plot='+1')
# # ax.set_xlabel('Interaction Sensitivity for H$_2$ Loss from Dissolution')
# # ax.set_xlabel('Interaction Sensitivity for H$_2$ Loss from Reactions')
# ax.set_xlabel('Interaction Sensitivity for Total H$_2$ Loss')
# # ax.set_xlabel('Interaction Sensitivity for H$_2$S Generation')
#
# fig.savefig('./H2_Tot_Interact_Goe.png', bbox_inches='tight', pad_inches=0.1, dpi=300)
# # fig.savefig('./H2_Dis_Interact_Goe.png', bbox_inches='tight', pad_inches=0.1, dpi=300)
# # fig.savefig('./H2_Rea_Interact_Goe.png', bbox_inches='tight', pad_inches=0.1, dpi=300)
# # fig.savefig('./H2S_Interact_Goe.png', bbox_inches='tight', pad_inches=0.1, dpi=300)
#
# # # By default, np_plot = '+5'
# # fig, ax = vert_pareto_plot(cluster_interact_sensitivity,
# #                            fmt='cluster_avg',
# #                            colors=cluster_colors)
# # ax.set_xlabel('Interaction Sensitivity for H$_2$ Loss from Dissolution within Clusters')
# # ax.set_xlabel('Interaction Sensitivity for H$_2$ Loss from Geochemical Reactions within Clusters')
# # ax.set_xlabel('Interaction Sensitivity for Total H$_2$ Loss')
# # ax.set_xlabel('Interaction Sensitivity for H$_2$S Generation within Clusters')
#
# plt.show()