"""
Module energy_solar
Translated using PySD version 3.14.3
"""

@component.add(
    name="Cost of Solar Energy",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "unit_cost_of_solar_capacity_installation": 1,
        "unit_cost_of_solar_energy_production": 1,
    },
)
def cost_of_solar_energy():
    """
    Cost of solar energy production assuming an impact of learning curve.
    """
    return (
        unit_cost_of_solar_capacity_installation()
        + unit_cost_of_solar_energy_production()
    )


@component.add(
    name="Cumulative Solar Energy Produced",
    units="Mtoe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_solar_energy_produced": 1},
    other_deps={
        "_integ_cumulative_solar_energy_produced": {
            "initial": {"init_cumulative_solar_produced": 1},
            "step": {"solar_energy_production": 1},
        }
    },
)
def cumulative_solar_energy_produced():
    """
    Cumulative solar energy that has been produced.
    """
    return _integ_cumulative_solar_energy_produced()


_integ_cumulative_solar_energy_produced = Integ(
    lambda: solar_energy_production(),
    lambda: init_cumulative_solar_produced(),
    "_integ_cumulative_solar_energy_produced",
)


@component.add(
    name="Delay Time ISETR",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"solar_energy_technology_development_time": 1},
)
def delay_time_isetr():
    return solar_energy_technology_development_time() / 3


@component.add(
    name="Delay Time ISITR",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"solar_installation_technology_development_time": 1},
)
def delay_time_isitr():
    return solar_installation_technology_development_time() / 3


@component.add(
    name="Desired Solar Energy Gross Margin",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def desired_solar_energy_gross_margin():
    """
    Desired Gross Margin per unit of solar energy.
    """
    return 0.2


@component.add(
    name="Desired Solar Installed Capacity",
    units="m*m",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_solar_demand": 1, "efficiency_of_solar_installed_capacity": 1},
)
def desired_solar_installed_capacity():
    """
    Desired Solar Installed Capacity accounting for Total Solar Demand and Efficiency of Solar Installed Capacity.
    """
    return total_solar_demand() / efficiency_of_solar_installed_capacity()


@component.add(
    name="Effect of Solar Energy Demand and Supply on Price",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_solar_demand": 1,
        "possible_solar_energy_production": 1,
        "sensitivity_of_solar_energy_price_to_supply_and_demand": 1,
    },
)
def effect_of_solar_energy_demand_and_supply_on_price():
    """
    Effect of Solar Demand and Supply ratio on actual solar energy price.
    """
    return (
        total_solar_demand() / possible_solar_energy_production()
    ) ** sensitivity_of_solar_energy_price_to_supply_and_demand()


@component.add(
    name="Effectiveness ISETR",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effectiveness_of_investment_in_solar_energy_technology": 1,
        "investment_in_solar_energy_efficiency": 1,
    },
)
def effectiveness_isetr():
    return (
        effectiveness_of_investment_in_solar_energy_technology()
        * investment_in_solar_energy_efficiency()
    )


@component.add(
    name="Effectiveness ISITR",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effectiveness_of_investment_in_solar_installation_technology": 1,
        "investment_in_solar_energy_installation": 1,
    },
)
def effectiveness_isitr():
    return (
        effectiveness_of_investment_in_solar_installation_technology()
        * investment_in_solar_energy_installation()
    )


@component.add(
    name="Effectiveness of Investment in Renewable Energy Technology Variation",
    units="1/$",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effectiveness_of_investment_in_renewable_energy_technology_variation():
    return 1e-09


@component.add(
    name="Effectiveness of Investment in Renewable Installation Technology Variation",
    units="1/$",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effectiveness_of_investment_in_renewable_installation_technology_variation():
    return 1e-10


@component.add(
    name="Effectiveness of Investment in Solar Energy Technology",
    units="1/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effectiveness_of_investment_in_renewable_energy_technology_variation": 1,
        "time": 1,
    },
)
def effectiveness_of_investment_in_solar_energy_technology():
    """
    Effectivenes of resources dedicated to solar conversion efficiency technology development.
    """
    return 1e-09 + step(
        __data["time"],
        effectiveness_of_investment_in_renewable_energy_technology_variation() - 1e-09,
        2020,
    )


@component.add(
    name="Effectiveness of Investment in Solar Installation Technology",
    units="1/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effectiveness_of_investment_in_renewable_installation_technology_variation": 1,
        "time": 1,
    },
)
def effectiveness_of_investment_in_solar_installation_technology():
    """
    Effectiveness of resources dedicated to solar energy capacity efficiency technology development.
    """
    return 1e-10 + step(
        __data["time"],
        effectiveness_of_investment_in_renewable_installation_technology_variation()
        - 1e-10,
        2020,
    )


