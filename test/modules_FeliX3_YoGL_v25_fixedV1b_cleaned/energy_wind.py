"""
Module energy_wind
Translated using PySD version 3.14.3
"""

@component.add(
    name="Average Capacity per SqMeter",
    units="kW/(m*m)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"variable3_wind": 1},
)
def average_capacity_per_sqmeter():
    """
    Average wind energy production from one sqr meter of wind installed capacity.
    """
    return variable3_wind()


@component.add(
    name="Cost of Wind Energy",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "unit_cost_of_wind_capacity_installation": 1,
        "unit_cost_of_wind_energy_production": 1,
    },
)
def cost_of_wind_energy():
    """
    Cost of wind energy production assuming an impact of learning curve.
    """
    return (
        unit_cost_of_wind_capacity_installation()
        + unit_cost_of_wind_energy_production()
    )


@component.add(
    name="Cumulative Wind Energy Produced",
    units="Mtoe",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_wind_energy_produced": 1},
    other_deps={
        "_integ_cumulative_wind_energy_produced": {
            "initial": {"init_cumulative_wind_produced": 1},
            "step": {"wind_energy_production": 1},
        }
    },
)
def cumulative_wind_energy_produced():
    """
    Cumulative wind energy that has been produced.
    """
    return _integ_cumulative_wind_energy_produced()


_integ_cumulative_wind_energy_produced = Integ(
    lambda: wind_energy_production(),
    lambda: init_cumulative_wind_produced(),
    "_integ_cumulative_wind_energy_produced",
)


@component.add(
    name="Delay Time IWETR",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_energy_technology_development_time": 1},
)
def delay_time_iwetr():
    return wind_energy_technology_development_time() / 3


@component.add(
    name="Delay Time IWIR",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_installation_technology_development_time": 1},
)
def delay_time_iwir():
    return wind_installation_technology_development_time() / 3


@component.add(
    name="Desired Wind Energy Gross Margin",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def desired_wind_energy_gross_margin():
    """
    Desired Gross Margin per unit of wind energy.
    """
    return 0.2


@component.add(
    name="Desired Wind Installed Capacity",
    units="m*m",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_wind_demand": 1, "efficiency_of_wind_installed_capacity": 1},
)
def desired_wind_installed_capacity():
    """
    Desired Wind Installed Capacity accounting for Total Wind Demand and Efficiency of Wind Installed Capacity.
    """
    return total_wind_demand() / efficiency_of_wind_installed_capacity()


@component.add(
    name="Effect of Wind Energy Demand and Supply on Price",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_wind_demand": 1,
        "potential_wind_energy_production": 1,
        "sensitivity_of_wind_energy_price_to_supply_and_demand": 1,
    },
)
def effect_of_wind_energy_demand_and_supply_on_price():
    """
    Effect of Wind Demand and Supply ratio on actual wind energy price.
    """
    return (
        total_wind_demand() / potential_wind_energy_production()
    ) ** sensitivity_of_wind_energy_price_to_supply_and_demand()


@component.add(
    name="Effectiveness IWETR",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_wind_energy_efficiency": 1,
        "effectiveness_of_investment_in_wind_energy_technology": 1,
    },
)
def effectiveness_iwetr():
    return (
        investment_in_wind_energy_efficiency()
        * effectiveness_of_investment_in_wind_energy_technology()
    )


@component.add(
    name="Effectiveness IWITR",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_wind_energy_installation": 1,
        "effectiveness_of_investment_in_wind_installation_technology": 1,
    },
)
def effectiveness_iwitr():
    return (
        investment_in_wind_energy_installation()
        * effectiveness_of_investment_in_wind_installation_technology()
    )


@component.add(
    name="Effectiveness of Investment in Wind Energy Technology",
    units="1/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effectiveness_of_investment_in_renewable_energy_technology_variation": 1,
        "time": 1,
    },
)
def effectiveness_of_investment_in_wind_energy_technology():
    """
    Effectivenes of resources dedicated to wind conversion efficiency technology development.
    """
    return 1e-09 + step(
        __data["time"],
        effectiveness_of_investment_in_renewable_energy_technology_variation() - 1e-09,
        2020,
    )


