"""
Module sdg_indicators
Translated using PySD version 3.14.3
"""

@component.add(
    name="Achieved Cropland Food Yield per Hectare",
    units="Ton/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"production_rate_of_crops": 1, "area_harvested": 1},
)
def achieved_cropland_food_yield_per_hectare():
    return sum(
        production_rate_of_crops().rename({"PlantFood": "PlantFood!"}),
        dim=["PlantFood!"],
    ) / sum(area_harvested().rename({"PlantFood": "PlantFood!"}), dim=["PlantFood!"])


@component.add(
    name="Achieved Grassland Meat Yield per Hectare",
    units="Ton/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "production_rate_of_animal_food": 1,
        "grassland_allocated_for_food_production": 1,
    },
)
def achieved_grassland_meat_yield_per_hectare():
    return (
        float(production_rate_of_animal_food().loc["PasMeat"])
        / grassland_allocated_for_food_production()
    )


@component.add(
    name="Adolescent Fertility Fraction",
    units="1",
    comp_type="Constant",
    comp_subtype="Normal",
)
def adolescent_fertility_fraction():
    """
    Calibrated with Adolescent fertility rate (births per 1,000 women ages 15-19) between 1960 and 2015 from the World Bank: https://data.worldbank.org/indicator/SP.ADO.TFRT
    """
    return 0.07


@component.add(
    name="Adolescent Fertility Rate",
    units="Person/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_fertility": 1,
        "per_1000_women": 1,
        "adolescent_fertility_fraction": 1,
        "adolescent_reproductive_lifetime": 1,
    },
)
def adolescent_fertility_rate():
    return (
        total_fertility()
        * per_1000_women()
        * adolescent_fertility_fraction()
        / adolescent_reproductive_lifetime()
    )


@component.add(
    name="Adolescent Reproductive Lifetime",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def adolescent_reproductive_lifetime():
    return 5


@component.add(
    name="AFOLU CO2 Emissions per Capita",
    units="TonCO2/(Person*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agriculture_co2_emissions_per_capita": 1,
        "land_use_co2_emissions_per_capita": 1,
    },
)
def afolu_co2_emissions_per_capita():
    return agriculture_co2_emissions_per_capita() + land_use_co2_emissions_per_capita()


@component.add(
    name="Agricultral Land Erosion",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"agricultural_land_erosion_rate": 1},
)
def agricultral_land_erosion():
    return agricultural_land_erosion_rate()


@component.add(
    name="Agricultural Land Conversion",
    units="ha/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"agricultural_land_conversion_rate_to_urban_land": 1},
)
def agricultural_land_conversion():
    return agricultural_land_conversion_rate_to_urban_land()


@component.add(
    name="Agricultural Land Degradation",
    units="ha",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_agricultural_land_degradation": 1},
    other_deps={
        "_integ_agricultural_land_degradation": {
            "initial": {},
            "step": {"agricultural_land_conversion": 1, "agricultral_land_erosion": 1},
        }
    },
)
def agricultural_land_degradation():
    """
    Negative changes in agricultural land area from year 1900.
    """
    return _integ_agricultural_land_degradation()


_integ_agricultural_land_degradation = Integ(
    lambda: agricultural_land_conversion() + agricultral_land_erosion(),
    lambda: 0,
    "_integ_agricultural_land_degradation",
)


@component.add(
    name="Agriculture C Emissions per Capita",
    units="TonC/(Person*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_agriculture_c_emissions": 1, "population": 1},
)
def agriculture_c_emissions_per_capita():
    return total_agriculture_c_emissions() / population()


@component.add(
    name="Agriculture CO2 Emissions per Capita",
    units="TonCO2/(Person*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_emissions_from_agriculture": 1, "population": 1},
)
def agriculture_co2_emissions_per_capita():
    return total_co2_emissions_from_agriculture() / population()