@component.add(
    name="Efficiency of Solar Installed Capacity",
    units="Mtoe/(Year*m*m)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"possible_solar_energy_production": 1, "solar_installed_capacity": 1},
)
def efficiency_of_solar_installed_capacity():
    """
    Total production efficiency of Solar Installed Capacity for given weather conditions and technology developments.
    """
    return possible_solar_energy_production() / solar_installed_capacity()


@component.add(
    name="Fraction for Solar Learning Curve Strength",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fraction_for_wind_and_solar_learning_curve_strength_variation": 1,
        "time": 1,
    },
)
def fraction_for_solar_learning_curve_strength():
    """
    Fraction for Solar Learning Curve Strength indicating by what percentage the solar energy cost will drop for each doubling of solar installed capacity.
    """
    return 0.2 + step(
        __data["time"],
        fraction_for_wind_and_solar_learning_curve_strength_variation() - 0.2,
        2020,
    )


@component.add(
    name="Fraction for Wind and Solar Learning Curve Strength Variation",
    units="1",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraction_for_wind_and_solar_learning_curve_strength_variation():
    return 0.2


@component.add(
    name="Fraction Invested in Solar Energy Installation",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"solar_installation_efficiency": 1, "table_for_fisei": 1},
)
def fraction_invested_in_solar_energy_installation():
    """
    Fraction of investments in solar energy technology dedicated to capacity.
    """
    return table_for_fisei(solar_installation_efficiency())


@component.add(
    name="Fraction of Revenue Invested in Solar Technology",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "solar_investment_fraction_slope": 1,
        "solar_investment_fraction_start": 1,
        "solar_investment_fraction_finish": 1,
        "time": 1,
    },
)
def fraction_of_revenue_invested_in_solar_technology():
    """
    Parameter to take into account historical increase of the solar energy significance and over time greater resources dedicated to the technology development.
    """
    return ramp(
        __data["time"],
        solar_investment_fraction_slope(),
        solar_investment_fraction_start(),
        solar_investment_fraction_finish(),
    )


@component.add(
    name="Fraction of Revenue Invested in Solar Technology Ramp Investment Period Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraction_of_revenue_invested_in_solar_technology_ramp_investment_period_variation():
    """
    Period of fractional investments in new energy technologies.
    """
    return 100


@component.add(
    name="Hours per Year",
    units="Hour/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def hours_per_year():
    """
    Assumed total number of hours per year.
    """
    return 8760


@component.add(
    name="Impact of Learning on Solar Unit Cost of Technology PC",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "solar_installed_capacity": 1,
        "init_sic": 1,
        "solar_learning_curve_strength": 1,
    },
)
def impact_of_learning_on_solar_unit_cost_of_technology_pc():
    """
    Impact of learning curve on solar energy cost.
    """
    return (solar_installed_capacity() / init_sic()) ** solar_learning_curve_strength()


@component.add(
    name="Impact of Space on Capacity Installation",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"solar_installed_capacity": 1, "solar_available_area": 1},
)
def impact_of_space_on_capacity_installation():
    """
    Ratio of currently installed solar capacity to total possible.
    """
    return float(np.maximum(0, 1 - solar_installed_capacity() / solar_available_area()))


@component.add(
    name="Increase in Solar Energy Technology Ratio",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_isetlv3": 1},
)
def increase_in_solar_energy_technology_ratio():
    """
    Increase in Solar Energy Technology Ratio due to investments in solar conversion efficiency technology and their productivity.
    """
    return outflow_isetlv3()


@component.add(
    name="Increase in Solar Energy Technology Ratio LV1",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_solar_energy_technology_ratio_lv1": 1},
    other_deps={
        "_integ_increase_in_solar_energy_technology_ratio_lv1": {
            "initial": {"increase_in_solar_energy_technology_ratio_lv3": 1},
            "step": {"inflow_isetlv1": 1, "outflow_isetlv1": 1},
        }
    },
)
def increase_in_solar_energy_technology_ratio_lv1():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_solar_energy_technology_ratio_lv1()


_integ_increase_in_solar_energy_technology_ratio_lv1 = Integ(
    lambda: inflow_isetlv1() - outflow_isetlv1(),
    lambda: increase_in_solar_energy_technology_ratio_lv3(),
    "_integ_increase_in_solar_energy_technology_ratio_lv1",
)


@component.add(
    name="Increase in Solar Energy Technology Ratio LV2",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_solar_energy_technology_ratio_lv2": 1},
    other_deps={
        "_integ_increase_in_solar_energy_technology_ratio_lv2": {
            "initial": {"increase_in_solar_energy_technology_ratio_lv3": 1},
            "step": {"inflow_isetlv2": 1, "outflow_isetlv2": 1},
        }
    },
)
def increase_in_solar_energy_technology_ratio_lv2():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_solar_energy_technology_ratio_lv2()


