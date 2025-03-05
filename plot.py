# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 15:40:34 2024

@author: Arindam
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

os.chdir(r"C:\Phd\CUDA test\Test\test 1\EV\ICDCN_extension\code")

# Set font type globally (Level 1)
plt.rcParams['font.family'] = 'serif'  # Example: 'serif', 'sans-serif', 'monospace', etc.


def plot_varyingEV(csv_file, q):
    data = pd.read_csv(csv_file)
    data = data[(data['Method'] != 'SMEVCA-D') & (data['Method'] != 'SMEVCA-G')]

    
    markers = {
        #'random_elemination': 'o',
        'PCG': 's',
        'PCD': 'D',
        'PCL': 'o'
    }
    
    plt.figure(figsize=(10, 6))
    plt.tight_layout()
    for method, marker in markers.items():
        method_data = data[data['Method'] == method]
        sns.lineplot(data=method_data, x='Total EV', y='execution time', marker=marker, label=method)
    plt.xlabel('Total EV', fontsize=22)
    plt.ylabel('Execution Time (ms)', fontsize=22)
    plt.title('Execution Time', fontsize=22)
    plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'execution_time_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    # Plot 2
    data['Total charge transferred'] = data['Total charge transferred in-net'] + data['Total charge transferred par-net']
    
    plt.figure(figsize=(10, 6))
    plt.tight_layout()
    for method, marker in markers.items():
        method_data = data[data['Method'] == method]
        sns.lineplot(data=method_data, x='Total EV', y='Total charge transferred', marker=marker, label=method)
    
    # Customize font sizes
    plt.xlabel('Total EV', fontsize=20)
    plt.ylabel('Charge Transferred (kWh)', fontsize=20)
    plt.title('Total charge transferred', fontsize=22)
    plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'Total_Charge_Transfer_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    # Plot 2 A
    data['Total EV charged'] = data['Total EV charged in-net'] + data['Total EV charged par-net']
    
    plt.figure(figsize=(10, 6))
    plt.tight_layout()
    for method, marker in markers.items():
        method_data = data[data['Method'] == method]
        sns.lineplot(data=method_data, x='Total EV', y='Total EV charged', marker=marker, label=method)
    
    # Customize font sizes
    plt.xlabel('Total EV', fontsize=20)
    plt.ylabel('EV Charged', fontsize=20)
    plt.title('Total EV Charged', fontsize=22)
    plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'Total_EV_charged_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    ## Plot 3
    # data2 = data[data['Method'] !='random_elemination']
    data['total SLA missed'] = data['Total SLA breach'] + data['unmatched EV']
    plt.figure(figsize=(10, 6))
    plt.tight_layout()
    for method, marker in markers.items():
        # if method=='random_elemination':
        #     continue
        method_data = data[data['Method'] == method]
        sns.lineplot(data=method_data, x='Total EV', y='total SLA missed', marker=marker, label=method)
    
    # Customize font sizes
    plt.xlabel('Total EV', fontsize=22)
    plt.ylabel('Unassigned EVs', fontsize=22)
    plt.title('SLA constraint Analysis', fontsize=22)
    plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'Unassigned_EV_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    ## Plot total cost
    # data2 = data[data['Method'] !='random_elemination']
    plt.figure(figsize=(10, 6))
    plt.tight_layout()
    for method, marker in markers.items():
        # if method=='random_elemination':
        #     continue
        method_data = data[data['Method'] == method]
        sns.lineplot(data=method_data, x='Total EV', y='Total cost to vendor', marker=marker, label=method)
    
    # Customize font sizes
    plt.xlabel('Total EV', fontsize=22)
    plt.ylabel('Total cost to vendor ($)', fontsize=22)
    plt.title('Cost Analysis', fontsize=22)
    plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'Total_cost_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    
    # ## Plot 4 & 5
    # # Filter the data for the required methods
    pcg_data = data[data['Method'] == 'PCG']
    pcd_data = data[data['Method'] == 'PCD']
    pcl_data = data[data['Method'] == 'PCL']
    # smevca_pcg_data = data[data['Method'] == 'SMEVCA-G']
    # smevca_pcd_data = data[data['Method'] == 'SMEVCA-D']
    
    # palette = sns.color_palette("mako", 8)
    
    # # Prepare the data for bar plotting
    # plot_data = pd.DataFrame({
    #     'Total EV': pd.concat([pcg_data['Total EV'], pcg_data['Total EV'], pcd_data['Total EV'], pcd_data['Total EV'], smevca_pcg_data['Total EV'], smevca_pcg_data['Total EV'], smevca_pcd_data['Total EV'], smevca_pcd_data['Total EV']]),
    #     'EV Charged': pd.concat([pcg_data['Total EV charged in-net'], pcg_data['Total EV charged par-net'], 
    #                              pcd_data['Total EV charged in-net'], pcd_data['Total EV charged par-net'],
    #                              smevca_pcg_data['Total EV charged in-net'], smevca_pcg_data['Total EV charged par-net'], 
    #                              smevca_pcd_data['Total EV charged in-net'], smevca_pcd_data['Total EV charged par-net']]),
    #     'Category': ['PCG In-net'] * len(pcg_data) + ['PCG par-net'] * len(pcg_data) + 
    #                 ['PCD In-net'] * len(pcd_data) + ['PCD par-net'] * len(pcd_data) +
    #                 ['SMEVCA-G In-net'] * len(pcg_data) + ['SMEVCA-G par-net'] * len(pcg_data) + 
    #                 ['SMEVCA-D In-net'] * len(pcd_data) + ['SMEVCA-D par-net'] * len(pcd_data)
    # })
    
    # # Create the bar plot
    # plt.figure(figsize=(16, 8))
    # plt.tight_layout()
    # sns.barplot(x='Total EV', y='EV Charged', hue='Category', data=plot_data, palette=palette)
    
    # # Customize font sizes
    # plt.xlabel('Total EV', fontsize=22)
    # plt.ylabel('EV Charged', fontsize=22)
    # plt.title('EV Assignments', fontsize=22)
    # #plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
    # plt.legend(title='Category', fontsize=16, title_fontsize=22, 
    #        loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4)
    # plt.tick_params(axis='both', which='major', labelsize=20)
    # plt.grid(True)
    # plt.savefig(f'EV_Assignments_q{q}.pdf', dpi=250, bbox_inches='tight')
    # plt.show()
    # plt.clf()
    
    
    # # plot charge transferred
    # palette = sns.color_palette("rocket", 8)
    # plot_data = pd.DataFrame({
    #     'Total EV': pd.concat([pcg_data['Total EV'], pcg_data['Total EV'], pcd_data['Total EV'], pcd_data['Total EV'], smevca_pcg_data['Total EV'], smevca_pcg_data['Total EV'], smevca_pcd_data['Total EV'], smevca_pcd_data['Total EV']]),
    #     'EV Charged': pd.concat([pcg_data['Total charge transferred in-net'], pcg_data['Total charge transferred par-net'], 
    #                              pcd_data['Total charge transferred in-net'], pcd_data['Total charge transferred par-net'],
    #                              smevca_pcg_data['Total charge transferred in-net'], smevca_pcg_data['Total charge transferred par-net'], 
    #                              smevca_pcd_data['Total charge transferred in-net'], smevca_pcd_data['Total charge transferred par-net']]),
    #     'Category': ['PCG In-net'] * len(pcg_data) + ['PCG par-net'] * len(pcg_data) + 
    #                 ['PCD In-net'] * len(pcd_data) + ['PCD par-net'] * len(pcd_data) +
    #                 ['SMEVCA-G In-net'] * len(pcg_data) + ['SMEVCA-G par-net'] * len(pcg_data) + 
    #                 ['SMEVCA-D In-net'] * len(pcd_data) + ['SMEVCA-D par-net'] * len(pcd_data)
    # })
    
    # # Create the bar plot
    # plt.figure(figsize=(16, 8))
    # plt.tight_layout()
    # sns.barplot(x='Total EV', y='EV Charged', hue='Category', data=plot_data, palette=palette)
    
    # # Customize font sizes
    # plt.xlabel('Total EV', fontsize=22)
    # plt.ylabel('Total charge transferred (kWh)', fontsize=22)
    # plt.title('Transferred Charge', fontsize=22)
    # #plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
    # plt.legend(title='Category', fontsize=16, title_fontsize=22, 
    #        loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4)
    # plt.tick_params(axis='both', which='major', labelsize=20)
    # plt.grid(True)
    # plt.savefig(f'Transferred_Charge_q{q}.pdf', dpi=250, bbox_inches='tight')
    # plt.show()
    # plt.clf()
    
    
    ## Plot avg cost per kWh
    # palette = sns.cubehelix_palette(n_colors=4, start=.75, rot=-.5)
    palette = sns.dark_palette("#69d", n_colors=4)
    plot_data = pd.DataFrame({
        'Total EV': pd.concat([pcg_data['Total EV'], pcd_data['Total EV'], pcl_data['Total EV']]),
        'Avg. cost per kWh charging': pd.concat([pcg_data['Avg. cost'], pcd_data['Avg. cost'],
                                                 pcl_data['Avg. cost']]),
        'Category': ['PCG'] * len(pcg_data) + ['PCD'] * len(pcd_data) + ['PCL'] * len(pcl_data)
    })
    
    # Create the bar plot
    plt.figure(figsize=(12, 8))
    plt.tight_layout()
    sns.barplot(x='Total EV', y='Avg. cost per kWh charging', hue='Category', data=plot_data, palette=palette)
    
    # Customize font sizes
    plt.xlabel('Total EV', fontsize=22)
    plt.ylabel('Avg. cost per EV charging', fontsize=22)
    plt.title('Avg. cost', fontsize=22)
    plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'AvgCost_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    ## Plot avg detour
    palette = sns.color_palette("viridis", 4)
    plot_data = pd.DataFrame({
        'Total EV': pd.concat([pcg_data['Total EV'], pcd_data['Total EV'], pcl_data['Total EV']]),
        'Avg. detour distance': pd.concat([pcg_data['Avg. detour'], pcd_data['Avg. detour'],
                                           pcl_data['Avg. detour']]),
        'Category': ['PCG'] * len(pcg_data) + ['PCD'] * len(pcd_data) + ['PCL'] * len(pcl_data)
    })
    
    # Create the bar plot
    plt.figure(figsize=(12, 8))
    plt.tight_layout()
    sns.barplot(x='Total EV', y='Avg. detour distance', hue='Category', data=plot_data, palette=palette)
    
    # Customize font sizes
    plt.xlabel('Total EV', fontsize=22)
    plt.ylabel('Avg. detour distance (mile)', fontsize=22)
    plt.title('Avg. detour', fontsize=22)
    plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'AvgDetour_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    
    
