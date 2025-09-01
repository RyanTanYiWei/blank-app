"""
Module water
Translated using PySD version 3.14.3
"""

@component.add(
    name="Additional Change in Reliable Water Supply",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def additional_change_in_reliable_water_supply():
    """
    A parameter that enables testing additional changes in reliable water supply independently from changes due to climate risk.
    """
    return 1


@component.add(
    name="Agricultural Water Demand",
    units="m*m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_agricultural_water_use_per_m2_irrigated": 1,
        "irrigated_agriculture_land": 1,
        "sqr_m_to_ha": 2,
        "rainfed_agriculture_land": 1,
        "average_agricultural_water_use_per_m2_rainfed": 1,
    },
)
def agricultural_water_demand():
    """
    Total water demand for agricultural purposes. Source of Historical Data: International Hydrological Programme (IHP) of UNESCO, data by Shiklomanov, I.A Dynamics of water use in the world (total) over the kinds of economic activities http://webworld.unesco.org/water/ihp/db/shiklomanov/
    """
    return (
        average_agricultural_water_use_per_m2_irrigated()
        * irrigated_agriculture_land()
        / sqr_m_to_ha()
        + average_agricultural_water_use_per_m2_rainfed()
        * rainfed_agriculture_land()
        / sqr_m_to_ha()
    )


@component.add(
    name="Agricultural Water Withdrawal Fulfillment Factor",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def agricultural_water_withdrawal_fulfillment_factor():
    """
    A factor determining the strength of infrastructure operating limits on agricultural water withdrawal fulfillment.
    """
    return 3.5


@component.add(
    name="Agricultural Water Withdrawal Fulfillment Rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agricultural_water_withdrawal_fulfillment_factor": 1,
        "max_water_withdrawal_rate": 1,
        "agricultural_water_demand": 1,
    },
)
def agricultural_water_withdrawal_fulfillment_rate():
    """
    Nonlinear relation that describes agricultural water withdrawal fulfillment as a relation of max water withdrawal and demand. With growing agricultural water demand the withdrawal fulfillment might be impaired which relates to infrastructure design and its operating limits.
    """
    return (
        2
        / (
            1
            + float(
                np.exp(
                    -agricultural_water_withdrawal_fulfillment_factor()
                    * (max_water_withdrawal_rate() / agricultural_water_demand())
                )
            )
        )
        - 1
    )


@component.add(
    name="Agricultural Water Withdrawal Rate",
    units="m*m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agricultural_water_demand": 1,
        "agricultural_water_withdrawal_fulfillment_rate": 1,
        "extreme_drought": 1,
    },
)
def agricultural_water_withdrawal_rate():
    """
    Water withdrawal rate for agricultural purposes.
    """
    return (
        agricultural_water_demand()
        * agricultural_water_withdrawal_fulfillment_rate()
        * (1 - extreme_drought())
    )


@component.add(
    name="Agricultural Water Withdrawal Rate no Drought",
    units="m*m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agricultural_water_demand": 1,
        "agricultural_water_withdrawal_fulfillment_rate": 1,
    },
)
def agricultural_water_withdrawal_rate_no_drought():
    """
    Drought scenario variable. Accounts for Agricultural Water Withdrawal Rate in no drought case.
    """
    return (
        agricultural_water_demand() * agricultural_water_withdrawal_fulfillment_rate()
    )


@component.add(
    name="Available Water Resources",
    units="m*m*m",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_available_water_resources": 1},
    other_deps={
        "_integ_available_water_resources": {
            "initial": {"desired_available_water_resources": 1},
            "step": {
                "recovery_of_used_water_resources_rate": 1,
                "water_supply_rate": 1,
                "agricultural_water_withdrawal_rate": 1,
                "domestic_water_withdrawal_rate": 1,
                "industrial_water_withdrawal_rate": 1,
                "drought_out": 1,
            },
        }
    },
)
def available_water_resources():
    """
    Available water resources to be used for domestic, agricultural and industrial use.
    """
    return _integ_available_water_resources()