_integ_increase_in_solar_energy_technology_ratio_lv2 = Integ(
    lambda: inflow_isetlv2() - outflow_isetlv2(),
    lambda: increase_in_solar_energy_technology_ratio_lv3(),
    "_integ_increase_in_solar_energy_technology_ratio_lv2",
)


@component.add(
    name="Increase in Solar Energy Technology Ratio LV3",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_solar_energy_technology_ratio_lv3": 1},
    other_deps={
        "_integ_increase_in_solar_energy_technology_ratio_lv3": {
            "initial": {"effectiveness_isetr": 1, "delay_time_isetr": 1},
            "step": {"inflow_isetlv3": 1, "outflow_isetlv3": 1},
        }
    },
)
def increase_in_solar_energy_technology_ratio_lv3():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_solar_energy_technology_ratio_lv3()


_integ_increase_in_solar_energy_technology_ratio_lv3 = Integ(
    lambda: inflow_isetlv3() - outflow_isetlv3(),
    lambda: effectiveness_isetr() * delay_time_isetr(),
    "_integ_increase_in_solar_energy_technology_ratio_lv3",
)


@component.add(
    name="Increase in Solar Installation Technology Ratio",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_isitrlv3": 1},
)
def increase_in_solar_installation_technology_ratio():
    """
    Increase in Solar Installation Technology Ratio due to investments in solar energy installation capacity.
    """
    return outflow_isitrlv3()


@component.add(
    name="Increase in Solar Installation Technology Ratio LV1",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_solar_installation_technology_ratio_lv1": 1},
    other_deps={
        "_integ_increase_in_solar_installation_technology_ratio_lv1": {
            "initial": {"increase_in_solar_installation_technology_ratio_lv3": 1},
            "step": {"inflow_isitrlv1": 1, "outflow_isitrlv1": 1},
        }
    },
)
def increase_in_solar_installation_technology_ratio_lv1():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_solar_installation_technology_ratio_lv1()


_integ_increase_in_solar_installation_technology_ratio_lv1 = Integ(
    lambda: inflow_isitrlv1() - outflow_isitrlv1(),
    lambda: increase_in_solar_installation_technology_ratio_lv3(),
    "_integ_increase_in_solar_installation_technology_ratio_lv1",
)


@component.add(
    name="Increase in Solar Installation Technology Ratio LV2",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_solar_installation_technology_ratio_lv2": 1},
    other_deps={
        "_integ_increase_in_solar_installation_technology_ratio_lv2": {
            "initial": {"increase_in_solar_installation_technology_ratio_lv3": 1},
            "step": {"inflow_isitrlv2": 1, "outflow_isitrlv2": 1},
        }
    },
)
def increase_in_solar_installation_technology_ratio_lv2():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_solar_installation_technology_ratio_lv2()


_integ_increase_in_solar_installation_technology_ratio_lv2 = Integ(
    lambda: inflow_isitrlv2() - outflow_isitrlv2(),
    lambda: increase_in_solar_installation_technology_ratio_lv3(),
    "_integ_increase_in_solar_installation_technology_ratio_lv2",
)


@component.add(
    name="Increase in Solar Installation Technology Ratio LV3",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_solar_installation_technology_ratio_lv3": 1},
    other_deps={
        "_integ_increase_in_solar_installation_technology_ratio_lv3": {
            "initial": {"effectiveness_isitr": 1, "delay_time_isitr": 1},
            "step": {"inflow_isitrlv3": 1, "outflow_isitrlv3": 1},
        }
    },
)
def increase_in_solar_installation_technology_ratio_lv3():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_solar_installation_technology_ratio_lv3()


_integ_increase_in_solar_installation_technology_ratio_lv3 = Integ(
    lambda: inflow_isitrlv3() - outflow_isitrlv3(),
    lambda: effectiveness_isitr() * delay_time_isitr(),
    "_integ_increase_in_solar_installation_technology_ratio_lv3",
)


@component.add(
    name="Indicated Solar Energy Price",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cost_of_solar_energy": 1, "desired_solar_energy_gross_margin": 1},
)
def indicated_solar_energy_price():
    """
    Indicated solar energy price accounting for unit cost and gross margin.
    """
    return cost_of_solar_energy() * (1 + desired_solar_energy_gross_margin())


@component.add(
    name="Inflow ISETLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effectiveness_isetr": 1},
)
def inflow_isetlv1():
    return effectiveness_isetr()


@component.add(
    name="Inflow ISETLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_isetlv1": 1},
)
def inflow_isetlv2():
    return outflow_isetlv1()


@component.add(
    name="Inflow ISETLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_isetlv2": 1},
)
def inflow_isetlv3():
    return outflow_isetlv2()


@component.add(
    name="Inflow ISITRLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effectiveness_isitr": 1},
)
def inflow_isitrlv1():
    return effectiveness_isitr()