@component.add(
    name="Agro Food Nitrogen Production Footprint",
    units="kg/(Year*Person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "denitrification_rate": 1,
        "nitrogen_leaching_and_runoff_rate": 1,
        "ton_to_kg": 1,
        "population": 1,
    },
)
def agro_food_nitrogen_production_footprint():
    return (
        (denitrification_rate() + nitrogen_leaching_and_runoff_rate())
        * ton_to_kg()
        / population()
    )


@component.add(
    name="Animal Food supply",
    units="kcal/(Person*Day)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"animal_food_supply_kcal_capita_day": 1},
)
def animal_food_supply():
    return animal_food_supply_kcal_capita_day()


@component.add(
    name="Average Dietary Energy Supply Adequacy",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"food_supply_in_kcal": 1, "annual_caloric_demand": 1},
)
def average_dietary_energy_supply_adequacy():
    """
    (Average Daily Calorie Supply per Capita/Average Total Daily Calorie Intake)*100
    """
    return (
        sum(
            food_supply_in_kcal().rename({"FoodCategories": "FoodCategories!"}),
            dim=["FoodCategories!"],
        )
        / sum(
            annual_caloric_demand().rename({"FoodCategories": "FoodCategories!"}),
            dim=["FoodCategories!"],
        )
    ) * 100


@component.add(
    name="C in Atmosphere Compared to Preindustrial",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_atmosphere": 1, "preindustrial_c_in_atmosphere": 2},
)
def c_in_atmosphere_compared_to_preindustrial():
    return (
        (c_in_atmosphere() - preindustrial_c_in_atmosphere())
        / preindustrial_c_in_atmosphere()
    ) * 100


@component.add(
    name="Carbon Emissions per GWP",
    units="TonC/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_c_emission": 1, "gross_world_product": 1},
)
def carbon_emissions_per_gwp():
    return total_c_emission() / gross_world_product()


@component.add(
    name="Cereal Yield",
    units="Ton/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"area_harvested": 2, "crop_yield_for_each_category": 1},
)
def cereal_yield():
    return (
        float(area_harvested().loc["Grains"])
        * float(crop_yield_for_each_category().loc["Grains"])
    ) / float(area_harvested().loc["Grains"])


@component.add(
    name="Children Out of Primary School Rate",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "population_with_no_or_incomplete_education": 1,
        "population_cohorts": 1,
    },
)
def children_out_of_primary_school_rate():
    """
    ((sum(Population with No or Incomplete Education[Gender!,"10-14"])) / (sum(Population Cohorts[Gender!,"10-14"])))*100
    """
    return (
        sum(
            population_with_no_or_incomplete_education()
            .loc[:, '"10-14"']
            .reset_coords(drop=True)
            .rename({"Gender": "Gender!"}),
            dim=["Gender!"],
        )
        / sum(
            population_cohorts()
            .loc[:, '"10-14"']
            .reset_coords(drop=True)
            .rename({"Gender": "Gender!"}),
            dim=["Gender!"],
        )
    ) * 100


@component.add(
    name="CO2 Emissions from Fossil Energy",
    units="Billion ton CO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_co2_emissions_from_fossil_energy": 1,
        "tonco2_to_billion_tonco2": 1,
    },
)
def co2_emissions_from_fossil_energy():
    return total_co2_emissions_from_fossil_energy() * tonco2_to_billion_tonco2()


@component.add(
    name="CO2 Emissions per GWP",
    units="kgCO2/$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_co2_emissions_from_fossil_energy": 1,
        "ton_to_kg": 1,
        "gross_world_product": 1,
    },
)
def co2_emissions_per_gwp():
    return (
        total_co2_emissions_from_fossil_energy() * ton_to_kg() / gross_world_product()
    )


@component.add(
    name="Daily Calorie Demand Supply Average Deficit per Capita",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_daily_calorie_demand_per_capita": 2,
        "total_daily_calorie_supply_per_capita": 2,
    },
)
def daily_calorie_demand_supply_average_deficit_per_capita():
    return if_then_else(
        average_daily_calorie_demand_per_capita()
        / total_daily_calorie_supply_per_capita()
        > 1,
        lambda: (
            average_daily_calorie_demand_per_capita()
            / total_daily_calorie_supply_per_capita()
            - 1
        )
        * 100,
        lambda: 0,
    )