@component.add(
    name="Effectiveness of Investment in Wind Installation Technology",
    units="1/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effectiveness_of_investment_in_renewable_installation_technology_variation": 1,
        "time": 1,
    },
)
def effectiveness_of_investment_in_wind_installation_technology():
    """
    Effectiveness of resources dedicated to wind energy capacity efficiency technology development.
    """
    return 1e-10 + step(
        __data["time"],
        effectiveness_of_investment_in_renewable_installation_technology_variation()
        - 1e-10,
        2020,
    )


@component.add(
    name="Efficiency of Wind Installed Capacity",
    units="Mtoe/(Year*m*m)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_wind_energy_production": 1, "wind_installed_capacity": 1},
)
def efficiency_of_wind_installed_capacity():
    """
    Total production efficiency of Wind Installed Capacity for given technology developments.
    """
    return zidz(potential_wind_energy_production(), wind_installed_capacity())


@component.add(
    name="Fraction for Wind Learning Curve Strength",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fraction_for_wind_and_solar_learning_curve_strength_variation": 1,
        "time": 1,
    },
)
def fraction_for_wind_learning_curve_strength():
    """
    Fraction for Wind Learning Curve Strength indicating by what percentage the wind energy cost will drop for each doubling of wind installed capacity.
    """
    return 0.2 + step(
        __data["time"],
        fraction_for_wind_and_solar_learning_curve_strength_variation() - 0.2,
        2020,
    )


@component.add(
    name="Fraction Invested in Wind Energy Installation",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_installation_efficiency": 1, "table_for_fiwei": 1},
)
def fraction_invested_in_wind_energy_installation():
    """
    Fraction of investments in wind energy technology dedicated to capacity.
    """
    return table_for_fiwei(wind_installation_efficiency())


@component.add(
    name="Fraction of Revenue Invested in Wind Technology",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wind_investment_fraction_slope": 1,
        "wind_investment_fraction_start": 1,
        "wind_investment_fraction_finish": 1,
        "time": 1,
    },
)
def fraction_of_revenue_invested_in_wind_technology():
    """
    Parameter to take into account historical increase of the wind energy significance and over time greater resources dedicated to the technology development.
    """
    return ramp(
        __data["time"],
        wind_investment_fraction_slope(),
        wind_investment_fraction_start(),
        wind_investment_fraction_finish(),
    )


@component.add(
    name="Impact of Learning on Wind Unit Cost of Technology",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wind_installed_capacity": 1,
        "init_wic": 1,
        "wind_learning_curve_strength": 1,
    },
)
def impact_of_learning_on_wind_unit_cost_of_technology():
    """
    Impact of learning curve on wind energy cost.
    """
    return (wind_installed_capacity() / init_wic()) ** wind_learning_curve_strength()


@component.add(
    name="Impact of Space on Wind Capacity Installation",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_installed_capacity": 1, "wind_available_area": 1},
)
def impact_of_space_on_wind_capacity_installation():
    """
    Ratio of currently installed wind capacity to total possible.
    """
    return float(np.maximum(0, 1 - wind_installed_capacity() / wind_available_area()))


@component.add(
    name="Increase in Wind Energy Technology Ratio",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_iwetrlv3": 1},
)
def increase_in_wind_energy_technology_ratio():
    """
    Increase in Wind Energy Technology Ratio due to investments in wind conversion efficiency technology and their productivity.
    """
    return outflow_iwetrlv3()


@component.add(
    name="Increase in Wind Energy Technology Ratio LV1",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_wind_energy_technology_ratio_lv1": 1},
    other_deps={
        "_integ_increase_in_wind_energy_technology_ratio_lv1": {
            "initial": {"increase_in_wind_energy_technology_ratio_lv3": 1},
            "step": {"inflow_iwetrlv1": 1, "outflow_iwetrlv1": 1},
        }
    },
)
def increase_in_wind_energy_technology_ratio_lv1():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_wind_energy_technology_ratio_lv1()


_integ_increase_in_wind_energy_technology_ratio_lv1 = Integ(
    lambda: inflow_iwetrlv1() - outflow_iwetrlv1(),
    lambda: increase_in_wind_energy_technology_ratio_lv3(),
    "_integ_increase_in_wind_energy_technology_ratio_lv1",
)