@component.add(
    name="Inflow ISITRLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_isitrlv1": 1},
)
def inflow_isitrlv2():
    return outflow_isitrlv1()


@component.add(
    name="Inflow ISITRLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_isitrlv2": 1},
)
def inflow_isitrlv3():
    return outflow_isitrlv2()


@component.add(
    name="INIT Cumulative Solar Produced", comp_type="Constant", comp_subtype="Normal"
)
def init_cumulative_solar_produced():
    return 0


@component.add(
    name="INIT SETRN", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def init_setrn():
    """
    Initial Solar Energy Technology Ratio.
    """
    return 0


@component.add(
    name="INIT SIC", units="m*m", comp_type="Constant", comp_subtype="Normal"
)
def init_sic():
    """
    Initial installed capacity to transform sun radiation into energy.
    """
    return 400


@component.add(
    name="INIT SITRN", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def init_sitrn():
    """
    Initial Solar Installation Technology Ratio.
    """
    return 0


@component.add(
    name="INIT Unit Cost of Solar Capacity Installation",
    units="$/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_unit_cost_of_solar_capacity_installation():
    """
    Initial unit cost per unit solar capacity installation.
    """
    return 2000000000.0


@component.add(
    name="Installation of Solar Capacity Rate",
    units="m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "productivity_of_investment_in_solar_capacity_installation": 1,
        "solar_infrastructure_adjustment": 1,
    },
)
def installation_of_solar_capacity_rate():
    """
    Rate of new solar capacity installation.
    """
    return (
        productivity_of_investment_in_solar_capacity_installation()
        * solar_infrastructure_adjustment()
    )


@component.add(
    name="Investment in Solar Capacity",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "installation_of_solar_capacity_rate": 1,
        "unit_cost_of_solar_capacity_installation": 1,
        "efficiency_of_solar_installed_capacity": 1,
        "solar_capacity_aging_time": 1,
    },
)
def investment_in_solar_capacity():
    """
    Amount of resources dedicated to solar energy capacity development.
    """
    return (
        installation_of_solar_capacity_rate()
        * unit_cost_of_solar_capacity_installation()
        * efficiency_of_solar_installed_capacity()
        * solar_capacity_aging_time()
    )


@component.add(
    name="Investment in Solar Energy Efficiency",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_solar_energy_technology": 1,
        "fraction_invested_in_solar_energy_installation": 1,
    },
)
def investment_in_solar_energy_efficiency():
    """
    Total investments in solar conversion efficiency technology.
    """
    return investment_in_solar_energy_technology() * (
        1 - fraction_invested_in_solar_energy_installation()
    )


@component.add(
    name="Investment in Solar Energy Installation",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_solar_energy_technology": 1,
        "fraction_invested_in_solar_energy_installation": 1,
    },
)
def investment_in_solar_energy_installation():
    """
    Total investments in solar energy capacity.
    """
    return (
        investment_in_solar_energy_technology()
        * fraction_invested_in_solar_energy_installation()
    )


@component.add(
    name="Investment in Solar Energy Technology",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fraction_of_revenue_invested_in_solar_technology": 1,
        "solar_energy_revenue": 1,
    },
)
def investment_in_solar_energy_technology():
    """
    Investments in development of solar conversion efficiency technology and production capability.
    """
    return fraction_of_revenue_invested_in_solar_technology() * solar_energy_revenue()


@component.add(
    name="kW into GW", units="kW/GW", comp_type="Constant", comp_subtype="Normal"
)
def kw_into_gw():
    """
    Coefficient to convert kilowatts into gigawatts.
    """
    return 1000000.0


@component.add(
    name="kWh into Mtoe",
    units="Mtoe/(kW*Hour)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def kwh_into_mtoe():
    """
    Coefficient to convert kWh into Mtoe.
    """
    return 8.6e-11


@component.add(
    name="kWh into Mtoe peak hour",
    units="Mtoe/kW",
    comp_type="Constant",
    comp_subtype="Normal",
)
def kwh_into_mtoe_peak_hour():
    """
    Coefficient to convert kWh into Mtoe peak hour.
    """
    return 8.6e-11


@component.add(
    name="Max Power Point",
    units="W",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "solar_conversion_efficiency": 1,
        "standard_test_conditions": 1,
        "solar_installed_capacity": 1,
    },
)
def max_power_point():
    """
    Max Power Point measured at Standard Test Conditions for installed solar energy production capacity and current solar conversion efficiency.
    """
    return (
        solar_conversion_efficiency()
        * standard_test_conditions()
        * solar_installed_capacity()
    )


@component.add(
    name="Max Power Point GW",
    units="GW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_power_point": 1, "w_into_gw": 1},
)
def max_power_point_gw():
    """
    Solar Max Power Point measured in GW.
    """
    return max_power_point() / w_into_gw()


