# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 15:56:38 2024

@author: Arindam
"""
from agents import CP, EV, compute_manhattan_distance
from typing import List, Dict, Tuple
import time

def time_function_call(func, *args, **kwargs):
    start_time = time.time()
    matched_s, matched_c = func(*args, **kwargs)
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000
    return elapsed_time, matched_s, matched_c

def noChargingOrder_analysis(cp_list: List[CP], ev_list:List[EV], matched_c: Dict[int, List[Tuple[int, int, float, int]]]):
    """

    Parameters
    ----------
    cp_list : List[CP]
    matched_c : Dict[int, List[Tuple[int, int, float, int]]]
        key is CP ID. Each value is list of tuples (s_i, t1_ij, psi_ij, delta_ij) 
    Returns
    -------

    """
    total_ct = 0 # total charge transferred
    total_s = 0 # total EV charged in-net
    total_SLA_breach = 0
    total_cost_to_vendor = 0
    total_detour = 0
    
    for cp_ in cp_list:
        c_id = cp_.ID
        total_ct_at_c = 0 # total charge transfer at c_id
        A_c = matched_c[c_id]  # matched_c has tuple (s_i, t1_ij, psi_ij, delta_ij) 
        
        
        min_delta = 9999
        total_charging_time = 0
        for s in A_c:
            min_delta_temp = min_delta
            delta = s[3]
            if delta < min_delta_temp:
                min_delta_temp = delta
            total_charging_time_temp = total_charging_time + s[1]
            Delta_r = min_delta_temp - total_charging_time_temp
            if Delta_r >= 0:
                if min_delta_temp < min_delta:
                    min_delta = min_delta_temp
                    total_charging_time = total_charging_time_temp
                total_s = total_s + 1
                total_ct = total_ct + s[2] # s[2] = psi_ij
                total_ct_at_c = total_ct_at_c + s[2] # s[2] = psi_ij
                ev_ = ev_list[s[0]] # s[0] = s_i
                detour = compute_manhattan_distance(ev_.x_loc, ev_.y_loc, cp_.x_loc, cp_.y_loc)
                total_detour = total_detour + detour
            if Delta_r < 0:
                total_SLA_breach = total_SLA_breach + 1
                
        total_cost_to_vendor = total_cost_to_vendor + total_ct_at_c * cp_.ucost
                    
    total_ev_charged = total_s
    avg_cost = total_cost_to_vendor/total_ev_charged
    avg_detour = total_detour/total_ev_charged
    
    return (total_ev_charged, total_ct, total_SLA_breach, total_cost_to_vendor, total_detour, avg_cost, avg_detour)
    
    
        
        
    

def charging_analysis(cp_list: List[CP], ev_list:List[EV], matched_c: Dict[int, List[Tuple[int, int, float, int]]]):
    """

    Parameters
    ----------
    cp_list : List[CP]
    matched_c : Dict[int, List[Tuple[int, int, float, int]]]
        key is CP ID. Each value is list of tuples (s_i, t1_ij, psi_ij, delta_ij) 
    Returns
    -------

    """
    innet_cp = [] # in-network CP
    outnet_cp = [] # par-network CP
    total_ct_in = 0 # total in-net charge transferred
    wait_time_list = [] # wait time list for all in-net EV 
    total_s = 0 # total EV charged in-net
    total_SLA_breach = 0
    total_cost_to_vendor = 0
    total_detour = 0
    
    for c in cp_list:
        if c.eta == 0:
            innet_cp.append(c.ID)
        else:
            outnet_cp.append(c.ID)
    for c_id in innet_cp:
        cp_ = cp_list[c_id] 
        total_ct_at_c = 0 # total charge transfer at c_id
        t_w_c_id = 0 # total wait time at c_id
        A_c = matched_c[c_id]  # matched_c has tuple (s_i, t1_ij, psi_ij, delta_ij) 
        total_s = total_s + len(A_c)
        for s in A_c:
            t1_ij = s[1] # charging time
            wait_time_list.append(t_w_c_id)
            if t_w_c_id + t1_ij > s[3]: # s[3] = delta_ij
                total_SLA_breach = total_SLA_breach + 1
            total_ct_in = total_ct_in + s[2] # s[2] = psi_ij
            total_ct_at_c = total_ct_at_c + s[2] # s[2] = psi_ij
            t_w_c_id = t_w_c_id + t1_ij # wait time for the next EV in the queue
            ev_ = ev_list[s[0]] # s[0] = s_i
            detour = compute_manhattan_distance(ev_.x_loc, ev_.y_loc, cp_.x_loc, cp_.y_loc)
            total_detour = total_detour + detour
        total_cost_to_vendor = total_cost_to_vendor + total_ct_at_c * cp_.ucost
    
    total_s_out = 0
    wait_time_list_out = [] # wait time list for all in-net EV        
    total_ct_out = 0
    for c_id in outnet_cp:
        cp_ = cp_list[c_id] 
        total_ct_at_c = 0 # total charge transfer at c_id
        t_w_c_id = 0 # total wait time at c_id
        A_c = matched_c[c_id]
        total_s_out = total_s_out + len(A_c)
        for s in A_c:
            t1_ij = s[1] # charging time
            wait_time_list_out.append(t_w_c_id)
            if t_w_c_id + t1_ij > s[3]:
                total_SLA_breach = total_SLA_breach + 1
            total_ct_out = total_ct_out + s[2] # s[2] = psi_ij
            total_ct_at_c = total_ct_at_c + s[2] # s[2] = psi_ij
            t_w_c_id = t_w_c_id + t1_ij # wait time for the next EV in the queue
            ev_ = ev_list[s[0]] # s[0] = s_i
            detour = compute_manhattan_distance(ev_.x_loc, ev_.y_loc, cp_.x_loc, cp_.y_loc)
            total_detour = total_detour + detour
        total_cost_to_vendor = total_cost_to_vendor + total_ct_at_c * cp_.ucost
            
    total_ev_charged = total_s + total_s_out
    avg_cost = total_cost_to_vendor/total_ev_charged
    avg_detour = total_detour/total_ev_charged
    
    print("*** METRICS ****")
    print(":: Total in-net CP = ", len(innet_cp))
    print("Total EV charged in-net = ", total_s)
    print("Total charge transferred in-net = ", total_ct_in)
    #print("In-net wait-time list = ", wait_time_list)
    
    print(":: Total par-net CP = ", len(outnet_cp))
    print("Total EV charged par-net = ", total_s_out)
    print("Total charge transferred par-net = ", total_ct_out)
    #print("par-net wait-time list = ", wait_time_list_out)
    print("Total EV in the system = ", len(ev_list))
    print("Total SLA breach = ", total_SLA_breach)
    print("Total EV charged = ", total_ev_charged)
    print("Total cost to vendor = ", total_cost_to_vendor)
    print("Avg. cost per vehicle = ", avg_cost)
    print("Avg. detour (miles) = ", avg_detour)
    return (len(innet_cp), len(outnet_cp), total_s, total_s_out, total_ct_in, total_ct_out, total_SLA_breach, total_cost_to_vendor, total_detour, avg_cost, avg_detour)
    
def find_unmatched(matched_s):
    unmatched = 0
    for s_id in matched_s.keys():
        if matched_s[s_id] == []:
            unmatched = unmatched + 1
    return unmatched

def find_distribution_CP(matched_c: Dict[int, List[Tuple[int, int, float, int]]]):
    """

    Parameters
    ----------
    matched_c : Dict[int, List[Tuple[int, int, float, int]]]
        key is CP ID. Each value is list of tuples (s_i, t1_ij, psi_ij, delta_ij) 
    Returns
    -------

    """
    ev_assigned_per_cp = [] # list of number of EV assigned to each CP (distribution)
    charge_transferred_per_cp = [] # list of number of EV assigned to each CP (distribution)
    for c_i in matched_c.keys():
        assigned_evs_at_j = matched_c[c_i]
        ev_assigned_per_cp.append(len(assigned_evs_at_j))
        if len(assigned_evs_at_j) == 0:
            charge_transferred_per_cp.append(0)
        else:
            psi_ij = 0
            for s in assigned_evs_at_j: # s = (s_i, t1_ij, psi_ij, delta_ij) 
                psi_ij = psi_ij + s[2]
            charge_transferred_per_cp.append(psi_ij)
    return ev_assigned_per_cp, charge_transferred_per_cp
            