# def plot_varyingQ(csv_file, n_ev):
#     data = pd.read_csv(csv_file)
#     xtick_values = data['CP Queue'].unique()
    
#     markers = {
#         'random_elemination': 'o',
#         'PCG': 's',
#         'PCD': 'D'
#     }
    
#     plt.figure(figsize=(10, 6))
#     plt.tight_layout()
#     for method, marker in markers.items():
#         method_data = data[data['Method'] == method]
#         sns.lineplot(data=method_data, x='CP Queue', y='execution time', marker=marker, label=method)
#     plt.xlabel(r'Charging Point Quota $q$', fontsize=22)
#     plt.ylabel('Execution Time (ms)', fontsize=22)
#     plt.title('Execution Time', fontsize=22)
#     plt.legend(title='Methods', fontsize=16, title_fontsize=22)
#     plt.tick_params(axis='both', which='major', labelsize=20)
#     plt.xticks(xtick_values)
#     plt.grid(True)
#     plt.savefig(f'execution_time_varyingQ_n_ev{n_ev}.pdf', dpi=250, bbox_inches='tight')
#     plt.show()
#     plt.clf()
    
    
#     # Plot 2
#     plt.figure(figsize=(10, 6))
#     plt.tight_layout()
#     for method, marker in markers.items():
#         method_data = data[data['Method'] == method]
#         sns.lineplot(data=method_data, x='CP Queue', y='Total charge transferred in-net', marker=marker, label=method)
    
