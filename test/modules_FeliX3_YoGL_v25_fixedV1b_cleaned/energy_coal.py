"""
Module energy_coal
Translated using PySD version 3.14.3
"""

@component.add(
    name="Adjustment for Identified Coal Resource",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "required_identified_coal_resources": 1,
        "identified_coal_resources": 1,
        "identified_coal_resources_adjustment_time": 1,
    },
)
def adjustment_for_identified_coal_resource():
    """
    Adjustment of Identified Coal Resource to the desired level over a specified adjustment time.
    """
    return (
        required_identified_coal_resources() - identified_coal_resources()
    ) / identified_coal_resources_adjustment_time()


@component.add(
    name="Average Coal Production",
    units="Mtoe/Year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_average_coal_production": 1},
    other_deps={
        "_integ_average_coal_production": {
            "initial": {"init_average_coal_production": 1},
            "step": {"change_in_average_coal_production": 1},
        }
    },
)
def average_coal_production():
    """
    Average total coal production per year.
    """
    return _integ_average_coal_production()


_integ_average_coal_production = Integ(
    lambda: change_in_average_coal_production(),
    lambda: init_average_coal_production(),
    "_integ_average_coal_production",
)


@component.add(
    name="Carbon Price",
    units="$/tCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "carbon_price_slope": 1,
        "climate_action_year": 1,
        "carbon_price_finish": 1,
        "time": 1,
    },
)
def carbon_price():
    return ramp(
        __data["time"],
        carbon_price_slope(),
        climate_action_year(),
        carbon_price_finish(),
    )


@component.add(
    name="Carbon Price Finish",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def carbon_price_finish():
    return 2100


@component.add(
    name="Carbon Price Slope",
    units="$/tCO2/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def carbon_price_slope():
    return 5


@component.add(name="CDR S", units="Year", comp_type="Constant", comp_subtype="Normal")
def cdr_s():
    return 6


@component.add(
    name="CDR Var S",
    units="$",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_cdr_var_s": 1},
    other_deps={
        "_smooth_cdr_var_s": {
            "initial": {"cdr_s": 1, "time": 1},
            "step": {"cdr_s": 1, "time": 1},
        }
    },
)
def cdr_var_s():
    return 6 + _smooth_cdr_var_s()


_smooth_cdr_var_s = Smooth(
    lambda: step(__data["time"], cdr_s() - 6, 2020),
    lambda: 1,
    lambda: step(__data["time"], cdr_s() - 6, 2020),
    lambda: 1,
    "_smooth_cdr_var_s",
)


@component.add(
    name="Change in Average Coal Production",
    units="Mtoe/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "coal_production": 1,
        "average_coal_production": 1,
        "time_to_average_coal_production": 1,
    },
)
def change_in_average_coal_production():
    """
    Change in Average Coal Production.
    """
    return (
        coal_production() - average_coal_production()
    ) / time_to_average_coal_production()


@component.add(
    name="Change in Coal Productivity of Investment",
    units="toe/(Year*$)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "productivity_of_investment_in_coal_exploration": 1,
        "coal_productivity_of_investment": 1,
        "coal_production_coverage": 1,
    },
)
def change_in_coal_productivity_of_investment():
    """
    Change in Coal Productivity of Investment.
    """
    return (
        productivity_of_investment_in_coal_exploration()
        - coal_productivity_of_investment()
    ) / coal_production_coverage()


@component.add(
    name="Change in Effective Investment in Coal Exploration",
    units="$/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_coal_exploration": 1,
        "effective_investment_in_coal_exploration": 1,
        "investment_in_coal_exploration_delay": 1,
    },
)
def change_in_effective_investment_in_coal_exploration():
    """
    Change in Effective Investment in Coal Exploration.
    """
    return (
        investment_in_coal_exploration() - effective_investment_in_coal_exploration()
    ) / investment_in_coal_exploration_delay()


@component.add(
    name="Change in Effective Investment in Coal Production",
    units="$/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_coal_production": 1,
        "effective_investment_in_coal_production": 1,
        "investment_in_coal_production_delay": 1,
    },
)
def change_in_effective_investment_in_coal_production():
    """
    Change in Effective Investment in Coal Production.
    """
    return (
        investment_in_coal_production() - effective_investment_in_coal_production()
    ) / investment_in_coal_production_delay()


@component.add(
    name="CO2 Intensity of Fuels",
    units="tCO2/Mtoe",
    subscripts=["Fossil Fuels"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def co2_intensity_of_fuels():
    """
    Coal: 220 (Pounds of CO2 emitted per million British thermal units for coal) * 0.000453592 (pound to ton) / 0.025 (milltion British thermal units to toe) * 1e+6 (toe to Mtoe) Gas: 117 (Pounds of CO2 emitted per million British thermal units for coal) * 0.000453592 (pound to ton) / 0.025 (milltion British thermal units to toe) * 1e+6 (toe to Mtoe) Oil: 160 (Pounds of CO2 emitted per million British thermal units for coal) * 0.000453592 (pound to ton) / 0.025 (milltion British thermal units to toe) * 1e+6 (toe to Mtoe) Data from EIA: https://www.eia.gov/tools/faqs/faq.php?id=73&t=11
    """
    value = xr.DataArray(
        np.nan, {"Fossil Fuels": _subscript_dict["Fossil Fuels"]}, ["Fossil Fuels"]
    )
    value.loc[["Coal"]] = 220 * (0.000453592 / 0.025) * 1000000.0
    value.loc[["Gas"]] = 117 * (0.000453592 / 0.025) * 1000000.0
    value.loc[["Oil"]] = 160 * (0.000453592 / 0.025) * 1000000.0
    return value


@component.add(
    name="Coal Cost",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"unit_cost_of_coal_exploration": 1, "unit_cost_of_coal_production": 1},
)
def coal_cost():
    """
    Cost of unit coal resources as a sum of unit exploration and production costs.
    """
    return unit_cost_of_coal_exploration() + unit_cost_of_coal_production()


@component.add(
    name="Coal Demand to Supply Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_coal_demand": 1, "potential_coal_production": 1},
)
def coal_demand_to_supply_ratio():
    """
    Coal Demand to Supply Ratio.
    """
    return total_coal_demand() / potential_coal_production()


