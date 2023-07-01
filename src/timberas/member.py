"""
TODO
"""
from __future__ import annotations
import math
from math import nan, isnan, floor, log10
from enum import auto, IntEnum, Enum
from dataclasses import dataclass, field
from timberas.material import TimberMaterial
from timberas.geometry import TimberSection


class EffectiveLengthFactor(float, Enum):
    """Dataclass containing values for effective length factor g_13 for columns with intermediate
    lateral restraint. End restraint conditions as listed in Table 3.2, AS1720.1:2010.

    Attributes:
        FIXED_FIXED (float): Both ends restrained in position and direction, g_13 = 0.7.
        FIXED_PINNED (float): One end restrained in position and direction, other in position only,
          g_13 = 0.85
        PINNED_PINNED (float): Both ends restrained in position only, g_13 = 1.
        FIXED_SWAY (float): One end restrained in position and direction, other in partial direction
        only and not position, g_13 = 1.5
        FIXED_FREE (float): One end restrained in position and direction, other unrestrained,
        g_13 = 2.0.
        FLAT_END_RESTRAINT (float): Flat ends, g_13 = 0.7
        BOLTED_END_RESTRAINT (float): Both ends held by bolts giving substantial restraint,
        g_13 = 0.7.
        FRAMING_STUDS (float): Studs in light framing, slight end restraint, g_13 = 0.9.
    """

    FIXED_FIXED: float = 0.7
    FIXED_PINNED: float = 0.85
    PINNED_PINNED: float = 1.0
    FIXED_SWAY: float = 1.5
    FIXED_FREE: float = 2.0
    FLAT_END_RESTRAINT: float = 0.7
    BOLTED_END_RESTRAINT: float = 0.75
    FRAMING_STUDS: float = 0.9


class ApplicationCategory(IntEnum):
    """Table 2.1, AS1720.1:2010"""

    SECONDARY_MEMBER = 1
    PRIMARY_MEMBER = 2
    PRIMARY_MEMBER_POST_DISASTER = 3
    LESS_THAN_25_SQM = 1
    GREATER_THAN_25_SQM = 2


class DurationFactorStrength(float, Enum):
    """Table 2.3, Table G1?, AS1720.1:2010"""

    FIVE_SECONDS = 1
    FIVE_MINUTES = 1
    FIVE_HOURS = 0.97
    FIVE_DAYS = 0.94
    FIVE_MONTHS = 0.8
    FIFTY_YEARS = 0.57
    # DL_ONLY = 0.57
    # DL_AND_LONG_TERM_LL = 0.57


class BendingRestraint(str, Enum):
    """compresssion edge is critical edge"""

    DISCRETE_LATERAL_RESTRAINT_COMPRESSION_EDGE = auto()
    DISCRETE_LATERAL_RESTRAINT_TENSION_EDGE = auto()
    CONTINUOUS_LATERAL_RESTRAINT_COMPRESSION_EDGE = auto()
    CONTINUOUS_LATERAL_RESTRAINT_TENSION_EDGE = auto()
    CONTINUOUS_LATERAL_RESTRAINT_TENSION_AND_DISCRETE_TORSIONAL_COMPRESSION = auto()


# def locations_latitudes():
#     """Clause 2.4.3, AS1720.1:2010"""
#     l = [
#         "Queensland_&_North_of_25˚S",
#         "Queensland_&_South_of_25˚S",
#         "Other_Regions_of_Australia_&_North_of_16˚S",
#         "Other_Regions_of_Australia_&_North_of_16˚S",
#         "Other_Regions_of_Australia_&_South_of_16˚S",
#     ]
#     return l