@component.add(name="MAXSCE", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def maxsce():
    """
    Maximal efficiency of solar radiation conversion.
    """
    return 0.4


@component.add(name="MAXSIE", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def maxsie():
    """
    Maximal value of Solar Installation Efficiency factor.
    """
    return 1


@component.add(name="MINSCE", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def minsce():
    """
    Minimal and initial efficiency of solar radiation conversion.
    """
    return 0.13


@component.add(name="MINSIE", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def minsie():
    """
    Minimal and initial value of Solar Installation Efficiency factor.
    """
    return 0.01


@component.add(
    name="Outflow ISETLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_solar_energy_technology_ratio_lv1": 1,
        "delay_time_isetr": 1,
    },
)
def outflow_isetlv1():
    return increase_in_solar_energy_technology_ratio_lv1() / delay_time_isetr()


@component.add(
    name="Outflow ISETLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_solar_energy_technology_ratio_lv2": 1,
        "delay_time_isetr": 1,
    },
)
def outflow_isetlv2():
    return increase_in_solar_energy_technology_ratio_lv2() / delay_time_isetr()


@component.add(
    name="Outflow ISETLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_solar_energy_technology_ratio_lv3": 1,
        "delay_time_isetr": 1,
    },
)
def outflow_isetlv3():
    return increase_in_solar_energy_technology_ratio_lv3() / delay_time_isetr()


@component.add(
    name="Outflow ISITRLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_solar_installation_technology_ratio_lv1": 1,
        "delay_time_isitr": 1,
    },
)
def outflow_isitrlv1():
    return increase_in_solar_installation_technology_ratio_lv1() / delay_time_isitr()


@component.add(
    name="Outflow ISITRLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_solar_installation_technology_ratio_lv2": 1,
        "delay_time_isitr": 1,
    },
)
def outflow_isitrlv2():
    return increase_in_solar_installation_technology_ratio_lv2() / delay_time_isitr()


@component.add(
    name="Outflow ISITRLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_solar_installation_technology_ratio_lv3": 1,
        "delay_time_isitr": 1,
    },
)
def outflow_isitrlv3():
    return increase_in_solar_installation_technology_ratio_lv3() / delay_time_isitr()


@component.add(
    name="Possible Solar Energy Production",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "solar_conversion_efficiency_factor": 1,
        "sun_radiation": 1,
        "solar_installed_capacity": 1,
        "time_fl": 1,
        "solar_conversion_efficiency": 1,
        "kwh_into_mtoe": 1,
    },
)
def possible_solar_energy_production():
    """
    Potential solar energy production per year due to available production capability, weather conditions and technical developments.
    """
    return (
        solar_conversion_efficiency_factor()
        * sun_radiation()
        * solar_installed_capacity()
        * time_fl()
        * solar_conversion_efficiency()
        * kwh_into_mtoe()
    )


@component.add(
    name="Production to Installation Ratio",
    units="Mtoe/(m*m*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"solar_energy_production": 1, "solar_installed_capacity": 1},
)
def production_to_installation_ratio():
    """
    Ratio of solar energy production to available production capacity.
    """
    return solar_energy_production() / solar_installed_capacity()


@component.add(
    name="Productivity of Investment in Solar Capacity Installation",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "impact_of_space_on_capacity_installation": 1,
        "solar_installation_efficiency": 1,
    },
)
def productivity_of_investment_in_solar_capacity_installation():
    """
    Productivity of solar capacity installation taking into account the level of available capacities and technology development state.
    """
    return impact_of_space_on_capacity_installation() * solar_installation_efficiency()


@component.add(
    name="Ramp Investment Period",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fraction_of_revenue_invested_in_solar_technology_ramp_investment_period_variation": 1,
        "time": 1,
    },
)
def ramp_investment_period():
    """
    Period of fractional investments in new energy technologies.
    """
    return 100 + step(
        __data["time"],
        fraction_of_revenue_invested_in_solar_technology_ramp_investment_period_variation()
        - 100,
        2020,
    )


@component.add(
    name="Reference Cost of Solar Energy Production",
    units="$/((m*m)*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"variable14_solar_cost": 1},
)
def reference_cost_of_solar_energy_production():
    """
    Reference cost of unit solar energy production per year.
    """
    return variable14_solar_cost()


