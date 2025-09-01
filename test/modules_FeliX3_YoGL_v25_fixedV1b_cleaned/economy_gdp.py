"""
Module economy_gdp
Translated using PySD version 3.14.3
"""

@component.add(
    name="Adjustments for relative incomes of skilled",
    units="Dmnl",
    subscripts=["Gender", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def adjustments_for_relative_incomes_of_skilled():
    """
    to adjust the relative incomes of skilled labor force of each population group Two assumptions: (1) the relationship between income and age tends to exhibit an inverted-U-shape pattern. Incomes rise with age and then drop slightly as taxpayers enter retirement. (2) Male has more incomes than female in the same age group.
    """
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )
    value.loc[["male"], _subscript_dict["Childhood"]] = 0.77
    value.loc[["male"], _subscript_dict['"15 to 39"']] = 1.05
    value.loc[["male"], _subscript_dict['"40 to 64"']] = 1.2
    value.loc[["male"], _subscript_dict['"65 plus"']] = 1.22
    value.loc[["female"], _subscript_dict["Childhood"]] = 0.77
    value.loc[["female"], _subscript_dict['"15 to 39"']] = 1
    value.loc[["female"], _subscript_dict['"40 to 64"']] = 1.07
    value.loc[["female"], _subscript_dict['"65 plus"']] = 1.05
    return value


@component.add(
    name="Biomass Technology",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_capacity_factor": 1,
        "maxbcf": 1,
        "biomass_installation_efficiency": 1,
        "maxbie": 1,
    },
)
def biomass_technology():
    """
    Factor productivity in Biomass energy sector.
    """
    return (
        biomass_capacity_factor() / maxbcf()
        + biomass_installation_efficiency() / maxbie()
    ) / 2


@component.add(
    name="Capital",
    units="$",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_capital": 1},
    other_deps={
        "_integ_capital": {
            "initial": {"init_capital": 1},
            "step": {"net_capital_change_rate": 1},
        }
    },
)
def capital():
    """
    Capital stock. Source of historical data: http://www.ggdc.net/MADDISON/oriindex.htm
    """
    return _integ_capital()


_integ_capital = Integ(
    lambda: net_capital_change_rate(), lambda: init_capital(), "_integ_capital"
)


@component.add(
    name="Capital Elasticity Output",
    units="Dmnl",
    subscripts=["Labor force type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cs": 1, "cu": 1},
)
def capital_elasticity_output():
    """
    CE Var S+SMOOTH(STEP(Capital Elasticity Output Variation-CE Var S, 2020+SE Var T),SSP Economic Variation Time)
    """
    value = xr.DataArray(
        np.nan,
        {"Labor force type": _subscript_dict["Labor force type"]},
        ["Labor force type"],
    )
    value.loc[["skill"]] = cs()
    value.loc[["unskill"]] = cu()
    return value


@component.add(
    name="Capital Elasticity Output Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def capital_elasticity_output_variation():
    """
    Capital Elasticity of Output.
    """
    return 0.425


@component.add(name="CE S", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def ce_s():
    """
    Capital Elasticity of Output.
    """
    return 0.425


@component.add(
    name="CE Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_ce_var_s": 1},
    other_deps={
        "_smooth_ce_var_s": {
            "initial": {"ce_s": 1, "time": 1},
            "step": {"ce_s": 1, "time": 1},
        }
    },
)
def ce_var_s():
    """
    Capital Elasticity of Output.
    """
    return 0.425 + _smooth_ce_var_s()


_smooth_ce_var_s = Smooth(
    lambda: step(__data["time"], ce_s() - 0.425, 2020),
    lambda: 1,
    lambda: step(__data["time"], ce_s() - 0.425, 2020),
    lambda: 1,
    "_smooth_ce_var_s",
)


@component.add(
    name="Coal Technology",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "coal_fraction_discoverable": 1,
        "maxcfd": 1,
        "maxcfr": 1,
        "coal_fraction_recoverable": 1,
    },
)
def coal_technology():
    """
    Factor productivity in Coal energy sector.
    """
    return (
        coal_fraction_discoverable() / maxcfd() + coal_fraction_recoverable() / maxcfr()
    ) / 2


@component.add(
    name="Consumption or income of a person per day",
    units="$/(Person*Day)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def consumption_or_income_of_a_person_per_day():
    """
    $2.15 a day (2017PPP) $1.9 a day (2011PPP)
    """
    return 2.15


@component.add(
    name="Cs",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_cs": 1},
    other_deps={
        "_smooth_cs": {
            "initial": {"cs_sa": 1, "current_year": 1, "time": 1},
            "step": {
                "cs_sa": 1,
                "current_year": 1,
                "time": 1,
                "sa_effective_change_delay": 1,
            },
        }
    },
)
def cs():
    return 0.595487 + _smooth_cs()


_smooth_cs = Smooth(
    lambda: step(__data["time"], cs_sa() - 0.595487, current_year()),
    lambda: sa_effective_change_delay(),
    lambda: step(__data["time"], cs_sa() - 0.595487, current_year()),
    lambda: 1,
    "_smooth_cs",
)


@component.add(name="Cs SA", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def cs_sa():
    """
    From calibration. Comment by Q. Ye in July 2024
    """
    return 0.595487


@component.add(
    name="Cu",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_cu": 1},
    other_deps={
        "_smooth_cu": {
            "initial": {"cu_sa": 1, "current_year": 1, "time": 1},
            "step": {
                "cu_sa": 1,
                "current_year": 1,
                "time": 1,
                "sa_effective_change_delay": 1,
            },
        }
    },
)
def cu():
    return 0.133783 + _smooth_cu()


_smooth_cu = Smooth(
    lambda: step(__data["time"], cu_sa() - 0.133783, current_year()),
    lambda: sa_effective_change_delay(),
    lambda: step(__data["time"], cu_sa() - 0.133783, current_year()),
    lambda: 1,
    "_smooth_cu",
)


@component.add(name="Cu SA", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def cu_sa():
    """
    From calibration. Comment by Q. Ye in July 2024.
    """
    return 0.133783


@component.add(
    name="Current to Max Other Capital",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "other_capital_change_ratio": 1,
        "reference_other_capital_change": 1,
        "other_capital_change": 1,
    },
)
def current_to_max_other_capital():
    """
    Adjustment of current to reference other capital change.
    """
    return other_capital_change_ratio() * (
        1 - other_capital_change() / reference_other_capital_change()
    )


@component.add(
    name="DemoFeliX target year",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def demofelix_target_year():
    return 2030


@component.add(
    name="Energy Technology",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "oil_technology": 1,
        "coal_technology": 1,
        "gas_technology": 1,
        "biomass_technology": 1,
        "solar_technology": 1,
        "wind_technology": 1,
    },
)
def energy_technology():
    """
    Factor productivity in energy sector.
    """
    return (
        oil_technology()
        + coal_technology()
        + gas_technology()
        + biomass_technology()
        + solar_technology()
        + wind_technology()
    )


@component.add(
    name="Fraction of skilled secondary education graduates",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "skilled_fraction_of_secondary_education_graduates_baseline": 1,
        "_smooth_fraction_of_skilled_secondary_education_graduates": 1,
    },
    other_deps={
        "_smooth_fraction_of_skilled_secondary_education_graduates": {
            "initial": {
                "skilled_fraction_of_secondary_education_graduates": 1,
                "skilled_fraction_of_secondary_education_graduates_baseline": 1,
                "current_year": 2,
                "demofelix_target_year": 2,
                "time": 1,
            },
            "step": {
                "skilled_fraction_of_secondary_education_graduates": 1,
                "skilled_fraction_of_secondary_education_graduates_baseline": 1,
                "current_year": 2,
                "demofelix_target_year": 2,
                "time": 1,
            },
        }
    },
)
def fraction_of_skilled_secondary_education_graduates():
    """
    the value was obtained by the model calibration.
    """
    return (
        skilled_fraction_of_secondary_education_graduates_baseline()
        + _smooth_fraction_of_skilled_secondary_education_graduates()
    )


_smooth_fraction_of_skilled_secondary_education_graduates = Smooth(
    lambda: ramp(
        __data["time"],
        (
            skilled_fraction_of_secondary_education_graduates()
            - skilled_fraction_of_secondary_education_graduates_baseline()
        )
        / (demofelix_target_year() - current_year()),
        current_year(),
        demofelix_target_year(),
    ),
    lambda: 5,
    lambda: ramp(
        __data["time"],
        (
            skilled_fraction_of_secondary_education_graduates()
            - skilled_fraction_of_secondary_education_graduates_baseline()
        )
        / (demofelix_target_year() - current_year()),
        current_year(),
        demofelix_target_year(),
    ),
    lambda: 1,
    "_smooth_fraction_of_skilled_secondary_education_graduates",
)


@component.add(
    name="Gas Technology",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gas_fraction_discoverable": 1,
        "maxgfd": 1,
        "gas_fraction_recoverable": 1,
        "maxgfr": 1,
    },
)
def gas_technology():
    """
    Factor productivity in Gas energy sector.
    """
    return (
        gas_fraction_discoverable() / maxgfd() + gas_fraction_recoverable() / maxgfr()
    ) / 2


