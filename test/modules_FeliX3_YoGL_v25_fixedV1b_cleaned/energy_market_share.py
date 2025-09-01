"""
Module energy_market_share
Translated using PySD version 3.14.3
"""

@component.add(
    name="Average Energy Price",
    units="$/toe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_price_oil": 1,
        "average_price_gas": 1,
        "average_price_coal": 1,
        "average_price_solar": 1,
        "average_price_wind": 1,
        "average_price_biomass": 1,
        "number_of_energy_sources": 1,
    },
)
def average_energy_price():
    """
    Average market energy price.
    """
    return (
        average_price_oil()
        + average_price_gas()
        + average_price_coal()
        + average_price_solar()
        + average_price_wind()
        + average_price_biomass()
    ) / number_of_energy_sources()


@component.add(
    name="Average Price Biomass",
    units="$/toe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_average_price_biomass": 1},
    other_deps={
        "_integ_average_price_biomass": {
            "initial": {"init_apb": 1},
            "step": {"change_in_price_biomass": 1},
        }
    },
)
def average_price_biomass():
    """
    Average market biomass energy price.
    """
    return _integ_average_price_biomass()


_integ_average_price_biomass = Integ(
    lambda: change_in_price_biomass(),
    lambda: init_apb(),
    "_integ_average_price_biomass",
)


@component.add(
    name="Average Price Coal",
    units="$/toe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_average_price_coal": 1},
    other_deps={
        "_integ_average_price_coal": {
            "initial": {"init_apc": 1},
            "step": {"change_in_price_coal": 1},
        }
    },
)
def average_price_coal():
    """
    Average market coal price.
    """
    return _integ_average_price_coal()


_integ_average_price_coal = Integ(
    lambda: change_in_price_coal(), lambda: init_apc(), "_integ_average_price_coal"
)


@component.add(
    name="Average Price Gas",
    units="$/toe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_average_price_gas": 1},
    other_deps={
        "_integ_average_price_gas": {
            "initial": {"init_apg": 1},
            "step": {"change_in_price_gas": 1},
        }
    },
)
def average_price_gas():
    """
    Average market gas price.
    """
    return _integ_average_price_gas()


_integ_average_price_gas = Integ(
    lambda: change_in_price_gas(), lambda: init_apg(), "_integ_average_price_gas"
)


@component.add(
    name="Average Price Oil",
    units="$/toe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_average_price_oil": 1},
    other_deps={
        "_integ_average_price_oil": {
            "initial": {"init_apo": 1},
            "step": {"change_in_price_oil": 1},
        }
    },
)
def average_price_oil():
    """
    Average market oil price.
    """
    return _integ_average_price_oil()


_integ_average_price_oil = Integ(
    lambda: change_in_price_oil(), lambda: init_apo(), "_integ_average_price_oil"
)


@component.add(
    name="Average Price Solar",
    units="$/toe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_average_price_solar": 1},
    other_deps={
        "_integ_average_price_solar": {
            "initial": {"init_aps": 1},
            "step": {"change_in_price_solar": 1},
        }
    },
)
def average_price_solar():
    """
    Average market solar energy price.
    """
    return _integ_average_price_solar()


_integ_average_price_solar = Integ(
    lambda: change_in_price_solar(), lambda: init_aps(), "_integ_average_price_solar"
)


@component.add(
    name="Average Price Wind",
    units="$/toe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_average_price_wind": 1},
    other_deps={
        "_integ_average_price_wind": {
            "initial": {"init_apw": 1},
            "step": {"change_in_price_wind": 1},
        }
    },
)
def average_price_wind():
    """
    Average market wind energy price.
    """
    return _integ_average_price_wind()


_integ_average_price_wind = Integ(
    lambda: change_in_price_wind(), lambda: init_apw(), "_integ_average_price_wind"
)


@component.add(
    name="Biomass Price toe",
    units="$/toe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biomass_energy_price": 1, "toe_per_mtoe": 1},
)
def biomass_price_toe():
    """
    Actual biomass energy price in dollars per toe.
    """
    return biomass_energy_price() / toe_per_mtoe()


@component.add(
    name="Carbon Price Change",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "scenario_bioenergyplus": 2,
        "time": 1,
        "factor_of_carbon_price_change": 1,
    },
)
def carbon_price_change():
    """
    WWF Scenario variable. Further development required.
    """
    return (1 - scenario_bioenergyplus()) * 1 + scenario_bioenergyplus() * (
        1 + step(__data["time"], factor_of_carbon_price_change(), 2010)
    )


@component.add(
    name="Change in Market Share Biomass",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_change_in_market_share_biomass": 1},
    other_deps={
        "_integ_change_in_market_share_biomass": {
            "initial": {
                "reference_change_in_market_share_biomass": 1,
                "effect_of_price_on_market_share_biomass": 1,
            },
            "step": {"change_rate_due_to_price_biomass": 1},
        }
    },
)
def change_in_market_share_biomass():
    """
    Change in biomass energy market share due to price competitiveness.
    """
    return _integ_change_in_market_share_biomass()


_integ_change_in_market_share_biomass = Integ(
    lambda: change_rate_due_to_price_biomass(),
    lambda: reference_change_in_market_share_biomass()
    * effect_of_price_on_market_share_biomass(),
    "_integ_change_in_market_share_biomass",
)


@component.add(
    name="Change in Market Share Coal",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_change_in_market_share_coal": 1},
    other_deps={
        "_integ_change_in_market_share_coal": {
            "initial": {
                "reference_change_in_market_share_coal": 1,
                "effect_of_price_on_market_share_coal": 1,
            },
            "step": {"change_rate_due_to_price_coal": 1},
        }
    },
)
def change_in_market_share_coal():
    """
    Change in coal energy market share due to price competitiveness.
    """
    return _integ_change_in_market_share_coal()


_integ_change_in_market_share_coal = Integ(
    lambda: change_rate_due_to_price_coal(),
    lambda: reference_change_in_market_share_coal()
    * effect_of_price_on_market_share_coal(),
    "_integ_change_in_market_share_coal",
)


@component.add(
    name="Change in Market Share Gas",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_change_in_market_share_gas": 1},
    other_deps={
        "_integ_change_in_market_share_gas": {
            "initial": {
                "reference_change_in_market_share_gas": 1,
                "effect_of_price_on_market_share_gas": 1,
            },
            "step": {"change_rate_due_to_price_gas": 1},
        }
    },
)
def change_in_market_share_gas():
    """
    Change in gas energy market share due to price competitiveness.
    """
    return _integ_change_in_market_share_gas()


_integ_change_in_market_share_gas = Integ(
    lambda: change_rate_due_to_price_gas(),
    lambda: reference_change_in_market_share_gas()
    * effect_of_price_on_market_share_gas(),
    "_integ_change_in_market_share_gas",
)