@component.add(
    name="Renewable Energy Technology Development Time Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def renewable_energy_technology_development_time_variation():
    return 50


@component.add(
    name="Renewable Final Investment Fraction Variation",
    comp_type="Constant",
    comp_subtype="Normal",
)
def renewable_final_investment_fraction_variation():
    return 0.03


@component.add(
    name="Renewable Installation Technology Development Time Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def renewable_installation_technology_development_time_variation():
    return 100


@component.add(name="SA S", units="m*m", comp_type="Constant", comp_subtype="Normal")
def sa_s():
    """
    Total area available for solar energy production capacities.
    """
    return 500000000000.0


@component.add(
    name="SA Var S",
    units="m*m",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_sa_var_s": 1},
    other_deps={
        "_smooth_sa_var_s": {
            "initial": {"sa_s": 1, "time": 1},
            "step": {"sa_s": 1, "time": 1},
        }
    },
)
def sa_var_s():
    """
    Total area available for solar energy production capacities.
    """
    return 500000000000.0 + _smooth_sa_var_s()


_smooth_sa_var_s = Smooth(
    lambda: step(__data["time"], sa_s() - 500000000000.0, 2020),
    lambda: 1,
    lambda: step(__data["time"], sa_s() - 500000000000.0, 2020),
    lambda: 1,
    "_smooth_sa_var_s",
)


@component.add(
    name="Sensitivity of Solar Energy Price to Supply and Demand",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sensitivity_of_solar_energy_price_to_supply_and_demand():
    """
    Sensitivity of Solar Energy Price to Supply and Demand ratio.
    """
    return 0


@component.add(
    name="Solar Available Area",
    units="m*m",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"sa_var_s": 1, "_smooth_solar_available_area": 1},
    other_deps={
        "_smooth_solar_available_area": {
            "initial": {
                "solar_available_area_variation": 1,
                "sa_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "solar_available_area_variation": 1,
                "sa_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_production_variation_time": 1,
            },
        }
    },
)
def solar_available_area():
    """
    Total area available for solar energy production capacities.
    """
    return sa_var_s() + _smooth_solar_available_area()


_smooth_solar_available_area = Smooth(
    lambda: step(
        __data["time"], solar_available_area_variation() - sa_var_s(), 2020 + e_var_t()
    ),
    lambda: ssp_energy_production_variation_time(),
    lambda: step(
        __data["time"], solar_available_area_variation() - sa_var_s(), 2020 + e_var_t()
    ),
    lambda: 1,
    "_smooth_solar_available_area",
)


@component.add(
    name="Solar Available Area Variation",
    units="m*m",
    comp_type="Constant",
    comp_subtype="Normal",
)
def solar_available_area_variation():
    """
    Total area available for solar energy production capacities.
    """
    return 500000000000.0


@component.add(
    name="Solar Capacity Aging Rate",
    units="m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"solar_installed_capacity": 1, "solar_capacity_aging_time": 1},
)
def solar_capacity_aging_rate():
    """
    Aging rate of solar energy production capacities.
    """
    return solar_installed_capacity() / solar_capacity_aging_time()


@component.add(
    name="Solar Capacity Aging Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def solar_capacity_aging_time():
    """
    Average solar energy production capacity aging time.
    """
    return 20


@component.add(
    name="Solar Conversion Efficiency",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"minsce": 2, "solar_energy_technology_ratio": 2, "maxsce": 1},
)
def solar_conversion_efficiency():
    """
    Parameter indicating efficiency of solar radiation conversion at the current state of technical developments.
    """
    return minsce() + (maxsce() - minsce()) * (
        solar_energy_technology_ratio() / (solar_energy_technology_ratio() + 1)
    )


@component.add(
    name="Solar Conversion Efficiency Factor",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"variable2_solar": 1},
)
def solar_conversion_efficiency_factor():
    return variable2_solar()


@component.add(
    name="Solar Energy Demand to Supply Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_solar_demand": 1, "possible_solar_energy_production": 1},
)
def solar_energy_demand_to_supply_ratio():
    """
    Solar Energy Demand to Supply Ratio.
    """
    return total_solar_demand() / possible_solar_energy_production()


@component.add(
    name="Solar Energy Price",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "indicated_solar_energy_price": 1,
        "effect_of_solar_energy_demand_and_supply_on_price": 1,
    },
)
def solar_energy_price():
    """
    Actual solar energy price accounting for indicated solar energy price and effect of demand and supply.
    """
    return (
        indicated_solar_energy_price()
        * effect_of_solar_energy_demand_and_supply_on_price()
    )


@component.add(
    name="Solar Energy Price per kWh",
    units="$/(kW*Hour)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"solar_energy_price": 1, "kwh_into_mtoe": 1},
)
def solar_energy_price_per_kwh():
    """
    Actual solar energy price accounting for indicated solar energy price and effect of demand and supply measured in dollars per kWh.
    """
    return solar_energy_price() * kwh_into_mtoe()


@component.add(
    name="Solar Energy Production",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"solar_energy_production_rate": 1},
)
def solar_energy_production():
    """
    Total solar energy production per year.
    """
    return solar_energy_production_rate()


@component.add(
    name="Solar Energy Production Indicator",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"solar_energy_production": 1, "mtoe_into_ej": 1},
)
def solar_energy_production_indicator():
    return solar_energy_production() * mtoe_into_ej()