@component.add(
    name="GDP per Capita GLOBIOM usd",
    units="$/(Year*Person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gwp_per_capita": 1},
)
def gdp_per_capita_globiom_usd():
    """
    Projection of GDP per Capita according to GLOBIOM model. Source of projection data: GLOBIOM model, IIASA.
    """
    return gwp_per_capita()


@component.add(
    name="Gini1",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "unskilled_population": 1,
        "relative_incomes_of_unskilled": 2,
        "skilled_population": 1,
        "relative_incomes_of_skilled": 1,
        "total_relative_incomes": 1,
        "population_cohorts": 1,
    },
)
def gini1():
    """
    if using the shares variables, the equation is: 1-(population share of unskilled*income share of unskilled+population share of skilled*(income share of unskilled+1))
    """
    return 1 - (
        unskilled_population() * relative_incomes_of_unskilled()
        + (2 * relative_incomes_of_unskilled() + relative_incomes_of_skilled())
        * skilled_population()
    ) / (population_cohorts() * total_relative_incomes())


@component.add(
    name="Gini2",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "skilled_population": 1,
        "relative_incomes_of_skilled": 2,
        "relative_incomes_of_unskilled": 1,
        "unskilled_population": 1,
        "total_relative_incomes": 1,
        "population_cohorts": 1,
    },
)
def gini2():
    """
    if using the shares variables, the equation is: 1-(population share of skilled*income share of skilled+population share of unskilled*(income share of skilled+1))
    """
    return 1 - (
        skilled_population() * relative_incomes_of_skilled()
        + (2 * relative_incomes_of_skilled() + relative_incomes_of_unskilled())
        * unskilled_population()
    ) / (population_cohorts() * total_relative_incomes())


@component.add(
    name="Gini coefficient",
    units="Dmnl",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gini1": 2, "gini2": 1},
)
def gini_coefficient():
    """
    To make sure the value of Gini coefficient>0
    """
    return if_then_else(gini1() > 0, lambda: gini1(), lambda: gini2())


@component.add(
    name="Global poverty rate",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"poverty_rate": 1, "population_cohorts": 2},
)
def global_poverty_rate():
    """
    Calibrated with historical data from World Bank: https://data.worldbank.org/indicator/SI.POV.DDAY
    """
    return sum(
        poverty_rate()
        .loc[:, _subscript_dict["SecondaryEdCohorts"]]
        .rename({"Gender": "Gender!", "Cohorts": "SecondaryEdCohorts!"})
        * population_cohorts()
        .loc[:, _subscript_dict["SecondaryEdCohorts"]]
        .rename({"Gender": "Gender!", "Cohorts": "SecondaryEdCohorts!"}),
        dim=["Gender!", "SecondaryEdCohorts!"],
    ) / sum(
        population_cohorts().rename({"Gender": "Gender!", "Cohorts": "Cohorts!"}),
        dim=["Gender!", "Cohorts!"],
    )


@component.add(
    name="Gross World Product",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_reo": 1,
        "net_climate_change_impact_on_economy": 1,
        "impact_of_biodiversity_on_economy": 1,
    },
)
def gross_world_product():
    return (
        total_reo()
        * net_climate_change_impact_on_economy()
        * impact_of_biodiversity_on_economy()
    )


@component.add(
    name="GWP Indicator",
    units="B$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gross_world_product": 1, "usd_to_billionusd": 1},
)
def gwp_indicator():
    return gross_world_product() * usd_to_billionusd()


@component.add(
    name="GWP per Capita",
    units="$/(Person*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gross_world_product": 1, "population": 1},
)
def gwp_per_capita():
    return gross_world_product() / population()


@component.add(
    name="GWP per Capita Indicator",
    units="$*Thousand/(Year*Person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gwp_per_capita": 1, "nvs_into_thousand": 1},
)
def gwp_per_capita_indicator():
    return gwp_per_capita() * nvs_into_thousand()


@component.add(
    name="Impact of Biodiversity on Economy",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "min_impact_of_biodiversity_on_economy": 2,
        "init_species_abundance": 1,
        "mean_species_abundance": 1,
        "max_impact_of_biodiversity_on_economy": 1,
    },
)
def impact_of_biodiversity_on_economy():
    """
    The fraction of ecomomy output loss due to changes in biodiversity.
    """
    return min_impact_of_biodiversity_on_economy() + (
        max_impact_of_biodiversity_on_economy()
        - min_impact_of_biodiversity_on_economy()
    ) * (mean_species_abundance() / init_species_abundance())


@component.add(
    name="INIT Capital", units="$", comp_type="Constant", comp_subtype="Normal"
)
def init_capital():
    """
    Initial Capital Stock.
    """
    return 1300000000000.0


