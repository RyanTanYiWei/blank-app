"""
Module land_use
Translated using PySD version 3.14.3
"""

@component.add(
    name="Actual Forest Land Harvested",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "forest_biomass_production": 1,
        "biomass_production_processing_loss": 1,
        "forest_land_energy_yield": 1,
    },
)
def actual_forest_land_harvested():
    """
    Forest biomass production expressed in terms of forest land harvested excluding forest biomass production processing loss.
    """
    return (
        forest_biomass_production() / (1 - biomass_production_processing_loss())
    ) / forest_land_energy_yield()


@component.add(name="AF S", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def af_s():
    return 0.95


@component.add(
    name="AF Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_af_var_s": 1},
    other_deps={
        "_smooth_af_var_s": {
            "initial": {"af_s": 1, "time": 1},
            "step": {"af_s": 1, "time": 1},
        }
    },
)
def af_var_s():
    return 0.95 + _smooth_af_var_s()


_smooth_af_var_s = Smooth(
    lambda: step(__data["time"], af_s() - 0.95, 2020),
    lambda: 1,
    lambda: step(__data["time"], af_s() - 0.95, 2020),
    lambda: 1,
    "_smooth_af_var_s",
)


@component.add(
    name="Agricultural Land",
    units="ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_agricultural_land": 1},
    other_deps={
        "_integ_agricultural_land": {
            "initial": {"init_agricultural_land": 1},
            "step": {
                "agricultural_land_erosion_rate": 1,
                "forestation_from_agricultural_land": 1,
                "agricultural_land_conversion_rate_to_urban_land": 1,
                "deforestation_to_agricultural_land": 1,
                "agricultural_land_development_rate": 1,
            },
        }
    },
)
def agricultural_land():
    """
    Total Agriculture Land.
    """
    return _integ_agricultural_land()


_integ_agricultural_land = Integ(
    lambda: -agricultural_land_erosion_rate()
    - forestation_from_agricultural_land()
    - agricultural_land_conversion_rate_to_urban_land()
    + deforestation_to_agricultural_land()
    + agricultural_land_development_rate(),
    lambda: init_agricultural_land(),
    "_integ_agricultural_land",
)


@component.add(
    name="Agricultural Land Conversion Rate to Urban Land",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "urban_and_industrial_land_discrepancy": 1,
        "fraction_of_urban_land_conversion_from_agriculture": 1,
        "agriculture_to_urban_land_allocation_time": 2,
        "agricultural_land": 1,
        "agriculture_protected_land": 1,
    },
)
def agricultural_land_conversion_rate_to_urban_land():
    """
    Transformation process of Agriculture Land into Urban and Industrial Land.
    """
    return float(
        np.minimum(
            urban_and_industrial_land_discrepancy()
            * fraction_of_urban_land_conversion_from_agriculture()
            / agriculture_to_urban_land_allocation_time(),
            (agricultural_land() - agriculture_protected_land())
            / agriculture_to_urban_land_allocation_time(),
        )
    )


@component.add(
    name="Agricultural Land Development Rate",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "intended_conversion_other_to_agriculture": 1,
        "other_land": 1,
        "other_protected_land": 1,
        "agricultural_land_development_time": 1,
    },
)
def agricultural_land_development_rate():
    return (
        float(
            np.minimum(
                intended_conversion_other_to_agriculture(),
                other_land() - other_protected_land(),
            )
        )
        / agricultural_land_development_time()
    )


@component.add(
    name="Agricultural Land Development Time",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"agricultural_land_development_time_variation": 1, "time": 1},
)
def agricultural_land_development_time():
    return 100 + step(
        __data["time"], agricultural_land_development_time_variation() - 100, 2020
    )


@component.add(
    name="Agricultural Land Development Time Variation",
    comp_type="Constant",
    comp_subtype="Normal",
)
def agricultural_land_development_time_variation():
    return 100


@component.add(
    name="Agricultural Land Erosion Fraction",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"agricultural_land_erosion_fraction_variation": 1, "time": 1},
)
def agricultural_land_erosion_fraction():
    """
    This is actually dependent on yield. The highher the yield, the shorter the lifetime of the agricultural land.
    """
    return 0.0001 + step(
        __data["time"], agricultural_land_erosion_fraction_variation() - 0.0001, 2020
    )


@component.add(
    name="Agricultural Land Erosion Fraction Variation",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def agricultural_land_erosion_fraction_variation():
    """
    This is actually dependent on yield. The highher the yield, the shorter the lifetime of the agricultural land.
    """
    return 0.0001


@component.add(
    name="Agricultural Land Erosion Rate",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"agricultural_land": 1, "agricultural_land_erosion_fraction": 1},
)
def agricultural_land_erosion_rate():
    """
    Process of transformation between Agriculture and Other Land.
    """
    return agricultural_land() * agricultural_land_erosion_fraction()


@component.add(
    name="Agriculture Land Energy Yield",
    units="Biomass ton/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nominal_energy_agriculture_land_productivity": 1,
        "effect_of_carbon_concentration_on_agricultural_yield": 1,
        "effect_of_climate_change_on_agricultural_yield": 1,
        "effect_of_input_neutral_technology_change_on_agricultural_land_fertility": 1,
        "effect_of_water_withdrawal_on_agriculture_land_fertility": 1,
        "effect_of_management_practices_on_agriculture_land_fertility": 1,
    },
)
def agriculture_land_energy_yield():
    """
    Yield from a unit energy crops land area.
    """
    return (
        nominal_energy_agriculture_land_productivity()
        * effect_of_carbon_concentration_on_agricultural_yield()
        * effect_of_climate_change_on_agricultural_yield()
        * effect_of_input_neutral_technology_change_on_agricultural_land_fertility()
        * effect_of_water_withdrawal_on_agriculture_land_fertility()
        * effect_of_management_practices_on_agriculture_land_fertility()
    )


@component.add(
    name="Agriculture Protected Land",
    units="ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def agriculture_protected_land():
    """
    Area of Agriculture Land not transformable into other kind of lands.
    """
    return 1466830000.0


@component.add(
    name="Agriculture to Forest Land Allocation Time",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"agriculture_to_forest_land_allocation_time_variation": 1, "time": 1},
)
def agriculture_to_forest_land_allocation_time():
    """
    Average time which natural transformation of Agriculture to Forest Land would take.
    """
    return 150 + step(
        __data["time"],
        agriculture_to_forest_land_allocation_time_variation() - 150,
        2020,
    )


@component.add(
    name="Agriculture to Forest Land Allocation Time Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def agriculture_to_forest_land_allocation_time_variation():
    """
    Average time which natural transformation of Agriculture to Forest Land would take.
    """
    return 150


@component.add(
    name="Agriculture to Urban Land Allocation Time",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"agriculture_to_urban_land_allocation_time_variation": 1, "time": 1},
)
def agriculture_to_urban_land_allocation_time():
    """
    Average time which natural transformation of Agriculture to Urban and Industrial Land would take.
    """
    return 5 + step(
        __data["time"], agriculture_to_urban_land_allocation_time_variation() - 5, 2020
    )


@component.add(
    name="Agriculture to Urban Land Allocation Time Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def agriculture_to_urban_land_allocation_time_variation():
    """
    Average time which natural transformation of Agriculture to Urban and Industrial Land would take.
    """
    return 5


@component.add(name="alpha", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def alpha():
    """
    Beginning point of the domain of the table function. In this model, equal to 0.
    """
    return 1.25


@component.add(
    name="Animal Food Supply kcal capita day",
    units="kcal/(Person*Day)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_supply_of_animal_calories": 1,
        "kcal_to_mkcal": 1,
        "days_in_year": 1,
        "population": 1,
    },
)
def animal_food_supply_kcal_capita_day():
    """
    Average amount of animal food measured in calories available for each person per day. Source of historical data: http://faostat.fao.org
    """
    return total_supply_of_animal_calories() / (
        population() * days_in_year() * kcal_to_mkcal()
    )


@component.add(
    name="Annual Caloric Demand inc Waste",
    units="Mkcal/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_caloric_demand": 1, "waste_fraction": 1},
)
def annual_caloric_demand_inc_waste():
    """
    Total Annual Calorie Demand for Food Category[FoodCategories]/(1-Waste fraction[FoodCategories])
    """
    return annual_caloric_demand() / (1 - waste_fraction())


@component.add(
    name="Arable Land",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"agricultural_land": 1, "arable_percentage_of_agriculture_land": 1},
)
def arable_land():
    """
    Area of arable land.
    """
    return agricultural_land() * arable_percentage_of_agriculture_land()


@component.add(
    name="Arable Land Allocated for Crops",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"arable_land": 1, "total_demand_for_arable_land": 1},
)
def arable_land_allocated_for_crops():
    return float(np.minimum(arable_land(), total_demand_for_arable_land()))


@component.add(
    name="Arable Land Allocated for Energy Crops",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"demand_fraction_of_energy_crops": 1, "arable_land": 1},
)
def arable_land_allocated_for_energy_crops():
    return demand_fraction_of_energy_crops() * arable_land()


@component.add(
    name="Arable land allocation fraction",
    units="Dmnl",
    subscripts=["PlantFood"],
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_arable_land_allocation_fraction": 1},
    other_deps={
        "_smooth_arable_land_allocation_fraction": {
            "initial": {"demand_fraction_of_food_and_feed_crops": 1},
            "step": {"demand_fraction_of_food_and_feed_crops": 1},
        }
    },
)
def arable_land_allocation_fraction():
    return _smooth_arable_land_allocation_fraction()


_smooth_arable_land_allocation_fraction = Smooth(
    lambda: demand_fraction_of_food_and_feed_crops(),
    lambda: xr.DataArray(5, {"PlantFood": _subscript_dict["PlantFood"]}, ["PlantFood"]),
    lambda: demand_fraction_of_food_and_feed_crops(),
    lambda: 1,
    "_smooth_arable_land_allocation_fraction",
)


@component.add(
    name="Arable Land Needed",
    units="ha",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_crop_production": 1, "expected_crop_yield": 1},
)
def arable_land_needed():
    return desired_crop_production() / expected_crop_yield()


@component.add(
    name="Arable Land Needed for Energy Crops",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_crops_biomass_demand": 1, "agriculture_land_energy_yield": 1},
)
def arable_land_needed_for_energy_crops():
    """
    Land area dedicated to energy crops production.
    """
    return total_crops_biomass_demand() / agriculture_land_energy_yield()


@component.add(
    name="Arable Percentage of Agriculture Land",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def arable_percentage_of_agriculture_land():
    """
    Percentage of agricultural land constituting the arable land.
    """
    return 0.287


@component.add(
    name="Area harvested",
    units="ha",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "arable_land_allocated_for_crops": 1,
        "arable_land_allocation_fraction": 1,
    },
)
def area_harvested():
    return arable_land_allocated_for_crops() * arable_land_allocation_fraction()


@component.add(
    name="Average expected crop yield",
    units="Ton/(Year*ha)",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"reference_crop_yield_2016": 1, "effect_of_fertilizer_on_yield": 1},
)
def average_expected_crop_yield():
    return reference_crop_yield_2016().loc[_subscript_dict["PlantFood"]].rename(
        {"FoodCategories": "PlantFood"}
    ) * effect_of_fertilizer_on_yield().loc[_subscript_dict["PlantFood"]].rename(
        {"FoodCategories": "PlantFood"}
    )


@component.add(name="beta", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def beta():
    """
    End point of the domain of the table function. In this model, qual to 1.
    """
    return 5


@component.add(
    name="Biomass Production Processing Loss",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biomass_production_processing_loss():
    """
    Average percentage of total forest biomass production lost due to processing.
    """
    return 0.1


@component.add(
    name="Biomass ton into Biomass million ton",
    units="Biomass million ton/Biomass ton",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biomass_ton_into_biomass_million_ton():
    return 1 / 1000000.0


@component.add(
    name="Caloric value of food",
    units="Mkcal/Ton",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "caloric_value_of_food_data": 1,
        "time": 1,
        "sa_multiplier_for_caloric_value": 1,
    },
)
def caloric_value_of_food():
    return caloric_value_of_food_data() * (
        1 + step(__data["time"], sa_multiplier_for_caloric_value() - 1, 2020)
    )


@component.add(
    name="Caloric value of food Data",
    units="Mkcal/Ton",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def caloric_value_of_food_data():
    return xr.DataArray(
        [1.2, 1.546, 0.6, 1.43, 3.442, 3.207, 0.483, 0.8],
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )


@component.add(name="Calpha", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def calpha():
    """
    Beginning point of the domain of the table function. In this model, equal to 0.
    """
    return 1.25


@component.add(name="Cbeta", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def cbeta():
    """
    End point of the domain of the table function. In this model, qual to 1.
    """
    return 5


@component.add(
    name="Climate Impact on Forest Land Fertility Nonlinearity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_impact_on_forest_land_fertility_nonlinearity():
    """
    Elasticity of climate impact on forest land fertility.
    """
    return 2


@component.add(
    name="Climate Impact on Forest Land Fertility Reference Temperature",
    units="DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_impact_on_forest_land_fertility_reference_temperature():
    """
    Reference temperature against which the average temerature is compared in calculation of impact of climate change on forest land fertility.
    """
    return 3


@component.add(
    name="Climate Impact on Forest Land Fertility Scale",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_impact_on_forest_land_fertility_scale():
    """
    Increment of climate impact on forest land fertility.
    """
    return 0.013


@component.add(
    name="CO2 emission rate of the agriculture sector",
    units="TonCO2/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "food_production_rate": 1,
        "unit_co2_emissions_from_food_production": 1,
    },
)
def co2_emission_rate_of_the_agriculture_sector():
    return food_production_rate() * unit_co2_emissions_from_food_production()


@component.add(
    name="CO2 to C", units="TonCO2/TonC", comp_type="Constant", comp_subtype="Normal"
)
def co2_to_c():
    return 3.664


@component.add(
    name="Crop demand for other uses",
    units="Ton/Year",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"food_demand_in_tonnes": 1, "other_uses_multiplier_for_food": 1},
)
def crop_demand_for_other_uses():
    return (
        food_demand_in_tonnes()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        * other_uses_multiplier_for_food()
    )


@component.add(
    name="Crop yield for each category",
    units="Ton/(ha*Year)",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_expected_crop_yield": 1,
        "effect_of_input_neutral_technology_change_on_agricultural_land_fertility": 1,
        "effect_of_climate_change_on_agricultural_yield": 1,
        "effect_of_carbon_concentration_on_agricultural_yield": 1,
        "effect_of_water_withdrawal_on_agriculture_land_fertility": 1,
    },
)
def crop_yield_for_each_category():
    return (
        average_expected_crop_yield()
        * effect_of_input_neutral_technology_change_on_agricultural_land_fertility()
        * effect_of_climate_change_on_agricultural_yield()
        * effect_of_carbon_concentration_on_agricultural_yield()
        * effect_of_water_withdrawal_on_agriculture_land_fertility()
    )


@component.add(
    name="Cropland Needed",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "arable_land_needed": 1,
        "permanent_crops": 1,
        "arable_land_needed_for_energy_crops": 1,
    },
)
def cropland_needed():
    """
    Land area required for food crops production due to food demand.
    """
    return (
        sum(
            arable_land_needed().rename({"PlantFood": "PlantFood!"}), dim=["PlantFood!"]
        )
        + permanent_crops()
        + arable_land_needed_for_energy_crops()
    )


@component.add(
    name="Cropland Yield",
    units="Ton/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"area_harvested": 2, "crop_yield_for_each_category": 1},
)
def cropland_yield():
    return sum(
        area_harvested().rename({"PlantFood": "PlantFood!"})
        * crop_yield_for_each_category().rename({"PlantFood": "PlantFood!"}),
        dim=["PlantFood!"],
    ) / sum(area_harvested().rename({"PlantFood": "PlantFood!"}), dim=["PlantFood!"])


@component.add(
    name="Cropland Yield Indicator",
    units="Ton/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cropland_yield": 1},
)
def cropland_yield_indicator():
    return cropland_yield()


@component.add(
    name="Current to Max Forest Protected Land",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "forest_protected_land_change_ratio": 1,
        "forest_protected_land": 1,
        "max_forest_protected_land": 1,
    },
)
def current_to_max_forest_protected_land():
    """
    Gap being closed between current and max forest protected land.
    """
    return forest_protected_land_change_ratio() * (
        1 - forest_protected_land() / max_forest_protected_land()
    )


@component.add(
    name="Daily caloric supply per capita",
    units="kcal/(Person*Day)",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "food_supply_in_kcal": 1,
        "kcal_to_mkcal": 1,
        "days_in_year": 1,
        "population": 1,
    },
)
def daily_caloric_supply_per_capita():
    return food_supply_in_kcal() / (population() * days_in_year() * kcal_to_mkcal())


@component.add(
    name="Days in Year", units="Days/Year", comp_type="Constant", comp_subtype="Normal"
)
def days_in_year():
    """
    The number of days per year.
    """
    return 365


@component.add(
    name="Deforestation",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "deforestation_to_urban_land": 1,
        "deforestation_to_agricultural_land": 1,
    },
)
def deforestation():
    return deforestation_to_urban_land() + deforestation_to_agricultural_land()