@component.add(
    name="Deforestation as Percentage of Initial Forest Land",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"init_forest_land": 2, "forest_land": 1},
)
def deforestation_as_percentage_of_initial_forest_land():
    return (
        float(np.maximum(0, init_forest_land() - forest_land())) / init_forest_land()
    ) * 100


@component.add(
    name="Energy Consumption",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_demand": 1, "energy_production": 1},
)
def energy_consumption():
    return float(np.minimum(energy_demand(), energy_production()))


@component.add(
    name="Energy Demand per Capita Calibrated",
    units="Mtoe/(Year*Person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"energy_demand": 1, "population": 1},
)
def energy_demand_per_capita_calibrated():
    return energy_demand() / population()


@component.add(
    name="Energy Intensity of GWP",
    units="MJ/$",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_energy_intensity_of_gwp": 1},
    other_deps={
        "_smooth_energy_intensity_of_gwp": {
            "initial": {
                "energy_production": 1,
                "mtoe_to_mj": 1,
                "gross_world_product": 1,
            },
            "step": {"energy_production": 1, "mtoe_to_mj": 1, "gross_world_product": 1},
        }
    },
)
def energy_intensity_of_gwp():
    return _smooth_energy_intensity_of_gwp()


_smooth_energy_intensity_of_gwp = Smooth(
    lambda: energy_production() * mtoe_to_mj() / gross_world_product(),
    lambda: 5,
    lambda: energy_production() * mtoe_to_mj() / gross_world_product(),
    lambda: 1,
    "_smooth_energy_intensity_of_gwp",
)


@component.add(
    name="Female to Male Enrollment in Tertiary Education",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"graduation_rate_from_tertiary_education": 2},
)
def female_to_male_enrollment_in_tertiary_education():
    return sum(
        graduation_rate_from_tertiary_education()
        .loc["female", :]
        .reset_coords(drop=True)
        .rename({"TertiaryGraduation": "TertiaryGraduation!"}),
        dim=["TertiaryGraduation!"],
    ) / sum(
        graduation_rate_from_tertiary_education()
        .loc["male", :]
        .reset_coords(drop=True)
        .rename({"TertiaryGraduation": "TertiaryGraduation!"}),
        dim=["TertiaryGraduation!"],
    )


@component.add(
    name="Food and Agriculture Nitrogen Balance",
    units="kg/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "commercial_n_application_for_agriculture": 1,
        "nitrogen_application_with_manure": 1,
        "total_n_uptake_rate": 1,
        "ton_to_kg": 1,
        "land_allocated_for_animal_calories": 1,
        "area_harvested": 1,
    },
)
def food_and_agriculture_nitrogen_balance():
    return (
        (
            commercial_n_application_for_agriculture()
            + nitrogen_application_with_manure()
            - total_n_uptake_rate()
        )
        * ton_to_kg()
        / (
            land_allocated_for_animal_calories()
            + sum(
                area_harvested().rename({"PlantFood": "PlantFood!"}), dim=["PlantFood!"]
            )
        )
    )


@component.add(
    name="Food and Agriculture Phosphorous Balance",
    units="kg/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "commercial_p_application_for_agriculture": 1,
        "phosphorus_application_with_manure": 1,
        "total_p_uptake_rate": 1,
        "ton_to_kg": 1,
        "land_allocated_for_animal_calories": 1,
        "area_harvested": 1,
    },
)
def food_and_agriculture_phosphorous_balance():
    return (
        (
            commercial_p_application_for_agriculture()
            + phosphorus_application_with_manure()
            - total_p_uptake_rate()
        )
        * ton_to_kg()
        / (
            land_allocated_for_animal_calories()
            + sum(
                area_harvested().rename({"PlantFood": "PlantFood!"}), dim=["PlantFood!"]
            )
        )
    )