#     # Customize font sizes
#     plt.xlabel(r'Charging Point Quota $q$', fontsize=22)
#     plt.ylabel('Charge Transferred (kWh)', fontsize=22)
#     plt.title('In-net Charge Transfer', fontsize=22)
#     plt.legend(title='Methods', fontsize=15, title_fontsize=16)
#     plt.tick_params(axis='both', which='major', labelsize=20)
#     plt.xticks(xtick_values)
#     plt.grid(True)
#     plt.savefig(f'In-net_Charge_Transfer_varyingQ_n_ev{n_ev}.pdf', dpi=250, bbox_inches='tight')
#     plt.show()
#     plt.clf()
    
    
#     ## Plot 3
#     # data2 = data[data['Method'] !='random_elemination']
#     data['total SLA missed'] = data['Total SLA breach'] + data['unmatched EV']
#     plt.figure(figsize=(10, 6))
#     plt.tight_layout()
#     for method, marker in markers.items():
#         # if method=='random_elemination':
#         #     continue
#         method_data = data[data['Method'] == method]
#         sns.lineplot(data=method_data, x='CP Queue', y='total SLA missed', marker=marker, label=method)
    
#     # Customize font sizes
#     plt.xlabel(r'Charging Point Quota $q$', fontsize=22)
#     plt.ylabel('Missed SLA', fontsize=22)
#     plt.title('SLA Analysis', fontsize=22)
#     plt.legend(title='Methods', fontsize=15, title_fontsize=16)
#     plt.tick_params(axis='both', which='major', labelsize=20)
#     plt.xticks(xtick_values)
#     plt.grid(True)
#     plt.savefig(f'missed_SLA_varyingQ_n_ev{n_ev}.pdf', dpi=250, bbox_inches='tight')
#     plt.show()
#     plt.clf()
    
    
#     ## Plot 4 & 5
#     # Filter the data for the required methods
#     pcg_data = data[data['Method'] == 'PCG']
#     pcd_data = data[data['Method'] == 'PCD']
    
#     palette = sns.color_palette("mako", 4)
    
#     # Prepare the data for bar plotting
#     plot_data = pd.DataFrame({
#         'CP Queue': pd.concat([pcg_data['CP Queue'], pcg_data['CP Queue'], pcd_data['CP Queue'], pcd_data['CP Queue']]),
#         'EV Charged': pd.concat([pcg_data['Total EV charged in-net'], pcg_data['Total EV charged par-net'], 
#                                   pcd_data['Total EV charged in-net'], pcd_data['Total EV charged par-net']]),
#         'Category': ['PCG In-net'] * len(pcg_data) + ['PCG par-net'] * len(pcg_data) + 
#                     ['PCD In-net'] * len(pcd_data) + ['PCD par-net'] * len(pcd_data)
#     })
    
#     # Create the bar plot
#     plt.figure(figsize=(12, 8))
#     plt.tight_layout()
#     sns.barplot(x='CP Queue', y='EV Charged', hue='Category', data=plot_data, palette=palette)
    
#     # Customize font sizes
#     plt.xlabel(r'Charging Point Quota $q$', fontsize=22)
#     plt.ylabel('EV Charged', fontsize=22)
#     plt.title('EV Assignments', fontsize=22)
#     plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
#     plt.tick_params(axis='both', which='major', labelsize=20)
#     #plt.xticks(xtick_values)
#     plt.grid(True)
#     plt.savefig(f'EV_Assignments_varyingQ_n_ev{n_ev}.pdf', dpi=250, bbox_inches='tight')
#     plt.show()
#     plt.clf()
    
    
#     # plot charge transferred
#     palette = sns.color_palette("rocket", 4)
#     plot_data = pd.DataFrame({
#         'CP Queue': pd.concat([pcg_data['CP Queue'], pcg_data['CP Queue'], pcd_data['CP Queue'], pcd_data['CP Queue']]),
#         'EV Charged': pd.concat([pcg_data['Total charge transferred in-net'], pcg_data['Total charge transferred par-net'], 
#                                   pcd_data['Total charge transferred in-net'], pcd_data['Total charge transferred par-net']]),
#         'Category': ['PCG In-net'] * len(pcg_data) + ['PCG par-net'] * len(pcg_data) + 
#                     ['PCD In-net'] * len(pcd_data) + ['PCD par-net'] * len(pcd_data)
#     })
    
#     # Create the bar plot
#     plt.figure(figsize=(12, 8))
#     plt.tight_layout()
#     sns.barplot(x='CP Queue', y='EV Charged', hue='Category', data=plot_data, palette=palette)
    
#     # Customize font sizes
#     plt.xlabel(r'Charging Point Quota $q$', fontsize=22)
#     plt.ylabel('Total charge transferred (kWh)', fontsize=22)
#     plt.title('Transferred Charge', fontsize=22)
#     plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
#     plt.tick_params(axis='both', which='major', labelsize=20)
#     #plt.xticks(xtick_values)
#     plt.grid(True)
#     plt.savefig(f'Transferred_Charge_varyingQ_n_ev{n_ev}.pdf', dpi=250, bbox_inches='tight')
#     plt.show()
#     plt.clf()