@component.add(
    name="Deforestation to Agricultural Land",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "forest_land": 1,
        "forest_protected_land": 1,
        "forest_to_agriculture_land_allocation_time": 2,
        "intended_conversion_forest_to_agriculture": 1,
    },
)
def deforestation_to_agricultural_land():
    return float(
        np.minimum(
            (forest_land() - forest_protected_land())
            / forest_to_agriculture_land_allocation_time(),
            intended_conversion_forest_to_agriculture()
            / forest_to_agriculture_land_allocation_time(),
        )
    )


@component.add(
    name="Deforestation to Urban Land",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "urban_and_industrial_land_discrepancy": 1,
        "fraction_of_urban_land_conversion_from_agriculture": 1,
        "forest_to_urban_land_allocation_time": 2,
        "forest_land": 1,
        "forest_protected_land": 1,
    },
)
def deforestation_to_urban_land():
    """
    Transformation process of Forest into Urban and Industrial Land.
    """
    return float(
        np.minimum(
            urban_and_industrial_land_discrepancy()
            * (1 - fraction_of_urban_land_conversion_from_agriculture())
            / forest_to_urban_land_allocation_time(),
            (forest_land() - forest_protected_land())
            / forest_to_urban_land_allocation_time(),
        )
    )


@component.add(
    name="Delay Time FPLCLV",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_to_adjust_forest_protected_land": 1},
)
def delay_time_fplclv():
    return time_to_adjust_forest_protected_land() / 3


@component.add(
    name="Demand Fraction of Energy Crops",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "arable_land_needed_for_energy_crops": 1,
        "total_demand_for_arable_land": 1,
    },
)
def demand_fraction_of_energy_crops():
    return arable_land_needed_for_energy_crops() / total_demand_for_arable_land()


@component.add(
    name="Demand Fraction of Food and Feed Crops",
    units="Dmnl",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"arable_land_needed": 1, "total_demand_for_arable_land": 1},
)
def demand_fraction_of_food_and_feed_crops():
    return arable_land_needed() / total_demand_for_arable_land()


@component.add(
    name="Demand fraction of Grassland",
    units="Dmnl",
    subscripts=["MapAltProteins"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grassland_needed": 2, "total_grassland_needed": 2},
)
def demand_fraction_of_grassland():
    value = xr.DataArray(
        np.nan,
        {"MapAltProteins": _subscript_dict["MapAltProteins"]},
        ["MapAltProteins"],
    )
    value.loc[["PasMeat"]] = (
        float(grassland_needed().loc["PasMeat"]) / total_grassland_needed()
    )
    value.loc[["Dairy"]] = (
        float(grassland_needed().loc["Dairy"]) / total_grassland_needed()
    )
    return value


@component.add(
    name="Demand Supply ratio of Agricultural Land",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_agricultural_land_demand": 1, "agricultural_land": 1},
)
def demand_supply_ratio_of_agricultural_land():
    return total_agricultural_land_demand() / agricultural_land()


@component.add(
    name="Desired Agricultural Land Conversion",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"trend_of_land_demand": 1, "agricultural_land": 1},
)
def desired_agricultural_land_conversion():
    return trend_of_land_demand() * agricultural_land()


@component.add(
    name="Desired Agricultural Land Conversion Trend Averaging Time Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def desired_agricultural_land_conversion_trend_averaging_time_variation():
    return 10


@component.add(
    name="Desired crop production",
    units="Ton/Year",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "food_demand_in_tonnes": 1,
        "feed_demand_in_tonnes": 1,
        "crop_demand_for_other_uses": 1,
    },
)
def desired_crop_production():
    return (
        food_demand_in_tonnes()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        + feed_demand_in_tonnes()
        + crop_demand_for_other_uses()
    )


@component.add(
    name="Desired Production Fraction",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_forest_biomass_demand": 1, "potential_biomass_production": 1},
)
def desired_production_fraction():
    """
    Ratio of demand for forest biomass to potential production.
    """
    return total_forest_biomass_demand() / potential_biomass_production()


@component.add(
    name="Distorted Effect of T on Yield",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "distortion_function_t": 1,
        "temperature_change_from_preindustrial": 1,
        "effect_of_t_on_yield_lookup": 1,
    },
)
def distorted_effect_of_t_on_yield():
    return distortion_function_t() * effect_of_t_on_yield_lookup(
        temperature_change_from_preindustrial()
    )


@component.add(
    name="Distortion Function C",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_concentration_ratio": 3,
        "p_effect_of_c_on_yield": 4,
        "calpha": 2,
        "m_effect_of_c_on_yield": 3,
        "u_effect_of_c_on_yield": 1,
        "cbeta": 1,
    },
)
def distortion_function_c():
    """
    Single Triangular Distortion Function with Static End Points l+m-(l+m-u)*(Iratio-p)/(1-p)
    """
    return if_then_else(
        c_concentration_ratio() <= p_effect_of_c_on_yield(),
        lambda: 1
        + m_effect_of_c_on_yield()
        * (c_concentration_ratio() - calpha())
        / (p_effect_of_c_on_yield() - calpha()),
        lambda: 1
        + m_effect_of_c_on_yield()
        - (1 + m_effect_of_c_on_yield() - u_effect_of_c_on_yield())
        * (c_concentration_ratio() - p_effect_of_c_on_yield())
        / (cbeta() - p_effect_of_c_on_yield()),
    )


@component.add(
    name="Distortion Function T",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "temperature_change_from_preindustrial": 3,
        "p_effect_of_t_on_yield": 4,
        "alpha": 2,
        "m_effect_of_t_on_yield": 3,
        "beta": 1,
        "u_effect_of_t_on_yield": 1,
    },
)
def distortion_function_t():
    """
    Single Triangular Distortion Function with Static End Points l+m-(l+m-u)*(Iratio-p)/(1-p)
    """
    return if_then_else(
        temperature_change_from_preindustrial() <= p_effect_of_t_on_yield(),
        lambda: 1
        + m_effect_of_t_on_yield()
        * (temperature_change_from_preindustrial() - alpha())
        / (p_effect_of_t_on_yield() - alpha()),
        lambda: 1
        + m_effect_of_t_on_yield()
        - (1 + m_effect_of_t_on_yield() - u_effect_of_t_on_yield())
        * (temperature_change_from_preindustrial() - p_effect_of_t_on_yield())
        / (beta() - p_effect_of_t_on_yield()),
    )


@component.add(
    name="Effect of Biodiversity on Forest Land Fertility",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "min_impact_of_biodiversity_on_forest_land_fertility": 2,
        "init_species_abundance": 1,
        "mean_species_abundance": 1,
        "max_impact_of_biodiversity_on_forest_land_fertility": 1,
    },
)
def effect_of_biodiversity_on_forest_land_fertility():
    """
    Impact of mean species abundance on forest land fertility. Scaled between minimal and maximal impact. Relative level is the value of mean species abundance in year 1900.
    """
    return min_impact_of_biodiversity_on_forest_land_fertility() + (
        max_impact_of_biodiversity_on_forest_land_fertility()
        - min_impact_of_biodiversity_on_forest_land_fertility()
    ) * (mean_species_abundance() / init_species_abundance())


@component.add(
    name="Effect of Carbon Concentration on Agricultural Yield",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"distortion_function_c": 1},
)
def effect_of_carbon_concentration_on_agricultural_yield():
    """
    Impact of carbon concentration on cropland fertility. L C on Yield / (1 + EXP(-k C on Yield * (C Concentration Ratio - x0 C on Yield)) )
    """
    return distortion_function_c()


@component.add(
    name="Effect of Climate Change on Agricultural Yield",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"distorted_effect_of_t_on_yield": 1, "time": 1},
)
def effect_of_climate_change_on_agricultural_yield():
    """
    Impact of climate change risk on cropland fertility. L T on Yield / (1 + EXP(-k T on Yield * (Temperature Change from Preindustrial - x0 T on Yield)) )
    """
    return 1 + step(__data["time"], distorted_effect_of_t_on_yield() - 1, 2020)


@component.add(
    name="Effect of Climate Change on Forest Land Fertility",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "climate_impact_on_forest_land_fertility_scale": 1,
        "climate_impact_on_forest_land_fertility_reference_temperature": 1,
        "temperature_change_from_preindustrial": 1,
        "climate_impact_on_forest_land_fertility_nonlinearity": 1,
    },
)
def effect_of_climate_change_on_forest_land_fertility():
    """
    Impact of climate change risk on forest land fertility.
    """
    return (
        1
        - climate_impact_on_forest_land_fertility_scale()
        * (
            temperature_change_from_preindustrial()
            / climate_impact_on_forest_land_fertility_reference_temperature()
        )
        ** climate_impact_on_forest_land_fertility_nonlinearity()
    )


@component.add(
    name="Effect of CO2 Concentration on Forest Land Fertility",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_effect_of_co2_concentration_on_forest_land_fertility": 2,
        "c_concentration_ratio": 2,
        "min_effect_of_co2_concentration_on_forest_land_fertility": 1,
        "elasticity_of_co2_concentration_on_forest_land_fertility": 1,
    },
)
def effect_of_co2_concentration_on_forest_land_fertility():
    """
    Impact of carbon concentration on forest land fertility. Scaled between minimal and maximal impact.
    """
    return max_effect_of_co2_concentration_on_forest_land_fertility() + (
        min_effect_of_co2_concentration_on_forest_land_fertility()
        - max_effect_of_co2_concentration_on_forest_land_fertility()
    ) * (
        (c_concentration_ratio() - 1)
        / (
            (c_concentration_ratio() - 1)
            + elasticity_of_co2_concentration_on_forest_land_fertility()
        )
    )


@component.add(
    name="Effect of GDP on Cropland Management Practices Elasticity",
    units="(Year*Year*Person*Person)/($*$)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effect_of_gdp_on_cropland_management_practices_elasticity_variation": 1,
        "time": 1,
    },
)
def effect_of_gdp_on_cropland_management_practices_elasticity():
    """
    Elasticity of impact of GDP on cropland management practices.
    """
    return 2.2e-08 + step(
        __data["time"],
        effect_of_gdp_on_cropland_management_practices_elasticity_variation() - 2.2e-08,
        2020,
    )


@component.add(
    name="Effect of GDP on Cropland Management Practices Elasticity Variation",
    units="(Year*Year*Person*Person)/($*$)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effect_of_gdp_on_cropland_management_practices_elasticity_variation():
    """
    Elasticity of impact of GDP on cropland management practices.
    """
    return 2.2e-08


@component.add(
    name="Effect of GDP on Cropland Management Practices Increment",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"variable8_cropland_mp": 1},
)
def effect_of_gdp_on_cropland_management_practices_increment():
    """
    Increment of impact of GDP on cropland management practices.
    """
    return variable8_cropland_mp()


@component.add(
    name="Effect of GDP on Forest Land Fertility Elasticity",
    units="(Year*Year*Person*Person)/($*$)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effect_of_gdp_on_forest_land_fertility_elasticity_variation": 1,
        "time": 1,
    },
)
def effect_of_gdp_on_forest_land_fertility_elasticity():
    """
    Elasticity of impact of GDP on forest land management practices.
    """
    return 9e-08 + step(
        __data["time"],
        effect_of_gdp_on_forest_land_fertility_elasticity_variation() - 7e-08,
        2020,
    )


@component.add(
    name="Effect of GDP on Forest Land Fertility Elasticity Variation",
    units="(Year*Year*Person*Person)/($*$)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effect_of_gdp_on_forest_land_fertility_elasticity_variation():
    """
    Elasticity of impact of GDP on forest land management practices.
    """
    return 7e-08


@component.add(
    name="Effect of GDP on Forest Management Practices Increment",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"variable7_forest_mp": 1},
)
def effect_of_gdp_on_forest_management_practices_increment():
    """
    Increment of impact of GDP on forest land management practices.
    """
    return variable7_forest_mp()


@component.add(
    name="Effect of GDP on Urban Land Requirement",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "l_urban_land": 1,
        "relative_gwp_per_capita": 1,
        "k_urban_land": 1,
        "x0_urban_land": 1,
    },
)
def effect_of_gdp_on_urban_land_requirement():
    """
    k urban land +
    """
    return l_urban_land() / (
        1
        + float(np.exp(-k_urban_land() * (relative_gwp_per_capita() - x0_urban_land())))
    )


@component.add(
    name="Effect of GDP on Urban Land Requirement k Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effect_of_gdp_on_urban_land_requirement_k_variation():
    return 1


@component.add(
    name="Effect of GDP on Urban Land Requirement l Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effect_of_gdp_on_urban_land_requirement_l_variation():
    return 1.25


@component.add(
    name="Effect of GDP on Urban Land Requirement x0 Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effect_of_gdp_on_urban_land_requirement_x0_variation():
    return 5


@component.add(
    name="Effect of Input Neutral Technology Change on Agricultural Land Fertility",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"l_gdp_agritech": 1, "relative_gwp_per_capita": 1, "k_gdp_agritech": 1},
)
def effect_of_input_neutral_technology_change_on_agricultural_land_fertility():
    """
    Impact of technological advancement on agricultural land fertility. 1+Reference Input Neutral TC in Agriculture Variation*(LN(Relative GWP per Capita+Delay in GWP for agriculture technology impact ))
    """
    return l_gdp_agritech() - float(
        np.exp(-k_gdp_agritech() * relative_gwp_per_capita())
    )


@component.add(
    name="Effect of Input Neutral Technology Change on Forest Land Fertility",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "input_neutral_forest_technology": 1,
        "init_input_neutral_tc_in_forest": 1,
    },
)
def effect_of_input_neutral_technology_change_on_forest_land_fertility():
    """
    Impact of technological advancement on forest land fertility.
    """
    return input_neutral_forest_technology() / init_input_neutral_tc_in_forest()


@component.add(
    name="Effect of Management Practices on Agriculture Land Fertility",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effect_of_gdp_on_cropland_management_practices_increment": 1,
        "smoothed_gwp_per_capita": 2,
        "effect_of_gdp_on_cropland_management_practices_elasticity": 1,
    },
)
def effect_of_management_practices_on_agriculture_land_fertility():
    """
    Impact of agricultural land management practices on cropland fertility.
    """
    return 1 + effect_of_gdp_on_cropland_management_practices_increment() * (
        1
        - float(
            np.exp(
                -effect_of_gdp_on_cropland_management_practices_elasticity()
                * smoothed_gwp_per_capita()
                * smoothed_gwp_per_capita()
            )
        )
    )


