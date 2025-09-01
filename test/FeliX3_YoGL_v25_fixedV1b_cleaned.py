"""
Python model 'FeliX3_YoGL_v25_fixedV1b_cleaned.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np
import xarray as xr

from pysd.py_backend.functions import zidz, pulse, ramp, step, sum, if_then_else
from pysd.py_backend.statefuls import (
    Initial,
    Smooth,
    Integ,
    Trend,
    DelayFixed,
    SampleIfTrue,
)
from pysd.py_backend.lookups import HardcodedLookups
from pysd.py_backend.utils import load_model_data, load_modules
from pysd import Component

__pysd_version__ = "3.14.3"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent

_subscript_dict, _modules = load_model_data(_root, "FeliX3_YoGL_v25_fixedV1b_cleaned")

component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 1900,
    "final_time": lambda: 2100,
    "time_step": lambda: 0.125,
    "saveper": lambda: 1,
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Year",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="Year",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################

# load modules from modules_FeliX3_YoGL_v25_fixedV1b_cleaned directory
exec(load_modules("modules_FeliX3_YoGL_v25_fixedV1b_cleaned", _modules, _root, []))


@component.add(name="standev", comp_type="Constant", comp_subtype="Normal")
def standev():
    return 0.5


@component.add(
    name='"95 gj"',
    units="$/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mtoe_to_gj": 1, "mtoe_per_barrel": 1},
)
def nvs_95_gj():
    return 9.5 * mtoe_to_gj() * mtoe_per_barrel()


@component.add(
    name='"Share of females aged 20-39 with sec plus education"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "secondary_education_graduates": 1,
        "tertiary_education_graduates": 1,
        "population_cohorts": 1,
    },
)
def share_of_females_aged_2039_with_sec_plus_education():
    return (
        sum(
            secondary_education_graduates()
            .loc["female", _subscript_dict['"20 to 39"']]
            .reset_coords(drop=True)
            .rename({"Cohorts": '"20 to 39"!'}),
            dim=['"20 to 39"!'],
        )
        + sum(
            tertiary_education_graduates()
            .loc["female", _subscript_dict['"20 to 39"']]
            .reset_coords(drop=True)
            .rename({"Cohorts": '"20 to 39"!'}),
            dim=['"20 to 39"!'],
        )
    ) / sum(
        population_cohorts()
        .loc["female", _subscript_dict['"20 to 39"']]
        .reset_coords(drop=True)
        .rename({"Cohorts": '"20 to 39"!'}),
        dim=['"20 to 39"!'],
    )


@component.add(
    name='"Prevalence model-based"',
    units="Dmnl",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "yogl_education_indicator": 1,
        "yogl_poverty_indicator": 1,
        "yogl_health_indicator": 1,
        "yogl_life_satisfaction_indicator": 1,
    },
)
def prevalence_modelbased():
    return (
        yogl_education_indicator()
        * yogl_poverty_indicator()
        * yogl_health_indicator()
        * yogl_life_satisfaction_indicator()
    )


@component.add(
    name="Population 65 plus",
    units="People",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_cohorts": 1},
)
def population_65_plus():
    return sum(
        population_cohorts()
        .loc[:, _subscript_dict['"65 plus"']]
        .rename({"Gender": "Gender!", "Cohorts": '"65 plus"!'}),
        dim=["Gender!", '"65 plus"!'],
    )


@component.add(
    name="Survivors in interval x x plus 5",
    units="People",
    subscripts=["Gender", "Cohorts"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_survivors_in_interval_x_x_plus_5": 1,
        "_integ_survivors_in_interval_x_x_plus_5_1": 1,
    },
    other_deps={
        "_integ_survivors_in_interval_x_x_plus_5": {
            "initial": {"actual_survivors_in_2000": 1},
            "step": {"maturation_rate_of_survivors": 2, "death_rate_of_survivors": 1},
        },
        "_integ_survivors_in_interval_x_x_plus_5_1": {
            "initial": {"actual_survivors_in_2000": 1},
            "step": {"maturation_rate_of_survivors": 1, "death_rate_of_survivors": 1},
        },
    },
)
def survivors_in_interval_x_x_plus_5():
    """
    Survivors with the simulated mortality rates, starting from year 2000. Initial values can be either the actual survisors (historical data) or an arbitrary value such as 1000. The simulated YoGL values do not differ.
    """
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )
    value.loc[:, _subscript_dict["AllButYoungest"]] = (
        _integ_survivors_in_interval_x_x_plus_5().values
    )
    value.loc[:, ['"0-4"']] = _integ_survivors_in_interval_x_x_plus_5_1().values
    return value


_integ_survivors_in_interval_x_x_plus_5 = Integ(
    lambda: xr.DataArray(
        maturation_rate_of_survivors()
        .loc[:, _subscript_dict["PreviousCohort"]]
        .rename({"Cohorts": "PreviousCohort"})
        .values,
        {
            "Gender": _subscript_dict["Gender"],
            "AllButYoungest": _subscript_dict["AllButYoungest"],
        },
        ["Gender", "AllButYoungest"],
    )
    - maturation_rate_of_survivors()
    .loc[:, _subscript_dict["AllButYoungest"]]
    .rename({"Cohorts": "AllButYoungest"})
    - death_rate_of_survivors()
    .loc[:, _subscript_dict["AllButYoungest"]]
    .rename({"Cohorts": "AllButYoungest"}),
    lambda: actual_survivors_in_2000()
    .loc[:, _subscript_dict["AllButYoungest"]]
    .rename({"Cohorts": "AllButYoungest"}),
    "_integ_survivors_in_interval_x_x_plus_5",
)

_integ_survivors_in_interval_x_x_plus_5_1 = Integ(
    lambda: (
        -maturation_rate_of_survivors().loc[:, '"0-4"'].reset_coords(drop=True)
        - death_rate_of_survivors().loc[:, '"0-4"'].reset_coords(drop=True)
    ).expand_dims({'"0 to 19"': ['"0-4"']}, 1),
    lambda: actual_survivors_in_2000()
    .loc[:, '"0-4"']
    .reset_coords(drop=True)
    .expand_dims({'"0 to 19"': ['"0-4"']}, 1),
    "_integ_survivors_in_interval_x_x_plus_5_1",
)


@component.add(
    name="net to gross fraction",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def net_to_gross_fraction():
    """
    Average value for the period (1998-2018) where the net rate data is available.
    """
    return xr.DataArray(
        [0.887368, 0.900536], {"Gender": _subscript_dict["Gender"]}, ["Gender"]
    )


@component.add(
    name="Net enrolment secondary historical",
    units="1/Year",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 2},
)
def net_enrolment_secondary_historical():
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["female"]] = np.interp(
        time(),
        [
            1998.0,
            1999.0,
            2000.0,
            2001.0,
            2002.0,
            2003.0,
            2004.0,
            2005.0,
            2006.0,
            2007.0,
            2008.0,
            2009.0,
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
            2018.0,
        ],
        [
            0.515403,
            0.518327,
            0.527175,
            0.536091,
            0.5437,
            0.555553,
            0.565771,
            0.574469,
            0.58152,
            0.591571,
            0.600249,
            0.607105,
            0.620955,
            0.632764,
            0.638382,
            0.648316,
            0.656666,
            0.657656,
            0.658486,
            0.662673,
            0.662658,
        ],
    )
    value.loc[["male"]] = np.interp(
        time(),
        [
            1998.0,
            1999.0,
            2000.0,
            2001.0,
            2002.0,
            2003.0,
            2004.0,
            2005.0,
            2006.0,
            2007.0,
            2008.0,
            2009.0,
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
            2018.0,
        ],
        [
            0.561372,
            0.562732,
            0.570533,
            0.573919,
            0.576707,
            0.582727,
            0.589875,
            0.594934,
            0.600299,
            0.609673,
            0.616124,
            0.618743,
            0.629693,
            0.637767,
            0.637554,
            0.649643,
            0.65632,
            0.656659,
            0.658112,
            0.661317,
            0.662793,
        ],
    )
    return value


@component.add(
    name="Waste Fraction PasMeat CropMeat Variation 0 0",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def waste_fraction_pasmeat_cropmeat_variation_0_0():
    return 1


@component.add(
    name="Waste Fraction PasMeat CropMeat Variation 0",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def waste_fraction_pasmeat_cropmeat_variation_0():
    return 1


@component.add(
    name="Price Elasticity of Demand Solar 0",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def price_elasticity_of_demand_solar_0():
    """
    Solar energy price elasticity of demand.
    """
    return 1


@component.add(
    name='"$ into $thousand"',
    units="Thousand",
    comp_type="Constant",
    comp_subtype="Normal",
)
def nvs_into_thousand():
    return 1 / 1000


@component.add(
    name="Change Rate Slope17",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "final_change_rate17": 1,
        "initial_change_rate17": 1,
        "ramp_period17": 1,
    },
)
def change_rate_slope17():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return (
        float(np.abs(final_change_rate17() - initial_change_rate17())) / ramp_period17()
    )


@component.add(
    name="SA Waste fraction 0 0 0 0",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_waste_fraction_0_0_0_0():
    return xr.DataArray(
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )


@component.add(name="Ramp Start161 0", comp_type="Constant", comp_subtype="Normal")
def ramp_start161_0():
    return 2020


@component.add(name="Ramp Start17", comp_type="Constant", comp_subtype="Normal")
def ramp_start17():
    return 2020


@component.add(
    name="Change Rate Slope161 0",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "final_change_rate161_0": 1,
        "initial_change_rate161_0": 1,
        "ramp_period161_0": 1,
    },
)
def change_rate_slope161_0():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return (
        float(np.abs(final_change_rate161_0() - initial_change_rate161_0()))
        / ramp_period161_0()
    )


@component.add(
    name="Ramp Period161 0", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def ramp_period161_0():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50


@component.add(
    name="Ramp Period17", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def ramp_period17():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50


@component.add(
    name="Final Change Rate161 0",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def final_change_rate161_0():
    """
    Final Educational Attainment Change Rate
    """
    return 6


@component.add(
    name="Final Change Rate17",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def final_change_rate17():
    """
    Final Educational Attainment Change Rate
    """
    return 6


@component.add(
    name="Change Rate Start17",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start17": 1},
)
def change_rate_start17():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start17()


@component.add(
    name="Initial Change Rate17",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_change_rate17():
    """
    Initial Educational Attainment Change Rate
    """
    return 3


@component.add(
    name="Change Rate Start161 0",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start161_0": 1},
)
def change_rate_start161_0():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start161_0()


@component.add(
    name="Change Rate Finish17",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start17": 1, "ramp_period17": 1},
)
def change_rate_finish17():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start17() + ramp_period17()


@component.add(
    name="Initial Change Rate161 0",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_change_rate161_0():
    """
    Initial Educational Attainment Change Rate
    """
    return 3


@component.add(
    name="Change Rate Finish161 0",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start161_0": 1, "ramp_period161_0": 1},
)
def change_rate_finish161_0():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start161_0() + ramp_period161_0()


@component.add(
    name="Eff p ON YIELD PREV",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def eff_p_on_yield_prev():
    return np.interp(
        time(),
        [
            1900.0,
            1901.0,
            1902.0,
            1903.0,
            1904.0,
            1905.0,
            1906.0,
            1907.0,
            1908.0,
            1909.0,
            1910.0,
            1911.0,
            1912.0,
            1913.0,
            1914.0,
            1915.0,
            1916.0,
            1917.0,
            1918.0,
            1919.0,
            1920.0,
            1921.0,
            1922.0,
            1923.0,
            1924.0,
            1925.0,
            1926.0,
            1927.0,
            1928.0,
            1929.0,
            1930.0,
            1931.0,
            1932.0,
            1933.0,
            1934.0,
            1935.0,
            1936.0,
            1937.0,
            1938.0,
            1939.0,
            1940.0,
            1941.0,
            1942.0,
            1943.0,
            1944.0,
            1945.0,
            1946.0,
            1947.0,
            1948.0,
            1949.0,
            1950.0,
            1951.0,
            1952.0,
            1953.0,
            1954.0,
            1955.0,
            1956.0,
            1957.0,
            1958.0,
            1959.0,
            1960.0,
            1961.0,
            1962.0,
            1963.0,
            1964.0,
            1965.0,
            1966.0,
            1967.0,
            1968.0,
            1969.0,
            1970.0,
            1971.0,
            1972.0,
            1973.0,
            1974.0,
            1975.0,
            1976.0,
            1977.0,
            1978.0,
            1979.0,
            1980.0,
            1981.0,
            1982.0,
            1983.0,
            1984.0,
            1985.0,
            1986.0,
            1987.0,
            1988.0,
            1989.0,
            1990.0,
            1991.0,
            1992.0,
            1993.0,
            1994.0,
            1995.0,
            1996.0,
            1997.0,
            1998.0,
            1999.0,
            2000.0,
            2001.0,
            2002.0,
            2003.0,
            2004.0,
            2005.0,
            2006.0,
            2007.0,
            2008.0,
            2009.0,
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
            2018.0,
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
            2024.0,
            2025.0,
            2026.0,
            2027.0,
            2028.0,
            2029.0,
            2030.0,
            2031.0,
            2032.0,
            2033.0,
            2034.0,
            2035.0,
            2036.0,
            2037.0,
            2038.0,
            2039.0,
            2040.0,
            2041.0,
            2042.0,
            2043.0,
            2044.0,
            2045.0,
            2046.0,
            2047.0,
            2048.0,
            2049.0,
            2050.0,
            2051.0,
            2052.0,
            2053.0,
            2054.0,
            2055.0,
            2056.0,
            2057.0,
            2058.0,
            2059.0,
            2060.0,
            2061.0,
            2062.0,
            2063.0,
            2064.0,
            2065.0,
            2066.0,
            2067.0,
            2068.0,
            2069.0,
            2070.0,
            2071.0,
            2072.0,
            2073.0,
            2074.0,
            2075.0,
            2076.0,
            2077.0,
            2078.0,
            2079.0,
            2080.0,
            2081.0,
            2082.0,
            2083.0,
            2084.0,
            2085.0,
            2086.0,
            2087.0,
            2088.0,
            2089.0,
            2090.0,
            2091.0,
            2092.0,
            2093.0,
            2094.0,
            2095.0,
            2096.0,
            2097.0,
            2098.0,
            2099.0,
            2100.0,
        ],
        [
            0.474935,
            0.476662,
            0.463615,
            0.452733,
            0.449628,
            0.448761,
            0.448516,
            0.448441,
            0.448411,
            0.448394,
            0.44838,
            0.448367,
            0.448352,
            0.448336,
            0.448318,
            0.448299,
            0.44828,
            0.448261,
            0.448244,
            0.448229,
            0.448217,
            0.448207,
            0.448202,
            0.4482,
            0.448202,
            0.448208,
            0.448219,
            0.448234,
            0.448253,
            0.448277,
            0.448305,
            0.448348,
            0.448444,
            0.448581,
            0.448745,
            0.448924,
            0.449117,
            0.449323,
            0.449542,
            0.449773,
            0.450019,
            0.450278,
            0.450551,
            0.450839,
            0.451142,
            0.451461,
            0.451796,
            0.452147,
            0.452516,
            0.452904,
            0.453311,
            0.453737,
            0.454184,
            0.454652,
            0.455142,
            0.455655,
            0.456192,
            0.456753,
            0.457339,
            0.457948,
            0.458578,
            0.459232,
            0.459911,
            0.460616,
            0.461347,
            0.462105,
            0.46289,
            0.463702,
            0.464541,
            0.465407,
            0.466298,
            0.46721,
            0.46803,
            0.468745,
            0.469423,
            0.470104,
            0.470799,
            0.471512,
            0.472203,
            0.472882,
            0.473569,
            0.474267,
            0.47498,
            0.475706,
            0.476445,
            0.477197,
            0.477961,
            0.478739,
            0.479529,
            0.480331,
            0.481145,
            0.481972,
            0.482811,
            0.483662,
            0.484526,
            0.485402,
            0.48629,
            0.48719,
            0.488102,
            0.489012,
            0.489916,
            0.490824,
            0.49174,
            0.492666,
            0.493603,
            0.494549,
            0.495506,
            0.496472,
            0.497447,
            0.49843,
            0.499422,
            0.500421,
            0.501426,
            0.502437,
            0.503451,
            0.504469,
            0.505476,
            0.506462,
            0.507436,
            0.508405,
            0.509371,
            0.510333,
            0.511291,
            0.512244,
            0.513189,
            0.514126,
            0.515052,
            0.515966,
            0.516863,
            0.517732,
            0.518573,
            0.519394,
            0.520195,
            0.520979,
            0.521746,
            0.522495,
            0.523225,
            0.523936,
            0.524617,
            0.525248,
            0.525838,
            0.526397,
            0.526931,
            0.52744,
            0.527926,
            0.528391,
            0.528833,
            0.529251,
            0.529638,
            0.529995,
            0.530324,
            0.530626,
            0.530905,
            0.531154,
            0.531354,
            0.531519,
            0.531661,
            0.531787,
            0.531897,
            0.53199,
            0.532064,
            0.532121,
            0.532163,
            0.53219,
            0.532203,
            0.532201,
            0.532184,
            0.532153,
            0.532109,
            0.532051,
            0.531975,
            0.531878,
            0.531761,
            0.531626,
            0.531469,
            0.531286,
            0.531074,
            0.530833,
            0.530565,
            0.530267,
            0.529938,
            0.529578,
            0.529201,
            0.528815,
            0.528424,
            0.528025,
            0.527602,
            0.527148,
            0.526675,
            0.526192,
            0.525696,
            0.525183,
            0.52465,
            0.524102,
            0.523539,
            0.522952,
            0.522331,
            0.521661,
            0.520943,
            0.520181,
            0.519385,
        ],
    )


@component.add(
    name="Eff N on Yield Prev",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def eff_n_on_yield_prev():
    return np.interp(
        time(),
        [
            1900.0,
            1901.0,
            1902.0,
            1903.0,
            1904.0,
            1905.0,
            1906.0,
            1907.0,
            1908.0,
            1909.0,
            1910.0,
            1911.0,
            1912.0,
            1913.0,
            1914.0,
            1915.0,
            1916.0,
            1917.0,
            1918.0,
            1919.0,
            1920.0,
            1921.0,
            1922.0,
            1923.0,
            1924.0,
            1925.0,
            1926.0,
            1927.0,
            1928.0,
            1929.0,
            1930.0,
            1931.0,
            1932.0,
            1933.0,
            1934.0,
            1935.0,
            1936.0,
            1937.0,
            1938.0,
            1939.0,
            1940.0,
            1941.0,
            1942.0,
            1943.0,
            1944.0,
            1945.0,
            1946.0,
            1947.0,
            1948.0,
            1949.0,
            1950.0,
            1951.0,
            1952.0,
            1953.0,
            1954.0,
            1955.0,
            1956.0,
            1957.0,
            1958.0,
            1959.0,
            1960.0,
            1961.0,
            1962.0,
            1963.0,
            1964.0,
            1965.0,
            1966.0,
            1967.0,
            1968.0,
            1969.0,
            1970.0,
            1971.0,
            1972.0,
            1973.0,
            1974.0,
            1975.0,
            1976.0,
            1977.0,
            1978.0,
            1979.0,
            1980.0,
            1981.0,
            1982.0,
            1983.0,
            1984.0,
            1985.0,
            1986.0,
            1987.0,
            1988.0,
            1989.0,
            1990.0,
            1991.0,
            1992.0,
            1993.0,
            1994.0,
            1995.0,
            1996.0,
            1997.0,
            1998.0,
            1999.0,
            2000.0,
            2001.0,
            2002.0,
            2003.0,
            2004.0,
            2005.0,
            2006.0,
            2007.0,
            2008.0,
            2009.0,
            2010.0,
            2011.0,
            2012.0,
            2013.0,
            2014.0,
            2015.0,
            2016.0,
            2017.0,
            2018.0,
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
            2024.0,
            2025.0,
            2026.0,
            2027.0,
            2028.0,
            2029.0,
            2030.0,
            2031.0,
            2032.0,
            2033.0,
            2034.0,
            2035.0,
            2036.0,
            2037.0,
            2038.0,
            2039.0,
            2040.0,
            2041.0,
            2042.0,
            2043.0,
            2044.0,
            2045.0,
            2046.0,
            2047.0,
            2048.0,
            2049.0,
            2050.0,
            2051.0,
            2052.0,
            2053.0,
            2054.0,
            2055.0,
            2056.0,
            2057.0,
            2058.0,
            2059.0,
            2060.0,
            2061.0,
            2062.0,
            2063.0,
            2064.0,
            2065.0,
            2066.0,
            2067.0,
            2068.0,
            2069.0,
            2070.0,
            2071.0,
            2072.0,
            2073.0,
            2074.0,
            2075.0,
            2076.0,
            2077.0,
            2078.0,
            2079.0,
            2080.0,
            2081.0,
            2082.0,
            2083.0,
            2084.0,
            2085.0,
            2086.0,
            2087.0,
            2088.0,
            2089.0,
            2090.0,
            2091.0,
            2092.0,
            2093.0,
            2094.0,
            2095.0,
            2096.0,
            2097.0,
            2098.0,
            2099.0,
            2100.0,
        ],
        [
            0.442961,
            0.453031,
            0.452814,
            0.452751,
            0.453009,
            0.453098,
            0.453029,
            0.45289,
            0.45273,
            0.452566,
            0.452403,
            0.452239,
            0.452073,
            0.451904,
            0.451733,
            0.451561,
            0.451391,
            0.451227,
            0.451069,
            0.450919,
            0.450779,
            0.450648,
            0.450528,
            0.450419,
            0.450322,
            0.450236,
            0.450162,
            0.4501,
            0.45005,
            0.450011,
            0.449982,
            0.449974,
            0.450089,
            0.450301,
            0.450562,
            0.450854,
            0.451173,
            0.45152,
            0.451894,
            0.452299,
            0.452734,
            0.453202,
            0.453702,
            0.454237,
            0.454807,
            0.455414,
            0.456059,
            0.456745,
            0.457473,
            0.458245,
            0.459062,
            0.459927,
            0.460842,
            0.461806,
            0.462823,
            0.463895,
            0.465023,
            0.466208,
            0.467452,
            0.468756,
            0.47012,
            0.471544,
            0.473026,
            0.474566,
            0.476164,
            0.477821,
            0.479535,
            0.481305,
            0.483129,
            0.485004,
            0.486927,
            0.488895,
            0.490604,
            0.492006,
            0.493359,
            0.494742,
            0.496165,
            0.497627,
            0.499126,
            0.500665,
            0.502242,
            0.503855,
            0.5055,
            0.507174,
            0.508877,
            0.510607,
            0.512364,
            0.514147,
            0.515954,
            0.517786,
            0.519642,
            0.521521,
            0.523423,
            0.525347,
            0.527294,
            0.529262,
            0.531251,
            0.53326,
            0.535286,
            0.537267,
            0.539221,
            0.541183,
            0.543161,
            0.545155,
            0.547165,
            0.549188,
            0.551223,
            0.55327,
            0.555324,
            0.557387,
            0.559454,
            0.561525,
            0.563596,
            0.565663,
            0.567725,
            0.569777,
            0.571756,
            0.573654,
            0.575517,
            0.577359,
            0.579181,
            0.58098,
            0.582752,
            0.584494,
            0.586204,
            0.587877,
            0.589512,
            0.591106,
            0.592637,
            0.594071,
            0.595437,
            0.596752,
            0.59802,
            0.599243,
            0.60042,
            0.601554,
            0.602645,
            0.603696,
            0.60466,
            0.605489,
            0.606246,
            0.606959,
            0.607637,
            0.608281,
            0.608896,
            0.609487,
            0.610055,
            0.610599,
            0.611117,
            0.611609,
            0.612078,
            0.612531,
            0.61297,
            0.613353,
            0.613636,
            0.613879,
            0.614106,
            0.614321,
            0.614522,
            0.614705,
            0.614872,
            0.615019,
            0.615144,
            0.615241,
            0.615303,
            0.615326,
            0.615307,
            0.615243,
            0.615135,
            0.614982,
            0.614778,
            0.614526,
            0.614225,
            0.613877,
            0.613479,
            0.613027,
            0.612519,
            0.611956,
            0.611344,
            0.610679,
            0.609949,
            0.609153,
            0.608304,
            0.607415,
            0.606483,
            0.605507,
            0.604465,
            0.603343,
            0.602163,
            0.600944,
            0.599678,
            0.598355,
            0.596973,
            0.595541,
            0.594062,
            0.592522,
            0.590906,
            0.589189,
            0.587375,
            0.585478,
            0.583512,
        ],
    )


@component.add(
    name="Fertilizer Efficiency",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fertilizer_efficiency():
    """
    Ton Crop / Ton fertilizer: 21.8 if related to consumption
    """
    return 100


@component.add(
    name="Normal perceived climate change",
    units="DegreesC",
    subscripts=["Education"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_perceived_climate_change():
    """
    2010 values, used ofr normalization
    """
    return xr.DataArray(
        [0.6212, 0.7562, 0.8162, 0.8852],
        {"Education": _subscript_dict["Education"]},
        ["Education"],
    )


@component.add(
    name="Transmission rate",
    units="Dmnl",
    subscripts=["Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def transmission_rate():
    """
    BAU: 1, 1, 2, 5, 5, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1 For StrongerImpact: 1, 1, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 3, 3, 3, 1, 1, 1, 1, 1, 1
    """
    return xr.DataArray(
        [
            1.0,
            1.0,
            2.0,
            5.0,
            5.0,
            4.0,
            4.0,
            4.0,
            3.0,
            3.0,
            3.0,
            3.0,
            2.0,
            2.0,
            2.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
        ],
        {"Cohorts": _subscript_dict["Cohorts"]},
        ["Cohorts"],
    )


@component.add(
    name="MIN Fertility", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def min_fertility():
    """
    The minimal level of the fertility. Logically set to 1 child.
    """
    return 1


@component.add(
    name="Forest Protected Land constant",
    units="m*m",
    comp_type="Constant",
    comp_subtype="Normal",
)
def forest_protected_land_constant():
    """
    Area of Forest Land not transformable into other kind of lands.
    """
    return 4786320000000.0
