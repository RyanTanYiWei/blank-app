"""
Module climate_damage
Translated using PySD version 3.14.3
"""

@component.add(
    name="alpha Nordhaus damage",
    units="1/DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def alpha_nordhaus_damage():
    return -0.00118


@component.add(
    name="beta Nordhaus damage",
    units="1/(DegreesC*DegreesC)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def beta_nordhaus_damage():
    return 0.00278


@component.add(
    name="Burke Damage long term pooled",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "temperature_change_from_preindustrial": 1,
        "unit_degreesc": 1,
        "burke_damage_long_term_pooled_lookup": 1,
    },
)
def burke_damage_long_term_pooled():
    return burke_damage_long_term_pooled_lookup(
        temperature_change_from_preindustrial() / unit_degreesc()
    )


@component.add(
    name="Burke Damage long term pooled Lookup",
    units="percent",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_burke_damage_long_term_pooled_lookup"},
)
def burke_damage_long_term_pooled_lookup(x, final_subs=None):
    """
    Damage estimate according to Burket et al. 2015 Nature Fig. 4d
    """
    return _hardcodedlookup_burke_damage_long_term_pooled_lookup(x, final_subs)


_hardcodedlookup_burke_damage_long_term_pooled_lookup = HardcodedLookups(
    [0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
    [0.0, 6.3, 35.0, 55.0, 68.7, 80.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_burke_damage_long_term_pooled_lookup",
)


@component.add(
    name="Burke Damage short term pooled",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "temperature_change_from_preindustrial": 1,
        "unit_degreesc": 1,
        "burke_damage_short_term_pooled_lookup": 1,
    },
)
def burke_damage_short_term_pooled():
    return burke_damage_short_term_pooled_lookup(
        temperature_change_from_preindustrial() / unit_degreesc()
    )


@component.add(
    name="Burke Damage short term pooled Lookup",
    units="percent",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_burke_damage_short_term_pooled_lookup"},
)
def burke_damage_short_term_pooled_lookup(x, final_subs=None):
    """
    Damage estimate according to Burket et al. 2015 Nature Fig. 4d
    """
    return _hardcodedlookup_burke_damage_short_term_pooled_lookup(x, final_subs)


_hardcodedlookup_burke_damage_short_term_pooled_lookup = HardcodedLookups(
    [0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
    [0.0, 1.0, 13.0, 19.0, 20.5, 21.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_burke_damage_short_term_pooled_lookup",
)


@component.add(
    name="Climate Damage Fraction OLD",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "climate_damage_scale": 1,
        "reference_temperature": 1,
        "temperature_change_from_preindustrial": 1,
        "climate_damage_nonlinearity": 1,
    },
)
def climate_damage_fraction_old():
    """
    Fraction of Output lost to Climate Change as a function of temperature rise. A logistic function is chosen to formulate climate damages due to its flexibility to capture various damage function estimates such as Nordhaus and Dietz&Stern ( exponential) or Burke (logarithmic).
    """
    return 1 / (
        1
        + climate_damage_scale()
        * (temperature_change_from_preindustrial() / reference_temperature())
        ** climate_damage_nonlinearity()
    )


@component.add(
    name="Climate Damage Function SWITCH",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_damage_function_switch():
    """
    0 : 0 1 : Nordhaus 2 : Dietz&Stern 3 : Burke short term pooled 4 : Burke long term pooled 5 : Logistic function defined by three parameters
    """
    return 4


@component.add(
    name="Climate Damage Inflection",
    units="DegreesC",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "climate_damage_inflection_0": 1,
        "_smooth_climate_damage_inflection": 1,
    },
    other_deps={
        "_smooth_climate_damage_inflection": {
            "initial": {
                "climate_damage_inflection_sa": 1,
                "climate_damage_inflection_0": 1,
                "current_year": 1,
                "time": 1,
            },
            "step": {
                "climate_damage_inflection_sa": 1,
                "climate_damage_inflection_0": 1,
                "current_year": 1,
                "time": 1,
                "sa_effective_change_delay": 1,
            },
        }
    },
)
def climate_damage_inflection():
    """
    This function starts with the parameter values defined by the original calibration (parameter "...0") e.g. to Nordhaus, until the present year, and it allows for user-defined values to cover future uncertainty (parameter "... SA").
    """
    return climate_damage_inflection_0() + _smooth_climate_damage_inflection()


_smooth_climate_damage_inflection = Smooth(
    lambda: step(
        __data["time"],
        climate_damage_inflection_sa() - climate_damage_inflection_0(),
        current_year(),
    ),
    lambda: sa_effective_change_delay(),
    lambda: step(
        __data["time"],
        climate_damage_inflection_sa() - climate_damage_inflection_0(),
        current_year(),
    ),
    lambda: 3,
    "_smooth_climate_damage_inflection",
)


@component.add(
    name="Climate Damage Inflection 0",
    units="DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_damage_inflection_0():
    """
    Nordhaus : 3.89219 D&S : 3.863367 Burke st : 1.773525 Burke lt : 2.2569
    """
    return 2.2569


@component.add(
    name="Climate Damage Inflection SA",
    units="DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_damage_inflection_sa():
    """
    Nordhaus : 3.89219 D&S : 3.863367 Burke st : 1.773525 Burke lt : 2.2569
    """
    return 2.2569


@component.add(
    name="Climate Damage Nonlinearity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_damage_nonlinearity():
    """
    Nonlinearity of Climate Damage Cost Fraction.
    """
    return 2


@component.add(
    name="Climate Damage Percentage",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "climate_damage_function_switch": 5,
        "logistic_damage": 1,
        "nordhaus_damage": 1,
        "dietz_and_stern_damage": 1,
        "burke_damage_long_term_pooled": 1,
        "burke_damage_short_term_pooled": 1,
    },
)
def climate_damage_percentage():
    """
    Can be set either to predefined functions according to the literature, or to a flexible logistic function that can capture a wide uncertainty range.
    """
    return if_then_else(
        climate_damage_function_switch() == 0,
        lambda: 0,
        lambda: if_then_else(
            climate_damage_function_switch() == 1,
            lambda: nordhaus_damage(),
            lambda: if_then_else(
                climate_damage_function_switch() == 2,
                lambda: dietz_and_stern_damage(),
                lambda: if_then_else(
                    climate_damage_function_switch() == 3,
                    lambda: burke_damage_short_term_pooled(),
                    lambda: if_then_else(
                        climate_damage_function_switch() == 4,
                        lambda: burke_damage_long_term_pooled(),
                        lambda: logistic_damage(),
                    ),
                ),
            ),
        ),
    )


@component.add(
    name="Climate Damage Saturation",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "climate_damage_saturation_0": 1,
        "_smooth_climate_damage_saturation": 1,
    },
    other_deps={
        "_smooth_climate_damage_saturation": {
            "initial": {
                "climate_damage_saturation_sa": 1,
                "climate_damage_saturation_0": 1,
                "current_year": 1,
                "time": 1,
            },
            "step": {
                "climate_damage_saturation_sa": 1,
                "climate_damage_saturation_0": 1,
                "current_year": 1,
                "time": 1,
                "sa_effective_change_delay": 1,
            },
        }
    },
)
def climate_damage_saturation():
    """
    This function starts with the parameter values defined by the original calibration (parameter "...0") e.g. to Nordhaus, until the present year, and it allows for user-defined values to cover future uncertainty (parameter "... SA").
    """
    return climate_damage_saturation_0() + _smooth_climate_damage_saturation()


_smooth_climate_damage_saturation = Smooth(
    lambda: step(
        __data["time"],
        climate_damage_saturation_sa() - climate_damage_saturation_0(),
        current_year(),
    ),
    lambda: sa_effective_change_delay(),
    lambda: step(
        __data["time"],
        climate_damage_saturation_sa() - climate_damage_saturation_0(),
        current_year(),
    ),
    lambda: 3,
    "_smooth_climate_damage_saturation",
)


@component.add(
    name="Climate Damage Saturation 0",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_damage_saturation_0():
    """
    Nordhaus: 0.073953 Dietz&Stern:0.935478 Burke st : 0.206988 Burke lt : 0.75716
    """
    return 0.75716


@component.add(
    name="Climate Damage Saturation SA",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_damage_saturation_sa():
    """
    Nordhaus: 0.073953 Dietz&Stern:0.935478 Burke st : 0.206988 Burke lt : 0.75716
    """
    return 0.75716


@component.add(
    name="Climate Damage Scale",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_damage_scale():
    """
    Climate Damage Fraction at Reference Temperature.
    """
    return 0.013


@component.add(
    name="Climate Damage Steepness",
    units="1/DegreesC",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"climate_damage_steepness_0": 1, "_smooth_climate_damage_steepness": 1},
    other_deps={
        "_smooth_climate_damage_steepness": {
            "initial": {
                "climate_damage_steepness_sa": 1,
                "climate_damage_steepness_0": 1,
                "current_year": 1,
                "time": 1,
            },
            "step": {
                "climate_damage_steepness_sa": 1,
                "climate_damage_steepness_0": 1,
                "current_year": 1,
                "time": 1,
                "sa_effective_change_delay": 1,
            },
        }
    },
)
def climate_damage_steepness():
    """
    This function starts with the parameter values defined by the original calibration (parameter "...0") e.g. to Nordhaus, until the present year, and it allows for user-defined values to cover future uncertainty (parameter "... SA").
    """
    return climate_damage_steepness_0() + _smooth_climate_damage_steepness()


_smooth_climate_damage_steepness = Smooth(
    lambda: step(
        __data["time"],
        climate_damage_steepness_sa() - climate_damage_steepness_0(),
        current_year(),
    ),
    lambda: sa_effective_change_delay(),
    lambda: step(
        __data["time"],
        climate_damage_steepness_sa() - climate_damage_steepness_0(),
        current_year(),
    ),
    lambda: 3,
    "_smooth_climate_damage_steepness",
)


@component.add(
    name="Climate Damage Steepness 0",
    units="1/DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_damage_steepness_0():
    """
    Nonlinearity of Climate Damage Fraction. Nordhaus :1.09955 D&S : 1.795846 Burke st:1.888017 Burke lt:1.43089
    """
    return 1.43089


@component.add(
    name="Climate Damage Steepness SA",
    units="1/DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_damage_steepness_sa():
    """
    Nonlinearity of Climate Damage Fraction. Nordhaus :1.09955 D&S : 1.795846 Burke st:1.888017 Burke lt:1.43089
    """
    return 1.43089


@component.add(
    name="denom1 DietzStern",
    units="DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def denom1_dietzstern():
    return 12.2


@component.add(
    name="denom2 DietzStern",
    units="DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def denom2_dietzstern():
    return 4


@component.add(
    name="Dietz and Stern Damage",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nvs_100_percent": 1,
        "exp2_dietzstern": 1,
        "denom1_dietzstern": 1,
        "exp1_dietzstern": 1,
        "temperature_change_from_preindustrial": 2,
        "denom2_dietzstern": 1,
    },
)
def dietz_and_stern_damage():
    """
    Formulation of the original damage function used by Dietz and Stern in the Economic Journal (2015) paper. https://doi.org/10.1111/ecoj.12188
    """
    return nvs_100_percent() * (
        1
        - 1
        / (
            1
            + (temperature_change_from_preindustrial() / denom1_dietzstern())
            ** exp1_dietzstern()
            + (temperature_change_from_preindustrial() / denom2_dietzstern())
            ** exp2_dietzstern()
        )
    )


@component.add(
    name="exp1 DietzStern", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def exp1_dietzstern():
    return 2


@component.add(
    name="exp2 DietzStern", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def exp2_dietzstern():
    return 7.02


@component.add(
    name="Logistic Damage",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nvs_100_percent": 1,
        "climate_damage_saturation": 1,
        "climate_damage_steepness": 1,
        "climate_damage_inflection": 1,
        "temperature_change_from_preindustrial": 1,
    },
)
def logistic_damage():
    """
    Fraction of Output lost to Climate Change as a function of temperature rise. A logistic function is chosen to formulate climate damages due to its flexibility to capture various damage function estimates such as Nordhaus and Dietz&Stern ( exponential) or Burke (logarithmic).
    """
    return (
        nvs_100_percent()
        * climate_damage_saturation()
        / (
            1
            + float(
                np.exp(
                    -climate_damage_steepness()
                    * (
                        temperature_change_from_preindustrial()
                        - climate_damage_inflection()
                    )
                )
            )
        )
    )


@component.add(
    name="Net Climate Change Impact on Economy",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"climate_damage_percentage": 1, "nvs_100_percent": 1},
)
def net_climate_change_impact_on_economy():
    """
    The fraction of ecomomy output after loss due to climate change.
    """
    return 1 - climate_damage_percentage() / nvs_100_percent()


@component.add(
    name="Nordhaus Damage",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nvs_100_percent": 1,
        "beta_nordhaus_damage": 1,
        "temperature_change_from_preindustrial": 2,
        "alpha_nordhaus_damage": 1,
    },
)
def nordhaus_damage():
    """
    Formulation of the original damage function used by Nordhaus in PNAS (2017) paper.
    """
    return nvs_100_percent() * (
        1
        - 1
        / (
            1
            + alpha_nordhaus_damage() * temperature_change_from_preindustrial()
            + beta_nordhaus_damage() * temperature_change_from_preindustrial() ** 2
        )
    )


@component.add(
    name='"100 percent"', units="percent", comp_type="Constant", comp_subtype="Normal"
)
def nvs_100_percent():
    return 100


@component.add(
    name="Reference Temperature",
    units="DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_temperature():
    """
    Reference Temperature for Calculation of Climate Damages.
    """
    return 3


@component.add(
    name="unit DegreesC", units="DegreesC", comp_type="Constant", comp_subtype="Normal"
)
def unit_degreesc():
    return 1