@component.add(
    name="Effect of Management Practices on Forest Land Fertility",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effect_of_gdp_on_forest_management_practices_increment": 1,
        "effect_of_gdp_on_forest_land_fertility_elasticity": 1,
        "gwp_per_capita": 2,
    },
)
def effect_of_management_practices_on_forest_land_fertility():
    """
    Impact of forest land management practices on forest land fertility.
    """
    return 1 + effect_of_gdp_on_forest_management_practices_increment() * (
        1
        - float(
            np.exp(
                -effect_of_gdp_on_forest_land_fertility_elasticity()
                * gwp_per_capita()
                * gwp_per_capita()
            )
        )
    )


@component.add(
    name="Effect of T on Yield Lookup",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_effect_of_t_on_yield_lookup"},
)
def effect_of_t_on_yield_lookup(x, final_subs=None):
    return _hardcodedlookup_effect_of_t_on_yield_lookup(x, final_subs)


_hardcodedlookup_effect_of_t_on_yield_lookup = HardcodedLookups(
    [1.25, 1.5, 2.0, 2.5, 3.0],
    [1.0, 1.0, 1.0, 1.0, 1.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_effect_of_t_on_yield_lookup",
)


@component.add(
    name="Effect of Trees Aging on Yield",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_production_fraction": 1, "table_for_etay": 1},
)
def effect_of_trees_aging_on_yield():
    """
    Parameter accounting for decreased forest biomass production from aging tress.
    """
    return table_for_etay(desired_production_fraction())


@component.add(
    name="Effect of Trees Maturing on Yield",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_production_fraction": 1, "table_for_etmy": 1},
)
def effect_of_trees_maturing_on_yield():
    """
    Parameter accounting for increased forest biomass production from mature trees.
    """
    return table_for_etmy(desired_production_fraction())


@component.add(
    name="Effect of Water Withdrawal on Agriculture Land Fertility",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"agricultural_water_withdrawal_fulfillment_rate": 1},
)
def effect_of_water_withdrawal_on_agriculture_land_fertility():
    """
    Impact of water availability on cropland fertility.
    """
    return agricultural_water_withdrawal_fulfillment_rate()


@component.add(name="EGI S", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def egi_s():
    return 1.25


@component.add(
    name="EGI Var S",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"egi_s": 1, "time": 1},
)
def egi_var_s():
    return 1.25 + step(__data["time"], egi_s() - 1.25, 2020)


@component.add(name="EGX S", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def egx_s():
    return 5


@component.add(
    name="EGX Var S",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"egx_s": 1, "time": 1},
)
def egx_var_s():
    return 5 + step(__data["time"], egx_s() - 5, 2020)


@component.add(
    name="Elasticity of CO2 Concentration on Forest Land Fertility",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def elasticity_of_co2_concentration_on_forest_land_fertility():
    """
    Elasticity of impact of carbon concentration on forest land fertility.
    """
    return 1


@component.add(
    name="End Year of Waste Switch",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def end_year_of_waste_switch():
    return 2040


@component.add(
    name="Energy Crops Production",
    units="Biomass ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "arable_land_allocated_for_energy_crops": 1,
        "agriculture_land_energy_yield": 1,
    },
)
def energy_crops_production():
    """
    Total energy biomass production from energy crops.
    """
    return arable_land_allocated_for_energy_crops() * agriculture_land_energy_yield()


@component.add(
    name="Energy Crops Production Indicator",
    units="Biomass million ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_crops_production": 1,
        "biomass_ton_into_biomass_million_ton": 1,
    },
)
def energy_crops_production_indicator():
    return energy_crops_production() * biomass_ton_into_biomass_million_ton()


@component.add(
    name="Expected crop yield",
    units="Ton/(Year*ha)",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_exya": 1},
)
def expected_crop_yield():
    return outflow_exya()


@component.add(
    name="Expected Crop Yield Accumulative",
    units="Ton/ha",
    subscripts=["PlantFood"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_expected_crop_yield_accumulative": 1},
    other_deps={
        "_integ_expected_crop_yield_accumulative": {
            "initial": {"init_crop_yield": 1},
            "step": {"inflow_exya": 1, "outflow_exya": 1},
        }
    },
)
def expected_crop_yield_accumulative():
    """
    For coverting DELAY1I function only. Added by Q Ye in July 2024
    """
    return _integ_expected_crop_yield_accumulative()


_integ_expected_crop_yield_accumulative = Integ(
    lambda: inflow_exya() - outflow_exya(),
    lambda: init_crop_yield(),
    "_integ_expected_crop_yield_accumulative",
)


@component.add(
    name="Expected Grassland Meat Yield",
    units="Ton/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_egmeya": 1},
)
def expected_grassland_meat_yield():
    return outflow_egmeya()


@component.add(
    name="Expected Grassland Meat Yield Accumulative",
    units="Ton/ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_expected_grassland_meat_yield_accumulative": 1},
    other_deps={
        "_integ_expected_grassland_meat_yield_accumulative": {
            "initial": {"initial_grassland_meat_yield": 1},
            "step": {"inflow_egmeya": 1, "outflow_egmeya": 1},
        }
    },
)
def expected_grassland_meat_yield_accumulative():
    """
    For coverting DELAY1I function only. Added by Q Ye in July 2024
    """
    return _integ_expected_grassland_meat_yield_accumulative()


_integ_expected_grassland_meat_yield_accumulative = Integ(
    lambda: inflow_egmeya() - outflow_egmeya(),
    lambda: initial_grassland_meat_yield() * 1,
    "_integ_expected_grassland_meat_yield_accumulative",
)


@component.add(
    name="Expected Grassland Milk Yield",
    units="Ton/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_egmya": 1},
)
def expected_grassland_milk_yield():
    return outflow_egmya()


@component.add(
    name="Expected Grassland Milk Yield Accumulative",
    units="Ton/Year",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_expected_grassland_milk_yield_accumulative": 1},
    other_deps={
        "_integ_expected_grassland_milk_yield_accumulative": {
            "initial": {"initial_grassland_milk_yield": 1},
            "step": {"inflow_egmya": 1, "outflow_egmya": 1},
        }
    },
)
def expected_grassland_milk_yield_accumulative():
    """
    For coverting DELAY1I function only. Added by Q Ye in July 2024
    """
    return _integ_expected_grassland_milk_yield_accumulative()


_integ_expected_grassland_milk_yield_accumulative = Integ(
    lambda: inflow_egmya() - outflow_egmya(),
    lambda: initial_grassland_milk_yield(),
    "_integ_expected_grassland_milk_yield_accumulative",
)


@component.add(name="FAT S", units="Year", comp_type="Constant", comp_subtype="Normal")
def fat_s():
    return 5


@component.add(
    name="FAT Var S",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_fat_var_s": 1},
    other_deps={
        "_smooth_fat_var_s": {
            "initial": {"fat_s": 1, "time": 1},
            "step": {"fat_s": 1, "time": 1},
        }
    },
)
def fat_var_s():
    return 5 + _smooth_fat_var_s()


_smooth_fat_var_s = Smooth(
    lambda: step(__data["time"], fat_s() - 5, 2020),
    lambda: 1,
    lambda: step(__data["time"], fat_s() - 5, 2020),
    lambda: 1,
    "_smooth_fat_var_s",
)


@component.add(
    name="Feed Availability",
    units="Ton/Year",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"production_rate_of_crops": 1, "feed_fraction_in_demand": 1},
)
def feed_availability():
    return production_rate_of_crops() * feed_fraction_in_demand()


@component.add(
    name="Feed demand in tonnes",
    units="Ton/Year",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "food_demand_in_tonnes": 1,
        "feed_share_of_crop_types": 1,
        "unit_feed_used_for_meat_production": 1,
    },
)
def feed_demand_in_tonnes():
    """
    The amount of PlantFood required for crop-based meat production
    """
    return (
        float(food_demand_in_tonnes().loc["CropMeat"])
        * feed_share_of_crop_types()
        * unit_feed_used_for_meat_production()
    )


@component.add(
    name="Feed fraction in demand",
    units="Dmnl",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"feed_demand_in_tonnes": 1, "desired_crop_production": 1},
)
def feed_fraction_in_demand():
    return feed_demand_in_tonnes() / desired_crop_production()


@component.add(
    name="Feed per meat DATA",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def feed_per_meat_data():
    """
    The amount (in tonnes) of feed for each crop type required to produce 1 ton of crop-based meat. Estimated based on the FAO data for Feed and Meat production, the data for 1961-1985. See FoodBalanceSheets.xlsx
    """
    return np.interp(
        time(),
        [
            1961.0,
            1962.0,
            1963.0,
            1964.0,
            1965.0,
            1966.0,
            1967.0,
            1968.0,
            1969.0,
            1970.0,
            1971.0,
            1972.0,
            1973.0,
            1974.0,
            1975.0,
            1976.0,
            1977.0,
            1978.0,
            1979.0,
            1980.0,
            1981.0,
            1982.0,
            1983.0,
            1984.0,
            1985.0,
            1986.0,
            1987.0,
            1988.0,
            1989.0,
            1990.0,
            1991.0,
            1992.0,
            1993.0,
            1994.0,
            1995.0,
            1996.0,
            1997.0,
            1998.0,
            1999.0,
            2000.0,
            2001.0,
            2002.0,
            2003.0,
            2004.0,
            2005.0,
            2006.0,
            2007.0,
            2008.0,
            2009.0,
            2010.0,
            2011.0,
            2012.0,
            2013.0,
        ],
        [
            12.7,
            12.78,
            12.5,
            12.79,
            12.41,
            12.59,
            12.34,
            13.04,
            13.19,
            12.89,
            12.19,
            12.01,
            12.36,
            11.37,
            11.49,
            11.78,
            11.66,
            11.63,
            10.84,
            10.0,
            9.84,
            9.98,
            9.48,
            9.76,
            9.42,
            9.34,
            9.01,
            8.19,
            8.23,
            8.09,
            7.66,
            7.56,
            7.35,
            7.07,
            6.68,
            6.91,
            6.6,
            6.25,
            6.15,
            6.2,
            6.24,
            5.99,
            5.84,
            6.1,
            5.85,
            5.61,
            5.49,
            5.55,
            5.22,
            5.09,
            5.35,
            5.1,
            5.39,
        ],
    )


@component.add(
    name="Feed share of crop types",
    units="Dmnl",
    subscripts=["PlantFood"],
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "feed_share_of_crop_types_data": 4,
        "_smooth_feed_share_of_crop_types": 1,
        "_smooth_feed_share_of_crop_types_1": 1,
        "_smooth_feed_share_of_crop_types_2": 1,
        "_smooth_feed_share_of_crop_types_3": 1,
    },
    other_deps={
        "_smooth_feed_share_of_crop_types": {
            "initial": {"feed_share_of_grains_variation": 1, "time": 1},
            "step": {
                "feed_share_of_grains_variation": 1,
                "time": 1,
                "ssp_food_and_diet_variation_time": 1,
            },
        },
        "_smooth_feed_share_of_crop_types_1": {
            "initial": {"feed_share_of_vegfruits_variation": 1, "time": 1},
            "step": {
                "feed_share_of_vegfruits_variation": 1,
                "time": 1,
                "ssp_food_and_diet_variation_time": 1,
            },
        },
        "_smooth_feed_share_of_crop_types_2": {
            "initial": {"feed_share_of_pulses_variation": 1, "time": 1},
            "step": {
                "feed_share_of_pulses_variation": 1,
                "time": 1,
                "ssp_food_and_diet_variation_time": 1,
            },
        },
        "_smooth_feed_share_of_crop_types_3": {
            "initial": {"feed_share_of_othercrops_variation": 1, "time": 1},
            "step": {
                "feed_share_of_othercrops_variation": 1,
                "time": 1,
                "ssp_food_and_diet_variation_time": 1,
            },
        },
    },
)
def feed_share_of_crop_types():
    """
    This parameter represents the fraction of each crop type in the total feed amount used to produce crop-based meat, i.e. pork and poultry. For instance, if the value of this parameter for grains is 72%, it means that 72% of total feed comes from grains. It is estimated based on the FAO balance sheets, the data for 1961-1985, by summing the amount of each crop type used as feed. See FoodBalanceSheets.xlsx
    """
    value = xr.DataArray(
        np.nan, {"PlantFood": _subscript_dict["PlantFood"]}, ["PlantFood"]
    )
    value.loc[["Grains"]] = (
        float(feed_share_of_crop_types_data().loc["Grains"])
        * (1 + _smooth_feed_share_of_crop_types())
    ).values
    value.loc[["VegFruits"]] = (
        float(feed_share_of_crop_types_data().loc["VegFruits"])
        * (1 + _smooth_feed_share_of_crop_types_1())
    ).values
    value.loc[["Pulses"]] = (
        float(feed_share_of_crop_types_data().loc["Pulses"])
        * (1 + _smooth_feed_share_of_crop_types_2())
    ).values
    value.loc[["OtherCrops"]] = (
        float(feed_share_of_crop_types_data().loc["OtherCrops"])
        * (1 + _smooth_feed_share_of_crop_types_3())
    ).values
    return value


_smooth_feed_share_of_crop_types = Smooth(
    lambda: xr.DataArray(
        step(__data["time"], feed_share_of_grains_variation() - 1, 2020),
        {"AllPlantButOther": ["Grains"]},
        ["AllPlantButOther"],
    ),
    lambda: xr.DataArray(
        ssp_food_and_diet_variation_time(),
        {"AllPlantButOther": ["Grains"]},
        ["AllPlantButOther"],
    ),
    lambda: xr.DataArray(
        step(__data["time"], feed_share_of_grains_variation() - 1, 2020),
        {"AllPlantButOther": ["Grains"]},
        ["AllPlantButOther"],
    ),
    lambda: 1,
    "_smooth_feed_share_of_crop_types",
)

_smooth_feed_share_of_crop_types_1 = Smooth(
    lambda: xr.DataArray(
        step(__data["time"], feed_share_of_vegfruits_variation() - 1, 2020),
        {"AllPlantButOther": ["VegFruits"]},
        ["AllPlantButOther"],
    ),
    lambda: xr.DataArray(
        ssp_food_and_diet_variation_time(),
        {"AllPlantButOther": ["VegFruits"]},
        ["AllPlantButOther"],
    ),
    lambda: xr.DataArray(
        step(__data["time"], feed_share_of_vegfruits_variation() - 1, 2020),
        {"AllPlantButOther": ["VegFruits"]},
        ["AllPlantButOther"],
    ),
    lambda: 1,
    "_smooth_feed_share_of_crop_types_1",
)

_smooth_feed_share_of_crop_types_2 = Smooth(
    lambda: xr.DataArray(
        step(__data["time"], feed_share_of_pulses_variation() - 1, 2020),
        {"AllPlantButOther": ["Pulses"]},
        ["AllPlantButOther"],
    ),
    lambda: xr.DataArray(
        ssp_food_and_diet_variation_time(),
        {"AllPlantButOther": ["Pulses"]},
        ["AllPlantButOther"],
    ),
    lambda: xr.DataArray(
        step(__data["time"], feed_share_of_pulses_variation() - 1, 2020),
        {"AllPlantButOther": ["Pulses"]},
        ["AllPlantButOther"],
    ),
    lambda: 1,
    "_smooth_feed_share_of_crop_types_2",
)

_smooth_feed_share_of_crop_types_3 = Smooth(
    lambda: xr.DataArray(
        step(__data["time"], feed_share_of_othercrops_variation() - 1, 2020),
        {"PlantFood": ["OtherCrops"]},
        ["PlantFood"],
    ),
    lambda: xr.DataArray(
        ssp_food_and_diet_variation_time(), {"PlantFood": ["OtherCrops"]}, ["PlantFood"]
    ),
    lambda: xr.DataArray(
        step(__data["time"], feed_share_of_othercrops_variation() - 1, 2020),
        {"PlantFood": ["OtherCrops"]},
        ["PlantFood"],
    ),
    lambda: 1,
    "_smooth_feed_share_of_crop_types_3",
)