@dataclass
class TimberMember:
    """TODO"""

    sec: TimberSection = field(repr=False)
    mat: TimberMaterial = field(repr=False)
    sec_name: str = field(init=False)
    mat_name: str = field(init=False)

    application_cat: int = 1  # application category for structural member
    high_temp_latitude: bool = False
    consider_partial_seasoning: bool = False

    n_com: int = 1
    n_mem: int = 1
    member_spacing: float = 0  # member spacing

    L: float = 1  # length
    L_ay: float = 0
    L_ar: float = nan  # torsional constraint, compression edge
    g_13: float = 1
    k_1: float = 1.0
    r: float = 0.25  # ratio of temporary to total design action effect
    restraint: str | BendingRestraint = (
        BendingRestraint.DISCRETE_LATERAL_RESTRAINT_TENSION_EDGE
    )

    N_dt: float = field(init=False)  # kN
    N_cx: float = field(init=False)  # kN
    N_cy: float = field(init=False)  # kN
    N_dc: float = field(init=False)  # kN
    M_d: float = field(init=False)  # kNm
    V_d: float = field(init=False)  # kNm

    sig_figs: int = field(repr=False, default=4)

    def __post_init__(self):
        self.sec_name = self.sec.name
        self.mat_name = self.mat.name
        # self.mat.update_f_t(self.sec_type, self.d)
        self.solve_capacities()

    def solve_capacities(self):
        """Calculate tension, compression, and bending design capacities."""
        self.N_dt = self._N_dt()
        self.N_cx = self._N_cx()
        self.N_cy = self._N_cy()
        self.N_dc = self._N_dc()
        self.M_d = self._M_d()
        self.V_d = self._V_d()

        # round to sig figs
        if self.sig_figs:
            for key, val in list(self.__dict__.items()):
                if isinstance(val, (float, int)) and (not isnan(val)) and (val != 0):
                    setattr(
                        self,
                        key,
                        round(val, self.sig_figs - int(floor(log10(abs(val)))) - 1),
                    )

    def update_k_1(self, k_1: float) -> TimberSection:
        """Change k_1 factor and recalculate section capacities."""
        self.k_1 = k_1
        self.solve_capacities()
        return self

    @property
    def phi(self) -> float:
        """Table 2.1, AS1720.1:2010"""
        phi: float = self.mat.phi(self.application_cat)
        return phi

    def _N_cx(self) -> float:
        """Clause 3.3.1.1, AS1720.1:2010"""
        return (
            self.phi
            * self.k_1
            * self.k_4
            * self.k_6
            * self.k_12_x
            * self.mat.f_c
            * self.sec.A_c
            / 1000
        )

    def _N_cy(self) -> float:
        """Clause 3.3.1.1, AS1720.1:2010"""
        return (
            self.phi
            * self.k_1
            * self.k_4
            * self.k_6
            * self.k_12_y
            * self.mat.f_c
            * self.sec.A_c
            / 1000
        )

    def _N_dc(self) -> float:
        """Clause 3.3.1.1, AS1720.1:2010"""
        return min(self._N_cx(), self._N_cy())

    def _N_dt(self) -> float:
        """Clause 3.4.1, AS1720.1:2010"""
        return (
            self.phi
            * self.k_1
            * self.k_4
            * self.k_6
            * self.mat.f_t
            * self.sec.A_t
            / 1000
        )

    def _M_d(self) -> float:
        """Clause 3.2.1.1, AS1720.1:2010"""
        return (
            self.phi
            * self.k_1
            * self.k_4
            * self.k_6
            * self.k_9
            * self.k_12_bend
            * self.mat.f_b
            * self.sec.Z_x
            / 1e6
        )

    def _V_d(self) -> float:
        """flexural shear strength Cl 3.2.5"""
        cap = (
            self.phi
            * self.k_1
            * self.k_4
            * self.k_6
            * self.mat.f_s
            * self.sec.A_s
            / 1e3
        )
        return cap

    @property
    def S1(self) -> float:
        """Slenderness coefficient for lateral buckling under bending, major axis. Clause 3.2.3,
        AS1720.1:2010. Not implemented in TimberMember parent class, added in child classes.
        """
        raise NotImplementedError

    @property
    def S2(self) -> float:
        """Slenderness coefficient for lateral buckling under bending, minor axis.
        Clause 3.2.3(c), AS1720.1:2010."""
        return 0

    @property
    def S3(self) -> float:
        """Slenderness coefficient for lateral buckling under compression, major axis.
        Clause 3.3.2, AS1720.1:2010. Not implemented in TimberMember parent class, added in
        child classes."""
        raise NotImplementedError

    @property
    def S4(self) -> float:
        """Clause 3.3.2.2(b), AS1720.1:2010"""
        # NOTE: b_i or b? valid for other cases?
        calc_1 = self.L_ay / self.sec.b
        calc_2 = self.g_13 * self.L / (self.sec.b)
        return round(min(calc_1, calc_2), 2)

    @property
    def rho_c(self) -> float:
        """Section E2, AS1720.1:2010"""
        # NOTE -> move to child class when other materials (LVL) added
        r = self.r if self.r > 0 else 0.25
        if self.mat.seasoned:
            rho = 11.39 * (self.mat.E / self.mat.f_c) ** (-0.408) * r ** (-0.074)
        else:
            rho = 9.29 * (self.mat.E / self.mat.f_c) ** (-0.367) * r ** (-0.146)
        return rho

    @property
    def rho_b(self) -> float:
        """Section E2, AS1720.1:2010"""
        r = self.r if self.r > 0 else 0.25
        # NOTE - some of this term is a material attribute only
        if self.mat.seasoned:
            rho = 14.71 * (self.mat.E / self.mat.f_b) ** (-0.480) * r ** (-0.061)
        else:
            rho = 11.63 * (self.mat.E / self.mat.f_b) ** (-0.435) * r ** (-0.110)
        return rho

    @property
    def L_CLR(self) -> float:
        """Clause"""
        raise NotImplementedError

    @property
    def k_4(self) -> float:
        """Table 2.5, AS1720.1:2010"""
        if self.mat.seasoned:
            return 1.0
        elif not self.consider_partial_seasoning:
            return 1.0
        else:  # material is unseasoned and consider_partial_seasoning
            # NOTE - k_4 between 75 and 100mm not defined?
            least_dim = min(self.sec.b, self.sec.d)
            if least_dim <= 38:
                return 1.15
            elif least_dim <= 50:
                return 1.10
            elif least_dim <= 75:
                return 1.05
            elif least_dim > 100:
                return 1.00
            else:
                raise NotImplementedError(
                    f"{self.sec.d} not defined for k_4 partial seasoning factor"
                )

    @property
    def k_6(self) -> float:
        """Çlause 2.4.3, AS1720.1:2010"""
        return self.k_6_lookup(self.mat.seasoned, self.high_temp_latitude)

    @property
    def k_9(self) -> float:
        """Modification factor for strength sharing. Clause 2.4.5.3, AS1720.1:2010.
        Not Implemented in TimberMember parent class, added in child classes."""
        raise NotImplementedError

    @property
    def k_12_c(self) -> float:
        """Modification factor for stability, to allow for slenderness effects on compression
        strength. Minimum of k_12_x and k_12_y. Clause 3.3.3, AS1720.1:2010."""
        return min(self.k_12_x, self.k_12_y)

    @property
    def k_12_x(self) -> float:
        """Modification factor for stability, to allow for slenderness effects on compression
        strength (x-axis). Clause 3.3.3, AS1720.1:2010."""
        return self.calc_k12_compression(self.rho_c, self.S3)

    @property
    def k_12_y(self) -> float:
        """Modification factor for stability, to allow for slenderness effects on compression
        strength (y-axis). Clause 3.3.3, AS1720.1:2010."""
        return self.calc_k12_compression(self.rho_c, self.S4)

    @property
    def k_12_bend(self) -> float:
        """Modification factor for stability, to allow for slenderness effects on bending
        strength. Clause 3.2.4, AS1720.1:2010."""
        return self.calc_k12_bending(self.rho_b, self.S1)

    def k_6_lookup(self, seasoned: bool, high_temp_latitude: float) -> float:
        """Modification factor for strength for the effect of temperature.
        Clause 2.4.3, AS1720.1:2010."""
        if seasoned and high_temp_latitude:
            k_6 = 0.9
        else:
            k_6 = 1.0
        return k_6

    def calc_k12_compression(self, rho_c: float, S3: float) -> float:
        """Calculate stability factor k12 for compression. Clause 3.3.3, AS 1720.1:2010."""
        rho_times_s = rho_c * S3
        if rho_times_s <= 10:
            return 1.0
        if rho_times_s >= 10 and rho_times_s <= 20:
            return 1.5 - (0.05 * rho_times_s)
        if rho_times_s >= 20:
            return 200 / ((rho_times_s) ** 2)

    def calc_k12_bending(self, rho_b: float, S1: float) -> float:
        """Calculate stability factor k12 for bending. Clause 3.2.4, AS1720.1:2010"""
        rho_times_s = rho_b * S1
        if rho_times_s <= 10:
            return 1.0
        if rho_times_s >= 10 and rho_times_s <= 20:
            return 1.5 - (0.05 * rho_times_s)
        if rho_times_s >= 20:
            return 200 / ((rho_times_s) ** 2)


