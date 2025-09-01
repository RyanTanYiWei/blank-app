"""
Module energy_biomass
Translated using PySD version 3.14.3
"""

@component.add(
    name="Average Annual Production per Capacity",
    units="Mtoe/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def average_annual_production_per_capacity():
    """
    Average annual energy production per unit of biomass installed capacity.
    """
    return 0.116


@component.add(
    name="Biomass Capacity Aging Rate",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_energy_installed_capacity": 1,
        "biomass_capacity_aging_time": 1,
    },
)
def biomass_capacity_aging_rate():
    """
    Aging rate of biomass energy production capacities.
    """
    return biomass_energy_installed_capacity() / biomass_capacity_aging_time()


@component.add(
    name="Biomass Capacity Aging Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biomass_capacity_aging_time():
    """
    Average biomass energy production capacity aging time.
    """
    return 20


@component.add(
    name="Biomass Capacity Factor",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"minbcf": 2, "maxbcf": 1, "biomass_energy_technology_ratio": 2},
)
def biomass_capacity_factor():
    """
    Parameter indicating what fraction of Biomass Conversion Efficiency it is possible to realize with the current state of technical developments.
    """
    return minbcf() + (maxbcf() - minbcf()) * (
        biomass_energy_technology_ratio() / (biomass_energy_technology_ratio() + 1)
    )


@component.add(
    name="Biomass Conversion Efficiency",
    units="Mtoe/Biomass ton",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"variable1_biomass": 1},
)
def biomass_conversion_efficiency():
    """
    Reference Biomass Conversion Efficiency indicating the greatest possibility of turning biomass into energy.
    """
    return variable1_biomass()


@component.add(
    name="Biomass Energy Demand to Supply Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_biomass_demand": 1, "potential_biomass_energy_production": 1},
)
def biomass_energy_demand_to_supply_ratio():
    """
    Biomass Energy Demand to Supply Ratio.
    """
    return total_biomass_demand() / potential_biomass_energy_production()


@component.add(
    name="Biomass Energy Installed Capacity",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_biomass_energy_installed_capacity": 1},
    other_deps={
        "_integ_biomass_energy_installed_capacity": {
            "initial": {"init_bic": 1},
            "step": {
                "installation_of_biomass_capacity_rate": 1,
                "biomass_capacity_aging_rate": 1,
            },
        }
    },
)
def biomass_energy_installed_capacity():
    """
    Installed capacity to transform biomass into energy.
    """
    return _integ_biomass_energy_installed_capacity()


_integ_biomass_energy_installed_capacity = Integ(
    lambda: installation_of_biomass_capacity_rate() - biomass_capacity_aging_rate(),
    lambda: init_bic(),
    "_integ_biomass_energy_installed_capacity",
)


@component.add(
    name="Biomass Energy Installed Capacity Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_energy_installed_capacity": 1,
        "reference_biomass_energy_installed_capacity": 1,
    },
)
def biomass_energy_installed_capacity_ratio():
    """
    Ratio of installed biomass energy production capacities to reference capacity.
    """
    return float(
        np.maximum(
            0,
            1
            - biomass_energy_installed_capacity()
            / reference_biomass_energy_installed_capacity(),
        )
    )


@component.add(
    name="Biomass Energy Price",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "indicated_biomass_energy_price": 1,
        "effect_of_biomass_energy_demand_and_supply_on_price": 1,
    },
)
def biomass_energy_price():
    """
    Actual biomass energy price accounting for indicated biomass energy price and effect of demand and supply.
    """
    return (
        indicated_biomass_energy_price()
        * effect_of_biomass_energy_demand_and_supply_on_price()
    )


@component.add(
    name="Biomass Energy Production",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biomass_energy_production_rate": 1},
)
def biomass_energy_production():
    """
    Total biomass energy production per year.
    """
    return biomass_energy_production_rate()


@component.add(
    name="Biomass Energy Production Indicator",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biomass_energy_production": 1, "mtoe_into_ej": 1},
)
def biomass_energy_production_indicator():
    return biomass_energy_production() * mtoe_into_ej()


@component.add(
    name="Biomass Energy Production Rate",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_biomass_energy_production": 1, "total_biomass_demand": 1},
)
def biomass_energy_production_rate():
    """
    Total biomass energy production per year accounting for demand and potential production due to available resources, production capability and technical developments.
    """
    return float(
        np.minimum(potential_biomass_energy_production(), total_biomass_demand())
    )


