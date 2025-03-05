# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 11:56:43 2024

@author: Arindam

# 8 block = 1 mile (Chicago)
# RSU radius is 2.5 mile = 20 blocks
# The largest square that can fit in RSU area will have 20*sqrt(2) = 28.28 blocks
# Let us consider the grid size 28 X 28
"""

from agents import EV, CP
import random

random.seed(123)



# 8 block = 1 mile (Chicago)
# RSU radius is 1.5 mile = 12 blocks
# The largest square that can fit in RSU area will have 12*sqrt(2) = 16.97 blocks
# Let us consider the grid size 16 X 16

def create_EVobjects(n_ev, start_id):
    ev_list = []
    for s_i in range(start_id, start_id + n_ev):
        x_loc = random.randint(0,16)
        y_loc = random.randint(0,16)
        ev = EV(s_i, x_loc, y_loc)
        ev_list.append(ev)
    return ev_list


def create_CPobjects(n_cp, start_id, theta, eta, q, ucost_lower, ucost_upper):
    cp_list = []
    for c_i in range(start_id, start_id + n_cp):
        x_loc = random.randint(0,16)
        y_loc = random.randint(0,16)
        # theta = random.randint(0,1)
        # eta = random.randint(0,1)
        ucost = random.uniform(ucost_lower, ucost_upper)
        cp = CP(ID=c_i, x_loc=x_loc, y_loc=y_loc, theta=theta, eta=eta, ucost=ucost, q=q)
        cp_list.append(cp)
    return cp_list

def debug_print(Debug, message):
    if Debug:
        print(message)