@component.add(
    name="INIT Other Capital Change",
    units="$/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_other_capital_change():
    """
    Inital capital in other sectors.
    """
    return 40000000000.0


@component.add(
    name="InitialREO",
    units="Dmnl",
    subscripts=["Labor force type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"reos": 2},
)
def initialreo():
    value = xr.DataArray(
        np.nan,
        {"Labor force type": _subscript_dict["Labor force type"]},
        ["Labor force type"],
    )
    value.loc[["skill"]] = reos()
    value.loc[["unskill"]] = 1 - reos()
    return value


@component.add(
    name="Inverse table for standard normal distribution",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_inverse_table_for_standard_normal_distribution"
    },
)
def inverse_table_for_standard_normal_distribution(x, final_subs=None):
    return _hardcodedlookup_inverse_table_for_standard_normal_distribution(
        x, final_subs
    )


_hardcodedlookup_inverse_table_for_standard_normal_distribution = HardcodedLookups(
    [
        0.5,
        0.504,
        0.508,
        0.512,
        0.516,
        0.5199,
        0.5239,
        0.5279,
        0.5319,
        0.5359,
        0.5398,
        0.5438,
        0.5478,
        0.5517,
        0.5557,
        0.5596,
        0.5636,
        0.5675,
        0.5714,
        0.5753,
        0.5793,
        0.5832,
        0.5871,
        0.591,
        0.5948,
        0.5987,
        0.6026,
        0.6064,
        0.6103,
        0.6141,
        0.6179,
        0.6217,
        0.6255,
        0.6293,
        0.6331,
        0.6368,
        0.6406,
        0.6443,
        0.648,
        0.6517,
        0.6554,
        0.6591,
        0.6628,
        0.6664,
        0.67,
        0.6736,
        0.6772,
        0.6808,
        0.6844,
        0.6879,
        0.6915,
        0.695,
        0.6985,
        0.7019,
        0.7054,
        0.7088,
        0.7123,
        0.7157,
        0.719,
        0.7224,
        0.7257,
        0.7291,
        0.7324,
        0.7357,
        0.7389,
        0.7422,
        0.7454,
        0.7486,
        0.7517,
        0.7549,
        0.758,
        0.7611,
        0.7642,
        0.7673,
        0.7703,
        0.7734,
        0.7764,
        0.7794,
        0.7823,
        0.7852,
        0.7881,
        0.791,
        0.7939,
        0.7967,
        0.7995,
        0.8023,
        0.8051,
        0.8078,
        0.8106,
        0.8133,
        0.8159,
        0.8186,
        0.8212,
        0.8238,
        0.8264,
        0.8289,
        0.834,
        0.8355,
        0.8365,
        0.8389,
        0.8413,
        0.8438,
        0.8461,
        0.8485,
        0.8508,
        0.8531,
        0.8554,
        0.8577,
        0.8599,
        0.8621,
        0.8643,
        0.8665,
        0.8686,
        0.8708,
        0.8729,
        0.8749,
        0.877,
        0.879,
        0.881,
        0.883,
        0.8849,
        0.8869,
        0.8888,
        0.8907,
        0.8925,
        0.8944,
        0.8962,
        0.898,
        0.8997,
        0.9015,
        0.9032,
        0.9049,
        0.9066,
        0.9082,
        0.9099,
        0.9115,
        0.9131,
        0.9147,
        0.9162,
        0.9177,
        0.9192,
        0.9207,
        0.9222,
        0.9236,
        0.9251,
        0.9265,
        0.9279,
        0.9292,
        0.9306,
        0.9319,
        0.9332,
        0.9345,
        0.9357,
        0.937,
        0.9382,
        0.9394,
        0.9406,
        0.9418,
        0.943,
        0.9441,
        0.9452,
        0.9463,
        0.9474,
        0.9484,
        0.9495,
        0.9505,
        0.9515,
        0.9525,
        0.9535,
        0.9535,
        0.9554,
        0.9564,
        0.9573,
        0.9582,
        0.9591,
        0.9599,
        0.9608,
        0.9616,
        0.9625,
        0.9633,
        0.9641,
        0.9648,
        0.9656,
        0.9664,
        0.9672,
        0.9678,
        0.9686,
        0.9693,
        0.97,
        0.9706,
        0.9713,
        0.9719,
        0.9726,
        0.9732,
        0.9738,
        0.9744,
        0.975,
        0.9756,
        0.9762,
        0.9767,
        0.9772,
        0.9778,
        0.9783,
        0.9788,
        0.9793,
        0.9798,
        0.9803,
        0.9808,
        0.9812,
        0.9817,
        0.9821,
        0.9826,
        0.983,
        0.9834,
        0.9838,
        0.9842,
        0.9846,
        0.985,
        0.9854,
        0.9857,
        0.9861,
        0.9864,
        0.9868,
        0.9871,
        0.9874,
        0.9878,
        0.9881,
        0.9884,
        0.9887,
        0.989,
        0.9893,
        0.9896,
        0.9898,
        0.9901,
        0.9904,
        0.9906,
        0.9909,
        0.9911,
        0.9913,
        0.9916,
        0.9918,
        0.992,
        0.9922,
        0.9925,
        0.9927,
        0.9929,
        0.9931,
        0.9932,
        0.9934,
        0.9936,
        0.9938,
        0.994,
        0.9941,
        0.9943,
        0.9945,
        0.9946,
        0.9948,
        0.9949,
        0.9951,
        0.9952,
        0.9953,
        0.9955,
        0.9956,
        0.9957,
        0.9959,
        0.996,
        0.9961,
        0.9962,
        0.9963,
        0.9964,
        0.9965,
        0.9966,
        0.9967,
        0.9968,
        0.9969,
        0.997,
        0.9971,
        0.9972,
        0.9973,
        0.9974,
        0.9974,
        0.9975,
        0.9976,
        0.9977,
        0.9977,
        0.9978,
        0.9979,
        0.9979,
        0.998,
        0.9981,
        0.9981,
        0.9982,
        0.9982,
        0.9983,
        0.9984,
        0.9984,
        0.9985,
        0.9985,
        0.9986,
        0.9986,
        0.9987,
        0.999,
        0.9993,
        0.9995,
        0.9997,
        0.9998,
        0.9998,
        0.9999,
        0.9999,
        1.0,
        1.0,
        1.0,
    ],
    [
        0.0,
        0.01,
        0.02,
        0.03,
        0.04,
        0.05,
        0.06,
        0.07,
        0.08,
        0.09,
        0.1,
        0.11,
        0.12,
        0.13,
        0.14,
        0.15,
        0.16,
        0.17,
        0.18,
        0.19,
        0.2,
        0.21,
        0.22,
        0.23,
        0.24,
        0.25,
        0.26,
        0.27,
        0.28,
        0.29,
        0.3,
        0.31,
        0.32,
        0.33,
        0.34,
        0.35,
        0.36,
        0.37,
        0.38,
        0.39,
        0.4,
        0.41,
        0.42,
        0.43,
        0.44,
        0.45,
        0.46,
        0.47,
        0.48,
        0.49,
        0.5,
        0.51,
        0.52,
        0.53,
        0.54,
        0.55,
        0.56,
        0.57,
        0.58,
        0.59,
        0.6,
        0.61,
        0.62,
        0.63,
        0.64,
        0.65,
        0.66,
        0.67,
        0.68,
        0.69,
        0.7,
        0.71,
        0.72,
        0.73,
        0.74,
        0.75,
        0.76,
        0.77,
        0.78,
        0.79,
        0.8,
        0.81,
        0.82,
        0.83,
        0.84,
        0.85,
        0.86,
        0.87,
        0.88,
        0.89,
        0.9,
        0.91,
        0.92,
        0.93,
        0.94,
        0.95,
        0.97,
        0.96,
        0.98,
        0.99,
        1.0,
        1.01,
        1.02,
        1.03,
        1.04,
        1.05,
        1.06,
        1.07,
        1.08,
        1.09,
        1.1,
        1.11,
        1.12,
        1.13,
        1.14,
        1.15,
        1.16,
        1.17,
        1.18,
        1.19,
        1.2,
        1.21,
        1.22,
        1.23,
        1.24,
        1.25,
        1.26,
        1.27,
        1.28,
        1.29,
        1.3,
        1.31,
        1.32,
        1.33,
        1.34,
        1.35,
        1.36,
        1.37,
        1.38,
        1.39,
        1.4,
        1.41,
        1.42,
        1.43,
        1.44,
        1.45,
        1.46,
        1.47,
        1.48,
        1.49,
        1.5,
        1.51,
        1.52,
        1.53,
        1.54,
        1.55,
        1.56,
        1.57,
        1.58,
        1.59,
        1.6,
        1.61,
        1.62,
        1.63,
        1.64,
        1.65,
        1.66,
        1.67,
        1.68,
        1.69,
        1.7,
        1.71,
        1.72,
        1.73,
        1.74,
        1.75,
        1.76,
        1.77,
        1.78,
        1.79,
        1.8,
        1.81,
        1.82,
        1.83,
        1.84,
        1.85,
        1.86,
        1.87,
        1.88,
        1.89,
        1.9,
        1.91,
        1.92,
        1.93,
        1.94,
        1.95,
        1.96,
        1.97,
        1.98,
        1.99,
        2.0,
        2.01,
        2.02,
        2.03,
        2.04,
        2.05,
        2.06,
        2.07,
        2.08,
        2.09,
        2.1,
        2.11,
        2.12,
        2.13,
        2.14,
        2.15,
        2.16,
        2.17,
        2.18,
        2.19,
        2.2,
        2.21,
        2.22,
        2.23,
        2.24,
        2.25,
        2.26,
        2.27,
        2.28,
        2.29,
        2.3,
        2.31,
        2.32,
        2.33,
        2.34,
        2.35,
        2.36,
        2.37,
        2.38,
        2.39,
        2.4,
        2.41,
        2.42,
        2.43,
        2.44,
        2.45,
        2.46,
        2.47,
        2.48,
        2.49,
        2.5,
        2.51,
        2.52,
        2.53,
        2.54,
        2.55,
        2.56,
        2.57,
        2.58,
        2.59,
        2.6,
        2.61,
        2.62,
        2.63,
        2.64,
        2.65,
        2.66,
        2.67,
        2.68,
        2.69,
        2.7,
        2.71,
        2.72,
        2.73,
        2.74,
        2.75,
        2.76,
        2.77,
        2.78,
        2.79,
        2.8,
        2.81,
        2.82,
        2.83,
        2.84,
        2.85,
        2.86,
        2.87,
        2.88,
        2.89,
        2.9,
        2.92,
        2.91,
        2.93,
        2.94,
        2.95,
        2.96,
        2.97,
        2.98,
        2.99,
        3.0,
        3.01,
        3.02,
        3.03,
        3.04,
        3.05,
        3.06,
        3.07,
        3.08,
        4.0,
        3.09,
        5.0,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_inverse_table_for_standard_normal_distribution",
)


@component.add(
    name='"lnPL-mean"',
    units="Dmnl",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "poverty_line": 1,
        "mean_value_of_the_lognormal_distribution_of_consumption_or_income": 1,
    },
)
def lnplmean():
    return (
        float(np.log(poverty_line()))
        - mean_value_of_the_lognormal_distribution_of_consumption_or_income()
    )


@component.add(
    name="Max Impact of Biodiversity on Economy",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_impact_of_biodiversity_on_economy():
    """
    Scaling factor indicating maximum impact of changes in biodiversity on economy output.
    """
    return 1


@component.add(
    name="Mean value of the lognormal distribution of consumption or income",
    units="$/(Person*Year)",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "real_incomes_per_capita": 1,
        "standard_deviation_of_the_lognormal_distribution_of_consumption": 1,
    },
)
def mean_value_of_the_lognormal_distribution_of_consumption_or_income():
    return (
        np.log(real_incomes_per_capita())
        - standard_deviation_of_the_lognormal_distribution_of_consumption() ** 2 / 2
    )


@component.add(
    name="Min Impact of Biodiversity on Economy",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def min_impact_of_biodiversity_on_economy():
    """
    Scaling factor indicating minimal impact of changes in biodiversity on economy output.
    """
    return 0.98


@component.add(
    name="Net Capital Change",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"net_energy_capital_change": 1, "other_capital_change": 1},
)
def net_capital_change():
    """
    Net capital change.
    """
    return net_energy_capital_change() + other_capital_change()


@component.add(
    name="Net Capital Change Rate",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"net_capital_change": 1},
)
def net_capital_change_rate():
    """
    Net Capital Stock change rate.
    """
    return net_capital_change()