@component.add(
    name="Change in Market Share Oil",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_change_in_market_share_oil": 1},
    other_deps={
        "_integ_change_in_market_share_oil": {
            "initial": {
                "reference_change_in_market_share_oil": 1,
                "effect_of_price_on_market_share_oil": 1,
            },
            "step": {"change_rate_due_to_price_oil": 1},
        }
    },
)
def change_in_market_share_oil():
    """
    Change in oil energy market share due to price competitiveness.
    """
    return _integ_change_in_market_share_oil()


_integ_change_in_market_share_oil = Integ(
    lambda: change_rate_due_to_price_oil(),
    lambda: reference_change_in_market_share_oil()
    * effect_of_price_on_market_share_oil(),
    "_integ_change_in_market_share_oil",
)


@component.add(
    name="Change in Market Share Solar",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_change_in_market_share_solar": 1},
    other_deps={
        "_integ_change_in_market_share_solar": {
            "initial": {
                "reference_change_in_market_share_solar": 1,
                "effect_of_price_on_market_share_solar": 1,
            },
            "step": {"change_rate_due_to_price_solar": 1},
        }
    },
)
def change_in_market_share_solar():
    """
    Change in solar energy market share due to price competitiveness.
    """
    return _integ_change_in_market_share_solar()


_integ_change_in_market_share_solar = Integ(
    lambda: change_rate_due_to_price_solar(),
    lambda: reference_change_in_market_share_solar()
    * effect_of_price_on_market_share_solar(),
    "_integ_change_in_market_share_solar",
)


@component.add(
    name="Change in Market Share Wind",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_change_in_market_share_wind": 1},
    other_deps={
        "_integ_change_in_market_share_wind": {
            "initial": {
                "reference_change_in_market_share_wind": 1,
                "effect_of_price_on_market_share_wind": 1,
            },
            "step": {"change_rate_due_to_price_wind": 1},
        }
    },
)
def change_in_market_share_wind():
    """
    Change in wind energy market share due to price competitiveness.
    """
    return _integ_change_in_market_share_wind()


_integ_change_in_market_share_wind = Integ(
    lambda: change_rate_due_to_price_wind(),
    lambda: reference_change_in_market_share_wind()
    * effect_of_price_on_market_share_wind(),
    "_integ_change_in_market_share_wind",
)


@component.add(
    name="Change in Price Biomass",
    units="$/(toe*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_price_toe": 1,
        "average_price_biomass": 1,
        "time_to_average_price_biomass": 1,
    },
)
def change_in_price_biomass():
    """
    Change in average market biomass energy price.
    """
    return (
        biomass_price_toe() - average_price_biomass()
    ) / time_to_average_price_biomass()


@component.add(
    name="Change in Price Coal",
    units="$/(toe*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "coal_price_toe": 1,
        "average_price_coal": 1,
        "time_to_average_price_coal": 1,
    },
)
def change_in_price_coal():
    """
    Change in average market coal price.
    """
    return (coal_price_toe() - average_price_coal()) / time_to_average_price_coal()


@component.add(
    name="Change in Price Gas",
    units="$/(toe*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gas_price_toe": 1,
        "average_price_gas": 1,
        "time_to_average_price_gas": 1,
    },
)
def change_in_price_gas():
    """
    Change in average market gas price.
    """
    return (gas_price_toe() - average_price_gas()) / time_to_average_price_gas()


@component.add(
    name="Change in Price Oil",
    units="$/(Year*toe)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "oil_price_toe": 1,
        "average_price_oil": 1,
        "time_to_average_price_oil": 1,
    },
)
def change_in_price_oil():
    """
    Change in average market oil price.
    """
    return (oil_price_toe() - average_price_oil()) / time_to_average_price_oil()


@component.add(
    name="Change in Price Solar",
    units="$/(toe*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "solar_price_toe": 1,
        "average_price_solar": 1,
        "time_to_average_price_solar": 1,
    },
)
def change_in_price_solar():
    """
    Change in average market solar energy price.
    """
    return (solar_price_toe() - average_price_solar()) / time_to_average_price_solar()


@component.add(
    name="Change in Price Wind",
    units="$/(toe*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wind_price_toe": 1,
        "average_price_wind": 1,
        "time_to_average_price_wind": 1,
    },
)
def change_in_price_wind():
    """
    Change in average market wind energy price.
    """
    return (wind_price_toe() - average_price_wind()) / time_to_average_price_wind()


@component.add(
    name="Change Rate Due to Price Biomass",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_change_in_market_share_biomass": 1,
        "effect_of_price_on_market_share_biomass": 1,
        "change_in_market_share_biomass": 1,
        "time_to_adjust_market_share": 1,
    },
)
def change_rate_due_to_price_biomass():
    """
    Ratio of change in biomass energy market share.
    """
    return (
        reference_change_in_market_share_biomass()
        * effect_of_price_on_market_share_biomass()
        - change_in_market_share_biomass()
    ) / time_to_adjust_market_share()


@component.add(
    name="Change Rate Due to Price Coal",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_change_in_market_share_coal": 1,
        "effect_of_price_on_market_share_coal": 1,
        "change_in_market_share_coal": 1,
        "time_to_adjust_market_share": 1,
    },
)
def change_rate_due_to_price_coal():
    """
    Ratio of change in coal energy market share.
    """
    return (
        reference_change_in_market_share_coal() * effect_of_price_on_market_share_coal()
        - change_in_market_share_coal()
    ) / time_to_adjust_market_share()


@component.add(
    name="Change Rate Due to Price Gas",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_change_in_market_share_gas": 1,
        "effect_of_price_on_market_share_gas": 1,
        "change_in_market_share_gas": 1,
        "time_to_adjust_market_share": 1,
    },
)
def change_rate_due_to_price_gas():
    """
    Ratio of change in gas energy market share.
    """
    return (
        reference_change_in_market_share_gas() * effect_of_price_on_market_share_gas()
        - change_in_market_share_gas()
    ) / time_to_adjust_market_share()


@component.add(
    name="Change Rate Due to Price Oil",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_change_in_market_share_oil": 1,
        "effect_of_price_on_market_share_oil": 1,
        "change_in_market_share_oil": 1,
        "time_to_adjust_market_share": 1,
    },
)
def change_rate_due_to_price_oil():
    """
    Ratio of change in oil energy market share.
    """
    return (
        reference_change_in_market_share_oil() * effect_of_price_on_market_share_oil()
        - change_in_market_share_oil()
    ) / time_to_adjust_market_share()