@component.add(
    name="Biomass Energy Revenue",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biomass_energy_production": 1, "biomass_energy_price": 1},
)
def biomass_energy_revenue():
    """
    Total revenue in biomass energy market.
    """
    return biomass_energy_production() * biomass_energy_price()


@component.add(
    name="Biomass Energy Technology Development Time",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"renewable_energy_technology_development_time_variation": 1, "time": 1},
)
def biomass_energy_technology_development_time():
    """
    Average time required to turn investments into concrete biomass energy efficiency technology developments. Since the simulation starts in 1900 it is a significant time.
    """
    return 50 + step(
        __data["time"],
        renewable_energy_technology_development_time_variation() - 50,
        2020,
    )


@component.add(
    name="Biomass Energy Technology Ratio",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_biomass_energy_technology_ratio": 1},
    other_deps={
        "_integ_biomass_energy_technology_ratio": {
            "initial": {"init_betrn": 1},
            "step": {"increase_in_biomass_energy_technology_ratio": 1},
        }
    },
)
def biomass_energy_technology_ratio():
    """
    Biomass Energy Technology Ratio increased due to investments in biomass energy efficiency.
    """
    return _integ_biomass_energy_technology_ratio()


_integ_biomass_energy_technology_ratio = Integ(
    lambda: increase_in_biomass_energy_technology_ratio(),
    lambda: init_betrn(),
    "_integ_biomass_energy_technology_ratio",
)


@component.add(
    name="Biomass Final Investment",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"renewable_final_investment_fraction_variation": 1, "time": 1},
)
def biomass_final_investment():
    """
    Eventual average level of investments in biomass energy technology.
    """
    return 0.03 + step(
        __data["time"], renewable_final_investment_fraction_variation() - 0.03, 2020
    )


@component.add(
    name="Biomass Infrastructure Adjustment",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_capacity_aging_rate": 1,
        "desired_biomass_installed_capacity": 1,
        "time_to_adjust_biomass_infrastructure": 1,
        "biomass_energy_installed_capacity": 1,
    },
)
def biomass_infrastructure_adjustment():
    """
    Adjustment of Biomass Infrastructure to the desired level over a specified adjustment time and accounting for constant infrastructure decrease due to aging process.
    """
    return (
        biomass_capacity_aging_rate()
        + (desired_biomass_installed_capacity() - biomass_energy_installed_capacity())
        / time_to_adjust_biomass_infrastructure()
    )


@component.add(
    name="Biomass Initial Investment",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biomass_initial_investment():
    """
    Initial level of fractional investments in biomass energy technology.
    """
    return 0


@component.add(
    name="Biomass Installation Efficiency",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"minbie": 2, "biomass_installation_technology_ratio": 2, "maxbie": 1},
)
def biomass_installation_efficiency():
    """
    Parameter indicating biomass energy capacity installation efficiency at the current state of technical developments.
    """
    return minbie() + (maxbie() - minbie()) * (
        biomass_installation_technology_ratio()
        / (biomass_installation_technology_ratio() + 1)
    )


@component.add(
    name="Biomass Installation Technology Development Time",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "renewable_installation_technology_development_time_variation": 1,
        "time": 1,
    },
)
def biomass_installation_technology_development_time():
    """
    Average time required to turn investments into concrete biomass energy production capacity. Since the simulation starts in 1900 it is a significant time.
    """
    return 100 + step(
        __data["time"],
        renewable_installation_technology_development_time_variation() - 100,
        2020,
    )


@component.add(
    name="Biomass Installation Technology Ratio",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_biomass_installation_technology_ratio": 1},
    other_deps={
        "_integ_biomass_installation_technology_ratio": {
            "initial": {"init_bitrn": 1},
            "step": {"increase_in_biomass_installation_technology_ratio": 1},
        }
    },
)
def biomass_installation_technology_ratio():
    """
    Biomass Installation Technology Ratio increased due to investments in biomass energy capacity efficiency.
    """
    return _integ_biomass_installation_technology_ratio()


_integ_biomass_installation_technology_ratio = Integ(
    lambda: increase_in_biomass_installation_technology_ratio(),
    lambda: init_bitrn(),
    "_integ_biomass_installation_technology_ratio",
)


