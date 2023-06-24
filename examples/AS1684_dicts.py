# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 15:19:49 2021

@author: uqjgatta
"""

#Referenced documents: AS 1720.3:2016 and AS1720.1:2010

#Method Definitions
def timber_types():
    t = ['Seasoned_timber','Unseasoned_timber']
    return t

# def timber_grades():
#     g = ['F5', 'F7', 'F8', 'MGP10', 'MGP12', 'MGP15']
#     return g
    
def locations_latitudes():
    '''Clause 2.4.3, AS1720.1:2010'''
    l = ['Queensland_&_North_of_25˚S','Queensland_&_South_of_25˚S','Other_Regions_of_Australia_&_North_of_16˚S',
         'Other_Regions_of_Australia_&_North_of_16˚S',
         'Other_Regions_of_Australia_&_South_of_16˚S']
    return l

def wind_classfications():
    '''Table 3.2.3.2(B), AS1720.3:2016'''
    w = ['N1','N2','N3','N4','C1','C2','C3']
    return w

def roof_types():
    r = ['sheet','tile']
    return r 

def axial_dead_loads_lookup(roof_type):     
    '''Table 3.2.2.2(A), AS1720.3:2016'''
    dls = {'sheet': 0.4, 'tile': 0.9}
    return dls[roof_type]

def Cptr_inwards_pressure_lookup(wind_classfication):     
    '''Table 3.2.2.2(D), AS1720.3:2016'''
    T_3_2_2_2_D_1={
    'N1':0.63,
    'N2':0.63,
    'N3':0.63,
    'N4':0.63,
    'C1':0.95,
    'C2':0.95,
    'C3':0.95
     }
    return T_3_2_2_2_D_1[wind_classfication]

def Cptr_outwards_pressure_lookup(wind_classfication):     
    '''Table 3.2.2.2(D), AS1720.3:2016'''
    T_3_2_2_2_D_2={
    'N1':-0.99,
    'N2':-0.99,
    'N3':-0.99,
    'N4':-0.99,
    'C1':-1.44,
    'C2':-1.44,
    'C3':-1.44
     }
    return T_3_2_2_2_D_2[wind_classfication]

def Cptr_inwards_pressure_plate_lookup(wind_classfication):     
    '''Table 3.3.2.2(D), AS1720.3:2016'''
    T_3_3_2_2_D_1={
    'N1':0.63,
    'N2':0.63,
    'N3':0.63,
    'N4':0.63,
    'C1':0.95,
    'C2':0.95,
    'C3':0.95
     }
    return T_3_3_2_2_D_1[wind_classfication]

def Cptr_outwards_pressure_plate_lookup(wind_classfication):     
    '''Table 3.3.2.2(D), AS1720.3:2016'''
    T_3_3_2_2_D_2={
    'N1':-1.0,
    'N2':-1.0,
    'N3':-1.0,
    'N4':-1.0,
    'C1':-1.44,
    'C2':-1.44,
    'C3':-1.44
     }
    return T_3_3_2_2_D_2[wind_classfication]

def Cptw_lookup(wind_classfication):     
    '''Table 3.2.2.2(D), AS1720.3:2016'''
    T3_2_2_2_D_3 = {
    'N1':0.9,
    'N2':0.9,
    'N3':0.9,
    'N4':0.9,
    'C1':1.2,
    'C2':1.2,
    'C3':1.2
     }
    return T3_2_2_2_D_3[wind_classfication]

def Cptws_lookup(wind_classfication):     
    '''Table 3.2.3.2(B), AS1720.3:2016'''
    T3_2_3_2_B = {
    'N1':0.9,
    'N2':0.9,
    'N3':0.9,
    'N4':0.9,
    'C1':0.9,
    'C2':0.9,
    'C3':0.9
     }
    return T3_2_3_2_B[wind_classfication]


def q_u_lookup(wind_classfication):     
    '''Table A2, AS1720.3:2016'''
    #Return dictionary with free stream dynamic gust pressure under ultimate limit state.
    T_A2_1={
    'N1':0.69,
    'N2':0.96,
    'N3':1.5,
    'N4':2.23,
    'C1':1.5,
    'C2':2.23,
    'C3':3.29
    }
    return T_A2_1[wind_classfication]

def q_s_lookup(wind_classfication):     
    '''Table A2, AS1720.3:2016'''
    #Return dictionary with free stream dynamic gust pressure under serviceability limit state.
    T_A2_1s={
    'N1':0.41,
    'N2':0.41,
    'N3':0.61,
    'N4':0.91,
    'C1':0.61,
    'C2':0.91,
    'C3':1.33
    }
    return T_A2_1s[wind_classfication]


def g13_lookup(L):
    '''Clause 3.2.2.4(d)(ii), AS1720.3:2016'''
    if L <= 2400:
        return 0.75
    if L >= 4200:
        return 1.0
    if 4200 >= L >= 2400:
        return (0.139*L/1000)+0.417

def c(L):    
    '''Table 3.2.2.3, AS1720.3:2016'''
    if L <= 2.4:
        return 0.07
    elif L >= 4.2:
        return 0.125
    elif 4.2 > L > 2.4:
        return (0.0306*L-0.003)
    
def c_serv(L):
    '''Table 3.2.3.3, AS1720.3:2016'''
    if L <= 2.4:
        return 0.0042
    elif L >= 4.2:
        return 0.013
    elif 4.2 > L > 2.4:
        return (0.0049*L-0.0076)
    
def k1_lookup(LC):    
    '''Table 3.2.2.4, AS1720.3:2016'''
    k1_dict={
        'LC1': 0.57,
        'LC2': 0.80,
        'LC3': 0.94,
        'LC4': 1.00,
        'LC5': 1.00
        }
    return k1_dict[LC]

def r_lookup(LC):    
    d={
        'LC1': 0.25,
        'LC2': 0.25,
        'LC3': 0.25,
        'LC4': 0.25,
        'LC5': 1.00
        }
    return d[LC]

def k4_category_4_dim(width):     #Table 2.5, AS1720.1:2010 *Unseasoned timber
    if width <= 38:
        return 1.15
    elif width <= 50:
        return 1.10
    elif width <= 75:
        return 1.05
    else:
        return 1.0

def k4_lookup(seasoned,LC, width):     #Clause 3.2.2.4(b), AS1720.3:2016 *Unseasoned timber
    k4_category_4_dimension = k4_category_4_dim(width)
    if seasoned:
        d = {'LC1': 1, 'LC2': 1, 'LC3': 1, 'LC4': 1, 'LC5': 1}
    else: 
        d = {'LC1': 1, 'LC2': 1, 'LC3': 1, 'LC4': k4_category_4_dimension, 'LC5': k4_category_4_dimension}
    return d[LC]

def RM_loopup(roof_types):
    T_3_3_2_2_A_1={
        'sheet': 40,
        'tile': 90
        }
    return T_3_3_2_2_A_1[roof_types]

def timber_factors():
    factor_dict = {
        'k1': 1.0, #override for each LC
        'k4': 1.0, #seasoned
        'k6': 1.0, #temperature factor
        #'k9': 1, #not implemented yet - for bending
        'S': 0,
        'g13': 1,
        'k12': 1,
        'pc': 1, #override for each LC
        'pb': 1, #override for each LC
        }
    return factor_dict    



def wall_frame_design_load_cases_axial(G, Q1, Q2, Q3, Wua_compression, Wua_tension) -> tuple:
    
    '''Table 3.2.2.3, AS 1720.3:2016'''
    #Design action for load case 1.
    P1_1 = 1.35 * G

    P2_1 = (1.2 * G) + (1.5 * Q1)
    P2_1_ratio = (1.5 * Q1) / P2_1

    #Design action for load case 2.
    P1_2 = (1.2 * G) + (1.5 * Q3)
    P1_2_ratio =  (1.5 * Q3)/ P1_2
    
    #Design action for load case 3.
    P1_3 = (1.2 * G) + (1.5 * Q2)
    P1_3_ratio = 0 if P1_3 == 0 else (1.5 * Q2) / P1_3

    #Design action for load case 4 (down) and 5 (up)         
    P1_4 = (1.2 * G) + Wua_compression + Q1
    P1_4_ratio = ( Wua_compression + Q1) / P1_4
    
    P2_4 = (0.9 * G) + Wua_tension 
    P2_4_ratio = 0 if P2_4 == 0 else (Wua_tension) / P2_4
    P3_4 = (1.2 * G) + Q1

    Nc_LC1 = max(P1_1,P2_1)
    Nc_LC2 = P1_2
    Nc_LC3 = P1_3
    Nc_LC4 = max(P1_4,P3_4) #downwards   
    Nc_LC5 = min(0,P2_4) #upwards, negative

    P_star_LC = [Nc_LC1, Nc_LC2, Nc_LC3, Nc_LC4, Nc_LC5]
    P_star_ratios = [P2_1_ratio, P1_2_ratio, P1_3_ratio, P1_4_ratio, P2_4_ratio]
    return (P_star_LC, P_star_ratios)

def wall_frame_design_load_cases_flexural(Wuw, L):
    M_LC1 = 0
    M_LC2 = 0 
    M_LC3 = 0
    M_LC4 = c(L) * Wuw * L**2
    M_LC5 = c(L) * Wuw * L**2
    
    M_star_LC = [M_LC1, M_LC2, M_LC3, M_LC4, M_LC5]
    return M_star_LC

def wall_frame_design_load_cases_serv(Wsw, L) -> list:
    '''
    returns delta_EI factor in kN m^3

    '''
    delta_EI = c_serv(L) * Wsw * (L*1000)**4
    
    return [delta_EI]