@component.add(
    name="Change Rate Due to Price Solar",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_change_in_market_share_solar": 1,
        "effect_of_price_on_market_share_solar": 1,
        "change_in_market_share_solar": 1,
        "time_to_adjust_market_share": 1,
    },
)
def change_rate_due_to_price_solar():
    """
    Ratio of change in solar energy market share.
    """
    return (
        reference_change_in_market_share_solar()
        * effect_of_price_on_market_share_solar()
        - change_in_market_share_solar()
    ) / time_to_adjust_market_share()


@component.add(
    name="Change Rate Due to Price Wind",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_change_in_market_share_wind": 1,
        "effect_of_price_on_market_share_wind": 1,
        "change_in_market_share_wind": 1,
        "time_to_adjust_market_share": 1,
    },
)
def change_rate_due_to_price_wind():
    """
    Ratio of change in wind energy market share.
    """
    return (
        reference_change_in_market_share_wind() * effect_of_price_on_market_share_wind()
        - change_in_market_share_wind()
    ) / time_to_adjust_market_share()


@component.add(
    name="Coal Price toe",
    units="$/toe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"coal_price": 1, "toe_per_mtoe": 1},
)
def coal_price_toe():
    """
    Actual coal price in dollars per toe.
    """
    return coal_price() / toe_per_mtoe()


@component.add(
    name="E Var T", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def e_var_t():
    return 0


@component.add(
    name="Effect of Price on Market Share Biomass",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "price_competitiveness_factor_biomass": 1,
        "price_elasticity_of_demand_biomass": 1,
    },
)
def effect_of_price_on_market_share_biomass():
    """
    Effect of biomass energy price competitiveness on market share.
    """
    return (
        price_competitiveness_factor_biomass() ** -price_elasticity_of_demand_biomass()
    )


@component.add(
    name="Effect of Price on Market Share Coal",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "price_competitiveness_factor_coal": 1,
        "price_elasticity_of_demand_coal": 1,
    },
)
def effect_of_price_on_market_share_coal():
    """
    Effect of coal energy price competitiveness on market share.
    """
    return price_competitiveness_factor_coal() ** -price_elasticity_of_demand_coal()


@component.add(
    name="Effect of Price on Market Share Gas",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "price_competitiveness_factor_gas": 1,
        "price_elasticity_of_demand_gas": 1,
    },
)
def effect_of_price_on_market_share_gas():
    """
    Effect of gas energy price competitiveness on market share.
    """
    return price_competitiveness_factor_gas() ** -price_elasticity_of_demand_gas()


@component.add(
    name="Effect of Price on Market Share Oil",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "price_competitiveness_factor_oil": 1,
        "price_elasticity_of_demand_oil": 1,
    },
)
def effect_of_price_on_market_share_oil():
    """
    Effect of oil energy price competitiveness on market share.
    """
    return price_competitiveness_factor_oil() ** -price_elasticity_of_demand_oil()


@component.add(
    name="Effect of Price on Market Share Solar",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "price_competitiveness_factor_solar": 1,
        "price_elasticity_of_demand_solar": 1,
    },
)
def effect_of_price_on_market_share_solar():
    """
    Effect of solar energy price competitiveness on market share.
    """
    return price_competitiveness_factor_solar() ** -price_elasticity_of_demand_solar()


@component.add(
    name="Effect of Price on Market Share Wind",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "price_competitiveness_factor_wind": 1,
        "price_elasticity_of_demand_wind": 1,
    },
)
def effect_of_price_on_market_share_wind():
    """
    Effect of wind energy price competitiveness on market share.
    """
    return price_competitiveness_factor_wind() ** -price_elasticity_of_demand_wind()


@component.add(
    name="Energy Demand",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_demand_per_capita": 1, "population": 1},
)
def energy_demand():
    """
    Total world demand for energy determined by population and energy demand per capita. Source of historical data: International Energy Agency – Key World Energy Statistics 2007
    """
    return energy_demand_per_capita() * population()


@component.add(
    name="Energy Demand 1900 Calibration",
    units="Mtoe/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def energy_demand_1900_calibration():
    """
    Energy demand calibration factor for year 1900.
    """
    return 120


@component.add(
    name="Energy Demand EJ",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_demand": 1, "mtoe_into_ej": 1},
)
def energy_demand_ej():
    return energy_demand() * mtoe_into_ej()


@component.add(
    name="Energy Demand Fulfillment Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_production": 1, "energy_demand": 1},
)
def energy_demand_fulfillment_ratio():
    """
    Ratio of energy production to energy demand indicating a level of energy demand fulfillment.
    """
    return energy_production() / energy_demand()


@component.add(
    name="Energy Demand per Capita",
    units="Mtoe/(Year*Person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_energy_demand_per_capita": 1,
        "impact_of_gwp_on_energy_demand_per_capita": 1,
    },
)
def energy_demand_per_capita():
    """
    Energy demand per capita taking into consideration the change in population wealth.
    """
    return max_energy_demand_per_capita() * impact_of_gwp_on_energy_demand_per_capita()


@component.add(
    name="Energy Production",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "coal_production": 1,
        "gas_production": 1,
        "oil_production": 1,
        "biomass_energy_production": 1,
        "solar_energy_production": 1,
        "wind_energy_production": 1,
    },
)
def energy_production():
    """
    Total energy production per year.
    """
    return (
        coal_production()
        + gas_production()
        + oil_production()
        + biomass_energy_production()
        + solar_energy_production()
        + wind_energy_production()
    )


@component.add(
    name="Factor of Carbon Price Change",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def factor_of_carbon_price_change():
    """
    WWF Scenario variable. Further development required.
    """
    return 99


@component.add(
    name="Gas Price toe",
    units="$/toe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gas_price": 1, "toe_per_mtoe": 1},
)
def gas_price_toe():
    """
    Actual gas price in dollars per toe.
    """
    return gas_price() / toe_per_mtoe()


@component.add(
    name="Impact of GWP on Energy Demand per Capita",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "impact_of_gwp_per_capita_on_energy_demand_inflection": 2,
        "impact_of_gwp_per_capita_on_energy_demand_steepness": 3,
        "smoothed_gwp_per_capita": 1,
        "reference_gwp_per_capita_for_energy_demand": 1,
    },
)
def impact_of_gwp_on_energy_demand_per_capita():
    """
    Impact of population wealth on energy demand per capita.
    """
    return (
        1
        - impact_of_gwp_per_capita_on_energy_demand_inflection()
        ** impact_of_gwp_per_capita_on_energy_demand_steepness()
        / (
            impact_of_gwp_per_capita_on_energy_demand_inflection()
            ** impact_of_gwp_per_capita_on_energy_demand_steepness()
            + (smoothed_gwp_per_capita() / reference_gwp_per_capita_for_energy_demand())
            ** impact_of_gwp_per_capita_on_energy_demand_steepness()
        )
    )