@component.add(
    name="Coal Desired Gross Margin",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def coal_desired_gross_margin():
    """
    Desired Gross Margin per unit coal resources.
    """
    return 0.2


@component.add(
    name="Coal Discovery and Recovery Technology Development Time Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def coal_discovery_and_recovery_technology_development_time_variation():
    return 6


@component.add(
    name="Coal Discovery Technology Development Time",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "cdr_var_s": 1,
        "_smooth_coal_discovery_technology_development_time": 1,
    },
    other_deps={
        "_smooth_coal_discovery_technology_development_time": {
            "initial": {
                "coal_discovery_and_recovery_technology_development_time_variation": 1,
                "cdr_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "coal_discovery_and_recovery_technology_development_time_variation": 1,
                "cdr_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def coal_discovery_technology_development_time():
    """
    Average time required to turn investments into concrete coal discovery developments.
    """
    return cdr_var_s() + _smooth_coal_discovery_technology_development_time()


_smooth_coal_discovery_technology_development_time = Smooth(
    lambda: step(
        __data["time"],
        coal_discovery_and_recovery_technology_development_time_variation()
        - cdr_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        coal_discovery_and_recovery_technology_development_time_variation()
        - cdr_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_coal_discovery_technology_development_time",
)


@component.add(
    name="Coal Exploration",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"coal_exploration_rate": 1},
)
def coal_exploration():
    """
    Coal resources discovery rate.
    """
    return float(np.maximum(coal_exploration_rate(), 0))


@component.add(
    name="Coal Exploration Rate",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_coal_exploration_rate": 1, "potential_coal_exploration": 1},
)
def coal_exploration_rate():
    """
    Coal Exploration Rate accounting for potential and desired coal exploration rates.
    """
    return float(
        np.minimum(desired_coal_exploration_rate(), potential_coal_exploration())
    )


@component.add(
    name="Coal Fraction Discoverable",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "mincfd": 2,
        "ratio_of_coal_fraction_discoverable_to_undiscoverable": 2,
        "maxcfd": 1,
    },
)
def coal_fraction_discoverable():
    """
    Percentage of coal resources that can be still explored due to current state of discovery technology.
    """
    return mincfd() + (maxcfd() - mincfd()) * (
        ratio_of_coal_fraction_discoverable_to_undiscoverable()
        / (ratio_of_coal_fraction_discoverable_to_undiscoverable() + 1)
    )


@component.add(
    name="Coal Fraction Recoverable",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "mincfr": 2,
        "maxcfr": 1,
        "ratio_of_coal_fraction_recoverable_to_unrecoverable": 2,
    },
)
def coal_fraction_recoverable():
    """
    Percentage of coal resources that can be produced due to current state of recovery technology.
    """
    return mincfr() + (maxcfr() - mincfr()) * (
        ratio_of_coal_fraction_recoverable_to_unrecoverable()
        / (ratio_of_coal_fraction_recoverable_to_unrecoverable() + 1)
    )


@component.add(
    name="Coal Gross Margin",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"coal_price": 1, "coal_cost": 2},
)
def coal_gross_margin():
    """
    Actual coal gross margin.
    """
    return (coal_price() - coal_cost()) / coal_cost()


@component.add(
    name="Coal Price",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "indicated_coal_price": 1,
        "effect_of_coal_demand_and_supply_on_price": 1,
    },
)
def coal_price():
    """
    Actual coal price accounting for indicated coal price and effect of demand and supply.
    """
    return indicated_coal_price() * effect_of_coal_demand_and_supply_on_price()


@component.add(
    name="Coal Price per Ton",
    units="$/Ton",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"coal_price": 1, "mtoe_per_ton": 1},
)
def coal_price_per_ton():
    """
    Actual Coal Price per Ton.
    """
    return coal_price() * mtoe_per_ton()


@component.add(
    name="Coal Production",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"coal_production_rate": 1},
)
def coal_production():
    """
    Total coal energy production per year. Source of historical data: International Energy Agency – Key World Energy Statistics 2007; BP Statistical Review of World Energy June 2008
    """
    return coal_production_rate()


@component.add(
    name="Coal Production Coverage",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"identified_coal_resources": 1, "average_coal_production": 1},
)
def coal_production_coverage():
    """
    Ratio indicating coal coverage in years for discovered resources and at the current average coal production.
    """
    return identified_coal_resources() / average_coal_production()


@component.add(
    name="Coal Production Indicator",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mtoe_into_ej": 1, "coal_production": 1},
)
def coal_production_indicator():
    return mtoe_into_ej() * coal_production()


@component.add(
    name="Coal Production Rate",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_coal_demand": 1, "potential_coal_production": 1},
)
def coal_production_rate():
    """
    Total coal energy production per year due to available resources, developments in production technology and coal energy demand.
    """
    return float(np.minimum(total_coal_demand(), potential_coal_production()))


@component.add(
    name="Coal Productivity of Investment",
    units="toe/$",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_coal_productivity_of_investment": 1},
    other_deps={
        "_integ_coal_productivity_of_investment": {
            "initial": {"init_cpi": 1},
            "step": {"change_in_coal_productivity_of_investment": 1},
        }
    },
)
def coal_productivity_of_investment():
    """
    Factor indicating productivity of investments in coal production.
    """
    return _integ_coal_productivity_of_investment()


_integ_coal_productivity_of_investment = Integ(
    lambda: change_in_coal_productivity_of_investment(),
    lambda: init_cpi(),
    "_integ_coal_productivity_of_investment",
)


@component.add(
    name="Coal Recovery Technology Development Time",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"cdr_var_s": 1, "_smooth_coal_recovery_technology_development_time": 1},
    other_deps={
        "_smooth_coal_recovery_technology_development_time": {
            "initial": {
                "coal_discovery_and_recovery_technology_development_time_variation": 1,
                "cdr_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "coal_discovery_and_recovery_technology_development_time_variation": 1,
                "cdr_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def coal_recovery_technology_development_time():
    """
    Average time required to turn investments into concrete coal recovery developments.
    """
    return cdr_var_s() + _smooth_coal_recovery_technology_development_time()


_smooth_coal_recovery_technology_development_time = Smooth(
    lambda: step(
        __data["time"],
        coal_discovery_and_recovery_technology_development_time_variation()
        - cdr_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        coal_discovery_and_recovery_technology_development_time_variation()
        - cdr_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_coal_recovery_technology_development_time",
)


@component.add(
    name="Coal Revenue",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"coal_price": 1, "average_coal_production": 1},
)
def coal_revenue():
    """
    Total revenue in coal market.
    """
    return coal_price() * average_coal_production()


@component.add(
    name="Coal Shortage",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_coal_demand": 1, "coal_production": 1},
)
def coal_shortage():
    """
    Difference between demand and the coal production rate.
    """
    return total_coal_demand() - coal_production()


@component.add(
    name="Cumulative Additions to Coal Production",
    units="Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"identified_coal_resources": 1, "cumulative_coal_production": 1},
)
def cumulative_additions_to_coal_production():
    """
    Identified and already produced coal resources.
    """
    return identified_coal_resources() + cumulative_coal_production()


@component.add(
    name="Cumulative Coal Production",
    units="Mtoe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_coal_production": 1},
    other_deps={
        "_integ_cumulative_coal_production": {
            "initial": {"init_ccpn": 1},
            "step": {"coal_production": 1},
        }
    },
)
def cumulative_coal_production():
    """
    Cumulative Coal resources that has been produced.
    """
    return _integ_cumulative_coal_production()


_integ_cumulative_coal_production = Integ(
    lambda: coal_production(), lambda: init_ccpn(), "_integ_cumulative_coal_production"
)


@component.add(
    name="Delay Time IRCFDU",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"coal_discovery_technology_development_time": 1},
)
def delay_time_ircfdu():
    return coal_discovery_technology_development_time() / 3


@component.add(
    name="Delay Time IRCFRU",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"coal_recovery_technology_development_time": 1},
)
def delay_time_ircfru():
    return coal_recovery_technology_development_time() / 3


@component.add(
    name="Desired Coal Exploration Rate",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"adjustment_for_identified_coal_resource": 1, "coal_production": 1},
)
def desired_coal_exploration_rate():
    """
    Desired Coal exploration rate due to Total Coal Demand and Identified Coal Resources safety coverage.
    """
    return float(
        np.maximum(0, adjustment_for_identified_coal_resource() + coal_production())
    )


