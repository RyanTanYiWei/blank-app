"""
Module energy_gas
Translated using PySD version 3.14.3
"""

@component.add(
    name="Adjustment for Identified Gas Resource",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_identified_gas_resources": 1,
        "identified_gas_resources": 1,
        "identified_gas_resources_adjustment_time": 1,
    },
)
def adjustment_for_identified_gas_resource():
    """
    Adjustment of Identified Gas Resource to the desired level over a specified adjustment time.
    """
    return (
        required_identified_gas_resources() - identified_gas_resources()
    ) / identified_gas_resources_adjustment_time()


@component.add(
    name="Annual Growth in Gas Reserves",
    units="Billion Cubic Meters/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"urg_var_s": 1, "_smooth_annual_growth_in_gas_reserves": 1, "time": 1},
    other_deps={
        "_smooth_annual_growth_in_gas_reserves": {
            "initial": {
                "annual_growth_in_gas_reserves_variation": 1,
                "urg_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "annual_growth_in_gas_reserves_variation": 1,
                "urg_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_production_variation_time": 1,
            },
        }
    },
)
def annual_growth_in_gas_reserves():
    """
    We asssumed the gas boost equal to the average annual growth in the total proved gas reserves is 2.2 Trillion cubic meters in the last 20 years (1999-2019).
    """
    return step(
        __data["time"], urg_var_s() + _smooth_annual_growth_in_gas_reserves(), 2010
    )


_smooth_annual_growth_in_gas_reserves = Smooth(
    lambda: step(
        __data["time"],
        annual_growth_in_gas_reserves_variation() - urg_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_production_variation_time(),
    lambda: step(
        __data["time"],
        annual_growth_in_gas_reserves_variation() - urg_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_annual_growth_in_gas_reserves",
)


@component.add(
    name="Annual Growth in Gas Reserves Variation",
    units="Billion Cubic Meters/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def annual_growth_in_gas_reserves_variation():
    return 5000


@component.add(
    name="Average Gas Production",
    units="Mtoe/Year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_average_gas_production": 1},
    other_deps={
        "_integ_average_gas_production": {
            "initial": {"init_average_gas_production": 1},
            "step": {"change_in_average_gas_production": 1},
        }
    },
)
def average_gas_production():
    """
    Average total gas production per year.
    """
    return _integ_average_gas_production()


_integ_average_gas_production = Integ(
    lambda: change_in_average_gas_production(),
    lambda: init_average_gas_production(),
    "_integ_average_gas_production",
)


@component.add(
    name="Change in Average Gas Production",
    units="Mtoe/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gas_production": 1,
        "average_gas_production": 1,
        "time_to_average_gas_production": 1,
    },
)
def change_in_average_gas_production():
    """
    Change in Average Gas Production.
    """
    return (
        gas_production() - average_gas_production()
    ) / time_to_average_gas_production()


@component.add(
    name="Change in Effective Investment in Gas Exploration",
    units="$/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_gas_exploration": 1,
        "effective_investment_in_gas_exploration": 1,
        "investment_in_gas_exploration_delay": 1,
    },
)
def change_in_effective_investment_in_gas_exploration():
    """
    Change in Effective Investment in Gas Exploration.
    """
    return (
        investment_in_gas_exploration() - effective_investment_in_gas_exploration()
    ) / investment_in_gas_exploration_delay()


@component.add(
    name="Change in Effective Investment in Gas Production",
    units="$/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_gas_production": 1,
        "effective_investment_in_gas_production": 1,
        "investment_in_gas_production_delay": 1,
    },
)
def change_in_effective_investment_in_gas_production():
    """
    Change in Effective Investment in Gas Production.
    """
    return (
        investment_in_gas_production() - effective_investment_in_gas_production()
    ) / investment_in_gas_production_delay()


@component.add(
    name="Change in Gas Productivity of Investment",
    units="toe/(Year*$)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "productivity_of_investment_in_gas_exploration": 1,
        "gas_productivity_of_investment": 1,
        "gas_production_coverage": 1,
    },
)
def change_in_gas_productivity_of_investment():
    """
    Change in Gas Productivity of Investment.
    """
    return (
        productivity_of_investment_in_gas_exploration()
        - gas_productivity_of_investment()
    ) / gas_production_coverage()


@component.add(
    name="Cumulative Additions to Gas Production",
    units="Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"identified_gas_resources": 1, "cumulative_gas_production": 1},
)
def cumulative_additions_to_gas_production():
    """
    Identified and already produced gas resources.
    """
    return identified_gas_resources() + cumulative_gas_production()


@component.add(
    name="Cumulative Gas Production",
    units="Mtoe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_gas_production": 1},
    other_deps={
        "_integ_cumulative_gas_production": {
            "initial": {"init_cgpn": 1},
            "step": {"gas_production": 1},
        }
    },
)
def cumulative_gas_production():
    """
    Cumulative Gas resources that has been produced.
    """
    return _integ_cumulative_gas_production()


_integ_cumulative_gas_production = Integ(
    lambda: gas_production(), lambda: init_cgpn(), "_integ_cumulative_gas_production"
)


@component.add(
    name="Delay Time IRGFDU",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gas_discovery_technology_development_time": 1},
)
def delay_time_irgfdu():
    return gas_discovery_technology_development_time() / 3


@component.add(
    name="Delay Time IRGFRU",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gas_recovery_technology_development_time": 1},
)
def delay_time_irgfru():
    return gas_recovery_technology_development_time() / 3


@component.add(
    name="Desired Gas Exploration Rate",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"adjustment_for_identified_gas_resource": 1, "gas_production": 1},
)
def desired_gas_exploration_rate():
    """
    Desired Gas exploration rate due to Total Gas Demand and Identified Gas Resources safety coverage.
    """
    return float(
        np.maximum(0, adjustment_for_identified_gas_resource() + gas_production())
    )


@component.add(
    name="Desired Gas Gross Margin",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def desired_gas_gross_margin():
    """
    Desired Gross Margin per unit gas resources.
    """
    return 0.2


@component.add(
    name="Desired Investment in Gas Exploration",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_gas_exploration_rate": 1, "unit_cost_of_gas_exploration": 1},
)
def desired_investment_in_gas_exploration():
    """
    Desired amount of resources that need to be invested in order to secure desired gas exploration.
    """
    return desired_gas_exploration_rate() * unit_cost_of_gas_exploration()


@component.add(
    name="Desired Investment in Gas Production",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_gas_production_from_resources": 1,
        "total_gas_demand": 1,
        "productivity_of_investment_in_gas_production": 1,
        "toe_per_mtoe": 1,
    },
)
def desired_investment_in_gas_production():
    """
    Desired Investment in Gas Production due to Total Gas Demand and Productivity of Investment in Gas Production.
    """
    return (
        float(np.minimum(potential_gas_production_from_resources(), total_gas_demand()))
        / productivity_of_investment_in_gas_production()
        * toe_per_mtoe()
    )