@component.add(
    name="Impact of GWP per Capita on Energy Demand Inflection",
    units="Dmnl",
    limits=(0.4, 1.0, 0.05),
    comp_type="Constant",
    comp_subtype="Normal",
)
def impact_of_gwp_per_capita_on_energy_demand_inflection():
    """
    A parameter determining the inflection point of the nonlinear function representing the impact of population wealth on energy demand.
    """
    return 1.1


@component.add(
    name="Impact of GWP per Capita on Energy Demand Steepness",
    units="Dmnl",
    limits=(0.5, 3.0, 0.05),
    comp_type="Constant",
    comp_subtype="Normal",
)
def impact_of_gwp_per_capita_on_energy_demand_steepness():
    """
    A parameter determining the steepness of the nonlinear function representing the impact of population wealth on energy demand.
    """
    return 0.7946


@component.add(
    name="INIT APB", units="$/toe", comp_type="Constant", comp_subtype="Normal"
)
def init_apb():
    """
    Initial average market biomass energy price.
    """
    return 500


@component.add(
    name="INIT APC", units="$/toe", comp_type="Constant", comp_subtype="Normal"
)
def init_apc():
    """
    Initial average market coal price.
    """
    return 4


@component.add(
    name="INIT APG", units="$/toe", comp_type="Constant", comp_subtype="Normal"
)
def init_apg():
    """
    Initial average market gas price.
    """
    return 50000


@component.add(
    name="INIT APO", units="$/toe", comp_type="Constant", comp_subtype="Normal"
)
def init_apo():
    """
    Initial average market oil price.
    """
    return 35


@component.add(
    name="INIT APO per bbl",
    units="$/Barrel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"init_apo": 1, "mtoe_per_barrel": 1},
)
def init_apo_per_bbl():
    return init_apo() * mtoe_per_barrel()


@component.add(
    name="INIT APS", units="$/toe", comp_type="Constant", comp_subtype="Normal"
)
def init_aps():
    """
    Initial average market solar energy price.
    """
    return 50000


@component.add(
    name="INIT APW", units="$/toe", comp_type="Constant", comp_subtype="Normal"
)
def init_apw():
    """
    Initial average market wind energy price.
    """
    return 50000


@component.add(
    name="Market Share Biomass",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "change_in_market_share_biomass": 1,
        "reference_change_in_total_market_share": 1,
    },
)
def market_share_biomass():
    """
    Biomass energy market share among other energy sources.
    """
    return change_in_market_share_biomass() / reference_change_in_total_market_share()


@component.add(
    name="Market Share Biomass Allocation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def market_share_biomass_allocation():
    """
    Market share allocation between forest and energy crops biomass.
    """
    return 0.7


@component.add(
    name="Market Share Biomass Crops",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"market_share_biomass": 1, "market_share_biomass_allocation": 1},
)
def market_share_biomass_crops():
    """
    Energy crops specific biomass energy market share among other energy sources.
    """
    return market_share_biomass() * (1 - market_share_biomass_allocation())


@component.add(
    name="Market Share Biomass Forest",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"market_share_biomass": 1, "market_share_biomass_allocation": 1},
)
def market_share_biomass_forest():
    """
    Forest specific biomass energy market share among other energy sources.
    """
    return market_share_biomass() * market_share_biomass_allocation()


@component.add(
    name="Market Share Coal",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "change_in_market_share_coal": 1,
        "reference_change_in_total_market_share": 1,
    },
)
def market_share_coal():
    """
    Coal market share among other energy sources.
    """
    return change_in_market_share_coal() / reference_change_in_total_market_share()


@component.add(
    name="Market Share Gas",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "change_in_market_share_gas": 1,
        "reference_change_in_total_market_share": 1,
    },
)
def market_share_gas():
    """
    Gas market share among other energy sources.
    """
    return change_in_market_share_gas() / reference_change_in_total_market_share()


@component.add(
    name="Market Share Oil",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "change_in_market_share_oil": 1,
        "reference_change_in_total_market_share": 1,
    },
)
def market_share_oil():
    """
    Oil market share among other energy sources.
    """
    return change_in_market_share_oil() / reference_change_in_total_market_share()


@component.add(
    name="Market Share Renewables",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "market_share_biomass": 1,
        "market_share_solar": 1,
        "market_share_wind": 1,
    },
)
def market_share_renewables():
    return market_share_biomass() + market_share_solar() + market_share_wind()


@component.add(
    name="Market Share Renewables Indicator",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"market_share_renewables": 1},
)
def market_share_renewables_indicator():
    return market_share_renewables()


@component.add(
    name="Market Share Solar",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "change_in_market_share_solar": 1,
        "reference_change_in_total_market_share": 1,
    },
)
def market_share_solar():
    """
    Solar energy market share among other energy sources.
    """
    return change_in_market_share_solar() / reference_change_in_total_market_share()


@component.add(
    name="Market Share Wind",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "change_in_market_share_wind": 1,
        "reference_change_in_total_market_share": 1,
    },
)
def market_share_wind():
    """
    Wind energy market share among other energy sources.
    """
    return change_in_market_share_wind() / reference_change_in_total_market_share()


@component.add(
    name="Max Energy Demand per Capita",
    units="Mtoe/(Year*Person)",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"me_var_s": 1, "_smooth_max_energy_demand_per_capita": 1},
    other_deps={
        "_smooth_max_energy_demand_per_capita": {
            "initial": {
                "max_energy_demand_per_capita_variation": 1,
                "me_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "max_energy_demand_per_capita_variation": 1,
                "me_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_demand_variation_time": 1,
            },
        }
    },
)
def max_energy_demand_per_capita():
    """
    Maximal reference Energy Demand per Capita.
    """
    return me_var_s() + _smooth_max_energy_demand_per_capita()