@component.add(
    name="Biomass Investment Fraction Finish",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_time": 1, "ramp_investment_period": 1},
)
def biomass_investment_fraction_finish():
    """
    End of fractional investments in biomass energy technology.
    """
    return initial_time() + ramp_investment_period()


@component.add(
    name="Biomass Investment Fraction Slope",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_final_investment": 1,
        "biomass_initial_investment": 1,
        "ramp_investment_period": 1,
    },
)
def biomass_investment_fraction_slope():
    """
    Intensity of increase in investments in biomass energy technology.
    """
    return (
        float(np.abs(biomass_final_investment() - biomass_initial_investment()))
        / ramp_investment_period()
    )


@component.add(
    name="Biomass Investment Fraction Start",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_time": 1},
)
def biomass_investment_fraction_start():
    """
    Start of investments in biomass energy technology.
    """
    return initial_time()


@component.add(
    name="Biomass Learning Curve Strength",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fraction_for_biomass_learning_curve_strength": 1},
)
def biomass_learning_curve_strength():
    """
    Strength of biomass learning curve with which the biomass energy costs are influenced..
    """
    return float(np.log(1 - fraction_for_biomass_learning_curve_strength())) / float(
        np.log(2)
    )


@component.add(
    name="Biomass Production",
    units="Biomass ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"forest_biomass_production": 1, "energy_crops_production": 1},
)
def biomass_production():
    """
    Total biomass production from forest and energy crops.
    """
    return forest_biomass_production() + energy_crops_production()


@component.add(
    name="Biomass Production to Installation Ratio",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biomass_energy_production": 1, "biomass_energy_installed_capacity": 1},
)
def biomass_production_to_installation_ratio():
    """
    Ratio of biomass energy production to available production capacity.
    """
    return biomass_energy_production() / biomass_energy_installed_capacity()


@component.add(
    name="Cost of Biomass Energy",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "unit_cost_of_biomass_capacity_installation": 1,
        "unit_cost_of_biomass_energy_production": 1,
    },
)
def cost_of_biomass_energy():
    """
    Cost of biomass energy production assuming an impact of learning curve.
    """
    return (
        unit_cost_of_biomass_capacity_installation()
        + unit_cost_of_biomass_energy_production()
    )


@component.add(
    name="Cumulative Biomass Energy Produced",
    units="Mtoe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_biomass_energy_produced": 1},
    other_deps={
        "_integ_cumulative_biomass_energy_produced": {
            "initial": {"init_cumulative_biomass_produced": 1},
            "step": {"biomass_energy_production": 1},
        }
    },
)
def cumulative_biomass_energy_produced():
    """
    Cumulative biomass energy that has been produced.
    """
    return _integ_cumulative_biomass_energy_produced()


_integ_cumulative_biomass_energy_produced = Integ(
    lambda: biomass_energy_production(),
    lambda: init_cumulative_biomass_produced(),
    "_integ_cumulative_biomass_energy_produced",
)


@component.add(
    name="Delay Time IBETR",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biomass_energy_technology_development_time": 1},
)
def delay_time_ibetr():
    return biomass_energy_technology_development_time() / 3


@component.add(
    name="Delay Time IBITR",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biomass_installation_technology_development_time": 1},
)
def delay_time_ibitr():
    return biomass_installation_technology_development_time() / 3


@component.add(
    name="Desired Biomass Energy Gross Margin",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def desired_biomass_energy_gross_margin():
    """
    Desired Gross Margin per unit of biomass energy.
    """
    return 0.2


@component.add(
    name="Desired Biomass Installed Capacity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_biomass_demand": 1,
        "efficiency_of_biomass_installed_capacity": 1,
    },
)
def desired_biomass_installed_capacity():
    """
    Desired Biomass Installed Capacity accounting for Total Biomass Demand and Efficiency of Biomass Installed Capacity.
    """
    return total_biomass_demand() / efficiency_of_biomass_installed_capacity()


@component.add(
    name="Effect of Biomass Energy Demand and Supply on Price",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_biomass_demand": 1,
        "potential_biomass_energy_production": 1,
        "sensitivity_of_biomass_energy_price_to_supply_and_demand": 1,
    },
)
def effect_of_biomass_energy_demand_and_supply_on_price():
    """
    Effect of Biomass Demand and Supply ratio on actual biomass energy price.
    """
    return (
        total_biomass_demand() / potential_biomass_energy_production()
    ) ** sensitivity_of_biomass_energy_price_to_supply_and_demand()


