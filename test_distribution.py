# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 16:58:31 2024

@author: Arindam
"""
# from agents import EV, CP
from matching_at_RSU import match, randomChoice, PCG, PCD, PCL
from metric import charging_analysis, find_unmatched, find_distribution_CP
from helper import create_EVobjects, create_CPobjects, debug_print
import time
import random
# import csv
# from plot import plot_varyingQ
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

os.chdir(r"C:\Phd\CUDA test\Test\test 1\EV\ICDCN_extension\code")


time_seed = time.time()
# random.seed(time_seed)
random.seed(123)
Debug = True


if __name__ == "__main__":
    # 8 block = 1 mile (Chicago)
    # RSU radius is 2.5 mile = 20 blocks
    # The largest square that can fit in RSU area will have 20*sqrt(2) = 28.28 blocks
    # Let us consider the grid size 28 X 28
   
    # # user input
    n_ev = 30
    q_range_min = 1
    q_range_max = 5
    n_cp_in_fast = 5
    n_cp_in_regular = 10
    n_cp_out_fast = 5
    n_cp_out_regular = 10
    max_itr = 20 # maximum iteration
    csv_file = 'results_varying_Q_1.csv'
    
    
    # Initialize EVs
    ev_list = create_EVobjects(n_ev, start_id=0) # create list of EVs
    
    
    q = 2     
    
    # ## For random unit cost order uncomment it
    # In Fast CP
    start_id = 0
    ucost_lower = 0.4 # unified cost lower limit
    ucost_upper = 0.5 # unified cost upper limit
    cp_in_fast = create_CPobjects(n_cp_in_fast, start_id=start_id, theta=1, eta=0, q=q, ucost_lower=ucost_lower, ucost_upper=ucost_upper) # in-net fast charging points
    # In Regular CP
    start_id = start_id + n_cp_in_fast
    ucost_lower = 0.2 # unified cost lower limit
    ucost_upper = 0.25 # unified cost upper limit
    cp_in_regular = create_CPobjects(n_cp_in_regular, start_id=start_id, theta=0, eta=0, q=q, ucost_lower=ucost_lower, ucost_upper=ucost_upper) # in-net regular charging points
    # Out Fast CP
    start_id = start_id + n_cp_in_regular
    ucost_lower = 0.4 # unified cost lower limit
    ucost_upper = 0.5 # unified cost upper limit
    cp_out_fast = create_CPobjects(n_cp_out_fast, start_id=start_id, theta=1, eta=1, q=q, ucost_lower=ucost_lower, ucost_upper=ucost_upper) # in-net fast charging points
    # Out Regular CP
    start_id = start_id + n_cp_out_fast
    ucost_lower = 0.2 # unified cost lower limit
    ucost_upper = 0.25 # unified cost upper limit
    cp_out_regular = create_CPobjects(n_cp_out_regular, start_id=start_id, theta=0, eta=1, q=q, ucost_lower=ucost_lower, ucost_upper=ucost_upper) # in-net fast charging points
    cp_list = cp_in_fast + cp_in_regular + cp_out_fast + cp_out_regular
    
    
    
    
    # # For SMEVCA unit cost order uncomment it
    # # In Fast CP
    # start_id = 0
    # ucost_lower = 0.4 # unified cost lower limit
    # ucost_upper = 0.5 # unified cost upper limit
    # cp_in_fast = create_CPobjects(n_cp_in_fast, start_id=start_id, theta=1, eta=0, q=q, ucost_lower=ucost_lower, ucost_upper=ucost_upper) # in-net fast charging points
    # # In Regular CP
    # start_id = start_id + n_cp_in_fast
    # ucost_lower = 0.2 # unified cost lower limit
    # ucost_upper = 0.25 # unified cost upper limit
    # cp_in_regular = create_CPobjects(n_cp_in_regular, start_id=start_id, theta=0, eta=0, q=q, ucost_lower=ucost_lower, ucost_upper=ucost_upper) # in-net regular charging points
    # # Out Fast CP
    # start_id = start_id + n_cp_in_regular
    # ucost_lower = 0.7 # unified cost lower limit
    # ucost_upper = 0.8 # unified cost upper limit
    # cp_out_fast = create_CPobjects(n_cp_out_fast, start_id=start_id, theta=1, eta=1, q=q, ucost_lower=ucost_lower, ucost_upper=ucost_upper) # in-net fast charging points
    # # Out Regular CP
    # start_id = start_id + n_cp_out_fast
    # ucost_lower = 0.55 # unified cost lower limit
    # ucost_upper = 0.65 # unified cost upper limit
    # cp_out_regular = create_CPobjects(n_cp_out_regular, start_id=start_id, theta=0, eta=1, q=q, ucost_lower=ucost_lower, ucost_upper=ucost_upper) # in-net fast charging points
    # cp_list = cp_in_fast + cp_in_regular + cp_out_fast + cp_out_regular
    
    
    
    # CP ID list (required for plotting)
    cp_id_list = [i for i in range(n_cp_in_fast + n_cp_in_regular + n_cp_out_fast + n_cp_out_regular)]
    # q_in_fast = str(q) +" in-net fast"
    # q_in_reg = str(q) +" in-net regular"
    # q_par_fast = str(q) +" par-net fast"
    # q_par_reg = str(q) +" par-net regular"
    # CP_category = [q_in_fast] * n_cp_in_fast + [q_in_reg] * n_cp_in_regular + \
                # [q_par_fast] * n_cp_par_fast + [q_par_reg] * n_cp_par_regular
    CP_category = ["in-net fast"] * n_cp_in_fast + ["in-net regular"] * n_cp_in_regular + \
                 ["par-net fast"] * n_cp_out_fast + ["par-net regular"] * n_cp_out_regular

    # compute preference list for EV
    Pref = {}
    #print("Preference list of EV (CP ID, Distance d_ij, time to reach t0_ij, psi, r_i, gamma):")
    for ev in ev_list:
        ev.reset_preference()
        ev.compute_preference_new(cp_list) # New Preference ## For random unit cost order uncomment it
        Pref[ev.ID] = ev.pref
        #print(ev.ID, " => ", ev.pref)
            
            
    print("\n***Method: Random***")
    print("-----------------------------------------")
    # start_time = time.time()
    matched_s, matched_c = match(ev_list, cp_list, Pref, randomChoice)
    ev_assigned_per_cp_rand, charge_transferred_per_cp_rand = find_distribution_CP(matched_c)
    print("EV distribution across the CPs:")
    print(ev_assigned_per_cp_rand)
    print("Charge transfer task aistribution across the CPs:")
    print(charge_transferred_per_cp_rand)
            
    print("\n***Method: PCG***")
    print("-----------------------------------------")
    matched_s, matched_c = match(ev_list, cp_list, Pref, PCG)
    ev_assigned_per_cp_PCG, charge_transferred_per_cp_PCG = find_distribution_CP(matched_c)
    print("EV distribution across the CPs:")
    print(ev_assigned_per_cp_PCG)
    print("Charge transfer task aistribution across the CPs:")
    print(charge_transferred_per_cp_PCG)
    
    print("\n***Method: PCD***")
    print("-----------------------------------------")
    matched_s, matched_c = match(ev_list, cp_list, Pref, PCD)
    ev_assigned_per_cp_PCD, charge_transferred_per_cp_PCD = find_distribution_CP(matched_c)
    print("EV distribution across the CPs:")
    print(ev_assigned_per_cp_PCD)
    print("Charge transfer task aistribution across the CPs:")
    print(charge_transferred_per_cp_PCD)
    
    
    print("\n***Method: PCL***")
    print("-----------------------------------------")
    matched_s, matched_c = match(ev_list, cp_list, Pref, PCL)
    ev_assigned_per_cp_PCL, charge_transferred_per_cp_PCL = find_distribution_CP(matched_c)
    
    
    
    
    data1 = pd.DataFrame({
        'ID': cp_id_list * 3,
        'Value': charge_transferred_per_cp_PCG + charge_transferred_per_cp_PCD + charge_transferred_per_cp_PCL,
        'Category': [category + " (PCG)" for category in CP_category] +
            [category + " (PCD)" for category in CP_category] + [category + " (PCL)" for category in CP_category]
    })
    
    # palette = sns.color_palette("rocket")
    data2 = pd.DataFrame({
        'ID': cp_id_list * 3,
        'Value': ev_assigned_per_cp_PCG + ev_assigned_per_cp_PCD + ev_assigned_per_cp_PCL,
        'Category': [category + " (PCG)" for category in CP_category] +
            [category + " (PCD)" for category in CP_category] + [category + " (PCL)" for category in CP_category]
    })
    ytick_values = data2['Value'].unique()
    
    
    
    
    
    
    
    # Create a figure with 2 subplots (side by side)
    fig, axes = plt.subplots(1, 2, figsize=(35, 5), sharey=False)
    
    # ---- First Bar Plot ----
    bar1 = sns.barplot(ax=axes[0], x='ID', y='Value', hue='Category', data=data1, palette="tab20")
    for patch in axes[0].patches:
        patch.set_width(0.3)  # Adjusting bar width for data1
    
    axes[0].set_xlabel('Charging Point ID', fontsize=24)
    axes[0].set_ylabel('Charge Transfer (kWh)', fontsize=24)
    axes[0].tick_params(axis='both', which='major', labelsize=20)
    axes[0].grid(True)
    
    # ---- Second Bar Plot ----
    bar2 = sns.barplot(ax=axes[1], x='ID', y='Value', hue='Category', data=data2, palette="tab20")
    for patch in axes[1].patches:
        patch.set_width(0.3)  # Adjusting bar width for data2
    
    axes[1].set_xlabel('Charging Point ID', fontsize=24)
    axes[1].set_ylabel('Number of EVs', fontsize=24)
    axes[1].tick_params(axis='both', which='major', labelsize=20)
    axes[1].set_yticks(ytick_values)  # Set y-ticks for the second plot
    axes[1].grid(True)
    
    # ---- Remove Individual Legends from Both Plots ----
    axes[0].legend_.remove()  # Remove the first subplot's legend
    axes[1].legend_.remove()  # Remove the second subplot's legend
    
    # # ---- Create a Single Legend Below Both Plots ----
    # handles, labels = bar1.get_legend_handles_labels()  # Get legend from the first plot only
    # fig.legend(handles, labels, title='Category', fontsize=20, title_fontsize=24, 
    #             loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=6)
    
    # # uncomment for SMEVCA order
    # plt.subplots_adjust(bottom=0.2)  # Extra space for legend below
    # plt.savefig(f'SMEVCAOrder_Comparison_n_ev{n_ev}_q{q}.pdf', dpi=250, bbox_inches='tight')
    # plt.show()
    # plt.clf()
    
    
    # uncomment for random order
    plt.subplots_adjust(bottom=0.2)  # Extra space for legend below
    plt.savefig(f'RandomOrder_Comparison_n_ev{n_ev}_q{q}.pdf', dpi=250, bbox_inches='tight')
    plt.show()
    plt.clf()
    