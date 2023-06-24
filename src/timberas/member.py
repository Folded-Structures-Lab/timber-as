# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 15:19:49 2021

@author: uqjgatta
"""

from dataclasses import dataclass, field
from timberas.material import TimberMaterial
from timberas.geometry import TimberSection

#from ...examples.AS1684_dicts import g13_lookup


#Referenced documents: AS1720.1:2010 and AS1720.3:2016



@dataclass 
class TimberMember():
    sec: TimberSection = field(repr = False)
    mat: TimberMaterial = field(repr = False)
    sec_name: str = field(init = False)
    mat_name: str = field(init = False)
    
    application_cat: 1 | 2 | 3 = 1 #application category for structural member
    high_temp_latitude: bool = False
    
    n_com: int = 1
    n_mem: int = 1
    member_spacing: float = 0 #member spacing
    
    L: float = 1 #length
    L_ay: float = 0
    k1: float = 1
    r: float = 0.25 #ratio of temporary to total design action effect
    
    N_dt: float = field(init = False) #kN
    N_dc: float = field(init = False) #kN
    N_cx: float = field(init = False) #kN
    N_cy: float = field(init = False) #kN
    M_d: float = field(init = False) #kNm

    def __post_init__(self):
        self.sec_name = self.sec.sec_name
        self.mat_name = self.mat.name
        self.N_dt = self._N_dt()
        self.N_cx = self._N_cx()
        self.N_cy = self._N_cy()
        self.M_d = self._M_d()
    
    @property
    def phi(self) -> float:     
        '''Table 2.1, AS1720.1:2010'''
        return self.mat.capacity_factor(self.application_cat)
        #return capacity_factor_lookup(self.application_cat, self.mat.grade)
    
    def _N_cx(self) -> float:     
        '''Clause 3.3.1.1, AS1720.1:2010'''
        return self.phi * self.k1 * self.k4 * self.k6 * self.k12_x * self.mat.f_c * self.sec.A_g / 1000     
    
    def _N_cy(self) -> float:     
        '''Clause 3.3.1.1, AS1720.1:2010'''    
        return self.phi * self.k1 * self.k4 * self.k6 * self.k12_y * self.mat.f_c * self.sec.A_g / 1000  
     
    def _N_dt(self) -> float:     
        '''Clause 3.4.1, AS1720.1:2010'''
        return self.phi * self.k1 * self.k4 * self.k6 * self.mat.f_t * self.sec.A_g / 1000  

    def _M_d(self) -> float:     
        '''Clause 3.2.1.1, AS1720.1:2010'''
        return self.phi * self.k1 * self.k4 * self.k6 * self.k9 * self.k12_bend * self.mat.f_b * self.sec.Z_x / 1E6     

    @property
    def g_13(self) -> float:
        '''Clause 3.2.2.4(d)(ii), AS1720.3:2016'''
        return g13_lookup(self.L)
    
    @property
    def S3(self) -> float:     
        '''Clause 3.3.2.2(a), AS1720.1:2010'''
        return self.g_13 * self.L / self.sec.d 
    
    #for n in n_all:
    @property
    def g_31(self) -> float:
        '''Table 2.7, AS1720.1:2010'''
        return g31_lookup(self.n_com)

    @property
    def g_32(self) -> float:
        '''Table 2.7, AS1720.1:2010'''
        return g32_lookup(self.n_com * self.n_mem)
     
    @property
    def S4(self) -> float:     
        '''Clause 3.3.2.2(b), AS1720.1:2010'''
        S4_1 =  self.L_ay / self.sec.b_stud
        S4_2 = self.g_13 * self.L / (self.sec.b_stud)
        return min(S4_1, S4_2)
        
    @property
    def S1(self) -> float:     
        '''Clause 3.2.3.2(b), AS1720.1:2010'''
        #Continuous restraint, tension edge
        return NotImplementedError
        #return (1.5 * (self.sec.d/self.sec.b_stud))/((((math.pi * self.sec.d)/600)**2+.4)**0.5)     

    @property
    def rho_c(self) -> float:     
        '''Section E2, AS1720.1:2010'''
        r = self.r if self.r > 0 else 0.25
        if self.mat.seasoned:
            rho = 11.39 * (self.mat.E / self.mat.f_c)**(-0.408)*r**(-0.074)
        else:
            rho = 9.29 * (self.mat.E / self.mat.f_c)**(-0.367)*r**(-0.146)
        return rho
        
    @property
    def rho_b(self) -> float:     
        '''Section E2, AS1720.1:2010'''
        r = self.r if self.r > 0 else 0.25
        if self.mat.seasoned:
            rho = 14.71 * (self.mat.E / self.mat.f_b)**(-0.480)*r**(-0.061)
        else:
            rho = 11.63 * (self.mat.E / self.mat.f_b)**(-0.435)*r**(-0.110)
        return rho
    
    @property
    def k4(self) -> float:     
        '''Table 2.5, AS1720.1:2010'''
        if self.mat.seasoned:            
            return 1.0 
        else:
            return NotImplementedError
    
    @property
    def k6(self) -> float:
        '''Çlause 2.4.3, AS1720.1:2010'''
        return k6_lookup(self.mat.seasoned, self.high_temp_latitude)
    
    @property
    def k9(self) -> float:     
        '''Clause 2.4.5.3, AS1720.1:2010'''
        return max(self.g_31 + (self.g_32 - self.g_31) * (1 - (2 * self.member_spacing/self.L)) , 1)
        
    @property
    def k12_x(self) -> float:
        '''Clause 3.3.3, AS1720.1:2010'''
        return k12_lookup_com(self.rho_c, self.S3)
    
    @property
    def k12_y(self) -> float:
        '''Clause 3.3.3, AS1720.1:2010'''
        return k12_lookup_com(self.rho_c, self.S4)
    
    @property
    def k12_bend(self) -> float:
        '''Clause 3.2.4, AS1720.1:2010'''
        return k12_lookup_bend(self.rho_b,self.S1)
        
def application_categories():
    '''Table 2.1, AS1720.1:2010'''
    a = [1, 2, 3]
    return a

#Determine capacity factor for different applicaiton categories,φ.
# def capacity_factor_lookup(application_cat, grade): #Table 2.1, AS1720.1:2010
#     #NOTE: ONLY IMPLEMENTED FOR MGP15, 
#     # NOT IMPLEMENTED FOR A17, >=F17

    
#     if application_cat == 1:
#         if grade[0] == 'MGP15':
#             phi = 0.95
#         else:
#             phi = 0.9
#     if application_cat == 2:
#         if grade[0] == 'MGP15':
#             phi = 0.85
#         else:
#             phi = 0.7
#     if application_cat == 3:
#         if grade[0] == 'MGP15':
#             phi = 0.75
#         else:
#             phi = 0.6
#     return phi

def k6_lookup(seasoned,high_temp_latitude):
    '''Clause 2.4.3, AS1720.1:2010'''
    #modification factor for strength for the effect of temperature
    #high temp latitude:
    # "Queensland_&_North_of_25˚S":0.9,
    # "Other_Regions_of_Australia_&_North_of_16˚S":0.9,
    #other regions:
    # "Queensland_&_South_of_25˚S":1.0,
    # "Other_Regions_of_Australia_&_South_of_16˚S":1.0
        
    if seasoned and high_temp_latitude:
        return 0.9
    else:
        return 1.0

def k12_lookup_com(rho_c,S3):
    '''Clause 3.3.3, AS 1720.1:2010'''
    pcS = rho_c * S3
    if pcS <= 10:
        return 1.0
    if pcS >= 10 and pcS <= 20:
        return 1.5-(0.05*pcS)
    if pcS >= 20:
        return 200/((pcS)**2)

def g31_lookup(n_com: int) -> float:     
    '''Table 2.7, AS1720.1:2010'''
    #g31 = geometric factor for combined members in combined system
    match n_com:
        case 1: v = 1
        case 2: v = 1.14
        case 3: v = 1.2
        case 4: v = 1.24
        case 5: v = 1.26
        case 6: v = 1.28
        case 7: v = 1.3
        case 8: v = 1.31
        case 9: v = 1.32
        case _: v = 1.33
    return v

def g32_lookup(n_cm):
    '''Table 2.7, AS1720.1:2010'''     
    #g31 = geometric factor for combined members in discrete parallel system
    g32 = g31_lookup(n_cm)
    return g32


def k12_lookup_bend(rho_b,S1):     
    '''Clause 3.2.4, AS1720.1:2010'''
    pbS = rho_b * S1
    if pbS <= 10:
        return 1.0
    if pbS >= 10 and pbS <= 20:
        return 1.5-(0.05*pbS)
    if pbS >= 20:
        return 200/((pbS)**2)