@component.add(
    name="Food Calorie Deficit per Capita",
    units="Mkcal/(Person*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"food_shortage_in_kcal": 1, "population": 1},
)
def food_calorie_deficit_per_capita():
    return (
        float(
            np.maximum(
                0,
                sum(
                    food_shortage_in_kcal().rename(
                        {"FoodCategories": "FoodCategories!"}
                    ),
                    dim=["FoodCategories!"],
                ),
            )
        )
        / population()
    )


@component.add(
    name="Forest to Total Land Area",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"forest_land": 1, "total_land_area": 1},
)
def forest_to_total_land_area():
    return (forest_land() / total_land_area()) * 100


@component.add(
    name="Fossil Energy C Emissions per Capita",
    units="TonC/(Person*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_fossil_energy_c_emissions": 1, "population": 1},
)
def fossil_energy_c_emissions_per_capita():
    return total_fossil_energy_c_emissions() / population()


@component.add(
    name="Fossil Energy CO2 Emissions per Capita",
    units="TonCO2/(Person*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_emissions_from_fossil_energy": 1, "population": 1},
)
def fossil_energy_co2_emissions_per_capita():
    return total_co2_emissions_from_fossil_energy() / population()


@component.add(
    name="Global Food Tonnes Shortage",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"food_shortage_in_tonnes": 1},
)
def global_food_tonnes_shortage():
    return float(
        np.maximum(
            0,
            sum(
                food_shortage_in_tonnes().rename({"FoodCategories": "FoodCategories!"}),
                dim=["FoodCategories!"],
            ),
        )
    )


@component.add(
    name="GWP per Employed Person",
    units="$*Thousand/(Year*Person)",
    subscripts=["Gender", "WorkingAge"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gross_world_product": 1,
        "nvs_into_thousand": 1,
        "labor_force_input": 1,
        "indicative_labor_force_participation_fraction": 1,
    },
)
def gwp_per_employed_person():
    return (
        (gross_world_product() * nvs_into_thousand())
        / sum(
            labor_force_input().rename({"Labor force type": "Labor force type!"}),
            dim=["Labor force type!"],
        )
        * indicative_labor_force_participation_fraction()
    )


@component.add(
    name="ha into million ha",
    units="Million ha/ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ha_into_million_ha():
    return 1 / 1000000.0


@component.add(
    name="Investment in Biomass",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_biomass_capacity": 1,
        "investment_in_biomass_energy_efficiency": 1,
        "investment_in_biomass_energy_installation": 1,
        "investment_in_biomass_energy_technology": 1,
    },
)
def investment_in_biomass():
    return (
        investment_in_biomass_capacity()
        + investment_in_biomass_energy_efficiency()
        + investment_in_biomass_energy_installation()
        + investment_in_biomass_energy_technology()
    )


@component.add(
    name="Investment in Solar",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_solar_capacity": 1,
        "investment_in_solar_energy_efficiency": 1,
        "investment_in_solar_energy_installation": 1,
        "investment_in_solar_energy_technology": 1,
    },
)
def investment_in_solar():
    return (
        investment_in_solar_capacity()
        + investment_in_solar_energy_efficiency()
        + investment_in_solar_energy_installation()
        + investment_in_solar_energy_technology()
    )


@component.add(
    name="Investment in Wind",
    units="$/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_wind_capacity": 1,
        "investment_in_wind_energy_efficiency": 1,
        "investment_in_wind_energy_installation": 1,
        "investment_in_wind_energy_technology": 1,
    },
)
def investment_in_wind():
    return (
        investment_in_wind_capacity()
        + investment_in_wind_energy_efficiency()
        + investment_in_wind_energy_installation()
        + investment_in_wind_energy_technology()
    )


@component.add(
    name="Labour Force Female to Male Ratio",
    units="1",
    subscripts=["Cohorts"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={"labor_force": 2},
)
def labour_force_female_to_male_ratio():
    value = xr.DataArray(np.nan, {"Cohorts": _subscript_dict["Cohorts"]}, ["Cohorts"])
    value.loc[_subscript_dict["WorkingAge"]] = (
        labor_force().loc["female", :, "skill"].reset_coords(drop=True)
        / labor_force().loc["male", :, "skill"].reset_coords(drop=True)
    ).values
    value.loc[_subscript_dict['"Non-working age"']] = 0
    return value


@component.add(
    name="Land use C Emissions per Capita",
    units="TonC/(Person*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_land_use_c_emissions": 1, "population": 1},
)
def land_use_c_emissions_per_capita():
    return total_land_use_c_emissions() / population()


