# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 15:19:49 2021

@author: uqjgatta
"""
from __future__ import annotations
from dataclasses import dataclass, field
from timberas.material import TimberMaterial
from timberas.geometry import TimberSection

from timberas.AS1684_dicts import g13_lookup
import math


@dataclass
class EffectiveLengthFactor():
    FixedFixed: float = 0.7
    FixedPinned: float = 0.85
    PinnedPinned: float = 1.0
    FixedSway: float = 1.5
    FixedFree: float = 2.0
    FlatEndRestraint: float = 0.7
    BoltedEndRestraint: float = 0.75
    FramingStuds: float = 0.9    






# EffectiveLengthFactor = SimpleNamespace(
#     FixedFixed = 0.7,
#     FixedPinned = 0.85,
#     PinnedPinned = 1.0,
#     FixedSway = 1.5,
#     FixedFree = 2.0,
#     FlatEndRestraint = 0.7,
#     BoltedEndRestraint = 0.75,
#     FramingStuds = 0.9    
# )
    # '''A the column effective length factor (g_13) listed in AS1720.1
    #    Table 3.2, for different end restaint conditions.'''



def locations_latitudes():
    '''Clause 2.4.3, AS1720.1:2010'''
    l = ['Queensland_&_North_of_25˚S','Queensland_&_South_of_25˚S','Other_Regions_of_Australia_&_North_of_16˚S',
         'Other_Regions_of_Australia_&_North_of_16˚S',
         'Other_Regions_of_Australia_&_South_of_16˚S']
    return l


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
    g_13: float = 1 
    k1: float = 1
    r: float = 0.25 #ratio of temporary to total design action effect

    N_dt: float = field(init = False) #kN
    N_dc: float = field(init = False) #kN
    N_cx: float = field(init = False) #kN
    N_cy: float = field(init = False) #kN
    M_d: float = field(init = False) #kNm

    def __post_init__(self):
        self.sec_name = self.sec.name
        self.mat_name = self.mat.name
        self.N_dt = self._N_dt()
        self.N_cx = self._N_cx()
        self.N_cy = self._N_cy()
        self.M_d = self._M_d()
    
    @property
    def phi(self) -> float:     
        '''Table 2.1, AS1720.1:2010'''
        return self.mat.phi(self.application_cat)
    
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

    # @property
    # def g_13(self) -> float:
    #     '''Clause 3.2.2.4(d)(ii), AS1720.3:2016'''
    #     return g13_lookup(self.L)
    
    @property
    def S3(self) -> float:     
        '''Clause 3.3.2.2(a), AS1720.1:2010'''
        return self.g_13 * self.L / self.sec.d 
    
    #for n in n_all:
    @property
    def g_31(self) -> float:
        '''Table 2.7, AS1720.1:2010'''
        return self.g31_lookup(self.n_com)

    @property
    def g_32(self) -> float:
        '''Table 2.7, AS1720.1:2010'''
        return self.g32_lookup(self.n_com * self.n_mem)
     
    @property
    def S4(self) -> float:     
        '''Clause 3.3.2.2(b), AS1720.1:2010'''
        #NOTE: b_i or b? valid for other cases?
        S4_1 =  self.L_ay / self.sec.b
        S4_2 = self.g_13 * self.L / (self.sec.b)
        return min(S4_1, S4_2)
        
    @property
    def S1(self) -> float:     
        raise NotImplementedError


    @property
    def rho_c(self) -> float:     
        '''Section E2, AS1720.1:2010'''
        #NOTE -> move to child class when other materials (LVL) added
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
        return self.k6_lookup(self.mat.seasoned, self.high_temp_latitude)
    
    @property
    def k9(self) -> float:     
        '''Clause 2.4.5.3, AS1720.1:2010'''
        return max(self.g_31 + (self.g_32 - self.g_31) * (1 - (2 * self.member_spacing/self.L)) , 1)
        
    @property
    def k12_x(self) -> float:
        '''Clause 3.3.3, AS1720.1:2010'''
        return self.k12_lookup_com(self.rho_c, self.S3)
    
    @property
    def k12_y(self) -> float:
        '''Clause 3.3.3, AS1720.1:2010'''
        return self.k12_lookup_com(self.rho_c, self.S4)
    
    @property
    def k12_bend(self) -> float:
        '''Clause 3.2.4, AS1720.1:2010'''
        return self.k12_lookup_bend(self.rho_b,self.S1)
            

    def k6_lookup(self, seasoned,high_temp_latitude):
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

    def k12_lookup_com(self, rho_c,S3):
        '''Clause 3.3.3, AS 1720.1:2010'''
        pcS = rho_c * S3
        if pcS <= 10:
            return 1.0
        if pcS >= 10 and pcS <= 20:
            return 1.5-(0.05*pcS)
        if pcS >= 20:
            return 200/((pcS)**2)

    def g31_lookup(self, n_com: int) -> float:     
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

    def g32_lookup(self, n_cm):
        '''Table 2.7, AS1720.1:2010'''     
        #g31 = geometric factor for combined members in discrete parallel system
        g32 = self.g31_lookup(n_cm)
        return g32


    def k12_lookup_bend(self, rho_b,S1):     
        '''Clause 3.2.4, AS1720.1:2010'''
        pbS = rho_b * S1
        if pbS <= 10:
            return 1.0
        if pbS >= 10 and pbS <= 20:
            return 1.5-(0.05*pbS)
        if pbS >= 20:
            return 200/((pbS)**2)


class BoardMember(TimberMember):
    ...
            
    @property
    def S1(self) -> float:     
        '''Clause 3.2.3.2(b), AS1720.1:2010'''
        #Continuous restraint, tension edge
        #NOTE -> self.b for single and multiboard?
        return (1.5 * (self.sec.d/self.sec.b))/((((math.pi * self.sec.d)/600)**2+.4)**0.5)     


class GlulamMember(BoardMember):
    ...