@component.add(
    name="Effectiveness IBETR",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_biomass_energy_efficiency": 1,
        "effectiveness_of_investment_in_biomass_energy_technology": 1,
    },
)
def effectiveness_ibetr():
    return (
        investment_in_biomass_energy_efficiency()
        * effectiveness_of_investment_in_biomass_energy_technology()
    )


@component.add(
    name="Effectiveness IBITR",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_biomass_energy_installation": 1,
        "effectiveness_of_investment_in_biomass_installation_technology": 1,
    },
)
def effectiveness_ibitr():
    return (
        investment_in_biomass_energy_installation()
        * effectiveness_of_investment_in_biomass_installation_technology()
    )


@component.add(
    name="Effectiveness of Investment in Biomass Energy Technology",
    units="1/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effectiveness_of_investment_in_renewable_energy_technology_variation": 1,
        "time": 1,
    },
)
def effectiveness_of_investment_in_biomass_energy_technology():
    """
    Effectiveness of resources dedicated to biomass energy efficiency technology development.
    """
    return 1e-09 + step(
        __data["time"],
        effectiveness_of_investment_in_renewable_energy_technology_variation() - 1e-09,
        2020,
    )


@component.add(
    name="Effectiveness of Investment in Biomass Installation Technology",
    units="1/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effectiveness_of_investment_in_renewable_installation_technology_variation": 1,
        "time": 1,
    },
)
def effectiveness_of_investment_in_biomass_installation_technology():
    """
    Effectiveness of resources dedicated to biomass energy capacity efficiency technology development.
    """
    return 1e-10 + step(
        __data["time"],
        effectiveness_of_investment_in_renewable_installation_technology_variation()
        - 1e-10,
        2020,
    )


@component.add(
    name="Efficiency of Biomass Installed Capacity",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_biomass_energy_production_from_infrastructure": 1,
        "biomass_energy_installed_capacity": 1,
    },
)
def efficiency_of_biomass_installed_capacity():
    """
    Total production efficiency of Biomass Installed Capacity.
    """
    return zidz(
        potential_biomass_energy_production_from_infrastructure(),
        biomass_energy_installed_capacity(),
    )


@component.add(
    name="Fraction for Biomass Learning Curve Strength",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fraction_for_biomass_learning_curve_strength_variation": 1, "time": 1},
)
def fraction_for_biomass_learning_curve_strength():
    """
    Fraction for Biomass Learning Curve Strength indicating by what percentage the biomass energy cost will drop for each doubling of biomass installed capacity.
    """
    return 0.01 + step(
        __data["time"],
        fraction_for_biomass_learning_curve_strength_variation() - 0.01,
        2020,
    )


@component.add(
    name="Fraction for Biomass Learning Curve Strength Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraction_for_biomass_learning_curve_strength_variation():
    """
    Fraction for Biomass Learning Curve Strength indicating by what percentage the biomass energy cost will drop for each doubling of biomass installed capacity.
    """
    return 0.01


@component.add(
    name="Fraction Invested in Biomass Energy Installation",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"biomass_installation_efficiency": 1, "table_for_fibei": 1},
)
def fraction_invested_in_biomass_energy_installation():
    """
    Fraction of investments in biomass energy technology dedicated to capacity.
    """
    return table_for_fibei(biomass_installation_efficiency())


@component.add(
    name="Fraction of Revenue Invested in Biomass Technology",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_investment_fraction_slope": 1,
        "biomass_investment_fraction_start": 1,
        "biomass_investment_fraction_finish": 1,
        "time": 1,
    },
)
def fraction_of_revenue_invested_in_biomass_technology():
    """
    Parameter to take into account historical increase of the biomass energy significance and over time greater resources dedicated to the technology development.
    """
    return ramp(
        __data["time"],
        biomass_investment_fraction_slope(),
        biomass_investment_fraction_start(),
        biomass_investment_fraction_finish(),
    )