@component.add(
    name="Effect of Gas Demand and Supply on Price",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sg_init": 1,
        "sensitivity_of_gas_price_to_supply_and_demand": 1,
        "potential_gas_production": 1,
        "total_gas_demand": 1,
    },
)
def effect_of_gas_demand_and_supply_on_price():
    """
    Effect of Gas Demand and Supply ratio on actual gas price.
    """
    return (
        sg_init()
        * (total_gas_demand() / potential_gas_production())
        ** sensitivity_of_gas_price_to_supply_and_demand()
    )


@component.add(
    name="Effect of Technology on Gas Discoveries",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_gas_discoverable_resources": 1, "init_ugrn": 1},
)
def effect_of_technology_on_gas_discoveries():
    """
    Impact of technology development on gas exploration taking into account remaining undiscovered gas resources (the less remaining undiscovered gas resources the more expensive it is to discover them).
    """
    return total_gas_discoverable_resources() / init_ugrn()


@component.add(
    name="Effective Investment in Gas Exploration",
    units="$/Year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_effective_investment_in_gas_exploration": 1},
    other_deps={
        "_integ_effective_investment_in_gas_exploration": {
            "initial": {"init_eige": 1},
            "step": {"change_in_effective_investment_in_gas_exploration": 1},
        }
    },
)
def effective_investment_in_gas_exploration():
    """
    Effective investments dedicated for gas resources exploration.
    """
    return _integ_effective_investment_in_gas_exploration()


_integ_effective_investment_in_gas_exploration = Integ(
    lambda: change_in_effective_investment_in_gas_exploration(),
    lambda: init_eige(),
    "_integ_effective_investment_in_gas_exploration",
)


@component.add(
    name="Effective Investment in Gas Production",
    units="$/Year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_effective_investment_in_gas_production": 1},
    other_deps={
        "_integ_effective_investment_in_gas_production": {
            "initial": {"init_eigp": 1},
            "step": {"change_in_effective_investment_in_gas_production": 1},
        }
    },
)
def effective_investment_in_gas_production():
    """
    Effective investments dedicated for gas resources production.
    """
    return _integ_effective_investment_in_gas_production()


_integ_effective_investment_in_gas_production = Integ(
    lambda: change_in_effective_investment_in_gas_production(),
    lambda: init_eigp(),
    "_integ_effective_investment_in_gas_production",
)


@component.add(
    name="Effectiveness IRGFDU",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_gas_discovery_technology": 1,
        "effectiveness_of_investment_in_gas_discovery_technology": 1,
    },
)
def effectiveness_irgfdu():
    return (
        investment_in_gas_discovery_technology()
        * effectiveness_of_investment_in_gas_discovery_technology()
    )


@component.add(
    name="Effectiveness IRGFRU",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_gas_recovery_technology": 1,
        "effectiveness_of_investment_in_gas_recovery_technology": 1,
    },
)
def effectiveness_irgfru():
    return (
        investment_in_gas_recovery_technology()
        * effectiveness_of_investment_in_gas_recovery_technology()
    )


@component.add(
    name="Effectiveness of Investment in Gas Discovery Technology",
    units="1/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effectiveness_of_investment_in_gas_discovery_technology_variation": 1,
        "time": 1,
    },
)
def effectiveness_of_investment_in_gas_discovery_technology():
    """
    Effectiveness of resources dedicated to gas discovery technology development.
    """
    return 1.86e-09 + step(
        __data["time"],
        effectiveness_of_investment_in_gas_discovery_technology_variation() - 1.86e-09,
        2020,
    )