@component.add(
    name="Net Change in Other Capital",
    units="$/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "other_capital_change": 1,
        "current_to_max_other_capital": 1,
        "time_to_adjust_other_capital": 1,
    },
)
def net_change_in_other_capital():
    """
    Adjustment of capital changes in sectors other than energy.
    """
    return (
        other_capital_change()
        * current_to_max_other_capital()
        / time_to_adjust_other_capital()
    )


@component.add(
    name="Net Energy Capital Change",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_oil_exploration": 1,
        "investment_in_oil_production": 1,
        "investment_in_oil_technology": 1,
        "investment_in_coal_exploration": 1,
        "investment_in_coal_production": 1,
        "investment_in_coal_technology": 1,
        "investment_in_gas_exploration": 1,
        "investment_in_gas_production": 1,
        "investment_in_gas_technology": 1,
        "investment_in_biomass_capacity": 1,
        "investment_in_biomass_energy_technology": 1,
        "investment_in_solar_capacity": 1,
        "investment_in_solar_energy_technology": 1,
        "investment_in_wind_capacity": 1,
        "investment_in_wind_energy_technology": 1,
    },
)
def net_energy_capital_change():
    """
    Capital change from energy sector.
    """
    return (
        investment_in_oil_exploration()
        + investment_in_oil_production()
        + investment_in_oil_technology()
        + investment_in_coal_exploration()
        + investment_in_coal_production()
        + investment_in_coal_technology()
        + investment_in_gas_exploration()
        + investment_in_gas_production()
        + investment_in_gas_technology()
        + investment_in_biomass_capacity()
        + investment_in_biomass_energy_technology()
        + investment_in_solar_capacity()
        + investment_in_solar_energy_technology()
        + investment_in_wind_capacity()
        + investment_in_wind_energy_technology()
    )


@component.add(
    name="Oil Technology",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "oil_fraction_discoverable": 1,
        "maxofd": 1,
        "maxofr": 1,
        "oil_fraction_recoverable": 1,
    },
)
def oil_technology():
    """
    Factor productivity in Oil energy sector.
    """
    return (
        oil_fraction_discoverable() / maxofd() + oil_fraction_recoverable() / maxofr()
    ) / 2


@component.add(
    name="OLDCapital",
    units="$",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_oldcapital": 1},
    other_deps={
        "_integ_oldcapital": {
            "initial": {"oldinit_capital": 1},
            "step": {"oldnet_capital_change_rate": 1},
        }
    },
)
def oldcapital():
    """
    Capital stock. Source of historical data: http://www.ggdc.net/MADDISON/oriindex.htm
    """
    return _integ_oldcapital()


_integ_oldcapital = Integ(
    lambda: oldnet_capital_change_rate(), lambda: oldinit_capital(), "_integ_oldcapital"
)


@component.add(
    name="OLDCapital Elasticity Output",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def oldcapital_elasticity_output():
    """
    Capital Elasticity of Output.
    """
    return 0.35


@component.add(
    name="OLDGross World Product",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "oldreference_economy_output": 1,
        "net_climate_change_impact_on_economy": 1,
        "impact_of_biodiversity_on_economy": 1,
    },
)
def oldgross_world_product():
    """
    Gross World Product taking into account climate change impact. Source of historical data: http://www.ggdc.net/MADDISON/oriindex.htm
    """
    return (
        sum(
            oldreference_economy_output().rename(
                {
                    "Gender": "Gender!",
                    "WorkingAge": "WorkingAge!",
                    "Labor force type": "Labor force type!",
                }
            ),
            dim=["Gender!", "WorkingAge!", "Labor force type!"],
        )
        * net_climate_change_impact_on_economy()
        * impact_of_biodiversity_on_economy()
    )


@component.add(
    name="OLDGWP per Capita",
    units="$/(Year*Person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oldgross_world_product": 1, "population": 1},
)
def oldgwp_per_capita():
    """
    Gross World Product per Capita. Source of historical data: http://www.ggdc.net/MADDISON/oriindex.htm
    """
    return oldgross_world_product() / population()


@component.add(
    name="OLDGWP Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oldgross_world_product": 1, "oldoutput_in_1900": 1},
)
def oldgwp_ratio():
    """
    Gross World Product compared to Output in 1900 as a reference indicator.
    """
    return oldgross_world_product() / oldoutput_in_1900()


@component.add(
    name="OLDINIT Capital", units="$", comp_type="Constant", comp_subtype="Normal"
)
def oldinit_capital():
    """
    Initial Capital Stock.
    """
    return 1300000000000.0


@component.add(
    name="OLDNet Capital Change",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"net_energy_capital_change": 1, "other_capital_change": 1},
)
def oldnet_capital_change():
    """
    Net capital change.
    """
    return net_energy_capital_change() + other_capital_change()


