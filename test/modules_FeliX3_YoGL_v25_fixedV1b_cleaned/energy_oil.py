"""
Module energy_oil
Translated using PySD version 3.14.3
"""

@component.add(
    name="Adjustment for Identified Oil Resource",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_identified_oil_resources": 1,
        "identified_oil_resources": 1,
        "identified_oil_resources_adjustment_time": 1,
    },
)
def adjustment_for_identified_oil_resource():
    """
    Adjustment of Identified Oil Resource to the desired level over a specified adjustment time.
    """
    return (
        required_identified_oil_resources() - identified_oil_resources()
    ) / identified_oil_resources_adjustment_time()


@component.add(
    name="Annual Change in Oil Reserves",
    units="Barrel/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"uro_var_s": 1, "_smooth_annual_change_in_oil_reserves": 1, "time": 1},
    other_deps={
        "_smooth_annual_change_in_oil_reserves": {
            "initial": {
                "annual_change_in_oil_reserves_variation": 1,
                "uro_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "annual_change_in_oil_reserves_variation": 1,
                "uro_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_production_variation_time": 1,
            },
        }
    },
)
def annual_change_in_oil_reserves():
    return step(
        __data["time"], uro_var_s() + _smooth_annual_change_in_oil_reserves(), 2010
    )


_smooth_annual_change_in_oil_reserves = Smooth(
    lambda: step(
        __data["time"],
        annual_change_in_oil_reserves_variation() - uro_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_production_variation_time(),
    lambda: step(
        __data["time"],
        annual_change_in_oil_reserves_variation() - uro_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_annual_change_in_oil_reserves",
)


@component.add(
    name="Annual Change in Oil Reserves Variation",
    units="Barrel/Year",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def annual_change_in_oil_reserves_variation():
    return 21000000000.0


@component.add(
    name="Average Oil Production",
    units="Mtoe/Year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_average_oil_production": 1},
    other_deps={
        "_integ_average_oil_production": {
            "initial": {"init_average_oil_production": 1},
            "step": {"change_in_average_oil_production": 1},
        }
    },
)
def average_oil_production():
    """
    Average total oil production per year.
    """
    return _integ_average_oil_production()


_integ_average_oil_production = Integ(
    lambda: change_in_average_oil_production(),
    lambda: init_average_oil_production(),
    "_integ_average_oil_production",
)


@component.add(
    name="Change in Average Oil Production",
    units="Mtoe/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "oil_production": 1,
        "average_oil_production": 1,
        "time_to_average_oil_production": 1,
    },
)
def change_in_average_oil_production():
    """
    Change in Average Oil Production.
    """
    return (
        oil_production() - average_oil_production()
    ) / time_to_average_oil_production()


@component.add(
    name="Change in Effective Investment in Oil Exploration",
    units="$/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_oil_exploration": 1,
        "effective_investment_in_oil_exploration": 1,
        "investment_in_oil_exploration_delay": 1,
    },
)
def change_in_effective_investment_in_oil_exploration():
    """
    Change in Effective Investment in Oil Exploration.
    """
    return (
        investment_in_oil_exploration() - effective_investment_in_oil_exploration()
    ) / investment_in_oil_exploration_delay()


@component.add(
    name="Change in Effective Investment in Oil Production",
    units="$/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_oil_production": 1,
        "effective_investment_in_oil_production": 1,
        "investment_in_oil_production_delay": 1,
    },
)
def change_in_effective_investment_in_oil_production():
    """
    Change in Effective Investment in Oil Production.
    """
    return (
        investment_in_oil_production() - effective_investment_in_oil_production()
    ) / investment_in_oil_production_delay()


@component.add(
    name="Change in Oil Productivity of Investment",
    units="toe/(Year*$)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "productivity_of_investment_in_oil_exploration": 1,
        "oil_productivity_of_investment": 1,
        "oil_production_coverage": 1,
    },
)
def change_in_oil_productivity_of_investment():
    """
    Change in Oil Productivity of Investment.
    """
    return (
        productivity_of_investment_in_oil_exploration()
        - oil_productivity_of_investment()
    ) / oil_production_coverage()


@component.add(
    name="Cumulative Additions to Oil Production",
    units="Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"identified_oil_resources": 1, "cumulative_oil_production": 1},
)
def cumulative_additions_to_oil_production():
    """
    Identified and already produced resources.
    """
    return identified_oil_resources() + cumulative_oil_production()


@component.add(
    name="Cumulative Oil Production",
    units="Mtoe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_oil_production": 1},
    other_deps={
        "_integ_cumulative_oil_production": {
            "initial": {"init_copn": 1},
            "step": {"oil_production": 1},
        }
    },
)
def cumulative_oil_production():
    """
    Cumulative Oil Resources that has been produced.
    """
    return _integ_cumulative_oil_production()


_integ_cumulative_oil_production = Integ(
    lambda: oil_production(), lambda: init_copn(), "_integ_cumulative_oil_production"
)


@component.add(
    name="Delay Time IROFDU",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_discovery_technology_development_time": 1},
)
def delay_time_irofdu():
    return oil_discovery_technology_development_time() / 3


@component.add(
    name="Delay Time IROFRU",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_recovery_technology_development_time": 1},
)
def delay_time_irofru():
    return oil_recovery_technology_development_time() / 3


@component.add(
    name="Desired Investment in Oil Exploration",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_oil_exploration_rate": 1, "unit_cost_of_oil_exploration": 1},
)
def desired_investment_in_oil_exploration():
    """
    Desired amount of resources that need to be invested in order to secure desired oil exploration.
    """
    return desired_oil_exploration_rate() * unit_cost_of_oil_exploration()


@component.add(
    name="Desired Investment in Oil Production",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_oil_production_from_resources": 1,
        "total_oil_demand": 1,
        "productivity_of_investment_in_oil_production": 1,
        "toe_per_mtoe": 1,
    },
)
def desired_investment_in_oil_production():
    """
    Desired Investment in Oil Production due to Total Oil Demand and Productivity of Investment in Oil Production.
    """
    return (
        float(np.minimum(potential_oil_production_from_resources(), total_oil_demand()))
        / productivity_of_investment_in_oil_production()
        * toe_per_mtoe()
    )


@component.add(
    name="Desired Oil Exploration Rate",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"adjustment_for_identified_oil_resource": 1, "oil_production": 1},
)
def desired_oil_exploration_rate():
    """
    Desired Oil exploration rate due to Total Oil Demand and Identified Oil Resources safety coverage.
    """
    return float(
        np.maximum(0, adjustment_for_identified_oil_resource() + oil_production())
    )


@component.add(
    name="Effect of Oil Demand and Supply on Price",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "so_init": 1,
        "sensitivity_of_oil_price_to_supply_and_demand": 1,
        "total_oil_demand": 1,
        "potential_oil_production": 1,
    },
)
def effect_of_oil_demand_and_supply_on_price():
    """
    Effect of Oil Demand and Supply ratio on actual oil price.
    """
    return (
        so_init()
        * (total_oil_demand() / potential_oil_production())
        ** sensitivity_of_oil_price_to_supply_and_demand()
    )


@component.add(
    name="Effect of Technology on Oil Discoveries",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_oil_discoverable_resources": 1, "init_uorn": 1},
)
def effect_of_technology_on_oil_discoveries():
    """
    Impact of technology development on oil exploration taking into account remaining undiscovered oil resources (the less remaining undiscovered oil resources the more expensive it to discover them).
    """
    return total_oil_discoverable_resources() / init_uorn()