@component.add(
    name="Desired Investment in Coal Exploration",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_coal_exploration_rate": 1, "unit_cost_of_coal_exploration": 1},
)
def desired_investment_in_coal_exploration():
    """
    Desired amount of resources that need to be invested in order to secure desired coal exploration.
    """
    return desired_coal_exploration_rate() * unit_cost_of_coal_exploration()


@component.add(
    name="Desired Investment in Coal Production",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_coal_production_from_resources": 1,
        "total_coal_demand": 1,
        "productivity_of_investment_in_coal_production": 1,
        "toe_per_mtoe": 1,
    },
)
def desired_investment_in_coal_production():
    """
    Desired Investment in Coal Production due to Total Coal Demand and Productivity of Investment in Coal Production.
    """
    return (
        float(
            np.minimum(potential_coal_production_from_resources(), total_coal_demand())
        )
        / productivity_of_investment_in_coal_production()
        * toe_per_mtoe()
    )


@component.add(
    name="Effect of Coal Demand and Supply on Price",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sc_init": 1,
        "total_coal_demand": 1,
        "sensitivity_of_coal_price_to_supply_and_demand": 1,
        "potential_coal_production": 1,
    },
)
def effect_of_coal_demand_and_supply_on_price():
    """
    Effect of Coal Demand and Supply ratio on actual coal price.
    """
    return (
        sc_init()
        * (total_coal_demand() / potential_coal_production())
        ** sensitivity_of_coal_price_to_supply_and_demand()
    )


@component.add(
    name="Effect of Technology on Coal Discoveries",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_coal_discoverable_resources": 1, "init_ucrn": 1},
)
def effect_of_technology_on_coal_discoveries():
    """
    Impact of technology development on coal exploration taking into account remaining undiscovered coal resources (the less remaining undiscovered coal resources the more expensive it is to discover them).
    """
    return total_coal_discoverable_resources() / init_ucrn()


@component.add(
    name="Effective Investment in Coal Exploration",
    units="$/Year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_effective_investment_in_coal_exploration": 1},
    other_deps={
        "_integ_effective_investment_in_coal_exploration": {
            "initial": {"init_eice": 1},
            "step": {"change_in_effective_investment_in_coal_exploration": 1},
        }
    },
)
def effective_investment_in_coal_exploration():
    """
    Effective investments dedicated for coal resources exploration.
    """
    return _integ_effective_investment_in_coal_exploration()


_integ_effective_investment_in_coal_exploration = Integ(
    lambda: change_in_effective_investment_in_coal_exploration(),
    lambda: init_eice(),
    "_integ_effective_investment_in_coal_exploration",
)


@component.add(
    name="Effective Investment in Coal Production",
    units="$/Year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_effective_investment_in_coal_production": 1},
    other_deps={
        "_integ_effective_investment_in_coal_production": {
            "initial": {"init_eicp": 1},
            "step": {"change_in_effective_investment_in_coal_production": 1},
        }
    },
)
def effective_investment_in_coal_production():
    """
    Effective investments dedicated for coal resources production.
    """
    return _integ_effective_investment_in_coal_production()


_integ_effective_investment_in_coal_production = Integ(
    lambda: change_in_effective_investment_in_coal_production(),
    lambda: init_eicp(),
    "_integ_effective_investment_in_coal_production",
)


@component.add(
    name="Effectiveness IRCFDU",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effectiveness_of_investment_in_coal_discovery_technology": 1,
        "investment_in_coal_discovery_technology": 1,
    },
)
def effectiveness_ircfdu():
    return (
        effectiveness_of_investment_in_coal_discovery_technology()
        * investment_in_coal_discovery_technology()
    )


@component.add(
    name="Effectiveness IRCFRU",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_coal_recovery_technology": 1,
        "effectiveness_of_investment_in_coal_recovery_technology": 1,
    },
)
def effectiveness_ircfru():
    return (
        investment_in_coal_recovery_technology()
        * effectiveness_of_investment_in_coal_recovery_technology()
    )


@component.add(
    name="Effectiveness of Investment in Coal Discovery Technology",
    units="1/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effectiveness_of_investment_in_coal_discovery_technology_variation": 1,
        "time": 1,
    },
)
def effectiveness_of_investment_in_coal_discovery_technology():
    """
    Effectiveness of resources dedicated to coal discovery technology development.
    """
    return 1.62e-11 + step(
        __data["time"],
        effectiveness_of_investment_in_coal_discovery_technology_variation() - 1.62e-11,
        2020,
    )


@component.add(
    name="Effectiveness of Investment in Coal Discovery Technology Variation",
    units="1/$",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effectiveness_of_investment_in_coal_discovery_technology_variation():
    """
    Effectiveness of resources dedicated to coal discovery technology development.
    """
    return 1.62e-11


@component.add(
    name="Effectiveness of Investment in Coal Recovery Technology",
    units="1/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effectiveness_of_investment_in_coal_recovery_technology_variation": 1,
        "time": 1,
    },
)
def effectiveness_of_investment_in_coal_recovery_technology():
    """
    Effectiveness of resources dedicated to coal recovery technology development.
    """
    return 1.3e-12 + step(
        __data["time"],
        effectiveness_of_investment_in_coal_recovery_technology_variation() - 1.3e-12,
        2020,
    )


@component.add(
    name="Effectiveness of Investment in Coal Recovery Technology Variation",
    units="1/$",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effectiveness_of_investment_in_coal_recovery_technology_variation():
    """
    Effectiveness of resources dedicated to coal recovery technology development.
    """
    return 1.3e-12


@component.add(name="FC S", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def fc_s():
    """
    Percentage of total coal sector revenue dedicated to exploration and production technology development.
    """
    return 0.03


@component.add(
    name="FC Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_fc_var_s": 1},
    other_deps={
        "_smooth_fc_var_s": {
            "initial": {"fc_s": 1, "time": 1},
            "step": {"fc_s": 1, "time": 1},
        }
    },
)
def fc_var_s():
    """
    Percentage of total coal sector revenue dedicated to exploration and production technology development.
    """
    return 0.03 + _smooth_fc_var_s()


_smooth_fc_var_s = Smooth(
    lambda: step(__data["time"], fc_s() - 0.03, 2020),
    lambda: 1,
    lambda: step(__data["time"], fc_s() - 0.03, 2020),
    lambda: 1,
    "_smooth_fc_var_s",
)


@component.add(
    name="Fraction Invested in Coal Discovery Technology",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"coal_fraction_discoverable": 1, "table_for_ficdt": 1},
)
def fraction_invested_in_coal_discovery_technology():
    """
    Fraction of investments in coal technology dedicated to discovery technology.
    """
    return table_for_ficdt(coal_fraction_discoverable())