@component.add(
    name="Land use CO2 Emissions per Capita",
    units="TonCO2/(Person*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_emissions_from_land_use": 1, "population": 1},
)
def land_use_co2_emissions_per_capita():
    return total_co2_emissions_from_land_use() / population()


@component.add(
    name="Meat Based Diet Population Percentage",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_meat_eaters": 1, "population": 1},
)
def meat_based_diet_population_percentage():
    return total_meat_eaters() / population()


@component.add(
    name="Meat Based Food Production",
    units="Billion ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"food_production_rate": 2, "ton_to_billion_ton": 1},
)
def meat_based_food_production():
    return (
        float(food_production_rate().loc["PasMeat"])
        + float(food_production_rate().loc["CropMeat"])
    ) * ton_to_billion_ton()


@component.add(
    name="Mtoe to MJ", units="MJ/Mtoe", comp_type="Constant", comp_subtype="Normal"
)
def mtoe_to_mj():
    """
    https://www.unitjuggler.com/convert-energy-from-Mtoe-to-MJ.html
    """
    return 41868000000.0


@component.add(
    name="Nitrogen Fertilizer Use in Agriculture",
    units="Million ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"commercial_n_application_for_agriculture": 1, "ton_to_million_ton": 1},
)
def nitrogen_fertilizer_use_in_agriculture():
    return commercial_n_application_for_agriculture() * ton_to_million_ton()


@component.add(
    name="People with Access to Renewable Energy",
    units="Person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "renewable_energy_production": 1,
        "energy_demand_per_capita_calibrated": 1,
    },
)
def people_with_access_to_renewable_energy():
    return renewable_energy_production() / energy_demand_per_capita_calibrated()


@component.add(
    name="Per 1000 Women", units="Person", comp_type="Constant", comp_subtype="Normal"
)
def per_1000_women():
    return 1000


@component.add(
    name="Phosphorous Budget",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"p_budget": 1},
)
def phosphorous_budget():
    return p_budget()


@component.add(
    name="Phosphorous Fertilizer Use in Agriculture",
    units="Million ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"commercial_p_application_for_agriculture": 1, "ton_to_million_ton": 1},
)
def phosphorous_fertilizer_use_in_agriculture():
    return commercial_p_application_for_agriculture() * ton_to_million_ton()


@component.add(
    name="Plant Based Food Production",
    units="Billion ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"food_production_rate": 4, "ton_to_billion_ton": 1},
)
def plant_based_food_production():
    return (
        float(food_production_rate().loc["Pulses"])
        + float(food_production_rate().loc["Grains"])
        + float(food_production_rate().loc["VegFruits"])
        + float(food_production_rate().loc["OtherCrops"])
    ) * ton_to_billion_ton()


@component.add(
    name="Population Age 25 to 34 with Tertiary Education",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tertiary_education_graduates": 2, "population_cohorts": 2},
)
def population_age_25_to_34_with_tertiary_education():
    return (
        (
            sum(
                tertiary_education_graduates()
                .loc[:, '"25-29"']
                .reset_coords(drop=True)
                .rename({"Gender": "Gender!"}),
                dim=["Gender!"],
            )
            + sum(
                tertiary_education_graduates()
                .loc[:, '"30-34"']
                .reset_coords(drop=True)
                .rename({"Gender": "Gender!"}),
                dim=["Gender!"],
            )
        )
        / (
            sum(
                population_cohorts()
                .loc[:, '"25-29"']
                .reset_coords(drop=True)
                .rename({"Gender": "Gender!"}),
                dim=["Gender!"],
            )
            + sum(
                population_cohorts()
                .loc[:, '"30-34"']
                .reset_coords(drop=True)
                .rename({"Gender": "Gender!"}),
                dim=["Gender!"],
            )
        )
    ) * 100