_integ_available_water_resources = Integ(
    lambda: recovery_of_used_water_resources_rate()
    + water_supply_rate()
    - agricultural_water_withdrawal_rate()
    - domestic_water_withdrawal_rate()
    - industrial_water_withdrawal_rate()
    - drought_out(),
    lambda: desired_available_water_resources(),
    "_integ_available_water_resources",
)


@component.add(
    name="Available Water Resources Adjustment",
    units="m*m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "desired_available_water_resources": 1,
        "available_water_resources": 1,
        "available_water_resources_adjustment_time": 1,
    },
)
def available_water_resources_adjustment():
    """
    Adjustment of available water resources to desired available water resources.
    """
    return (
        desired_available_water_resources() - available_water_resources()
    ) / available_water_resources_adjustment_time()


@component.add(
    name="Available Water Resources Adjustment Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def available_water_resources_adjustment_time():
    """
    Time required to adjust available water resources to desired water resources.
    """
    return 1


@component.add(
    name="Average Agricultural Water Use per m2 Irrigated",
    units="m*m*m/(Year*m*m)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "min_agricultural_water_use_irrigated": 2,
        "max_agricultural_water_use_irrigated": 1,
        "smoothed_gwp_per_capita": 2,
        "reference_gwp_per_capita_for_agricultural_water_use_irrigated": 1,
    },
)
def average_agricultural_water_use_per_m2_irrigated():
    """
    Nonlinear relation that describes average agricultural water use on irrigated part of agricultural land as dependent on the population wealth represented by GWP per capita. Scaled between minimal and maximal level.
    """
    return min_agricultural_water_use_irrigated() + (
        max_agricultural_water_use_irrigated() - min_agricultural_water_use_irrigated()
    ) * (
        smoothed_gwp_per_capita()
        / (
            smoothed_gwp_per_capita()
            + reference_gwp_per_capita_for_agricultural_water_use_irrigated()
        )
    )


@component.add(
    name="Average Agricultural Water Use per m2 Rainfed",
    units="m*m*m/(Year*m*m)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "min_agricultural_water_use_rainfed": 2,
        "smoothed_gwp_per_capita": 2,
        "reference_gwp_per_capita_for_agricultural_water_use_rainfed": 1,
        "max_agricultural_water_use_rainfed": 1,
    },
)
def average_agricultural_water_use_per_m2_rainfed():
    """
    Nonlinear relation that describes average agricultural water use on rainfed part of agricultural land as dependent on the population wealth represented by GWP per capita. Scaled between minimal and maximal level.
    """
    return min_agricultural_water_use_rainfed() + (
        max_agricultural_water_use_rainfed() - min_agricultural_water_use_rainfed()
    ) * (
        smoothed_gwp_per_capita()
        / (
            smoothed_gwp_per_capita()
            + reference_gwp_per_capita_for_agricultural_water_use_rainfed()
        )
    )


@component.add(
    name="Average Domestic Water Use per Capita",
    units="m*m*m/(Year*People)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "min_domestic_water_use_per_capita": 2,
        "max_domestic_water_use_per_capita": 1,
        "smoothed_gwp_per_capita": 2,
        "reference_gwp_per_capita_for_domestic_water_use": 1,
    },
)
def average_domestic_water_use_per_capita():
    """
    Nonlinear relation that describes average domestic water use per capita as dependent on the population wealth represented by GWP per capita. Scaled between minimal and maximal level.
    """
    return min_domestic_water_use_per_capita() + (
        max_domestic_water_use_per_capita() - min_domestic_water_use_per_capita()
    ) * (
        smoothed_gwp_per_capita()
        / (
            smoothed_gwp_per_capita()
            + reference_gwp_per_capita_for_domestic_water_use()
        )
    )