@component.add(
    name="Increase in Wind Energy Technology Ratio LV2",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_wind_energy_technology_ratio_lv2": 1},
    other_deps={
        "_integ_increase_in_wind_energy_technology_ratio_lv2": {
            "initial": {"increase_in_wind_energy_technology_ratio_lv3": 1},
            "step": {"inflow_iwetrlv2": 1, "outflow_iwetrlv2": 1},
        }
    },
)
def increase_in_wind_energy_technology_ratio_lv2():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_wind_energy_technology_ratio_lv2()


_integ_increase_in_wind_energy_technology_ratio_lv2 = Integ(
    lambda: inflow_iwetrlv2() - outflow_iwetrlv2(),
    lambda: increase_in_wind_energy_technology_ratio_lv3(),
    "_integ_increase_in_wind_energy_technology_ratio_lv2",
)


@component.add(
    name="Increase in Wind Energy Technology Ratio LV3",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_wind_energy_technology_ratio_lv3": 1},
    other_deps={
        "_integ_increase_in_wind_energy_technology_ratio_lv3": {
            "initial": {"effectiveness_iwetr": 1, "delay_time_iwetr": 1},
            "step": {"inflow_iwetrlv3": 1, "outflow_iwetrlv3": 1},
        }
    },
)
def increase_in_wind_energy_technology_ratio_lv3():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_wind_energy_technology_ratio_lv3()


_integ_increase_in_wind_energy_technology_ratio_lv3 = Integ(
    lambda: inflow_iwetrlv3() - outflow_iwetrlv3(),
    lambda: effectiveness_iwetr() * delay_time_iwetr(),
    "_integ_increase_in_wind_energy_technology_ratio_lv3",
)


@component.add(
    name="Increase in Wind Installation Technology Ratio",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_iwitrlv3": 1},
)
def increase_in_wind_installation_technology_ratio():
    """
    Increase in Wind Installation Technology Ratio due to investments in wind energy installation capacity.
    """
    return outflow_iwitrlv3()


@component.add(
    name="Increase in Wind Installation Technology Ratio LV1",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_wind_installation_technology_ratio_lv1": 1},
    other_deps={
        "_integ_increase_in_wind_installation_technology_ratio_lv1": {
            "initial": {"increase_in_wind_installation_technology_ratio_lv3": 1},
            "step": {"inflow_iwitrlv1": 1, "outflow_iwitrlv1": 1},
        }
    },
)
def increase_in_wind_installation_technology_ratio_lv1():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_wind_installation_technology_ratio_lv1()


_integ_increase_in_wind_installation_technology_ratio_lv1 = Integ(
    lambda: inflow_iwitrlv1() - outflow_iwitrlv1(),
    lambda: increase_in_wind_installation_technology_ratio_lv3(),
    "_integ_increase_in_wind_installation_technology_ratio_lv1",
)


@component.add(
    name="Increase in Wind Installation Technology Ratio LV2",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_wind_installation_technology_ratio_lv2": 1},
    other_deps={
        "_integ_increase_in_wind_installation_technology_ratio_lv2": {
            "initial": {"increase_in_wind_installation_technology_ratio_lv3": 1},
            "step": {"inflow_iwitrlv2": 1, "ourflow_iwitrlv2": 1},
        }
    },
)
def increase_in_wind_installation_technology_ratio_lv2():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_wind_installation_technology_ratio_lv2()


_integ_increase_in_wind_installation_technology_ratio_lv2 = Integ(
    lambda: inflow_iwitrlv2() - ourflow_iwitrlv2(),
    lambda: increase_in_wind_installation_technology_ratio_lv3(),
    "_integ_increase_in_wind_installation_technology_ratio_lv2",
)


@component.add(
    name="Increase in Wind Installation Technology Ratio LV3",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_increase_in_wind_installation_technology_ratio_lv3": 1},
    other_deps={
        "_integ_increase_in_wind_installation_technology_ratio_lv3": {
            "initial": {"effectiveness_iwitr": 1, "delay_time_iwir": 1},
            "step": {"inflow_iwitrlv3": 1, "outflow_iwitrlv3": 1},
        }
    },
)
def increase_in_wind_installation_technology_ratio_lv3():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_increase_in_wind_installation_technology_ratio_lv3()


_integ_increase_in_wind_installation_technology_ratio_lv3 = Integ(
    lambda: inflow_iwitrlv3() - outflow_iwitrlv3(),
    lambda: effectiveness_iwitr() * delay_time_iwir(),
    "_integ_increase_in_wind_installation_technology_ratio_lv3",
)