@component.add(
    name="Potential Cropland Food Yield per Hectare",
    units="Ton/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"cropland_yield": 1},
)
def potential_cropland_food_yield_per_hectare():
    return cropland_yield()


@component.add(
    name="Potential Grassland Meat Yield per Hectare",
    units="Ton/(Year*ha)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"grassland_meat_yield": 1},
)
def potential_grassland_meat_yield_per_hectare():
    return grassland_meat_yield()


@component.add(
    name="Ratio of Agricultural Land Degraded",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"agricultural_land_degradation": 1, "agricultural_land": 1},
)
def ratio_of_agricultural_land_degraded():
    return (agricultural_land_degradation() / agricultural_land()) * 100


@component.add(
    name="Ratio of Agricultural Lands to Total Lands",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agricultural_land": 2,
        "forest_land": 1,
        "urban_and_industrial_land": 1,
    },
)
def ratio_of_agricultural_lands_to_total_lands():
    return agricultural_land() / (
        agricultural_land() + forest_land() + urban_and_industrial_land()
    )


@component.add(
    name="Renewable C Emissions per Capita",
    units="TonC/(Person*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_renewable_energy_c_emissions": 1, "population": 1},
)
def renewable_c_emissions_per_capita():
    return total_renewable_energy_c_emissions() / population()


@component.add(
    name="Renewable CO2 Emissions per Capita",
    units="TonCO2/(Person*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_emissions_from_renewables": 1, "population": 1},
)
def renewable_co2_emissions_per_capita():
    return total_co2_emissions_from_renewables() / population()


@component.add(
    name="Renewable Energy Access Percentage",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"people_with_access_to_renewable_energy": 1, "population": 1},
)
def renewable_energy_access_percentage():
    return (people_with_access_to_renewable_energy() / population()) * 100


@component.add(
    name="Renewable Energy Production",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_energy_production": 1,
        "solar_energy_production": 1,
        "wind_energy_production": 1,
    },
)
def renewable_energy_production():
    return (
        biomass_energy_production()
        + solar_energy_production()
        + wind_energy_production()
    )


@component.add(
    name="Share of Agriculture in Total C Emissions",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_c_emissions_from_the_agriculture": 1, "total_c_emission": 1},
)
def share_of_agriculture_in_total_c_emissions():
    return total_c_emissions_from_the_agriculture() / total_c_emission()


@component.add(
    name="Share of Fossil Energy in Total C Emissions",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_c_emission_from_fossil_fuels": 1, "total_c_emission": 1},
)
def share_of_fossil_energy_in_total_c_emissions():
    return total_c_emission_from_fossil_fuels() / total_c_emission()


@component.add(
    name="Share of Fossil Energy Supply",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "coal_production_indicator": 2,
        "gas_production_indicator": 2,
        "oil_production_indicator": 2,
        "wind_energy_production_indicator": 1,
        "solar_energy_production_indicator": 1,
        "biomass_energy_production_indicator": 1,
    },
)
def share_of_fossil_energy_supply():
    return (
        (
            coal_production_indicator()
            + gas_production_indicator()
            + oil_production_indicator()
        )
        / (
            coal_production_indicator()
            + gas_production_indicator()
            + oil_production_indicator()
            + solar_energy_production_indicator()
            + wind_energy_production_indicator()
            + biomass_energy_production_indicator()
        )
    ) * 100


@component.add(
    name="Share of Land Use in Total C Emissions",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_emission_from_land_use": 1, "total_c_emission": 1},
)
def share_of_land_use_in_total_c_emissions():
    return c_emission_from_land_use() / total_c_emission()


@component.add(
    name="Share of Renewable Energy in Total C Emissions",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_c_emission_from_renewables": 1, "total_c_emission": 1},
)
def share_of_renewable_energy_in_total_c_emissions():
    return total_c_emission_from_renewables() / total_c_emission()