class BoardMember(TimberMember):
    """TODO"""

    @property
    def S1(self) -> float:
        """Clause 3.2.3.2(b), AS1720.1:2010"""
        # Continuous restraint, tension edge
        # NOTE -> self.b for single and multiboard?
        match self.restraint:
            case BendingRestraint.DISCRETE_LATERAL_RESTRAINT_COMPRESSION_EDGE:
                val = 1.25 * self.sec.d / self.sec.b * (self.L_ay / self.sec.d) ** 0.5
            case BendingRestraint.DISCRETE_LATERAL_RESTRAINT_TENSION_EDGE:
                val = (self.sec.d / self.sec.b) ** 1.35 * (
                    self.L_ay / self.sec.d
                ) ** 0.25
            case BendingRestraint.CONTINUOUS_LATERAL_RESTRAINT_COMPRESSION_EDGE:
                val = 2.25 * self.sec.d / self.sec.b
            case BendingRestraint.CONTINUOUS_LATERAL_RESTRAINT_TENSION_EDGE:
                bot = (((math.pi * self.sec.d) / self.L_ar) ** 2 + 0.4) ** 0.5
                val = 1.5 * (self.sec.d / self.sec.b) / bot

        return round(val, 2)

    @property
    def S3(self) -> float:
        """Slenderness coefficient for buckling about major axis in rectangular sections.
        Clause 3.3.2.2(a), AS1720.1:2010."""
        return round(self.g_13 * self.L / self.sec.d, 2)

    @property
    def k_9(self) -> float:
        """Clause 2.4.5.3, AS1720.1:2010"""
        return max(
            self.g_31
            + (self.g_32 - self.g_31) * (1 - (2 * self.member_spacing / self.L)),
            1,
        )

    # for n in n_all:

    @property
    def L_CLR(self) -> float:
        """3.2.3.2"""
        val = 64 / self.sec.d * (self.sec.b / self.rho_b) ** 2
        return val

    @property
    def g_31(self) -> float:
        """Table 2.7, AS1720.1:2010"""
        return self.g3_lookup(self.n_com)

    @property
    def g_32(self) -> float:
        """Table 2.7, AS1720.1:2010"""
        g32 = self.g3_lookup(self.n_com * self.n_mem)
        return g32
        # return self.g32_lookup(self.n_com * self.n_mem)

    @staticmethod
    def g3_lookup(n: int) -> float:
        """Table 2.7, AS1720.1:2010"""
        match n:
            case 1:
                val = 1
            case 2:
                val = 1.14
            case 3:
                val = 1.2
            case 4:
                val = 1.24
            case 5:
                val = 1.26
            case 6:
                val = 1.28
            case 7:
                val = 1.3
            case 8:
                val = 1.31
            case 9:
                val = 1.32
            case _:
                val = 1.33
        return val

    # def g32_lookup(self, n_cm: int) -> float:
    #     """Table 2.7, AS1720.1:2010"""
    #     # g31 = geometric factor for combined members in discrete parallel system
    #     g32 = self.g31_lookup(n_cm)
    #     return g32


class GlulamMember(BoardMember):
    """TODO"""

    @property
    def k_9(self) -> float:
        """TODO"""
        return 1.0