@component.add(
    name="Indicated Wind Energy Price",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cost_of_wind_energy": 1, "desired_wind_energy_gross_margin": 1},
)
def indicated_wind_energy_price():
    """
    Indicated wind energy price accounting for unit cost and gross margin.
    """
    return cost_of_wind_energy() * (1 + desired_wind_energy_gross_margin())


@component.add(
    name="Inflow IWETRLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effectiveness_iwetr": 1},
)
def inflow_iwetrlv1():
    return effectiveness_iwetr()


@component.add(
    name="Inflow IWETRLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_iwetrlv1": 1},
)
def inflow_iwetrlv2():
    return outflow_iwetrlv1()


@component.add(
    name="Inflow IWETRLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_iwetrlv2": 1},
)
def inflow_iwetrlv3():
    return outflow_iwetrlv2()


@component.add(
    name="Inflow IWITRLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effectiveness_iwitr": 1},
)
def inflow_iwitrlv1():
    return effectiveness_iwitr()


@component.add(
    name="Inflow IWITRLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_iwitrlv1": 1},
)
def inflow_iwitrlv2():
    return outflow_iwitrlv1()


@component.add(
    name="Inflow IWITRLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ourflow_iwitrlv2": 1},
)
def inflow_iwitrlv3():
    return ourflow_iwitrlv2()


@component.add(
    name="INIT Cumulative Wind Produced", comp_type="Constant", comp_subtype="Normal"
)
def init_cumulative_wind_produced():
    return 0


@component.add(
    name="INIT Unit Cost of Wind Capacity Installation",
    units="$/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_unit_cost_of_wind_capacity_installation():
    """
    Initial unit cost per unit wind capacity installation.
    """
    return 2000000000.0


@component.add(
    name="INIT WETRN", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def init_wetrn():
    """
    Initial Wind Energy Technology Ratio.
    """
    return 0


@component.add(
    name="INIT WIC", units="m*m", comp_type="Constant", comp_subtype="Normal"
)
def init_wic():
    """
    Initial installed capacity to transform wind into energy.
    """
    return 4000


@component.add(
    name="INIT WITRN", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def init_witrn():
    """
    Initial Wind Installation Technology Ratio.
    """
    return 0


@component.add(
    name="Installation of Wind Capacity Rate",
    units="m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "productivity_of_investment_in_wind_capacity_installation": 1,
        "wind_infrastructure_adjustment": 1,
    },
)
def installation_of_wind_capacity_rate():
    """
    Rate of new wind capacity installation.
    """
    return (
        productivity_of_investment_in_wind_capacity_installation()
        * wind_infrastructure_adjustment()
    )


@component.add(
    name="Investment in Wind Capacity",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "installation_of_wind_capacity_rate": 1,
        "unit_cost_of_wind_capacity_installation": 1,
        "efficiency_of_wind_installed_capacity": 1,
        "wind_aging_time": 1,
    },
)
def investment_in_wind_capacity():
    """
    Amount of resources dedicated to wind energy capacity development.
    """
    return (
        installation_of_wind_capacity_rate()
        * unit_cost_of_wind_capacity_installation()
        * efficiency_of_wind_installed_capacity()
        * wind_aging_time()
    )


@component.add(
    name="Investment in Wind Energy Efficiency",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_wind_energy_technology": 1,
        "fraction_invested_in_wind_energy_installation": 1,
    },
)
def investment_in_wind_energy_efficiency():
    """
    Total investments in wind conversion efficiency technology.
    """
    return investment_in_wind_energy_technology() * (
        1 - fraction_invested_in_wind_energy_installation()
    )


@component.add(
    name="Investment in Wind Energy Installation",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_wind_energy_technology": 1,
        "fraction_invested_in_wind_energy_installation": 1,
    },
)
def investment_in_wind_energy_installation():
    """
    Total investments in wind energy capacity.
    """
    return (
        investment_in_wind_energy_technology()
        * fraction_invested_in_wind_energy_installation()
    )


@component.add(
    name="Investment in Wind Energy Technology",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fraction_of_revenue_invested_in_wind_technology": 1,
        "wind_energy_revenue": 1,
    },
)
def investment_in_wind_energy_technology():
    """
    Investments in development of wind conversion efficiency technology and production capability.
    """
    return fraction_of_revenue_invested_in_wind_technology() * wind_energy_revenue()


