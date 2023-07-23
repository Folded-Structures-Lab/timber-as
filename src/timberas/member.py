"""
TODO
"""
from __future__ import annotations
import math
from math import isnan, floor, log10
from enum import IntEnum, Enum
from dataclasses import dataclass, field
from timberas.material import TimberMaterial
from timberas.geometry import TimberSection
from timberas.utils import nomenclature_AS1720 as NOMEN


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


class RestraintEdge(str, Enum):
    """compression edge is critical edge"""

    TENSION = "tension"
    COMPRESSION = "compression"
    BOTH = "both"  # uses compression edge formulas
    TENSION_AND_TORSIONAL = "tension_and_torsional"


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

    L: float = 1  # length
    L_a: float | dict | None = None
    # L_ar: float = nan  # torsional constraint, compression edge
    g_13: float | dict = 1
    k_1: float = 1.0
    r: float = 0.25  # ratio of temporary to total design action effect
    restraint_edge: str | RestraintEdge = RestraintEdge.TENSION

    N_dt: float = field(init=False)  # kN
    N_dcx: float = field(init=False)  # kN
    N_dcy: float = field(init=False)  # kN
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
        self.N_dcx = self._N_dcx()
        self.N_dcy = self._N_dcy()
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

    def report(
        self,
        attribute_names: str | list[str] | None = None,
        report_type: str = "print",
        with_nomenclature: bool = False,
        with_clause: bool = False,
    ) -> None:
        # convert single-value attribute to list
        if attribute_names is None:
            attribute_names = list(self.__annotations__.keys())
        if not isinstance(attribute_names, list):
            attribute_names = [attribute_names]

        if report_type == "print":
            # print out attributes
            for att in attribute_names:
                # get attribute val from self, self.sec, or self.mat
                att_val = None
                if hasattr(self, att):
                    att_val = getattr(self, att)
                elif hasattr(self.mat, att):
                    att_val = getattr(self.mat, att)
                elif hasattr(self.sec, att):
                    att_val = getattr(self.sec, att)
                if att_val is not None:
                    prefix = ""
                    if att in NOMEN:
                        # check it attribute defined in nomenclature dictionary
                        nom, clause = NOMEN[att]
                        if with_nomenclature:
                            # add nomenclature
                            prefix = prefix + " " + nom
                        if with_clause:
                            # add clause
                            prefix = prefix + " " + clause
                    print(f"    {att}{prefix} = {att_val}")
                else:
                    print(f"Unknown attribute {att}")

    @property
    def phi(self) -> float:
        """Table 2.1, AS1720.1:2010"""
        phi: float = self.mat.phi(self.application_cat)
        return phi

    def _N_dcx(self) -> float:
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

    def _N_dcy(self) -> float:
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
        return min(self._N_dcx(), self._N_dcy())

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
        """Slenderness coefficient for lateral buckling under compression, x axis.
        Clause 3.3.2, AS1720.1:2010. Not implemented in TimberMember parent class, added in
        child classes."""
        raise NotImplementedError

    @property
    def S4(self) -> float:
        """Clause 3.3.2.2(b), AS1720.1:2010"""
        # NOTE: b_i or b? valid for other cases?
        calc_1 = self.L_ay / self.sec.b
        calc_2 = self.g_13_y * self.L / (self.sec.b)
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
    def g_13_x(self) -> float:
        """Effective length factor for compressive buckling, x-axis"""
        # g_13 is float - use in x and y axes
        if isinstance(self.g_13, float | int):
            return self.g_13
        # else g_13 is dictionary - use x axis key value only
        if "x" in self.g_13:
            return self.g_13["x"]
        # raise error if not yet returned
        raise KeyError(
            "effective length factor g_13 not defined for x-axis compressive buckling"
        )

    @property
    def g_13_y(self) -> float:
        """Effective length factor for compressive buckling, y-axis"""
        # g_13 is float - use in x and y axes
        if isinstance(self.g_13, float | int):
            return self.g_13
        # else g_13 is dictionary - use y axis key value only
        if "y" in self.g_13:
            return self.g_13["y"]
        # raise error if not yet returned
        raise KeyError(
            "effective length factor g_13 not defined for y-axis compressive buckling"
        )

    @property
    def L_ax(self) -> float:
        """distance between effective lateral restraint against buckling about x-axis."""
        if isinstance(self.L_a, float | int) or (self.L_a is None):
            l_ax = self.L_a
        elif isinstance(self.L_a, dict) and "x" in self.L_a:
            l_ax = self.L_a["x"]
        else:  # raise error if not yet returned
            raise KeyError(
                "lateral restraint for x-axis compressive buckling L_ax not defined"
            )
        if l_ax is None:
            l_ax = self.L
        return l_ax

    @property
    def L_ay(self) -> float:
        """distance between effective lateral restraint against buckling about y-axis."""
        if isinstance(self.L_a, float | int) or (self.L_a is None):
            l_ay = self.L_a
        elif isinstance(self.L_a, dict) and "y" in self.L_a:
            l_ay = self.L_a["y"]
        else:  # raise error if not yet returned
            raise KeyError(
                "lateral restraint for y-axis compressive buckling L_ay not defined"
            )
        if l_ay is None:
            l_ay = self.L
        return l_ay

    @property
    def L_a_phi(self) -> float:
        """distance between effective torsional restraint against buckling, Cl 3.2.3.2(b)."""
        if isinstance(self.L_a, dict) and "phi" in self.L_a:
            return self.L_a["phi"]
        raise KeyError(
            "no torsional restraint distance L_a_phi provided, i.e. not 'phi' key in L_a input"
        )

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
    def CLR(self) -> bool:
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
        """Clause 2.4.3, AS1720.1:2010"""
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
        if self.sec.I_x < self.sec.I_y:
            # x axis is minor axis
            print("note - x-axis is minor axis, k_12_bend = 1.0")
            return 1.0
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


