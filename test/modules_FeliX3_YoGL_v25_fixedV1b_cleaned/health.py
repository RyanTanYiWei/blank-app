"""
Module health
Translated using PySD version 3.14.3
"""

@component.add(
    name="a GDP HLE",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gdp_hle_impact_variation": 1, "time": 1},
)
def a_gdp_hle():
    """
    value calibrated to the historical data for HLE at birth, taking food effect into account
    """
    return 0.979513 + ramp(
        __data["time"],
        (gdp_hle_impact_variation() * 0.979513 - 0.979513) / 78,
        2022,
        2100,
    )


@component.add(
    name="b GDP HLE", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def b_gdp_hle():
    """
    value calibrated according to the historical HLE at birth values, taking food effect into account
    """
    return 0.0629177


@component.add(
    name="Effect of food supply on HLE",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ratio_of_sugar_and_oil_supply_to_its_reference_value": 1,
        "lookup_for_the_effect_of_food_on_hle": 1,
    },
)
def effect_of_food_supply_on_hle():
    return lookup_for_the_effect_of_food_on_hle(
        ratio_of_sugar_and_oil_supply_to_its_reference_value()
    )


@component.add(
    name="Effect of GDP pc on HLE",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"a_gdp_hle": 1, "ratio_of_gdp_pc_to_the_reference": 1, "b_gdp_hle": 1},
)
def effect_of_gdp_pc_on_hle():
    return a_gdp_hle() * ratio_of_gdp_pc_to_the_reference() ** b_gdp_hle()


@component.add(
    name="Effect of LE on HLE",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_effect_of_le_on_hle"},
)
def effect_of_le_on_hle(x, final_subs=None):
    """
    Fuzzy min formulation to make sure that HLE does not exceed LE
    """
    return _hardcodedlookup_effect_of_le_on_hle(x, final_subs)