@component.add(
    name="kW into TW", units="kW/TW", comp_type="Constant", comp_subtype="Normal"
)
def kw_into_tw():
    """
    Coefficient to convert kilowatts into terawatts.
    """
    return 10000000000.0


@component.add(
    name="Max Wind Power Point",
    units="kW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wind_installed_capacity": 1,
        "average_capacity_per_sqmeter": 1,
        "wind_capacity_factor": 1,
    },
)
def max_wind_power_point():
    """
    Max Power Point measured at Standard Test Conditions for installed wind energy production capacity and current wind conversion efficiency.
    """
    return (
        wind_installed_capacity()
        * average_capacity_per_sqmeter()
        * wind_capacity_factor()
    )


@component.add(
    name="Max Wind Power Point GW",
    units="GW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_wind_power_point": 1, "kw_into_gw": 1},
)
def max_wind_power_point_gw():
    """
    Wind Max Power Point measured in GW.
    """
    return max_wind_power_point() / kw_into_gw()


@component.add(
    name="Max Wind Power Point TW",
    units="TW",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_wind_power_point": 1, "kw_into_tw": 1},
)
def max_wind_power_point_tw():
    """
    Wind Max Power Point measured in TW.
    """
    return max_wind_power_point() / kw_into_tw()


@component.add(name="MAXWCF", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def maxwcf():
    """
    Maximal wind capacity factor.
    """
    return 0.5


@component.add(name="MAXWIE", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def maxwie():
    """
    Maximal value of Wind Installation Efficiency factor.
    """
    return 1


@component.add(name="MINWCF", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def minwcf():
    """
    Minimal and initial wind capacity factor.
    """
    return 0.2


@component.add(name="MINWIE", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def minwie():
    """
    Minimal and initial value of Wind Installation Efficiency factor.
    """
    return 0.01


@component.add(
    name="Ourflow IWITRLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_wind_installation_technology_ratio_lv2": 1,
        "delay_time_iwir": 1,
    },
)
def ourflow_iwitrlv2():
    return increase_in_wind_installation_technology_ratio_lv2() / delay_time_iwir()


@component.add(
    name="Outflow IWETRLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_wind_energy_technology_ratio_lv1": 1,
        "delay_time_iwetr": 1,
    },
)
def outflow_iwetrlv1():
    return increase_in_wind_energy_technology_ratio_lv1() / delay_time_iwetr()


@component.add(
    name="Outflow IWETRLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_wind_energy_technology_ratio_lv2": 1,
        "delay_time_iwetr": 1,
    },
)
def outflow_iwetrlv2():
    return increase_in_wind_energy_technology_ratio_lv2() / delay_time_iwetr()


@component.add(
    name="Outflow IWETRLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_wind_energy_technology_ratio_lv3": 1,
        "delay_time_iwetr": 1,
    },
)
def outflow_iwetrlv3():
    return increase_in_wind_energy_technology_ratio_lv3() / delay_time_iwetr()


@component.add(
    name="Outflow IWITRLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_wind_installation_technology_ratio_lv1": 1,
        "delay_time_iwir": 1,
    },
)
def outflow_iwitrlv1():
    return increase_in_wind_installation_technology_ratio_lv1() / delay_time_iwir()


@component.add(
    name="Outflow IWITRLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "increase_in_wind_installation_technology_ratio_lv3": 1,
        "delay_time_iwir": 1,
    },
)
def outflow_iwitrlv3():
    return increase_in_wind_installation_technology_ratio_lv3() / delay_time_iwir()


@component.add(
    name="Potential Wind Energy Production",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wind_installed_capacity": 1,
        "average_capacity_per_sqmeter": 1,
        "wind_capacity_factor": 1,
        "hours_per_year": 1,
        "kwh_into_mtoe": 1,
    },
)
def potential_wind_energy_production():
    """
    Potential solar energy production per year due to available production capability and technical developments.
    """
    return (
        wind_installed_capacity()
        * average_capacity_per_sqmeter()
        * wind_capacity_factor()
        * hours_per_year()
        * kwh_into_mtoe()
    )