@component.add(
    name="Effective Investment in Oil Exploration",
    units="$/Year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_effective_investment_in_oil_exploration": 1},
    other_deps={
        "_integ_effective_investment_in_oil_exploration": {
            "initial": {"init_eioe": 1},
            "step": {"change_in_effective_investment_in_oil_exploration": 1},
        }
    },
)
def effective_investment_in_oil_exploration():
    """
    Effective investments dedicated for oil resources exploration.
    """
    return _integ_effective_investment_in_oil_exploration()


_integ_effective_investment_in_oil_exploration = Integ(
    lambda: change_in_effective_investment_in_oil_exploration(),
    lambda: init_eioe(),
    "_integ_effective_investment_in_oil_exploration",
)


@component.add(
    name="Effective Investment in Oil Production",
    units="$/Year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_effective_investment_in_oil_production": 1},
    other_deps={
        "_integ_effective_investment_in_oil_production": {
            "initial": {"init_eiop": 1},
            "step": {"change_in_effective_investment_in_oil_production": 1},
        }
    },
)
def effective_investment_in_oil_production():
    """
    Effective investments dedicated for oil resources production.
    """
    return _integ_effective_investment_in_oil_production()


_integ_effective_investment_in_oil_production = Integ(
    lambda: change_in_effective_investment_in_oil_production(),
    lambda: init_eiop(),
    "_integ_effective_investment_in_oil_production",
)


@component.add(
    name="Effectiveness IROFDU",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_oil_discovery_technology": 1,
        "effectiveness_of_investment_in_oil_discovery_technology": 1,
    },
)
def effectiveness_irofdu():
    return (
        investment_in_oil_discovery_technology()
        * effectiveness_of_investment_in_oil_discovery_technology()
    )


@component.add(
    name="Effectiveness IROFRU",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_oil_recovery_technology": 1,
        "effectiveness_of_investment_in_oil_recovery_technology": 1,
    },
)
def effectiveness_irofru():
    return (
        investment_in_oil_recovery_technology()
        * effectiveness_of_investment_in_oil_recovery_technology()
    )


@component.add(
    name="Effectiveness of Investment in Oil Discovery Technology",
    units="1/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effectiveness_of_investment_in_oil_discovery_technology_variation": 1,
        "time": 1,
    },
)
def effectiveness_of_investment_in_oil_discovery_technology():
    """
    Effectiveness of resources dedicated to oil discovery technology development.
    """
    return 4.48e-09 + step(
        __data["time"],
        effectiveness_of_investment_in_oil_discovery_technology_variation() - 4.48e-09,
        2020,
    )