@component.add(
    name="Average Industrial Water Use",
    units="m*m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "min_industrial_water_use": 2,
        "max_industrial_water_use": 1,
        "smoothed_gwp_per_capita": 2,
        "reference_gwp_per_capita_for_industrial_water_use": 1,
    },
)
def average_industrial_water_use():
    """
    Nonlinear relation that describes average industrial water use as dependent on the population wealth represented by GWP per capita. Scaled between minimal and maximal level.
    """
    return min_industrial_water_use() + (
        max_industrial_water_use() - min_industrial_water_use()
    ) * (
        smoothed_gwp_per_capita()
        / (
            smoothed_gwp_per_capita()
            + reference_gwp_per_capita_for_industrial_water_use()
        )
    )


@component.add(
    name="Average Used Water Recovery Fraction",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"variable12_water_recovery": 1},
)
def average_used_water_recovery_fraction():
    """
    Factor determining the percentage of consumed water resources that can be recovered.
    """
    return variable12_water_recovery()


@component.add(
    name="Desired Available Water Resources",
    units="m*m*m",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_water_demand": 1,
        "min_water_withdrawal_time": 1,
        "water_safety_stock_coverage": 1,
    },
)
def desired_available_water_resources():
    """
    Total desired available water resources including demand from industrial, agricultural and domestic sectors as well as safety coverage.
    """
    return total_water_demand() * (
        min_water_withdrawal_time() + water_safety_stock_coverage()
    )


@component.add(
    name="Desired Water Supply Rate",
    units="m*m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "water_consumption_adjustment": 1,
        "available_water_resources_adjustment": 1,
    },
)
def desired_water_supply_rate():
    """
    Desired water supply including constant water consumption and available water resources adjustment.
    """
    return float(
        np.maximum(
            0, water_consumption_adjustment() + available_water_resources_adjustment()
        )
    )


@component.add(
    name="Domestic Water Demand",
    units="m*m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "smoothed_total_population": 1,
        "average_domestic_water_use_per_capita": 1,
    },
)
def domestic_water_demand():
    """
    Total water demand for domestic purposes. Source of Historical Data: International Hydrological Programme (IHP) of UNESCO, data by Shiklomanov, I.A – Dynamics of water use in the world (total) over the kinds of economic activities http://webworld.unesco.org/water/ihp/db/shiklomanov/
    """
    return smoothed_total_population() * average_domestic_water_use_per_capita()


@component.add(
    name="Domestic Water Withdrawal Fulfillment Factor",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def domestic_water_withdrawal_fulfillment_factor():
    """
    A factor determining the strength of infrastructure operating limits on domestic water withdrawal fulfillment.
    """
    return 0.8


@component.add(
    name="Domestic Water Withdrawal Fulfillment Rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_water_withdrawal_fulfillment_factor": 1,
        "domestic_water_demand": 1,
        "max_water_withdrawal_rate": 1,
    },
)
def domestic_water_withdrawal_fulfillment_rate():
    """
    Nonlinear relation that describes domestic water withdrawal fulfillment as a relation of max water withdrawal and demand. With growing domestic water demand the withdrawal fulfillment might be impaired which relates to infrastructure design and its operating limits.
    """
    return (
        2
        / (
            1
            + float(
                np.exp(
                    -domestic_water_withdrawal_fulfillment_factor()
                    * (max_water_withdrawal_rate() / domestic_water_demand())
                )
            )
        )
        - 1
    )


@component.add(
    name="Domestic Water Withdrawal Rate",
    units="m*m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_water_demand": 1,
        "domestic_water_withdrawal_fulfillment_rate": 1,
    },
)
def domestic_water_withdrawal_rate():
    """
    Water withdrawal rate for domestic purposes.
    """
    return domestic_water_demand() * domestic_water_withdrawal_fulfillment_rate()


@component.add(
    name="Drought Out",
    units="m*m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agricultural_water_withdrawal_rate_no_drought": 1,
        "agricultural_water_withdrawal_rate": 1,
    },
)
def drought_out():
    """
    Water resources decrease rate due to drought.
    """
    return (
        agricultural_water_withdrawal_rate_no_drought()
        - agricultural_water_withdrawal_rate()
    )