@component.add(
    name="Productivity of Investment in Wind Capacity Installation",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "impact_of_space_on_wind_capacity_installation": 1,
        "wind_installation_efficiency": 1,
    },
)
def productivity_of_investment_in_wind_capacity_installation():
    """
    Productivity of wind capacity installation taking into account the level of remaining possible capacities and technology development state.
    """
    return (
        impact_of_space_on_wind_capacity_installation() * wind_installation_efficiency()
    )


@component.add(
    name="Reference Cost of Wind Energy Production",
    units="$/((m*m)*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"variable15_wind_cost": 1},
)
def reference_cost_of_wind_energy_production():
    """
    Reference cost of unit wind energy production per year.
    """
    return variable15_wind_cost()


@component.add(
    name="Sensitivity of Wind Energy Price to Supply and Demand",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sensitivity_of_wind_energy_price_to_supply_and_demand():
    """
    Sensitivity of Wind Energy Price to Supply and Demand ratio.
    """
    return 0


@component.add(
    name="Table for FIWEI",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_table_for_fiwei"},
)
def table_for_fiwei(x, final_subs=None):
    """
    Table determining order by which technology investments are dedicated to energy and installation efficiency. For small Wind Installation Efficiency, in order to secure sufficient production capacity, more investments are directed to infrastructure. Once the Wind Installation Efficiency increases the investments are redirected to solar conversion efficiency technologies.
    """
    return _hardcodedlookup_table_for_fiwei(x, final_subs)


_hardcodedlookup_table_for_fiwei = HardcodedLookups(
    [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
    [0.8, 0.8, 0.7, 0.5, 0.2, 0.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_for_fiwei",
)


@component.add(
    name="Time to Adjust Wind Infrastructure",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_adjust_wind_infrastructure():
    """
    Time to adjust Wind Infrastructure to the desired level.
    """
    return 5


@component.add(
    name="Total Wind Demand",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_demand": 1, "market_share_wind": 1},
)
def total_wind_demand():
    """
    Total demand for wind energy.
    """
    return energy_demand() * market_share_wind()


@component.add(
    name="Total Wind Demand GW",
    units="GW/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_wind_demand": 1, "kwh_into_mtoe_peak_hour": 1, "kw_into_gw": 1},
)
def total_wind_demand_gw():
    """
    Total demand for wind energy measured in GW.
    """
    return total_wind_demand() / kwh_into_mtoe_peak_hour() / kw_into_gw()


@component.add(
    name="Unit Cost of Wind Capacity Installation",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "init_unit_cost_of_wind_capacity_installation": 1,
        "impact_of_learning_on_wind_unit_cost_of_technology": 1,
    },
)
def unit_cost_of_wind_capacity_installation():
    """
    Unit Cost of Wind Capacity Installation. Determined by Productivity of Investment in Wind Capacity Installation.
    """
    return (
        init_unit_cost_of_wind_capacity_installation()
        * impact_of_learning_on_wind_unit_cost_of_technology()
    )


@component.add(
    name="Unit Cost of Wind Energy Production",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_cost_of_wind_energy_production": 1,
        "wind_production_to_installation_ratio": 1,
    },
)
def unit_cost_of_wind_energy_production():
    """
    Unit cost of wind capacity installation per energy unit.
    """
    return (
        reference_cost_of_wind_energy_production()
        / wind_production_to_installation_ratio()
    )


@component.add(
    name="Wind Aging Time", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def wind_aging_time():
    """
    Average wind energy production capacity aging time.
    """
    return 20


@component.add(
    name="Wind Available Area",
    units="m*m",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_available_area_variation": 1, "time": 1},
)
def wind_available_area():
    """
    Total area available for wind energy production capacities.
    """
    return 8000000000000.0 + step(
        __data["time"], wind_available_area_variation() - 8000000000000.0, 2020
    )


@component.add(
    name="Wind Available Area Variation",
    units="m*m",
    comp_type="Constant",
    comp_subtype="Normal",
)
def wind_available_area_variation():
    """
    Total area available for wind energy production capacities.
    """
    return 8000000000000.0


@component.add(
    name="Wind Capacity Aging Rate",
    units="m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_installed_capacity": 1, "wind_aging_time": 1},
)
def wind_capacity_aging_rate():
    """
    Aging rate of wind energy production capacities.
    """
    return wind_installed_capacity() / wind_aging_time()


@component.add(
    name="Wind Capacity Factor",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"minwcf": 2, "wind_energy_technology_ratio": 2, "maxwcf": 1},
)
def wind_capacity_factor():
    """
    Parameter indicating what fraction of average wind capacity per sqr meter it is possible to realize with the current state of technical developments.
    """
    return minwcf() + (maxwcf() - minwcf()) * (
        wind_energy_technology_ratio() / (wind_energy_technology_ratio() + 1)
    )


