# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 13:37:31 2022

@author: uqjgatta
"""
from __future__ import annotations

from dataclasses import dataclass, field
from timberas.shapes import rectangle


from math import nan, isnan, floor, log10

# from enum import Enum
# class SectionTypes(Enum):
#     RECTANGLE: 'rectangle'
#     ROUND: 'round'


@dataclass(kw_only=True)
class BlockSection():
    name: str = ''
    section: str = ''
    sec_type: str = ''

    n: int = 1
    b_i: float = 10
    d: float = nan
    b: float = nan

    A_g: float = nan
    I_x: float = nan
    I_y: float = nan
    #S_x: float = nan
    #S_y: float = nan
    Z_x: float = nan
    Z_y: float = nan
    r_x: float = nan
    r_y: float = nan
    I_w: float = nan
    J: float = nan

    x_c: float = 0
    y_c: float = 0

    # round values to a number of significant figures
    sig_figs: int = field(repr=False, default=4)

    def __post_init__(self):
        if self.sec_type != '':
            self.b = self.n * self.b_i
            self.solve_shape()

    def solve_shape(self):
        if self.sec_type in ['rectangle']:
            shape_fn = rectangle
        else:
            raise NotImplementedError(f'section type: {self.sec_type} has no shape function')

        self.A_g = shape_fn.A_g(self)
        self.I_x = shape_fn.I_x(self)
        self.I_y = shape_fn.I_y(self)
        #self.S_x = shape_fn.S_x(self)
        #self.S_y = shape_fn.S_y(self)
        self.J = shape_fn.J(self)
        self.I_w = shape_fn.I_w(self)       

        self.Z_x = self._Z_x()
        self.Z_y = self._Z_y()
        self.r_x = self._r_x()
        self.r_y = self._r_y() 

        # round to sig figs
        if self.sig_figs:
            for k, v in list(self.__dict__.items()):
                if isinstance(v, (float, int)) and (not isnan(v)) and (v != 0):
                    setattr(self, k, round(v, self.sig_figs -
                            int(floor(log10(abs(v))))-1))

    def _Z_x(self) -> float:
        #Note - these are private methods rather than properties to allow for rounding
        return self.I_x / self.y_max

    def _Z_y(self)-> float:
        return self.I_y / self.x_max

    def _r_x(self) -> float:
        return (self.I_x / self.A_g) ** 0.5

    def _r_y(self) -> float:
        return (self.I_y / self.A_g) ** 0.5
    
    @property
    def x_max(self):
        return self.b/2


    @property
    def y_max(self):
        return self.d/2
        
    @classmethod
    def from_dict(cls, **kwargs):
        o = cls()
        #all_ann = cls.__annotations__
        for k, v in kwargs.items():
            # note - @property items are in hasattr but not in __annotations__)
            if hasattr(o, k):  # and (k in cls.__annotations__):
                setattr(o, k, v)

        if isnan(o.A_g):
            # if section properties aren't created in cls() or by dictionary override, add them here
            o.solve_shape()
        return o



TimberSection = BlockSection # | ISection

# @dataclass(kw_only = True)
# class StudSection(RectSection):
#     n: int = 1
#     b_stud: float = 10
#     b: float = 0
#     d: float = 10
#     b: float = 10
    
#     def __post_init__(self):
#         #if self.name == '':
#         self.sec_name = self._stud_name()
#         self.b = self.n * self.b_stud
#         self.solve_props()
#         self.name = self._stud_name()
        
#     def _stud_name(self):
#         return f'{self.n}/{self.d}x{self.b_stud}'


# @dataclass(kw_only = True)
# class Section():
#     name: str = '' 
#     A_g: float = 0
#     I_x: float = 0
#     I_y: float = 0
#     S_x: float = 0
#     S_y: float = 0
#     Z_x: float = 0
#     Z_y: float = 0
#     r_x: float = 0
#     r_y: float = 0
#     I_w: float = 0
#     J: float = 0
    
#     A_v: float = 0 #area of voids within section

#     def solve_props(self):        
#         self.A_g = self._A_g()
#         self.I_x = self._I_x()
#         self.I_y = self._I_y() 
#         self.S_x = self._S_x()
#         self.S_y = self._S_y()
#         self.Z_x = self._Z_x()
#         self.Z_y = self._Z_y()
#         self.r_x = self._r_x()
#         self.r_y = self._r_y()
#         self.I_w = self._I_w()
#         self.J = self._J()
        
    
#     @property
#     def A_n(self):
#         #net section area
#         return self.A_g - self.A_v
    
#     @property
#     def x_max(self):
#         raise NotImplementedError()    

#     @property
#     def y_max(self):
#         raise NotImplementedError()  
        
#     def _Z_x(self) -> float:
#         return self.I_x / self.y_max

#     def _Z_y(self)-> float:
#         return self.I_y / self.x_max

#     def _r_x(self) -> float:
#         return (self.I_x / self.A_g) ** 0.5

#     def _r_y(self) -> float:
#         return (self.I_y / self.A_g) ** 0.5
    
#     def _A_g(self):
#         return self._build_section('A_g')

#     def _I_x(self):
#         return self._build_section('I_x')
    
#     def _I_y(self):
#         return self._build_section('I_y')

#     def _S_x(self):
#         return self._build_section('S_x')
    
#     def _S_y(self):
#         return self._build_section('S_y')    

#     def _I_w(self):
#         return self._build_section('I_w')    

#     def _J(self):
#         return self._build_section('J')    

#     def _build_section(self):
#         raise NotImplementedError()

#     @classmethod
#     def from_dict(cls, **kwargs):
#         o = cls()
#         for k, v in kwargs.items():
#             setattr(o, k, v)
#         return o        

# #https://www.projectengineer.net/what-is-the-torsion-constant/