def plot_varyingBeta(csv_file, q):
    data = pd.read_csv(csv_file)
    data = data[(data['Method'] != 'SMEVCA-D') & (data['Method'] != 'SMEVCA-G')]

    
    # markers = {
    #     #'random_elemination': 'o',
    #     'PCG': 's',
    #     'PCD': 'D',
    #     'PCL': 'o'
    # }
    
    # plt.figure(figsize=(10, 6))
    # plt.tight_layout()
    # for method, marker in markers.items():
    #     method_data = data[data['Method'] == method]
    #     sns.lineplot(data=method_data, x='Total EV', y='execution time', marker=marker, label=method)
    # plt.xlabel('Total EV', fontsize=22)
    # plt.ylabel('Execution Time (ms)', fontsize=22)
    # plt.title('Execution Time', fontsize=22)
    # plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    # plt.tick_params(axis='both', which='major', labelsize=20)
    # plt.grid(True)
    # plt.savefig(f'execution_time_q{q}.pdf', dpi=250, bbox_inches='tight')
    # plt.show()
    # plt.clf()
    
    
    # # Plot 2
    # data['Total charge transferred'] = data['Total charge transferred in-net'] + data['Total charge transferred par-net']
    
    # plt.figure(figsize=(10, 6))
    # plt.tight_layout()
    # for method, marker in markers.items():
    #     method_data = data[data['Method'] == method]
    #     sns.lineplot(data=method_data, x='Total EV', y='Total charge transferred', marker=marker, label=method)
    
    # # Customize font sizes
    # plt.xlabel('Total EV', fontsize=20)
    # plt.ylabel('Charge Transferred (kWh)', fontsize=20)
    # plt.title('Total charge transferred', fontsize=22)
    # plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    # plt.tick_params(axis='both', which='major', labelsize=20)
    # plt.grid(True)
    # plt.savefig(f'Total_Charge_Transfer_q{q}.pdf', dpi=250, bbox_inches='tight')
    # plt.show()
    # plt.clf()
    
    
    # # Plot 2 A
    # data['Total EV charged'] = data['Total EV charged in-net'] + data['Total EV charged par-net']
    
    # plt.figure(figsize=(10, 6))
    # plt.tight_layout()
    # for method, marker in markers.items():
    #     method_data = data[data['Method'] == method]
    #     sns.lineplot(data=method_data, x='Total EV', y='Total EV charged', marker=marker, label=method)
    
    # # Customize font sizes
    # plt.xlabel('Total EV', fontsize=20)
    # plt.ylabel('EV Charged', fontsize=20)
    # plt.title('Total EV Charged', fontsize=22)
    # plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    # plt.tick_params(axis='both', which='major', labelsize=20)
    # plt.grid(True)
    # plt.savefig(f'Total_EV_charged_q{q}.pdf', dpi=250, bbox_inches='tight')
    # plt.show()
    # plt.clf()
    
    
    # ## Plot 3
    # # data2 = data[data['Method'] !='random_elemination']
    # data['total SLA missed'] = data['Total SLA breach'] + data['unmatched EV']
    # plt.figure(figsize=(10, 6))
    # plt.tight_layout()
    # for method, marker in markers.items():
    #     # if method=='random_elemination':
    #     #     continue
    #     method_data = data[data['Method'] == method]
    #     sns.lineplot(data=method_data, x='Total EV', y='total SLA missed', marker=marker, label=method)
    
    # # Customize font sizes
    # plt.xlabel('Total EV', fontsize=22)
    # plt.ylabel('Unassigned EVs', fontsize=22)
    # plt.title('SLA constraint Analysis', fontsize=22)
    # plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    # plt.tick_params(axis='both', which='major', labelsize=20)
    # plt.grid(True)
    # plt.savefig(f'Unassigned_EV_q{q}.pdf', dpi=250, bbox_inches='tight')
    # plt.show()
    # plt.clf()
    
    
    # ## Plot total cost
    # # data2 = data[data['Method'] !='random_elemination']
    # plt.figure(figsize=(10, 6))
    # plt.tight_layout()
    # for method, marker in markers.items():
    #     # if method=='random_elemination':
    #     #     continue
    #     method_data = data[data['Method'] == method]
    #     sns.lineplot(data=method_data, x='Total EV', y='Total cost to vendor', marker=marker, label=method)
    
    # # Customize font sizes
    # plt.xlabel('Total EV', fontsize=22)
    # plt.ylabel('Total cost to vendor ($)', fontsize=22)
    # plt.title('Cost Analysis', fontsize=22)
    # plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    # plt.tick_params(axis='both', which='major', labelsize=20)
    # plt.grid(True)
    # plt.savefig(f'Total_cost_q{q}.pdf', dpi=250, bbox_inches='tight')
    # plt.show()
    # plt.clf()
    
    
    
    # ## Plot 4 & 5
    # # Filter the data for the required methods
    pcg_data = data[data['Method'] == 'PCG']
    pcd_data = data[data['Method'] == 'PCD']
    pcl_data = data[data['Method'] == 'PCL']
    
    
    
    ## Plot avg cost per kWh
    # palette = sns.cubehelix_palette(n_colors=4, start=.75, rot=-.5)
    # palette = sns.dark_palette("#69d", n_colors=4)
    palette = sns.color_palette("rocket", 3)
    plot_data = pd.DataFrame({
        'Beta': pd.concat([pcg_data['Beta'], pcd_data['Beta'], pcl_data['Beta']]),
        'Avg. cost per kWh charging': pd.concat([pcg_data['Avg. cost'], pcd_data['Avg. cost'],
                                                 pcl_data['Avg. cost']]),
        'Category': ['PCG'] * len(pcg_data) + ['PCD'] * len(pcd_data) + ['PCL'] * len(pcl_data)
    })
    
    # Create the bar plot
    plt.figure(figsize=(12, 8))
    plt.tight_layout()
    sns.barplot(x='Beta', y='Avg. cost per kWh charging', hue='Category', data=plot_data, palette=palette)
    
    # Customize font sizes
    plt.xlabel(r'$(\beta_1,\beta_2)$', fontsize=22)
    plt.ylabel('Avg. cost per EV charging ($)', fontsize=22)
    plt.title('Avg. cost', fontsize=22)
    plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'Beta_avgCost_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    ## Plot avg cost per kWh
    #palette = sns.cubehelix_palette(n_colors=4, start=.75, rot=-.5)
    # palette = sns.dark_palette("#008080", n_colors=4)  ##FFA500
    palette = sns.color_palette("rocket", 4)
    plot_data = pd.DataFrame({
        'Beta': pd.concat([pcg_data['Beta'], pcd_data['Beta'], pcl_data['Beta']]),
        'Total cost to vendor': pd.concat([pcg_data['Total cost to vendor'], pcd_data['Total cost to vendor'],
                                                 pcl_data['Total cost to vendor']]),
        'Category': ['PCG'] * len(pcg_data) + ['PCD'] * len(pcd_data) + ['PCL'] * len(pcl_data)
    })
    
    # Create the bar plot
    plt.figure(figsize=(12, 8))
    plt.tight_layout()
    sns.barplot(x='Beta', y='Total cost to vendor', hue='Category', data=plot_data, palette=palette)
    
    # Customize font sizes
    plt.xlabel(r'$(\beta_1,\beta_2)$', fontsize=22)
    plt.ylabel('Total cost for charging ($)', fontsize=22)
    plt.title('Total. cost', fontsize=22)
    plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'Beta_TotalCost_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    ## Plot avg detour
    #palette = sns.color_palette("viridis", 4)
    #palette = sns.dark_palette("#FFA500", n_colors=4)  ##FFA500
    palette = sns.color_palette("mako", 3)
    plot_data = pd.DataFrame({
        'Total EV': pd.concat([pcg_data['Beta'], pcd_data['Beta'], pcl_data['Beta']]),
        'Avg. detour distance': pd.concat([pcg_data['Avg. detour'], pcd_data['Avg. detour'],
                                           pcl_data['Avg. detour']]),
        'Category': ['PCG'] * len(pcg_data) + ['PCD'] * len(pcd_data) + ['PCL'] * len(pcl_data)
    })
    
    # Create the bar plot
    plt.figure(figsize=(12, 8))
    plt.tight_layout()
    sns.barplot(x='Total EV', y='Avg. detour distance', hue='Category', data=plot_data, palette=palette)
    
    # Customize font sizes
    plt.xlabel(r'$(\beta_1,\beta_2)$', fontsize=22)
    plt.ylabel('Avg. detour distance (mile)', fontsize=22)
    plt.title('Avg. detour', fontsize=22)
    plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'Beta_avgDetour_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    ## Plot avg cost per kWh
    #palette = sns.cubehelix_palette(n_colors=4, start=.75, rot=-.5)
    #palette = sns.dark_palette("#33FF57", n_colors=4)  ##FFA500
    palette = sns.color_palette("mako", 4)
    plot_data = pd.DataFrame({
        'Beta': pd.concat([pcg_data['Beta'], pcd_data['Beta'], pcl_data['Beta']]),
        'Total detour': pd.concat([pcg_data['Total detour'], pcd_data['Total detour'],
                                                 pcl_data['Total detour']]),
        'Category': ['PCG'] * len(pcg_data) + ['PCD'] * len(pcd_data) + ['PCL'] * len(pcl_data)
    })
    
    # Create the bar plot
    plt.figure(figsize=(12, 8))
    plt.tight_layout()
    sns.barplot(x='Beta', y='Total detour', hue='Category', data=plot_data, palette=palette)
    
    # Customize font sizes
    plt.xlabel(r'$(\beta_1,\beta_2)$', fontsize=22)
    plt.ylabel('Total detour (mile)', fontsize=22)
    plt.title('Total detour', fontsize=22)
    plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'Beta_TotalDetour_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
