# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 14:28:57 2024

@author: Arindam
"""
# from agents import EV, CP
from matching_at_RSU import match, randomChoice, PCG, PCD, PCL
from metric import charging_analysis, find_unmatched
from helper import create_EVobjects, create_CPobjects, debug_print
import time
import random
import csv
from plot import plot_varyingBeta
import os

os.chdir(r"C:\Phd\CUDA test\Test\test 1\EV\ICDCN_extension\code")


time_seed = time.time()
#random.seed(time_seed)
random.seed(123)
Debug = False


if __name__ == "__main__":
    # 8 block = 1 mile (Chicago)
    # RSU radius is 2.5 mile = 20 blocks
    # The largest square that can fit in RSU area will have 20*sqrt(2) = 28.28 blocks
    # Let us consider the grid size 28 X 28
   
    # # user input
    n_ev_min = 30
    n_ev_max = 60
    n_cp_in_fast = 5
    n_cp_in_regular = 10
    n_cp_out_fast = 5
    n_cp_out_regular = 10
    q = 2 # quota of each CP
    max_itr = 1 # maximum iteration
    csv_file = 'results_varying_beta.csv'
    
    # Initialize Charging points (Static for the whole experiment)
    
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
    ucost_upper = 0.7 # unified cost upper limit
    cp_out_fast = create_CPobjects(n_cp_out_fast, start_id=start_id, theta=1, eta=1, q=q, ucost_lower=ucost_lower, ucost_upper=ucost_upper) # in-net fast charging points
    # Out Regular CP
    start_id = start_id + n_cp_out_fast
    ucost_lower = 0.2 # unified cost lower limit
    ucost_upper = 0.45 # unified cost upper limit
    cp_out_regular = create_CPobjects(n_cp_out_regular, start_id=start_id, theta=0, eta=1, q=q, ucost_lower=ucost_lower, ucost_upper=ucost_upper) # in-net fast charging points
    cp_list = cp_in_fast + cp_in_regular + cp_out_fast + cp_out_regular
    
    n_ev = 30
    # Initialize EVs
    ev_list = create_EVobjects(n_ev, start_id=0) # create list of EVs
    # # Print the sorted EV list
    # print(sorted_ev_list)
    # print("List of EV:")
    # print(ev_list)
    
    beta_combination = [(5,1), (1,1), (1,5)]
    
    for b1,b2 in beta_combination:
        for itr in range(max_itr):
            # Initialize EVs
            # ev_list = create_EVobjects(n_ev, start_id=0) # create list of EVs
            # # Print the sorted EV list
            # print(sorted_ev_list)
            # print("List of EV:")
            # print(ev_list)
            
            # compute preference list for EV
            Pref = {}
            #print("Preference list of EV (CP ID, Distance d_ij, time to reach t0_ij, psi, r_i, gamma):")
            for ev in ev_list:
                ev.reset_preference()
                #ev.compute_preference(cp_list) # SMEVCA preference
                ev.compute_preference_new(cp_list, beta1=b1, beta2=b2) # New Preference
                Pref[ev.ID] = ev.pref
                #print(ev.ID, " => ", ev.pref)
            
            
            # print("\n***Method: Random***")
            # print("-----------------------------------------")
            # start_time = time.time()
            # matched_s, matched_c = match(ev_list, cp_list, Pref, randomChoice)
            # end_time = time.time()
            # elapsed_time_random = (end_time - start_time) * 1000
            # results_random = charging_analysis(cp_list, ev_list, matched_c) # returns (len(innet_cp), len(outnet_cp), total_s, total_s_out, total_ct_in, total_ct_out, total_SLA_breach)
            # unmatched_random = find_unmatched(matched_s)
            # debug_print(Debug, f"Elapsed time: {elapsed_time_random} ms")
            # debug_print(Debug, "Matching for EV:")
            # debug_print(Debug, f"{matched_s}")
            # debug_print(Debug, "Matching for CP:")
            # debug_print(Debug, f"{matched_c}")
            # debug_print(Debug, f"No. of unmatched EV: {unmatched_random}")
            
            print("\n***Method: PCG***")
            print("-----------------------------------------")
            #matched_s, matched_c, elapsed_time = time_function_call(match, ev_list, cp_list, Pref, PCG)
            #print("Elapsed time: ", elapsed_time, " ms")
            start_time = time.time()
            matched_s, matched_c = match(ev_list, cp_list, Pref, PCG)
            end_time = time.time()
            elapsed_time_PCG = (end_time - start_time) * 1000
            results_PCG = charging_analysis(cp_list, ev_list, matched_c)
            unmatched_PCG = find_unmatched(matched_s)
            debug_print(Debug, f"Elapsed time: {elapsed_time_PCG} ms")
            debug_print(Debug, "Matching for EV:")
            debug_print(Debug, f"{matched_s}")
            debug_print(Debug, "Matching for CP:")
            debug_print(Debug, f"{matched_c}")
            debug_print(Debug, f"No. of unmatched EV: {unmatched_PCG}")
            
            print("\n***Method: PCD***")
            print("-----------------------------------------")
            start_time = time.time()
            matched_s, matched_c = match(ev_list, cp_list, Pref, PCD)
            end_time = time.time()
            elapsed_time_PCD = (end_time - start_time) * 1000
            results_PCD = charging_analysis(cp_list, ev_list, matched_c)
            unmatched_PCD = find_unmatched(matched_s)
            debug_print(Debug, f"Elapsed time: {elapsed_time_PCD} ms")
            debug_print(Debug, "Matching for EV:")
            debug_print(Debug, f"{matched_s}")
            debug_print(Debug, "Matching for CP:")
            debug_print(Debug, f"{matched_c}")
            debug_print(Debug, f"No. of unmatched EV: {unmatched_PCD}")
            
            
            
            print("\n***Method: PCL***")
            print("-----------------------------------------")
            start_time = time.time()
            matched_s, matched_c = match(ev_list, cp_list, Pref, PCL)
            end_time = time.time()
            elapsed_time_PCL = (end_time - start_time) * 1000
            results_PCL = charging_analysis(cp_list, ev_list, matched_c)
            unmatched_PCL = find_unmatched(matched_s)
            debug_print(Debug, f"Elapsed time: {elapsed_time_PCL} ms")
            debug_print(Debug, "Matching for EV:")
            debug_print(Debug, f"{matched_s}")
            debug_print(Debug, "Matching for CP:")
            debug_print(Debug, f"{matched_c}")
            debug_print(Debug, f"No. of unmatched EV: {unmatched_PCL}")

            
            
            
            
            file_exists = os.path.isfile(csv_file)
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
            
                # Write the header only if the file doesn't exist
                if not file_exists:
                    writer.writerow(['itr', 'Method', 'Beta', 'Total EV', 'CP Queue', 'Total in-net CP', 'Total par-net CP', 'Total EV charged in-net', 'Total EV charged par-net','Total charge transferred in-net',
                                       'Total charge transferred par-net', 'Total SLA breach', 'unmatched EV', "execution time", "Total cost to vendor", "Total detour", "Avg. cost", "Avg. detour"])
                
                # results_random = (len(innet_cp), len(outnet_cp), total_s, total_s_out, total_ct_in, total_ct_out, total_SLA_breach, total_cost_to_vendor, total_detour, avg_cost, avg_detour)
                
                #writer.writerow([itr, 'random_elemination', n_ev, q, results_random[0], results_random[1], results_random[2], results_random[3], results_random[4], results_random[5], results_random[6], unmatched_random, elapsed_time_random, results_random[7], results_random[8], results_random[9], results_random[10]])  
                
                # results_PCG = (len(innet_cp), len(outnet_cp), total_s, total_s_out, total_ct_in, total_ct_out, total_SLA_breach, total_cost_to_vendor, total_detour, avg_cost, avg_detour)
                writer.writerow([itr, 'PCG', (b1, b2) , n_ev, q, results_PCG[0], results_PCG[1], results_PCG[2], results_PCG[3], results_PCG[4], results_PCG[5], results_PCG[6], unmatched_PCG, elapsed_time_PCG, results_PCG[7], results_PCG[8], results_PCG[9], results_PCG[10]]) 
                
                # results_PCD = (len(innet_cp), len(outnet_cp), total_s, total_s_out, total_ct_in, total_ct_out, total_SLA_breach, total_cost_to_vendor, total_detour, avg_cost, avg_detour)
                writer.writerow([itr, 'PCD', (b1, b2), n_ev, q, results_PCD[0], results_PCD[1], results_PCD[2], results_PCD[3], results_PCD[4], results_PCD[5], results_PCD[6], unmatched_PCD, elapsed_time_PCD, results_PCD[7], results_PCD[8], results_PCD[9], results_PCD[10]]) 
                
                # results_PCL = (len(innet_cp), len(outnet_cp), total_s, total_s_out, total_ct_in, total_ct_out, total_SLA_breach, total_cost_to_vendor, total_detour, avg_cost, avg_detour)
                writer.writerow([itr, 'PCL', (b1, b2), n_ev, q, results_PCL[0], results_PCL[1], results_PCL[2], results_PCL[3], results_PCL[4], results_PCL[5], results_PCL[6], unmatched_PCL, elapsed_time_PCL, results_PCL[7], results_PCL[8], results_PCL[9], results_PCL[10]]) 

    
    
    
    plot_varyingBeta(csv_file, q)
    
    
  