@component.add(
    name="OLDNet Capital Change Rate",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oldnet_capital_change": 1},
)
def oldnet_capital_change_rate():
    """
    Net Capital Stock change rate.
    """
    return oldnet_capital_change()


@component.add(
    name="OLDOutput in 1900",
    units="$/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def oldoutput_in_1900():
    """
    Economy output in 1900.
    """
    return 1300000000000.0


@component.add(
    name="OLDReference Economy Output",
    units="$/Year",
    subscripts=["Gender", "WorkingAge", "Labor force type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "oldoutput_in_1900": 1,
        "oldtechnology": 1,
        "labor_force": 1,
        "oldcapital_elasticity_output": 2,
        "initial_labor_force": 1,
        "oldcapital": 1,
        "oldinit_capital": 1,
        "indicative_labor_force_participation_fraction": 1,
    },
)
def oldreference_economy_output():
    """
    Reference Output before effects of climate damage and emissions abatement are considered. Calculated as Cobb-Douglas functional form of production functions.
    """
    return (
        oldoutput_in_1900()
        * oldtechnology()
        * (
            (oldcapital() / oldinit_capital()) ** oldcapital_elasticity_output()
            * labor_force()
            / initial_labor_force()
            * indicative_labor_force_participation_fraction()
        )
        ** (1 - oldcapital_elasticity_output())
    )


@component.add(
    name="OLDTechnology",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_technology": 1, "other_technologies": 1},
)
def oldtechnology():
    """
    Total factor productivity.
    """
    return energy_technology() + other_technologies()


@component.add(
    name="Other Capital Change",
    units="$/Year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_other_capital_change": 1},
    other_deps={
        "_integ_other_capital_change": {
            "initial": {"init_other_capital_change": 1},
            "step": {"net_change_in_other_capital": 1},
        }
    },
)
def other_capital_change():
    """
    Capital change from other sector.
    """
    return _integ_other_capital_change()


_integ_other_capital_change = Integ(
    lambda: net_change_in_other_capital(),
    lambda: init_other_capital_change(),
    "_integ_other_capital_change",
)


@component.add(
    name="Other Capital Change Ratio",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def other_capital_change_ratio():
    """
    Strength of adjustment of current to reference capital change related to sectors other than energy.
    """
    return 0.77


@component.add(
    name="Other Technologies",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_other_technology": 1,
        "time": 1,
        "other_technology_steepness": 3,
        "initial_time": 1,
        "year_period": 1,
        "other_technology_inflection_point": 2,
    },
)
def other_technologies():
    """
    Factor productivity in other than energy sectors.
    """
    return reference_other_technology() * (
        1
        - other_technology_inflection_point() ** other_technology_steepness()
        / (
            other_technology_inflection_point() ** other_technology_steepness()
            + ((time() - initial_time()) / year_period())
            ** other_technology_steepness()
        )
    )


@component.add(
    name="Other Technology Inflection Point",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"other_technology_inflection_point_variation": 1, "time": 1},
)
def other_technology_inflection_point():
    """
    Parameter determining inflection point of reference factor productivity in other than energy sectors.
    """
    return 100 + step(
        __data["time"], other_technology_inflection_point_variation() - 100, 2020
    )


@component.add(
    name="Other Technology Inflection Point Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def other_technology_inflection_point_variation():
    """
    Parameter determining inflection point of reference factor productivity in other than energy sectors.
    """
    return 100


@component.add(
    name="Other Technology Steepness",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"variable16_technology": 1},
)
def other_technology_steepness():
    """
    Parameter determining intensity of reference factor productivity in other than energy sectors.
    """
    return variable16_technology()


@component.add(
    name="Output in 1900", units="$/Year", comp_type="Constant", comp_subtype="Normal"
)
def output_in_1900():
    return 1300000000000.0


@component.add(
    name="Poverty line",
    units="$/(Person*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"consumption_or_income_of_a_person_per_day": 1, "days_in_year": 1},
)
def poverty_line():
    return consumption_or_income_of_a_person_per_day() * days_in_year()


@component.add(
    name="Poverty rate",
    units="percent",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "standard_deviation_of_the_lognormal_distribution_of_consumption": 3,
        "table_for_standard_normal_distribution": 2,
        "lnplmean": 3,
        "nvs_100_percent": 1,
    },
)
def poverty_rate():
    return (
        if_then_else(
            standard_deviation_of_the_lognormal_distribution_of_consumption() == 0,
            lambda: xr.DataArray(
                0.5,
                {
                    "Gender": _subscript_dict["Gender"],
                    "Cohorts": _subscript_dict["Cohorts"],
                },
                ["Gender", "Cohorts"],
            ),
            lambda: if_then_else(
                lnplmean() < 0,
                lambda: 1
                - table_for_standard_normal_distribution(
                    -lnplmean()
                    / standard_deviation_of_the_lognormal_distribution_of_consumption(),
                    {
                        "Gender": ["male", "female"],
                        "Cohorts": [
                            '"0-4"',
                            '"5-9"',
                            '"10-14"',
                            '"15-19"',
                            '"20-24"',
                            '"25-29"',
                            '"30-34"',
                            '"35-39"',
                            '"40-44"',
                            '"45-49"',
                            '"50-54"',
                            '"55-59"',
                            '"60-64"',
                            '"65-69"',
                            '"70-74"',
                            '"75-79"',
                            '"80-84"',
                            '"85-89"',
                            '"90-94"',
                            '"95-99"',
                            '"100+"',
                        ],
                    },
                ),
                lambda: table_for_standard_normal_distribution(
                    lnplmean()
                    / standard_deviation_of_the_lognormal_distribution_of_consumption(),
                    {
                        "Gender": ["male", "female"],
                        "Cohorts": [
                            '"0-4"',
                            '"5-9"',
                            '"10-14"',
                            '"15-19"',
                            '"20-24"',
                            '"25-29"',
                            '"30-34"',
                            '"35-39"',
                            '"40-44"',
                            '"45-49"',
                            '"50-54"',
                            '"55-59"',
                            '"60-64"',
                            '"65-69"',
                            '"70-74"',
                            '"75-79"',
                            '"80-84"',
                            '"85-89"',
                            '"90-94"',
                            '"95-99"',
                            '"100+"',
                        ],
                    },
                ),
            ),
        )
        * nvs_100_percent()
    )