def plot_testNoChOrder(csv_file, q):
    data = pd.read_csv(csv_file)
    data = data[(data['Method'] != 'SMEVCA-D') & (data['Method'] != 'SMEVCA-G')]

    
    markers = {
        #'random_elemination': 'o',
        'PCG': 's',
        'PCD': 'D',
        'PCL': 'o'
    }
    
    # plt.figure(figsize=(10, 6))
    # plt.tight_layout()
    # for method, marker in markers.items():
    #     method_data = data[data['Method'] == method]
    #     sns.lineplot(data=method_data, x='Total EV', y='execution time', marker=marker, label=method)
    # plt.xlabel('Total EV', fontsize=22)
    # plt.ylabel('Execution Time (ms)', fontsize=22)
    # plt.title('Execution Time', fontsize=22)
    # plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    # plt.tick_params(axis='both', which='major', labelsize=20)
    # plt.grid(True)
    # plt.savefig(f'execution_time_q{q}.pdf', dpi=250, bbox_inches='tight')
    # plt.show()
    # plt.clf()
    
    
    # # Plot 2
    # data['Total charge transferred'] = data['Total charge transferred in-net'] + data['Total charge transferred par-net']
    
    plt.figure(figsize=(10, 6))
    plt.tight_layout()
    for method, marker in markers.items():
        method_data = data[data['Method'] == method]
        sns.lineplot(data=method_data, x='Total EV', y='Total charge transferred', marker=marker, label=method)
    
    # Customize font sizes
    plt.xlabel('Total EV', fontsize=20)
    plt.ylabel('Charge Transferred (kWh)', fontsize=20)
    plt.title('Total charge transferred', fontsize=22)
    plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'testNoChOrder_Total_Charge_Transfer_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    # # Plot 2 A
    # data['Total EV charged'] = data['Total EV charged in-net'] + data['Total EV charged par-net']
    
    plt.figure(figsize=(10, 6))
    plt.tight_layout()
    for method, marker in markers.items():
        method_data = data[data['Method'] == method]
        sns.lineplot(data=method_data, x='Total EV', y='Total EV charged', marker=marker, label=method)
    
    # Customize font sizes
    plt.xlabel('Total EV', fontsize=20)
    plt.ylabel('EV Charged', fontsize=20)
    plt.title('Total EV Charged', fontsize=22)
    plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'testNoChOrder_EV_charged_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    ## Plot 3
    # data2 = data[data['Method'] !='random_elemination']
    data['total SLA missed'] = data['Total SLA breach'] + data['unmatched EV']
    plt.figure(figsize=(10, 6))
    plt.tight_layout()
    for method, marker in markers.items():
        # if method=='random_elemination':
        #     continue
        method_data = data[data['Method'] == method]
        sns.lineplot(data=method_data, x='Total EV', y='total SLA missed', marker=marker, label=method)
    
    # Customize font sizes
    plt.xlabel('Total EV', fontsize=22)
    plt.ylabel('Unassigned EVs', fontsize=22)
    plt.title('SLA constraint Analysis', fontsize=22)
    plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'testNoChOrder_Unassigned_EV_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    ## Plot total cost
    # data2 = data[data['Method'] !='random_elemination']
    plt.figure(figsize=(10, 6))
    plt.tight_layout()
    for method, marker in markers.items():
        # if method=='random_elemination':
        #     continue
        method_data = data[data['Method'] == method]
        sns.lineplot(data=method_data, x='Total EV', y='Total cost to vendor', marker=marker, label=method)
    
    # Customize font sizes
    plt.xlabel('Total EV', fontsize=22)
    plt.ylabel('Total cost to vendor ($)', fontsize=22)
    plt.title('Cost Analysis', fontsize=22)
    plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'testNoChOrder_Total_cost_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    
    # ## Plot 4 & 5
    # # Filter the data for the required methods
    pcg_data = data[data['Method'] == 'PCG']
    pcd_data = data[data['Method'] == 'PCD']
    pcl_data = data[data['Method'] == 'PCL']
    
    
    
    # ## Plot avg cost per kWh
    # # palette = sns.cubehelix_palette(n_colors=4, start=.75, rot=-.5)
    # # palette = sns.dark_palette("#69d", n_colors=4)
    # palette = sns.color_palette("rocket", 3)
    # plot_data = pd.DataFrame({
    #     'Beta': pd.concat([pcg_data['Beta'], pcd_data['Beta'], pcl_data['Beta']]),
    #     'Avg. cost per kWh charging': pd.concat([pcg_data['Avg. cost'], pcd_data['Avg. cost'],
    #                                              pcl_data['Avg. cost']]),
    #     'Category': ['PCG'] * len(pcg_data) + ['PCD'] * len(pcd_data) + ['PCL'] * len(pcl_data)
    # })
    
    # # Create the bar plot
    # plt.figure(figsize=(12, 8))
    # plt.tight_layout()
    # sns.barplot(x='Beta', y='Avg. cost per kWh charging', hue='Category', data=plot_data, palette=palette)
    
    # # Customize font sizes
    # plt.xlabel(r'$(\beta_1,\beta_2)$', fontsize=22)
    # plt.ylabel('Avg. cost per EV charging ($)', fontsize=22)
    # plt.title('Avg. cost', fontsize=22)
    # plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
    # plt.tick_params(axis='both', which='major', labelsize=20)
    # plt.grid(True)
    # plt.savefig(f'Beta_avgCost_q{q}.pdf', dpi=250, bbox_inches='tight')
    # plt.show()
    # plt.clf()
    
    
    # ## Plot avg cost per kWh
    # #palette = sns.cubehelix_palette(n_colors=4, start=.75, rot=-.5)
    # # palette = sns.dark_palette("#008080", n_colors=4)  ##FFA500
    # palette = sns.color_palette("rocket", 4)
    # plot_data = pd.DataFrame({
    #     'Beta': pd.concat([pcg_data['Beta'], pcd_data['Beta'], pcl_data['Beta']]),
    #     'Total cost to vendor': pd.concat([pcg_data['Total cost to vendor'], pcd_data['Total cost to vendor'],
    #                                              pcl_data['Total cost to vendor']]),
    #     'Category': ['PCG'] * len(pcg_data) + ['PCD'] * len(pcd_data) + ['PCL'] * len(pcl_data)
    # })
    
    # # Create the bar plot
    # plt.figure(figsize=(12, 8))
    # plt.tight_layout()
    # sns.barplot(x='Beta', y='Total cost to vendor', hue='Category', data=plot_data, palette=palette)
    
    # # Customize font sizes
    # plt.xlabel(r'$(\beta_1,\beta_2)$', fontsize=22)
    # plt.ylabel('Total cost for charging ($)', fontsize=22)
    # plt.title('Total. cost', fontsize=22)
    # plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
    # plt.tick_params(axis='both', which='major', labelsize=20)
    # plt.grid(True)
    # plt.savefig(f'Beta_TotalCost_q{q}.pdf', dpi=250, bbox_inches='tight')
    # plt.show()
    # plt.clf()
    
    
    # ## Plot avg detour
    # #palette = sns.color_palette("viridis", 4)
    # #palette = sns.dark_palette("#FFA500", n_colors=4)  ##FFA500
    # palette = sns.color_palette("mako", 3)
    # plot_data = pd.DataFrame({
    #     'Total EV': pd.concat([pcg_data['Beta'], pcd_data['Beta'], pcl_data['Beta']]),
    #     'Avg. detour distance': pd.concat([pcg_data['Avg. detour'], pcd_data['Avg. detour'],
    #                                        pcl_data['Avg. detour']]),
    #     'Category': ['PCG'] * len(pcg_data) + ['PCD'] * len(pcd_data) + ['PCL'] * len(pcl_data)
    # })
    
    # # Create the bar plot
    # plt.figure(figsize=(12, 8))
    # plt.tight_layout()
    # sns.barplot(x='Total EV', y='Avg. detour distance', hue='Category', data=plot_data, palette=palette)
    
    # # Customize font sizes
    # plt.xlabel(r'$(\beta_1,\beta_2)$', fontsize=22)
    # plt.ylabel('Avg. detour distance (mile)', fontsize=22)
    # plt.title('Avg. detour', fontsize=22)
    # plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
    # plt.tick_params(axis='both', which='major', labelsize=20)
    # plt.grid(True)
    # plt.savefig(f'Beta_avgDetour_q{q}.pdf', dpi=250, bbox_inches='tight')
    # plt.show()
    # plt.clf()
    
    
    # ## Plot avg cost per kWh
    # #palette = sns.cubehelix_palette(n_colors=4, start=.75, rot=-.5)
    # #palette = sns.dark_palette("#33FF57", n_colors=4)  ##FFA500
    # palette = sns.color_palette("mako", 4)
    # plot_data = pd.DataFrame({
    #     'Beta': pd.concat([pcg_data['Beta'], pcd_data['Beta'], pcl_data['Beta']]),
    #     'Total detour': pd.concat([pcg_data['Total detour'], pcd_data['Total detour'],
    #                                              pcl_data['Total detour']]),
    #     'Category': ['PCG'] * len(pcg_data) + ['PCD'] * len(pcd_data) + ['PCL'] * len(pcl_data)
    # })
    
    # # Create the bar plot
    # plt.figure(figsize=(12, 8))
    # plt.tight_layout()
    # sns.barplot(x='Beta', y='Total detour', hue='Category', data=plot_data, palette=palette)
    
    # # Customize font sizes
    # plt.xlabel(r'$(\beta_1,\beta_2)$', fontsize=22)
    # plt.ylabel('Total detour (mile)', fontsize=22)
    # plt.title('Total detour', fontsize=22)
    # plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
    # plt.tick_params(axis='both', which='major', labelsize=20)
    # plt.grid(True)
    # plt.savefig(f'Beta_TotalDetour_q{q}.pdf', dpi=250, bbox_inches='tight')
    # plt.show()
    # plt.clf()
    