@component.add(
    name="Effectiveness of Investment in Gas Discovery Technology Variation",
    units="1/$",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effectiveness_of_investment_in_gas_discovery_technology_variation():
    """
    Effectiveness of resources dedicated to gas discovery technology development.
    """
    return 1.86e-09


@component.add(
    name="Effectiveness of Investment in Gas Recovery Technology",
    units="1/$",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "eigr_var_s": 1,
        "_smooth_effectiveness_of_investment_in_gas_recovery_technology": 1,
    },
    other_deps={
        "_smooth_effectiveness_of_investment_in_gas_recovery_technology": {
            "initial": {
                "effectiveness_of_investment_in_gas_recovery_technology_variation": 1,
                "eigr_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "effectiveness_of_investment_in_gas_recovery_technology_variation": 1,
                "eigr_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def effectiveness_of_investment_in_gas_recovery_technology():
    """
    Effectiveness of resources dedicated to gas recovery technology development.
    """
    return (
        eigr_var_s() + _smooth_effectiveness_of_investment_in_gas_recovery_technology()
    )


_smooth_effectiveness_of_investment_in_gas_recovery_technology = Smooth(
    lambda: step(
        __data["time"],
        effectiveness_of_investment_in_gas_recovery_technology_variation()
        - eigr_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        effectiveness_of_investment_in_gas_recovery_technology_variation()
        - eigr_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_effectiveness_of_investment_in_gas_recovery_technology",
)


@component.add(
    name="Effectiveness of Investment in Gas Recovery Technology Variation",
    units="1/$",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effectiveness_of_investment_in_gas_recovery_technology_variation():
    """
    Effectiveness of resources dedicated to gas recovery technology development.
    """
    return 3e-11


@component.add(name="EIGR S", units="1/$", comp_type="Constant", comp_subtype="Normal")
def eigr_s():
    """
    Effectiveness of resources dedicated to gas recovery technology development.
    """
    return 3e-11


@component.add(
    name="EIGR Var S",
    units="1/$",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_eigr_var_s": 1},
    other_deps={
        "_smooth_eigr_var_s": {
            "initial": {"eigr_s": 1, "time": 1},
            "step": {"eigr_s": 1, "time": 1},
        }
    },
)
def eigr_var_s():
    """
    Effectiveness of resources dedicated to gas recovery technology development.
    """
    return 3e-11 + _smooth_eigr_var_s()


_smooth_eigr_var_s = Smooth(
    lambda: step(__data["time"], eigr_s() - 3e-11, 2020),
    lambda: 1,
    lambda: step(__data["time"], eigr_s() - 3e-11, 2020),
    lambda: 1,
    "_smooth_eigr_var_s",
)


@component.add(
    name="FG S",
    units="Dmnl",
    limits=(0.0, 0.6),
    comp_type="Constant",
    comp_subtype="Normal",
)
def fg_s():
    """
    Percentage of total gas sector revenue dedicated to exploration and production technology development.
    """
    return 0.4


@component.add(
    name="FG Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_fg_var_s": 1},
    other_deps={
        "_smooth_fg_var_s": {
            "initial": {"fg_s": 1, "time": 1},
            "step": {"fg_s": 1, "time": 1},
        }
    },
)
def fg_var_s():
    """
    Percentage of total gas sector revenue dedicated to exploration and production technology development.
    """
    return 0.4 + _smooth_fg_var_s()


_smooth_fg_var_s = Smooth(
    lambda: step(__data["time"], fg_s() - 0.4, 2020),
    lambda: 1,
    lambda: step(__data["time"], fg_s() - 0.4, 2020),
    lambda: 1,
    "_smooth_fg_var_s",
)


@component.add(
    name="Fraction Invested in Gas Discovery Technology",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gas_fraction_discoverable": 1, "table_for_figdt": 1},
)
def fraction_invested_in_gas_discovery_technology():
    """
    Fraction of investments in gas technology dedicated to discovery technology.
    """
    return table_for_figdt(gas_fraction_discoverable())


@component.add(
    name="Fraction of Gas Revenues Invested in Technology",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "fg_var_s": 1,
        "_smooth_fraction_of_gas_revenues_invested_in_technology": 1,
    },
    other_deps={
        "_smooth_fraction_of_gas_revenues_invested_in_technology": {
            "initial": {
                "fraction_of_gas_revenues_invested_in_technology_variation": 1,
                "fg_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "fraction_of_gas_revenues_invested_in_technology_variation": 1,
                "fg_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def fraction_of_gas_revenues_invested_in_technology():
    """
    Percentage of total gas sector revenue dedicated to exploration and production technology development.
    """
    return fg_var_s() + _smooth_fraction_of_gas_revenues_invested_in_technology()


_smooth_fraction_of_gas_revenues_invested_in_technology = Smooth(
    lambda: step(
        __data["time"],
        fraction_of_gas_revenues_invested_in_technology_variation() - fg_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        fraction_of_gas_revenues_invested_in_technology_variation() - fg_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_fraction_of_gas_revenues_invested_in_technology",
)


@component.add(
    name="Fraction of Gas Revenues Invested in Technology Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraction_of_gas_revenues_invested_in_technology_variation():
    """
    Percentage of total gas sector revenue dedicated to exploration and production technology development.
    """
    return 0.4


@component.add(
    name="Gas Cost",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"unit_cost_of_gas_exploration": 1, "unit_cost_of_gas_production": 1},
)
def gas_cost():
    """
    Cost of unit gas resources as a sum of unit exploration and production costs.
    """
    return unit_cost_of_gas_exploration() + unit_cost_of_gas_production()


@component.add(
    name="Gas Demand to Supply Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_gas_demand": 1, "potential_gas_production": 1},
)
def gas_demand_to_supply_ratio():
    """
    Gas Demand to Supply Ratio.
    """
    return total_gas_demand() / potential_gas_production()


@component.add(
    name="Gas Discovery and Recovery Technology Development Time Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def gas_discovery_and_recovery_technology_development_time_variation():
    return 6


@component.add(
    name="Gas Discovery Technology Development Time",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"gdr_var_s": 1, "_smooth_gas_discovery_technology_development_time": 1},
    other_deps={
        "_smooth_gas_discovery_technology_development_time": {
            "initial": {
                "gas_discovery_and_recovery_technology_development_time_variation": 1,
                "gdr_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "gas_discovery_and_recovery_technology_development_time_variation": 1,
                "gdr_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def gas_discovery_technology_development_time():
    """
    Average time required to turn investments into concrete gas discovery developments.
    """
    return gdr_var_s() + _smooth_gas_discovery_technology_development_time()


_smooth_gas_discovery_technology_development_time = Smooth(
    lambda: step(
        __data["time"],
        gas_discovery_and_recovery_technology_development_time_variation()
        - gdr_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        gas_discovery_and_recovery_technology_development_time_variation()
        - gdr_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_gas_discovery_technology_development_time",
)


@component.add(
    name="Gas Exploration",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gas_exploration_rate": 1},
)
def gas_exploration():
    """
    Gas resources discovery rate.
    """
    return float(np.maximum(0, gas_exploration_rate()))


@component.add(
    name="Gas Exploration Rate",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_gas_exploration_rate": 1, "potential_gas_exploration": 1},
)
def gas_exploration_rate():
    """
    Gas Exploration Rate accounting for potential and desired gas exploration rates.
    """
    return float(
        np.minimum(desired_gas_exploration_rate(), potential_gas_exploration())
    )


@component.add(
    name="Gas Fraction Discoverable",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "mingfd": 2,
        "ratio_of_gas_fraction_discoverable_to_undiscoverable": 2,
        "maxgfd": 1,
    },
)
def gas_fraction_discoverable():
    """
    Percentage of gas resources that can be still explored due to current state of discovery technology.
    """
    return mingfd() + (maxgfd() - mingfd()) * (
        ratio_of_gas_fraction_discoverable_to_undiscoverable()
        / (ratio_of_gas_fraction_discoverable_to_undiscoverable() + 1)
    )


@component.add(
    name="Gas Fraction Recoverable",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "mingfr": 2,
        "maxgfr": 1,
        "ratio_of_gas_fraction_recoverable_to_unrecoverable": 2,
    },
)
def gas_fraction_recoverable():
    """
    Percentage of gas resources that can be produced due to current state of recovery technology.
    """
    return mingfr() + (maxgfr() - mingfr()) * (
        ratio_of_gas_fraction_recoverable_to_unrecoverable()
        / (ratio_of_gas_fraction_recoverable_to_unrecoverable() + 1)
    )


@component.add(
    name="Gas Gross Margin",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gas_price": 1, "gas_cost": 2},
)
def gas_gross_margin():
    """
    Actual gas gross margin.
    """
    return (gas_price() - gas_cost()) / gas_cost()


@component.add(
    name="Gas Price",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "indicated_gas_price": 1,
        "effect_of_gas_demand_and_supply_on_price": 1,
    },
)
def gas_price():
    """
    Actual gas price accounting for indicated gas price and effect of demand and supply.
    """
    return indicated_gas_price() * effect_of_gas_demand_and_supply_on_price()


@component.add(
    name="Gas Price per MBtu",
    units="$/MBtu",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gas_price": 1, "mtoe_per_btu": 1},
)
def gas_price_per_mbtu():
    """
    Actual Gas Price per Barrel.
    """
    return gas_price() * mtoe_per_btu()


@component.add(
    name="Gas Production",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gas_production_rate": 1},
)
def gas_production():
    """
    Total gas energy production per year. Source of historical data: International Energy Agency – Key World Energy Statistics 2007; BP Statistical Review of World Energy June 2008
    """
    return gas_production_rate()


@component.add(
    name="Gas Production Coverage",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"identified_gas_resources": 1, "average_gas_production": 1},
)
def gas_production_coverage():
    """
    Ratio indicating gas coverage in years for discovered resources and at the current average gas production.
    """
    return identified_gas_resources() / average_gas_production()


@component.add(
    name="Gas Production Indicator",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gas_production": 1, "mtoe_into_ej": 1},
)
def gas_production_indicator():
    return gas_production() * mtoe_into_ej()


@component.add(
    name="Gas Production Rate",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_gas_demand": 1, "potential_gas_production": 1},
)
def gas_production_rate():
    """
    Total gas energy production per year due to available resources, developments in production technology and gas energy demand.
    """
    return float(np.minimum(total_gas_demand(), potential_gas_production()))


@component.add(
    name="Gas Productivity of Investment",
    units="toe/$",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_gas_productivity_of_investment": 1},
    other_deps={
        "_integ_gas_productivity_of_investment": {
            "initial": {"init_gpi": 1},
            "step": {"change_in_gas_productivity_of_investment": 1},
        }
    },
)
def gas_productivity_of_investment():
    """
    Factor indicating productivity of investments in gas production.
    """
    return _integ_gas_productivity_of_investment()


_integ_gas_productivity_of_investment = Integ(
    lambda: change_in_gas_productivity_of_investment(),
    lambda: init_gpi(),
    "_integ_gas_productivity_of_investment",
)


@component.add(
    name="Gas Recovery Technology Development Time",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"gdr_var_s": 1, "_smooth_gas_recovery_technology_development_time": 1},
    other_deps={
        "_smooth_gas_recovery_technology_development_time": {
            "initial": {
                "gas_discovery_and_recovery_technology_development_time_variation": 1,
                "gdr_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "gas_discovery_and_recovery_technology_development_time_variation": 1,
                "gdr_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def gas_recovery_technology_development_time():
    """
    Average time required to turn investments into concrete gas recovery developments.
    """
    return gdr_var_s() + _smooth_gas_recovery_technology_development_time()


_smooth_gas_recovery_technology_development_time = Smooth(
    lambda: step(
        __data["time"],
        gas_discovery_and_recovery_technology_development_time_variation()
        - gdr_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        gas_discovery_and_recovery_technology_development_time_variation()
        - gdr_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_gas_recovery_technology_development_time",
)


@component.add(
    name="Gas Revenue",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gas_price": 1, "average_gas_production": 1},
)
def gas_revenue():
    """
    Total revenue in gas market.
    """
    return gas_price() * average_gas_production()


@component.add(
    name="Gas Shortage",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_gas_demand": 1, "gas_production": 1},
)
def gas_shortage():
    """
    Difference between demand and the gas production rate.
    """
    return total_gas_demand() - gas_production()


@component.add(name="GDR S", units="Year", comp_type="Constant", comp_subtype="Normal")
def gdr_s():
    return 6


@component.add(
    name="GDR Var S",
    units="$",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_gdr_var_s": 1},
    other_deps={
        "_smooth_gdr_var_s": {
            "initial": {"gdr_s": 1, "time": 1},
            "step": {"gdr_s": 1, "time": 1},
        }
    },
)
def gdr_var_s():
    return 6 + _smooth_gdr_var_s()


_smooth_gdr_var_s = Smooth(
    lambda: step(__data["time"], gdr_s() - 6, 2020),
    lambda: 1,
    lambda: step(__data["time"], gdr_s() - 6, 2020),
    lambda: 1,
    "_smooth_gdr_var_s",
)


@component.add(
    name="Identified Gas Resources",
    units="Mtoe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_identified_gas_resources": 1},
    other_deps={
        "_integ_identified_gas_resources": {
            "initial": {
                "total_gas_demand": 1,
                "normal_gas_production_ratio": 1,
                "cumulative_gas_production": 1,
                "gas_fraction_recoverable": 2,
            },
            "step": {"gas_exploration": 1, "gas_production": 1},
        }
    },
)
def identified_gas_resources():
    """
    Gas Resources discovered thanks to developments in exploration technology.
    """
    return _integ_identified_gas_resources()


_integ_identified_gas_resources = Integ(
    lambda: gas_exploration() - gas_production(),
    lambda: (
        total_gas_demand() * normal_gas_production_ratio()
        + cumulative_gas_production() * (1 - gas_fraction_recoverable())
    )
    / gas_fraction_recoverable(),
    "_integ_identified_gas_resources",
)


@component.add(
    name="Identified Gas Resources Adjustment Time",
    units="Year",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def identified_gas_resources_adjustment_time():
    """
    Time to adjust Identified Gas Resource to the desired level.
    """
    return 5


@component.add(name="IG S", units="Year", comp_type="Constant", comp_subtype="Normal")
def ig_s():
    return 5


@component.add(
    name="IG Var S",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_ig_var_s": 1},
    other_deps={
        "_smooth_ig_var_s": {
            "initial": {"ig_s": 1, "time": 1},
            "step": {"ig_s": 1, "time": 1},
        }
    },
)
def ig_var_s():
    return 5 + _smooth_ig_var_s()


_smooth_ig_var_s = Smooth(
    lambda: step(__data["time"], ig_s() - 5, 2020),
    lambda: 1,
    lambda: step(__data["time"], ig_s() - 5, 2020),
    lambda: 1,
    "_smooth_ig_var_s",
)


@component.add(
    name="Increase in Ratio of Gas Fraction Discoverable to Undiscoverable",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_irgfdulv3": 1},
)
def increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable():
    """
    Increase in Ratio of Gas Fraction Discoverable to Undiscoverable due to investments in discovery technology and their productivity.
    """
    return outflow_irgfdulv3()


@component.add(
    name="Increase in Ratio of Gas Fraction Discoverable to Undiscoverable LV1",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv1": 1
    },
    other_deps={
        "_integ_increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv1": {
            "initial": {
                "increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv3": 1
            },
            "step": {"inflow_irgfdulv1": 1, "outflow_irgfdulv1": 1},
        }
    },
)
def increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv1():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv1()


_integ_increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv1 = Integ(
    lambda: inflow_irgfdulv1() - outflow_irgfdulv1(),
    lambda: increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv3(),
    "_integ_increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv1",
)


@component.add(
    name="Increase in Ratio of Gas Fraction Discoverable to Undiscoverable LV2",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv2": 1
    },
    other_deps={
        "_integ_increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv2": {
            "initial": {
                "increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv3": 1
            },
            "step": {"inflow_irgfdulv2": 1, "outflow_irgfdulv2": 1},
        }
    },
)
def increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv2():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv2()


_integ_increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv2 = Integ(
    lambda: inflow_irgfdulv2() - outflow_irgfdulv2(),
    lambda: increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv3(),
    "_integ_increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv2",
)


@component.add(
    name="Increase in Ratio of Gas Fraction Discoverable to Undiscoverable LV3",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv3": 1
    },
    other_deps={
        "_integ_increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv3": {
            "initial": {"effectiveness_irgfdu": 1, "delay_time_irgfdu": 1},
            "step": {"inflow_irgfdulv3": 1, "outflow_irgfdulv3": 1},
        }
    },
)
def increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv3():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv3()


_integ_increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv3 = Integ(
    lambda: inflow_irgfdulv3() - outflow_irgfdulv3(),
    lambda: effectiveness_irgfdu() * delay_time_irgfdu(),
    "_integ_increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv3",
)


@component.add(
    name="Increase in Ratio of Gas Fraction Recoverable to Unrecoverable",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_irgfrulv3": 1},
)
def increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable():
    """
    Increase in Ratio of Gas Fraction Recoverable to Unrecoverable due to investments in recovery technology and their productivity.
    """
    return outflow_irgfrulv3()


@component.add(
    name="Increase in Ratio of Gas Fraction Recoverable to Unrecoverable LV1",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv1": 1
    },
    other_deps={
        "_integ_increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv1": {
            "initial": {
                "increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv3": 1
            },
            "step": {"inflow_irgfrulv1": 1, "outflow_irgfrulv1": 1},
        }
    },
)
def increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv1():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv1()


_integ_increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv1 = Integ(
    lambda: inflow_irgfrulv1() - outflow_irgfrulv1(),
    lambda: increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv3(),
    "_integ_increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv1",
)


@component.add(
    name="Increase in Ratio of Gas Fraction Recoverable to Unrecoverable LV2",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv2": 1
    },
    other_deps={
        "_integ_increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv2": {
            "initial": {
                "increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv3": 1
            },
            "step": {"inflow_irgfrulv2": 1, "outflow_irgfrulv2": 1},
        }
    },
)
def increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv2():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv2()


_integ_increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv2 = Integ(
    lambda: inflow_irgfrulv2() - outflow_irgfrulv2(),
    lambda: increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv3(),
    "_integ_increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv2",
)


@component.add(
    name="Increase in Ratio of Gas Fraction Recoverable to Unrecoverable LV3",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv3": 1
    },
    other_deps={
        "_integ_increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv3": {
            "initial": {"effectiveness_irgfru": 1, "delay_time_irgfru": 1},
            "step": {"inflow_irgfrulv3": 1, "outflow_irgfrulv3": 1},
        }
    },
)
def increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv3():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv3()


_integ_increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv3 = Integ(
    lambda: inflow_irgfrulv3() - outflow_irgfrulv3(),
    lambda: effectiveness_irgfru() * delay_time_irgfru(),
    "_integ_increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv3",
)


@component.add(
    name="Indicated Gas Price",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gas_cost": 1, "desired_gas_gross_margin": 1},
)
def indicated_gas_price():
    """
    Indicated gas price accounting for exploration and production cost and gross margin.
    """
    return gas_cost() * (1 + desired_gas_gross_margin())


@component.add(
    name="Inflow IRGFDULV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effectiveness_irgfdu": 1},
)
def inflow_irgfdulv1():
    return effectiveness_irgfdu()


@component.add(
    name="Inflow IRGFDULV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_irgfdulv1": 1},
)
def inflow_irgfdulv2():
    return outflow_irgfdulv1()


@component.add(
    name="Inflow IRGFDULV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_irgfdulv2": 1},
)
def inflow_irgfdulv3():
    return outflow_irgfdulv2()


@component.add(
    name="Inflow IRGFRULV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effectiveness_irgfru": 1},
)
def inflow_irgfrulv1():
    return effectiveness_irgfru()


@component.add(
    name="Inflow IRGFRULV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_irgfrulv1": 1},
)
def inflow_irgfrulv2():
    return outflow_irgfrulv1()


@component.add(
    name="Inflow IRGFRULV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_irgfrulv2": 1},
)
def inflow_irgfrulv3():
    return outflow_irgfrulv2()


@component.add(
    name="INIT Average Gas Production", comp_type="Constant", comp_subtype="Normal"
)
def init_average_gas_production():
    return 1.87028


@component.add(
    name="INIT CGPN", units="Mtoe", comp_type="Constant", comp_subtype="Normal"
)
def init_cgpn():
    """
    Cumulative Gas Production
    """
    return 0


@component.add(name="INIT EIGE", comp_type="Constant", comp_subtype="Normal")
def init_eige():
    """
    Effective Investment in Gas Exploration
    """
    return 90816400.0


@component.add(name="INIT EIGP", comp_type="Constant", comp_subtype="Normal")
def init_eigp():
    """
    Effective Investment in Gas Production
    """
    return 9081650.0


@component.add(name="INIT GPI", comp_type="Constant", comp_subtype="Normal")
def init_gpi():
    """
    Gas Productivity of Investment
    """
    return 0.0205941


@component.add(
    name="INIT RGDU",
    units="Dmnl",
    limits=(0.0, 0.2),
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_rgdu():
    """
    Initial Ratio of Gas Fraction Discoverable to Undiscoverable.
    """
    return 0.15


@component.add(
    name="INIT RGRU", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def init_rgru():
    """
    Initial Ratio of Gas Fraction Recoverable to Unrecoverable.
    """
    return 0


@component.add(
    name="INIT UGRN",
    units="Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_world_stock_of_gas_billion_cubic_meter": 1,
        "mtoe_per_billion_cubic_meter": 1,
    },
)
def init_ugrn():
    """
    Initial amount of Undiscovered Gas Resources.
    """
    return (
        initial_world_stock_of_gas_billion_cubic_meter()
        * mtoe_per_billion_cubic_meter()
    )


@component.add(
    name="Initial World Stock of Gas Billion Cubic meter",
    units="Billion Cubic Meters",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_world_stock_of_gas_billion_cubic_meter():
    return 849505


@component.add(
    name="Investment in Gas Discovery Technology",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_gas_technology": 1,
        "fraction_invested_in_gas_discovery_technology": 1,
    },
)
def investment_in_gas_discovery_technology():
    """
    Total investments in gas exploration technology.
    """
    return (
        investment_in_gas_technology() * fraction_invested_in_gas_discovery_technology()
    )


@component.add(
    name="Investment in Gas Exploration",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_investment_in_gas_exploration": 1},
)
def investment_in_gas_exploration():
    """
    Amount of resources dedicated to gas exploration.
    """
    return desired_investment_in_gas_exploration()


@component.add(
    name="Investment in Gas Exploration and Production Delay Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def investment_in_gas_exploration_and_production_delay_variation():
    return 5


@component.add(
    name="Investment in Gas Exploration Delay",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"ig_var_s": 1, "_smooth_investment_in_gas_exploration_delay": 1},
    other_deps={
        "_smooth_investment_in_gas_exploration_delay": {
            "initial": {
                "investment_in_gas_exploration_and_production_delay_variation": 1,
                "ig_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "investment_in_gas_exploration_and_production_delay_variation": 1,
                "ig_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def investment_in_gas_exploration_delay():
    """
    Time delay to make investments in gas exploration effective.
    """
    return ig_var_s() + _smooth_investment_in_gas_exploration_delay()


_smooth_investment_in_gas_exploration_delay = Smooth(
    lambda: step(
        __data["time"],
        investment_in_gas_exploration_and_production_delay_variation() - ig_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        investment_in_gas_exploration_and_production_delay_variation() - ig_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_investment_in_gas_exploration_delay",
)


@component.add(
    name="Investment in Gas Production",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_investment_in_gas_production": 1},
)
def investment_in_gas_production():
    """
    Amount of resources dedicated to gas production.
    """
    return desired_investment_in_gas_production()


@component.add(
    name="Investment in Gas Production Delay",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"ig_var_s": 1, "_smooth_investment_in_gas_production_delay": 1},
    other_deps={
        "_smooth_investment_in_gas_production_delay": {
            "initial": {
                "investment_in_gas_exploration_and_production_delay_variation": 1,
                "ig_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "investment_in_gas_exploration_and_production_delay_variation": 1,
                "ig_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def investment_in_gas_production_delay():
    """
    Time delay to make investments in gas production effective.
    """
    return ig_var_s() + _smooth_investment_in_gas_production_delay()


_smooth_investment_in_gas_production_delay = Smooth(
    lambda: step(
        __data["time"],
        investment_in_gas_exploration_and_production_delay_variation() - ig_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        investment_in_gas_exploration_and_production_delay_variation() - ig_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_investment_in_gas_production_delay",
)


@component.add(
    name="Investment in Gas Recovery Technology",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_gas_technology": 1,
        "fraction_invested_in_gas_discovery_technology": 1,
    },
)
def investment_in_gas_recovery_technology():
    """
    Total investments in gas production technology.
    """
    return investment_in_gas_technology() * (
        1 - fraction_invested_in_gas_discovery_technology()
    )


@component.add(
    name="Investment in Gas Technology",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fraction_of_gas_revenues_invested_in_technology": 1, "gas_revenue": 1},
)
def investment_in_gas_technology():
    """
    Investments in development of gas exploration and production technology.
    """
    return fraction_of_gas_revenues_invested_in_technology() * gas_revenue()


@component.add(
    name="Max Unit Cost of Gas Exploration",
    units="$/Mtoe",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"mfc_var_s": 1, "_smooth_max_unit_cost_of_gas_exploration": 1},
    other_deps={
        "_smooth_max_unit_cost_of_gas_exploration": {
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
def max_unit_cost_of_gas_exploration():
    """
    Upper level limit for unit cost of gas exploration.
    """
    return mfc_var_s() + _smooth_max_unit_cost_of_gas_exploration()


_smooth_max_unit_cost_of_gas_exploration = Smooth(
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
    "_smooth_max_unit_cost_of_gas_exploration",
)


@component.add(name="MAXGFD", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def maxgfd():
    """
    Maximal possible percentage of gas resources to be discovered.
    """
    return 1


@component.add(name="MAXGFR", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def maxgfr():
    """
    Maximal possible percentage of gas resources to be recovered.
    """
    return 1


@component.add(name="MINGFD", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def mingfd():
    """
    Initial and minimal possible percentage of gas resources to be discovered.
    """
    return 0.02


@component.add(name="MINGFR", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def mingfr():
    """
    Initial and minimal possible percentage of gas resources to be recovered.
    """
    return 0.008


@component.add(
    name="Mtoe per Billion Cubic meter",
    units="Mtoe/Billion Cubic Meters",
    comp_type="Constant",
    comp_subtype="Normal",
)
def mtoe_per_billion_cubic_meter():
    """
    Unit conversion: https://www.bp.com/content/dam/bp/business-sites/en/global/corporate/pdfs/e nergy-economics/statistical-review/bp-stats-review-2019-approximate-convers ion-factors.pdf
    """
    return 0.86


@component.add(
    name="Mtoe per Btu", units="Mtoe/MBtu", comp_type="Constant", comp_subtype="Normal"
)
def mtoe_per_btu():
    """
    Coefficient to convert million tons of oil equivalent unit (Mtoe) into British thermal unit (Btu).
    """
    return 2.5e-08


@component.add(
    name="Normal Gas Production Ratio",
    units="Year",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_gas_production_ratio():
    """
    Safety stock coverage as a number of years of the total gas demand the gas sector would like to maintain in identified gas resources. It secures the market against possibility of unforeseen variations in demand. It is also a stimulus for gas exploration.
    """
    return 5


@component.add(
    name="Outflow IRGFDULV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv1": 1,
        "delay_time_irgfdu": 1,
    },
)
def outflow_irgfdulv1():
    return (
        increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv1()
        / delay_time_irgfdu()
    )


@component.add(
    name="Outflow IRGFDULV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv2": 1,
        "delay_time_irgfdu": 1,
    },
)
def outflow_irgfdulv2():
    return (
        increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv2()
        / delay_time_irgfdu()
    )


@component.add(
    name="Outflow IRGFDULV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv3": 1,
        "delay_time_irgfdu": 1,
    },
)
def outflow_irgfdulv3():
    return (
        increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable_lv3()
        / delay_time_irgfdu()
    )


@component.add(
    name="Outflow IRGFRULV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv1": 1,
        "delay_time_irgfru": 1,
    },
)
def outflow_irgfrulv1():
    return (
        increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv1()
        / delay_time_irgfru()
    )


@component.add(
    name="Outflow IRGFRULV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv2": 1,
        "delay_time_irgfru": 1,
    },
)
def outflow_irgfrulv2():
    return (
        increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv2()
        / delay_time_irgfru()
    )


@component.add(
    name="Outflow IRGFRULV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv3": 1,
        "delay_time_irgfru": 1,
    },
)
def outflow_irgfrulv3():
    return (
        increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable_lv3()
        / delay_time_irgfru()
    )


@component.add(
    name="Potential Gas Exploration",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effective_investment_in_gas_exploration": 1,
        "productivity_of_investment_in_gas_exploration": 1,
        "toe_per_mtoe": 1,
    },
)
def potential_gas_exploration():
    """
    Potential Gas exploration due to available investments in gas resources discovery.
    """
    return (
        effective_investment_in_gas_exploration()
        * productivity_of_investment_in_gas_exploration()
        / toe_per_mtoe()
    )


@component.add(
    name="Potential Gas Production",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_gas_production_from_investment": 1,
        "potential_gas_production_from_resources": 1,
    },
)
def potential_gas_production():
    """
    Potential Gas Production due to available investments in gas resources recovery and recovery technology.
    """
    return float(
        np.minimum(
            potential_gas_production_from_investment(),
            potential_gas_production_from_resources(),
        )
    )


@component.add(
    name="Potential Gas Production from Investment",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "productivity_of_investment_in_gas_production": 1,
        "effective_investment_in_gas_production": 1,
        "toe_per_mtoe": 1,
    },
)
def potential_gas_production_from_investment():
    """
    Potential Gas Production due to available investments in gas resources recovery.
    """
    return (
        productivity_of_investment_in_gas_production()
        * effective_investment_in_gas_production()
        / toe_per_mtoe()
    )


@component.add(
    name="Potential Gas Production from Resources",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_gas_recoverable_resource_remaining": 1,
        "normal_gas_production_ratio": 1,
    },
)
def potential_gas_production_from_resources():
    """
    Potential Gas Production rate due to Total Oil Recoverable Resource Remaining adjusted by oil production safety coverage.
    """
    return total_gas_recoverable_resource_remaining() / normal_gas_production_ratio()


@component.add(
    name="Productivity of Investment in Gas Exploration",
    units="toe/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "relative_productivity_of_investment_in_gas_exploration": 1,
        "effect_of_technology_on_gas_discoveries": 1,
    },
)
def productivity_of_investment_in_gas_exploration():
    """
    Parameter indicating the amount of gas resources possible to be explored per unit investment spent.
    """
    return float(
        np.maximum(
            0,
            relative_productivity_of_investment_in_gas_exploration()
            * effect_of_technology_on_gas_discoveries(),
        )
    )


@component.add(
    name="Productivity of Investment in Gas Production",
    units="toe/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "relative_productivity_of_investment_in_gas_production_to_exploration": 1,
        "gas_productivity_of_investment": 1,
    },
)
def productivity_of_investment_in_gas_production():
    """
    Parameter indicating the amount of gas resources possible to be recovered per unit investment spent.
    """
    return (
        relative_productivity_of_investment_in_gas_production_to_exploration()
        * gas_productivity_of_investment()
    )


@component.add(
    name="Rate of New Discovery Gas",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_growth_in_gas_reserves": 1, "mtoe_per_billion_cubic_meter": 1},
)
def rate_of_new_discovery_gas():
    return annual_growth_in_gas_reserves() * mtoe_per_billion_cubic_meter()


@component.add(
    name="Ratio of Gas Fraction Discoverable to Undiscoverable",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ratio_of_gas_fraction_discoverable_to_undiscoverable": 1},
    other_deps={
        "_integ_ratio_of_gas_fraction_discoverable_to_undiscoverable": {
            "initial": {"init_rgdu": 1},
            "step": {
                "increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable": 1
            },
        }
    },
)
def ratio_of_gas_fraction_discoverable_to_undiscoverable():
    """
    Ratio of Gas Fraction Discoverable to Undiscoverable increased due to investments in discovery technology and their productivity.
    """
    return _integ_ratio_of_gas_fraction_discoverable_to_undiscoverable()


_integ_ratio_of_gas_fraction_discoverable_to_undiscoverable = Integ(
    lambda: increase_in_ratio_of_gas_fraction_discoverable_to_undiscoverable(),
    lambda: init_rgdu(),
    "_integ_ratio_of_gas_fraction_discoverable_to_undiscoverable",
)


@component.add(
    name="Ratio of Gas Fraction Recoverable to Unrecoverable",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ratio_of_gas_fraction_recoverable_to_unrecoverable": 1},
    other_deps={
        "_integ_ratio_of_gas_fraction_recoverable_to_unrecoverable": {
            "initial": {"init_rgru": 1},
            "step": {
                "increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable": 1
            },
        }
    },
)
def ratio_of_gas_fraction_recoverable_to_unrecoverable():
    """
    Ratio of Gas Fraction Recoverable to Unrecoverable increased due to investments in recovery technology and their productivity.
    """
    return _integ_ratio_of_gas_fraction_recoverable_to_unrecoverable()


_integ_ratio_of_gas_fraction_recoverable_to_unrecoverable = Integ(
    lambda: increase_in_ratio_of_gas_fraction_recoverable_to_unrecoverable(),
    lambda: init_rgru(),
    "_integ_ratio_of_gas_fraction_recoverable_to_unrecoverable",
)


@component.add(
    name="Relative Productivity of Investment in Gas Exploration",
    units="toe/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "relative_productivity_of_investment_in_gas_exploration_variation": 1,
        "time": 1,
    },
)
def relative_productivity_of_investment_in_gas_exploration():
    """
    Relative Productivity of Investment in Gas Exploration without taking into account remaining undiscovered gas resources and advances in exploration technologies.
    """
    return 0.1 + step(
        __data["time"],
        relative_productivity_of_investment_in_gas_exploration_variation() - 0.1,
        2020,
    )


@component.add(
    name="Relative Productivity of Investment in Gas Exploration Variation",
    units="toe/$",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def relative_productivity_of_investment_in_gas_exploration_variation():
    """
    Relative Productivity of Investment in Gas Exploration without taking into account remaining undiscovered gas resources and advances in exploration technologies.
    """
    return 0.1


@component.add(
    name="Relative Productivity of Investment in Gas Production Compared to Exploration Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def relative_productivity_of_investment_in_gas_production_compared_to_exploration_variation():
    return 0.3


@component.add(
    name="Relative Productivity of Investment in Gas Production to Exploration",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "rpgpe_var_s": 1,
        "_smooth_relative_productivity_of_investment_in_gas_production_to_exploration": 1,
    },
    other_deps={
        "_smooth_relative_productivity_of_investment_in_gas_production_to_exploration": {
            "initial": {
                "relative_productivity_of_investment_in_gas_production_compared_to_exploration_variation": 1,
                "rpgpe_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "relative_productivity_of_investment_in_gas_production_compared_to_exploration_variation": 1,
                "rpgpe_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def relative_productivity_of_investment_in_gas_production_to_exploration():
    """
    Relative Productivity of Investment in Gas Production as a multiplier of Productivity of Investment in Gas Exploration.
    """
    return (
        rpgpe_var_s()
        + _smooth_relative_productivity_of_investment_in_gas_production_to_exploration()
    )


_smooth_relative_productivity_of_investment_in_gas_production_to_exploration = Smooth(
    lambda: step(
        __data["time"],
        relative_productivity_of_investment_in_gas_production_compared_to_exploration_variation()
        - rpgpe_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        relative_productivity_of_investment_in_gas_production_compared_to_exploration_variation()
        - rpgpe_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_relative_productivity_of_investment_in_gas_production_to_exploration",
)


@component.add(
    name="Required Identified Gas Resources",
    units="Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "identified_gas_resources": 1,
        "total_gas_recoverable_resource_remaining": 1,
        "normal_gas_production_ratio": 1,
        "total_gas_demand": 1,
    },
)
def required_identified_gas_resources():
    """
    The desired Identified Gas Resources level sought by the gas sector.
    """
    return (identified_gas_resources() / total_gas_recoverable_resource_remaining()) * (
        normal_gas_production_ratio() * total_gas_demand()
    )


@component.add(
    name="RPGPE S", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def rpgpe_s():
    return 0.3


@component.add(
    name="RPGPE Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_rpgpe_var_s": 1},
    other_deps={
        "_smooth_rpgpe_var_s": {
            "initial": {"rpgpe_s": 1, "time": 1},
            "step": {"rpgpe_s": 1, "time": 1},
        }
    },
)
def rpgpe_var_s():
    return 0.3 + _smooth_rpgpe_var_s()


_smooth_rpgpe_var_s = Smooth(
    lambda: step(__data["time"], rpgpe_s() - 0.3, 2020),
    lambda: 1,
    lambda: step(__data["time"], rpgpe_s() - 0.3, 2020),
    lambda: 1,
    "_smooth_rpgpe_var_s",
)


@component.add(
    name="Sensitivity of Gas Price to Supply and Demand",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "sg_var_s": 1,
        "_smooth_sensitivity_of_gas_price_to_supply_and_demand": 1,
    },
    other_deps={
        "_smooth_sensitivity_of_gas_price_to_supply_and_demand": {
            "initial": {
                "sensitivity_of_gas_price_to_supply_and_demand_variation": 1,
                "sg_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "sensitivity_of_gas_price_to_supply_and_demand_variation": 1,
                "sg_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_demand_variation_time": 1,
            },
        }
    },
)
def sensitivity_of_gas_price_to_supply_and_demand():
    """
    Sensitivity of Gas Price to Supply and Demand ratio.
    """
    return sg_var_s() + _smooth_sensitivity_of_gas_price_to_supply_and_demand()


_smooth_sensitivity_of_gas_price_to_supply_and_demand = Smooth(
    lambda: step(
        __data["time"],
        sensitivity_of_gas_price_to_supply_and_demand_variation() - sg_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_demand_variation_time(),
    lambda: step(
        __data["time"],
        sensitivity_of_gas_price_to_supply_and_demand_variation() - sg_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_sensitivity_of_gas_price_to_supply_and_demand",
)


@component.add(
    name="Sensitivity of Gas Price to Supply and Demand Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sensitivity_of_gas_price_to_supply_and_demand_variation():
    return 1.11429


@component.add(
    name="SG Init",
    units="Dmnl",
    limits=(0.0, 1.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def sg_init():
    """
    A CONSTANT
    """
    return 0.05


@component.add(
    name="SG S",
    units="Dmnl",
    limits=(0.0, 3.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def sg_s():
    return 1.11429


@component.add(
    name="SG Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_sg_var_s": 1},
    other_deps={
        "_smooth_sg_var_s": {
            "initial": {"sg_s": 1, "time": 1},
            "step": {"sg_s": 1, "time": 1},
        }
    },
)
def sg_var_s():
    return 1.11429 + _smooth_sg_var_s()


_smooth_sg_var_s = Smooth(
    lambda: step(__data["time"], sg_s() - 1.11429, 2020),
    lambda: 1,
    lambda: step(__data["time"], sg_s() - 1.11429, 2020),
    lambda: 1,
    "_smooth_sg_var_s",
)


@component.add(
    name="Share of Investment in Revenue Gas",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_investment_in_gas": 1, "gas_revenue": 1},
)
def share_of_investment_in_revenue_gas():
    return total_investment_in_gas() / gas_revenue()


@component.add(
    name="Share of Upstream Investment in Total Investment Gas",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def share_of_upstream_investment_in_total_investment_gas():
    """
    Data from World Energy Investment 2023
    """
    return 0.9


@component.add(
    name="Table for FIGDT",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_table_for_figdt"},
)
def table_for_figdt(x, final_subs=None):
    """
    Table determining order by which technology investments are dedicated to gas exploration and production technologies. For small Gas Fraction Discoverable, in order to make sufficient resources available to be produced, more investments are directed to exploration technologies. Once the Gas Fraction Discoverable increases the investments are redirected to production technologies.
    """
    return _hardcodedlookup_table_for_figdt(x, final_subs)


_hardcodedlookup_table_for_figdt = HardcodedLookups(
    [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
    [0.8, 0.8, 0.7, 0.5, 0.2, 0.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_for_figdt",
)


@component.add(
    name="Time to Average Gas Production",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_average_gas_production():
    """
    Time to average total gas production per year.
    """
    return 1


@component.add(
    name="Total Gas Demand",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_demand": 1, "market_share_gas": 1},
)
def total_gas_demand():
    """
    Total demand for gas resources.
    """
    return energy_demand() * market_share_gas()


@component.add(
    name="Total Gas Discoverable Resources",
    units="Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_gas_resources": 1,
        "gas_fraction_discoverable": 1,
        "cumulative_additions_to_gas_production": 1,
    },
)
def total_gas_discoverable_resources():
    """
    Total Gas Discoverable Resources as a percentage of Total Gas Resources. It excludes identified and already produced resources. The percentage is determined by exploration technology developments.
    """
    return (
        total_gas_resources() * gas_fraction_discoverable()
        - cumulative_additions_to_gas_production()
    )


@component.add(
    name="Total Gas Recoverable Resource Remaining",
    units="Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cumulative_additions_to_gas_production": 1,
        "gas_fraction_recoverable": 1,
        "cumulative_gas_production": 1,
    },
)
def total_gas_recoverable_resource_remaining():
    """
    Total Gas Recoverable Resources Remaining as a percentage of Cumulative Additions to Gas Production. It excludes already produced resources. The percentage is determined by production technology developments.
    """
    return (
        cumulative_additions_to_gas_production() * gas_fraction_recoverable()
        - cumulative_gas_production()
    )


@component.add(
    name="Total Gas Resources",
    units="Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "undiscovered_gas_resources": 1,
        "cumulative_additions_to_gas_production": 1,
    },
)
def total_gas_resources():
    """
    Total gas resources including Undiscovered Gas Resources, Identified Gas Resources and resources already produced i.e. Cumulative Gas Production.
    """
    return undiscovered_gas_resources() + cumulative_additions_to_gas_production()


@component.add(
    name="Total Investment in Gas",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_gas_exploration": 1,
        "investment_in_gas_production": 1,
        "investment_in_gas_technology": 1,
        "share_of_upstream_investment_in_total_investment_gas": 1,
    },
)
def total_investment_in_gas():
    return (
        investment_in_gas_exploration()
        + investment_in_gas_production()
        + investment_in_gas_technology()
    ) / share_of_upstream_investment_in_total_investment_gas()


@component.add(
    name="Undiscovered Gas Resources",
    units="Mtoe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_undiscovered_gas_resources": 1},
    other_deps={
        "_integ_undiscovered_gas_resources": {
            "initial": {"init_ugrn": 1},
            "step": {"rate_of_new_discovery_gas": 1, "gas_exploration": 1},
        }
    },
)
def undiscovered_gas_resources():
    """
    Existing Gas Resources but not discovered yet.
    """
    return _integ_undiscovered_gas_resources()


_integ_undiscovered_gas_resources = Integ(
    lambda: rate_of_new_discovery_gas() - gas_exploration(),
    lambda: init_ugrn(),
    "_integ_undiscovered_gas_resources",
)


@component.add(
    name="Unit Cost of Gas Exploration",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_unit_cost_of_gas_exploration": 1,
        "productivity_of_investment_in_gas_exploration": 2,
        "toe_per_mtoe": 1,
    },
)
def unit_cost_of_gas_exploration():
    """
    Unit cost of gas exploration. Depends on remaining undiscovered gas resources and advances in exploration technologies.
    """
    return float(
        np.minimum(
            max_unit_cost_of_gas_exploration(),
            if_then_else(
                productivity_of_investment_in_gas_exploration() == 0,
                lambda: 0,
                lambda: 1
                / productivity_of_investment_in_gas_exploration()
                * toe_per_mtoe(),
            ),
        )
    )


@component.add(
    name="Unit Cost of Gas Production",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "productivity_of_investment_in_gas_production": 1,
        "toe_per_mtoe": 1,
        "carbon_price": 1,
        "climate_policy_scenario": 1,
        "co2_intensity_of_fuels": 1,
    },
)
def unit_cost_of_gas_production():
    """
    Unit cost of gas production.
    """
    return (
        1 / productivity_of_investment_in_gas_production() * toe_per_mtoe()
        + climate_policy_scenario()
        * float(co2_intensity_of_fuels().loc["Gas"])
        * carbon_price()
    )


@component.add(
    name="URG S",
    units="Billion Cubic Meters/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def urg_s():
    return 3400


@component.add(
    name="URG Var S",
    units="Billion Cubic Meters/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_urg_var_s": 1},
    other_deps={
        "_smooth_urg_var_s": {
            "initial": {"urg_s": 1, "time": 1},
            "step": {"urg_s": 1, "time": 1},
        }
    },
)
def urg_var_s():
    return 3400 + _smooth_urg_var_s()


_smooth_urg_var_s = Smooth(
    lambda: step(__data["time"], urg_s() - 3400, 2020),
    lambda: 1,
    lambda: step(__data["time"], urg_s() - 3400, 2020),
    lambda: 1,
    "_smooth_urg_var_s",
)