@component.add(
    name="Extreme Drought", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def extreme_drought():
    """
    Drought scenario trigger.
    """
    return 0


@component.add(
    name="Impact of Climate Damage on Reliable Water Supply",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"climate_damage_fraction_old": 1},
)
def impact_of_climate_damage_on_reliable_water_supply():
    """
    A parameter that determines the impact of climate risk on water resources or infrastructure availability to provide reliable water supply.
    """
    return climate_damage_fraction_old()


@component.add(
    name="Industrial Water Demand",
    units="m*m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"average_industrial_water_use": 1},
)
def industrial_water_demand():
    """
    Total water demand for industrial purposes. Source of Historical Data: International Hydrological Programme (IHP) of UNESCO, data by Shiklomanov, I.A – Dynamics of water use in the world (total) over the kinds of economic activities http://webworld.unesco.org/water/ihp/db/shiklomanov/
    """
    return average_industrial_water_use()


@component.add(
    name="Industrial Water Withdrawal Fulfillment Factor",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def industrial_water_withdrawal_fulfillment_factor():
    """
    A factor determining the strength of infrastructure operating limits on industrial water withdrawal fulfillment.
    """
    return 2


@component.add(
    name="Industrial Water Withdrawal Fulfillment Rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "industrial_water_withdrawal_fulfillment_factor": 1,
        "max_water_withdrawal_rate": 1,
        "industrial_water_demand": 1,
    },
)
def industrial_water_withdrawal_fulfillment_rate():
    """
    Nonlinear relation that describes industrial water withdrawal fulfillment as a relation of max water withdrawal and demand. With growing industrial water demand the withdrawal fulfillment might be impaired which relates to infrastructure design and its operating limits.
    """
    return (
        2
        / (
            1
            + float(
                np.exp(
                    -industrial_water_withdrawal_fulfillment_factor()
                    * (max_water_withdrawal_rate() / industrial_water_demand())
                )
            )
        )
        - 1
    )


@component.add(
    name="Industrial Water Withdrawal Rate",
    units="m*m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "industrial_water_demand": 1,
        "industrial_water_withdrawal_fulfillment_rate": 1,
    },
)
def industrial_water_withdrawal_rate():
    """
    Water withdrawal rate for industrial purposes.
    """
    return industrial_water_demand() * industrial_water_withdrawal_fulfillment_rate()


@component.add(
    name="INIT Reliable Water Supply",
    units="m*m*m/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_reliable_water_supply():
    """
    Amount of water that can be reliably provided on annual basis for domestic, agricultural and industrial use due to resources and infrastructure availability for year 1900.
    """
    return 4200000000000.0


@component.add(
    name="Irrigated Agriculture Land",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"agricultural_land": 1, "percent_of_irrigated_land": 1},
)
def irrigated_agriculture_land():
    """
    Area of agricultural land on which the supply of water is only due to irrigation. Source of Historical Data: Gleick,P.H., et al. The World's Water Volume 7: The Biennial Report on Freshwater Resources. Washington: Island Press, 2012.
    """
    return agricultural_land() * percent_of_irrigated_land() / 100