_smooth_max_energy_demand_per_capita = Smooth(
    lambda: step(
        __data["time"],
        max_energy_demand_per_capita_variation() - me_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_demand_variation_time(),
    lambda: step(
        __data["time"],
        max_energy_demand_per_capita_variation() - me_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_max_energy_demand_per_capita",
)


@component.add(
    name="Max Energy Demand per Capita Variation",
    units="Mtoe/(Year*Person)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_energy_demand_per_capita_variation():
    """
    Maximal reference Energy Demand per Capita.
    """
    return 4.8e-06


@component.add(
    name="ME S", units="Mtoe/(Year*Person)", comp_type="Constant", comp_subtype="Normal"
)
def me_s():
    """
    Maximal reference Energy Demand per Capita.
    """
    return 4.8e-06


@component.add(
    name="ME Var S",
    units="Mtoe/(Year*Person)",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_me_var_s": 1},
    other_deps={
        "_smooth_me_var_s": {
            "initial": {"me_s": 1, "time": 1},
            "step": {"me_s": 1, "time": 1},
        }
    },
)
def me_var_s():
    """
    Maximal reference Energy Demand per Capita.
    """
    return 4.8e-06 + _smooth_me_var_s()


_smooth_me_var_s = Smooth(
    lambda: step(__data["time"], me_s() - 4.8e-06, 2020),
    lambda: 1,
    lambda: step(__data["time"], me_s() - 4.8e-06, 2020),
    lambda: 1,
    "_smooth_me_var_s",
)


@component.add(
    name="Mtoe into EJ", units="EJ/Mtoe", comp_type="Constant", comp_subtype="Normal"
)
def mtoe_into_ej():
    return 1 / 23.8846


@component.add(
    name="Number of Energy Sources",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def number_of_energy_sources():
    """
    Number of various energy sources to average energy price.
    """
    return 6


@component.add(
    name="Oil Price toe",
    units="$/toe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_price": 1, "toe_per_mtoe": 1},
)
def oil_price_toe():
    """
    Actual oil price in dollars per toe.
    """
    return oil_price() / toe_per_mtoe()


@component.add(name="PEB S", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def peb_s():
    """
    Biomass energy price elasticity of demand.
    """
    return 0.8


@component.add(
    name="PEB Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_peb_var_s": 1},
    other_deps={
        "_smooth_peb_var_s": {
            "initial": {"peb_s": 1, "time": 1},
            "step": {"peb_s": 1, "time": 1},
        }
    },
)
def peb_var_s():
    """
    Biomass energy price elasticity of demand.
    """
    return 0.8 + _smooth_peb_var_s()


_smooth_peb_var_s = Smooth(
    lambda: step(__data["time"], peb_s() - 0.8, 2020),
    lambda: 1,
    lambda: step(__data["time"], peb_s() - 0.8, 2020),
    lambda: 1,
    "_smooth_peb_var_s",
)


@component.add(name="PEC S", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def pec_s():
    """
    Coal energy price elasticity of demand.
    """
    return 0.89


@component.add(
    name="PEC Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_pec_var_s": 1},
    other_deps={
        "_smooth_pec_var_s": {
            "initial": {"pec_s": 1, "time": 1},
            "step": {"pec_s": 1, "time": 1},
        }
    },
)
def pec_var_s():
    """
    Coal energy price elasticity of demand.
    """
    return 0.89 + _smooth_pec_var_s()


_smooth_pec_var_s = Smooth(
    lambda: step(__data["time"], pec_s() - 0.89, 2020),
    lambda: 1,
    lambda: step(__data["time"], pec_s() - 0.89, 2020),
    lambda: 1,
    "_smooth_pec_var_s",
)


@component.add(name="PEG S", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def peg_s():
    """
    Gas energy price elasticity of demand.
    """
    return 0.54


@component.add(
    name="PEG Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_peg_var_s": 1},
    other_deps={
        "_smooth_peg_var_s": {
            "initial": {"peg_s": 1, "time": 1},
            "step": {"peg_s": 1, "time": 1},
        }
    },
)
def peg_var_s():
    """
    Gas energy price elasticity of demand.
    """
    return 0.54 + _smooth_peg_var_s()


_smooth_peg_var_s = Smooth(
    lambda: step(__data["time"], peg_s() - 0.54, 2020),
    lambda: 1,
    lambda: step(__data["time"], peg_s() - 0.54, 2020),
    lambda: 1,
    "_smooth_peg_var_s",
)


@component.add(name="PEO S", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def peo_s():
    """
    Oil energy price elasticity of demand.
    """
    return 0.6


@component.add(
    name="PEO Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_peo_var_s": 1},
    other_deps={
        "_smooth_peo_var_s": {
            "initial": {"peo_s": 1, "time": 1},
            "step": {"peo_s": 1, "time": 1},
        }
    },
)
def peo_var_s():
    """
    Oil energy price elasticity of demand.
    """
    return 0.6 + _smooth_peo_var_s()


_smooth_peo_var_s = Smooth(
    lambda: step(__data["time"], peo_s() - 0.6, 2020),
    lambda: 1,
    lambda: step(__data["time"], peo_s() - 0.6, 2020),
    lambda: 1,
    "_smooth_peo_var_s",
)


@component.add(name="PEW S", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def pew_s():
    """
    Wind energy price elasticity of demand.
    """
    return 1


@component.add(
    name="PEW Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_pew_var_s": 1},
    other_deps={
        "_smooth_pew_var_s": {
            "initial": {"pew_s": 1, "time": 1},
            "step": {"pew_s": 1, "time": 1},
        }
    },
)
def pew_var_s():
    """
    Wind energy price elasticity of demand.
    """
    return 1 + _smooth_pew_var_s()


_smooth_pew_var_s = Smooth(
    lambda: step(__data["time"], pew_s() - 1, 2020),
    lambda: 1,
    lambda: step(__data["time"], pew_s() - 1, 2020),
    lambda: 1,
    "_smooth_pew_var_s",
)


@component.add(
    name="Price Competitiveness Factor Biomass",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"average_price_biomass": 1, "average_energy_price": 1},
)
def price_competitiveness_factor_biomass():
    """
    Biomass energy price competitiveness as a ratio of biomass energy market price to average market energy price.
    """
    return average_price_biomass() / average_energy_price()


@component.add(
    name="Price Competitiveness Factor Coal",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "carbon_price_change": 1,
        "average_price_coal": 1,
        "average_energy_price": 1,
    },
)
def price_competitiveness_factor_coal():
    """
    Coal price competitiveness as a ratio of coal market price to average market energy price.
    """
    return carbon_price_change() * average_price_coal() / average_energy_price()


@component.add(
    name="Price Competitiveness Factor Gas",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "carbon_price_change": 1,
        "average_price_gas": 1,
        "average_energy_price": 1,
    },
)
def price_competitiveness_factor_gas():
    """
    Gas price competitiveness as a ratio of gas market price to average market energy price.
    """
    return carbon_price_change() * average_price_gas() / average_energy_price()


@component.add(
    name="Price Competitiveness Factor Oil",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "carbon_price_change": 1,
        "average_price_oil": 1,
        "average_energy_price": 1,
    },
)
def price_competitiveness_factor_oil():
    """
    Oil price competitiveness as a ratio of oil market price to average market energy price.
    """
    return carbon_price_change() * average_price_oil() / average_energy_price()


@component.add(
    name="Price Competitiveness Factor Solar",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"average_price_solar": 1, "average_energy_price": 1},
)
def price_competitiveness_factor_solar():
    """
    Solar energy price competitiveness as a ratio of solar energy market price to average market energy price.
    """
    return average_price_solar() / average_energy_price()