@component.add(
    name="Fraction of Coal Revenues Invested in Technology",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "fc_var_s": 1,
        "_smooth_fraction_of_coal_revenues_invested_in_technology": 1,
    },
    other_deps={
        "_smooth_fraction_of_coal_revenues_invested_in_technology": {
            "initial": {
                "fraction_of_coal_revenues_invested_in_technology_variation": 1,
                "fc_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "fraction_of_coal_revenues_invested_in_technology_variation": 1,
                "fc_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def fraction_of_coal_revenues_invested_in_technology():
    """
    Percentage of total coal sector revenue dedicated to exploration and production technology development.
    """
    return fc_var_s() + _smooth_fraction_of_coal_revenues_invested_in_technology()


_smooth_fraction_of_coal_revenues_invested_in_technology = Smooth(
    lambda: step(
        __data["time"],
        fraction_of_coal_revenues_invested_in_technology_variation() - fc_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        fraction_of_coal_revenues_invested_in_technology_variation() - fc_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_fraction_of_coal_revenues_invested_in_technology",
)


@component.add(
    name="Fraction of Coal Revenues Invested in Technology Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraction_of_coal_revenues_invested_in_technology_variation():
    """
    Percentage of total coal sector revenue dedicated to exploration and production technology development.
    """
    return 0.03


@component.add(name="IC S", units="Year", comp_type="Constant", comp_subtype="Normal")
def ic_s():
    return 5


@component.add(
    name="IC Var S",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_ic_var_s": 1},
    other_deps={
        "_smooth_ic_var_s": {
            "initial": {"ic_s": 1, "time": 1},
            "step": {"ic_s": 1, "time": 1},
        }
    },
)
def ic_var_s():
    return 5 + _smooth_ic_var_s()


_smooth_ic_var_s = Smooth(
    lambda: step(__data["time"], ic_s() - 5, 2020),
    lambda: 1,
    lambda: step(__data["time"], ic_s() - 5, 2020),
    lambda: 1,
    "_smooth_ic_var_s",
)


@component.add(
    name="Identified Coal Resources",
    units="Mtoe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_identified_coal_resources": 1},
    other_deps={
        "_integ_identified_coal_resources": {
            "initial": {
                "total_coal_demand": 1,
                "normal_coal_production_ratio": 1,
                "cumulative_coal_production": 1,
                "coal_fraction_recoverable": 2,
            },
            "step": {"coal_exploration": 1, "coal_production": 1},
        }
    },
)
def identified_coal_resources():
    """
    Coal Resources discovered thanks to developments in exploration technology.
    """
    return _integ_identified_coal_resources()


_integ_identified_coal_resources = Integ(
    lambda: coal_exploration() - coal_production(),
    lambda: (
        total_coal_demand() * normal_coal_production_ratio()
        + cumulative_coal_production() * (1 - coal_fraction_recoverable())
    )
    / coal_fraction_recoverable(),
    "_integ_identified_coal_resources",
)


@component.add(
    name="Identified Coal Resources Adjustment Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def identified_coal_resources_adjustment_time():
    """
    Time to adjust Identified Oil Coal Resource to the desired level.
    """
    return 10


@component.add(
    name="Increase in Ratio of Coal Fraction Discoverable to Undiscoverable",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ircfdulv3": 1},
)
def increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable():
    """
    Increase in Ratio of Coal Fraction Discoverable to Undiscoverable due to investments in discovery technology and their productivity.
    """
    return outflow_ircfdulv3()


@component.add(
    name="Increase in Ratio of Coal Fraction Discoverable to Undiscoverable LV1",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv1": 1
    },
    other_deps={
        "_integ_increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv1": {
            "initial": {
                "increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv3": 1
            },
            "step": {"inflow_ircfdulv1": 1, "outflow_ircfdulv1": 1},
        }
    },
)
def increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv1():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return (
        _integ_increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv1()
    )


_integ_increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv1 = Integ(
    lambda: inflow_ircfdulv1() - outflow_ircfdulv1(),
    lambda: increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv3(),
    "_integ_increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv1",
)


@component.add(
    name="Increase in Ratio of Coal Fraction Discoverable to Undiscoverable LV2",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv2": 1
    },
    other_deps={
        "_integ_increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv2": {
            "initial": {
                "increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv3": 1
            },
            "step": {"inflow_ircfdulv2": 1, "outflow_ircfdulv2": 1},
        }
    },
)
def increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv2():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return (
        _integ_increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv2()
    )


_integ_increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv2 = Integ(
    lambda: inflow_ircfdulv2() - outflow_ircfdulv2(),
    lambda: increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv3(),
    "_integ_increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv2",
)


@component.add(
    name="Increase in Ratio of Coal Fraction Discoverable to Undiscoverable LV3",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv3": 1
    },
    other_deps={
        "_integ_increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv3": {
            "initial": {"effectiveness_ircfdu": 1, "delay_time_ircfdu": 1},
            "step": {"inflow_ircfdulv3": 1, "outflow_ircfdulv3": 1},
        }
    },
)
def increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv3():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return (
        _integ_increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv3()
    )


_integ_increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv3 = Integ(
    lambda: inflow_ircfdulv3() - outflow_ircfdulv3(),
    lambda: effectiveness_ircfdu() * delay_time_ircfdu(),
    "_integ_increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv3",
)


@component.add(
    name="Increase in Ratio of Coal Fraction Recoverable to Unrecoverable",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ircfrulv3": 1},
)
def increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable():
    """
    Increase in Ratio of Coal Fraction Recoverable to Unrecoverable due to investments in recovery technology and their productivity.
    """
    return outflow_ircfrulv3()


@component.add(
    name="Increase in Ratio of Coal Fraction Recoverable to Unrecoverable LV1",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv1": 1
    },
    other_deps={
        "_integ_increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv1": {
            "initial": {
                "increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv3": 1
            },
            "step": {"inflow_ircfrulv1": 1, "outflow_ircfrulv1": 1},
        }
    },
)
def increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv1():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv1()


_integ_increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv1 = Integ(
    lambda: inflow_ircfrulv1() - outflow_ircfrulv1(),
    lambda: increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv3(),
    "_integ_increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv1",
)


@component.add(
    name="Increase in Ratio of Coal Fraction Recoverable to Unrecoverable LV2",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv2": 1
    },
    other_deps={
        "_integ_increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv2": {
            "initial": {
                "increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv3": 1
            },
            "step": {"inflow_ircfrulv2": 1, "outflow_ircfrulv2": 1},
        }
    },
)
def increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv2():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv2()


_integ_increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv2 = Integ(
    lambda: inflow_ircfrulv2() - outflow_ircfrulv2(),
    lambda: increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv3(),
    "_integ_increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv2",
)


@component.add(
    name="Increase in Ratio of Coal Fraction Recoverable to Unrecoverable LV3",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv3": 1
    },
    other_deps={
        "_integ_increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv3": {
            "initial": {"effectiveness_ircfru": 1, "delay_time_ircfru": 1},
            "step": {"inflow_ircfrulv3": 1, "outflow_ircfrulv3": 1},
        }
    },
)
def increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv3():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv3()


_integ_increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv3 = Integ(
    lambda: inflow_ircfrulv3() - outflow_ircfrulv3(),
    lambda: effectiveness_ircfru() * delay_time_ircfru(),
    "_integ_increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv3",
)


@component.add(
    name="Indicated Coal Price",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"coal_cost": 1, "coal_desired_gross_margin": 1},
)
def indicated_coal_price():
    """
    Indicated coal price accounting for exploration and production cost and gross margin.
    """
    return coal_cost() * (1 + coal_desired_gross_margin())