@component.add(
    name="Share of Renewable Energy Supply",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_energy_production_indicator": 2,
        "solar_energy_production_indicator": 2,
        "wind_energy_production_indicator": 2,
        "coal_production_indicator": 1,
        "oil_production_indicator": 1,
        "gas_production_indicator": 1,
    },
)
def share_of_renewable_energy_supply():
    return (
        (
            biomass_energy_production_indicator()
            + solar_energy_production_indicator()
            + wind_energy_production_indicator()
        )
        / (
            coal_production_indicator()
            + gas_production_indicator()
            + oil_production_indicator()
            + solar_energy_production_indicator()
            + wind_energy_production_indicator()
            + biomass_energy_production_indicator()
        )
    ) * 100


@component.add(
    name="SSP Demographic Variation Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ssp_demographic_variation_time():
    return 5


@component.add(
    name="SSP Energy Demand Variation Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ssp_energy_demand_variation_time():
    return 5


@component.add(
    name="SSP Energy Production Variation Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ssp_energy_production_variation_time():
    return 5


@component.add(
    name="SSP Energy Technology Variation Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ssp_energy_technology_variation_time():
    return 5


@component.add(
    name="SSP Food and Diet Variation Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ssp_food_and_diet_variation_time():
    return 5


@component.add(
    name="SSP Land Use Change Variation Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ssp_land_use_change_variation_time():
    return 5


@component.add(
    name="ton to 1000ton",
    units="Thousonds ton/Ton",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ton_to_1000ton():
    return 1 / 1000


@component.add(
    name="ton to billion ton",
    units="Billion ton/Ton",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ton_to_billion_ton():
    return 1 / 1000000000.0


@component.add(
    name="ton to kg", units="kg/Ton", comp_type="Constant", comp_subtype="Normal"
)
def ton_to_kg():
    return 1000


@component.add(
    name="TonCO2 to Billion TonCO2",
    units="Billion ton CO2/TonCO2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def tonco2_to_billion_tonco2():
    return 1 / 1000000000.0


@component.add(
    name="Total Accumulated Phosphorous in Soil",
    units="Ton",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"phosphorus": 1},
)
def total_accumulated_phosphorous_in_soil():
    return phosphorus()


@component.add(
    name="Total Agriculture C Emissions",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_c_emissions_from_the_agriculture": 1},
)
def total_agriculture_c_emissions():
    return total_c_emissions_from_the_agriculture()


@component.add(
    name="Total CO2",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_co2_emissions_from_land_use": 1,
        "total_co2_emissions_from_agriculture": 1,
        "total_co2_emissions_from_fossil_energy": 1,
        "total_co2_emissions_from_renewables": 1,
    },
)
def total_co2():
    return (
        total_co2_emissions_from_land_use()
        + total_co2_emissions_from_agriculture()
        + total_co2_emissions_from_fossil_energy()
        + total_co2_emissions_from_renewables()
    )


@component.add(
    name="Total CO2 Emissions",
    units="Billion ton CO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tonco2_to_billion_tonco2": 1, "total_co2": 1},
)
def total_co2_emissions():
    return tonco2_to_billion_tonco2() * total_co2()


@component.add(
    name="Total CO2 Emissions from AFOLU",
    units="Billion ton CO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_from_agriculture": 1, "total_co2_from_land_use": 1},
)
def total_co2_emissions_from_afolu():
    return total_co2_from_agriculture() + total_co2_from_land_use()


@component.add(
    name="Total CO2 Emissions from Fossil Energy",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_c_emission_from_fossil_fuels": 1, "co2_to_c": 1},
)
def total_co2_emissions_from_fossil_energy():
    return total_c_emission_from_fossil_fuels() * co2_to_c()


@component.add(
    name="Total CO2 Emissions from Renewables",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_c_emission_from_renewables": 1, "co2_to_c": 1},
)
def total_co2_emissions_from_renewables():
    return total_c_emission_from_renewables() * co2_to_c()


@component.add(
    name="Total CO2 Emissions per Capita",
    units="TonCO2/(Person*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2": 1, "population": 1},
)
def total_co2_emissions_per_capita():
    return total_co2() / population()


@component.add(
    name="Total CO2 from Agriculture",
    units="Billion ton CO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_co2_emissions_from_agriculture": 1,
        "tonco2_to_billion_tonco2": 1,
    },
)
def total_co2_from_agriculture():
    return total_co2_emissions_from_agriculture() * tonco2_to_billion_tonco2()


@component.add(
    name="Total CO2 from Land Use",
    units="Billion ton CO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_emissions_from_land_use": 1, "tonco2_to_billion_tonco2": 1},
)
def total_co2_from_land_use():
    return total_co2_emissions_from_land_use() * tonco2_to_billion_tonco2()


@component.add(
    name="Total Croplands Indicator",
    units="Million ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"arable_land": 1, "permanent_crops": 1, "ha_into_million_ha": 1},
)
def total_croplands_indicator():
    return (arable_land() + permanent_crops()) * ha_into_million_ha()


@component.add(
    name="Total Energy CO2 Emissions per Capita",
    units="TonCO2/(Person*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fossil_energy_co2_emissions_per_capita": 1,
        "renewable_co2_emissions_per_capita": 1,
    },
)
def total_energy_co2_emissions_per_capita():
    return (
        fossil_energy_co2_emissions_per_capita() + renewable_co2_emissions_per_capita()
    )


@component.add(
    name="Total Food Supply",
    units="kcal/(Person*Day)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_daily_calorie_supply_per_capita": 1},
)
def total_food_supply():
    return total_daily_calorie_supply_per_capita()