@component.add(
    name="Price Competitiveness Factor Wind",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"average_price_wind": 1, "average_energy_price": 1},
)
def price_competitiveness_factor_wind():
    """
    Wind energy price competitiveness as a ratio of wind energy market price to average market energy price.
    """
    return average_price_wind() / average_energy_price()


@component.add(
    name="Price Elasticity of Demand Biomass",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"peb_var_s": 1, "_smooth_price_elasticity_of_demand_biomass": 1},
    other_deps={
        "_smooth_price_elasticity_of_demand_biomass": {
            "initial": {
                "price_elasticity_of_demand_biomass_variation": 1,
                "peb_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "price_elasticity_of_demand_biomass_variation": 1,
                "peb_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_demand_variation_time": 1,
            },
        }
    },
)
def price_elasticity_of_demand_biomass():
    """
    Biomass energy price elasticity of demand.
    """
    return peb_var_s() + _smooth_price_elasticity_of_demand_biomass()


_smooth_price_elasticity_of_demand_biomass = Smooth(
    lambda: step(
        __data["time"],
        price_elasticity_of_demand_biomass_variation() - peb_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_demand_variation_time(),
    lambda: step(
        __data["time"],
        price_elasticity_of_demand_biomass_variation() - peb_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_price_elasticity_of_demand_biomass",
)


@component.add(
    name="Price Elasticity of Demand Biomass Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def price_elasticity_of_demand_biomass_variation():
    """
    Biomass energy price elasticity of demand.
    """
    return 0.8


@component.add(
    name="Price Elasticity of Demand Coal",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"pec_var_s": 1, "_smooth_price_elasticity_of_demand_coal": 1},
    other_deps={
        "_smooth_price_elasticity_of_demand_coal": {
            "initial": {
                "price_elasticity_of_demand_coal_variation": 1,
                "pec_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "price_elasticity_of_demand_coal_variation": 1,
                "pec_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_demand_variation_time": 1,
            },
        }
    },
)
def price_elasticity_of_demand_coal():
    """
    Coal energy price elasticity of demand.
    """
    return pec_var_s() + _smooth_price_elasticity_of_demand_coal()


_smooth_price_elasticity_of_demand_coal = Smooth(
    lambda: step(
        __data["time"],
        price_elasticity_of_demand_coal_variation() - pec_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_demand_variation_time(),
    lambda: step(
        __data["time"],
        price_elasticity_of_demand_coal_variation() - pec_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_price_elasticity_of_demand_coal",
)


@component.add(
    name="Price Elasticity of Demand Coal Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def price_elasticity_of_demand_coal_variation():
    """
    Coal energy price elasticity of demand.
    """
    return 0.89


@component.add(
    name="Price Elasticity of Demand Gas",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"peg_var_s": 1, "_smooth_price_elasticity_of_demand_gas": 1},
    other_deps={
        "_smooth_price_elasticity_of_demand_gas": {
            "initial": {
                "price_elasticity_of_demand_gas_variation": 1,
                "peg_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "price_elasticity_of_demand_gas_variation": 1,
                "peg_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_demand_variation_time": 1,
            },
        }
    },
)
def price_elasticity_of_demand_gas():
    """
    Gas energy price elasticity of demand.
    """
    return peg_var_s() + _smooth_price_elasticity_of_demand_gas()


_smooth_price_elasticity_of_demand_gas = Smooth(
    lambda: step(
        __data["time"],
        price_elasticity_of_demand_gas_variation() - peg_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_demand_variation_time(),
    lambda: step(
        __data["time"],
        price_elasticity_of_demand_gas_variation() - peg_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_price_elasticity_of_demand_gas",
)


@component.add(
    name="Price Elasticity of Demand Gas Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def price_elasticity_of_demand_gas_variation():
    """
    Gas energy price elasticity of demand.
    """
    return 0.54


@component.add(
    name="Price Elasticity of Demand Oil",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"peo_var_s": 1, "_smooth_price_elasticity_of_demand_oil": 1},
    other_deps={
        "_smooth_price_elasticity_of_demand_oil": {
            "initial": {
                "price_elasticity_of_demand_oil_variation": 1,
                "peo_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "price_elasticity_of_demand_oil_variation": 1,
                "peo_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_demand_variation_time": 1,
            },
        }
    },
)
def price_elasticity_of_demand_oil():
    """
    Oil energy price elasticity of demand.
    """
    return peo_var_s() + _smooth_price_elasticity_of_demand_oil()


_smooth_price_elasticity_of_demand_oil = Smooth(
    lambda: step(
        __data["time"],
        price_elasticity_of_demand_oil_variation() - peo_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_demand_variation_time(),
    lambda: step(
        __data["time"],
        price_elasticity_of_demand_oil_variation() - peo_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_price_elasticity_of_demand_oil",
)


@component.add(
    name="Price Elasticity of Demand Oil Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def price_elasticity_of_demand_oil_variation():
    """
    Oil energy price elasticity of demand.
    """
    return 0.6


@component.add(
    name="Price Elasticity of Demand Solar",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"pew_var_s": 1, "_smooth_price_elasticity_of_demand_solar": 1},
    other_deps={
        "_smooth_price_elasticity_of_demand_solar": {
            "initial": {
                "price_elasticity_of_demand_wind_and_solar_variation": 1,
                "pew_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "price_elasticity_of_demand_wind_and_solar_variation": 1,
                "pew_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_demand_variation_time": 1,
            },
        }
    },
)
def price_elasticity_of_demand_solar():
    """
    Solar energy price elasticity of demand.
    """
    return pew_var_s() + _smooth_price_elasticity_of_demand_solar()


_smooth_price_elasticity_of_demand_solar = Smooth(
    lambda: step(
        __data["time"],
        price_elasticity_of_demand_wind_and_solar_variation() - pew_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_demand_variation_time(),
    lambda: step(
        __data["time"],
        price_elasticity_of_demand_wind_and_solar_variation() - pew_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_price_elasticity_of_demand_solar",
)


@component.add(
    name="Price Elasticity of Demand Wind",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"pew_var_s": 1, "_smooth_price_elasticity_of_demand_wind": 1},
    other_deps={
        "_smooth_price_elasticity_of_demand_wind": {
            "initial": {
                "price_elasticity_of_demand_wind_and_solar_variation": 1,
                "pew_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "price_elasticity_of_demand_wind_and_solar_variation": 1,
                "pew_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_demand_variation_time": 1,
            },
        }
    },
)
def price_elasticity_of_demand_wind():
    """
    Wind energy price elasticity of demand.
    """
    return pew_var_s() + _smooth_price_elasticity_of_demand_wind()


_smooth_price_elasticity_of_demand_wind = Smooth(
    lambda: step(
        __data["time"],
        price_elasticity_of_demand_wind_and_solar_variation() - pew_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_demand_variation_time(),
    lambda: step(
        __data["time"],
        price_elasticity_of_demand_wind_and_solar_variation() - pew_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_price_elasticity_of_demand_wind",
)


@component.add(
    name="Price Elasticity of Demand Wind and Solar Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def price_elasticity_of_demand_wind_and_solar_variation():
    """
    Wind energy price elasticity of demand.
    """
    return 1


@component.add(name="RCBI S", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def rcbi_s():
    """
    Reference change in biomass energy market share due to price competitiveness.
    """
    return 1.5


@component.add(
    name="RCBI Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_rcbi_var_s": 1},
    other_deps={
        "_smooth_rcbi_var_s": {
            "initial": {"rcbi_s": 1, "time": 1},
            "step": {"rcbi_s": 1, "time": 1},
        }
    },
)
def rcbi_var_s():
    """
    Reference change in biomass energy market share due to price competitiveness.
    """
    return 1.5 + _smooth_rcbi_var_s()


_smooth_rcbi_var_s = Smooth(
    lambda: step(__data["time"], rcbi_s() - 1.5, 2020),
    lambda: 1,
    lambda: step(__data["time"], rcbi_s() - 1.5, 2020),
    lambda: 1,
    "_smooth_rcbi_var_s",
)


@component.add(name="RCF S", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def rcf_s():
    return 1


@component.add(
    name="RCF Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_rcf_var_s": 1},
    other_deps={
        "_smooth_rcf_var_s": {
            "initial": {"rcf_s": 1, "time": 1},
            "step": {"rcf_s": 1, "time": 1},
        }
    },
)
def rcf_var_s():
    return 1 + _smooth_rcf_var_s()


_smooth_rcf_var_s = Smooth(
    lambda: step(__data["time"], rcf_s() - 1, 2020),
    lambda: 1,
    lambda: step(__data["time"], rcf_s() - 1, 2020),
    lambda: 1,
    "_smooth_rcf_var_s",
)


@component.add(name="RCMS S", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def rcms_s():
    """
    Reference change in solar energy market share due to price competitiveness.
    """
    return 4.5


@component.add(
    name="RCMS Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_rcms_var_s": 1},
    other_deps={
        "_smooth_rcms_var_s": {
            "initial": {"rcms_s": 1, "time": 1},
            "step": {"rcms_s": 1, "time": 1},
        }
    },
)
def rcms_var_s():
    """
    Reference change in solar energy market share due to price competitiveness.
    """
    return 4.5 + _smooth_rcms_var_s()


_smooth_rcms_var_s = Smooth(
    lambda: step(__data["time"], rcms_s() - 4.5, 2020),
    lambda: 1,
    lambda: step(__data["time"], rcms_s() - 4.5, 2020),
    lambda: 1,
    "_smooth_rcms_var_s",
)


@component.add(name="RCMW S", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def rcmw_s():
    """
    Reference change in wind energy market share due to price competitiveness.
    """
    return 3


@component.add(
    name="RCMW Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_rcmw_var_s": 1},
    other_deps={
        "_smooth_rcmw_var_s": {
            "initial": {"rcmw_s": 1, "time": 1},
            "step": {"rcmw_s": 1, "time": 1},
        }
    },
)
def rcmw_var_s():
    """
    Reference change in wind energy market share due to price competitiveness.
    """
    return 3 + _smooth_rcmw_var_s()


_smooth_rcmw_var_s = Smooth(
    lambda: step(__data["time"], rcmw_s() - 3, 2020),
    lambda: 1,
    lambda: step(__data["time"], rcmw_s() - 3, 2020),
    lambda: 1,
    "_smooth_rcmw_var_s",
)


@component.add(
    name="Reference Change in Fossil Fuel Market Share Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_change_in_fossil_fuel_market_share_variation():
    return 1


@component.add(
    name="Reference Change in Market Share Biomass",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"rcbi_var_s": 1, "_smooth_reference_change_in_market_share_biomass": 1},
    other_deps={
        "_smooth_reference_change_in_market_share_biomass": {
            "initial": {
                "reference_change_in_market_share_biomass_variation": 1,
                "rcbi_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "reference_change_in_market_share_biomass_variation": 1,
                "rcbi_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_demand_variation_time": 1,
            },
        }
    },
)
def reference_change_in_market_share_biomass():
    """
    Reference change in biomass energy market share due to price competitiveness.
    """
    return rcbi_var_s() + _smooth_reference_change_in_market_share_biomass()


_smooth_reference_change_in_market_share_biomass = Smooth(
    lambda: step(
        __data["time"],
        reference_change_in_market_share_biomass_variation() - rcbi_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_demand_variation_time(),
    lambda: step(
        __data["time"],
        reference_change_in_market_share_biomass_variation() - rcbi_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_reference_change_in_market_share_biomass",
)


@component.add(
    name="Reference Change in Market Share Biomass Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_change_in_market_share_biomass_variation():
    """
    Reference change in biomass energy market share due to price competitiveness.
    """
    return 3.25


@component.add(
    name="Reference Change in Market Share Coal",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"rcf_var_s": 1, "_smooth_reference_change_in_market_share_coal": 1},
    other_deps={
        "_smooth_reference_change_in_market_share_coal": {
            "initial": {
                "reference_change_in_fossil_fuel_market_share_variation": 1,
                "rcf_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "reference_change_in_fossil_fuel_market_share_variation": 1,
                "rcf_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_demand_variation_time": 1,
            },
        }
    },
)
def reference_change_in_market_share_coal():
    """
    Reference change in coal energy market share due to price competitiveness.
    """
    return rcf_var_s() + _smooth_reference_change_in_market_share_coal()


_smooth_reference_change_in_market_share_coal = Smooth(
    lambda: step(
        __data["time"],
        reference_change_in_fossil_fuel_market_share_variation() - rcf_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_demand_variation_time(),
    lambda: step(
        __data["time"],
        reference_change_in_fossil_fuel_market_share_variation() - rcf_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_reference_change_in_market_share_coal",
)


@component.add(
    name="Reference Change in Market Share Gas",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"rcf_var_s": 1, "_smooth_reference_change_in_market_share_gas": 1},
    other_deps={
        "_smooth_reference_change_in_market_share_gas": {
            "initial": {
                "reference_change_in_fossil_fuel_market_share_variation": 1,
                "rcf_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "reference_change_in_fossil_fuel_market_share_variation": 1,
                "rcf_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_demand_variation_time": 1,
            },
        }
    },
)
def reference_change_in_market_share_gas():
    """
    Reference change in gas energy market share due to price competitiveness.
    """
    return rcf_var_s() + _smooth_reference_change_in_market_share_gas()


_smooth_reference_change_in_market_share_gas = Smooth(
    lambda: step(
        __data["time"],
        reference_change_in_fossil_fuel_market_share_variation() - rcf_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_demand_variation_time(),
    lambda: step(
        __data["time"],
        reference_change_in_fossil_fuel_market_share_variation() - rcf_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_reference_change_in_market_share_gas",
)


@component.add(
    name="Reference Change in Market Share Oil",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"rcf_var_s": 1, "_smooth_reference_change_in_market_share_oil": 1},
    other_deps={
        "_smooth_reference_change_in_market_share_oil": {
            "initial": {
                "reference_change_in_fossil_fuel_market_share_variation": 1,
                "rcf_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "reference_change_in_fossil_fuel_market_share_variation": 1,
                "rcf_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_demand_variation_time": 1,
            },
        }
    },
)
def reference_change_in_market_share_oil():
    """
    Reference change in oil energy market share due to price competitiveness.
    """
    return rcf_var_s() + _smooth_reference_change_in_market_share_oil()


_smooth_reference_change_in_market_share_oil = Smooth(
    lambda: step(
        __data["time"],
        reference_change_in_fossil_fuel_market_share_variation() - rcf_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_demand_variation_time(),
    lambda: step(
        __data["time"],
        reference_change_in_fossil_fuel_market_share_variation() - rcf_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_reference_change_in_market_share_oil",
)


@component.add(
    name="Reference Change in Market Share Solar",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"rcms_var_s": 1, "_smooth_reference_change_in_market_share_solar": 1},
    other_deps={
        "_smooth_reference_change_in_market_share_solar": {
            "initial": {
                "reference_change_in_market_share_solar_variation": 1,
                "rcms_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "reference_change_in_market_share_solar_variation": 1,
                "rcms_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_demand_variation_time": 1,
            },
        }
    },
)
def reference_change_in_market_share_solar():
    """
    Reference change in solar energy market share due to price competitiveness.
    """
    return rcms_var_s() + _smooth_reference_change_in_market_share_solar()


_smooth_reference_change_in_market_share_solar = Smooth(
    lambda: step(
        __data["time"],
        reference_change_in_market_share_solar_variation() - rcms_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_demand_variation_time(),
    lambda: step(
        __data["time"],
        reference_change_in_market_share_solar_variation() - rcms_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_reference_change_in_market_share_solar",
)


@component.add(
    name="Reference Change in Market Share Solar Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_change_in_market_share_solar_variation():
    """
    Reference change in solar energy market share due to price competitiveness.
    """
    return 8


@component.add(
    name="Reference Change in Market Share Wind",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"rcmw_var_s": 1, "_smooth_reference_change_in_market_share_wind": 1},
    other_deps={
        "_smooth_reference_change_in_market_share_wind": {
            "initial": {
                "reference_change_in_market_share_wind_variation": 1,
                "rcmw_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "reference_change_in_market_share_wind_variation": 1,
                "rcmw_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_demand_variation_time": 1,
            },
        }
    },
)
def reference_change_in_market_share_wind():
    """
    Reference change in wind energy market share due to price competitiveness.
    """
    return rcmw_var_s() + _smooth_reference_change_in_market_share_wind()


_smooth_reference_change_in_market_share_wind = Smooth(
    lambda: step(
        __data["time"],
        reference_change_in_market_share_wind_variation() - rcmw_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_demand_variation_time(),
    lambda: step(
        __data["time"],
        reference_change_in_market_share_wind_variation() - rcmw_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_reference_change_in_market_share_wind",
)


@component.add(
    name="Reference Change in Market Share Wind Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_change_in_market_share_wind_variation():
    """
    Reference change in wind energy market share due to price competitiveness.
    """
    return 6


@component.add(
    name="Reference Change in Total Market Share",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "change_in_market_share_oil": 1,
        "change_in_market_share_gas": 1,
        "change_in_market_share_coal": 1,
        "change_in_market_share_solar": 1,
        "change_in_market_share_wind": 1,
        "change_in_market_share_biomass": 1,
    },
)
def reference_change_in_total_market_share():
    """
    Reference Change in Total Market Share taking into account changes in specific energy sectors.
    """
    return (
        change_in_market_share_oil()
        + change_in_market_share_gas()
        + change_in_market_share_coal()
        + change_in_market_share_solar()
        + change_in_market_share_wind()
        + change_in_market_share_biomass()
    )


@component.add(
    name="Reference GWP per Capita for Energy Demand",
    units="$/(Year*Person)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_gwp_per_capita_for_energy_demand():
    """
    A reference value against which the GDP per Capita is compared to in order to calculate the impact of population wealth on energy demand.
    """
    return 16000


@component.add(
    name="SCENARIO BioenergyPlus",
    units="Dmnl",
    limits=(0.0, 1.0, 1.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def scenario_bioenergyplus():
    """
    WWF Scenario variable. Further development required.
    """
    return 0


@component.add(
    name="Solar Price toe",
    units="$/toe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"solar_energy_price": 1, "toe_per_mtoe": 1},
)
def solar_price_toe():
    """
    Actual solar energy price in dollars per toe.
    """
    return solar_energy_price() / toe_per_mtoe()


@component.add(
    name="Time to Adjust Market Share",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_adjust_market_share():
    """
    Time to adjust changes in market share.
    """
    return 10


@component.add(
    name="Time to Average Price Biomass",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_average_price_biomass():
    """
    Time to average market biomass energy price.
    """
    return 18


@component.add(
    name="Time to Average Price Coal",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_average_price_coal():
    """
    Time to average market coal price.
    """
    return 5


@component.add(
    name="Time to Average Price Gas",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_average_price_gas():
    """
    Time to average market gas price.
    """
    return 5


@component.add(
    name="Time to Average Price Oil",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_average_price_oil():
    """
    Time to average market oil price.
    """
    return 5


@component.add(
    name="Time to Average Price Solar",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_average_price_solar():
    """
    Time to average market solar energy price.
    """
    return 15


@component.add(
    name="Time to Average Price Wind",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_average_price_wind():
    """
    Time to average market wind energy price.
    """
    return 20


@component.add(
    name="Total Energy Market",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "market_share_oil": 1,
        "market_share_gas": 1,
        "market_share_coal": 1,
        "market_share_solar": 1,
        "market_share_wind": 1,
        "market_share_biomass": 1,
    },
)
def total_energy_market():
    """
    Total energy market share.
    """
    return (
        market_share_oil()
        + market_share_gas()
        + market_share_coal()
        + market_share_solar()
        + market_share_wind()
        + market_share_biomass()
    )


@component.add(
    name="Wind Price toe",
    units="$/toe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_energy_price": 1, "toe_per_mtoe": 1},
)
def wind_price_toe():
    """
    Actual wind energy price in dollars per toe.
    """
    return wind_energy_price() / toe_per_mtoe()