@component.add(
    name="Inflow IRCFDULV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effectiveness_ircfdu": 1},
)
def inflow_ircfdulv1():
    return effectiveness_ircfdu()


@component.add(
    name="Inflow IRCFDULV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ircfdulv1": 1},
)
def inflow_ircfdulv2():
    return outflow_ircfdulv1()


@component.add(
    name="Inflow IRCFDULV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ircfdulv2": 1},
)
def inflow_ircfdulv3():
    return outflow_ircfdulv2()


@component.add(
    name="Inflow IRCFRULV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effectiveness_ircfru": 1},
)
def inflow_ircfrulv1():
    return effectiveness_ircfru()


@component.add(
    name="Inflow IRCFRULV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ircfrulv1": 1},
)
def inflow_ircfrulv2():
    return outflow_ircfrulv1()


@component.add(
    name="Inflow IRCFRULV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ircfrulv2": 1},
)
def inflow_ircfrulv3():
    return outflow_ircfrulv2()


@component.add(
    name="INIT Average Coal Production", comp_type="Constant", comp_subtype="Normal"
)
def init_average_coal_production():
    return 191.404


@component.add(
    name="INIT CCPN", units="Mtoe", comp_type="Constant", comp_subtype="Normal"
)
def init_ccpn():
    """
    Cumulative Coal resources for 1900.
    """
    return 37630


@component.add(name="INIT CPI", comp_type="Constant", comp_subtype="Normal")
def init_cpi():
    return 0.00188537


@component.add(name="INIT EICE", comp_type="Constant", comp_subtype="Normal")
def init_eice():
    """
    Effective Investment in Coal Exploration
    """
    return 101518000000.0


@component.add(name="INIT EICP", comp_type="Constant", comp_subtype="Normal")
def init_eicp():
    """
    Effective Investment in Coal Production
    """
    return 10152100000.0