@component.add(
    name="MAX Agricultural Water Use Irrigated",
    units="m*m*m/(Year*m*m)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_agricultural_water_use_irrigated():
    """
    Max level of average agricultural water use on part of agricultural land that is irrigated.
    """
    return 0.05


@component.add(
    name="MAX Agricultural Water Use Rainfed",
    units="m*m*m/(Year*m*m)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_agricultural_water_use_rainfed():
    """
    Max level of average agricultural water use on part of agricultural land that is rainfed.
    """
    return 0.1


@component.add(
    name="MAX Domestic Water Use per Capita",
    units="m*m*m/(Year*People)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"variable11_domestic_water": 1},
)
def max_domestic_water_use_per_capita():
    """
    Max level of average domestic water use per capita.
    """
    return variable11_domestic_water()


@component.add(
    name="MAX Industrial Water Use",
    units="m*m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"variable10_industrial_water": 1},
)
def max_industrial_water_use():
    """
    Max level of average industrial water use.
    """
    return variable10_industrial_water()


@component.add(
    name="MAX Percent of Irrigated Land",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_percent_of_irrigated_land():
    """
    Max percentage of total agricultural land that can be eventually irrigated.
    """
    return 100


@component.add(
    name="Max Water Withdrawal Rate",
    units="m*m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"available_water_resources": 1, "min_water_withdrawal_time": 1},
)
def max_water_withdrawal_rate():
    """
    Max possible water withdrawal rate due to available water resources.
    """
    return available_water_resources() / min_water_withdrawal_time()


@component.add(
    name="MIN Agricultural Water Use Irrigated",
    units="m*m*m/(Year*m*m)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def min_agricultural_water_use_irrigated():
    """
    Min level of average agricultural water use on part of agricultural land that is irrigated.
    """
    return 0.005


@component.add(
    name="MIN Agricultural Water Use Rainfed",
    units="m*m*m/(Year*m*m)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def min_agricultural_water_use_rainfed():
    """
    Min level of average agricultural water use on part of agricultural land that is rainfed.
    """
    return 0.005


@component.add(
    name="MIN Domestic Water Use per Capita",
    units="m*m*m/(Year*People)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def min_domestic_water_use_per_capita():
    """
    Min level of average domestic water use per capita.
    """
    return 5


@component.add(
    name="MIN Industrial Water Use",
    units="m*m*m/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def min_industrial_water_use():
    """
    Min level of average industrial water use.
    """
    return 2000


@component.add(
    name="MIN Percent of Irrigated Land",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def min_percent_of_irrigated_land():
    """
    Min percentage of total agricultural land that can be irrigated.
    """
    return 0


@component.add(
    name="Min Reliable Water Supply Decrease Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def min_reliable_water_supply_decrease_time():
    """
    Minimal period of time used to consider changes in water resources or infrastructure availability.
    """
    return 1


@component.add(
    name="Min Water Withdrawal Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def min_water_withdrawal_time():
    """
    Minimal time unit constraining water withdrawal.
    """
    return 1


@component.add(
    name="Net Change in Reliable Water Supply",
    units="m*m*m/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "init_reliable_water_supply": 1,
        "impact_of_climate_damage_on_reliable_water_supply": 1,
        "additional_change_in_reliable_water_supply": 1,
        "reliable_water_supply": 1,
        "min_reliable_water_supply_decrease_time": 1,
    },
)
def net_change_in_reliable_water_supply():
    """
    Change in reliable water supply due to changes in water resources or infrastructure availability.
    """
    return (
        init_reliable_water_supply()
        * impact_of_climate_damage_on_reliable_water_supply()
        * additional_change_in_reliable_water_supply()
        - reliable_water_supply()
    ) / min_reliable_water_supply_decrease_time()


@component.add(
    name="Non Recoverable Water Consumption Rate",
    units="m*m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"used_water_resources": 1, "average_used_water_recovery_fraction": 1},
)
def non_recoverable_water_consumption_rate():
    """
    Rate of water consumption not possible to be recovered.
    """
    return used_water_resources() * (1 - average_used_water_recovery_fraction())


@component.add(
    name="Percent of Irrigated Land",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "min_percent_of_irrigated_land": 2,
        "smoothed_gwp_per_capita": 2,
        "reference_gwp_per_capita_for_land_irrigation": 1,
        "max_percent_of_irrigated_land": 1,
    },
)
def percent_of_irrigated_land():
    """
    Nonlinear relation that determines the area of irrigated land as percentage of total agricultural land as dependent on the population wealth represented by GWP per capita. Scaled between minimal and maximal percentage.
    """
    return min_percent_of_irrigated_land() + (
        max_percent_of_irrigated_land() - min_percent_of_irrigated_land()
    ) * (
        smoothed_gwp_per_capita()
        / (smoothed_gwp_per_capita() + reference_gwp_per_capita_for_land_irrigation())
    )


@component.add(
    name="Quality of Domestic Water",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "domestic_water_withdrawal_fulfillment_rate": 2,
        "water_quality_steepness": 4,
        "water_quality_inflection": 2,
    },
)
def quality_of_domestic_water():
    """
    Nonlinear relation describing the quality of domestic as dependent on withdrawal fulfillment rate.
    """
    return (
        domestic_water_withdrawal_fulfillment_rate() ** water_quality_steepness()
        * (water_quality_inflection() ** water_quality_steepness() + 1)
        / (
            water_quality_inflection() ** water_quality_steepness()
            + domestic_water_withdrawal_fulfillment_rate() ** water_quality_steepness()
        )
    )


@component.add(
    name="Rainfed Agriculture Land",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"agricultural_land": 1, "percent_of_irrigated_land": 1},
)
def rainfed_agriculture_land():
    """
    Area of agricultural land on which the supply of water is only due to rain.
    """
    return agricultural_land() * (1 - percent_of_irrigated_land() / 100)


@component.add(
    name="Recovery of Used Water Resources Rate",
    units="m*m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"used_water_resources": 1, "average_used_water_recovery_fraction": 1},
)
def recovery_of_used_water_resources_rate():
    """
    Rate of water consumption possible to be recovered and thus return to available water resources stock.
    """
    return used_water_resources() * average_used_water_recovery_fraction()


@component.add(
    name="Reference GWP per Capita for Agricultural Water Use Irrigated",
    units="$/(Year*Person)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_gwp_per_capita_for_agricultural_water_use_irrigated():
    """
    A reference value against which the GDP per Capita is compared to calculate the impact of population wealth on average agricultural water use on the land where the supply of water is due to irrigation.
    """
    return 3500


@component.add(
    name="Reference GWP per Capita for Agricultural Water Use Rainfed",
    units="$/(Year*Person)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_gwp_per_capita_for_agricultural_water_use_rainfed():
    """
    A reference value against which the GDP per Capita is compared to calculate the impact of population wealth on average agricultural water use on the land where the supply of water is only due to rainfall.
    """
    return 7000


@component.add(
    name="Reference GWP per Capita for Domestic Water Use",
    units="$/(Year*Person)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_gwp_per_capita_for_domestic_water_use():
    """
    A reference value against which the GDP per Capita is compared to calculate the impact of population wealth on domestic water use.
    """
    return 9000


@component.add(
    name="Reference GWP per Capita for Industrial Water Use",
    units="$/(Year*Person)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_gwp_per_capita_for_industrial_water_use():
    """
    A reference value against which the GDP per Capita is compared to calculate the impact of population wealth on average inductrial water use.
    """
    return 17000


@component.add(
    name="Reference GWP per Capita for Land Irrigation",
    units="$/(Year*Person)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_gwp_per_capita_for_land_irrigation():
    """
    A reference value against which the GDP per Capita is compared to calculate the impact of population wealth on percentage of agricultural land irrigation.
    """
    return 120000


@component.add(
    name="Reliable Water Supply",
    units="m*m*m/Year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_reliable_water_supply": 1},
    other_deps={
        "_integ_reliable_water_supply": {
            "initial": {"init_reliable_water_supply": 1},
            "step": {"net_change_in_reliable_water_supply": 1},
        }
    },
)
def reliable_water_supply():
    """
    Amount of water that can be reliably provided on annual basis for domestic, agricultural and industrial use due to resources and infrastructure availability. Source of historical data: 2030 Water Resources Group, 2009. Charting Our Water Future - Economic frameworks to inform decision-making. http://www.mckinsey.com/App_Media/Reports/Water/Charting_Our_Water_Future_F ull_Report_001.pdf
    """
    return _integ_reliable_water_supply()


_integ_reliable_water_supply = Integ(
    lambda: net_change_in_reliable_water_supply(),
    lambda: init_reliable_water_supply(),
    "_integ_reliable_water_supply",
)


@component.add(
    name="Total Water Demand",
    units="m*m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agricultural_water_demand": 1,
        "domestic_water_demand": 1,
        "industrial_water_demand": 1,
    },
)
def total_water_demand():
    """
    Total world water demand related to various purposes. http://webworld.unesco.org/water/ihp/db/shiklomanov/index.shtml
    """
    return (
        agricultural_water_demand()
        + domestic_water_demand()
        + industrial_water_demand()
    )


@component.add(
    name="Used Water Resources",
    units="m*m*m",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_used_water_resources": 1},
    other_deps={
        "_integ_used_water_resources": {
            "initial": {"available_water_resources": 1},
            "step": {
                "agricultural_water_withdrawal_rate": 1,
                "domestic_water_withdrawal_rate": 1,
                "industrial_water_withdrawal_rate": 1,
                "non_recoverable_water_consumption_rate": 1,
                "recovery_of_used_water_resources_rate": 1,
            },
        }
    },
)
def used_water_resources():
    """
    Water resources that have been used for industrial, agricultural and domestic purposes.
    """
    return _integ_used_water_resources()


_integ_used_water_resources = Integ(
    lambda: agricultural_water_withdrawal_rate()
    + domestic_water_withdrawal_rate()
    + industrial_water_withdrawal_rate()
    - non_recoverable_water_consumption_rate()
    - recovery_of_used_water_resources_rate(),
    lambda: available_water_resources(),
    "_integ_used_water_resources",
)


@component.add(
    name="Water Consumption Adjustment",
    units="m*m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agricultural_water_withdrawal_rate": 1,
        "domestic_water_withdrawal_rate": 1,
        "industrial_water_withdrawal_rate": 1,
        "recovery_of_used_water_resources_rate": 1,
    },
)
def water_consumption_adjustment():
    """
    The sum of consumption of water in industrial, agricultural and domestic sectors corected by used water recovery rate.
    """
    return (
        agricultural_water_withdrawal_rate()
        + domestic_water_withdrawal_rate()
        + industrial_water_withdrawal_rate()
        - recovery_of_used_water_resources_rate()
    )


@component.add(
    name="Water Quality Inflection",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def water_quality_inflection():
    """
    Inflection point of nonlinear relation describing domestic water quality.
    """
    return 0.5


@component.add(
    name="Water Quality Steepness",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def water_quality_steepness():
    """
    Steepness of nonlinear relation describing domestic water quality.
    """
    return 5


@component.add(
    name="Water Safety Stock Coverage",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def water_safety_stock_coverage():
    """
    Water resources safety stock expressed in terms of time duration. Additional time period during which the water resources need to be available at the total water demand level.
    """
    return 0.1


@component.add(
    name="Water Supply Fulfillment Factor",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def water_supply_fulfillment_factor():
    """
    A factor determining the strength of infrastructure operating limits on water supply fulfillment.
    """
    return 3


@component.add(
    name="Water Supply Fulfillment Rate",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "water_supply_fulfillment_factor": 1,
        "reliable_water_supply": 1,
        "desired_water_supply_rate": 1,
    },
)
def water_supply_fulfillment_rate():
    """
    Nonlinear relation that describes water supply fulfillment as a relation of water supply and demand. With growing water demand the supply fulfillment might be impaired which relates to infrastructure design and its operating limits.
    """
    return (
        2
        / (
            1
            + float(
                np.exp(
                    -water_supply_fulfillment_factor()
                    * (reliable_water_supply() / desired_water_supply_rate())
                )
            )
        )
        - 1
    )


@component.add(
    name="Water Supply Rate",
    units="m*m*m/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_water_supply_rate": 1, "water_supply_fulfillment_rate": 1},
)
def water_supply_rate():
    """
    Water supply taking into account the desired water supply and the supply fulfillment rate. The water supply includes withdrawals from surface water, groundwater or nonconventional sources for example desalination.
    """
    return desired_water_supply_rate() * water_supply_fulfillment_rate()