_hardcodedlookup_effect_of_le_on_hle = HardcodedLookups(
    [0.0, 0.5, 0.9, 0.95, 1.05, 1.1],
    [0.0, 0.5, 0.9, 0.95, 1.0, 1.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_effect_of_le_on_hle",
)


@component.add(
    name="Food supply sugar and oil variation",
    units="kcal/(Person*Day)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def food_supply_sugar_and_oil_variation():
    return 650.2


@component.add(
    name="GDP HLE Impact variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def gdp_hle_impact_variation():
    return 1


@component.add(
    name="HALE coefficient for age",
    units="Dmnl",
    subscripts=["Gender", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def hale_coefficient_for_age():
    """
    The ratio of HALE at age gorups between 1-95+ to the HALE at birth has been almost constant (<10% change, <5% change in the age groups below 75) over time between 1990 and 2019. Therefore, we assume that HALE is a constrant fraction of HALE at birth. These constants are the average of the ratio "HALE / HALE at birth" over time.
    """
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )
    value.loc[["male"], :] = xr.DataArray(
        [
            [
                1.032,
                0.987,
                0.91,
                0.833,
                0.758,
                0.685,
                0.613,
                0.543,
                0.475,
                0.41,
                0.347,
                0.288,
                0.235,
                0.186,
                0.144,
                0.109,
                0.08,
                0.058,
                0.044,
                0.033,
                0.033,
            ]
        ],
        {"Gender": ["male"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    ).values
    value.loc[["female"], :] = xr.DataArray(
        [
            [
                1.027,
                0.985,
                0.912,
                0.837,
                0.766,
                0.696,
                0.628,
                0.562,
                0.497,
                0.433,
                0.372,
                0.313,
                0.258,
                0.207,
                0.161,
                0.122,
                0.089,
                0.064,
                0.046,
                0.032,
                0.032,
            ]
        ],
        {"Gender": ["female"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    ).values
    return value


@component.add(
    name="Healthy life expectancy",
    units="Year",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"healthy_life_expectancy_at_birth": 1, "hale_coefficient_for_age": 1},
)
def healthy_life_expectancy():
    return healthy_life_expectancy_at_birth() * hale_coefficient_for_age()


@component.add(
    name="Healthy life expectancy at birth",
    units="Year",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "life_expectancy_at_birth": 1,
        "ratio_of_indicative_hle_to_le": 1,
        "effect_of_le_on_hle": 1,
    },
)
def healthy_life_expectancy_at_birth():
    return life_expectancy_at_birth() * effect_of_le_on_hle(
        ratio_of_indicative_hle_to_le(), {"Gender": ["male", "female"]}
    )


@component.add(
    name="Indicative healthy life expectancy at birth",
    units="Year",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_healthy_life_expectancy_at_birth": 1,
        "effect_of_food_supply_on_hle": 1,
        "effect_of_gdp_pc_on_hle": 1,
    },
)
def indicative_healthy_life_expectancy_at_birth():
    return (
        reference_healthy_life_expectancy_at_birth()
        * effect_of_food_supply_on_hle()
        * effect_of_gdp_pc_on_hle()
    )


@component.add(
    name="Lookup for the effect of food on HLE",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_lookup_for_the_effect_of_food_on_hle"},
)
def lookup_for_the_effect_of_food_on_hle(x, final_subs=None):
    """
    Inverted U-shaped function estimated based on the Food supply - BMI - HALE relationship across all countries and years. Food supply data from FAO, BMI and HALE data from IHME.
    """
    return _hardcodedlookup_lookup_for_the_effect_of_food_on_hle(x, final_subs)


_hardcodedlookup_lookup_for_the_effect_of_food_on_hle = HardcodedLookups(
    [
        0.09,
        0.19,
        0.28,
        0.37,
        0.46,
        0.56,
        0.65,
        0.74,
        0.83,
        0.93,
        1.02,
        1.11,
        1.2,
        1.3,
        1.39,
        1.48,
        1.57,
        1.67,
        1.76,
        1.85,
        1.94,
        2.04,
        2.13,
        2.22,
        2.31,
        2.41,
        2.5,
        2.59,
        2.69,
        2.78,
        2.87,
        2.96,
    ],
    [
        0.83,
        0.85,
        0.87,
        0.89,
        0.92,
        0.94,
        0.96,
        0.96,
        0.96,
        0.98,
        1.02,
        1.06,
        1.08,
        1.09,
        1.11,
        1.12,
        1.12,
        1.13,
        1.15,
        1.16,
        1.18,
        1.18,
        1.17,
        1.15,
        1.13,
        1.1,
        1.07,
        1.03,
        0.99,
        0.95,
        0.91,
        0.87,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_lookup_for_the_effect_of_food_on_hle",
)


@component.add(
    name="Ratio of Indicative HLE to LE",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "indicative_healthy_life_expectancy_at_birth": 1,
        "life_expectancy_at_birth": 1,
    },
)
def ratio_of_indicative_hle_to_le():
    return indicative_healthy_life_expectancy_at_birth() / life_expectancy_at_birth()


@component.add(
    name="Ratio of sugar and oil supply to its reference value",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "daily_caloric_supply_per_capita": 1,
        "reference_supply_of_sugar_and_oil_calories": 1,
    },
)
def ratio_of_sugar_and_oil_supply_to_its_reference_value():
    return (
        float(daily_caloric_supply_per_capita().loc["OtherCrops"])
        / reference_supply_of_sugar_and_oil_calories()
    )


@component.add(
    name="Reference healthy life expectancy at birth",
    units="Year",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_healthy_life_expectancy_at_birth():
    """
    The global average data value in year 2000, reported by Institute for Health Metrics and Evaluation (IHME).
    """
    return xr.DataArray(
        [57.35, 59.84], {"Gender": _subscript_dict["Gender"]}, ["Gender"]
    )


@component.add(
    name="Reference supply of sugar and oil calories",
    units="kcal/(Person*Day)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"food_supply_sugar_and_oil_variation": 1, "time": 1},
)
def reference_supply_of_sugar_and_oil_calories():
    """
    Daily caloric supply per person from sugar, sugar crops, oil crops and vegetable oils in year 2000. Data obtained from FAO Food Balance Sheets. 540
    """
    return 650.2 + ramp(
        __data["time"], (food_supply_sugar_and_oil_variation() - 650.2) / 78, 2022, 2100
    )