@component.add(
    name="Wind Energy Demand to Supply Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_wind_demand": 1, "potential_wind_energy_production": 1},
)
def wind_energy_demand_to_supply_ratio():
    """
    Wind Energy Demand to Supply Ratio.
    """
    return total_wind_demand() / potential_wind_energy_production()


@component.add(
    name="Wind Energy Price",
    units="$/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "indicated_wind_energy_price": 1,
        "effect_of_wind_energy_demand_and_supply_on_price": 1,
    },
)
def wind_energy_price():
    """
    Actual wind energy price accounting for indicated wind energy price and effect of demand and supply.
    """
    return (
        indicated_wind_energy_price()
        * effect_of_wind_energy_demand_and_supply_on_price()
    )


@component.add(
    name="Wind Energy Price per kWh",
    units="$/(kW*Hour)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_energy_price": 1, "kwh_into_mtoe": 1},
)
def wind_energy_price_per_kwh():
    """
    Actual wind energy price accounting for indicated wind energy price and effect of demand and supply measured in dollars per kWh.
    """
    return wind_energy_price() * kwh_into_mtoe()


@component.add(
    name="Wind Energy Production",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_energy_production_rate": 1},
)
def wind_energy_production():
    """
    Total wind energy production per year.
    """
    return wind_energy_production_rate()


@component.add(
    name="Wind Energy Production Indicator",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_energy_production": 1, "mtoe_into_ej": 1},
)
def wind_energy_production_indicator():
    return wind_energy_production() * mtoe_into_ej()


@component.add(
    name="Wind Energy Production Rate",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_wind_energy_production": 1, "total_wind_demand": 1},
)
def wind_energy_production_rate():
    """
    Total wind energy production per year accounting for demand and potential production due to available production capability and technical developments.
    """
    return float(np.minimum(potential_wind_energy_production(), total_wind_demand()))


@component.add(
    name="Wind Energy Revenue",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_energy_production": 1, "wind_energy_price": 1},
)
def wind_energy_revenue():
    """
    Total revenue in wind energy market.
    """
    return wind_energy_production() * wind_energy_price()


@component.add(
    name="Wind Energy Technology Development Time",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"renewable_energy_technology_development_time_variation": 1, "time": 1},
)
def wind_energy_technology_development_time():
    """
    Average time required to turn investments into concrete wind conversion efficiency technology developments. Since the simulation starts in 1900 it is a significant time.
    """
    return 50 + step(
        __data["time"],
        renewable_energy_technology_development_time_variation() - 50,
        2020,
    )


@component.add(
    name="Wind Energy Technology Ratio",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_wind_energy_technology_ratio": 1},
    other_deps={
        "_integ_wind_energy_technology_ratio": {
            "initial": {"init_wetrn": 1},
            "step": {"increase_in_wind_energy_technology_ratio": 1},
        }
    },
)
def wind_energy_technology_ratio():
    """
    Wind Energy Technology Ratio increased due to investments in wind conversion efficiency.
    """
    return _integ_wind_energy_technology_ratio()


_integ_wind_energy_technology_ratio = Integ(
    lambda: increase_in_wind_energy_technology_ratio(),
    lambda: init_wetrn(),
    "_integ_wind_energy_technology_ratio",
)


@component.add(
    name="Wind Final Investment",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"renewable_final_investment_fraction_variation": 1, "time": 1},
)
def wind_final_investment():
    """
    Eventual average level of investments in wind energy technology.
    """
    return 0.03 + step(
        __data["time"], renewable_final_investment_fraction_variation() - 0.03, 2020
    )