@component.add(
    name="Feed share of crop types Data",
    units="Dmnl",
    subscripts=["PlantFood"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def feed_share_of_crop_types_data():
    """
    PlantFood includes Pulses, grains, vegfruits, and other crops
    """
    return xr.DataArray(
        [0.014, 0.715, 0.223, 0.048],
        {"PlantFood": _subscript_dict["PlantFood"]},
        ["PlantFood"],
    )


@component.add(
    name="Feed Share of Grains Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def feed_share_of_grains_variation():
    return 1


@component.add(
    name="Feed Share of OtherCrops Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def feed_share_of_othercrops_variation():
    return 1


@component.add(
    name="Feed Share of Pulses Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def feed_share_of_pulses_variation():
    return 1


@component.add(
    name="Feed Share of VegFruits Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def feed_share_of_vegfruits_variation():
    return 1


@component.add(
    name="Fertilization Related Practices",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effect_of_input_neutral_technology_change_on_agricultural_land_fertility": 1,
        "effect_of_management_practices_on_agriculture_land_fertility": 1,
    },
)
def fertilization_related_practices():
    """
    Variable representing extent of technical advancement and management practices related to fertilization.
    """
    return (
        effect_of_input_neutral_technology_change_on_agricultural_land_fertility()
        * effect_of_management_practices_on_agriculture_land_fertility()
    )


@component.add(
    name="Food demand in tonnes",
    units="Ton/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_caloric_demand_inc_waste": 1, "caloric_value_of_food": 1},
)
def food_demand_in_tonnes():
    return annual_caloric_demand_inc_waste() / caloric_value_of_food()


@component.add(
    name="Food fraction in demand",
    units="Dmnl",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"food_demand_in_tonnes": 1, "desired_crop_production": 1},
)
def food_fraction_in_demand():
    return (
        food_demand_in_tonnes()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        / desired_crop_production()
    )


@component.add(
    name="Food production rate",
    units="Ton/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"production_rate_of_crops": 1, "production_rate_of_animal_food": 1},
)
def food_production_rate():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = production_rate_of_crops().values
    value.loc[_subscript_dict["AnimalFood"]] = (
        production_rate_of_animal_food().rename({"MapAltProteins": "AnimalFood"}).values
    )
    return value


@component.add(
    name="Food shortage in kcal",
    units="Mkcal/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_caloric_demand_inc_waste": 1, "food_supply_in_kcal": 1},
)
def food_shortage_in_kcal():
    return annual_caloric_demand_inc_waste() - food_supply_in_kcal()


@component.add(
    name="Food shortage in tonnes",
    units="Ton/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"food_demand_in_tonnes": 1, "food_supply_in_tonnes": 1},
)
def food_shortage_in_tonnes():
    return food_demand_in_tonnes() - food_supply_in_tonnes()


@component.add(
    name="Food supply in kcal",
    units="Mkcal/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"caloric_value_of_food": 1, "food_supply_in_tonnes": 1},
)
def food_supply_in_kcal():
    return caloric_value_of_food() * food_supply_in_tonnes()


@component.add(
    name="Food supply in tonnes",
    units="Ton/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"food_production_rate": 2, "food_fraction_in_demand": 1},
)
def food_supply_in_tonnes():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = (
        food_production_rate()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        * food_fraction_in_demand()
    ).values
    value.loc[_subscript_dict["AnimalFood"]] = (
        food_production_rate()
        .loc[_subscript_dict["AnimalFood"]]
        .rename({"FoodCategories": "AnimalFood"})
        .values
    )
    return value


@component.add(
    name="Forest Biomass Production",
    units="Biomass ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_forest_biomass_demand": 1,
        "harvest_available_forest_land": 1,
        "forest_land_energy_yield": 1,
        "biomass_production_processing_loss": 1,
    },
)
def forest_biomass_production():
    """
    Total biomass production from forest.
    """
    return float(
        np.minimum(
            total_forest_biomass_demand(),
            harvest_available_forest_land()
            * forest_land_energy_yield()
            * (1 - biomass_production_processing_loss()),
        )
    )


@component.add(
    name="Forest Land",
    units="ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_forest_land": 1},
    other_deps={
        "_integ_forest_land": {
            "initial": {"init_forest_land": 1},
            "step": {
                "forestation_from_agricultural_land": 1,
                "forestation_from_other_land": 1,
                "deforestation_to_agricultural_land": 1,
                "deforestation_to_urban_land": 1,
            },
        }
    },
)
def forest_land():
    """
    Total Forest Land.
    """
    return _integ_forest_land()


_integ_forest_land = Integ(
    lambda: forestation_from_agricultural_land()
    + forestation_from_other_land()
    - deforestation_to_agricultural_land()
    - deforestation_to_urban_land(),
    lambda: init_forest_land(),
    "_integ_forest_land",
)


@component.add(
    name="Forest Land Discrepancy",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "forest_land_needed_to_be_harvested": 1,
        "harvest_available_forest_land": 1,
    },
)
def forest_land_discrepancy():
    return float(
        np.maximum(
            0, forest_land_needed_to_be_harvested() - harvest_available_forest_land()
        )
    )


@component.add(
    name="Forest Land Energy Yield",
    units="Biomass ton/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "forest_land_yield": 1,
        "effect_of_trees_maturing_on_yield": 1,
        "effect_of_trees_aging_on_yield": 1,
    },
)
def forest_land_energy_yield():
    """
    Forest Land Energy Yield accounting for reference forest biomass production and effect of trees age.
    """
    return (
        forest_land_yield()
        * effect_of_trees_maturing_on_yield()
        * effect_of_trees_aging_on_yield()
    )


@component.add(
    name="Forest Land Fertility",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_forest_land_fertility": 1,
        "effect_of_climate_change_on_forest_land_fertility": 1,
        "effect_of_management_practices_on_forest_land_fertility": 1,
        "effect_of_co2_concentration_on_forest_land_fertility": 1,
        "effect_of_biodiversity_on_forest_land_fertility": 1,
        "effect_of_input_neutral_technology_change_on_forest_land_fertility": 1,
    },
)
def forest_land_fertility():
    """
    Multiplier inidcating forest land fertility i.e. how many times the nominal forest land yield has changed since the reference value in year 1900.
    """
    return (
        normal_forest_land_fertility()
        * effect_of_climate_change_on_forest_land_fertility()
        * effect_of_management_practices_on_forest_land_fertility()
        * effect_of_co2_concentration_on_forest_land_fertility()
        * effect_of_biodiversity_on_forest_land_fertility()
        * effect_of_input_neutral_technology_change_on_forest_land_fertility()
    )


@component.add(
    name="Forest Land Fraction Harvested excluding Protected Area",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "forest_land_fraction_harvested_excluding_protected_area_variation": 1,
        "time": 1,
    },
)
def forest_land_fraction_harvested_excluding_protected_area():
    """
    Fraction of Forest dedicated to be harvested.
    """
    return 0.5 + step(
        __data["time"],
        forest_land_fraction_harvested_excluding_protected_area_variation() - 0.5,
        2020,
    )


@component.add(
    name="Forest Land Fraction Harvested excluding Protected Area Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def forest_land_fraction_harvested_excluding_protected_area_variation():
    """
    Fraction of Forest dedicated to be harvested.
    """
    return 0.5


@component.add(
    name="Forest Land Indicator",
    units="Million ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"forest_land": 1, "ha_into_million_ha": 1},
)
def forest_land_indicator():
    return forest_land() * ha_into_million_ha()


@component.add(
    name="Forest Land Needed to be Harvested",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_forest_biomass_demand": 1,
        "biomass_production_processing_loss": 1,
        "forest_land_energy_yield": 1,
    },
)
def forest_land_needed_to_be_harvested():
    """
    Total area of Forest needed for biomass production purposes accounting for total demand for forest biomass, average forest land yield and average losses in forest biomass production process.
    """
    return (
        total_forest_biomass_demand() / (1 - biomass_production_processing_loss())
    ) / forest_land_energy_yield()


@component.add(
    name="Forest Land Yield",
    units="Biomass ton/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "forest_land_fertility": 1,
        "nominal_energy_forest_land_productivity": 1,
    },
)
def forest_land_yield():
    """
    Actual annual amount of forest biomass production from unit forest land area for given Forest Land Fertility.
    """
    return forest_land_fertility() * nominal_energy_forest_land_productivity()


@component.add(
    name="Forest Protected Land",
    units="ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_forest_protected_land": 1},
    other_deps={
        "_integ_forest_protected_land": {
            "initial": {"init_forest_protected_land": 1},
            "step": {"forest_protected_land_change": 1},
        }
    },
)
def forest_protected_land():
    """
    Area of forest land indicated as protected. Source of historical data: http://www.fao.org/docrep/003/x4108e/X4108E11.htm# P3941_174357
    """
    return _integ_forest_protected_land()


_integ_forest_protected_land = Integ(
    lambda: forest_protected_land_change(),
    lambda: init_forest_protected_land(),
    "_integ_forest_protected_land",
)


@component.add(
    name="Forest Protected Land Change",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_fplclv3": 1},
)
def forest_protected_land_change():
    """
    Changes in area of forest land indicated as protected.
    """
    return outflow_fplclv3()


@component.add(
    name="Forest Protected Land Change LV1",
    units="ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_forest_protected_land_change_lv1": 1},
    other_deps={
        "_integ_forest_protected_land_change_lv1": {
            "initial": {"forest_protected_land_change_lv3": 1},
            "step": {"inflow_fplclv1": 1, "outflow_fplclv1": 1},
        }
    },
)
def forest_protected_land_change_lv1():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_forest_protected_land_change_lv1()


_integ_forest_protected_land_change_lv1 = Integ(
    lambda: inflow_fplclv1() - outflow_fplclv1(),
    lambda: forest_protected_land_change_lv3(),
    "_integ_forest_protected_land_change_lv1",
)


@component.add(
    name="Forest Protected Land Change LV2",
    units="ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_forest_protected_land_change_lv2": 1},
    other_deps={
        "_integ_forest_protected_land_change_lv2": {
            "initial": {"forest_protected_land_change_lv3": 1},
            "step": {"inflow_fplclv2": 1, "outflow_fplclv2": 1},
        }
    },
)
def forest_protected_land_change_lv2():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_forest_protected_land_change_lv2()


_integ_forest_protected_land_change_lv2 = Integ(
    lambda: inflow_fplclv2() - outflow_fplclv2(),
    lambda: forest_protected_land_change_lv3(),
    "_integ_forest_protected_land_change_lv2",
)


@component.add(
    name="Forest Protected Land Change LV3",
    units="ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_forest_protected_land_change_lv3": 1},
    other_deps={
        "_integ_forest_protected_land_change_lv3": {
            "initial": {"fraction_fplc": 1, "delay_time_fplclv": 1},
            "step": {"inflow_fplclv3": 1, "outflow_fplclv3": 1},
        }
    },
)
def forest_protected_land_change_lv3():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_forest_protected_land_change_lv3()


_integ_forest_protected_land_change_lv3 = Integ(
    lambda: inflow_fplclv3() - outflow_fplclv3(),
    lambda: fraction_fplc() * delay_time_fplclv(),
    "_integ_forest_protected_land_change_lv3",
)


@component.add(
    name="Forest Protected Land Change Ratio",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def forest_protected_land_change_ratio():
    """
    Ratio at which the gap between current and max forest protected land is closed.
    """
    return 0.1


@component.add(
    name="Forest to Agriculture Land Allocation Time",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "fat_var_s": 1,
        "_smooth_forest_to_agriculture_land_allocation_time": 1,
    },
    other_deps={
        "_smooth_forest_to_agriculture_land_allocation_time": {
            "initial": {
                "forest_to_agriculture_land_allocation_time_variation": 1,
                "fat_var_s": 1,
                "l_var_t": 1,
                "time": 1,
            },
            "step": {
                "forest_to_agriculture_land_allocation_time_variation": 1,
                "fat_var_s": 1,
                "l_var_t": 1,
                "time": 1,
                "ssp_land_use_change_variation_time": 1,
            },
        }
    },
)
def forest_to_agriculture_land_allocation_time():
    """
    Average time which natural transformation of Forest to Agriculture Land would take.130
    """
    return fat_var_s() + _smooth_forest_to_agriculture_land_allocation_time()


_smooth_forest_to_agriculture_land_allocation_time = Smooth(
    lambda: step(
        __data["time"],
        forest_to_agriculture_land_allocation_time_variation() - fat_var_s(),
        2020 + l_var_t(),
    ),
    lambda: ssp_land_use_change_variation_time(),
    lambda: step(
        __data["time"],
        forest_to_agriculture_land_allocation_time_variation() - fat_var_s(),
        2020 + l_var_t(),
    ),
    lambda: 1,
    "_smooth_forest_to_agriculture_land_allocation_time",
)


@component.add(
    name="Forest to Agriculture Land Allocation Time Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def forest_to_agriculture_land_allocation_time_variation():
    return 5


@component.add(
    name="Forest to Urban Land Allocation Time",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"forest_to_urban_land_allocation_time_variation": 1, "time": 1},
)
def forest_to_urban_land_allocation_time():
    """
    Average time which natural transformation of Forest to Urban and Industrial Land would take.
    """
    return 10 + step(
        __data["time"], forest_to_urban_land_allocation_time_variation() - 10, 2020
    )


@component.add(
    name="Forest to Urban Land Allocation Time Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def forest_to_urban_land_allocation_time_variation():
    """
    Average time which natural transformation of Forest to Urban and Industrial Land would take.
    """
    return 10


@component.add(
    name="Forestation from Agricultural Land",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agricultural_land": 1,
        "agriculture_protected_land": 1,
        "time_step": 1,
        "fraction_of_forest_land_conversion_from_agriculture": 1,
        "forest_land_discrepancy": 1,
        "agriculture_to_forest_land_allocation_time": 1,
    },
)
def forestation_from_agricultural_land():
    """
    Process of transformation between Forest and Agriculture Land.
    """
    return float(
        np.minimum(
            (agricultural_land() - agriculture_protected_land()) / time_step(),
            forest_land_discrepancy()
            * fraction_of_forest_land_conversion_from_agriculture()
            / agriculture_to_forest_land_allocation_time(),
        )
    )


@component.add(
    name="Forestation from Other Land",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "other_land": 1,
        "other_protected_land": 1,
        "other_to_forest_land_allocation_time": 2,
        "fraction_of_forest_land_conversion_from_agriculture": 1,
        "forest_land_discrepancy": 1,
    },
)
def forestation_from_other_land():
    return float(
        np.minimum(
            (other_land() - other_protected_land())
            / other_to_forest_land_allocation_time(),
            forest_land_discrepancy()
            * (1 - fraction_of_forest_land_conversion_from_agriculture())
            / other_to_forest_land_allocation_time(),
        )
    )


@component.add(
    name="Fraction FPLC",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"current_to_max_forest_protected_land": 1, "forest_protected_land": 1},
)
def fraction_fplc():
    return current_to_max_forest_protected_land() * forest_protected_land()


@component.add(
    name="Fraction of Agricultural Land Conversion from Forest",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "af_var_s": 1,
        "_smooth_fraction_of_agricultural_land_conversion_from_forest": 1,
    },
    other_deps={
        "_smooth_fraction_of_agricultural_land_conversion_from_forest": {
            "initial": {
                "fraction_of_agricultural_land_conversion_from_forest_variation": 1,
                "af_var_s": 1,
                "l_var_t": 1,
                "time": 1,
            },
            "step": {
                "fraction_of_agricultural_land_conversion_from_forest_variation": 1,
                "af_var_s": 1,
                "l_var_t": 1,
                "time": 1,
                "ssp_land_use_change_variation_time": 1,
            },
        }
    },
)
def fraction_of_agricultural_land_conversion_from_forest():
    return af_var_s() + _smooth_fraction_of_agricultural_land_conversion_from_forest()