@component.add(
    name="Effectiveness of Investment in Oil Discovery Technology Variation",
    units="1/$",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def effectiveness_of_investment_in_oil_discovery_technology_variation():
    """
    Effectiveness of resources dedicated to oil discovery technology development.
    """
    return 4.48e-09


@component.add(
    name="Effectiveness of Investment in Oil Recovery Technology",
    units="1/$",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "eior_var_s": 1,
        "_smooth_effectiveness_of_investment_in_oil_recovery_technology": 1,
    },
    other_deps={
        "_smooth_effectiveness_of_investment_in_oil_recovery_technology": {
            "initial": {
                "effectiveness_of_investment_in_oil_recovery_technology_variation": 1,
                "eior_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "effectiveness_of_investment_in_oil_recovery_technology_variation": 1,
                "eior_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def effectiveness_of_investment_in_oil_recovery_technology():
    """
    Effectiveness of resources dedicated to recovery technology development.
    """
    return (
        eior_var_s() + _smooth_effectiveness_of_investment_in_oil_recovery_technology()
    )


_smooth_effectiveness_of_investment_in_oil_recovery_technology = Smooth(
    lambda: step(
        __data["time"],
        effectiveness_of_investment_in_oil_recovery_technology_variation()
        - eior_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        effectiveness_of_investment_in_oil_recovery_technology_variation()
        - eior_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_effectiveness_of_investment_in_oil_recovery_technology",
)


@component.add(
    name="Effectiveness of Investment in Oil Recovery Technology Variation",
    units="1/$",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effectiveness_of_investment_in_oil_recovery_technology_variation():
    """
    Effectiveness of resources dedicated to recovery technology development.
    """
    return 2.8e-11


@component.add(
    name="EIOR S",
    units="1/$",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def eior_s():
    """
    Effectiveness of resources dedicated to recovery technology development.
    """
    return 2.8e-11


@component.add(
    name="EIOR Var S",
    units="1/$",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_eior_var_s": 1},
    other_deps={
        "_smooth_eior_var_s": {
            "initial": {"eior_s": 1, "time": 1},
            "step": {"eior_s": 1, "time": 1},
        }
    },
)
def eior_var_s():
    """
    Effectiveness of resources dedicated to recovery technology development.
    """
    return 2.8e-11 + _smooth_eior_var_s()


_smooth_eior_var_s = Smooth(
    lambda: step(__data["time"], eior_s() - 2.8e-11, 2020),
    lambda: 1,
    lambda: step(__data["time"], eior_s() - 2.8e-11, 2020),
    lambda: 1,
    "_smooth_eior_var_s",
)


@component.add(
    name="FDR S",
    units="Year",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def fdr_s():
    return 6


@component.add(
    name="FDR Var S",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_fdr_var_s": 1},
    other_deps={
        "_smooth_fdr_var_s": {
            "initial": {"fdr_s": 1, "time": 1},
            "step": {"fdr_s": 1, "time": 1},
        }
    },
)
def fdr_var_s():
    return 6 + _smooth_fdr_var_s()


_smooth_fdr_var_s = Smooth(
    lambda: step(__data["time"], fdr_s() - 6, 2020),
    lambda: 1,
    lambda: step(__data["time"], fdr_s() - 6, 2020),
    lambda: 1,
    "_smooth_fdr_var_s",
)


@component.add(
    name="FO S",
    units="Dmnl",
    limits=(0.0, 1.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def fo_s():
    """
    Percentage of total oil sector revenue dedicated to exploration and production technology development.
    """
    return 0.04


@component.add(
    name="FO Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_fo_var_s": 1},
    other_deps={
        "_smooth_fo_var_s": {
            "initial": {"fo_s": 1, "time": 1},
            "step": {"fo_s": 1, "time": 1},
        }
    },
)
def fo_var_s():
    """
    Percentage of total oil sector revenue dedicated to exploration and production technology development.
    """
    return 0.04 + _smooth_fo_var_s()


_smooth_fo_var_s = Smooth(
    lambda: step(__data["time"], fo_s() - 0.04, 2020),
    lambda: 1,
    lambda: step(__data["time"], fo_s() - 0.04, 2020),
    lambda: 1,
    "_smooth_fo_var_s",
)


@component.add(
    name="Fossil Fuel Discovery and Recovery Technology Development Time Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fossil_fuel_discovery_and_recovery_technology_development_time_variation():
    return 6


@component.add(
    name="Fraction Invested in Oil Discovery Technology",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_fraction_discoverable": 1, "table_for_fiodt": 1},
)
def fraction_invested_in_oil_discovery_technology():
    """
    Fraction of investments in oil technology dedicated to discovery technology.
    """
    return table_for_fiodt(oil_fraction_discoverable())


@component.add(
    name="Fraction of Oil Revenues Invested in Technology",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "fo_var_s": 1,
        "_smooth_fraction_of_oil_revenues_invested_in_technology": 1,
    },
    other_deps={
        "_smooth_fraction_of_oil_revenues_invested_in_technology": {
            "initial": {
                "fraction_of_oil_revenues_invested_in_technology_variation": 1,
                "fo_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "fraction_of_oil_revenues_invested_in_technology_variation": 1,
                "fo_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def fraction_of_oil_revenues_invested_in_technology():
    """
    Percentage of total oil sector revenue dedicated to exploration and production technology development.
    """
    return fo_var_s() + _smooth_fraction_of_oil_revenues_invested_in_technology()


_smooth_fraction_of_oil_revenues_invested_in_technology = Smooth(
    lambda: step(
        __data["time"],
        fraction_of_oil_revenues_invested_in_technology_variation() - fo_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        fraction_of_oil_revenues_invested_in_technology_variation() - fo_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_fraction_of_oil_revenues_invested_in_technology",
)


@component.add(
    name="Fraction of Oil Revenues Invested in Technology Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraction_of_oil_revenues_invested_in_technology_variation():
    """
    Percentage of total oil sector revenue dedicated to exploration and production technology development.
    """
    return 0.04


@component.add(
    name="Identified Oil Resources",
    units="Mtoe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_identified_oil_resources": 1},
    other_deps={
        "_integ_identified_oil_resources": {
            "initial": {
                "total_oil_demand": 1,
                "normal_oil_production_ratio": 1,
                "oil_fraction_recoverable": 2,
                "cumulative_oil_production": 1,
            },
            "step": {"oil_exploration": 1, "oil_production": 1},
        }
    },
)
def identified_oil_resources():
    """
    Oil Resources discovered thanks to developments in exploration technology.
    """
    return _integ_identified_oil_resources()


_integ_identified_oil_resources = Integ(
    lambda: oil_exploration() - oil_production(),
    lambda: (
        total_oil_demand() * normal_oil_production_ratio()
        + cumulative_oil_production() * (1 - oil_fraction_recoverable())
    )
    / oil_fraction_recoverable(),
    "_integ_identified_oil_resources",
)


@component.add(
    name="Identified Oil Resources Adjustment Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def identified_oil_resources_adjustment_time():
    """
    Time to adjust Identified Oil Resource to the desired level.
    """
    return 2


@component.add(
    name="IF S",
    units="Year",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def if_s():
    return 5


@component.add(
    name="IF Var S",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_if_var_s": 1},
    other_deps={
        "_smooth_if_var_s": {
            "initial": {"if_s": 1, "time": 1},
            "step": {"if_s": 1, "time": 1},
        }
    },
)
def if_var_s():
    return 5 + _smooth_if_var_s()


_smooth_if_var_s = Smooth(
    lambda: step(__data["time"], if_s() - 5, 2020),
    lambda: 1,
    lambda: step(__data["time"], if_s() - 5, 2020),
    lambda: 1,
    "_smooth_if_var_s",
)


@component.add(
    name="Increase in Ratio of Oil Fraction Discoverable to Undiscoverable",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_irofdulv3": 1},
)
def increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable():
    """
    Increase in Ratio of Oil Fraction Discoverable to Undiscoverable due to investments in discovery technology and their productivity.
    """
    return outflow_irofdulv3()


@component.add(
    name="Increase in Ratio of Oil Fraction Discoverable to Undiscoverable LV1",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv1": 1
    },
    other_deps={
        "_integ_increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv1": {
            "initial": {
                "increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv3": 1
            },
            "step": {"inflow_irofdulv1": 1, "outflow_irofdulv1": 1},
        }
    },
)
def increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv1():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv1()


_integ_increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv1 = Integ(
    lambda: inflow_irofdulv1() - outflow_irofdulv1(),
    lambda: increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv3(),
    "_integ_increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv1",
)


@component.add(
    name="Increase in Ratio of Oil Fraction Discoverable to Undiscoverable LV2",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv2": 1
    },
    other_deps={
        "_integ_increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv2": {
            "initial": {
                "increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv3": 1
            },
            "step": {"inflow_irofdulv2": 1, "outflow_irofdulv2": 1},
        }
    },
)
def increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv2():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv2()


_integ_increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv2 = Integ(
    lambda: inflow_irofdulv2() - outflow_irofdulv2(),
    lambda: increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv3(),
    "_integ_increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv2",
)


@component.add(
    name="Increase in Ratio of Oil Fraction Discoverable to Undiscoverable LV3",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv3": 1
    },
    other_deps={
        "_integ_increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv3": {
            "initial": {"effectiveness_irofdu": 1, "delay_time_irofdu": 1},
            "step": {"inflow_irofdulv3": 1, "outflow_irofdulv3": 1},
        }
    },
)
def increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv3():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv3()


_integ_increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv3 = Integ(
    lambda: inflow_irofdulv3() - outflow_irofdulv3(),
    lambda: effectiveness_irofdu() * delay_time_irofdu(),
    "_integ_increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv3",
)


@component.add(
    name="Increase in Ratio of Oil Fraction Recoverable to Unrecoverable",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_irofrulv3": 1},
)
def increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable():
    """
    Increase in Ratio of Oil Fraction Recoverable to Unrecoverable due to investments in recovery technology and their productivity.
    """
    return outflow_irofrulv3()


@component.add(
    name="Increase in Ratio of Oil Fraction Recoverable to Unrecoverable LV1",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv1": 1
    },
    other_deps={
        "_integ_increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv1": {
            "initial": {
                "increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv3": 1
            },
            "step": {"inflow_irofrulv1": 1, "outflow_irofrulv1": 1},
        }
    },
)
def increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv1():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv1()


_integ_increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv1 = Integ(
    lambda: inflow_irofrulv1() - outflow_irofrulv1(),
    lambda: increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv3(),
    "_integ_increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv1",
)


@component.add(
    name="Increase in Ratio of Oil Fraction Recoverable to Unrecoverable LV2",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv2": 1
    },
    other_deps={
        "_integ_increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv2": {
            "initial": {
                "increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv3": 1
            },
            "step": {"inflow_irofrulv2": 1, "outflow_irofrulv2": 1},
        }
    },
)
def increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv2():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv2()


_integ_increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv2 = Integ(
    lambda: inflow_irofrulv2() - outflow_irofrulv2(),
    lambda: increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv3(),
    "_integ_increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv2",
)


@component.add(
    name="Increase in Ratio of Oil Fraction Recoverable to Unrecoverable LV3",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv3": 1
    },
    other_deps={
        "_integ_increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv3": {
            "initial": {"effectiveness_irofru": 1, "delay_time_irofru": 1},
            "step": {"inflow_irofrulv3": 1, "outflow_irofrulv3": 1},
        }
    },
)
def increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv3():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv3()


_integ_increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv3 = Integ(
    lambda: inflow_irofrulv3() - outflow_irofrulv3(),
    lambda: effectiveness_irofru() * delay_time_irofru(),
    "_integ_increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv3",
)


@component.add(
    name="Indicated Oil Price",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_cost": 1, "oil_desired_gross_margin": 1},
)
def indicated_oil_price():
    """
    Indicated oil price accounting for exploration and production cost and gross margin.
    """
    return oil_cost() * (1 + oil_desired_gross_margin())


@component.add(
    name="Inflow IROFDULV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effectiveness_irofdu": 1},
)
def inflow_irofdulv1():
    return effectiveness_irofdu()


@component.add(
    name="Inflow IROFDULV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_irofdulv1": 1},
)
def inflow_irofdulv2():
    return outflow_irofdulv1()


@component.add(
    name="Inflow IROFDULV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_irofdulv2": 1},
)
def inflow_irofdulv3():
    return outflow_irofdulv2()


@component.add(
    name="Inflow IROFRULV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effectiveness_irofru": 1},
)
def inflow_irofrulv1():
    return effectiveness_irofru()


@component.add(
    name="Inflow IROFRULV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_irofrulv1": 1},
)
def inflow_irofrulv2():
    return outflow_irofrulv1()


@component.add(
    name="Inflow IROFRULV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_irofrulv2": 1},
)
def inflow_irofrulv3():
    return outflow_irofrulv2()


@component.add(
    name="INIT Average Oil Production",
    units="Mtoe/Year",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_average_oil_production():
    return 6.537


@component.add(
    name="INIT COPN",
    units="Mtoe",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_copn():
    """
    Cumulative Oil Resources for 2016
    """
    return 0


@component.add(
    name="INIT EIOE", limits=(0.0, np.nan), comp_type="Constant", comp_subtype="Normal"
)
def init_eioe():
    """
    Effective Investment in Oil Exploration
    """
    return 1250680000.0


@component.add(
    name="INIT EIOP", limits=(0.0, np.nan), comp_type="Constant", comp_subtype="Normal"
)
def init_eiop():
    """
    Effective Investment in Oil Production
    """
    return 125068000.0


@component.add(
    name="INIT OPI", limits=(0.0, np.nan), comp_type="Constant", comp_subtype="Normal"
)
def init_opi():
    """
    Oil Productivity of Investment
    """
    return 0.01


@component.add(
    name="INIT RODU",
    units="Dmnl",
    limits=(0.0, 1.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_rodu():
    """
    Initial Ratio of Oil Fraction Discoverable to Undiscoverable.
    """
    return 0.2


@component.add(
    name="INIT RORU",
    units="Dmnl",
    limits=(0.0, 1.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_roru():
    """
    Initial Ratio of Oil Fraction Recoverable to Unrecoverable.
    """
    return 0.2


@component.add(
    name="INIT UORN",
    units="Mtoe",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_uorn():
    """
    Initial amount of Undiscovered Oil Resources.
    """
    return 500000


@component.add(
    name="Investment in Fossil Fuel Exploration and Production Delay Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def investment_in_fossil_fuel_exploration_and_production_delay_variation():
    return 5


@component.add(
    name="Investment in Oil Discovery Technology",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_oil_technology": 1,
        "fraction_invested_in_oil_discovery_technology": 1,
    },
)
def investment_in_oil_discovery_technology():
    """
    Total investments in oil exploration technology.
    """
    return (
        investment_in_oil_technology() * fraction_invested_in_oil_discovery_technology()
    )


@component.add(
    name="Investment in Oil Exploration",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_investment_in_oil_exploration": 1},
)
def investment_in_oil_exploration():
    """
    Amount of resources dedicated to oil exploration.
    """
    return desired_investment_in_oil_exploration()


@component.add(
    name="Investment in Oil Exploration and Production Delay Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def investment_in_oil_exploration_and_production_delay_variation():
    return 5


@component.add(
    name="Investment in Oil Exploration Delay",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"io_var_s": 1, "_smooth_investment_in_oil_exploration_delay": 1},
    other_deps={
        "_smooth_investment_in_oil_exploration_delay": {
            "initial": {
                "investment_in_oil_exploration_and_production_delay_variation": 1,
                "io_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "investment_in_oil_exploration_and_production_delay_variation": 1,
                "io_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def investment_in_oil_exploration_delay():
    """
    Time delay to make investments in oil exploration effective.
    """
    return io_var_s() + _smooth_investment_in_oil_exploration_delay()


_smooth_investment_in_oil_exploration_delay = Smooth(
    lambda: step(
        __data["time"],
        investment_in_oil_exploration_and_production_delay_variation() - io_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        investment_in_oil_exploration_and_production_delay_variation() - io_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_investment_in_oil_exploration_delay",
)


@component.add(
    name="Investment in Oil Production",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_investment_in_oil_production": 1},
)
def investment_in_oil_production():
    """
    Amount of resources dedicated to oil production.
    """
    return desired_investment_in_oil_production()


@component.add(
    name="Investment in Oil Production Delay",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"io_var_s": 1, "_smooth_investment_in_oil_production_delay": 1},
    other_deps={
        "_smooth_investment_in_oil_production_delay": {
            "initial": {
                "investment_in_oil_exploration_and_production_delay_variation": 1,
                "io_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "investment_in_oil_exploration_and_production_delay_variation": 1,
                "io_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def investment_in_oil_production_delay():
    """
    Time delay to make investments in oil production effective.
    """
    return io_var_s() + _smooth_investment_in_oil_production_delay()


_smooth_investment_in_oil_production_delay = Smooth(
    lambda: step(
        __data["time"],
        investment_in_oil_exploration_and_production_delay_variation() - io_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        investment_in_oil_exploration_and_production_delay_variation() - io_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_investment_in_oil_production_delay",
)


@component.add(
    name="Investment in Oil Recovery Technology",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_oil_technology": 1,
        "fraction_invested_in_oil_discovery_technology": 1,
    },
)
def investment_in_oil_recovery_technology():
    """
    Total investments in oil production technology.
    """
    return investment_in_oil_technology() * (
        1 - fraction_invested_in_oil_discovery_technology()
    )


@component.add(
    name="Investment in Oil Technology",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fraction_of_oil_revenues_invested_in_technology": 1, "oil_revenue": 1},
)
def investment_in_oil_technology():
    """
    Investments in development of exploration and production technology.
    """
    return fraction_of_oil_revenues_invested_in_technology() * oil_revenue()


@component.add(name="IO S", units="Year", comp_type="Constant", comp_subtype="Normal")
def io_s():
    return 5


@component.add(
    name="IO Var S",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_io_var_s": 1},
    other_deps={
        "_smooth_io_var_s": {
            "initial": {"io_s": 1, "time": 1},
            "step": {"io_s": 1, "time": 1},
        }
    },
)
def io_var_s():
    return 5 + _smooth_io_var_s()


_smooth_io_var_s = Smooth(
    lambda: step(__data["time"], io_s() - 5, 2020),
    lambda: 1,
    lambda: step(__data["time"], io_s() - 5, 2020),
    lambda: 1,
    "_smooth_io_var_s",
)


@component.add(
    name="Max Unit Cost of Oil Exploration",
    units="$/Mtoe",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"mfc_var_s": 1, "_smooth_max_unit_cost_of_oil_exploration": 1},
    other_deps={
        "_smooth_max_unit_cost_of_oil_exploration": {
            "initial": {
                "max_unit_cost_of_fossil_fuel_exploration_variation": 1,
                "mfc_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "max_unit_cost_of_fossil_fuel_exploration_variation": 1,
                "mfc_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_production_variation_time": 1,
            },
        }
    },
)
def max_unit_cost_of_oil_exploration():
    """
    Upper level limit for unit cost of oil exploration.
    """
    return mfc_var_s() + _smooth_max_unit_cost_of_oil_exploration()


_smooth_max_unit_cost_of_oil_exploration = Smooth(
    lambda: step(
        __data["time"],
        max_unit_cost_of_fossil_fuel_exploration_variation() - mfc_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_production_variation_time(),
    lambda: step(
        __data["time"],
        max_unit_cost_of_fossil_fuel_exploration_variation() - mfc_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_max_unit_cost_of_oil_exploration",
)


@component.add(name="MAXOFD", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def maxofd():
    """
    Maximal possible percentage of oil resources to be discovered.
    """
    return 1


@component.add(name="MAXOFR", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def maxofr():
    """
    Maximal possible percentage of oil resources to be recovered.
    """
    return 1


@component.add(name="MINOFD", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def minofd():
    """
    Initial and minimal possible percentage of oil resources to be discovered.
    """
    return 0.02


@component.add(name="MINOFR", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def minofr():
    """
    Initial and minimal possible percentage of oil resources to be recovered.
    """
    return 0.1


@component.add(
    name="Mtoe per Barrel",
    units="Mtoe/Barrel",
    comp_type="Constant",
    comp_subtype="Normal",
)
def mtoe_per_barrel():
    """
    Coefficient to convert million tons of oil equivalent unit (Mtoe) into barrels.
    """
    return 1.364e-07


@component.add(
    name="Normal Oil Production Ratio",
    units="Year",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_oil_production_ratio():
    """
    Safety stock coverage as a number of years of the total oil demand the oil sector would like to maintain in identified oil resources. It secures the market against possibility of unforeseen variations in demand. It is also a stimulus for oil exploration.
    """
    return 2


@component.add(name="ODR S", units="Year", comp_type="Constant", comp_subtype="Normal")
def odr_s():
    return 6


@component.add(
    name="ODR Var S",
    units="{6}",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_odr_var_s": 1},
    other_deps={
        "_smooth_odr_var_s": {
            "initial": {"odr_s": 1, "time": 1},
            "step": {"odr_s": 1, "time": 1},
        }
    },
)
def odr_var_s():
    return 6 + _smooth_odr_var_s()


_smooth_odr_var_s = Smooth(
    lambda: step(__data["time"], odr_s() - 6, 2020),
    lambda: 1,
    lambda: step(__data["time"], odr_s() - 6, 2020),
    lambda: 1,
    "_smooth_odr_var_s",
)


@component.add(
    name="Oil Cost",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"unit_cost_of_oil_exploration": 1, "unit_cost_of_oil_production": 1},
)
def oil_cost():
    """
    Cont of unit oil resources as a sum of unit exploration and production costs.
    """
    return unit_cost_of_oil_exploration() + unit_cost_of_oil_production()


@component.add(
    name="Oil Demand to Supply Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_oil_demand": 1, "potential_oil_production": 1},
)
def oil_demand_to_supply_ratio():
    """
    Oil Demand to Supply Ratio.
    """
    return total_oil_demand() / potential_oil_production()


@component.add(
    name="Oil Desired Gross Margin",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def oil_desired_gross_margin():
    """
    Desired Gross Margin per unit oil resources.
    """
    return 0.2


@component.add(
    name="Oil Discovery and Recovery Technology Development Time Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def oil_discovery_and_recovery_technology_development_time_variation():
    return 6


@component.add(
    name="Oil Discovery Technology Development Time",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"odr_var_s": 1, "_smooth_oil_discovery_technology_development_time": 1},
    other_deps={
        "_smooth_oil_discovery_technology_development_time": {
            "initial": {
                "oil_discovery_and_recovery_technology_development_time_variation": 1,
                "odr_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "oil_discovery_and_recovery_technology_development_time_variation": 1,
                "odr_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def oil_discovery_technology_development_time():
    """
    Average time required to turn investments into concrete oil discovery developments.
    """
    return odr_var_s() + _smooth_oil_discovery_technology_development_time()


_smooth_oil_discovery_technology_development_time = Smooth(
    lambda: step(
        __data["time"],
        oil_discovery_and_recovery_technology_development_time_variation()
        - odr_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        oil_discovery_and_recovery_technology_development_time_variation()
        - odr_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_oil_discovery_technology_development_time",
)


@component.add(
    name="Oil Exploration",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_exploration_rate": 1},
)
def oil_exploration():
    """
    Oil resources discovery rate.
    """
    return float(np.maximum(0, oil_exploration_rate()))


@component.add(
    name="Oil Exploration Rate",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_oil_exploration_rate": 1, "potential_oil_exploration": 1},
)
def oil_exploration_rate():
    """
    Oil Exploration Rate accounting for potential and desired oil exploration rates.
    """
    return float(
        np.minimum(desired_oil_exploration_rate(), potential_oil_exploration())
    )


@component.add(
    name="Oil Fraction Discoverable",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "minofd": 2,
        "maxofd": 1,
        "ratio_of_oil_fraction_discoverable_to_undiscoverable": 2,
    },
)
def oil_fraction_discoverable():
    """
    Percentage of oil resources that can be still explored due to current state of discovery technology.
    """
    return minofd() + (maxofd() - minofd()) * (
        ratio_of_oil_fraction_discoverable_to_undiscoverable()
        / (ratio_of_oil_fraction_discoverable_to_undiscoverable() + 1)
    )


@component.add(
    name="Oil Fraction Recoverable",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "minofr": 2,
        "maxofr": 1,
        "ratio_of_oil_fraction_recoverable_to_unrecoverable": 2,
    },
)
def oil_fraction_recoverable():
    """
    Percentage of oil resources that can be produced due to current state of recovery technology.
    """
    return minofr() + (maxofr() - minofr()) * (
        ratio_of_oil_fraction_recoverable_to_unrecoverable()
        / (ratio_of_oil_fraction_recoverable_to_unrecoverable() + 1)
    )


@component.add(
    name="Oil Gross Margin",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_price": 1, "oil_cost": 2},
)
def oil_gross_margin():
    """
    Actual oil gross margin.
    """
    return (oil_price() - oil_cost()) / oil_cost()


@component.add(
    name="Oil Price",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "indicated_oil_price": 1,
        "effect_of_oil_demand_and_supply_on_price": 1,
    },
)
def oil_price():
    """
    Actual oil price accounting for indicated oil price and effect of demand and supply.
    """
    return indicated_oil_price() * effect_of_oil_demand_and_supply_on_price()


@component.add(
    name="Oil Price per Barrel",
    units="$/Barrel",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_price": 1, "mtoe_per_barrel": 1},
)
def oil_price_per_barrel():
    """
    Actual Oil Price per Barrel.
    """
    return oil_price() * mtoe_per_barrel()


@component.add(
    name="Oil Production",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_production_rate": 1},
)
def oil_production():
    """
    Total oil energy production per year. Source of historical data: International Energy Agency – Key World Energy Statistics 2007; BP Statistical Review of World Energy June 2008
    """
    return oil_production_rate()


@component.add(
    name="Oil Production Coverage",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"identified_oil_resources": 1, "average_oil_production": 1},
)
def oil_production_coverage():
    """
    Ratio indicating oil coverage in years for discovered resources and at the current average oil production.
    """
    return identified_oil_resources() / average_oil_production()


@component.add(
    name="Oil Production Indicator",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_production": 1, "mtoe_into_ej": 1},
)
def oil_production_indicator():
    return oil_production() * mtoe_into_ej()


@component.add(
    name="Oil Production Rate",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_oil_demand": 1, "potential_oil_production": 1},
)
def oil_production_rate():
    """
    Total oil energy production per year due to available resources, developments in production technology and oil energy demand.
    """
    return float(np.minimum(total_oil_demand(), potential_oil_production()))


@component.add(
    name="Oil Productivity of Investment",
    units="toe/$",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_oil_productivity_of_investment": 1},
    other_deps={
        "_integ_oil_productivity_of_investment": {
            "initial": {"init_opi": 1},
            "step": {"change_in_oil_productivity_of_investment": 1},
        }
    },
)
def oil_productivity_of_investment():
    """
    Factor indicating productivity of investments in oil production.
    """
    return _integ_oil_productivity_of_investment()


_integ_oil_productivity_of_investment = Integ(
    lambda: change_in_oil_productivity_of_investment(),
    lambda: init_opi(),
    "_integ_oil_productivity_of_investment",
)


@component.add(
    name="Oil Recovery Technology Development Time",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"odr_var_s": 1, "_smooth_oil_recovery_technology_development_time": 1},
    other_deps={
        "_smooth_oil_recovery_technology_development_time": {
            "initial": {
                "oil_discovery_and_recovery_technology_development_time_variation": 1,
                "odr_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "oil_discovery_and_recovery_technology_development_time_variation": 1,
                "odr_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def oil_recovery_technology_development_time():
    """
    Average time required to turn investments into concrete oil recovery developments.
    """
    return odr_var_s() + _smooth_oil_recovery_technology_development_time()


_smooth_oil_recovery_technology_development_time = Smooth(
    lambda: step(
        __data["time"],
        oil_discovery_and_recovery_technology_development_time_variation()
        - odr_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        oil_discovery_and_recovery_technology_development_time_variation()
        - odr_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_oil_recovery_technology_development_time",
)


@component.add(
    name="Oil Revenue",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_price": 1, "average_oil_production": 1},
)
def oil_revenue():
    """
    Total revenue in oil market.
    """
    return oil_price() * average_oil_production()


@component.add(
    name="Oil Shortage",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_oil_demand": 1, "oil_production": 1},
)
def oil_shortage():
    """
    Difference between demand and the oil production rate.
    """
    return total_oil_demand() - oil_production()


@component.add(
    name="Outflow IROFDULV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv1": 1,
        "delay_time_irofdu": 1,
    },
)
def outflow_irofdulv1():
    return (
        increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv1()
        / delay_time_irofdu()
    )


@component.add(
    name="Outflow IROFDULV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv2": 1,
        "delay_time_irofdu": 1,
    },
)
def outflow_irofdulv2():
    return (
        increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv2()
        / delay_time_irofdu()
    )


@component.add(
    name="Outflow IROFDULV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv3": 1,
        "delay_time_irofdu": 1,
    },
)
def outflow_irofdulv3():
    return (
        increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable_lv3()
        / delay_time_irofdu()
    )


@component.add(
    name="Outflow IROFRULV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv1": 1,
        "delay_time_irofru": 1,
    },
)
def outflow_irofrulv1():
    return (
        increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv1()
        / delay_time_irofru()
    )


@component.add(
    name="Outflow IROFRULV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv2": 1,
        "delay_time_irofru": 1,
    },
)
def outflow_irofrulv2():
    return (
        increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv2()
        / delay_time_irofru()
    )


@component.add(
    name="Outflow IROFRULV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv3": 1,
        "delay_time_irofru": 1,
    },
)
def outflow_irofrulv3():
    return (
        increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable_lv3()
        / delay_time_irofru()
    )


@component.add(
    name="Potential Oil Exploration",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effective_investment_in_oil_exploration": 1,
        "productivity_of_investment_in_oil_exploration": 1,
        "toe_per_mtoe": 1,
    },
)
def potential_oil_exploration():
    """
    Potential Oil exploration due to available investments in oil resources discovery.
    """
    return (
        effective_investment_in_oil_exploration()
        * productivity_of_investment_in_oil_exploration()
        / toe_per_mtoe()
    )


@component.add(
    name="Potential Oil Production",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_oil_production_from_investment": 1,
        "potential_oil_production_from_resources": 1,
    },
)
def potential_oil_production():
    """
    Potential Oil Production due to available investments in oil resources recovery and recovery technology.
    """
    return float(
        np.minimum(
            potential_oil_production_from_investment(),
            potential_oil_production_from_resources(),
        )
    )


@component.add(
    name="Potential Oil Production from Investment",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "productivity_of_investment_in_oil_production": 1,
        "effective_investment_in_oil_production": 1,
        "toe_per_mtoe": 1,
    },
)
def potential_oil_production_from_investment():
    """
    Potential Oil Production due to available investments in oil resources recovery.
    """
    return (
        productivity_of_investment_in_oil_production()
        * effective_investment_in_oil_production()
        / toe_per_mtoe()
    )


@component.add(
    name="Potential Oil Production from Resources",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_oil_recoverable_resource_remaining": 1,
        "normal_oil_production_ratio": 1,
    },
)
def potential_oil_production_from_resources():
    """
    Desired Oil Production rate due to Total Oil Recoverable Resource Remaining adjusted by oil production safety coverage.
    """
    return total_oil_recoverable_resource_remaining() / normal_oil_production_ratio()


@component.add(
    name="Productivity of Investment in Oil Exploration",
    units="toe/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "relative_productivity_of_investment_in_oil_exploration": 1,
        "effect_of_technology_on_oil_discoveries": 1,
    },
)
def productivity_of_investment_in_oil_exploration():
    """
    Parameter indicating the amount of oil resources possible to be explored per unit investment spent.
    """
    return float(
        np.maximum(
            0,
            relative_productivity_of_investment_in_oil_exploration()
            * effect_of_technology_on_oil_discoveries(),
        )
    )


@component.add(
    name="Productivity of Investment in Oil Production",
    units="toe/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "relative_productivity_of_investment_in_oil_production_compared_to_exploration": 1,
        "oil_productivity_of_investment": 1,
    },
)
def productivity_of_investment_in_oil_production():
    """
    Parameter indicating the amount of oil resources possible to be recovered per unit investment spent.
    """
    return (
        relative_productivity_of_investment_in_oil_production_compared_to_exploration()
        * oil_productivity_of_investment()
    )


@component.add(
    name="Rate of New Discovery Oil",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mtoe_per_barrel": 1, "annual_change_in_oil_reserves": 1},
)
def rate_of_new_discovery_oil():
    return mtoe_per_barrel() * annual_change_in_oil_reserves()


@component.add(
    name="Ratio of Oil Fraction Discoverable to Undiscoverable",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ratio_of_oil_fraction_discoverable_to_undiscoverable": 1},
    other_deps={
        "_integ_ratio_of_oil_fraction_discoverable_to_undiscoverable": {
            "initial": {"init_rodu": 1},
            "step": {
                "increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable": 1
            },
        }
    },
)
def ratio_of_oil_fraction_discoverable_to_undiscoverable():
    """
    Ratio of Oil Fraction Discoverable to Undiscoverable increased due to investments in discovery technology and their productivity.
    """
    return _integ_ratio_of_oil_fraction_discoverable_to_undiscoverable()


_integ_ratio_of_oil_fraction_discoverable_to_undiscoverable = Integ(
    lambda: increase_in_ratio_of_oil_fraction_discoverable_to_undiscoverable(),
    lambda: init_rodu(),
    "_integ_ratio_of_oil_fraction_discoverable_to_undiscoverable",
)


@component.add(
    name="Ratio of Oil Fraction Recoverable to Unrecoverable",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ratio_of_oil_fraction_recoverable_to_unrecoverable": 1},
    other_deps={
        "_integ_ratio_of_oil_fraction_recoverable_to_unrecoverable": {
            "initial": {"init_roru": 1},
            "step": {
                "increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable": 1
            },
        }
    },
)
def ratio_of_oil_fraction_recoverable_to_unrecoverable():
    """
    Ratio of Oil Fraction Recoverable to Unrecoverable increased due to investments in recovery technology and their productivity.
    """
    return _integ_ratio_of_oil_fraction_recoverable_to_unrecoverable()


_integ_ratio_of_oil_fraction_recoverable_to_unrecoverable = Integ(
    lambda: increase_in_ratio_of_oil_fraction_recoverable_to_unrecoverable(),
    lambda: init_roru(),
    "_integ_ratio_of_oil_fraction_recoverable_to_unrecoverable",
)


@component.add(
    name="Relative Productivity of Investment in Fossil Fuel Production Compared to Exploration Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def relative_productivity_of_investment_in_fossil_fuel_production_compared_to_exploration_variation():
    return 10


@component.add(
    name="Relative Productivity of Investment in Oil Exploration",
    units="toe/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "relative_productivity_of_investment_in_oil_exploration_variation": 1,
        "time": 1,
    },
)
def relative_productivity_of_investment_in_oil_exploration():
    """
    Relative Productivity of Investment in Oil Exploration without taking into account remaining undiscovered oil resources and advances in exploration technologies.
    """
    return 0.05 + step(
        __data["time"],
        relative_productivity_of_investment_in_oil_exploration_variation() - 0.05,
        2020,
    )


@component.add(
    name="Relative Productivity of Investment in Oil Exploration Variation",
    units="toe/$",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def relative_productivity_of_investment_in_oil_exploration_variation():
    """
    Relative Productivity of Investment in Oil Exploration without taking into account remaining undiscovered oil resources and advances in exploration technologies.
    """
    return 0.05


@component.add(
    name="Relative Productivity of Investment in Oil Production Compared to Exploration",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "rpope_var_s": 1,
        "_smooth_relative_productivity_of_investment_in_oil_production_compared_to_exploration": 1,
    },
    other_deps={
        "_smooth_relative_productivity_of_investment_in_oil_production_compared_to_exploration": {
            "initial": {
                "relative_productivity_of_investment_in_oil_production_compared_to_exploration_variation": 1,
                "rpope_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "relative_productivity_of_investment_in_oil_production_compared_to_exploration_variation": 1,
                "rpope_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def relative_productivity_of_investment_in_oil_production_compared_to_exploration():
    """
    Relative Productivity of Investment in Oil Production as a multiplier of Productivity of Investment in Oil Exploration.
    """
    return (
        rpope_var_s()
        + _smooth_relative_productivity_of_investment_in_oil_production_compared_to_exploration()
    )


_smooth_relative_productivity_of_investment_in_oil_production_compared_to_exploration = Smooth(
    lambda: step(
        __data["time"],
        relative_productivity_of_investment_in_oil_production_compared_to_exploration_variation()
        - rpope_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        relative_productivity_of_investment_in_oil_production_compared_to_exploration_variation()
        - rpope_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_relative_productivity_of_investment_in_oil_production_compared_to_exploration",
)


@component.add(
    name="Relative Productivity of Investment in Oil Production Compared to Exploration Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def relative_productivity_of_investment_in_oil_production_compared_to_exploration_variation():
    return 10


@component.add(
    name="Required Identified Oil Resources",
    units="Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "identified_oil_resources": 1,
        "total_oil_recoverable_resource_remaining": 1,
        "normal_oil_production_ratio": 1,
        "total_oil_demand": 1,
    },
)
def required_identified_oil_resources():
    """
    The desired Identified Oil Resources level sought by the oil sector.
    """
    return (identified_oil_resources() / total_oil_recoverable_resource_remaining()) * (
        normal_oil_production_ratio() * total_oil_demand()
    )


@component.add(
    name="RPOPE S", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def rpope_s():
    return 10


@component.add(
    name="RPOPE Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_rpope_var_s": 1},
    other_deps={
        "_smooth_rpope_var_s": {
            "initial": {"rpope_s": 1, "time": 1},
            "step": {"rpope_s": 1, "time": 1},
        }
    },
)
def rpope_var_s():
    return 10 + _smooth_rpope_var_s()


_smooth_rpope_var_s = Smooth(
    lambda: step(__data["time"], rpope_s() - 10, 2020),
    lambda: 1,
    lambda: step(__data["time"], rpope_s() - 10, 2020),
    lambda: 1,
    "_smooth_rpope_var_s",
)


@component.add(
    name="RPPE S",
    units="Dmnl",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def rppe_s():
    return 10


@component.add(
    name="RPPE Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_rppe_var_s": 1},
    other_deps={
        "_smooth_rppe_var_s": {
            "initial": {"rppe_s": 1, "time": 1},
            "step": {"rppe_s": 1, "time": 1},
        }
    },
)
def rppe_var_s():
    return 10 + _smooth_rppe_var_s()


_smooth_rppe_var_s = Smooth(
    lambda: step(__data["time"], rppe_s() - 10, 2020),
    lambda: 1,
    lambda: step(__data["time"], rppe_s() - 10, 2020),
    lambda: 1,
    "_smooth_rppe_var_s",
)


@component.add(
    name="Sensitivity of Fossil Fuel Price to Supply and Demand Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sensitivity_of_fossil_fuel_price_to_supply_and_demand_variation():
    return 2


@component.add(
    name="Sensitivity of Oil Price to Supply and Demand",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "so_var_s": 1,
        "_smooth_sensitivity_of_oil_price_to_supply_and_demand": 1,
    },
    other_deps={
        "_smooth_sensitivity_of_oil_price_to_supply_and_demand": {
            "initial": {
                "sensitivity_of_oil_price_to_supply_and_demand_variation": 1,
                "so_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "sensitivity_of_oil_price_to_supply_and_demand_variation": 1,
                "so_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_demand_variation_time": 1,
            },
        }
    },
)
def sensitivity_of_oil_price_to_supply_and_demand():
    """
    Sensitivity of Oil Price to Supply and Demand ratio.
    """
    return so_var_s() + _smooth_sensitivity_of_oil_price_to_supply_and_demand()


_smooth_sensitivity_of_oil_price_to_supply_and_demand = Smooth(
    lambda: step(
        __data["time"],
        sensitivity_of_oil_price_to_supply_and_demand_variation() - so_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_demand_variation_time(),
    lambda: step(
        __data["time"],
        sensitivity_of_oil_price_to_supply_and_demand_variation() - so_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_sensitivity_of_oil_price_to_supply_and_demand",
)


@component.add(
    name="Sensitivity of Oil Price to Supply and Demand Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sensitivity_of_oil_price_to_supply_and_demand_variation():
    return 1.4


@component.add(
    name="SF S",
    units="Dmnl",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def sf_s():
    return 1.4


@component.add(
    name="SF Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_sf_var_s": 1},
    other_deps={
        "_smooth_sf_var_s": {
            "initial": {"sf_s": 1, "time": 1},
            "step": {"sf_s": 1, "time": 1},
        }
    },
)
def sf_var_s():
    return 2 + _smooth_sf_var_s()


_smooth_sf_var_s = Smooth(
    lambda: step(__data["time"], sf_s() - 2, 2020),
    lambda: 1,
    lambda: step(__data["time"], sf_s() - 2, 2020),
    lambda: 1,
    "_smooth_sf_var_s",
)


@component.add(
    name="Share of Investment in Revenue Oil",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_investment_in_oil": 1, "oil_revenue": 1},
)
def share_of_investment_in_revenue_oil():
    return total_investment_in_oil() / oil_revenue()


@component.add(
    name="Share of Upstream Investment in Total Investment Oil",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def share_of_upstream_investment_in_total_investment_oil():
    """
    Data from World Energy Investment 2023
    """
    return 0.65


@component.add(
    name="SO Init", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def so_init():
    """
    A CONSTANT
    """
    return 0.095


@component.add(name="SO S", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def so_s():
    return 1.4


@component.add(
    name="SO Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_so_var_s": 1},
    other_deps={
        "_smooth_so_var_s": {
            "initial": {"so_s": 1, "time": 1},
            "step": {"so_s": 1, "time": 1},
        }
    },
)
def so_var_s():
    return 1.4 + _smooth_so_var_s()


_smooth_so_var_s = Smooth(
    lambda: step(__data["time"], so_s() - 1.4, 2020),
    lambda: 1,
    lambda: step(__data["time"], so_s() - 1.4, 2020),
    lambda: 1,
    "_smooth_so_var_s",
)


@component.add(
    name="Table for FIODT",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_table_for_fiodt"},
)
def table_for_fiodt(x, final_subs=None):
    """
    Table determining order by which technology investments are dedicated to exploration and production technologies. For small Oil Fraction Discoverable, in order to make sufficient resources available to be produced, more investments are directed to exploration technologies. Once the Oil Fraction Discoverable increases the investments are redirected to production technologies.
    """
    return _hardcodedlookup_table_for_fiodt(x, final_subs)


_hardcodedlookup_table_for_fiodt = HardcodedLookups(
    [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
    [0.8, 0.8, 0.7, 0.5, 0.2, 0.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_for_fiodt",
)


@component.add(
    name="Time to Average Oil Production",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_average_oil_production():
    """
    Time to average total oil production per year.
    """
    return 1


@component.add(
    name="toe per Mtoe", units="toe/Mtoe", comp_type="Constant", comp_subtype="Normal"
)
def toe_per_mtoe():
    """
    Conversion from Mtoe to toe.
    """
    return 1000000.0


@component.add(
    name="Total Investment in Oil",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_oil_exploration": 1,
        "investment_in_oil_production": 1,
        "investment_in_oil_technology": 1,
        "share_of_upstream_investment_in_total_investment_oil": 1,
    },
)
def total_investment_in_oil():
    return (
        investment_in_oil_exploration()
        + investment_in_oil_production()
        + investment_in_oil_technology()
    ) / share_of_upstream_investment_in_total_investment_oil()


@component.add(
    name="Total Oil Demand",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_demand": 1, "market_share_oil": 1},
)
def total_oil_demand():
    """
    Total demand for oil resources.
    """
    return energy_demand() * market_share_oil()


@component.add(
    name="Total Oil Discoverable Resources",
    units="Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_oil_resources": 1,
        "oil_fraction_discoverable": 1,
        "cumulative_additions_to_oil_production": 1,
    },
)
def total_oil_discoverable_resources():
    """
    Total Oil Discoverable Resources as a percentage of Total Oil Resources. It excludes identified and already produced resources. The percentage is determined by exploration technology developments.
    """
    return (
        total_oil_resources() * oil_fraction_discoverable()
        - cumulative_additions_to_oil_production()
    )


@component.add(
    name="Total Oil Recoverable Resource Remaining",
    units="Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cumulative_additions_to_oil_production": 1,
        "oil_fraction_recoverable": 1,
        "cumulative_oil_production": 1,
    },
)
def total_oil_recoverable_resource_remaining():
    """
    Total Oil Recoverable Resources Remaining as a percentage of Cumulative Additions to Oil Production. It already produced resources. The percentage is determined by production technology developments.
    """
    return (
        cumulative_additions_to_oil_production() * oil_fraction_recoverable()
        - cumulative_oil_production()
    )


@component.add(
    name="Total Oil Resources",
    units="Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "undiscovered_oil_resources": 1,
        "cumulative_additions_to_oil_production": 1,
    },
)
def total_oil_resources():
    """
    Total oil resources including Undiscovered Oil Resources, Identified Oil Resources and resources already produced i.e. Cumulative Oil Production.
    """
    return undiscovered_oil_resources() + cumulative_additions_to_oil_production()


@component.add(
    name="Undiscovered Oil Resources",
    units="Mtoe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_undiscovered_oil_resources": 1},
    other_deps={
        "_integ_undiscovered_oil_resources": {
            "initial": {"init_uorn": 1},
            "step": {"rate_of_new_discovery_oil": 1, "oil_exploration": 1},
        }
    },
)
def undiscovered_oil_resources():
    """
    Existing Oil Resources but not discovered yet.
    """
    return _integ_undiscovered_oil_resources()


_integ_undiscovered_oil_resources = Integ(
    lambda: rate_of_new_discovery_oil() - oil_exploration(),
    lambda: init_uorn(),
    "_integ_undiscovered_oil_resources",
)


@component.add(
    name="Unit Cost of Oil Exploration",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_unit_cost_of_oil_exploration": 1,
        "productivity_of_investment_in_oil_exploration": 2,
        "toe_per_mtoe": 1,
    },
)
def unit_cost_of_oil_exploration():
    """
    Unit cost of oil exploration. Depends on remaining undiscovered oil resources and advances in exploration technologies.
    """
    return float(
        np.minimum(
            max_unit_cost_of_oil_exploration(),
            if_then_else(
                productivity_of_investment_in_oil_exploration() == 0,
                lambda: 0,
                lambda: 1
                / productivity_of_investment_in_oil_exploration()
                * toe_per_mtoe(),
            ),
        )
    )


@component.add(
    name="Unit Cost of Oil Production",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "productivity_of_investment_in_oil_production": 1,
        "toe_per_mtoe": 1,
        "carbon_price": 1,
        "climate_policy_scenario": 1,
        "co2_intensity_of_fuels": 1,
    },
)
def unit_cost_of_oil_production():
    """
    Unit cost of oil production.
    """
    return (
        1 / productivity_of_investment_in_oil_production() * toe_per_mtoe()
        + climate_policy_scenario()
        * float(co2_intensity_of_fuels().loc["Oil"])
        * carbon_price()
    )


@component.add(
    name="URO S",
    units="Barrel/Year",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def uro_s():
    return 5000000000.0


@component.add(
    name="URO Var S",
    units="Barrel/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_uro_var_s": 1},
    other_deps={
        "_smooth_uro_var_s": {
            "initial": {"uro_s": 1, "time": 1},
            "step": {"uro_s": 1, "time": 1},
        }
    },
)
def uro_var_s():
    return 5000000000.0 + _smooth_uro_var_s()


_smooth_uro_var_s = Smooth(
    lambda: step(__data["time"], uro_s() - 5000000000.0, 2020),
    lambda: 1,
    lambda: step(__data["time"], uro_s() - 5000000000.0, 2020),
    lambda: 1,
    "_smooth_uro_var_s",
)