@component.add(
    name="Solar Energy Production Rate",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"possible_solar_energy_production": 1, "total_solar_demand": 1},
)
def solar_energy_production_rate():
    """
    Total solar energy production per year accounting for demand and potential production due to available production capability and technical developments.
    """
    return float(np.minimum(possible_solar_energy_production(), total_solar_demand()))


@component.add(
    name="Solar Energy Revenue",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"solar_energy_production": 1, "solar_energy_price": 1},
)
def solar_energy_revenue():
    """
    Total revenue in solar energy market.
    """
    return solar_energy_production() * solar_energy_price()


@component.add(
    name="Solar Energy Technology Development Time",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"renewable_energy_technology_development_time_variation": 1, "time": 1},
)
def solar_energy_technology_development_time():
    """
    Average time required to turn investments into concrete solar conversion efficiency technology developments. Since the simulation starts in 1900 it is a significant time.
    """
    return 50 + step(
        __data["time"],
        renewable_energy_technology_development_time_variation() - 50,
        2020,
    )


@component.add(
    name="Solar Energy Technology Ratio",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_solar_energy_technology_ratio": 1},
    other_deps={
        "_integ_solar_energy_technology_ratio": {
            "initial": {"init_setrn": 1},
            "step": {"increase_in_solar_energy_technology_ratio": 1},
        }
    },
)
def solar_energy_technology_ratio():
    """
    Solar Energy Technology Ratio increased due to investments in solar conversion efficiency.
    """
    return _integ_solar_energy_technology_ratio()


_integ_solar_energy_technology_ratio = Integ(
    lambda: increase_in_solar_energy_technology_ratio(),
    lambda: init_setrn(),
    "_integ_solar_energy_technology_ratio",
)


@component.add(
    name="Solar Final Investment",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"renewable_final_investment_fraction_variation": 1, "time": 1},
)
def solar_final_investment():
    """
    Eventual average level of investments in solar energy technology.
    """
    return 0.03 + step(
        __data["time"], renewable_final_investment_fraction_variation() - 0.03, 2020
    )


@component.add(
    name="Solar Infrastructure Adjustment",
    units="m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "solar_capacity_aging_rate": 1,
        "solar_installed_capacity": 1,
        "time_to_adjust_solar_infrastructure": 1,
        "desired_solar_installed_capacity": 1,
    },
)
def solar_infrastructure_adjustment():
    """
    Adjustment of Solar Infrastructure to the desired level over a specified adjustment time and accounting for constant infrastructure decrease due to aging process.
    """
    return (
        solar_capacity_aging_rate()
        + (desired_solar_installed_capacity() - solar_installed_capacity())
        / time_to_adjust_solar_infrastructure()
    )


@component.add(
    name="Solar Initial Investment",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def solar_initial_investment():
    """
    Initial level of fractional investments in solar energy technology.
    """
    return 0


@component.add(
    name="Solar Installation Efficiency",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"minsie": 2, "maxsie": 1, "solar_installation_technology_ratio": 2},
)
def solar_installation_efficiency():
    """
    Parameter indicating solar energy capacity installation efficiency at the current state of technical developments.
    """
    return minsie() + (maxsie() - minsie()) * (
        solar_installation_technology_ratio()
        / (solar_installation_technology_ratio() + 1)
    )


@component.add(
    name="Solar Installation Technology Development Time",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "renewable_installation_technology_development_time_variation": 1,
        "time": 1,
    },
)
def solar_installation_technology_development_time():
    """
    Average time required to turn investments into concrete solar energy production capacity. Since the simulation starts in 1900 it is a significant time.
    """
    return 100 + step(
        __data["time"],
        renewable_installation_technology_development_time_variation() - 100,
        2020,
    )


@component.add(
    name="Solar Installation Technology Ratio",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_solar_installation_technology_ratio": 1},
    other_deps={
        "_integ_solar_installation_technology_ratio": {
            "initial": {"init_sitrn": 1},
            "step": {"increase_in_solar_installation_technology_ratio": 1},
        }
    },
)
def solar_installation_technology_ratio():
    """
    Solar Installation Technology Ratio increased due to investments in solar energy capacity installation efficiency.
    """
    return _integ_solar_installation_technology_ratio()


_integ_solar_installation_technology_ratio = Integ(
    lambda: increase_in_solar_installation_technology_ratio(),
    lambda: init_sitrn(),
    "_integ_solar_installation_technology_ratio",
)


@component.add(
    name="Solar Installed Capacity",
    units="m*m",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_solar_installed_capacity": 1},
    other_deps={
        "_integ_solar_installed_capacity": {
            "initial": {"init_sic": 1},
            "step": {
                "installation_of_solar_capacity_rate": 1,
                "solar_capacity_aging_rate": 1,
            },
        }
    },
)
def solar_installed_capacity():
    """
    Installed capacity to transform solar radiation into energy.
    """
    return _integ_solar_installed_capacity()