_smooth_fraction_of_agricultural_land_conversion_from_forest = Smooth(
    lambda: step(
        __data["time"],
        fraction_of_agricultural_land_conversion_from_forest_variation() - af_var_s(),
        2020 + l_var_t(),
    ),
    lambda: ssp_land_use_change_variation_time(),
    lambda: step(
        __data["time"],
        fraction_of_agricultural_land_conversion_from_forest_variation() - af_var_s(),
        2020 + l_var_t(),
    ),
    lambda: 1,
    "_smooth_fraction_of_agricultural_land_conversion_from_forest",
)


@component.add(
    name="Fraction of Agricultural Land Conversion from Forest Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraction_of_agricultural_land_conversion_from_forest_variation():
    return 0.95


@component.add(
    name="Fraction of Forest Land Conversion from Agriculture",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fraction_of_forest_land_conversion_from_agriculture_variation": 1,
        "time": 1,
    },
)
def fraction_of_forest_land_conversion_from_agriculture():
    return 0.1 + step(
        __data["time"],
        fraction_of_forest_land_conversion_from_agriculture_variation() - 0.1,
        2020,
    )


@component.add(
    name="Fraction of Forest Land Conversion from Agriculture Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraction_of_forest_land_conversion_from_agriculture_variation():
    return 0.1


@component.add(
    name="Fraction of Urban Land Conversion from Agriculture",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fraction_of_urban_land_conversion_from_agriculture_variation": 1,
        "time": 1,
    },
)
def fraction_of_urban_land_conversion_from_agriculture():
    return 0.9 + step(
        __data["time"],
        fraction_of_urban_land_conversion_from_agriculture_variation() - 0.9,
        2020,
    )


@component.add(
    name="Fraction of Urban Land Conversion from Agriculture Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraction_of_urban_land_conversion_from_agriculture_variation():
    return 0.9


@component.add(
    name="Grassland Allocated for Food Production",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"permanent_meadows_and_pastures": 1, "grassland_allocation_demand": 1},
)
def grassland_allocated_for_food_production():
    return float(
        np.minimum(permanent_meadows_and_pastures(), grassland_allocation_demand())
    )


@component.add(
    name="Grassland allocation demand",
    units="ha",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_grassland_allocation_demand": 1},
    other_deps={
        "_smooth_grassland_allocation_demand": {
            "initial": {"total_grassland_needed": 1},
            "step": {"total_grassland_needed": 1},
        }
    },
)
def grassland_allocation_demand():
    return _smooth_grassland_allocation_demand()


_smooth_grassland_allocation_demand = Smooth(
    lambda: total_grassland_needed(),
    lambda: 5,
    lambda: total_grassland_needed(),
    lambda: 1,
    "_smooth_grassland_allocation_demand",
)


@component.add(
    name="Grassland allocation fraction",
    units="Dmnl",
    subscripts=["MapAltProteins"],
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "_smooth_grassland_allocation_fraction": 1,
        "_smooth_grassland_allocation_fraction_1": 1,
    },
    other_deps={
        "_smooth_grassland_allocation_fraction": {
            "initial": {"demand_fraction_of_grassland": 1},
            "step": {"demand_fraction_of_grassland": 1},
        },
        "_smooth_grassland_allocation_fraction_1": {
            "initial": {"demand_fraction_of_grassland": 1},
            "step": {"demand_fraction_of_grassland": 1},
        },
    },
)
def grassland_allocation_fraction():
    value = xr.DataArray(
        np.nan,
        {"MapAltProteins": _subscript_dict["MapAltProteins"]},
        ["MapAltProteins"],
    )
    value.loc[["PasMeat"]] = _smooth_grassland_allocation_fraction().values
    value.loc[["Dairy"]] = _smooth_grassland_allocation_fraction_1().values
    return value


_smooth_grassland_allocation_fraction = Smooth(
    lambda: xr.DataArray(
        float(demand_fraction_of_grassland().loc["PasMeat"]),
        {"MapAltProteins": ["PasMeat"]},
        ["MapAltProteins"],
    ),
    lambda: xr.DataArray(5, {"MapAltProteins": ["PasMeat"]}, ["MapAltProteins"]),
    lambda: xr.DataArray(
        float(demand_fraction_of_grassland().loc["PasMeat"]),
        {"MapAltProteins": ["PasMeat"]},
        ["MapAltProteins"],
    ),
    lambda: 1,
    "_smooth_grassland_allocation_fraction",
)

_smooth_grassland_allocation_fraction_1 = Smooth(
    lambda: xr.DataArray(
        float(demand_fraction_of_grassland().loc["Dairy"]),
        {"MapAltProteins": ["Dairy"]},
        ["MapAltProteins"],
    ),
    lambda: xr.DataArray(5, {"MapAltProteins": ["Dairy"]}, ["MapAltProteins"]),
    lambda: xr.DataArray(
        float(demand_fraction_of_grassland().loc["Dairy"]),
        {"MapAltProteins": ["Dairy"]},
        ["MapAltProteins"],
    ),
    lambda: 1,
    "_smooth_grassland_allocation_fraction_1",
)


@component.add(
    name="Grassland Meat Yield",
    units="Ton/(ha*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_meat_yield": 1,
        "effect_of_input_neutral_technology_change_on_agricultural_land_fertility": 1,
        "effect_of_climate_change_on_agricultural_yield": 1,
        "effect_of_carbon_concentration_on_agricultural_yield": 1,
        "effect_of_fertilizer_on_yield": 1,
        "effect_of_water_withdrawal_on_agriculture_land_fertility": 1,
    },
)
def grassland_meat_yield():
    """
    Tons of meat per ha of grassland.The data for this variable is calculated based on the total production of pasture-based animal products (bovine meat, butter, cheese, animal fat, milk, mutton and goat meat) divided by the total pasture land.
    """
    return (
        reference_meat_yield()
        * effect_of_input_neutral_technology_change_on_agricultural_land_fertility()
        * effect_of_climate_change_on_agricultural_yield()
        * effect_of_carbon_concentration_on_agricultural_yield()
        * float(effect_of_fertilizer_on_yield().loc["PasMeat"])
        * effect_of_water_withdrawal_on_agriculture_land_fertility()
    )


@component.add(
    name="Grassland Meat Yield Indicator",
    units="Ton/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grassland_meat_yield": 1},
)
def grassland_meat_yield_indicator():
    return grassland_meat_yield()


@component.add(
    name="Grassland Milk Yield",
    units="Ton/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grassland_meat_yield": 1, "meat_to_milk_multiplier": 1},
)
def grassland_milk_yield():
    return grassland_meat_yield() * meat_to_milk_multiplier()


@component.add(
    name="Grassland Needed",
    units="ha",
    subscripts=["MapAltProteins"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "food_demand_in_tonnes": 2,
        "expected_grassland_meat_yield": 1,
        "expected_grassland_milk_yield": 1,
    },
)
def grassland_needed():
    value = xr.DataArray(
        np.nan,
        {"MapAltProteins": _subscript_dict["MapAltProteins"]},
        ["MapAltProteins"],
    )
    value.loc[["PasMeat"]] = (
        float(food_demand_in_tonnes().loc["PasMeat"]) / expected_grassland_meat_yield()
    )
    value.loc[["Dairy"]] = (
        float(food_demand_in_tonnes().loc["Dairy"]) / expected_grassland_milk_yield()
    )
    return value


@component.add(
    name="Half Measures",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "scenario_half_measures": 2,
        "time": 1,
        "half_measures_scenario_ramp_change": 1,
    },
)
def half_measures():
    """
    WWF Scenario variable. Further development required.
    """
    return (1 - scenario_half_measures()) * 1 + scenario_half_measures() * (
        1 + ramp(__data["time"], half_measures_scenario_ramp_change(), 2010, 2020)
    )


@component.add(
    name="Half Measures Deforestation Time Factor",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "scenario_half_measures": 1,
        "time": 1,
        "half_measures_scenario_ramp_time_change": 1,
    },
)
def half_measures_deforestation_time_factor():
    """
    WWF Scenario variable. Further development required.
    """
    return scenario_half_measures() * ramp(
        __data["time"], half_measures_scenario_ramp_time_change(), 2019, 2020
    )


@component.add(
    name="Half Measures Scenario Ramp Change",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def half_measures_scenario_ramp_change():
    """
    WWF Scenario variable. Further development required.
    """
    return -0.0215


@component.add(
    name="Half Measures Scenario Ramp Time Change",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def half_measures_scenario_ramp_time_change():
    """
    WWF Scenario variable. Further development required.
    """
    return 1


@component.add(
    name="Harvest Available Forest Land",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "forest_land_fraction_harvested_excluding_protected_area": 1,
        "forest_land": 1,
        "forest_protected_land": 1,
    },
)
def harvest_available_forest_land():
    """
    Actual area of Forest available to be harvested.
    """
    return forest_land_fraction_harvested_excluding_protected_area() * float(
        np.maximum(0, forest_land() - forest_protected_land())
    )


@component.add(
    name="Harvested Forest Biomass Land Indicator",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"actual_forest_land_harvested": 1},
)
def harvested_forest_biomass_land_indicator():
    return actual_forest_land_harvested()


@component.add(
    name="Inflow EGMeYA",
    units="Ton/(ha*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grassland_meat_yield": 1},
)
def inflow_egmeya():
    return grassland_meat_yield()


@component.add(
    name="Inflow EGMYA",
    units="Ton/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grassland_milk_yield": 1},
)
def inflow_egmya():
    return grassland_milk_yield()


@component.add(
    name="Inflow EXYA",
    units="Ton/(ha*Year)",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"crop_yield_for_each_category": 1},
)
def inflow_exya():
    return crop_yield_for_each_category()


@component.add(
    name="Inflow FPLCLV1",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"fraction_fplc": 1},
)
def inflow_fplclv1():
    return fraction_fplc()


@component.add(
    name="Inflow FPLCLV2",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_fplclv1": 1},
)
def inflow_fplclv2():
    return outflow_fplclv1()


@component.add(
    name="Inflow FPLCLV3",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_fplclv2": 1},
)
def inflow_fplclv3():
    return outflow_fplclv2()