@component.add(
    name="Impact of Learning on Biomass Unit Cost of Technology",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_energy_installed_capacity": 1,
        "init_bic": 1,
        "biomass_learning_curve_strength": 1,
    },
)
def impact_of_learning_on_biomass_unit_cost_of_technology():
    """
    Impact of learning curve on biomass energy cost.
    """
    return (
        biomass_energy_installed_capacity() / init_bic()
    ) ** biomass_learning_curve_strength()


@component.add(
    name="Increase in Biomass Energy Technology Ratio",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ibetrlv3": 1},
)
def increase_in_biomass_energy_technology_ratio():
    """
    Increase in Biomass Energy Technology Ratio due to investments in biomass energy efficiency technology and their productivity.
    """
    return outflow_ibetrlv3()


@component.add(
    name="Increase in Biomass Energy Technology Ratio LV1",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_biomass_energy_technology_ratio_lv1": 1},
    other_deps={
        "_integ_increase_in_biomass_energy_technology_ratio_lv1": {
            "initial": {"increase_in_biomass_energy_technology_ratio_lv3": 1},
            "step": {"inflow_ibetrlv1": 1, "outflow_ibetrlv1": 1},
        }
    },
)
def increase_in_biomass_energy_technology_ratio_lv1():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_biomass_energy_technology_ratio_lv1()


_integ_increase_in_biomass_energy_technology_ratio_lv1 = Integ(
    lambda: inflow_ibetrlv1() - outflow_ibetrlv1(),
    lambda: increase_in_biomass_energy_technology_ratio_lv3(),
    "_integ_increase_in_biomass_energy_technology_ratio_lv1",
)


@component.add(
    name="Increase in Biomass Energy Technology Ratio LV2",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_biomass_energy_technology_ratio_lv2": 1},
    other_deps={
        "_integ_increase_in_biomass_energy_technology_ratio_lv2": {
            "initial": {"increase_in_biomass_energy_technology_ratio_lv3": 1},
            "step": {"inflow_ibetrlv2": 1, "outflow_ibetrlv2": 1},
        }
    },
)
def increase_in_biomass_energy_technology_ratio_lv2():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_biomass_energy_technology_ratio_lv2()


_integ_increase_in_biomass_energy_technology_ratio_lv2 = Integ(
    lambda: inflow_ibetrlv2() - outflow_ibetrlv2(),
    lambda: increase_in_biomass_energy_technology_ratio_lv3(),
    "_integ_increase_in_biomass_energy_technology_ratio_lv2",
)


@component.add(
    name="Increase in Biomass Energy Technology Ratio LV3",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_biomass_energy_technology_ratio_lv3": 1},
    other_deps={
        "_integ_increase_in_biomass_energy_technology_ratio_lv3": {
            "initial": {"effectiveness_ibetr": 1, "delay_time_ibetr": 1},
            "step": {"inflow_ibetrlv3": 1, "outflow_ibetrlv3": 1},
        }
    },
)
def increase_in_biomass_energy_technology_ratio_lv3():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_biomass_energy_technology_ratio_lv3()


_integ_increase_in_biomass_energy_technology_ratio_lv3 = Integ(
    lambda: inflow_ibetrlv3() - outflow_ibetrlv3(),
    lambda: effectiveness_ibetr() * delay_time_ibetr(),
    "_integ_increase_in_biomass_energy_technology_ratio_lv3",
)


@component.add(
    name="Increase in Biomass Installation Technology Ratio",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ibitrlv3": 1},
)
def increase_in_biomass_installation_technology_ratio():
    """
    Increase in Biomass Installation Technology Ratio due to investments in biomass energy capacity.
    """
    return outflow_ibitrlv3()


@component.add(
    name="Increase in Biomass Installation Technology Ratio LV1",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_biomass_installation_technology_ratio_lv1": 1},
    other_deps={
        "_integ_increase_in_biomass_installation_technology_ratio_lv1": {
            "initial": {"increase_in_biomass_installation_technology_ratio_lv3": 1},
            "step": {"inflow_ibitrlv1": 1, "outflow_ibitrlv1": 1},
        }
    },
)
def increase_in_biomass_installation_technology_ratio_lv1():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_biomass_installation_technology_ratio_lv1()


_integ_increase_in_biomass_installation_technology_ratio_lv1 = Integ(
    lambda: inflow_ibitrlv1() - outflow_ibitrlv1(),
    lambda: increase_in_biomass_installation_technology_ratio_lv3(),
    "_integ_increase_in_biomass_installation_technology_ratio_lv1",
)