@component.add(
    name="Total Fossil Energy C Emissions",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_c_emission_from_fossil_fuels": 1},
)
def total_fossil_energy_c_emissions():
    return total_c_emission_from_fossil_fuels()


@component.add(
    name="Total Land Area",
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
def total_land_area():
    return (
        agricultural_land() + forest_land() + other_land() + urban_and_industrial_land()
    )


@component.add(
    name="Total Land use C Emissions",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_emission_from_land_use": 1},
)
def total_land_use_c_emissions():
    return c_emission_from_land_use()


@component.add(
    name="Total Plant and Meat Based Food",
    units="Billion ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"meat_based_food_production": 1, "plant_based_food_production": 1},
)
def total_plant_and_meat_based_food():
    return meat_based_food_production() + plant_based_food_production()


@component.add(
    name="Total Renewable Energy C Emissions",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_c_emission_from_renewables": 1},
)
def total_renewable_energy_c_emissions():
    return total_c_emission_from_renewables()


@component.add(
    name="Total Renewable Investment per GWP",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "investment_in_biomass": 1,
        "investment_in_solar": 1,
        "investment_in_wind": 1,
        "population": 1,
        "gwp_per_capita": 1,
    },
)
def total_renewable_investment_per_gwp():
    return (
        (investment_in_biomass() + investment_in_solar() + investment_in_wind())
        / (population() * gwp_per_capita())
    ) * 100


@component.add(
    name="Total Secondary Enrolment Rate",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "primary_education_graduates": 1,
        "secondary_education_graduates": 1,
        "population_cohorts": 1,
    },
)
def total_secondary_enrolment_rate():
    return (
        (
            sum(
                primary_education_graduates()
                .loc[:, '"15-19"']
                .reset_coords(drop=True)
                .rename({"Gender": "Gender!"}),
                dim=["Gender!"],
            )
            + sum(
                secondary_education_graduates()
                .loc[:, '"15-19"']
                .reset_coords(drop=True)
                .rename({"Gender": "Gender!"}),
                dim=["Gender!"],
            )
        )
        / sum(
            population_cohorts()
            .loc[:, '"15-19"']
            .reset_coords(drop=True)
            .rename({"Gender": "Gender!"}),
            dim=["Gender!"],
        )
    ) * 100


@component.add(
    name="Vegetal Food Supply",
    units="kcal/(Person*Day)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"vegetal_food_supply_kcal_capita_day": 1},
)
def vegetal_food_supply():
    return vegetal_food_supply_kcal_capita_day()