@component.add(
    name="INIT Agricultural Land",
    units="ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_agricultural_land():
    """
    The area of agriculture land for year 1900.4.4e+009
    """
    return 4400000000.0


@component.add(
    name="INIT Crop Yield",
    units="Ton/(Year*ha)",
    subscripts=["PlantFood"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_crop_yield():
    return xr.DataArray(
        [0.34, 0.97, 4.89, 2.99],
        {"PlantFood": _subscript_dict["PlantFood"]},
        ["PlantFood"],
    )


@component.add(
    name="INIT Forest Land", units="ha", comp_type="Constant", comp_subtype="Normal"
)
def init_forest_land():
    """
    The area of forest land for year 1900. : 4.41e+013 (Felicjan) Calibrated: 5.14e+013 m2, 5.14e+09 ha
    """
    return 4400000000.0


@component.add(
    name="INIT Forest Protected Land",
    units="ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_forest_protected_land():
    """
    Area of forest land indicated as protected in year 1900.
    """
    return 282254


@component.add(
    name="INIT Input Neutral TC in Forest",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_input_neutral_tc_in_forest():
    """
    Reference variable representing technological advancement and its positive impact on forest land fertility in year 1900.
    """
    return 1


@component.add(
    name="INIT Other Land", units="ha", comp_type="Constant", comp_subtype="Normal"
)
def init_other_land():
    """
    The area of other land for year 1900.
    """
    return 4100000000.0


@component.add(
    name="INIT Urban and Industrial Land",
    units="ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_urban_and_industrial_land():
    """
    The area of urban and industrial land for year 1900.
    """
    return 4000000.0


@component.add(
    name="Initial Grassland Meat Yield",
    units="Mkcal/(Year*ha)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_grassland_meat_yield():
    """
    0.007
    """
    return 0.015


@component.add(
    name="Initial Grassland Milk Yield",
    units="Ton/(Year*ha)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_grassland_milk_yield():
    """
    0.2288
    """
    return 0.45


@component.add(
    name="Initial Trend", units="1/Year", comp_type="Constant", comp_subtype="Normal"
)
def initial_trend():
    return 0.01


@component.add(
    name="Input Neutral Forest Technology",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_input_neutral_forest_technology": 1},
    other_deps={
        "_integ_input_neutral_forest_technology": {
            "initial": {"init_input_neutral_tc_in_forest": 1},
            "step": {"input_neutral_technology_change_in_forest": 1},
        }
    },
)
def input_neutral_forest_technology():
    """
    Exogenous variable representing technological advancement and its positive impact on forest land fertility.
    """
    return _integ_input_neutral_forest_technology()


_integ_input_neutral_forest_technology = Integ(
    lambda: input_neutral_technology_change_in_forest(),
    lambda: init_input_neutral_tc_in_forest(),
    "_integ_input_neutral_forest_technology",
)


@component.add(
    name="Input Neutral Technology Change in Forest",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"input_neutral_technology_change_in_forest_factor": 1},
)
def input_neutral_technology_change_in_forest():
    """
    Change in technological advancement related to forest land fertility.
    """
    return input_neutral_technology_change_in_forest_factor()


@component.add(
    name="Input Neutral Technology Change in Forest Factor",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def input_neutral_technology_change_in_forest_factor():
    """
    Factor change of technological advancement related to forest land fertility.
    """
    return 0.001


@component.add(
    name="Intended Conversion Forest to Agriculture",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "desired_agricultural_land_conversion": 1,
        "fraction_of_agricultural_land_conversion_from_forest": 1,
    },
)
def intended_conversion_forest_to_agriculture():
    return (
        desired_agricultural_land_conversion()
        * fraction_of_agricultural_land_conversion_from_forest()
    )


@component.add(
    name="Intended Conversion Other to Agriculture",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "desired_agricultural_land_conversion": 1,
        "fraction_of_agricultural_land_conversion_from_forest": 1,
    },
)
def intended_conversion_other_to_agriculture():
    return desired_agricultural_land_conversion() * (
        1 - fraction_of_agricultural_land_conversion_from_forest()
    )


@component.add(
    name="k C on Yield",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_k_c_on_yield": 1, "time": 1},
)
def k_c_on_yield():
    return 0 + step(__data["time"], sa_k_c_on_yield(), 2020)


@component.add(
    name="k gdp agritech", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def k_gdp_agritech():
    return 0.466


@component.add(
    name="k T on Yield",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_k_t_on_yield": 1, "time": 1},
)
def k_t_on_yield():
    return 0 + step(__data["time"], sa_k_t_on_yield(), 2020)


@component.add(
    name="k urban land",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effect_of_gdp_on_urban_land_requirement_k_variation": 1, "time": 1},
)
def k_urban_land():
    return 1 + step(
        __data["time"], effect_of_gdp_on_urban_land_requirement_k_variation() - 1, 2020
    )


@component.add(
    name="L C on Yield",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_l_c_on_yield": 1, "time": 1},
)
def l_c_on_yield():
    return 2 + step(__data["time"], sa_l_c_on_yield() - 2, 2020)


@component.add(
    name="L gdp agritech", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def l_gdp_agritech():
    return 1.45


@component.add(
    name="L T on Yield",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_l_t_on_yield": 1, "time": 1},
)
def l_t_on_yield():
    return 2 + step(__data["time"], sa_l_t_on_yield() - 2, 2020)


@component.add(
    name="L urban land",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "egi_var_s": 2,
        "time": 1,
        "se_var_t": 1,
        "effect_of_gdp_on_urban_land_requirement_l_variation": 1,
    },
)
def l_urban_land():
    return egi_var_s() + step(
        __data["time"],
        effect_of_gdp_on_urban_land_requirement_l_variation() - egi_var_s(),
        2020 + se_var_t(),
    )


@component.add(
    name="L Var T", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def l_var_t():
    return 0


@component.add(
    name="Land Allocated for Animal Calories",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grassland_allocated_for_food_production": 1},
)
def land_allocated_for_animal_calories():
    """
    Calculated historical data and projection for land for animal food according to FAO. Source of historical data: http://faostat.fao.org
    """
    return grassland_allocated_for_food_production()


@component.add(
    name="Land Allocated for Energy Crops",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"arable_land_allocated_for_energy_crops": 1},
)
def land_allocated_for_energy_crops():
    """
    Land area dedicated to energy crops production.
    """
    return arable_land_allocated_for_energy_crops()


@component.add(
    name="Land Allocated for Food Crops",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"arable_land_allocated_for_crops": 1, "permanent_crops": 1},
)
def land_allocated_for_food_crops():
    """
    Land area dedicated to crops production decreased by the area dedicated to energy crops production.
    """
    return arable_land_allocated_for_crops() + permanent_crops()


@component.add(
    name="Land Conversion Delay Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def land_conversion_delay_time():
    """
    Parameter indicating time delay required to change land from vegetal to animal food production land.
    """
    return 5


@component.add(
    name="Livestock Production Indicator",
    units="Million tDM/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "production_rate_of_animal_food": 4,
        "moisture_content": 4,
        "tdm_to_million_tdm": 1,
    },
)
def livestock_production_indicator():
    return (
        float(production_rate_of_animal_food().loc["CropMeat"])
        * (1 - float(moisture_content().loc["CropMeat"]))
        + float(production_rate_of_animal_food().loc["PasMeat"])
        * (1 - float(moisture_content().loc["PasMeat"]))
        + float(production_rate_of_animal_food().loc["Dairy"])
        * (1 - float(moisture_content().loc["Dairy"]))
        + float(production_rate_of_animal_food().loc["Eggs"])
        * (1 - float(moisture_content().loc["Eggs"]))
    ) * tdm_to_million_tdm()


@component.add(
    name="m Effect of C on Yield",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_m_effect_of_c_on_yield": 1, "time": 1},
)
def m_effect_of_c_on_yield():
    return 0 + step(__data["time"], sa_m_effect_of_c_on_yield(), 2020)


@component.add(
    name="m Effect of T on Yield",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_m_effect_of_t_on_yield": 1, "time": 1},
)
def m_effect_of_t_on_yield():
    return 0 + step(__data["time"], sa_m_effect_of_t_on_yield(), 2020)


@component.add(
    name="Max Effect of CO2 Concentration on Forest Land Fertility",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_effect_of_co2_concentration_on_forest_land_fertility():
    """
    Max impact of carbon concentration on forest land fertility.
    """
    return 1


@component.add(
    name="Max Forest Protected Land",
    units="ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_forest_protected_land():
    """
    Maximum area of forest land that can become protected.: 3.5e+009
    """
    return 500000000.0


@component.add(
    name="Max Impact of Biodiversity on Forest Land Fertility",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_impact_of_biodiversity_on_forest_land_fertility():
    """
    Max impact of mean species abundance on forest land fertility.
    """
    return 1


@component.add(
    name="Meadows and Pastures Percentage of Agriculture Land",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def meadows_and_pastures_percentage_of_agriculture_land():
    """
    Percentage of agricultural land constituting the meadows and pastures land.
    """
    return 0.689


@component.add(
    name="Meat to Eggs Multiplier",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def meat_to_eggs_multiplier():
    """
    Calibrated. Within the range of historical values, close to the histprical average.
    """
    return 0.29


@component.add(
    name="Meat to Milk Multiplier",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def meat_to_milk_multiplier():
    """
    Tonnes of milk / tonnes of bovine meat. For now, based globiom 2000 value
    """
    return 30


@component.add(
    name="Min Effect of CO2 Concentration on Forest Land Fertility",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def min_effect_of_co2_concentration_on_forest_land_fertility():
    """
    Min impact of carbon concentration on forest land fertility.
    """
    return 2


@component.add(
    name="Min Impact of Biodiversity on Forest Land Fertility",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def min_impact_of_biodiversity_on_forest_land_fertility():
    """
    Min impact of mean species abundance on forest land fertility.
    """
    return 0.1


@component.add(
    name="Moisture Content",
    units="tDM/Ton",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def moisture_content():
    """
    Data from Food and Animal moisture content https://lca-net.com/files/LCAfood2014-LCAofGlobalFoodConsumption.pdf CropMeat = average (poultry and pork) PasMeat = average ( Cattle beef and other meats) Dairy = Animal raw milk Vegetable and fruits = vegetable and fuits Other plant products = average (oil crops, sugar crops and crops other) https://www.researchgate.net/publication/325594668_Postharvest_Losses_in_Ethiopia_and _Opportunities_for_Reduction_A_Review/figures?lo=1 Crops = average of all crops in Table 2. Pulses = average pulses and lentil and pea from Table 2
    """
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[["CropMeat"]] = (0.7 + 0.55) / 2
    value.loc[["Eggs"]] = 0.26
    value.loc[["PasMeat"]] = (0.53 + 0.57) / 2
    value.loc[["Dairy"]] = 0.88
    value.loc[["Pulses"]] = (0.15 + 0.14) / 2
    value.loc[["Grains"]] = (
        0.15 + 0.115 + 0.13 + 0.135 + 0.16 + 0.135 + 0.135 + 0.12
    ) / 8
    value.loc[["VegFruits"]] = 0.82
    value.loc[["OtherCrops"]] = (0.79 + 0.09 + 0.75) / 3
    return value


@component.add(name="MY S", units="Ton/ha", comp_type="Constant", comp_subtype="Normal")
def my_s():
    return 0.1877


@component.add(
    name="MY Var S",
    units="Ton/ha",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_my_var_s": 1},
    other_deps={
        "_smooth_my_var_s": {
            "initial": {"my_s": 1, "time": 1},
            "step": {"my_s": 1, "time": 1},
        }
    },
)
def my_var_s():
    return 0.1877 + _smooth_my_var_s()


_smooth_my_var_s = Smooth(
    lambda: step(__data["time"], my_s() - 0.1877, 2020),
    lambda: 1,
    lambda: step(__data["time"], my_s() - 0.1877, 2020),
    lambda: 1,
    "_smooth_my_var_s",
)


@component.add(
    name="Nominal Energy Agriculture Land Productivity",
    units="Biomass ton/(ha*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nominal_energy_agriculture_land_productivity_variation": 1, "time": 1},
)
def nominal_energy_agriculture_land_productivity():
    """
    Reference annual amount of energy crops biomass yield from unit energy crops land area.
    """
    return 12.5 + step(
        __data["time"],
        nominal_energy_agriculture_land_productivity_variation() - 12.5,
        2020,
    )


@component.add(
    name="Nominal Energy Agriculture Land Productivity Variation",
    units="Biomass ton/(ha*Year)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def nominal_energy_agriculture_land_productivity_variation():
    return 12.5


@component.add(
    name="Nominal Energy Forest Land Productivity",
    units="Biomass ton/(Year*ha)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def nominal_energy_forest_land_productivity():
    """
    Reference annual amount of forest biomass production from unit forest land area.
    """
    return 50


@component.add(
    name="Nonenergy Crops Production Indicator",
    units="Million tDM/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "production_rate_of_crops": 4,
        "moisture_content": 4,
        "tdm_to_million_tdm": 1,
    },
)
def nonenergy_crops_production_indicator():
    return (
        float(production_rate_of_crops().loc["Pulses"])
        * (1 - float(moisture_content().loc["Pulses"]))
        + float(production_rate_of_crops().loc["Grains"])
        * (1 - float(moisture_content().loc["Grains"]))
        + float(production_rate_of_crops().loc["VegFruits"])
        * (1 - float(moisture_content().loc["VegFruits"]))
        + float(production_rate_of_crops().loc["OtherCrops"])
        * (1 - float(moisture_content().loc["OtherCrops"]))
    ) * tdm_to_million_tdm()


@component.add(
    name="Normal Forest Land Fertility",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_forest_land_fertility():
    """
    Reference value of forest land fertility in year 1900.
    """
    return 1


@component.add(
    name="Normal Urban and Industrial Land per Capita",
    units="ha/Person",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_urban_and_industrial_land_per_capita():
    """
    Normal required Urban and Industrial Land per capita assuming equal land distribution between the total population.
    """
    return 0.02


@component.add(
    name="Other crops supply in Mkcal",
    units="Mkcal/Year",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def other_crops_supply_in_mkcal():
    return np.interp(
        time(),
        [
            1961.0,
            1962.0,
            1963.0,
            1964.0,
            1965.0,
            1966.0,
            1967.0,
            1968.0,
            1969.0,
            1970.0,
            1971.0,
            1972.0,
            1973.0,
            1974.0,
            1975.0,
            1976.0,
            1977.0,
            1978.0,
            1979.0,
            1980.0,
            1981.0,
            1982.0,
            1983.0,
            1984.0,
            1985.0,
            1986.0,
            1987.0,
            1988.0,
            1989.0,
            1990.0,
            1991.0,
            1992.0,
            1993.0,
            1994.0,
            1995.0,
            1996.0,
            1997.0,
            1998.0,
            1999.0,
            2000.0,
            2001.0,
            2002.0,
            2003.0,
            2004.0,
            2005.0,
            2006.0,
            2007.0,
            2008.0,
            2009.0,
            2010.0,
            2011.0,
            2012.0,
            2013.0,
        ],
        [
            3.51924e08,
            3.72430e08,
            3.81990e08,
            4.01483e08,
            4.18100e08,
            4.35388e08,
            4.49529e08,
            4.61531e08,
            4.79091e08,
            5.03815e08,
            5.18190e08,
            5.27180e08,
            5.46183e08,
            5.58201e08,
            5.62792e08,
            5.88330e08,
            6.09745e08,
            6.39437e08,
            6.61950e08,
            6.83474e08,
            7.03933e08,
            7.29974e08,
            7.36189e08,
            7.65215e08,
            7.88066e08,
            8.13465e08,
            8.48841e08,
            8.75718e08,
            8.93310e08,
            9.14523e08,
            9.15743e08,
            9.28207e08,
            9.38241e08,
            9.66534e08,
            9.95063e08,
            1.02382e09,
            1.05926e09,
            1.07329e09,
            1.07620e09,
            1.11249e09,
            1.13804e09,
            1.16394e09,
            1.19023e09,
            1.21458e09,
            1.24409e09,
            1.27171e09,
            1.30225e09,
            1.32835e09,
            1.34729e09,
            1.36892e09,
            1.40103e09,
            1.42838e09,
            1.42318e09,
        ],
    )


@component.add(
    name="Other crops tonnes",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"other_crops_supply_in_mkcal": 1, "caloric_value_of_food": 1},
)
def other_crops_tonnes():
    return other_crops_supply_in_mkcal() / float(
        caloric_value_of_food().loc["OtherCrops"]
    )


@component.add(
    name="Other Land",
    units="ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_other_land": 1},
    other_deps={
        "_integ_other_land": {
            "initial": {"init_other_land": 1},
            "step": {
                "agricultural_land_erosion_rate": 1,
                "agricultural_land_development_rate": 1,
                "forestation_from_other_land": 1,
            },
        }
    },
)
def other_land():
    """
    Land not classified as Agricultural area, Forest area or Urban and Industrial Land.
    """
    return _integ_other_land()


_integ_other_land = Integ(
    lambda: agricultural_land_erosion_rate()
    - agricultural_land_development_rate()
    - forestation_from_other_land(),
    lambda: init_other_land(),
    "_integ_other_land",
)


@component.add(
    name="Other Land Indicator",
    units="Million ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"other_land": 1, "ha_into_million_ha": 1},
)
def other_land_indicator():
    return other_land() * ha_into_million_ha()


@component.add(
    name="Other Protected Land", units="ha", comp_type="Constant", comp_subtype="Normal"
)
def other_protected_land():
    """
    Area of Other Land not transformable into other kind of lands.
    """
    return 500000000.0


@component.add(
    name="Other to Forest Land Allocation Time",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"other_to_forest_land_allocation_time_variation": 1, "time": 1},
)
def other_to_forest_land_allocation_time():
    """
    Average time which natural transformation of Other to Forest Land would take.
    """
    return 40 + step(
        __data["time"], other_to_forest_land_allocation_time_variation() - 40, 2020
    )


@component.add(
    name="Other to Forest Land Allocation Time Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def other_to_forest_land_allocation_time_variation():
    """
    Average time which natural transformation of Other to Forest Land would take.
    """
    return 40


@component.add(
    name="Other uses multiplier for food",
    units="Dmnl",
    subscripts=["PlantFood"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def other_uses_multiplier_for_food():
    """
    This parameter indicates how much of produced crop is used for puposes other than food and feed (seed, loss, other uses) with respect to FOOD. It is estimated based on the FAO food balance sheets, the data for 1961-1985. See FoodBalanceSheets.xlsx/AvgPercentages
    """
    return xr.DataArray(
        [0.19, 0.24, 0.16, 0.08],
        {"PlantFood": _subscript_dict["PlantFood"]},
        ["PlantFood"],
    )


@component.add(
    name="Outflow EGMeYA",
    units="Ton/(ha*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"expected_grassland_meat_yield_accumulative": 1},
)
def outflow_egmeya():
    return expected_grassland_meat_yield_accumulative() / 1


@component.add(
    name="Outflow EGMYA",
    units="Ton/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"expected_grassland_milk_yield_accumulative": 1},
)
def outflow_egmya():
    return expected_grassland_milk_yield_accumulative() / 1


@component.add(
    name="Outflow EXYA",
    units="Ton/(ha*Year)",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"expected_crop_yield_accumulative": 1},
)
def outflow_exya():
    return expected_crop_yield_accumulative() / 1


@component.add(
    name="Outflow FPLCLV1",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"forest_protected_land_change_lv1": 1, "delay_time_fplclv": 1},
)
def outflow_fplclv1():
    return forest_protected_land_change_lv1() / delay_time_fplclv()


@component.add(
    name="Outflow FPLCLV2",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"forest_protected_land_change_lv2": 1, "delay_time_fplclv": 1},
)
def outflow_fplclv2():
    return forest_protected_land_change_lv2() / delay_time_fplclv()


@component.add(
    name="Outflow FPLCLV3",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"forest_protected_land_change_lv3": 1, "delay_time_fplclv": 1},
)
def outflow_fplclv3():
    return forest_protected_land_change_lv3() / delay_time_fplclv()


@component.add(
    name="p Effect of C on Yield",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_p_effect_of_c_on_yield": 1, "time": 1},
)
def p_effect_of_c_on_yield():
    return 1.5 + step(__data["time"], sa_p_effect_of_c_on_yield() - 1.5, 2020)


@component.add(
    name="p Effect of T on Yield",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_p_effect_of_t_on_yield": 1, "time": 1},
)
def p_effect_of_t_on_yield():
    return 1.5 + step(__data["time"], sa_p_effect_of_t_on_yield() - 1.5, 2020)


@component.add(
    name="Pasture Land Indicator",
    units="Million ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"permanent_meadows_and_pastures": 1, "ha_into_million_ha": 1},
)
def pasture_land_indicator():
    return permanent_meadows_and_pastures() * ha_into_million_ha()


@component.add(
    name="Permanent crops",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agricultural_land": 1,
        "permanent_crops_percentage_of_agriculture_land": 1,
    },
)
def permanent_crops():
    """
    Area of permanent crops land.
    """
    return agricultural_land() * permanent_crops_percentage_of_agriculture_land()


@component.add(
    name="Permanent Crops Percentage of Agriculture Land",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def permanent_crops_percentage_of_agriculture_land():
    """
    Percentage of agricultural land constituting the permanent crops land.
    """
    return 0.05


@component.add(
    name="Permanent meadows and pastures",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agricultural_land": 1,
        "meadows_and_pastures_percentage_of_agriculture_land": 1,
    },
)
def permanent_meadows_and_pastures():
    """
    Area of permanent meadows and pastures land.
    """
    return agricultural_land() * meadows_and_pastures_percentage_of_agriculture_land()


@component.add(
    name="Population Data",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def population_data():
    return np.interp(
        time(),
        [
            1900.0,
            1910.0,
            1920.0,
            1930.0,
            1940.0,
            1950.0,
            1960.0,
            1970.0,
            1980.0,
            1990.0,
            2000.0,
            2010.0,
            2015.0,
            2016.0,
            2017.0,
            2018.0,
            2019.0,
            2020.0,
            2021.0,
            2022.0,
            2023.0,
            2024.0,
            2025.0,
            2026.0,
            2027.0,
            2028.0,
            2029.0,
            2030.0,
            2031.0,
            2032.0,
            2033.0,
            2034.0,
            2035.0,
            2036.0,
            2037.0,
            2038.0,
            2039.0,
            2040.0,
            2041.0,
            2042.0,
            2043.0,
            2044.0,
            2045.0,
            2046.0,
            2047.0,
            2048.0,
            2049.0,
            2050.0,
            2051.0,
            2052.0,
            2053.0,
            2054.0,
            2055.0,
            2056.0,
            2057.0,
            2058.0,
            2059.0,
            2060.0,
            2061.0,
            2062.0,
            2063.0,
            2064.0,
            2065.0,
            2066.0,
            2067.0,
            2068.0,
            2069.0,
            2070.0,
            2071.0,
            2072.0,
            2073.0,
            2074.0,
            2075.0,
            2076.0,
            2077.0,
            2078.0,
            2079.0,
            2080.0,
            2081.0,
            2082.0,
            2083.0,
            2084.0,
            2085.0,
            2086.0,
            2087.0,
            2088.0,
            2089.0,
            2090.0,
            2091.0,
            2092.0,
            2093.0,
            2094.0,
            2095.0,
            2096.0,
            2097.0,
            2098.0,
            2099.0,
        ],
        [
            1.60000e09,
            1.71092e09,
            1.94955e09,
            2.10000e09,
            2.30000e09,
            2.55000e09,
            3.00000e09,
            3.70000e09,
            4.50000e09,
            5.30000e09,
            6.24176e09,
            7.12458e09,
            7.56345e09,
            7.64832e09,
            7.73203e09,
            7.81452e09,
            7.89638e09,
            7.97785e09,
            8.05888e09,
            8.13938e09,
            8.21929e09,
            8.29854e09,
            8.37707e09,
            8.45482e09,
            8.53172e09,
            8.60768e09,
            8.68265e09,
            8.75657e09,
            8.82939e09,
            8.90108e09,
            8.97158e09,
            9.04086e09,
            9.10887e09,
            9.17557e09,
            9.24087e09,
            9.30473e09,
            9.36709e09,
            9.42791e09,
            9.48716e09,
            9.54481e09,
            9.60083e09,
            9.65519e09,
            9.70786e09,
            9.75887e09,
            9.80831e09,
            9.85617e09,
            9.90239e09,
            9.94695e09,
            9.98980e09,
            1.00309e10,
            1.00702e10,
            1.01076e10,
            1.01430e10,
            1.01764e10,
            1.02079e10,
            1.02373e10,
            1.02646e10,
            1.02900e10,
            1.03133e10,
            1.03346e10,
            1.03539e10,
            1.03712e10,
            1.03866e10,
            1.04000e10,
            1.04116e10,
            1.04213e10,
            1.04291e10,
            1.04351e10,
            1.04393e10,
            1.04415e10,
            1.04414e10,
            1.04392e10,
            1.04349e10,
            1.04285e10,
            1.04201e10,
            1.04097e10,
            1.03974e10,
            1.03833e10,
            1.03673e10,
            1.03497e10,
            1.03303e10,
            1.03093e10,
            1.02868e10,
            1.02627e10,
            1.02371e10,
            1.02102e10,
            1.01818e10,
            1.01522e10,
            1.01213e10,
            1.00891e10,
            1.00558e10,
            1.00213e10,
            9.98575e09,
            9.94913e09,
            9.91151e09,
            9.87291e09,
            9.83339e09,
        ],
    )


@component.add(
    name="Potential Biomass Production",
    units="Biomass ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "forest_land_yield": 1,
        "harvest_available_forest_land": 1,
        "biomass_production_processing_loss": 1,
    },
)
def potential_biomass_production():
    """
    Potential Biomass Production for given area to be harvested, actual yield from ha and excluding forest biomass production processing losses.
    """
    return (
        forest_land_yield()
        * harvest_available_forest_land()
        * (1 - biomass_production_processing_loss())
    )


@component.add(
    name="Production rate of animal food",
    units="Ton/Year",
    subscripts=["MapAltProteins"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "food_demand_in_tonnes": 1,
        "feed_availability": 1,
        "unit_feed_used_for_meat_production": 1,
        "production_rate_of_animal_food": 1,
        "meat_to_eggs_multiplier": 1,
        "production_rate_of_pasture_based_food": 2,
    },
)
def production_rate_of_animal_food():
    value = xr.DataArray(
        np.nan,
        {"MapAltProteins": _subscript_dict["MapAltProteins"]},
        ["MapAltProteins"],
    )
    value.loc[["CropMeat"]] = float(
        np.minimum(
            float(food_demand_in_tonnes().loc["CropMeat"]),
            sum(
                feed_availability().rename({"PlantFood": "PlantFood!"})
                / unit_feed_used_for_meat_production(),
                dim=["PlantFood!"],
            ),
        )
    )
    value.loc[["Eggs"]] = (
        float(production_rate_of_animal_food().loc["CropMeat"])
        * meat_to_eggs_multiplier()
    )
    value.loc[["PasMeat"]] = float(
        production_rate_of_pasture_based_food().loc["PasMeat"]
    )
    value.loc[["Dairy"]] = float(production_rate_of_pasture_based_food().loc["Dairy"])
    return value


@component.add(
    name="Production rate of crops",
    units="Ton/Year",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "desired_crop_production": 1,
        "crop_yield_for_each_category": 1,
        "area_harvested": 1,
    },
)
def production_rate_of_crops():
    return np.minimum(
        desired_crop_production(), area_harvested() * crop_yield_for_each_category()
    )


@component.add(
    name="Production rate of pasture based food",
    units="Ton/Year",
    subscripts=["MapAltProteins"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "grassland_allocated_for_food_production": 2,
        "grassland_allocation_fraction": 2,
        "grassland_meat_yield": 1,
        "food_demand_in_tonnes": 2,
        "grassland_milk_yield": 1,
    },
)
def production_rate_of_pasture_based_food():
    """
    Total animal food production due to animal food land availability and animal food land yield.
    """
    value = xr.DataArray(
        np.nan,
        {"MapAltProteins": _subscript_dict["MapAltProteins"]},
        ["MapAltProteins"],
    )
    value.loc[["PasMeat"]] = float(
        np.minimum(
            grassland_allocated_for_food_production()
            * float(grassland_allocation_fraction().loc["PasMeat"])
            * grassland_meat_yield(),
            float(food_demand_in_tonnes().loc["PasMeat"]),
        )
    )
    value.loc[["Dairy"]] = float(
        np.minimum(
            grassland_allocated_for_food_production()
            * float(grassland_allocation_fraction().loc["Dairy"])
            * grassland_milk_yield(),
            float(food_demand_in_tonnes().loc["Dairy"]),
        )
    )
    return value


@component.add(
    name="Reference crop yield 2016",
    units="Ton/(Year*ha)",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_crop_yield_2016():
    """
    2016 values for each food category, based on FAO data
    """
    return xr.DataArray(
        [1.28, 0.65, 6.42, 0.8, 0.99, 3.97, 15.13, 9.03],
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )


@component.add(
    name="Reference Input Neutral TC in Agriculture",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"tc_var_s": 1, "_smooth_reference_input_neutral_tc_in_agriculture": 1},
    other_deps={
        "_smooth_reference_input_neutral_tc_in_agriculture": {
            "initial": {
                "reference_input_neutral_tc_in_agriculture_variation": 1,
                "tc_var_s": 1,
                "l_var_t": 1,
                "time": 1,
            },
            "step": {
                "reference_input_neutral_tc_in_agriculture_variation": 1,
                "tc_var_s": 1,
                "l_var_t": 1,
                "time": 1,
                "ssp_land_use_change_variation_time": 1,
            },
        }
    },
)
def reference_input_neutral_tc_in_agriculture():
    """
    Reference variable representing technological advancement and its positive impact on agricultural land fertility in year 1900. Equal to 1 in Felicjan's formulation. ---- In Brians's GDP dependent in formulation, it is 0.3
    """
    return tc_var_s() + _smooth_reference_input_neutral_tc_in_agriculture()


_smooth_reference_input_neutral_tc_in_agriculture = Smooth(
    lambda: step(
        __data["time"],
        reference_input_neutral_tc_in_agriculture_variation() - tc_var_s(),
        2020 + l_var_t(),
    ),
    lambda: ssp_land_use_change_variation_time(),
    lambda: step(
        __data["time"],
        reference_input_neutral_tc_in_agriculture_variation() - tc_var_s(),
        2020 + l_var_t(),
    ),
    lambda: 1,
    "_smooth_reference_input_neutral_tc_in_agriculture",
)


@component.add(
    name="Reference Input Neutral TC in Agriculture Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_input_neutral_tc_in_agriculture_variation():
    return 0.3


@component.add(
    name="Reference meat yield",
    units="Ton/ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_meat_yield():
    """
    MY Var S+SMOOTH(STEP(Reference meat yield Variation-MY Var S, 2020+L Var T),SSP Land Use Change Variation Time)
    """
    return 0.1877


@component.add(
    name="Reference meat yield Variation",
    units="Ton/ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_meat_yield_variation():
    return 0.1877


@component.add(
    name="SA Feed share of crop types",
    units="Dmnl",
    subscripts=["PlantFood"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_feed_share_of_crop_types():
    return xr.DataArray(
        [1.0, 1.0, 1.0, 1.0], {"PlantFood": _subscript_dict["PlantFood"]}, ["PlantFood"]
    )


@component.add(
    name="SA k C on Yield", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def sa_k_c_on_yield():
    return 0


@component.add(
    name="SA k T on Yield", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def sa_k_t_on_yield():
    return 0


@component.add(
    name="SA L C on Yield", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def sa_l_c_on_yield():
    return 2


@component.add(
    name="SA L T on Yield", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def sa_l_t_on_yield():
    return 2


@component.add(
    name="SA m Effect of C on Yield",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_m_effect_of_c_on_yield():
    return 0


@component.add(
    name="SA m Effect of T on Yield",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_m_effect_of_t_on_yield():
    return 0


@component.add(
    name="SA multiplier for caloric value",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_multiplier_for_caloric_value():
    return 1


@component.add(
    name="SA p Effect of C on Yield",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_p_effect_of_c_on_yield():
    return 1.5


@component.add(
    name="SA p Effect of T on Yield",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_p_effect_of_t_on_yield():
    return 1.5


@component.add(
    name="SA u Effect of C on Yield",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_u_effect_of_c_on_yield():
    return 1


@component.add(
    name="SA u Effect of T on Yield",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_u_effect_of_t_on_yield():
    return 1


@component.add(
    name="SA Waste fraction",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_waste_fraction():
    return xr.DataArray(
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )


@component.add(
    name="SA x0 C on Yield", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def sa_x0_c_on_yield():
    return 5


@component.add(
    name="SA x0 T on Yield",
    units="DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_x0_t_on_yield():
    return 2


@component.add(
    name="SCENARIO Half Measures",
    units="Dmnl",
    limits=(0.0, 1.0, 1.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def scenario_half_measures():
    """
    WWF Scenario variable. Further development required.
    """
    return 0


@component.add(
    name="SCENARIO Target",
    units="Dmnl",
    limits=(0.0, 1.0, 1.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def scenario_target():
    """
    WWF Scenario variable. Further development required.
    """
    return 0


@component.add(
    name="SCENARIO Target Delayed",
    units="Dmnl",
    limits=(0.0, 1.0, 1.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def scenario_target_delayed():
    """
    WWF Scenario variable. Further development required.
    """
    return 0


@component.add(
    name="Sqr m to ha", units="ha/(m*m)", comp_type="Constant", comp_subtype="Normal"
)
def sqr_m_to_ha():
    """
    Coefficient to convert sqr meters into ha.
    """
    return 0.0001


@component.add(
    name="Start Year of Waste Switch",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def start_year_of_waste_switch():
    return 2020


@component.add(
    name="Supply chain waste variation",
    units="Dmnl",
    subscripts=["SupplyChain"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def supply_chain_waste_variation():
    return xr.DataArray(
        [1.0, 1.0, 1.0, 1.0, 1.0],
        {"SupplyChain": _subscript_dict["SupplyChain"]},
        ["SupplyChain"],
    )


@component.add(
    name="Table for ETAY",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_table_for_etay"},
)
def table_for_etay(x, final_subs=None):
    """
    Table for Effect of Trees Aging on Yield.
    """
    return _hardcodedlookup_table_for_etay(x, final_subs)


_hardcodedlookup_table_for_etay = HardcodedLookups(
    [0.0, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    [1.0, 1.0, 0.98, 0.9, 0.7, 0.4, 0.15, 0.001],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_for_etay",
)


@component.add(
    name="Table for ETMY",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_table_for_etmy"},
)
def table_for_etmy(x, final_subs=None):
    """
    Table for Effect of Trees Maturing on Yield.
    """
    return _hardcodedlookup_table_for_etmy(x, final_subs)


_hardcodedlookup_table_for_etmy = HardcodedLookups(
    [0.0, 0.1, 0.2, 0.3, 0.4, 1.0],
    [0.15, 0.45, 0.75, 0.95, 1.0, 1.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_for_etmy",
)


@component.add(
    name="Target",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"scenario_target": 2, "time": 1, "target_scenario_ramp_change": 1},
)
def target():
    """
    WWF Scenario variable. Further development required.
    """
    return (1 - scenario_target()) * 1 + scenario_target() * (
        1 + ramp(__data["time"], target_scenario_ramp_change(), 2010, 2020)
    )


@component.add(
    name="Target Deforestation Time Factor",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"scenario_target": 1, "time": 1},
)
def target_deforestation_time_factor():
    """
    WWF Scenario variable. Further development required.
    """
    return scenario_target() * ramp(__data["time"], 100, 2019, 2020)


@component.add(
    name="Target Delayed",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "scenario_target_delayed": 2,
        "time": 1,
        "target_delayed_scenario_ramp_change": 1,
    },
)
def target_delayed():
    """
    WWF Scenario variable. Further development required.
    """
    return (1 - scenario_target_delayed()) * 1 + scenario_target_delayed() * (
        1 + ramp(__data["time"], target_delayed_scenario_ramp_change(), 2020, 2030)
    )


@component.add(
    name="Target Delayed Deforestation Time Factor",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"scenario_target_delayed": 1, "time": 1},
)
def target_delayed_deforestation_time_factor():
    """
    WWF Scenario variable. Further development required.
    """
    return scenario_target_delayed() * ramp(__data["time"], 100, 2025, 2030)


@component.add(
    name="Target Delayed Scenario Ramp Change",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def target_delayed_scenario_ramp_change():
    """
    WWF Scenario variable. Further development required.
    """
    return -0.09


@component.add(
    name="Target Scenario Ramp Change",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def target_scenario_ramp_change():
    """
    WWF Scenario variable. Further development required.
    """
    return -0.0673


@component.add(name="TC S", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def tc_s():
    return 0.3


@component.add(
    name="TC Var S",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_tc_var_s": 1},
    other_deps={
        "_smooth_tc_var_s": {
            "initial": {"tc_s": 1, "time": 1},
            "step": {"tc_s": 1, "time": 1},
        }
    },
)
def tc_var_s():
    return 0.3 + _smooth_tc_var_s()


_smooth_tc_var_s = Smooth(
    lambda: step(__data["time"], tc_s() - 0.3, 2020),
    lambda: 1,
    lambda: step(__data["time"], tc_s() - 0.3, 2020),
    lambda: 1,
    "_smooth_tc_var_s",
)


@component.add(
    name="tDM to Million tDM",
    units="Million tDM/tDM",
    comp_type="Constant",
    comp_subtype="Normal",
)
def tdm_to_million_tdm():
    return 1 / 1000000.0


@component.add(
    name="Time to Adjust Forest Protected Land",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_adjust_forest_protected_land():
    """
    Average time required to establish land protection.
    """
    return 2


@component.add(
    name="Ton to Million ton",
    units="Million ton/Ton",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ton_to_million_ton():
    return 1 / 1000000.0


@component.add(
    name="Total Agricultural and Land Use Emissions",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_co2_emissions_from_land_use": 1,
        "total_co2_emissions_from_agriculture": 1,
    },
)
def total_agricultural_and_land_use_emissions():
    return total_co2_emissions_from_land_use() + total_co2_emissions_from_agriculture()


@component.add(
    name="Total Agricultural Land Demand",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cropland_needed": 1, "total_grassland_needed": 1},
)
def total_agricultural_land_demand():
    return cropland_needed() + total_grassland_needed()


@component.add(
    name="Total C emissions from the agriculture",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_emissions_from_agriculture": 1, "co2_to_c": 1},
)
def total_c_emissions_from_the_agriculture():
    return total_co2_emissions_from_agriculture() / co2_to_c()


@component.add(
    name="Total CO2 Emissions from Agriculture",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_emission_rate_of_the_agriculture_sector": 1},
)
def total_co2_emissions_from_agriculture():
    return sum(
        co2_emission_rate_of_the_agriculture_sector().rename(
            {"FoodCategories": "FoodCategories!"}
        ),
        dim=["FoodCategories!"],
    )


@component.add(
    name="Total Crops Biomass Demand",
    units="Biomass ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_demand": 1,
        "market_share_biomass_crops": 1,
        "biomass_conversion_efficiency": 1,
    },
)
def total_crops_biomass_demand():
    """
    Total demand for energy crops accounting for biomass energy market share and reference technology development.
    """
    return (
        energy_demand() * market_share_biomass_crops() / biomass_conversion_efficiency()
    )


@component.add(
    name="Total Daily Calorie Supply per Capita",
    units="kcal/Person/Day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "animal_food_supply_kcal_capita_day": 1,
        "vegetal_food_supply_kcal_capita_day": 1,
    },
)
def total_daily_calorie_supply_per_capita():
    """
    Total average amount of food measured in calories available for each person per day. Source of projection data: GLOBIOM model, IIASA.
    """
    return animal_food_supply_kcal_capita_day() + vegetal_food_supply_kcal_capita_day()


@component.add(
    name="Total Demand for Arable Land",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"arable_land_needed_for_energy_crops": 1, "arable_land_needed": 1},
)
def total_demand_for_arable_land():
    return arable_land_needed_for_energy_crops() + sum(
        arable_land_needed().rename({"PlantFood": "PlantFood!"}), dim=["PlantFood!"]
    )


@component.add(
    name="Total food shortage in kcal",
    units="Mkcal/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"food_shortage_in_kcal": 1},
)
def total_food_shortage_in_kcal():
    return sum(
        food_shortage_in_kcal().rename({"FoodCategories": "FoodCategories!"}),
        dim=["FoodCategories!"],
    )


@component.add(
    name="Total Forest Biomass Demand",
    units="Biomass ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "energy_demand": 1,
        "market_share_biomass_forest": 1,
        "biomass_conversion_efficiency": 1,
    },
)
def total_forest_biomass_demand():
    """
    Total demand for forest biomass accounting for forest biomass energy market share and reference technology development.
    """
    return (
        energy_demand()
        * market_share_biomass_forest()
        / biomass_conversion_efficiency()
    )


@component.add(
    name="Total Grassland Needed",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grassland_needed": 2},
)
def total_grassland_needed():
    return float(grassland_needed().loc["PasMeat"]) + float(
        grassland_needed().loc["Dairy"]
    )


@component.add(
    name="Total Land",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agricultural_land": 1,
        "forest_land": 1,
        "other_land": 1,
        "urban_and_industrial_land": 1,
    },
)
def total_land():
    """
    Total considered land.
    """
    return (
        agricultural_land() + forest_land() + other_land() + urban_and_industrial_land()
    )


@component.add(
    name="Total Supply of Animal Calories",
    units="Mkcal/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"food_supply_in_kcal": 1},
)
def total_supply_of_animal_calories():
    return sum(
        food_supply_in_kcal()
        .loc[_subscript_dict["AnimalFood"]]
        .rename({"FoodCategories": "AnimalFood!"}),
        dim=["AnimalFood!"],
    )


@component.add(
    name="Total Supply of Vegetal Calories",
    units="Mkcal/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"food_supply_in_kcal": 1},
)
def total_supply_of_vegetal_calories():
    return sum(
        food_supply_in_kcal()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood!"}),
        dim=["PlantFood!"],
    )


@component.add(
    name="Trend Averaging Time",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "desired_agricultural_land_conversion_trend_averaging_time_variation": 1,
        "time": 1,
    },
)
def trend_averaging_time():
    """
    This parameter represents how many years ahead is taken into account to foresee the land demand for land conversion.
    """
    return 10 + step(
        __data["time"],
        desired_agricultural_land_conversion_trend_averaging_time_variation() - 10,
        2020,
    )


@component.add(
    name="Trend of Land Demand",
    units="1/Year",
    comp_type="Stateful",
    comp_subtype="Trend",
    depends_on={"_trend_trend_of_land_demand": 1},
    other_deps={
        "_trend_trend_of_land_demand": {
            "initial": {
                "initial_trend": 1,
                "total_agricultural_land_demand": 1,
                "trend_averaging_time": 1,
            },
            "step": {"total_agricultural_land_demand": 1, "trend_averaging_time": 1},
        }
    },
)
def trend_of_land_demand():
    return _trend_trend_of_land_demand()


_trend_trend_of_land_demand = Trend(
    lambda: total_agricultural_land_demand(),
    lambda: trend_averaging_time(),
    lambda: initial_trend(),
    "_trend_trend_of_land_demand",
)


@component.add(
    name="u Effect of C on Yield",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_u_effect_of_c_on_yield": 1, "time": 1},
)
def u_effect_of_c_on_yield():
    return 0 + step(__data["time"], sa_u_effect_of_c_on_yield() - 0, 2020)


@component.add(
    name="u Effect of T on Yield",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_u_effect_of_t_on_yield": 1, "time": 1},
)
def u_effect_of_t_on_yield():
    return 0 + step(__data["time"], sa_u_effect_of_t_on_yield() - 0, 2020)


@component.add(
    name="Unit CO2 emissions from food production",
    units="TonC/Ton",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def unit_co2_emissions_from_food_production():
    return xr.DataArray(
        [32.58, 1.32, 1.22, 1.58, 0.23, 0.47, 0.07, 0.3],
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )


@component.add(
    name="Unit feed used for meat production",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def unit_feed_used_for_meat_production():
    return np.interp(
        time(),
        [
            1961.0,
            1965.0,
            1975.0,
            1979.0,
            1984.0,
            1988.0,
            1995.0,
            2000.0,
            2006.0,
            2010.0,
            2015.0,
        ],
        [12.7, 12.41, 11.49, 10.84, 9.76, 8.19, 6.68, 6.2, 5.61, 5.09, 5.0],
    )


@component.add(
    name="Urban and Industrial Land",
    units="ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_urban_and_industrial_land": 1},
    other_deps={
        "_integ_urban_and_industrial_land": {
            "initial": {"init_urban_and_industrial_land": 1},
            "step": {
                "agricultural_land_conversion_rate_to_urban_land": 1,
                "deforestation_to_urban_land": 1,
            },
        }
    },
)
def urban_and_industrial_land():
    """
    Total Urban and Industrial Land.
    """
    return _integ_urban_and_industrial_land()


_integ_urban_and_industrial_land = Integ(
    lambda: agricultural_land_conversion_rate_to_urban_land()
    + deforestation_to_urban_land(),
    lambda: init_urban_and_industrial_land(),
    "_integ_urban_and_industrial_land",
)


@component.add(
    name="Urban and Industrial Land Discrepancy",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "urban_and_industrial_land_required": 1,
        "urban_and_industrial_land": 1,
    },
)
def urban_and_industrial_land_discrepancy():
    return float(
        np.maximum(
            urban_and_industrial_land_required() - urban_and_industrial_land(), 0
        )
    )


@component.add(
    name="Urban and Industrial Land per Capita",
    units="ha/Person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effect_of_gdp_on_urban_land_requirement": 1,
        "normal_urban_and_industrial_land_per_capita": 1,
    },
)
def urban_and_industrial_land_per_capita():
    """
    Actual available area of Urban and Industrial Land per capita assuming equal land distribution between the total population.
    """
    return (
        effect_of_gdp_on_urban_land_requirement()
        * normal_urban_and_industrial_land_per_capita()
    )


@component.add(
    name="Urban and Industrial Land Required",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population": 1, "urban_and_industrial_land_per_capita": 1},
)
def urban_and_industrial_land_required():
    return population() * urban_and_industrial_land_per_capita()


@component.add(
    name="Urban Industrial Land Indicator",
    units="Million ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"urban_and_industrial_land": 1, "ha_into_million_ha": 1},
)
def urban_industrial_land_indicator():
    return urban_and_industrial_land() * ha_into_million_ha()


@component.add(
    name="Variable Smooth Waste Switch Fnc",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "end_year_of_waste_switch": 3,
        "start_year_of_waste_switch": 4,
        "time": 2,
    },
)
def variable_smooth_waste_switch_fnc():
    """
    Logistic Curve
    """
    return if_then_else(
        end_year_of_waste_switch() - start_year_of_waste_switch() > 0,
        lambda: 1
        / (
            1
            + float(
                np.exp(
                    -10
                    / (end_year_of_waste_switch() - start_year_of_waste_switch())
                    * (
                        time()
                        - (start_year_of_waste_switch() + end_year_of_waste_switch())
                        / 2
                    )
                )
            )
        ),
        lambda: step(__data["time"], 1, start_year_of_waste_switch()),
    )


@component.add(
    name="Vegetal Food supply kcal capita day",
    units="kcal/(Person*Day)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_supply_of_vegetal_calories": 1,
        "kcal_to_mkcal": 1,
        "days_in_year": 1,
        "population": 1,
    },
)
def vegetal_food_supply_kcal_capita_day():
    """
    Average amount of vegetal food measured in calories available for each person per day. Source of historical data: http://faostat.fao.org
    """
    return total_supply_of_vegetal_calories() / (
        population() * days_in_year() * kcal_to_mkcal()
    )


@component.add(
    name="Washing Fraction Variation by supply chain and food category",
    units="Dmnl",
    subscripts=["FoodCategories", "SupplyChain"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "supply_chain_waste_variation": 1,
        "waste_fraction_data_by_supply_chain_and_food_category": 1,
    },
)
def washing_fraction_variation_by_supply_chain_and_food_category():
    return (
        supply_chain_waste_variation()
        * waste_fraction_data_by_supply_chain_and_food_category().transpose(
            "SupplyChain", "FoodCategories"
        )
    ).transpose("FoodCategories", "SupplyChain")


@component.add(
    name="Waste fraction",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "waste_scenario_switch": 1,
        "variable_smooth_waste_switch_fnc": 2,
        "waste_fraction_data": 4,
        "waste_fraction_scenarios_by_food_category": 1,
        "waste_fraction_scenarios_by_supply_chain": 1,
    },
)
def waste_fraction():
    """
    0: Scenarios by Food Categories 1: Scenarios by Supply Chain
    """
    return if_then_else(
        waste_scenario_switch() == 0,
        lambda: waste_fraction_data()
        + variable_smooth_waste_switch_fnc()
        * (waste_fraction_scenarios_by_food_category() - waste_fraction_data()),
        lambda: waste_fraction_data()
        + variable_smooth_waste_switch_fnc()
        * (waste_fraction_scenarios_by_supply_chain() - waste_fraction_data()),
    )


@component.add(
    name="Waste fraction Data",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def waste_fraction_data():
    return xr.DataArray(
        [0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.45, 0.2],
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )


@component.add(
    name="Waste fraction Data by supply chain and food category",
    units="Dmnl",
    subscripts=["FoodCategories", "SupplyChain"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def waste_fraction_data_by_supply_chain_and_food_category():
    """
    0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.45, 0.2
    """
    return xr.DataArray(
        [
            [0.04, 0.04, 0.04, 0.04, 0.04],
            [0.04, 0.04, 0.04, 0.04, 0.04],
            [0.04, 0.04, 0.04, 0.04, 0.04],
            [0.04, 0.04, 0.04, 0.04, 0.04],
            [0.04, 0.04, 0.04, 0.04, 0.04],
            [0.06, 0.06, 0.06, 0.06, 0.06],
            [0.09, 0.09, 0.09, 0.09, 0.09],
            [0.04, 0.04, 0.04, 0.04, 0.04],
        ],
        {
            "FoodCategories": _subscript_dict["FoodCategories"],
            "SupplyChain": _subscript_dict["SupplyChain"],
        },
        ["FoodCategories", "SupplyChain"],
    )


@component.add(
    name="Waste Fraction EggsDairy Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def waste_fraction_eggsdairy_variation():
    return 1


@component.add(
    name="Waste Fraction PasMeat CropMeat Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def waste_fraction_pasmeat_cropmeat_variation():
    return 1


@component.add(
    name="Waste Fraction PlantFood Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def waste_fraction_plantfood_variation():
    return 1


@component.add(
    name="Waste Fraction Scenarios by Food Category",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def waste_fraction_scenarios_by_food_category():
    return xr.DataArray(
        [0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.45, 0.2],
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )


@component.add(
    name="Waste Fraction Scenarios by Supply Chain",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"washing_fraction_variation_by_supply_chain_and_food_category": 1},
)
def waste_fraction_scenarios_by_supply_chain():
    """
    0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.45, 0.2
    """
    return sum(
        washing_fraction_variation_by_supply_chain_and_food_category().rename(
            {"SupplyChain": "SupplyChain!"}
        ),
        dim=["SupplyChain!"],
    )


@component.add(
    name="Waste scenario switch",
    units="Dmnl",
    limits=(0.0, 1.0, 1.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def waste_scenario_switch():
    """
    0: by food categories 1: by supply chain
    """
    return 1


@component.add(
    name="x0 C on Yield",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_x0_c_on_yield": 1, "time": 1},
)
def x0_c_on_yield():
    return 5 + step(__data["time"], sa_x0_c_on_yield() - 5, 2020)


@component.add(
    name="x0 gdp agritech", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def x0_gdp_agritech():
    return 0.8


@component.add(
    name="x0 T on Yield",
    units="DegreesC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_x0_t_on_yield": 1, "time": 1},
)
def x0_t_on_yield():
    return 2 + step(__data["time"], sa_x0_t_on_yield() - 2, 2020)


@component.add(
    name="x0 urban land",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "egx_var_s": 2,
        "time": 1,
        "effect_of_gdp_on_urban_land_requirement_x0_variation": 1,
        "se_var_t": 1,
    },
)
def x0_urban_land():
    return egx_var_s() + step(
        __data["time"],
        effect_of_gdp_on_urban_land_requirement_x0_variation() - egx_var_s(),
        2020 + se_var_t(),
    )


@component.add(
    name="Zero Net Deforestation and Forest Degradation Scenarios",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"target": 1, "target_delayed": 1, "half_measures": 1},
)
def zero_net_deforestation_and_forest_degradation_scenarios():
    """
    WWF Scenario variable. Further development required.
    """
    return target() * target_delayed() * half_measures()