@component.add(
    name="Wind Infrastructure Adjustment",
    units="m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wind_capacity_aging_rate": 1,
        "desired_wind_installed_capacity": 1,
        "time_to_adjust_wind_infrastructure": 1,
        "wind_installed_capacity": 1,
    },
)
def wind_infrastructure_adjustment():
    """
    Adjustment of Wind Infrastructure to the desired level over a specified adjustment time and accounting for constant infrastructure decrease due to aging process.
    """
    return (
        wind_capacity_aging_rate()
        + (desired_wind_installed_capacity() - wind_installed_capacity())
        / time_to_adjust_wind_infrastructure()
    )


@component.add(
    name="Wind Initial Investment",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def wind_initial_investment():
    """
    Initial level of fractional investments in wind energy technology.
    """
    return 0


@component.add(
    name="Wind Installation Efficiency",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"minwie": 2, "wind_installation_technology_ratio": 2, "maxwie": 1},
)
def wind_installation_efficiency():
    """
    Parameter indicating wind energy capacity installation efficiency at the current state of technical developments.
    """
    return minwie() + (maxwie() - minwie()) * (
        wind_installation_technology_ratio()
        / (wind_installation_technology_ratio() + 1)
    )


@component.add(
    name="Wind Installation Technology Development Time",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "renewable_installation_technology_development_time_variation": 1,
        "time": 1,
    },
)
def wind_installation_technology_development_time():
    """
    Average time required to turn investments into concrete wind energy production capacity. Since the simulation starts in 1900 it is a significant time.
    """
    return 100 + step(
        __data["time"],
        renewable_installation_technology_development_time_variation() - 100,
        2020,
    )


@component.add(
    name="Wind Installation Technology Ratio",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_wind_installation_technology_ratio": 1},
    other_deps={
        "_integ_wind_installation_technology_ratio": {
            "initial": {"init_witrn": 1},
            "step": {"increase_in_wind_installation_technology_ratio": 1},
        }
    },
)
def wind_installation_technology_ratio():
    """
    Wind Installation Technology Ratio increased due to investments in wind energy capacity installation efficiency.
    """
    return _integ_wind_installation_technology_ratio()


_integ_wind_installation_technology_ratio = Integ(
    lambda: increase_in_wind_installation_technology_ratio(),
    lambda: init_witrn(),
    "_integ_wind_installation_technology_ratio",
)


@component.add(
    name="Wind Installed Capacity",
    units="m*m",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_wind_installed_capacity": 1},
    other_deps={
        "_integ_wind_installed_capacity": {
            "initial": {"init_wic": 1},
            "step": {
                "installation_of_wind_capacity_rate": 1,
                "wind_capacity_aging_rate": 1,
            },
        }
    },
)
def wind_installed_capacity():
    """
    Installed capacity to transform wind into energy.
    """
    return _integ_wind_installed_capacity()


_integ_wind_installed_capacity = Integ(
    lambda: installation_of_wind_capacity_rate() - wind_capacity_aging_rate(),
    lambda: init_wic(),
    "_integ_wind_installed_capacity",
)


@component.add(
    name="Wind Investment Fraction Finish",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_time": 1, "ramp_investment_period": 1},
)
def wind_investment_fraction_finish():
    """
    End of fractional investments in wind energy technology.
    """
    return initial_time() + ramp_investment_period()


@component.add(
    name="Wind Investment Fraction Slope",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wind_final_investment": 1,
        "wind_initial_investment": 1,
        "ramp_investment_period": 1,
    },
)
def wind_investment_fraction_slope():
    """
    Intensity of increase in investments in wind energy technology.
    """
    return (
        float(np.abs(wind_final_investment() - wind_initial_investment()))
        / ramp_investment_period()
    )


@component.add(
    name="Wind Investment Fraction Start",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_time": 1},
)
def wind_investment_fraction_start():
    """
    Start of investments in wind energy technology.
    """
    return initial_time()


@component.add(
    name="Wind Learning Curve Strength",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fraction_for_wind_learning_curve_strength": 1},
)
def wind_learning_curve_strength():
    """
    Strength of learning curve with which the wind energy costs are influenced.
    """
    return float(np.log(1 - fraction_for_wind_learning_curve_strength())) / float(
        np.log(2)
    )


@component.add(
    name="Wind Production to Installation Ratio",
    units="Mtoe/(m*m*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"wind_energy_production": 1, "wind_installed_capacity": 1},
)
def wind_production_to_installation_ratio():
    """
    Ratio of wind energy production to available production capacity.
    """
    return wind_energy_production() / wind_installed_capacity()