@component.add(
    name="INIT RCDU", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def init_rcdu():
    """
    Initial Ratio of Coal Fraction Discoverable to Undiscoverable.
    """
    return 0


@component.add(
    name="INIT RCRU", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def init_rcru():
    """
    Initial Ratio of Coal Fraction Recoverable to Unrecoverable.
    """
    return 0


@component.add(
    name="INIT UCRN",
    units="Mtoe",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"uc_var_s": 1, "_smooth_init_ucrn": 1},
    other_deps={
        "_smooth_init_ucrn": {
            "initial": {
                "undiscovered_coal_resources_variation": 1,
                "uc_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "undiscovered_coal_resources_variation": 1,
                "uc_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_production_variation_time": 1,
            },
        }
    },
)
def init_ucrn():
    """
    Initial amount of Undiscovered Coal Resources.
    """
    return uc_var_s() + _smooth_init_ucrn()


_smooth_init_ucrn = Smooth(
    lambda: step(
        __data["time"],
        undiscovered_coal_resources_variation() - uc_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_production_variation_time(),
    lambda: step(
        __data["time"],
        undiscovered_coal_resources_variation() - uc_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_init_ucrn",
)


@component.add(
    name="Investment in Coal Discovery Technology",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_coal_technology": 1,
        "fraction_invested_in_coal_discovery_technology": 1,
    },
)
def investment_in_coal_discovery_technology():
    """
    Total investments in coal exploration technology.
    """
    return (
        investment_in_coal_technology()
        * fraction_invested_in_coal_discovery_technology()
    )


@component.add(
    name="Investment in Coal Exploration",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_investment_in_coal_exploration": 1},
)
def investment_in_coal_exploration():
    """
    Amount of resources dedicated to coal exploration.
    """
    return desired_investment_in_coal_exploration()


@component.add(
    name="Investment in Coal Exploration and Production Delay Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def investment_in_coal_exploration_and_production_delay_variation():
    return 5


@component.add(
    name="Investment in Coal Exploration Delay",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"ic_var_s": 1, "_smooth_investment_in_coal_exploration_delay": 1},
    other_deps={
        "_smooth_investment_in_coal_exploration_delay": {
            "initial": {
                "investment_in_coal_exploration_and_production_delay_variation": 1,
                "ic_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "investment_in_coal_exploration_and_production_delay_variation": 1,
                "ic_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def investment_in_coal_exploration_delay():
    """
    Time delay to make investments in coal exploration effective.
    """
    return ic_var_s() + _smooth_investment_in_coal_exploration_delay()


_smooth_investment_in_coal_exploration_delay = Smooth(
    lambda: step(
        __data["time"],
        investment_in_coal_exploration_and_production_delay_variation() - ic_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        investment_in_coal_exploration_and_production_delay_variation() - ic_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_investment_in_coal_exploration_delay",
)


@component.add(
    name="Investment in Coal Production",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_investment_in_coal_production": 1},
)
def investment_in_coal_production():
    """
    Amount of resources dedicated to coal production.
    """
    return desired_investment_in_coal_production()


@component.add(
    name="Investment in Coal Production Delay",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"ic_var_s": 1, "_smooth_investment_in_coal_production_delay": 1},
    other_deps={
        "_smooth_investment_in_coal_production_delay": {
            "initial": {
                "investment_in_coal_exploration_and_production_delay_variation": 1,
                "ic_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "investment_in_coal_exploration_and_production_delay_variation": 1,
                "ic_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def investment_in_coal_production_delay():
    """
    Time delay to make investments in coal production effective.
    """
    return ic_var_s() + _smooth_investment_in_coal_production_delay()


_smooth_investment_in_coal_production_delay = Smooth(
    lambda: step(
        __data["time"],
        investment_in_coal_exploration_and_production_delay_variation() - ic_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        investment_in_coal_exploration_and_production_delay_variation() - ic_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_investment_in_coal_production_delay",
)


@component.add(
    name="Investment in Coal Recovery Technology",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_coal_technology": 1,
        "fraction_invested_in_coal_discovery_technology": 1,
    },
)
def investment_in_coal_recovery_technology():
    """
    Total investments in coal production technology.
    """
    return investment_in_coal_technology() * (
        1 - fraction_invested_in_coal_discovery_technology()
    )


@component.add(
    name="Investment in Coal Technology",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fraction_of_coal_revenues_invested_in_technology": 1,
        "coal_revenue": 1,
    },
)
def investment_in_coal_technology():
    """
    Investments in development of coal exploration and production technology.
    """
    return fraction_of_coal_revenues_invested_in_technology() * coal_revenue()


@component.add(
    name="Max Unit Cost of Coal Exploration",
    units="$/Mtoe",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"mfc_var_s": 1, "_smooth_max_unit_cost_of_coal_exploration": 1},
    other_deps={
        "_smooth_max_unit_cost_of_coal_exploration": {
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
def max_unit_cost_of_coal_exploration():
    """
    Upper level limit for unit cost of coal exploration.
    """
    return mfc_var_s() + _smooth_max_unit_cost_of_coal_exploration()


_smooth_max_unit_cost_of_coal_exploration = Smooth(
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
    "_smooth_max_unit_cost_of_coal_exploration",
)


@component.add(
    name="Max Unit Cost of Fossil Fuel Exploration Variation",
    units="$/Mtoe",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_unit_cost_of_fossil_fuel_exploration_variation():
    return 1000000000.0


@component.add(name="MAXCFD", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def maxcfd():
    """
    Maximal possible percentage of coal resources to be discovered.
    """
    return 1


@component.add(name="MAXCFR", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def maxcfr():
    """
    Maximal possible percentage of coal resources to be recovered.
    """
    return 1


@component.add(
    name="MFC S", units="$/Mtoe", comp_type="Constant", comp_subtype="Normal"
)
def mfc_s():
    return 1000000000.0


@component.add(
    name="MFC Var S",
    units="$/Mtoe",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_mfc_var_s": 1},
    other_deps={
        "_smooth_mfc_var_s": {
            "initial": {"mfc_s": 1, "time": 1},
            "step": {"mfc_s": 1, "time": 1},
        }
    },
)
def mfc_var_s():
    return 1000000000.0 + _smooth_mfc_var_s()


_smooth_mfc_var_s = Smooth(
    lambda: step(__data["time"], mfc_s() - 1000000000.0, 2020),
    lambda: 1,
    lambda: step(__data["time"], mfc_s() - 1000000000.0, 2020),
    lambda: 1,
    "_smooth_mfc_var_s",
)


@component.add(name="MINCFD", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def mincfd():
    """
    Initial and minimal possible percentage of coal resources to be discovered.
    """
    return 0.5


@component.add(name="MINCFR", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def mincfr():
    """
    Initial and minimal possible percentage of coal resources to be recovered.
    """
    return 0.15


@component.add(
    name="Mtoe per Ton", units="Mtoe/Ton", comp_type="Constant", comp_subtype="Normal"
)
def mtoe_per_ton():
    """
    Coefficient to convert million tons of oil equivalent unit (Mtoe) into coal tons (Ton).
    """
    return 4.9e-07


@component.add(
    name="Normal Coal Production Ratio",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_coal_production_ratio():
    """
    Safety stock coverage as a number of years of the total coal demand the coal sector would like to maintain in identified coal resources. It secures the market against possibility of unforeseen variations in demand. It is also a stimulus for coal exploration.
    """
    return 10


@component.add(
    name="Outflow IRCFDULV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv1": 1,
        "delay_time_ircfdu": 1,
    },
)
def outflow_ircfdulv1():
    return (
        increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv1()
        / delay_time_ircfdu()
    )


@component.add(
    name="Outflow IRCFDULV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv2": 1,
        "delay_time_ircfdu": 1,
    },
)
def outflow_ircfdulv2():
    return (
        increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv2()
        / delay_time_ircfdu()
    )


@component.add(
    name="Outflow IRCFDULV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv3": 1,
        "delay_time_ircfdu": 1,
    },
)
def outflow_ircfdulv3():
    return (
        increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable_lv3()
        / delay_time_ircfdu()
    )


@component.add(
    name="Outflow IRCFRULV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv1": 1,
        "delay_time_ircfru": 1,
    },
)
def outflow_ircfrulv1():
    return (
        increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv1()
        / delay_time_ircfru()
    )


@component.add(
    name="Outflow IRCFRULV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv2": 1,
        "delay_time_ircfru": 1,
    },
)
def outflow_ircfrulv2():
    return (
        increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv2()
        / delay_time_ircfru()
    )


@component.add(
    name="Outflow IRCFRULV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv3": 1,
        "delay_time_ircfru": 1,
    },
)
def outflow_ircfrulv3():
    return (
        increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable_lv3()
        / delay_time_ircfru()
    )


@component.add(
    name="Potential Coal Exploration",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effective_investment_in_coal_exploration": 1,
        "productivity_of_investment_in_coal_exploration": 1,
        "toe_per_mtoe": 1,
    },
)
def potential_coal_exploration():
    """
    Potential Coal exploration due to available investments in coal resources discovery.
    """
    return (
        effective_investment_in_coal_exploration()
        * productivity_of_investment_in_coal_exploration()
        / toe_per_mtoe()
    )


@component.add(
    name="Potential Coal Production",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_coal_production_from_investment": 1,
        "potential_coal_production_from_resources": 1,
    },
)
def potential_coal_production():
    """
    Potential Coal Production due to available investments in coal resources recovery and recovery technology.
    """
    return float(
        np.minimum(
            potential_coal_production_from_investment(),
            potential_coal_production_from_resources(),
        )
    )


@component.add(
    name="Potential Coal Production from Investment",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "productivity_of_investment_in_coal_production": 1,
        "effective_investment_in_coal_production": 1,
        "toe_per_mtoe": 1,
    },
)
def potential_coal_production_from_investment():
    """
    Potential Coal Production due to available investments in coal resources recovery.
    """
    return (
        productivity_of_investment_in_coal_production()
        * effective_investment_in_coal_production()
        / toe_per_mtoe()
    )


@component.add(
    name="Potential Coal Production from Resources",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_coal_recoverable_resource_remaining": 1,
        "normal_coal_production_ratio": 1,
    },
)
def potential_coal_production_from_resources():
    """
    Potential Coal Production rate due to Total Coal Recoverable Resource Remaining adjusted by coal production safety coverage.
    """
    return total_coal_recoverable_resource_remaining() / normal_coal_production_ratio()


@component.add(
    name="Productivity of Investment in Coal Exploration",
    units="toe/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "relative_productivity_of_investment_in_coal_exploration": 1,
        "effect_of_technology_on_coal_discoveries": 1,
    },
)
def productivity_of_investment_in_coal_exploration():
    """
    Parameter indicating the amount of coal resources possible to be explored per unit investment spent.
    """
    return float(
        np.maximum(
            0,
            relative_productivity_of_investment_in_coal_exploration()
            * effect_of_technology_on_coal_discoveries(),
        )
    )


@component.add(
    name="Productivity of Investment in Coal Production",
    units="toe/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "relative_productivity_of_investment_in_coal_production_compared_to_exploration": 1,
        "coal_productivity_of_investment": 1,
    },
)
def productivity_of_investment_in_coal_production():
    """
    Parameter indicating the amount of coal resources possible to be recovered per unit investment spent.
    """
    return (
        relative_productivity_of_investment_in_coal_production_compared_to_exploration()
        * coal_productivity_of_investment()
    )


@component.add(
    name="Ratio of Coal Fraction Discoverable to Undiscoverable",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ratio_of_coal_fraction_discoverable_to_undiscoverable": 1},
    other_deps={
        "_integ_ratio_of_coal_fraction_discoverable_to_undiscoverable": {
            "initial": {"init_rcdu": 1},
            "step": {
                "increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable": 1
            },
        }
    },
)
def ratio_of_coal_fraction_discoverable_to_undiscoverable():
    """
    Ratio of Coal Fraction Discoverable to Undiscoverable increased due to investments in discovery technology and their productivity.
    """
    return _integ_ratio_of_coal_fraction_discoverable_to_undiscoverable()


_integ_ratio_of_coal_fraction_discoverable_to_undiscoverable = Integ(
    lambda: increase_in_ratio_of_coal_fraction_discoverable_to_undiscoverable(),
    lambda: init_rcdu(),
    "_integ_ratio_of_coal_fraction_discoverable_to_undiscoverable",
)


@component.add(
    name="Ratio of Coal Fraction Recoverable to Unrecoverable",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ratio_of_coal_fraction_recoverable_to_unrecoverable": 1},
    other_deps={
        "_integ_ratio_of_coal_fraction_recoverable_to_unrecoverable": {
            "initial": {"init_rcru": 1},
            "step": {
                "increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable": 1
            },
        }
    },
)
def ratio_of_coal_fraction_recoverable_to_unrecoverable():
    """
    Ratio of Coal Fraction Recoverable to Unrecoverable increased due to investments in recovery technology and their productivity.
    """
    return _integ_ratio_of_coal_fraction_recoverable_to_unrecoverable()


_integ_ratio_of_coal_fraction_recoverable_to_unrecoverable = Integ(
    lambda: increase_in_ratio_of_coal_fraction_recoverable_to_unrecoverable(),
    lambda: init_rcru(),
    "_integ_ratio_of_coal_fraction_recoverable_to_unrecoverable",
)


@component.add(
    name="Relative Productivity of Investment in Coal Exploration",
    units="toe/$",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "rpc_var_s": 1,
        "_smooth_relative_productivity_of_investment_in_coal_exploration": 1,
    },
    other_deps={
        "_smooth_relative_productivity_of_investment_in_coal_exploration": {
            "initial": {
                "relative_productivity_of_investment_in_coal_exploration_variation": 1,
                "rpc_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "relative_productivity_of_investment_in_coal_exploration_variation": 1,
                "rpc_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def relative_productivity_of_investment_in_coal_exploration():
    """
    Relative Productivity of Investment in Coal Exploration without taking into account remaining undiscovered coal resources and advances in exploration technologies.
    """
    return (
        rpc_var_s() + _smooth_relative_productivity_of_investment_in_coal_exploration()
    )


_smooth_relative_productivity_of_investment_in_coal_exploration = Smooth(
    lambda: step(
        __data["time"],
        relative_productivity_of_investment_in_coal_exploration_variation()
        - rpc_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        relative_productivity_of_investment_in_coal_exploration_variation()
        - rpc_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_relative_productivity_of_investment_in_coal_exploration",
)


@component.add(
    name="Relative Productivity of Investment in Coal Exploration Variation",
    units="toe/$",
    comp_type="Constant",
    comp_subtype="Normal",
)
def relative_productivity_of_investment_in_coal_exploration_variation():
    """
    Relative Productivity of Investment in Coal Exploration without taking into account remaining undiscovered coal resources and advances in exploration technologies.
    """
    return 0.5


@component.add(
    name="Relative Productivity of Investment in Coal Production Compared to Exploration",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "rpcpe_var_s": 1,
        "_smooth_relative_productivity_of_investment_in_coal_production_compared_to_exploration": 1,
    },
    other_deps={
        "_smooth_relative_productivity_of_investment_in_coal_production_compared_to_exploration": {
            "initial": {
                "relative_productivity_of_investment_in_coal_production_compared_to_exploration_variation": 1,
                "rpcpe_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "relative_productivity_of_investment_in_coal_production_compared_to_exploration_variation": 1,
                "rpcpe_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def relative_productivity_of_investment_in_coal_production_compared_to_exploration():
    """
    Relative Productivity of Investment in Coal Production as a multiplier of Productivity of Investment in Coal Exploration.
    """
    return (
        rpcpe_var_s()
        + _smooth_relative_productivity_of_investment_in_coal_production_compared_to_exploration()
    )


_smooth_relative_productivity_of_investment_in_coal_production_compared_to_exploration = Smooth(
    lambda: step(
        __data["time"],
        relative_productivity_of_investment_in_coal_production_compared_to_exploration_variation()
        - rpcpe_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        relative_productivity_of_investment_in_coal_production_compared_to_exploration_variation()
        - rpcpe_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_relative_productivity_of_investment_in_coal_production_compared_to_exploration",
)


@component.add(
    name="Relative Productivity of Investment in Coal Production Compared to Exploration Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def relative_productivity_of_investment_in_coal_production_compared_to_exploration_variation():
    return 10


@component.add(
    name="Required Identified Coal Resources",
    units="Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "identified_coal_resources": 1,
        "total_coal_recoverable_resource_remaining": 1,
        "total_coal_demand": 1,
        "normal_coal_production_ratio": 1,
    },
)
def required_identified_coal_resources():
    """
    The desired Identified Coal Resources level sought by the coal sector.
    """
    return (
        identified_coal_resources() / total_coal_recoverable_resource_remaining()
    ) * (normal_coal_production_ratio() * total_coal_demand())


@component.add(
    name="RPC S",
    units="toe/$",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def rpc_s():
    """
    Relative Productivity of Investment in Coal Exploration without taking into account remaining undiscovered coal resources and advances in exploration technologies.
    """
    return 0.5


@component.add(
    name="RPC Var S",
    units="toe/$",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_rpc_var_s": 1},
    other_deps={
        "_smooth_rpc_var_s": {
            "initial": {"rpc_s": 1, "time": 1},
            "step": {"rpc_s": 1, "time": 1},
        }
    },
)
def rpc_var_s():
    """
    Relative Productivity of Investment in Coal Exploration without taking into account remaining undiscovered coal resources and advances in exploration technologies.
    """
    return 0.5 + _smooth_rpc_var_s()


_smooth_rpc_var_s = Smooth(
    lambda: step(__data["time"], rpc_s() - 0.5, 2020),
    lambda: 1,
    lambda: step(__data["time"], rpc_s() - 0.5, 2020),
    lambda: 1,
    "_smooth_rpc_var_s",
)


@component.add(
    name="RPCPE S", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def rpcpe_s():
    return 10


@component.add(
    name="RPCPE Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_rpcpe_var_s": 1},
    other_deps={
        "_smooth_rpcpe_var_s": {
            "initial": {"rpcpe_s": 1, "time": 1},
            "step": {"rpcpe_s": 1, "time": 1},
        }
    },
)
def rpcpe_var_s():
    return 10 + _smooth_rpcpe_var_s()


_smooth_rpcpe_var_s = Smooth(
    lambda: step(__data["time"], rpcpe_s() - 10, 2020),
    lambda: 1,
    lambda: step(__data["time"], rpcpe_s() - 10, 2020),
    lambda: 1,
    "_smooth_rpcpe_var_s",
)


@component.add(
    name="SC Init", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def sc_init():
    return 2


@component.add(name="SCo S", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def sco_s():
    return 0.1


@component.add(
    name="SCo Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_sco_var_s": 1},
    other_deps={
        "_smooth_sco_var_s": {
            "initial": {"sco_s": 1, "time": 1},
            "step": {"sco_s": 1, "time": 1},
        }
    },
)
def sco_var_s():
    return 0.1 + _smooth_sco_var_s()


_smooth_sco_var_s = Smooth(
    lambda: step(__data["time"], sco_s() - 0.1, 2020),
    lambda: 1,
    lambda: step(__data["time"], sco_s() - 0.1, 2020),
    lambda: 1,
    "_smooth_sco_var_s",
)


@component.add(
    name="Sensitivity of Coal Price to Supply and Demand",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "sco_var_s": 1,
        "_smooth_sensitivity_of_coal_price_to_supply_and_demand": 1,
    },
    other_deps={
        "_smooth_sensitivity_of_coal_price_to_supply_and_demand": {
            "initial": {
                "sensitivity_of_coal_price_to_supply_and_demand_variation": 1,
                "sco_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "sensitivity_of_coal_price_to_supply_and_demand_variation": 1,
                "sco_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_demand_variation_time": 1,
            },
        }
    },
)
def sensitivity_of_coal_price_to_supply_and_demand():
    """
    Sensitivity of Coal Price to Supply and Demand ratio.
    """
    return sco_var_s() + _smooth_sensitivity_of_coal_price_to_supply_and_demand()


_smooth_sensitivity_of_coal_price_to_supply_and_demand = Smooth(
    lambda: step(
        __data["time"],
        sensitivity_of_coal_price_to_supply_and_demand_variation() - sco_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_demand_variation_time(),
    lambda: step(
        __data["time"],
        sensitivity_of_coal_price_to_supply_and_demand_variation() - sco_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_sensitivity_of_coal_price_to_supply_and_demand",
)


@component.add(
    name="Sensitivity of Coal Price to Supply and Demand Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sensitivity_of_coal_price_to_supply_and_demand_variation():
    return 0.1


@component.add(
    name="Share of Investment in Revenue Coal",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_investment_in_coal": 1, "coal_revenue": 1},
)
def share_of_investment_in_revenue_coal():
    return total_investment_in_coal() / coal_revenue()


@component.add(
    name="Share of Upstream Investment in Total Investment Coal",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def share_of_upstream_investment_in_total_investment_coal():
    """
    Data from World Energy Investment 2023
    """
    return 0.753623


@component.add(
    name="Table for FICDT",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_table_for_ficdt"},
)
def table_for_ficdt(x, final_subs=None):
    """
    Table determining order by which technology investments are dedicated to exploration and production technologies. For small Coal Fraction Discoverable, in order to make sufficient resources available to be produced, more investments are directed to exploration technologies. Once the Coal Fraction Discoverable increases the investments are redirected to production technologies.
    """
    return _hardcodedlookup_table_for_ficdt(x, final_subs)


_hardcodedlookup_table_for_ficdt = HardcodedLookups(
    [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
    [0.8, 0.8, 0.7, 0.5, 0.2, 0.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_for_ficdt",
)


@component.add(
    name="Time to Average Coal Production",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_average_coal_production():
    """
    Time to average total coal production per year.
    """
    return 1


@component.add(
    name="Total Coal Demand",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_demand": 1, "market_share_coal": 1},
)
def total_coal_demand():
    """
    Total demand for coal resources.
    """
    return energy_demand() * market_share_coal()


@component.add(
    name="Total Coal Discoverable Resources",
    units="Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_coal_resources": 1,
        "coal_fraction_discoverable": 1,
        "cumulative_additions_to_coal_production": 1,
    },
)
def total_coal_discoverable_resources():
    """
    Total Coal Discoverable Resources as a percentage of Total Coal Resources. It excludes identified and already produced resources. The percentage is determined by exploration technology developments.
    """
    return (
        total_coal_resources() * coal_fraction_discoverable()
        - cumulative_additions_to_coal_production()
    )


@component.add(
    name="Total Coal Recoverable Resource Remaining",
    units="Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "cumulative_additions_to_coal_production": 1,
        "coal_fraction_recoverable": 1,
        "cumulative_coal_production": 1,
    },
)
def total_coal_recoverable_resource_remaining():
    """
    Total Coal Recoverable Resources Remaining as a percentage of Cumulative Additions to Coal Production. It excludes already produced resources. The percentage is determined by production technology developments.
    """
    return (
        cumulative_additions_to_coal_production() * coal_fraction_recoverable()
        - cumulative_coal_production()
    )


@component.add(
    name="Total Coal Resources",
    units="Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "undiscovered_coal_resources": 1,
        "cumulative_additions_to_coal_production": 1,
    },
)
def total_coal_resources():
    """
    Total coal resources including Undiscovered Coal Resources, Identified Coal Resources and resources already produced i.e. Cumulative Coal Production.
    """
    return undiscovered_coal_resources() + cumulative_additions_to_coal_production()


@component.add(
    name="Total Investment in Coal",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_coal_exploration": 1,
        "investment_in_coal_production": 1,
        "investment_in_coal_technology": 1,
        "share_of_upstream_investment_in_total_investment_coal": 1,
    },
)
def total_investment_in_coal():
    return (
        investment_in_coal_exploration()
        + investment_in_coal_production()
        + investment_in_coal_technology()
    ) / share_of_upstream_investment_in_total_investment_coal()


@component.add(name="UC S", units="Mtoe", comp_type="Constant", comp_subtype="Normal")
def uc_s():
    return 900000


@component.add(
    name="UC Var S",
    units="Mtoe",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_uc_var_s": 1},
    other_deps={
        "_smooth_uc_var_s": {
            "initial": {"uc_s": 1, "time": 1},
            "step": {"uc_s": 1, "time": 1},
        }
    },
)
def uc_var_s():
    return 900000 + _smooth_uc_var_s()


_smooth_uc_var_s = Smooth(
    lambda: step(__data["time"], uc_s() - 900000, 2020),
    lambda: 1,
    lambda: step(__data["time"], uc_s() - 900000, 2020),
    lambda: 1,
    "_smooth_uc_var_s",
)


@component.add(
    name="Undiscovered Coal Resources",
    units="Mtoe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_undiscovered_coal_resources": 1},
    other_deps={
        "_integ_undiscovered_coal_resources": {
            "initial": {"init_ucrn": 1},
            "step": {"coal_exploration": 1},
        }
    },
)
def undiscovered_coal_resources():
    """
    Existing Coal Resources but not discovered yet.
    """
    return _integ_undiscovered_coal_resources()


_integ_undiscovered_coal_resources = Integ(
    lambda: -coal_exploration(),
    lambda: init_ucrn(),
    "_integ_undiscovered_coal_resources",
)


@component.add(
    name="Undiscovered Coal Resources Variation",
    units="Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def undiscovered_coal_resources_variation():
    return 900000


@component.add(
    name="Unit Cost of Coal Exploration",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_unit_cost_of_coal_exploration": 1,
        "productivity_of_investment_in_coal_exploration": 2,
        "toe_per_mtoe": 1,
    },
)
def unit_cost_of_coal_exploration():
    """
    Unit cost of coal exploration. Depends on remaining undiscovered coal resources and advances in exploration technologies.
    """
    return float(
        np.minimum(
            max_unit_cost_of_coal_exploration(),
            if_then_else(
                productivity_of_investment_in_coal_exploration() == 0,
                lambda: 0,
                lambda: 1
                / productivity_of_investment_in_coal_exploration()
                * toe_per_mtoe(),
            ),
        )
    )


@component.add(
    name="Unit Cost of Coal Production",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "productivity_of_investment_in_coal_production": 1,
        "toe_per_mtoe": 1,
        "carbon_price": 1,
        "climate_policy_scenario": 1,
        "co2_intensity_of_fuels": 1,
    },
)
def unit_cost_of_coal_production():
    """
    Unit cost of coal production. ZIDZ(1, Productivity of Investment in Coal Production/Million toe per Mtoe)
    """
    return (
        1 / productivity_of_investment_in_coal_production() * toe_per_mtoe()
        + climate_policy_scenario()
        * float(co2_intensity_of_fuels().loc["Coal"])
        * carbon_price()
    )