def plot_varyingGamma(csv_file, q):
    data = pd.read_csv(csv_file)
    data = data[(data['Method'] != 'SMEVCA-D') & (data['Method'] != 'SMEVCA-G')]

    
    markers = {
        #'random_elemination': 'o',
        'PCG': 's',
        'PCD': 'D',
        'PCL': 'o'
    }
    
    # plt.figure(figsize=(10, 6))
    # plt.tight_layout()
    # for method, marker in markers.items():
    #     method_data = data[data['Method'] == method]
    #     sns.lineplot(data=method_data, x='Total EV', y='execution time', marker=marker, label=method)
    # plt.xlabel('Total EV', fontsize=22)
    # plt.ylabel('Execution Time (ms)', fontsize=22)
    # plt.title('Execution Time', fontsize=22)
    # plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    # plt.tick_params(axis='both', which='major', labelsize=20)
    # plt.grid(True)
    # plt.savefig(f'execution_time_q{q}.pdf', dpi=250, bbox_inches='tight')
    # plt.show()
    # plt.clf()
    
    
    # # Plot 2
    data['Total charge transferred'] = data['Total charge transferred in-net'] + data['Total charge transferred par-net']
    
    plt.figure(figsize=(10, 6))
    plt.tight_layout()
    for method, marker in markers.items():
        method_data = data[data['Method'] == method]
        sns.lineplot(data=method_data, x='gamma upper', y='Total charge transferred', marker=marker, label=method)
    
    # Customize font sizes
    plt.xlabel(r'SLA $(\gamma)$ upper bound (min)', fontsize=20)
    plt.ylabel('Charge Transferred (kWh)', fontsize=20)
    plt.title('Total charge transferred', fontsize=22)
    plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'Gamma_Total_Charge_Transfer_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    # # Plot 2 A
    # data['Total EV charged'] = data['Total EV charged in-net'] + data['Total EV charged par-net']
    
    # plt.figure(figsize=(10, 6))
    # plt.tight_layout()
    # for method, marker in markers.items():
    #     method_data = data[data['Method'] == method]
    #     sns.lineplot(data=method_data, x='Total EV', y='Total EV charged', marker=marker, label=method)
    
    # # Customize font sizes
    # plt.xlabel('Total EV', fontsize=20)
    # plt.ylabel('EV Charged', fontsize=20)
    # plt.title('Total EV Charged', fontsize=22)
    # plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    # plt.tick_params(axis='both', which='major', labelsize=20)
    # plt.grid(True)
    # plt.savefig(f'Total_EV_charged_q{q}.pdf', dpi=250, bbox_inches='tight')
    # plt.show()
    # plt.clf()
    
    
    # ## Plot 3
    # # data2 = data[data['Method'] !='random_elemination']
    data['total SLA missed'] = data['Total SLA breach'] + data['unmatched EV']
    plt.figure(figsize=(10, 6))
    plt.tight_layout()
    for method, marker in markers.items():
        # if method=='random_elemination':
        #     continue
        method_data = data[data['Method'] == method]
        sns.lineplot(data=method_data, x='gamma upper', y='total SLA missed', marker=marker, label=method)
    
    # Customize font sizes
    plt.xlabel(r'SLA $(\gamma)$ upper bound (min)', fontsize=22)
    plt.ylabel('Unassigned EVs', fontsize=22)
    plt.title('SLA constraint Analysis', fontsize=22)
    plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'Gamma_Unassigned_EV_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    # ## Plot total cost
    # # data2 = data[data['Method'] !='random_elemination']
    # plt.figure(figsize=(10, 6))
    # plt.tight_layout()
    # for method, marker in markers.items():
    #     # if method=='random_elemination':
    #     #     continue
    #     method_data = data[data['Method'] == method]
    #     sns.lineplot(data=method_data, x='Total EV', y='Total cost to vendor', marker=marker, label=method)
    
    # # Customize font sizes
    # plt.xlabel('Total EV', fontsize=22)
    # plt.ylabel('Total cost to vendor ($)', fontsize=22)
    # plt.title('Cost Analysis', fontsize=22)
    # plt.legend(title='Methods', fontsize=15, title_fontsize=16)
    # plt.tick_params(axis='both', which='major', labelsize=20)
    # plt.grid(True)
    # plt.savefig(f'Total_cost_q{q}.pdf', dpi=250, bbox_inches='tight')
    # plt.show()
    # plt.clf()
    
    
    
    # ## Plot 4 & 5
    # # Filter the data for the required methods
    data['Total EV charged'] = data['Total EV charged in-net'] + data['Total EV charged par-net']
    pcg_data = data[data['Method'] == 'PCG']
    pcd_data = data[data['Method'] == 'PCD']
    pcl_data = data[data['Method'] == 'PCL']
    
    
    
    ## Plot avg cost per kWh
    # palette = sns.cubehelix_palette(n_colors=4, start=.75, rot=-.5)
    # palette = sns.dark_palette("#69d", n_colors=4)
    palette = sns.color_palette("viridis", 3)
    plot_data = pd.DataFrame({
        'SLA': pd.concat([pcg_data['gamma upper'], pcd_data['gamma upper'], pcl_data['gamma upper']]),
        'Total EV charged': pd.concat([pcg_data['Total EV charged'], pcd_data['Total EV charged'],
                                                 pcl_data['Total EV charged']]),
        'Category': ['PCG'] * len(pcg_data) + ['PCD'] * len(pcd_data) + ['PCL'] * len(pcl_data)
    })
    
    # Create the bar plot
    plt.figure(figsize=(12, 8))
    plt.tight_layout()
    sns.barplot(x='SLA', y='Total EV charged', hue='Category', data=plot_data, palette=palette)
    
    # Customize font sizes
    plt.xlabel(r'SLA $(\gamma)$ upper bound (min)', fontsize=22)
    plt.ylabel('Total EV charged', fontsize=22)
    plt.title('EV charged', fontsize=22)
    plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'Gamma_Total EV charged_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    
    ## Plot avg cost per kWh
    # palette = sns.cubehelix_palette(n_colors=4, start=.75, rot=-.5)
    # palette = sns.dark_palette("#69d", n_colors=4)
    palette = sns.color_palette("rocket", 3)
    plot_data = pd.DataFrame({
        'SLA': pd.concat([pcg_data['gamma upper'], pcd_data['gamma upper'], pcl_data['gamma upper']]),
        'Avg. cost per kWh charging': pd.concat([pcg_data['Avg. cost'], pcd_data['Avg. cost'],
                                                 pcl_data['Avg. cost']]),
        'Category': ['PCG'] * len(pcg_data) + ['PCD'] * len(pcd_data) + ['PCL'] * len(pcl_data)
    })
    
    # Create the bar plot
    plt.figure(figsize=(12, 8))
    plt.tight_layout()
    sns.barplot(x='SLA', y='Avg. cost per kWh charging', hue='Category', data=plot_data, palette=palette)
    
    # Customize font sizes
    plt.xlabel(r'SLA $(\gamma)$ upper bound (min)', fontsize=22)
    plt.ylabel('Avg. cost per EV charging ($)', fontsize=22)
    plt.title('Avg. cost', fontsize=22)
    plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'Gamma_avgCost_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    # ## Plot avg cost per kWh
    # #palette = sns.cubehelix_palette(n_colors=4, start=.75, rot=-.5)
    # # palette = sns.dark_palette("#008080", n_colors=4)  ##FFA500
    # palette = sns.color_palette("rocket", 4)
    # plot_data = pd.DataFrame({
    #     'Beta': pd.concat([pcg_data['Beta'], pcd_data['Beta'], pcl_data['Beta']]),
    #     'Total cost to vendor': pd.concat([pcg_data['Total cost to vendor'], pcd_data['Total cost to vendor'],
    #                                              pcl_data['Total cost to vendor']]),
    #     'Category': ['PCG'] * len(pcg_data) + ['PCD'] * len(pcd_data) + ['PCL'] * len(pcl_data)
    # })
    
    # # Create the bar plot
    # plt.figure(figsize=(12, 8))
    # plt.tight_layout()
    # sns.barplot(x='Beta', y='Total cost to vendor', hue='Category', data=plot_data, palette=palette)
    
    # # Customize font sizes
    # plt.xlabel(r'$(\beta_1,\beta_2)$', fontsize=22)
    # plt.ylabel('Total cost for charging ($)', fontsize=22)
    # plt.title('Total. cost', fontsize=22)
    # plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
    # plt.tick_params(axis='both', which='major', labelsize=20)
    # plt.grid(True)
    # plt.savefig(f'Gamma_TotalCost_q{q}.pdf', dpi=250, bbox_inches='tight')
    # plt.show()
    # plt.clf()
    
    
    ## Plot avg detour
    #palette = sns.color_palette("viridis", 4)
    #palette = sns.dark_palette("#FFA500", n_colors=4)  ##FFA500
    palette = sns.color_palette("mako", 3)
    plot_data = pd.DataFrame({
        'SLA': pd.concat([pcg_data['gamma upper'], pcd_data['gamma upper'], pcl_data['gamma upper']]),
        'Avg. detour distance': pd.concat([pcg_data['Avg. detour'], pcd_data['Avg. detour'],
                                           pcl_data['Avg. detour']]),
        'Category': ['PCG'] * len(pcg_data) + ['PCD'] * len(pcd_data) + ['PCL'] * len(pcl_data)
    })
    
    # Create the bar plot
    plt.figure(figsize=(12, 8))
    plt.tight_layout()
    sns.barplot(x='SLA', y='Avg. detour distance', hue='Category', data=plot_data, palette=palette)
    
    # Customize font sizes
    plt.xlabel(r'SLA $(\gamma)$ upper bound (min)', fontsize=22)
    plt.ylabel('Avg. detour distance (mile)', fontsize=22)
    plt.title('Avg. detour', fontsize=22)
    plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
    plt.tick_params(axis='both', which='major', labelsize=20)
    plt.grid(True)
    plt.savefig(f'Gamma_avgDetour_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    
    
    # ## Plot avg cost per kWh
    # #palette = sns.cubehelix_palette(n_colors=4, start=.75, rot=-.5)
    # #palette = sns.dark_palette("#33FF57", n_colors=4)  ##FFA500
    # palette = sns.color_palette("mako", 4)
    # plot_data = pd.DataFrame({
    #     'Beta': pd.concat([pcg_data['Beta'], pcd_data['Beta'], pcl_data['Beta']]),
    #     'Total detour': pd.concat([pcg_data['Total detour'], pcd_data['Total detour'],
    #                                              pcl_data['Total detour']]),
    #     'Category': ['PCG'] * len(pcg_data) + ['PCD'] * len(pcd_data) + ['PCL'] * len(pcl_data)
    # })
    
    # # Create the bar plot
    # plt.figure(figsize=(12, 8))
    # plt.tight_layout()
    # sns.barplot(x='Beta', y='Total detour', hue='Category', data=plot_data, palette=palette)
    
    # # Customize font sizes
    # plt.xlabel(r'$(\beta_1,\beta_2)$', fontsize=22)
    # plt.ylabel('Total detour (mile)', fontsize=22)
    # plt.title('Total detour', fontsize=22)
    # plt.legend(title='Category', fontsize=16, title_fontsize=22, loc='lower right', ncol=4)
    # plt.tick_params(axis='both', which='major', labelsize=20)
    # plt.grid(True)
    # plt.savefig(f'Gamma_TotalDetour_q{q}.pdf', dpi=250, bbox_inches='tight')
    # plt.show()
    # plt.clf()

# # Test
# if __name__ == "__main__":
#     csv_file = 'results_varying_EV_4.csv'
#     plot_varyingEV(csv_file, 2)

# # Test
# if __name__ == "__main__":
#     csv_file = 'results_varying_Q_2.csv'
#     plot_varyingQ(csv_file, 45)


# if __name__ == "__main__":
#     csv_file = 'results_varying_beta.csv'
#     plot_varyingBeta(csv_file, 2)

# if __name__ == "__main__":
#     csv_file = 'results_NoChOrder_varying_EV_4.csv'
#     plot_testNoChOrder(csv_file, 2)

if __name__ == "__main__":
    csv_file = 'results_varying_gamma.csv'
    plot_varyingGamma(csv_file, 2)