@component.add(
    name="Increase in Biomass Installation Technology Ratio LV2",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_biomass_installation_technology_ratio_lv2": 1},
    other_deps={
        "_integ_increase_in_biomass_installation_technology_ratio_lv2": {
            "initial": {"increase_in_biomass_installation_technology_ratio_lv3": 1},
            "step": {"inflow_ibitrlv2": 1, "outflow_ibitrlv2": 1},
        }
    },
)
def increase_in_biomass_installation_technology_ratio_lv2():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_biomass_installation_technology_ratio_lv2()


_integ_increase_in_biomass_installation_technology_ratio_lv2 = Integ(
    lambda: inflow_ibitrlv2() - outflow_ibitrlv2(),
    lambda: increase_in_biomass_installation_technology_ratio_lv3(),
    "_integ_increase_in_biomass_installation_technology_ratio_lv2",
)


@component.add(
    name="Increase in Biomass Installation Technology Ratio LV3",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_biomass_installation_technology_ratio_lv3": 1},
    other_deps={
        "_integ_increase_in_biomass_installation_technology_ratio_lv3": {
            "initial": {"effectiveness_ibitr": 1, "delay_time_ibitr": 1},
            "step": {"inflow_ibitrlv3": 1, "outflow_ibitrlv3": 1},
        }
    },
)
def increase_in_biomass_installation_technology_ratio_lv3():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_biomass_installation_technology_ratio_lv3()


_integ_increase_in_biomass_installation_technology_ratio_lv3 = Integ(
    lambda: inflow_ibitrlv3() - outflow_ibitrlv3(),
    lambda: effectiveness_ibitr() * delay_time_ibitr(),
    "_integ_increase_in_biomass_installation_technology_ratio_lv3",
)


@component.add(
    name="Indicated Biomass Energy Price",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cost_of_biomass_energy": 1, "desired_biomass_energy_gross_margin": 1},
)
def indicated_biomass_energy_price():
    """
    Indicated biomass energy price accounting for unit cost and gross margin.
    """
    return cost_of_biomass_energy() * (1 + desired_biomass_energy_gross_margin())


@component.add(
    name="Inflow IBETRLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effectiveness_ibetr": 1},
)
def inflow_ibetrlv1():
    return effectiveness_ibetr()


@component.add(
    name="Inflow IBETRLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ibetrlv1": 1},
)
def inflow_ibetrlv2():
    return outflow_ibetrlv1()


@component.add(
    name="Inflow IBETRLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ibetrlv2": 1},
)
def inflow_ibetrlv3():
    return outflow_ibetrlv2()


@component.add(
    name="Inflow IBITRLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effectiveness_ibitr": 1},
)
def inflow_ibitrlv1():
    return effectiveness_ibitr()


@component.add(
    name="Inflow IBITRLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ibitrlv1": 1},
)
def inflow_ibitrlv2():
    return outflow_ibitrlv1()


@component.add(
    name="Inflow IBITRLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ibitrlv2": 1},
)
def inflow_ibitrlv3():
    return outflow_ibitrlv2()