class RectangleMemberStabilityMixin:
    """TODO"""

    @property
    def S1(self) -> float:
        """Clause   (b), AS1720.1:2010"""
        # Continuous restraint, tension edge
        # NOTE -> self.b for single and multiboard?

        if self.CLR:
            # continuous restraint
            match self.restraint_edge:
                case RestraintEdge.COMPRESSION | RestraintEdge.BOTH:
                    # continuous compression - Cl 3.2.3.2(b)
                    val = 0
                case RestraintEdge.TENSION:
                    # continuous tension - Eq 3.2(7)
                    val = 2.25 * self.sec.d / self.sec.b
                case RestraintEdge.TENSION_AND_TORSIONAL:
                    # continuous tension - Eq 3.2(8)
                    bot = (((math.pi * self.sec.d) / self.L_a_phi) ** 2 + 0.4) ** 0.5
                    val = 1.5 * (self.sec.d / self.sec.b) / bot
        else:
            # discrete restraint
            match self.restraint_edge:
                case RestraintEdge.COMPRESSION | RestraintEdge.BOTH:
                    # discrete compression - Cl 3.2.3.2(a), Eq 3.2(4)
                    val = (
                        1.25 * self.sec.d / self.sec.b * (self.L_ay / self.sec.d) ** 0.5
                    )
                case RestraintEdge.TENSION:
                    # discrete tension edge Cl 3.2.3.2(a), Eq 3.2(5)
                    val = (self.sec.d / self.sec.b) ** 1.35 * (
                        self.L_ay / self.sec.d
                    ) ** 0.25
                case RestraintEdge.TENSION_AND_TORSIONAL:
                    raise ValueError(
                        "restraint_edge error - discrete (non-continuous) tension edge"
                        "restraint defined with torsional restraint - no formula for S1"
                    )

        return round(val, 2)

    @property
    def S3(self) -> float:
        """Slenderness coefficient for buckling about x axis in rectangular sections.
        Clause 3.3.2.2(a), AS1720.1:2010."""
        return round(self.g_13_x * self.L / self.sec.d, 2)

    @property
    def L_CLR(self) -> float:
        """3.2.3.2"""
        # Eq 3.2(6)
        val = 64 / self.sec.d * (self.sec.b / self.rho_b) ** 2
        return val

    @property
    def CLR(self) -> bool:
        # evaluate if lateral restraint is continuous
        if self.L_ay <= self.L_CLR:
            # continuous restraint
            return True
        return False


class BoardMember(RectangleMemberStabilityMixin, TimberMember):
    """TODO"""

    # member spacing parameters for k_9 evaluation
    # n_com: int = 1
    n_mem: int = 1
    s: float = 0  # member spacing

    @property
    def k_9(self) -> float:
        """Clause 2.4.5.3, AS1720.1:2010"""
        return max(
            self.g_31 + (self.g_32 - self.g_31) * (1 - (2 * self.s / self.L)),
            1,
        )

    @property
    def n_com(self) -> int:
        if self.sec.n > 1:
            return self.sec.n
        return 1

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


class GlulamMember(RectangleMemberStabilityMixin, TimberMember):
    """TODO"""

    @property
    def k_9(self) -> float:
        """TODO"""
        return 1.0