@component.add(
    name="Ratio of capital",
    units="Dmnl",
    subscripts=["Labor force type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"rcs": 2},
)
def ratio_of_capital():
    value = xr.DataArray(
        np.nan,
        {"Labor force type": _subscript_dict["Labor force type"]},
        ["Labor force type"],
    )
    value.loc[["skill"]] = rcs()
    value.loc[["unskill"]] = 1 - rcs()
    return value


@component.add(
    name="Ratio of technology",
    units="Dmnl",
    subscripts=["Labor force type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ts": 2},
)
def ratio_of_technology():
    value = xr.DataArray(
        np.nan,
        {"Labor force type": _subscript_dict["Labor force type"]},
        ["Labor force type"],
    )
    value.loc[["skill"]] = ts()
    value.loc[["unskill"]] = 1 - ts()
    return value


@component.add(
    name="RCs",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_rcs": 1},
    other_deps={
        "_smooth_rcs": {
            "initial": {"rcs_sa": 1, "current_year": 1, "time": 1},
            "step": {
                "rcs_sa": 1,
                "current_year": 1,
                "time": 1,
                "sa_effective_change_delay": 1,
            },
        }
    },
)
def rcs():
    return 0.125608 + _smooth_rcs()


_smooth_rcs = Smooth(
    lambda: step(__data["time"], rcs_sa() - 0.125608, current_year()),
    lambda: sa_effective_change_delay(),
    lambda: step(__data["time"], rcs_sa() - 0.125608, current_year()),
    lambda: 1,
    "_smooth_rcs",
)


@component.add(name="RCs SA", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def rcs_sa():
    """
    From calibration. Comment by Q. Ye in July 2024
    """
    return 0.125608


@component.add(
    name="Real incomes parameter",
    units="Dmnl",
    subscripts=["Gender", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def real_incomes_parameter():
    """
    to obtain the real earnings per capita of each group instead of relative incomes by model calibration. Two assumptions: (1) the relationship between income and age tends to exhibit an inverted-U-shape pattern. Incomes rise with age and then drop slightly as taxpayers enter retirement. (2) Male has more incomes than female in the same age group.
    """
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )
    value.loc[["male"], _subscript_dict["Childhood"]] = 0.18842
    value.loc[["male"], _subscript_dict['"15 to 39"']] = 0.195
    value.loc[["male"], _subscript_dict['"40 to 64"']] = 0.21
    value.loc[["male"], _subscript_dict['"65 plus"']] = 0.19
    value.loc[["female"], _subscript_dict["Childhood"]] = 0.18
    value.loc[["female"], _subscript_dict['"15 to 39"']] = 0.156082
    value.loc[["female"], _subscript_dict['"40 to 64"']] = 0.18117
    value.loc[["female"], _subscript_dict['"65 plus"']] = 0.16
    return value


@component.add(
    name="Real incomes per capita",
    units="$/(Person*Year)",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gwp_per_capita": 1, "real_incomes_parameter": 1},
)
def real_incomes_per_capita():
    return gwp_per_capita() * real_incomes_parameter()


@component.add(
    name="Reference Economy Output",
    units="$/Year",
    subscripts=["Labor force type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initialreo": 1,
        "output_in_1900": 1,
        "ratio_of_technology": 1,
        "technology": 1,
        "ratio_of_capital": 1,
        "capital": 1,
        "init_capital": 1,
        "capital_elasticity_output": 2,
        "labor_force_input": 1,
    },
)
def reference_economy_output():
    """
    Output in 1900*Technology*(((Capital/INIT Capital)^Capital Elasticity Output)*(Labor Force input)^(1-Capital Elasticity Output))
    """
    return (
        initialreo()
        * output_in_1900()
        * ratio_of_technology()
        * technology()
        * (ratio_of_capital() * (capital() / init_capital()))
        ** capital_elasticity_output()
        * sum(
            labor_force_input().rename(
                {"Gender": "Gender!", "WorkingAge": "WorkingAge!"}
            ),
            dim=["Gender!", "WorkingAge!"],
        )
        ** (1 - capital_elasticity_output())
    )


@component.add(
    name="Reference Other Capital Change",
    units="$/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_other_capital_change():
    """
    Reference other capital change than from energy sector.
    """
    return 1000000000000000.0


@component.add(
    name="Reference Other Technology",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_other_technology_baseline": 2,
        "time": 1,
        "reference_other_technology_variation": 1,
        "year2100": 2,
        "current_year": 2,
    },
)
def reference_other_technology():
    """
    Reference factor productivity in other than energy sectors.
    """
    return reference_other_technology_baseline() + ramp(
        __data["time"],
        (reference_other_technology_variation() - reference_other_technology_baseline())
        / (year2100() - current_year()),
        current_year(),
        year2100(),
    )


@component.add(
    name="Reference Other Technology baseline",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_other_technology_baseline():
    """
    Reference factor productivity in other than energy sectors.
    """
    return 1


@component.add(
    name="Reference Other Technology Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_other_technology_variation():
    """
    Reference factor productivity in other than energy sectors.
    """
    return 1


@component.add(
    name="Reference relative income of skilled",
    units="$/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "relative_income_of_skilled_variation_baseline": 1,
        "_smooth_reference_relative_income_of_skilled": 1,
    },
    other_deps={
        "_smooth_reference_relative_income_of_skilled": {
            "initial": {
                "relative_income_of_skilled_variation": 1,
                "relative_income_of_skilled_variation_baseline": 1,
                "current_year": 2,
                "demofelix_target_year": 2,
                "time": 1,
            },
            "step": {
                "relative_income_of_skilled_variation": 1,
                "relative_income_of_skilled_variation_baseline": 1,
                "current_year": 2,
                "demofelix_target_year": 2,
                "time": 1,
            },
        }
    },
)
def reference_relative_income_of_skilled():
    return (
        relative_income_of_skilled_variation_baseline()
        + _smooth_reference_relative_income_of_skilled()
    )


_smooth_reference_relative_income_of_skilled = Smooth(
    lambda: ramp(
        __data["time"],
        (
            relative_income_of_skilled_variation()
            - relative_income_of_skilled_variation_baseline()
        )
        / (demofelix_target_year() - current_year()),
        current_year(),
        demofelix_target_year(),
    ),
    lambda: 5,
    lambda: ramp(
        __data["time"],
        (
            relative_income_of_skilled_variation()
            - relative_income_of_skilled_variation_baseline()
        )
        / (demofelix_target_year() - current_year()),
        current_year(),
        demofelix_target_year(),
    ),
    lambda: 1,
    "_smooth_reference_relative_income_of_skilled",
)


@component.add(
    name="Relative income of skilled variation",
    units="$/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def relative_income_of_skilled_variation():
    return 65


@component.add(
    name="Relative income of skilled variation baseline",
    units="$/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def relative_income_of_skilled_variation_baseline():
    return 65


@component.add(
    name="Relative incomes of skilled",
    units="$/Year",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_relative_income_of_skilled": 1,
        "adjustments_for_relative_incomes_of_skilled": 1,
    },
)
def relative_incomes_of_skilled():
    """
    Relative incomes of skilled. Need data about the earnings of skilled in each population cohort. Data from OECD datasets. https://stats.oecd.org/Index.aspx?DataSetCode=EAG_EARNINGS 65 is about the average relative incomes of skilled population in OECD countries. Detailed data collection can be found in the file: Data collection from OECD earnings.xlsx
    """
    return (
        reference_relative_income_of_skilled()
        * adjustments_for_relative_incomes_of_skilled()
    )


@component.add(
    name="Relative incomes of unskilled",
    units="$/Year",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_relative_incomes": 2, "relative_incomes_of_skilled": 2},
)
def relative_incomes_of_unskilled():
    """
    Relative incomes of unskilled. Need data about the earnings of unskilled population in each population cohort. Data from OECD datasets. https://stats.oecd.org/Index.aspx?DataSetCode=EAG_EARNINGS Detailed data collection can be found in the file: Data collection from OECD earnings.xlsx
    """
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )
    value.loc[["male"], :] = (
        (
            total_relative_incomes().loc["male", :].reset_coords(drop=True)
            - relative_incomes_of_skilled().loc["male", :].reset_coords(drop=True)
        )
        .expand_dims({"Gender": ["male"]}, 0)
        .values
    )
    value.loc[["female"], :] = (
        (
            total_relative_incomes().loc["female", :].reset_coords(drop=True)
            - relative_incomes_of_skilled().loc["female", :].reset_coords(drop=True)
        )
        .expand_dims({"Gender": ["female"]}, 0)
        .values
    )
    return value


@component.add(name="REOs", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def reos():
    return 0.210843


@component.add(
    name="Skilled fraction of secondary education graduates",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def skilled_fraction_of_secondary_education_graduates():
    return 0.5


@component.add(
    name="Skilled fraction of secondary education graduates baseline",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def skilled_fraction_of_secondary_education_graduates_baseline():
    return 0.5


@component.add(
    name="Skilled population",
    units="People",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "tertiary_education_graduates": 1,
        "fraction_of_skilled_secondary_education_graduates": 1,
        "secondary_education_graduates": 1,
    },
)
def skilled_population():
    return (
        tertiary_education_graduates()
        + fraction_of_skilled_secondary_education_graduates()
        * secondary_education_graduates()
    )


@component.add(
    name="Smoothed GWP per Capita",
    units="$/(Person*Year)",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_smoothed_gwp_per_capita": 1},
    other_deps={
        "_smooth_smoothed_gwp_per_capita": {
            "initial": {"gwp_per_capita": 1},
            "step": {"gwp_per_capita": 1, "year_period": 1},
        }
    },
)
def smoothed_gwp_per_capita():
    return _smooth_smoothed_gwp_per_capita()


_smooth_smoothed_gwp_per_capita = Smooth(
    lambda: gwp_per_capita(),
    lambda: year_period(),
    lambda: gwp_per_capita(),
    lambda: 1,
    "_smooth_smoothed_gwp_per_capita",
)


@component.add(
    name="Solar Technology",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "solar_conversion_efficiency": 1,
        "maxsce": 1,
        "solar_installation_efficiency": 1,
        "maxsie": 1,
    },
)
def solar_technology():
    """
    Factor productivity in Solar energy sector.
    """
    return (
        solar_conversion_efficiency() / maxsce()
        + solar_installation_efficiency() / maxsie()
    ) / 2


@component.add(
    name="SSP Economic Variation Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ssp_economic_variation_time():
    return 5


@component.add(
    name="Standard deviation of the lognormal distribution of consumption",
    units="Dmnl",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gini_coefficient": 1,
        "inverse_table_for_standard_normal_distribution": 1,
    },
)
def standard_deviation_of_the_lognormal_distribution_of_consumption():
    return float(np.sqrt(2)) * inverse_table_for_standard_normal_distribution(
        (gini_coefficient() + 1) / 2,
        {
            "Gender": ["male", "female"],
            "Cohorts": [
                '"0-4"',
                '"5-9"',
                '"10-14"',
                '"15-19"',
                '"20-24"',
                '"25-29"',
                '"30-34"',
                '"35-39"',
                '"40-44"',
                '"45-49"',
                '"50-54"',
                '"55-59"',
                '"60-64"',
                '"65-69"',
                '"70-74"',
                '"75-79"',
                '"80-84"',
                '"85-89"',
                '"90-94"',
                '"95-99"',
                '"100+"',
            ],
        },
    )


@component.add(
    name="Table for standard normal distribution",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_for_standard_normal_distribution"
    },
)
def table_for_standard_normal_distribution(x, final_subs=None):
    return _hardcodedlookup_table_for_standard_normal_distribution(x, final_subs)


_hardcodedlookup_table_for_standard_normal_distribution = HardcodedLookups(
    [
        0.0,
        0.01,
        0.02,
        0.03,
        0.04,
        0.05,
        0.06,
        0.07,
        0.08,
        0.09,
        0.1,
        0.11,
        0.12,
        0.13,
        0.14,
        0.15,
        0.16,
        0.17,
        0.18,
        0.19,
        0.2,
        0.21,
        0.22,
        0.23,
        0.24,
        0.25,
        0.26,
        0.27,
        0.28,
        0.29,
        0.3,
        0.31,
        0.32,
        0.33,
        0.34,
        0.35,
        0.36,
        0.37,
        0.38,
        0.39,
        0.4,
        0.41,
        0.42,
        0.43,
        0.44,
        0.45,
        0.46,
        0.47,
        0.48,
        0.49,
        0.5,
        0.51,
        0.52,
        0.53,
        0.54,
        0.55,
        0.56,
        0.57,
        0.58,
        0.59,
        0.6,
        0.61,
        0.62,
        0.63,
        0.64,
        0.65,
        0.66,
        0.67,
        0.68,
        0.69,
        0.7,
        0.71,
        0.72,
        0.73,
        0.74,
        0.75,
        0.76,
        0.77,
        0.78,
        0.79,
        0.8,
        0.81,
        0.82,
        0.83,
        0.84,
        0.85,
        0.86,
        0.87,
        0.88,
        0.89,
        0.9,
        0.91,
        0.92,
        0.93,
        0.94,
        0.95,
        0.96,
        0.97,
        0.98,
        0.99,
        1.0,
        1.01,
        1.02,
        1.03,
        1.04,
        1.05,
        1.06,
        1.07,
        1.08,
        1.09,
        1.1,
        1.11,
        1.12,
        1.13,
        1.14,
        1.15,
        1.16,
        1.17,
        1.18,
        1.19,
        1.2,
        1.21,
        1.22,
        1.23,
        1.24,
        1.25,
        1.26,
        1.27,
        1.28,
        1.29,
        1.3,
        1.31,
        1.32,
        1.33,
        1.34,
        1.35,
        1.36,
        1.37,
        1.38,
        1.39,
        1.4,
        1.41,
        1.42,
        1.43,
        1.44,
        1.45,
        1.46,
        1.47,
        1.48,
        1.49,
        1.5,
        1.51,
        1.52,
        1.53,
        1.54,
        1.55,
        1.56,
        1.57,
        1.58,
        1.59,
        1.6,
        1.61,
        1.62,
        1.63,
        1.64,
        1.65,
        1.66,
        1.67,
        1.68,
        1.69,
        1.7,
        1.71,
        1.72,
        1.73,
        1.74,
        1.75,
        1.76,
        1.77,
        1.78,
        1.79,
        1.8,
        1.81,
        1.82,
        1.83,
        1.84,
        1.85,
        1.86,
        1.87,
        1.88,
        1.89,
        1.9,
        1.91,
        1.92,
        1.93,
        1.94,
        1.95,
        1.96,
        1.97,
        1.98,
        1.99,
        2.0,
        2.01,
        2.02,
        2.03,
        2.04,
        2.05,
        2.06,
        2.07,
        2.08,
        2.09,
        2.1,
        2.11,
        2.12,
        2.13,
        2.14,
        2.15,
        2.16,
        2.17,
        2.18,
        2.19,
        2.2,
        2.21,
        2.22,
        2.23,
        2.24,
        2.25,
        2.26,
        2.27,
        2.28,
        2.29,
        2.3,
        2.31,
        2.32,
        2.33,
        2.34,
        2.35,
        2.36,
        2.37,
        2.38,
        2.39,
        2.4,
        2.41,
        2.42,
        2.43,
        2.44,
        2.45,
        2.46,
        2.47,
        2.48,
        2.49,
        2.5,
        2.51,
        2.52,
        2.53,
        2.54,
        2.55,
        2.56,
        2.57,
        2.58,
        2.59,
        2.6,
        2.61,
        2.62,
        2.63,
        2.64,
        2.65,
        2.66,
        2.67,
        2.68,
        2.69,
        2.7,
        2.71,
        2.72,
        2.73,
        2.74,
        2.75,
        2.76,
        2.77,
        2.78,
        2.79,
        2.8,
        2.81,
        2.82,
        2.83,
        2.84,
        2.85,
        2.86,
        2.87,
        2.88,
        2.89,
        2.9,
        2.91,
        2.92,
        2.93,
        2.94,
        2.95,
        2.96,
        2.97,
        2.98,
        2.99,
        3.0,
        3.01,
        3.02,
        3.03,
        3.04,
        3.05,
        3.06,
        3.07,
        3.08,
        3.09,
        4.0,
        5.0,
    ],
    [
        0.5,
        0.504,
        0.508,
        0.512,
        0.516,
        0.5199,
        0.5239,
        0.5279,
        0.5319,
        0.5359,
        0.5398,
        0.5438,
        0.5478,
        0.5517,
        0.5557,
        0.5596,
        0.5636,
        0.5675,
        0.5714,
        0.5753,
        0.5793,
        0.5832,
        0.5871,
        0.591,
        0.5948,
        0.5987,
        0.6026,
        0.6064,
        0.6103,
        0.6141,
        0.6179,
        0.6217,
        0.6255,
        0.6293,
        0.6331,
        0.6368,
        0.6406,
        0.6443,
        0.648,
        0.6517,
        0.6554,
        0.6591,
        0.6628,
        0.6664,
        0.67,
        0.6736,
        0.6772,
        0.6808,
        0.6844,
        0.6879,
        0.6915,
        0.695,
        0.6985,
        0.7019,
        0.7054,
        0.7088,
        0.7123,
        0.7157,
        0.719,
        0.7224,
        0.7257,
        0.7291,
        0.7324,
        0.7357,
        0.7389,
        0.7422,
        0.7454,
        0.7486,
        0.7517,
        0.7549,
        0.758,
        0.7611,
        0.7642,
        0.7673,
        0.7703,
        0.7734,
        0.7764,
        0.7794,
        0.7823,
        0.7852,
        0.7881,
        0.791,
        0.7939,
        0.7967,
        0.7995,
        0.8023,
        0.8051,
        0.8078,
        0.8106,
        0.8133,
        0.8159,
        0.8186,
        0.8212,
        0.8238,
        0.8264,
        0.8289,
        0.8355,
        0.834,
        0.8365,
        0.8389,
        0.8413,
        0.8438,
        0.8461,
        0.8485,
        0.8508,
        0.8531,
        0.8554,
        0.8577,
        0.8599,
        0.8621,
        0.8643,
        0.8665,
        0.8686,
        0.8708,
        0.8729,
        0.8749,
        0.877,
        0.879,
        0.881,
        0.883,
        0.8849,
        0.8869,
        0.8888,
        0.8907,
        0.8925,
        0.8944,
        0.8962,
        0.898,
        0.8997,
        0.9015,
        0.9032,
        0.9049,
        0.9066,
        0.9082,
        0.9099,
        0.9115,
        0.9131,
        0.9147,
        0.9162,
        0.9177,
        0.9192,
        0.9207,
        0.9222,
        0.9236,
        0.9251,
        0.9265,
        0.9279,
        0.9292,
        0.9306,
        0.9319,
        0.9332,
        0.9345,
        0.9357,
        0.937,
        0.9382,
        0.9394,
        0.9406,
        0.9418,
        0.943,
        0.9441,
        0.9452,
        0.9463,
        0.9474,
        0.9484,
        0.9495,
        0.9505,
        0.9515,
        0.9525,
        0.9535,
        0.9535,
        0.9554,
        0.9564,
        0.9573,
        0.9582,
        0.9591,
        0.9599,
        0.9608,
        0.9616,
        0.9625,
        0.9633,
        0.9641,
        0.9648,
        0.9656,
        0.9664,
        0.9672,
        0.9678,
        0.9686,
        0.9693,
        0.97,
        0.9706,
        0.9713,
        0.9719,
        0.9726,
        0.9732,
        0.9738,
        0.9744,
        0.975,
        0.9756,
        0.9762,
        0.9767,
        0.9772,
        0.9778,
        0.9783,
        0.9788,
        0.9793,
        0.9798,
        0.9803,
        0.9808,
        0.9812,
        0.9817,
        0.9821,
        0.9826,
        0.983,
        0.9834,
        0.9838,
        0.9842,
        0.9846,
        0.985,
        0.9854,
        0.9857,
        0.9861,
        0.9864,
        0.9868,
        0.9871,
        0.9874,
        0.9878,
        0.9881,
        0.9884,
        0.9887,
        0.989,
        0.9893,
        0.9896,
        0.9898,
        0.9901,
        0.9904,
        0.9906,
        0.9909,
        0.9911,
        0.9913,
        0.9916,
        0.9918,
        0.992,
        0.9922,
        0.9925,
        0.9927,
        0.9929,
        0.9931,
        0.9932,
        0.9934,
        0.9936,
        0.9938,
        0.994,
        0.9941,
        0.9943,
        0.9945,
        0.9946,
        0.9948,
        0.9949,
        0.9951,
        0.9952,
        0.9953,
        0.9955,
        0.9956,
        0.9957,
        0.9959,
        0.996,
        0.9961,
        0.9962,
        0.9963,
        0.9964,
        0.9965,
        0.9966,
        0.9967,
        0.9968,
        0.9969,
        0.997,
        0.9971,
        0.9972,
        0.9973,
        0.9974,
        0.9974,
        0.9975,
        0.9976,
        0.9977,
        0.9977,
        0.9978,
        0.9979,
        0.9979,
        0.998,
        0.9981,
        0.9981,
        0.9982,
        0.9982,
        0.9983,
        0.9984,
        0.9984,
        0.9985,
        0.9985,
        0.9986,
        0.9986,
        0.9987,
        0.999,
        0.9993,
        0.9995,
        0.9997,
        0.9998,
        0.9998,
        0.9999,
        0.9999,
        1.0,
        1.0,
        1.0,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_for_standard_normal_distribution",
)


@component.add(
    name="Technology",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_technology": 1, "other_technologies": 1},
)
def technology():
    """
    Total factor productivity.
    """
    return energy_technology() + other_technologies()


@component.add(
    name="Time to Adjust Other Capital",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_adjust_other_capital():
    """
    Time required to adjust capital changes in sectors other than energy.
    """
    return 20


@component.add(
    name="Total relative incomes",
    units="$/Year",
    subscripts=["Gender", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def total_relative_incomes():
    """
    Relative total incomes of skilled and unskilled.
    """
    return xr.DataArray(
        100,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )


@component.add(
    name="Total REO",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"reference_economy_output": 1},
)
def total_reo():
    return sum(
        reference_economy_output().rename({"Labor force type": "Labor force type!"}),
        dim=["Labor force type!"],
    )


@component.add(
    name="Ts",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_ts": 1},
    other_deps={
        "_smooth_ts": {
            "initial": {"ts_sa": 1, "current_year": 1, "time": 1},
            "step": {
                "ts_sa": 1,
                "current_year": 1,
                "time": 1,
                "sa_effective_change_delay": 1,
            },
        }
    },
)
def ts():
    return 0.904986 + _smooth_ts()


_smooth_ts = Smooth(
    lambda: step(__data["time"], ts_sa() - 0.904986, current_year()),
    lambda: sa_effective_change_delay(),
    lambda: step(__data["time"], ts_sa() - 0.904986, current_year()),
    lambda: 1,
    "_smooth_ts",
)


@component.add(name="Ts SA", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def ts_sa():
    """
    From calibration. Commented by Q. Ye in July 2024
    """
    return 0.904986


@component.add(
    name="Unskilled population",
    units="People",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_cohorts": 1, "skilled_population": 1},
)
def unskilled_population():
    return population_cohorts() - skilled_population()


@component.add(
    name="USD to billionUSD", units="B$/$", comp_type="Constant", comp_subtype="Normal"
)
def usd_to_billionusd():
    return 1 / 1000000000.0


@component.add(
    name="Variable16 Technology",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_change_rate16": 1,
        "time": 1,
        "change_rate_start16": 1,
        "change_rate_slope16": 1,
        "scenario_on": 1,
        "change_rate_finish16": 1,
    },
)
def variable16_technology():
    """
    Educational Attainment Change Rate.
    """
    return initial_change_rate16() + scenario_on() * ramp(
        __data["time"],
        change_rate_slope16(),
        change_rate_start16(),
        change_rate_finish16(),
    )


@component.add(
    name="Wind Technology",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wind_capacity_factor": 1,
        "maxwcf": 1,
        "wind_installation_efficiency": 1,
        "maxwie": 1,
    },
)
def wind_technology():
    """
    Factor productivity in Wind energy sector.
    """
    return (
        wind_capacity_factor() / maxwcf() + wind_installation_efficiency() / maxwie()
    ) / 2


@component.add(
    name="Year2100", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def year2100():
    return 2100