@component.add(
    name="INIT BETRN", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def init_betrn():
    """
    Initial Biomass Energy Technology Ratio.
    """
    return 0


@component.add(
    name="INIT BIC", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def init_bic():
    """
    Initial installed capacity to transform biomass into energy.
    """
    return 40


@component.add(
    name="INIT BITRN", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def init_bitrn():
    """
    Initial Biomass Installation Technology Ratio.
    """
    return 0


@component.add(
    name="INIT Cumulative Biomass Produced", comp_type="Constant", comp_subtype="Normal"
)
def init_cumulative_biomass_produced():
    return 0


@component.add(
    name="INIT Unit Cost of Biomass Capacity Installation",
    units="$/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_unit_cost_of_biomass_capacity_installation():
    """
    Initial unit cost per unit biomass capacity installation.
    """
    return 2000000.0


@component.add(
    name="Installation of Biomass Capacity Rate",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_infrastructure_adjustment": 1,
        "productivity_of_investment_in_biomass_capacity_installation": 1,
    },
)
def installation_of_biomass_capacity_rate():
    """
    Rate of new biomass capacity installation.
    """
    return float(
        np.maximum(
            0,
            biomass_infrastructure_adjustment()
            * productivity_of_investment_in_biomass_capacity_installation(),
        )
    )


@component.add(
    name="Investment in Biomass Capacity",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "installation_of_biomass_capacity_rate": 1,
        "unit_cost_of_biomass_capacity_installation": 1,
        "efficiency_of_biomass_installed_capacity": 1,
        "biomass_capacity_aging_time": 1,
    },
)
def investment_in_biomass_capacity():
    """
    Amount of resources dedicated to biomass capacity development.
    """
    return (
        installation_of_biomass_capacity_rate()
        * unit_cost_of_biomass_capacity_installation()
        * efficiency_of_biomass_installed_capacity()
        * biomass_capacity_aging_time()
    )


@component.add(
    name="Investment in Biomass Energy Efficiency",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_biomass_energy_technology": 1,
        "fraction_invested_in_biomass_energy_installation": 1,
    },
)
def investment_in_biomass_energy_efficiency():
    """
    Total investments in biomass energy efficiency technology.
    """
    return investment_in_biomass_energy_technology() * (
        1 - fraction_invested_in_biomass_energy_installation()
    )


@component.add(
    name="Investment in Biomass Energy Installation",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_biomass_energy_technology": 1,
        "fraction_invested_in_biomass_energy_installation": 1,
    },
)
def investment_in_biomass_energy_installation():
    """
    Total investments in biomass energy capacity.
    """
    return (
        investment_in_biomass_energy_technology()
        * fraction_invested_in_biomass_energy_installation()
    )


@component.add(
    name="Investment in Biomass Energy Technology",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fraction_of_revenue_invested_in_biomass_technology": 1,
        "biomass_energy_revenue": 1,
    },
)
def investment_in_biomass_energy_technology():
    """
    Investments in development of biomass energy efficiency technology and production capability.
    """
    return (
        fraction_of_revenue_invested_in_biomass_technology() * biomass_energy_revenue()
    )


@component.add(name="MAXBCF", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def maxbcf():
    """
    Maximal possible value of Biomass Capacity Factor.
    """
    return 1


@component.add(name="MAXBIE", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def maxbie():
    """
    Maximal value of Biomass Installation Efficiency factor.
    """
    return 1


@component.add(name="MINBCF", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def minbcf():
    """
    Minimal and initial value of Biomass Capacity Factor.
    """
    return 0.4


@component.add(name="MINBIE", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def minbie():
    """
    Minimal and initial value of Biomass Installation Efficiency factor.
    """
    return 0.5


@component.add(
    name="Outflow IBETRLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_biomass_energy_technology_ratio_lv1": 1,
        "delay_time_ibetr": 1,
    },
)
def outflow_ibetrlv1():
    return increase_in_biomass_energy_technology_ratio_lv1() / delay_time_ibetr()


@component.add(
    name="Outflow IBETRLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_biomass_energy_technology_ratio_lv2": 1,
        "delay_time_ibetr": 1,
    },
)
def outflow_ibetrlv2():
    return increase_in_biomass_energy_technology_ratio_lv2() / delay_time_ibetr()


@component.add(
    name="Outflow IBETRLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_biomass_energy_technology_ratio_lv3": 1,
        "delay_time_ibetr": 1,
    },
)
def outflow_ibetrlv3():
    return increase_in_biomass_energy_technology_ratio_lv3() / delay_time_ibetr()


@component.add(
    name="Outflow IBITRLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_biomass_installation_technology_ratio_lv1": 1,
        "delay_time_ibitr": 1,
    },
)
def outflow_ibitrlv1():
    return increase_in_biomass_installation_technology_ratio_lv1() / delay_time_ibitr()


@component.add(
    name="Outflow IBITRLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_biomass_installation_technology_ratio_lv2": 1,
        "delay_time_ibitr": 1,
    },
)
def outflow_ibitrlv2():
    return increase_in_biomass_installation_technology_ratio_lv2() / delay_time_ibitr()


@component.add(
    name="Outflow IBITRLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_biomass_installation_technology_ratio_lv3": 1,
        "delay_time_ibitr": 1,
    },
)
def outflow_ibitrlv3():
    return increase_in_biomass_installation_technology_ratio_lv3() / delay_time_ibitr()