_integ_solar_installed_capacity = Integ(
    lambda: installation_of_solar_capacity_rate() - solar_capacity_aging_rate(),
    lambda: init_sic(),
    "_integ_solar_installed_capacity",
)


@component.add(
    name="Solar Investment Fraction Finish",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_time": 1, "ramp_investment_period": 1},
)
def solar_investment_fraction_finish():
    """
    End of fractional investments in solar energy technology.
    """
    return initial_time() + ramp_investment_period()


@component.add(
    name="Solar Investment Fraction Slope",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "solar_final_investment": 1,
        "solar_initial_investment": 1,
        "ramp_investment_period": 1,
    },
)
def solar_investment_fraction_slope():
    """
    Intensity of increase in investments in solar energy technology.
    """
    return (
        float(np.abs(solar_final_investment() - solar_initial_investment()))
        / ramp_investment_period()
    )


@component.add(
    name="Solar Investment Fraction Start",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_time": 1},
)
def solar_investment_fraction_start():
    """
    Start of investments in solar energy technology.
    """
    return initial_time()


@component.add(
    name="Solar Learning Curve Strength",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fraction_for_solar_learning_curve_strength": 1},
)
def solar_learning_curve_strength():
    """
    Strength of learning curve with which the solar energy costs are influenced.
    """
    return float(np.log(1 - fraction_for_solar_learning_curve_strength())) / float(
        np.log(2)
    )


@component.add(
    name="Standard Test Conditions",
    units="W/(m*m)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def standard_test_conditions():
    """
    Standard Test Conditions assuming irradiance of 1000 W/(m*m) to calculate Max Power Point.
    """
    return 1000


@component.add(
    name="Sun Radiation", units="kW/(m*m)", comp_type="Constant", comp_subtype="Normal"
)
def sun_radiation():
    """
    Average sun radiation in kW per sqr meter.
    """
    return 0.5


@component.add(
    name="Table for FISEI",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_table_for_fisei"},
)
def table_for_fisei(x, final_subs=None):
    """
    Table determining order by which technology investments are dedicated to energy and installation efficiency. For small Solar Installation Efficiency, in order to secure sufficient production capacity, more investments are directed to infrastructure. Once the Solar Installation Efficiency increases the investments are redirected to solar conversion efficiency technologies.
    """
    return _hardcodedlookup_table_for_fisei(x, final_subs)


_hardcodedlookup_table_for_fisei = HardcodedLookups(
    [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
    [0.8, 0.8, 0.7, 0.5, 0.2, 0.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_for_fisei",
)


@component.add(
    name="Time FL",
    units="Hour/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"weather_factor": 1, "hours_per_year": 1},
)
def time_fl():
    """
    Average time of sun availability.
    """
    return weather_factor() * hours_per_year()


@component.add(
    name="Time to Adjust Solar Infrastructure",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_adjust_solar_infrastructure():
    """
    Time to adjust Solar Infrastructure to the desired level.
    """
    return 5


@component.add(
    name="Total Solar Demand",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_demand": 1, "market_share_solar": 1},
)
def total_solar_demand():
    """
    Total demand for solar energy.
    """
    return energy_demand() * market_share_solar()


@component.add(
    name="Total Solar Demand GW",
    units="GW/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_solar_demand": 1, "kwh_into_mtoe_peak_hour": 1, "kw_into_gw": 1},
)
def total_solar_demand_gw():
    """
    Total demand for solar energy measured in GW.
    """
    return total_solar_demand() / kwh_into_mtoe_peak_hour() / kw_into_gw()


@component.add(
    name="Unit Cost of Solar Capacity Installation",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "init_unit_cost_of_solar_capacity_installation": 1,
        "impact_of_learning_on_solar_unit_cost_of_technology_pc": 1,
    },
)
def unit_cost_of_solar_capacity_installation():
    """
    Unit Cost of Solar Capacity Installation. Determined by Productivity of Investment in Solar Capacity Installation.
    """
    return (
        init_unit_cost_of_solar_capacity_installation()
        * impact_of_learning_on_solar_unit_cost_of_technology_pc()
    )


@component.add(
    name="Unit Cost of Solar Energy Production",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_cost_of_solar_energy_production": 1,
        "production_to_installation_ratio": 1,
    },
)
def unit_cost_of_solar_energy_production():
    """
    Unit cost of solar capacity installation per energy unit.
    """
    return (
        reference_cost_of_solar_energy_production() / production_to_installation_ratio()
    )


@component.add(
    name="W into GW", units="W/GW", comp_type="Constant", comp_subtype="Normal"
)
def w_into_gw():
    """
    Coefficient to convert watts into gigawatts
    """
    return 1000000000.0


@component.add(
    name="Weather Factor", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def weather_factor():
    """
    Percentage of total hours per year when solar energy can be produced.
    """
    return 0.1