@component.add(
    name="Potential Biomass Energy Production",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_biomass_energy_production_from_infrastructure": 1,
        "potential_biomass_energy_production_from_resources": 1,
    },
)
def potential_biomass_energy_production():
    """
    Potential biomass energy production per year due to available resources, production capability and technical developments.
    """
    return float(
        np.minimum(
            potential_biomass_energy_production_from_infrastructure(),
            potential_biomass_energy_production_from_resources(),
        )
    )


@component.add(
    name="Potential Biomass Energy Production from Infrastructure",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_energy_installed_capacity": 1,
        "average_annual_production_per_capacity": 1,
    },
)
def potential_biomass_energy_production_from_infrastructure():
    """
    Potential biomass energy production per year due to available production capability.
    """
    return (
        biomass_energy_installed_capacity() * average_annual_production_per_capacity()
    )


@component.add(
    name="Potential Biomass Energy Production from Resources",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_production": 1,
        "biomass_conversion_efficiency": 1,
        "biomass_capacity_factor": 1,
    },
)
def potential_biomass_energy_production_from_resources():
    """
    Potential biomass energy production per year due to available resources and technical developments.
    """
    return (
        biomass_production()
        * biomass_conversion_efficiency()
        * biomass_capacity_factor()
    )


@component.add(
    name="Productivity of Investment in Biomass Capacity Installation",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_energy_installed_capacity_ratio": 1,
        "biomass_installation_efficiency": 1,
    },
)
def productivity_of_investment_in_biomass_capacity_installation():
    """
    Productivity of biomass capacity installation taking into account the level of available capacities and technology development state.
    """
    return biomass_energy_installed_capacity_ratio() * biomass_installation_efficiency()


@component.add(
    name="Reference Biomass Energy Installed Capacity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_biomass_energy_installed_capacity():
    """
    Reference biomass capacity.
    """
    return 500000000000.0


@component.add(
    name="Reference Cost of Biomass Energy Production",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"variable13_biomas_cost": 1},
)
def reference_cost_of_biomass_energy_production():
    """
    Reference cost of unit biomass energy production per year.
    """
    return variable13_biomas_cost()


@component.add(
    name="Sensitivity of Biomass Energy Price to Supply and Demand",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sensitivity_of_biomass_energy_price_to_supply_and_demand():
    """
    Sensitivity of Biomass Energy Price to Supply and Demand ratio.
    """
    return 0


@component.add(
    name="Table for FIBEI",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_table_for_fibei"},
)
def table_for_fibei(x, final_subs=None):
    """
    Table determining order by which technology investments are dedicated to energy and installation efficiency. For small Biomass Installation Efficiency, in order to secure sufficient production capacity, more investments are directed to infrastructure. Once the Biomass Installation Efficiency increases the investments are redirected to energy efficiency technologies.
    """
    return _hardcodedlookup_table_for_fibei(x, final_subs)


_hardcodedlookup_table_for_fibei = HardcodedLookups(
    [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
    [0.8, 0.8, 0.7, 0.5, 0.2, 0.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_for_fibei",
)


@component.add(
    name="Time to Adjust Biomass Infrastructure",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_adjust_biomass_infrastructure():
    """
    Time to adjust Biomass Infrastructure to the desired level.
    """
    return 5


@component.add(
    name="Total Biomass Demand",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_demand": 1, "market_share_biomass": 1},
)
def total_biomass_demand():
    """
    Total demand for energy from biomass.
    """
    return energy_demand() * market_share_biomass()


@component.add(
    name="Unit Cost of Biomass Capacity Installation",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "init_unit_cost_of_biomass_capacity_installation": 1,
        "impact_of_learning_on_biomass_unit_cost_of_technology": 1,
    },
)
def unit_cost_of_biomass_capacity_installation():
    """
    Unit Cost of Biomass Capacity Installation. Determined by Productivity of Investment in Biomass Capacity Installation.
    """
    return (
        init_unit_cost_of_biomass_capacity_installation()
        * impact_of_learning_on_biomass_unit_cost_of_technology()
    )


@component.add(
    name="Unit Cost of Biomass Energy Production",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_cost_of_biomass_energy_production": 1,
        "biomass_production_to_installation_ratio": 1,
    },
)
def unit_cost_of_biomass_energy_production():
    """
    Unit cost of biomass capacity installation per energy unit.
    """
    return (
        reference_cost_of_biomass_energy_production()
        / biomass_production_to_installation_ratio()
    )
