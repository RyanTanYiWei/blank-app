"""
Module diet_change
Translated using PySD version 3.14.3
"""

@component.add(
    name="Animal Calories Consumption Indicator",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"percentage_of_animal_calories": 1},
)
def animal_calories_consumption_indicator():
    return percentage_of_animal_calories()


@component.add(
    name="Animal Food Caloric Intake Indicator",
    units="kcal/(Person*Day)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"average_kcal_intake_per_person": 1},
)
def animal_food_caloric_intake_indicator():
    return sum(
        average_kcal_intake_per_person()
        .loc[_subscript_dict["AnimalFood"]]
        .rename({"FoodCategories": "AnimalFood!"}),
        dim=["AnimalFood!"],
    )


@component.add(
    name="Annual Caloric Demand",
    units="Mkcal/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "annual_caloric_demand_shift": 2,
        "variable_smooth_vegetarian_diet_switch_fnc": 1,
        "variable_smooth_meat_diet_switch_fnc": 1,
        "percentage_of_population_with_flexitarian_diet_from_meat_diet": 1,
        "percentage_of_population_with_flexitarian_diet_from_vegetarian_diet": 1,
        "annual_caloric_demand_flex": 1,
    },
)
def annual_caloric_demand():
    """
    This variable can be changed according to which diet composition is used.
    """
    return annual_caloric_demand_shift() + (
        variable_smooth_meat_diet_switch_fnc()
        * percentage_of_population_with_flexitarian_diet_from_meat_diet()
        + variable_smooth_vegetarian_diet_switch_fnc()
        * percentage_of_population_with_flexitarian_diet_from_vegetarian_diet()
    ) * (annual_caloric_demand_flex() - annual_caloric_demand_shift())


@component.add(
    name="Annual Caloric Demand AP",
    units="Mkcal/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "annual_caloric_demand_from_alternative_proteins": 1,
        "annual_caloric_demand_from_conventional_food": 2,
    },
)
def annual_caloric_demand_ap():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["AnimalFood"]] = (
        xr.DataArray(
            annual_caloric_demand_from_alternative_proteins()
            .rename({"AltProteins": "MapAnimalFood"})
            .values,
            {"AnimalFood": _subscript_dict["AnimalFood"]},
            ["AnimalFood"],
        )
        + annual_caloric_demand_from_conventional_food()
        .loc[_subscript_dict["AnimalFood"]]
        .rename({"FoodCategories": "AnimalFood"})
    ).values
    value.loc[_subscript_dict["PlantFood"]] = (
        annual_caloric_demand_from_conventional_food()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        .values
    )
    return value


@component.add(
    name="Annual Caloric Demand FAO",
    units="Mkcal/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_kcal_intake_per_person_fao": 1,
        "population": 1,
        "kcal_to_mkcal": 1,
        "days_in_year": 1,
    },
)
def annual_caloric_demand_fao():
    return (
        average_kcal_intake_per_person_fao()
        * population()
        * kcal_to_mkcal()
        * days_in_year()
    )


@component.add(
    name="Annual Caloric Demand FLEX",
    units="Mkcal/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_kcal_intake_per_person_flex": 1,
        "population": 1,
        "kcal_to_mkcal": 1,
        "days_in_year": 1,
    },
)
def annual_caloric_demand_flex():
    return (
        average_kcal_intake_per_person_flex()
        * population()
        * kcal_to_mkcal()
        * days_in_year()
    )


@component.add(
    name="Annual Caloric Demand from Alternative Proteins",
    units="Mkcal/Year",
    subscripts=["AltProteins"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_kcal_intake_per_person_from_alternative_proteins": 1,
        "population": 1,
        "days_in_year": 1,
        "kcal_to_mkcal": 1,
    },
)
def annual_caloric_demand_from_alternative_proteins():
    return (
        xr.DataArray(
            average_kcal_intake_per_person_from_alternative_proteins()
            .loc[_subscript_dict["MapAltProteins"]]
            .rename({"FoodCategories": "MapAltProteins"})
            .values,
            {"AltProteins": _subscript_dict["AltProteins"]},
            ["AltProteins"],
        )
        * population()
        * days_in_year()
        * kcal_to_mkcal()
    )


@component.add(
    name="Annual Caloric Demand from Conventional Food",
    units="Mkcal/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_kcal_intake_per_person_from_conventional_food": 1,
        "population": 1,
        "days_in_year": 1,
        "kcal_to_mkcal": 1,
    },
)
def annual_caloric_demand_from_conventional_food():
    return (
        average_kcal_intake_per_person_from_conventional_food()
        * population()
        * days_in_year()
        * kcal_to_mkcal()
    )


@component.add(
    name="Annual Caloric Demand Ref",
    units="Mkcal/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_kcal_intake_per_person_ref": 1,
        "population": 1,
        "days_in_year": 1,
        "kcal_to_mkcal": 1,
    },
)
def annual_caloric_demand_ref():
    return (
        average_kcal_intake_per_person_ref()
        * population()
        * days_in_year()
        * kcal_to_mkcal()
    )


@component.add(
    name="Annual Caloric Demand SHIFT",
    units="Mkcal/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_kcal_intake_shift": 1},
)
def annual_caloric_demand_shift():
    return sum(
        annual_kcal_intake_shift().rename({"Gender": "Gender!", "Cohorts": "Cohorts!"}),
        dim=["Gender!", "Cohorts!"],
    )


@component.add(
    name="Annual Caloric Demand WRI",
    units="Mkcal/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_kcal_intake_per_person_wri": 1,
        "population": 1,
        "kcal_to_mkcal": 1,
        "days_in_year": 1,
    },
)
def annual_caloric_demand_wri():
    return (
        average_kcal_intake_per_person_wri()
        * population()
        * kcal_to_mkcal()
        * days_in_year()
    )


@component.add(
    name="Annual Demand for Alternative Protein Technologies",
    units="Ton/Year",
    subscripts=["AltProteins", "AltProteinTech"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "annual_demand_for_alternative_proteins": 1,
        "fraction_of_alternative_protein_types_in_the_market": 1,
        "conventional_to_alternative_protein_conversion_factor": 1,
    },
)
def annual_demand_for_alternative_protein_technologies():
    """
    Annual demand for each alternative protein category (beef, chicken etc.) and technology (plant-based, microbial, cultivated)
    """
    return (
        annual_demand_for_alternative_proteins()
        * fraction_of_alternative_protein_types_in_the_market()
        * conventional_to_alternative_protein_conversion_factor()
    )


@component.add(
    name="Annual Demand for Alternative Proteins",
    units="Ton/Year",
    subscripts=["AltProteins"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "annual_caloric_demand_from_alternative_proteins": 1,
        "caloric_value_of_food": 1,
    },
)
def annual_demand_for_alternative_proteins():
    """
    Here, we assume that caloric value of per gram of alternative proteins is similar to the caloric value of animal source foods. This assumption is based on the fact that caloric value of alternative proteins is almost the same as conventional protein. For microbial protein and cultivated meat, it is because the same type of proteins and fat content is created, so leads to the same caloric values, For plant-based alternatives, the products sampled in the US market (Table 1 in OECD (2022) Meat Protein Alternatives) and in the Dutch market by me report caloric values per 100 gr similar to those of conventional counterparts. Therefore, we assume equivalent caloric values per mass.
    """
    return annual_caloric_demand_from_alternative_proteins() / xr.DataArray(
        caloric_value_of_food()
        .loc[_subscript_dict["MapAltProteins"]]
        .rename({"FoodCategories": "MapAltProteins"})
        .values,
        {"AltProteins": _subscript_dict["AltProteins"]},
        ["AltProteins"],
    )


@component.add(
    name="Annual Feedstock Demand of APs",
    units="Ton/Year",
    subscripts=["AltProteins", "AltProteinTech", "PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "annual_demand_for_alternative_protein_technologies": 1,
        "unit_feedstock_demand_for_alternative_proteins": 1,
    },
)
def annual_feedstock_demand_of_aps():
    return (
        annual_demand_for_alternative_protein_technologies()
        * unit_feedstock_demand_for_alternative_proteins()
    )


@component.add(
    name="Annual Kcal Intake SHIFT",
    units="Mkcal/Year",
    subscripts=["FoodCategories", "Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "days_in_year": 1,
        "kcal_to_mkcal": 1,
        "average_calorie_intake_in_vegetarian_diet": 1,
        "average_calorie_intake_in_meat_diet": 1,
        "meatbased_diet_followers": 1,
        "lactoovo_vegetarian_diet_followers": 1,
    },
)
def annual_kcal_intake_shift():
    return (
        days_in_year()
        * kcal_to_mkcal()
        * (
            average_calorie_intake_in_meat_diet()
            * sum(
                meatbased_diet_followers().rename({"Education": "Education!"}),
                dim=["Education!"],
            )
            + average_calorie_intake_in_vegetarian_diet()
            * sum(
                lactoovo_vegetarian_diet_followers().rename(
                    {"Education": "Education!"}
                ),
                dim=["Education!"],
            )
        )
    )


@component.add(
    name="Annual Total Crop Demand for APs",
    units="Ton/Year",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_feedstock_demand_of_aps": 1},
)
def annual_total_crop_demand_for_aps():
    return sum(
        annual_feedstock_demand_of_aps().rename(
            {"AltProteins": "AltProteins!", "AltProteinTech": "AltProteinTech!"}
        ),
        dim=["AltProteins!", "AltProteinTech!"],
    )


@component.add(
    name="Attitude multiplier for diet change",
    units="Dmnl",
    subscripts=["Education"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "l_risk_attitude": 1,
        "perceived_risk": 1,
        "k_risk_attitude": 1,
        "x0_risk_attitude": 1,
    },
)
def attitude_multiplier_for_diet_change():
    """
    ( L events risk / (1+( EXP(-k events risk*(Climate Events in Memory-x0 events risk) ) )) -(L events risk / 2))+0.5
    """
    return l_risk_attitude() / (
        1 + np.exp(-k_risk_attitude() * (perceived_risk() - x0_risk_attitude()))
    )


@component.add(
    name="Average calorie intake in meat diet",
    units="kcal/(Person*Day)",
    subscripts=["FoodCategories", "Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_total_daily_calorie_intake": 1,
        "meat_diet_composition_multiplier": 1,
    },
)
def average_calorie_intake_in_meat_diet():
    return average_total_daily_calorie_intake() * meat_diet_composition_multiplier()


@component.add(
    name="Average calorie intake in vegetarian diet",
    units="kcal/(Person*Day)",
    subscripts=["FoodCategories", "Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_total_daily_calorie_intake": 1,
        "vegetarian_diet_composition_multipliers": 1,
    },
)
def average_calorie_intake_in_vegetarian_diet():
    return (
        average_total_daily_calorie_intake() * vegetarian_diet_composition_multipliers()
    )


@component.add(
    name="Average Daily Calorie Demand per Capita",
    units="kcal/(Person*Day)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "global_total_calorie_demand_shift": 1,
        "population": 1,
        "kcal_to_mkcal": 1,
        "days_in_year": 1,
    },
)
def average_daily_calorie_demand_per_capita():
    return (
        global_total_calorie_demand_shift()
        / population()
        / kcal_to_mkcal()
        / days_in_year()
    )


@component.add(
    name="Average Kcal Intake per Person",
    units="kcal/(Person*Day)",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "annual_caloric_demand": 1,
        "kcal_to_mkcal": 1,
        "days_in_year": 1,
        "population": 1,
    },
)
def average_kcal_intake_per_person():
    return annual_caloric_demand() / (population() * days_in_year() * kcal_to_mkcal())


@component.add(
    name="Average Kcal Intake per Person FAO",
    units="kcal/(Person*Day)",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_total_daily_calorie_intake": 1,
        "global_average_diet_composition_fao": 1,
    },
)
def average_kcal_intake_per_person_fao():
    return (
        average_total_daily_calorie_intake()
        * global_average_diet_composition_fao()
        / 100
    )


@component.add(
    name="Average Kcal Intake per Person FLEX",
    units="kcal/(Person*Day)",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_total_daily_calorie_intake": 1,
        "global_average_diet_composition_flex": 1,
    },
)
def average_kcal_intake_per_person_flex():
    return (
        average_total_daily_calorie_intake()
        * global_average_diet_composition_flex()
        / 100
    )


@component.add(
    name="Average Kcal Intake per Person from Alternative Proteins",
    units="kcal/(Person*Day)",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={
        "average_total_daily_calorie_intake": 1,
        "felix_diet_composition": 1,
        "market_share_of_alternative_proteins": 1,
        "nvs_100_percent": 2,
    },
)
def average_kcal_intake_per_person_from_alternative_proteins():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["AnimalFood"]] = (
        average_total_daily_calorie_intake()
        * felix_diet_composition()
        .loc[_subscript_dict["AnimalFood"]]
        .rename({"FoodCategories": "AnimalFood"})
        * xr.DataArray(
            market_share_of_alternative_proteins()
            .rename({"AltProteins": "MapAnimalFood"})
            .values,
            {"AnimalFood": _subscript_dict["AnimalFood"]},
            ["AnimalFood"],
        )
        / (nvs_100_percent() * nvs_100_percent())
    ).values
    value.loc[_subscript_dict["PlantFood"]] = 0
    return value


@component.add(
    name="Average Kcal Intake per Person from Conventional Food",
    units="kcal/(Person*Day)",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_total_daily_calorie_intake": 2,
        "felix_diet_composition": 2,
        "market_share_of_alternative_proteins": 1,
        "nvs_100_percent": 4,
    },
)
def average_kcal_intake_per_person_from_conventional_food():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["AnimalFood"]] = (
        average_total_daily_calorie_intake()
        * felix_diet_composition()
        .loc[_subscript_dict["AnimalFood"]]
        .rename({"FoodCategories": "AnimalFood"})
        * (
            nvs_100_percent()
            - xr.DataArray(
                market_share_of_alternative_proteins()
                .rename({"AltProteins": "MapAnimalFood"})
                .values,
                {"AnimalFood": _subscript_dict["AnimalFood"]},
                ["AnimalFood"],
            )
        )
        / (nvs_100_percent() * nvs_100_percent())
    ).values
    value.loc[_subscript_dict["PlantFood"]] = (
        felix_diet_composition()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        * average_total_daily_calorie_intake()
        / nvs_100_percent()
    ).values
    return value


@component.add(
    name="Average Kcal Intake per Person Ref",
    units="kcal/(Person*Day)",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "felix_diet_composition": 1,
        "average_total_daily_calorie_intake": 1,
        "nvs_100_percent": 1,
    },
)
def average_kcal_intake_per_person_ref():
    return (
        felix_diet_composition()
        * average_total_daily_calorie_intake()
        / nvs_100_percent()
    )


@component.add(
    name="Average Kcal Intake per Person SHIFT",
    units="kcal/(Person*Day)",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "annual_caloric_demand_shift": 1,
        "kcal_to_mkcal": 1,
        "days_in_year": 1,
        "population": 1,
    },
)
def average_kcal_intake_per_person_shift():
    return annual_caloric_demand_shift() / (
        population() * days_in_year() * kcal_to_mkcal()
    )


@component.add(
    name="Average Kcal Intake per Person WRI",
    units="kcal/(Person*Day)",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_total_daily_calorie_intake": 1,
        "global_average_diet_composition_wri": 1,
    },
)
def average_kcal_intake_per_person_wri():
    return (
        average_total_daily_calorie_intake()
        * global_average_diet_composition_wri()
        / 100
    )


@component.add(
    name="Average Total Daily Calorie Intake",
    units="kcal/(Person*Day)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_daily_caloric_intake": 1,
        "effect_of_gwp_on_daily_caloric_intake": 1,
    },
)
def average_total_daily_calorie_intake():
    return reference_daily_caloric_intake() * effect_of_gwp_on_daily_caloric_intake()


@component.add(
    name="CI S", units="kcal/(Person*Day)", comp_type="Constant", comp_subtype="Normal"
)
def ci_s():
    """
    1961 World average, from FAO data - 2194 kcal Calibrated 1672.6 kcal 1970 value, when gdp effect=1:2325
    """
    return 1672.6


@component.add(
    name="CI Var S",
    units="kcal/(Person*Day)",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_ci_var_s": 1},
    other_deps={
        "_smooth_ci_var_s": {
            "initial": {"ci_s": 1, "time": 1},
            "step": {"ci_s": 1, "time": 1},
        }
    },
)
def ci_var_s():
    """
    1961 World average, from FAO data - 2194 kcal Calibrated 1672.6 kcal 1970 value, when gdp effect=1:2325
    """
    return 1672.6 + _smooth_ci_var_s()


_smooth_ci_var_s = Smooth(
    lambda: step(__data["time"], ci_s() - 1672.6, 2020),
    lambda: 1,
    lambda: step(__data["time"], ci_s() - 1672.6, 2020),
    lambda: 1,
    "_smooth_ci_var_s",
)


@component.add(
    name="Conventional to alternative protein conversion factor",
    units="Dmnl",
    subscripts=["AltProteinTech"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def conventional_to_alternative_protein_conversion_factor():
    """
    This parameter represents how much of the alternative protein is required to replace the conventional protein. For plant-based and cultivated meat, it is assumed to be 1, since for plant-based alternatives, the recipes are designed accordingly and for cultivated meat, it is the same protein type. For microbial protein, due to the protein and moisture content, Humpenoder (2022) calculates that 1 dry-matter ton of meat can be replaced by 0.73 DM ton of microbial protein.
    """
    return xr.DataArray(
        [1.0, 0.73, 1.0],
        {"AltProteinTech": _subscript_dict["AltProteinTech"]},
        ["AltProteinTech"],
    )


@component.add(
    name="Diet Composition Percentage",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"average_kcal_intake_per_person": 2},
)
def diet_composition_percentage():
    return average_kcal_intake_per_person() / sum(
        average_kcal_intake_per_person().rename({"FoodCategories": "FoodCategories!"}),
        dim=["FoodCategories!"],
    )


@component.add(
    name="Effect of GWP on Calorie Intake Lookup",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_effect_of_gwp_on_calorie_intake_lookup"
    },
)
def effect_of_gwp_on_calorie_intake_lookup(x, final_subs=None):
    return _hardcodedlookup_effect_of_gwp_on_calorie_intake_lookup(x, final_subs)


_hardcodedlookup_effect_of_gwp_on_calorie_intake_lookup = HardcodedLookups(
    [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0],
    [0.4, 0.52, 1.0, 1.15, 1.26, 1.33, 1.38, 1.4, 1.42],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_effect_of_gwp_on_calorie_intake_lookup",
)


@component.add(
    name="Effect of GWP on Daily Caloric Intake",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "relative_gwp_per_capita": 1,
        "effect_of_gwp_on_calorie_intake_lookup": 1,
    },
)
def effect_of_gwp_on_daily_caloric_intake():
    """
    See FAOSTAT_..DailyCaloriesOverTime.xlsx GWP scenario: [(0,0)-(2.5,1.5)],(0,0.5),(0.25,0.55),(0.5,0.62),(0.75,0.75),(1,1),(1.25,1. 12),(1.5,1.2),(1.75,1.26),(2,1.3),(2.25,1.33),(2.5,1.35) ) BAU Scenario: ([(0,0)-(4,1.5)],(0,0.4),(0.5,0.52),(1,1),(1.5,1.15),(2,1.26),(2.5,1.33),(3 ,1.38),(3.5,1.4),(4,1.42) )
    """
    return effect_of_gwp_on_calorie_intake_lookup(relative_gwp_per_capita())


@component.add(
    name="Effect of GWP on Meat Consumption",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"relative_gwp_per_capita": 1},
)
def effect_of_gwp_on_meat_consumption():
    """
    See FAOSTAT_...meatpercapita.xlsx forhow I derived the lookup.
    """
    return np.interp(
        relative_gwp_per_capita(),
        [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0],
        [0.4, 0.47, 0.57, 0.76, 1.0, 1.24, 1.43, 1.53, 1.67, 1.82, 1.87, 1.9, 1.92],
    )


@component.add(
    name="End Year of Meat Diet Switch",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def end_year_of_meat_diet_switch():
    return 2050


@component.add(
    name="End Year of Vegetarian Diet Switch",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def end_year_of_vegetarian_diet_switch():
    return 2050


@component.add(
    name="FeliX Diet Composition",
    units="percent",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def felix_diet_composition():
    return xr.DataArray(
        [1.845, 5.775, 6.759, 1.198, 2.356, 47.829, 8.237, 26.0],
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )


@component.add(
    name="Flexitarian diet decomposition multiplier",
    units="Dmnl",
    subscripts=["FoodCategories", "Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "flexitarian_diet_decomposition_multiplier_male": 1,
        "flexitarian_diet_decomposition_multiplier_female": 1,
    },
)
def flexitarian_diet_decomposition_multiplier():
    """
    Modified by Q. Ye in June 2024
    """
    value = xr.DataArray(
        np.nan,
        {
            "FoodCategories": _subscript_dict["FoodCategories"],
            "Gender": _subscript_dict["Gender"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["FoodCategories", "Gender", "Cohorts"],
    )
    value.loc[:, ["male"], :] = (
        flexitarian_diet_decomposition_multiplier_male()
        .expand_dims({"Gender": ["male"]}, 1)
        .values
    )
    value.loc[:, ["female"], :] = (
        flexitarian_diet_decomposition_multiplier_female()
        .expand_dims({"Gender": ["female"]}, 1)
        .values
    )
    return value


@component.add(
    name="Flexitarian diet decomposition multiplier female",
    subscripts=["FoodCategories", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def flexitarian_diet_decomposition_multiplier_female():
    """
    Data please see the excel file 'New_DietData.xlsx' , 'Model Input' , 'y22' Added by Q. Ye
    """
    value = xr.DataArray(
        np.nan,
        {
            "FoodCategories": _subscript_dict["FoodCategories"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["FoodCategories", "Cohorts"],
    )
    value.loc[["PasMeat"], :] = xr.DataArray(
        [
            [
                0.0026121,
                0.00330866,
                0.00417936,
                0.00444057,
                0.00478885,
                0.0043535,
                0.0043535,
                0.0043535,
                0.0043535,
                0.0043535,
                0.00391815,
                0.00391815,
                0.00391815,
                0.00391815,
                0.00391815,
                0.00391815,
                0.00391815,
                0.00391815,
                0.00391815,
                0.00391815,
                0.00391815,
            ]
        ],
        {"FoodCategories": ["PasMeat"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["CropMeat"], :] = xr.DataArray(
        [
            [
                0.0146278,
                0.0185285,
                0.0234044,
                0.0248672,
                0.0268176,
                0.0243796,
                0.0243796,
                0.0243796,
                0.0243796,
                0.0243796,
                0.0219416,
                0.0219416,
                0.0219416,
                0.0219416,
                0.0219416,
                0.0219416,
                0.0219416,
                0.0219416,
                0.0219416,
                0.0219416,
                0.0219416,
            ]
        ],
        {"FoodCategories": ["CropMeat"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Dairy"], :] = xr.DataArray(
        [
            [
                0.0463213,
                0.0586736,
                0.074114,
                0.0787461,
                0.0849223,
                0.0772021,
                0.0772021,
                0.0772021,
                0.0772021,
                0.0772021,
                0.0694819,
                0.0694819,
                0.0694819,
                0.0694819,
                0.0694819,
                0.0694819,
                0.0694819,
                0.0694819,
                0.0694819,
                0.0694819,
                0.0694819,
            ]
        ],
        {"FoodCategories": ["Dairy"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Eggs"], :] = xr.DataArray(
        [
            [
                0.00441155,
                0.00558796,
                0.00705848,
                0.00749963,
                0.00808784,
                0.00735258,
                0.00735258,
                0.00735258,
                0.00735258,
                0.00735258,
                0.00661732,
                0.00661732,
                0.00661732,
                0.00661732,
                0.00661732,
                0.00661732,
                0.00661732,
                0.00661732,
                0.00661732,
                0.00661732,
                0.00661732,
            ]
        ],
        {"FoodCategories": ["Eggs"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Pulses"], :] = xr.DataArray(
        [
            [
                0.040981,
                0.0519092,
                0.0655695,
                0.0696676,
                0.0751318,
                0.0683016,
                0.0683016,
                0.0683016,
                0.0683016,
                0.0683016,
                0.0614714,
                0.0614714,
                0.0614714,
                0.0614714,
                0.0614714,
                0.0614714,
                0.0614714,
                0.0614714,
                0.0614714,
                0.0614714,
                0.0614714,
            ]
        ],
        {"FoodCategories": ["Pulses"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Grains"], :] = xr.DataArray(
        [
            [
                0.17407,
                0.220489,
                0.278513,
                0.29592,
                0.319129,
                0.290117,
                0.290117,
                0.290117,
                0.290117,
                0.290117,
                0.261106,
                0.261106,
                0.261106,
                0.261106,
                0.261106,
                0.261106,
                0.261106,
                0.261106,
                0.261106,
                0.261106,
                0.261106,
            ]
        ],
        {"FoodCategories": ["Grains"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["VegFruits"], :] = xr.DataArray(
        [
            [
                0.0700159,
                0.0886868,
                0.112025,
                0.119027,
                0.128363,
                0.116693,
                0.116693,
                0.116693,
                0.116693,
                0.116693,
                0.105024,
                0.105024,
                0.105024,
                0.105024,
                0.105024,
                0.105024,
                0.105024,
                0.105024,
                0.105024,
                0.105024,
                0.105024,
            ]
        ],
        {"FoodCategories": ["VegFruits"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["OtherCrops"], :] = xr.DataArray(
        [
            [
                0.223073,
                0.28256,
                0.356917,
                0.379225,
                0.408968,
                0.371789,
                0.371789,
                0.371789,
                0.371789,
                0.371789,
                0.33461,
                0.33461,
                0.33461,
                0.33461,
                0.33461,
                0.33461,
                0.33461,
                0.33461,
                0.33461,
                0.33461,
                0.33461,
            ]
        ],
        {"FoodCategories": ["OtherCrops"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    return value


@component.add(
    name="Flexitarian diet decomposition multiplier male",
    subscripts=["FoodCategories", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def flexitarian_diet_decomposition_multiplier_male():
    """
    Data please see the excel file 'New_DietData.xlsx' , 'Model Input' , 'y22' Added by Q. Ye
    """
    value = xr.DataArray(
        np.nan,
        {
            "FoodCategories": _subscript_dict["FoodCategories"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["FoodCategories", "Cohorts"],
    )
    value.loc[["PasMeat"], :] = xr.DataArray(
        [
            [
                0.00275722,
                0.0034828,
                0.00461471,
                0.00600783,
                0.0060949,
                0.00565955,
                0.00565955,
                0.00565955,
                0.00565955,
                0.0052242,
                0.0052242,
                0.0052242,
                0.0052242,
                0.00478885,
                0.00478885,
                0.00478885,
                0.00478885,
                0.00478885,
                0.00478885,
                0.00478885,
                0.00478885,
            ]
        ],
        {"FoodCategories": ["PasMeat"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["CropMeat"], :] = xr.DataArray(
        [
            [
                0.0154404,
                0.0195037,
                0.0258424,
                0.0336439,
                0.0341314,
                0.0316935,
                0.0316935,
                0.0316935,
                0.0316935,
                0.0292555,
                0.0292555,
                0.0292555,
                0.0292555,
                0.0268176,
                0.0268176,
                0.0268176,
                0.0268176,
                0.0268176,
                0.0268176,
                0.0268176,
                0.0268176,
            ]
        ],
        {"FoodCategories": ["CropMeat"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Dairy"], :] = xr.DataArray(
        [
            [
                0.0488947,
                0.0617617,
                0.0818342,
                0.106539,
                0.108083,
                0.100363,
                0.100363,
                0.100363,
                0.100363,
                0.0926425,
                0.0926425,
                0.0926425,
                0.0926425,
                0.0849223,
                0.0849223,
                0.0849223,
                0.0849223,
                0.0849223,
                0.0849223,
                0.0849223,
                0.0849223,
            ]
        ],
        {"FoodCategories": ["Dairy"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Eggs"], :] = xr.DataArray(
        [
            [
                0.00465663,
                0.00588206,
                0.00779373,
                0.0101466,
                0.0102936,
                0.00955835,
                0.00955835,
                0.00955835,
                0.00955835,
                0.0088231,
                0.0088231,
                0.0088231,
                0.0088231,
                0.00808784,
                0.00808784,
                0.00808784,
                0.00808784,
                0.00808784,
                0.00808784,
                0.00808784,
                0.00808784,
            ]
        ],
        {"FoodCategories": ["Eggs"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Pulses"], :] = xr.DataArray(
        [
            [
                0.0432577,
                0.0546413,
                0.0723997,
                0.0942562,
                0.0956222,
                0.0887921,
                0.0887921,
                0.0887921,
                0.0887921,
                0.0819619,
                0.0819619,
                0.0819619,
                0.0819619,
                0.0751318,
                0.0751318,
                0.0751318,
                0.0751318,
                0.0751318,
                0.0751318,
                0.0751318,
                0.0751318,
            ]
        ],
        {"FoodCategories": ["Pulses"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Grains"], :] = xr.DataArray(
        [
            [
                0.183741,
                0.232094,
                0.307524,
                0.400362,
                0.406164,
                0.377153,
                0.377153,
                0.377153,
                0.377153,
                0.348141,
                0.348141,
                0.348141,
                0.348141,
                0.319129,
                0.319129,
                0.319129,
                0.319129,
                0.319129,
                0.319129,
                0.319129,
                0.319129,
            ]
        ],
        {"FoodCategories": ["Grains"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["VegFruits"], :] = xr.DataArray(
        [
            [
                0.0739057,
                0.0933545,
                0.123695,
                0.161037,
                0.16337,
                0.151701,
                0.151701,
                0.151701,
                0.151701,
                0.140032,
                0.140032,
                0.140032,
                0.140032,
                0.128363,
                0.128363,
                0.128363,
                0.128363,
                0.128363,
                0.128363,
                0.128363,
                0.128363,
            ]
        ],
        {"FoodCategories": ["VegFruits"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["OtherCrops"], :] = xr.DataArray(
        [
            [
                0.235466,
                0.297431,
                0.394096,
                0.513069,
                0.520505,
                0.483326,
                0.483326,
                0.483326,
                0.483326,
                0.446147,
                0.446147,
                0.446147,
                0.446147,
                0.408968,
                0.408968,
                0.408968,
                0.408968,
                0.408968,
                0.408968,
                0.408968,
                0.408968,
            ]
        ],
        {"FoodCategories": ["OtherCrops"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    return value


@component.add(
    name="Fraction intended to change diet",
    units="Dmnl",
    subscripts=["Cohorts", "Gender", "Education"],
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_fraction_intended_to_change_diet": 1},
    other_deps={
        "_smooth_fraction_intended_to_change_diet": {
            "initial": {"indicative_fraction_intended_to_change_diet": 1},
            "step": {
                "indicative_fraction_intended_to_change_diet": 1,
                "intention_delay": 1,
            },
        }
    },
)
def fraction_intended_to_change_diet():
    return _smooth_fraction_intended_to_change_diet()


_smooth_fraction_intended_to_change_diet = Smooth(
    lambda: indicative_fraction_intended_to_change_diet(),
    lambda: xr.DataArray(
        intention_delay(),
        {
            "Cohorts": _subscript_dict["Cohorts"],
            "Gender": _subscript_dict["Gender"],
            "Education": _subscript_dict["Education"],
        },
        ["Cohorts", "Gender", "Education"],
    ),
    lambda: indicative_fraction_intended_to_change_diet(),
    lambda: 1,
    "_smooth_fraction_intended_to_change_diet",
)


@component.add(
    name="Fraction of alternative protein types in the market",
    units="Dmnl",
    subscripts=["AltProteins", "AltProteinTech"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def fraction_of_alternative_protein_types_in_the_market():
    """
    This parameter represents the share of each alternative protein technology in the substitution of each alternative protein category. For each protein category, the sum of parameters should be equal to 1. For instance, Fraction...[AltPasMeat,Plant]=0.8 means that 80% of the substition of pasture-based meat by alternative proteins will be provided by plant-based alternative proteins. The values of this parameter also depend on the overall replacement share, since higher replacement rates can only be achieved by precision fermentation and cultivated meat, as they are the only ones that can replcae unprocessed meat and dairy and eggs.
    """
    value = xr.DataArray(
        np.nan,
        {
            "AltProteins": _subscript_dict["AltProteins"],
            "AltProteinTech": _subscript_dict["AltProteinTech"],
        },
        ["AltProteins", "AltProteinTech"],
    )
    value.loc[["AltPasMeat"], :] = xr.DataArray(
        [[0.8, 0.1, 0.1]],
        {
            "AltProteins": ["AltPasMeat"],
            "AltProteinTech": _subscript_dict["AltProteinTech"],
        },
        ["AltProteins", "AltProteinTech"],
    ).values
    value.loc[["AltCropMeat"], :] = xr.DataArray(
        [[0.8, 0.1, 0.1]],
        {
            "AltProteins": ["AltCropMeat"],
            "AltProteinTech": _subscript_dict["AltProteinTech"],
        },
        ["AltProteins", "AltProteinTech"],
    ).values
    value.loc[["AltDairy"], :] = xr.DataArray(
        [[0.33, 0.67, 0.0]],
        {
            "AltProteins": ["AltDairy"],
            "AltProteinTech": _subscript_dict["AltProteinTech"],
        },
        ["AltProteins", "AltProteinTech"],
    ).values
    value.loc[["AltEggs"], :] = xr.DataArray(
        [[0.0, 1.0, 0.0]],
        {
            "AltProteins": ["AltEggs"],
            "AltProteinTech": _subscript_dict["AltProteinTech"],
        },
        ["AltProteins", "AltProteinTech"],
    ).values
    return value


@component.add(
    name="Global Average Diet Composition FAO",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def global_average_diet_composition_fao():
    """
    Wordl reference: m4 Flexitarian : y4
    """
    return xr.DataArray(
        [1.77, 7.54, 6.92, 1.25, 2.36, 46.11, 12.77, 20.4],
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )


@component.add(
    name="Global Average Diet Composition FLEX",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def global_average_diet_composition_flex():
    """
    Wordl reference: m4 Flexitarian : y4
    """
    return xr.DataArray(
        [0.45, 2.52, 7.98, 0.76, 7.06, 29.988, 12.062, 38.43],
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )


@component.add(
    name="Global Average Diet Composition WRI",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def global_average_diet_composition_wri():
    """
    Wordl reference: m4 Flexitarian : y4
    """
    return xr.DataArray(
        [1.8, 5.7, 6.8, 1.2, 2.3, 48.0, 8.2, 26.0],
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )


@component.add(
    name="Global Total Calorie Demand FAO",
    units="Mkcal/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_caloric_demand_fao": 1},
)
def global_total_calorie_demand_fao():
    return sum(
        annual_caloric_demand_fao().rename({"FoodCategories": "FoodCategories!"}),
        dim=["FoodCategories!"],
    )


@component.add(
    name="Global Total Calorie Demand FLEX",
    units="Mkcal/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_caloric_demand_flex": 1},
)
def global_total_calorie_demand_flex():
    return sum(
        annual_caloric_demand_flex().rename({"FoodCategories": "FoodCategories!"}),
        dim=["FoodCategories!"],
    )


@component.add(
    name="Global Total Calorie Demand SHIFT",
    units="Mkcal/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_caloric_demand_shift": 1},
)
def global_total_calorie_demand_shift():
    return sum(
        annual_caloric_demand_shift().rename({"FoodCategories": "FoodCategories!"}),
        dim=["FoodCategories!"],
    )


@component.add(
    name="Global Total Calorie Demand WRI",
    units="Mkcal/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"annual_caloric_demand_wri": 1},
)
def global_total_calorie_demand_wri():
    return sum(
        annual_caloric_demand_wri().rename({"FoodCategories": "FoodCategories!"}),
        dim=["FoodCategories!"],
    )


@component.add(
    name="Healthy diet decomposition multiplier",
    units="Dmnl",
    subscripts=["FoodCategories", "Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "healthy_diet_decomposition_multiplier_male": 1,
        "healthy_diet_decomposition_multiplier_female": 1,
    },
)
def healthy_diet_decomposition_multiplier():
    value = xr.DataArray(
        np.nan,
        {
            "FoodCategories": _subscript_dict["FoodCategories"],
            "Gender": _subscript_dict["Gender"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["FoodCategories", "Gender", "Cohorts"],
    )
    value.loc[:, ["male"], :] = (
        healthy_diet_decomposition_multiplier_male()
        .expand_dims({"Gender": ["male"]}, 1)
        .values
    )
    value.loc[:, ["female"], :] = (
        healthy_diet_decomposition_multiplier_female()
        .expand_dims({"Gender": ["female"]}, 1)
        .values
    )
    return value


@component.add(
    name="Healthy diet decomposition multiplier female",
    subscripts=["FoodCategories", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def healthy_diet_decomposition_multiplier_female():
    """
    Original data please see the excel file New_DietData, sheet Model Input, B74 add by Q. Ye in June 2024
    """
    value = xr.DataArray(
        np.nan,
        {
            "FoodCategories": _subscript_dict["FoodCategories"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["FoodCategories", "Cohorts"],
    )
    value.loc[["PasMeat"], :] = xr.DataArray(
        [
            [
                0.00777826,
                0.00985246,
                0.0124452,
                0.013223,
                0.0142601,
                0.0129638,
                0.0129638,
                0.0129638,
                0.0129638,
                0.0129638,
                0.0116674,
                0.0116674,
                0.0116674,
                0.0116674,
                0.0116674,
                0.0116674,
                0.0116674,
                0.0116674,
                0.0116674,
                0.0116674,
                0.0116674,
            ]
        ],
        {"FoodCategories": ["PasMeat"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["CropMeat"], :] = xr.DataArray(
        [
            [
                0.0237411,
                0.0300721,
                0.0379857,
                0.0403599,
                0.0435253,
                0.0395685,
                0.0395685,
                0.0395685,
                0.0395685,
                0.0395685,
                0.0356116,
                0.0356116,
                0.0356116,
                0.0356116,
                0.0356116,
                0.0356116,
                0.0356116,
                0.0356116,
                0.0356116,
                0.0356116,
                0.0356116,
            ]
        ],
        {"FoodCategories": ["CropMeat"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Dairy"], :] = xr.DataArray(
        [
            [
                0.0451603,
                0.0572031,
                0.0722565,
                0.0767725,
                0.0827939,
                0.0752672,
                0.0752672,
                0.0752672,
                0.0752672,
                0.0752672,
                0.0677405,
                0.0677405,
                0.0677405,
                0.0677405,
                0.0677405,
                0.0677405,
                0.0677405,
                0.0677405,
                0.0677405,
                0.0677405,
                0.0677405,
            ]
        ],
        {"FoodCategories": ["Dairy"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Eggs"], :] = xr.DataArray(
        [
            [
                0.00429545,
                0.00544091,
                0.00687273,
                0.00730227,
                0.007875,
                0.00715909,
                0.00715909,
                0.00715909,
                0.00715909,
                0.00715909,
                0.00644318,
                0.00644318,
                0.00644318,
                0.00644318,
                0.00644318,
                0.00644318,
                0.00644318,
                0.00644318,
                0.00644318,
                0.00644318,
                0.00644318,
            ]
        ],
        {"FoodCategories": ["Eggs"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Pulses"], :] = xr.DataArray(
        [
            [
                0.0399361,
                0.0505858,
                0.0638978,
                0.0678914,
                0.0732162,
                0.0665602,
                0.0665602,
                0.0665602,
                0.0665602,
                0.0665602,
                0.0599042,
                0.0599042,
                0.0599042,
                0.0599042,
                0.0599042,
                0.0599042,
                0.0599042,
                0.0599042,
                0.0599042,
                0.0599042,
                0.0599042,
            ]
        ],
        {"FoodCategories": ["Pulses"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Grains"], :] = xr.DataArray(
        [
            [
                0.169679,
                0.214927,
                0.271487,
                0.288455,
                0.311078,
                0.282799,
                0.282799,
                0.282799,
                0.282799,
                0.282799,
                0.254519,
                0.254519,
                0.254519,
                0.254519,
                0.254519,
                0.254519,
                0.254519,
                0.254519,
                0.254519,
                0.254519,
                0.254519,
            ]
        ],
        {"FoodCategories": ["Grains"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["VegFruits"], :] = xr.DataArray(
        [
            [
                0.0682542,
                0.0864553,
                0.109207,
                0.116032,
                0.125133,
                0.113757,
                0.113757,
                0.113757,
                0.113757,
                0.113757,
                0.102381,
                0.102381,
                0.102381,
                0.102381,
                0.102381,
                0.102381,
                0.102381,
                0.102381,
                0.102381,
                0.102381,
                0.102381,
            ]
        ],
        {"FoodCategories": ["VegFruits"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["OtherCrops"], :] = xr.DataArray(
        [
            [
                0.217385,
                0.275354,
                0.347816,
                0.369554,
                0.398539,
                0.362308,
                0.362308,
                0.362308,
                0.362308,
                0.362308,
                0.326077,
                0.326077,
                0.326077,
                0.326077,
                0.326077,
                0.326077,
                0.326077,
                0.326077,
                0.326077,
                0.326077,
                0.326077,
            ]
        ],
        {"FoodCategories": ["OtherCrops"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    return value


@component.add(
    name="Healthy diet decomposition multiplier male",
    subscripts=["FoodCategories", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def healthy_diet_decomposition_multiplier_male():
    """
    Original data please see the excel file New_DietData, sheet Model Input, B74 add by Q. Ye in June 2024
    """
    value = xr.DataArray(
        np.nan,
        {
            "FoodCategories": _subscript_dict["FoodCategories"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["FoodCategories", "Cohorts"],
    )
    value.loc[["PasMeat"], :] = xr.DataArray(
        [
            [
                0.00821038,
                0.010371,
                0.0137416,
                0.01789,
                0.0181493,
                0.0168529,
                0.0168529,
                0.0168529,
                0.0168529,
                0.0155565,
                0.0155565,
                0.0155565,
                0.0155565,
                0.0142601,
                0.0142601,
                0.0142601,
                0.0142601,
                0.0142601,
                0.0142601,
                0.0142601,
                0.0142601,
            ]
        ],
        {"FoodCategories": ["PasMeat"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["CropMeat"], :] = xr.DataArray(
        [
            [
                0.02506,
                0.0316548,
                0.0419426,
                0.0546045,
                0.0553959,
                0.051439,
                0.051439,
                0.051439,
                0.051439,
                0.0474822,
                0.0474822,
                0.0474822,
                0.0474822,
                0.0435253,
                0.0435253,
                0.0435253,
                0.0435253,
                0.0435253,
                0.0435253,
                0.0435253,
                0.0435253,
            ]
        ],
        {"FoodCategories": ["CropMeat"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Dairy"], :] = xr.DataArray(
        [
            [
                0.0476692,
                0.0602138,
                0.0797832,
                0.103869,
                0.105374,
                0.0978474,
                0.0978474,
                0.0978474,
                0.0978474,
                0.0903206,
                0.0903206,
                0.0903206,
                0.0903206,
                0.0827939,
                0.0827939,
                0.0827939,
                0.0827939,
                0.0827939,
                0.0827939,
                0.0827939,
                0.0827939,
            ]
        ],
        {"FoodCategories": ["Dairy"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Eggs"], :] = xr.DataArray(
        [
            [
                0.00453409,
                0.00572727,
                0.00758864,
                0.00987955,
                0.0100227,
                0.00930682,
                0.00930682,
                0.00930682,
                0.00930682,
                0.00859091,
                0.00859091,
                0.00859091,
                0.00859091,
                0.007875,
                0.007875,
                0.007875,
                0.007875,
                0.007875,
                0.007875,
                0.007875,
                0.007875,
            ]
        ],
        {"FoodCategories": ["Eggs"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Pulses"], :] = xr.DataArray(
        [
            [
                0.0421548,
                0.0532482,
                0.0705538,
                0.0918531,
                0.0931843,
                0.0865283,
                0.0865283,
                0.0865283,
                0.0865283,
                0.0798722,
                0.0798722,
                0.0798722,
                0.0798722,
                0.0732162,
                0.0732162,
                0.0732162,
                0.0732162,
                0.0732162,
                0.0732162,
                0.0732162,
                0.0732162,
            ]
        ],
        {"FoodCategories": ["Pulses"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Grains"], :] = xr.DataArray(
        [
            [
                0.179106,
                0.226239,
                0.299767,
                0.390262,
                0.395918,
                0.367638,
                0.367638,
                0.367638,
                0.367638,
                0.339358,
                0.339358,
                0.339358,
                0.339358,
                0.311078,
                0.311078,
                0.311078,
                0.311078,
                0.311078,
                0.311078,
                0.311078,
                0.311078,
            ]
        ],
        {"FoodCategories": ["Grains"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["VegFruits"], :] = xr.DataArray(
        [
            [
                0.0720461,
                0.0910056,
                0.120582,
                0.156985,
                0.15926,
                0.147884,
                0.147884,
                0.147884,
                0.147884,
                0.136508,
                0.136508,
                0.136508,
                0.136508,
                0.125133,
                0.125133,
                0.125133,
                0.125133,
                0.125133,
                0.125133,
                0.125133,
                0.125133,
            ]
        ],
        {"FoodCategories": ["VegFruits"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["OtherCrops"], :] = xr.DataArray(
        [
            [
                0.229462,
                0.289846,
                0.384047,
                0.499985,
                0.507231,
                0.471,
                0.471,
                0.471,
                0.471,
                0.43477,
                0.43477,
                0.43477,
                0.43477,
                0.398539,
                0.398539,
                0.398539,
                0.398539,
                0.398539,
                0.398539,
                0.398539,
                0.398539,
            ]
        ],
        {"FoodCategories": ["OtherCrops"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    return value


@component.add(
    name="Indicative fraction intended to change diet",
    units="1/Year",
    subscripts=["Cohorts", "Gender", "Education"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "self_efficacy_multiplier": 1,
        "subjective_norm_multiplier_for_diet_change": 1,
        "attitude_multiplier_for_diet_change": 1,
        "normal_fraction_intended_to_change_diet_stepped": 1,
    },
)
def indicative_fraction_intended_to_change_diet():
    return (
        self_efficacy_multiplier()
        * subjective_norm_multiplier_for_diet_change()
        * attitude_multiplier_for_diet_change()
        * normal_fraction_intended_to_change_diet_stepped()
    ).transpose("Cohorts", "Gender", "Education")


@component.add(
    name="Inflow PVA",
    units="People",
    subscripts=["Gender", "Cohorts", "Education"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"meatbased_diet_followers": 1},
)
def inflow_pva():
    return meatbased_diet_followers()


@component.add(
    name='"Initial Meat-based Diet Followers"',
    units="People",
    subscripts=["Gender", "Cohorts", "Education"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_meatbased_diet_followers_male": 1,
        "initial_meatbased_diet_followers_female": 1,
    },
)
def initial_meatbased_diet_followers():
    """
    these are 1900 values.
    """
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "Cohorts": _subscript_dict["Cohorts"],
            "Education": _subscript_dict["Education"],
        },
        ["Gender", "Cohorts", "Education"],
    )
    value.loc[["male"], :, :] = (
        initial_meatbased_diet_followers_male()
        .transpose("Cohorts", "Education")
        .expand_dims({"Gender": ["male"]}, 0)
        .values
    )
    value.loc[["female"], :, :] = (
        initial_meatbased_diet_followers_female()
        .transpose("Cohorts", "Education")
        .expand_dims({"Gender": ["female"]}, 0)
        .values
    )
    return value


@component.add(
    name='"Initial Meat-based Diet Followers Female"',
    subscripts=["Education", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_meatbased_diet_followers_female():
    """
    For original data, please see the excel file 'InitialValues.xlsx','Diet','I3' Added by Q. Ye in June 2024
    """
    value = xr.DataArray(
        np.nan,
        {
            "Education": _subscript_dict["Education"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["Education", "Cohorts"],
    )
    value.loc[["noEd"], :] = xr.DataArray(
        [
            [
                9.18850e07,
                8.00404e07,
                5.91789e07,
                4.27795e07,
                3.40475e07,
                2.90060e07,
                2.47110e07,
                2.05249e07,
                1.65649e07,
                1.29426e07,
                9.75216e06,
                7.05763e06,
                4.65308e06,
                2.46278e06,
                1.12046e06,
                4.31770e05,
                1.52535e05,
                4.12820e04,
                1.11720e04,
                2.54000e03,
                5.17000e02,
            ]
        ],
        {"Education": ["noEd"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Education", "Cohorts"],
    ).values
    value.loc[["primary"], :] = xr.DataArray(
        [
            [
                1.00000e00,
                1.00000e00,
                1.19116e07,
                1.05796e07,
                9.21584e06,
                7.85123e06,
                6.68868e06,
                5.55560e06,
                4.48371e06,
                3.50326e06,
                2.63968e06,
                1.91033e06,
                1.25948e06,
                6.66617e05,
                3.03281e05,
                1.16870e05,
                4.12880e04,
                1.11740e04,
                3.02400e03,
                6.88000e02,
                1.40000e02,
            ]
        ],
        {"Education": ["primary"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Education", "Cohorts"],
    ).values
    value.loc[["secondary"], :] = xr.DataArray(
        [
            [
                1.00000e00,
                1.00000e00,
                1.00000e00,
                1.12297e07,
                9.78214e06,
                8.33368e06,
                7.09969e06,
                5.89699e06,
                4.75923e06,
                3.71854e06,
                2.80188e06,
                2.02772e06,
                1.33687e06,
                7.07579e05,
                3.21918e05,
                1.24052e05,
                4.38250e04,
                1.18610e04,
                3.21000e03,
                7.30000e02,
                1.49000e02,
            ]
        ],
        {"Education": ["secondary"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Education", "Cohorts"],
    ).values
    value.loc[["tertiary"], :] = xr.DataArray(
        [
            [
                1.00000e00,
                1.00000e00,
                1.00000e00,
                1.00000e00,
                1.95643e06,
                1.66674e06,
                1.41994e06,
                1.17940e06,
                9.51846e05,
                7.43707e05,
                5.60377e05,
                4.05544e05,
                2.67374e05,
                1.41516e05,
                6.43840e04,
                2.48110e04,
                8.76500e03,
                2.37200e03,
                6.42000e02,
                1.46000e02,
                3.00000e01,
            ]
        ],
        {"Education": ["tertiary"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Education", "Cohorts"],
    ).values
    return value


@component.add(
    name='"Initial Meat-based Diet Followers Male"',
    subscripts=["Education", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_meatbased_diet_followers_male():
    """
    For original data, please see the excel file 'InitialValues.xlsx','Diet','C3' Added by Q. Ye in June 2024
    """
    value = xr.DataArray(
        np.nan,
        {
            "Education": _subscript_dict["Education"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["Education", "Cohorts"],
    )
    value.loc[["noEd"], :] = xr.DataArray(
        [
            [
                9.28938e07,
                8.09191e07,
                5.45859e07,
                3.71262e07,
                2.86053e07,
                2.43696e07,
                2.07612e07,
                1.72442e07,
                1.39171e07,
                1.08739e07,
                8.19336e06,
                5.92953e06,
                3.90932e06,
                2.06913e06,
                9.41365e05,
                3.62756e05,
                1.28154e05,
                3.46830e04,
                9.38600e03,
                2.13500e03,
                4.34000e02,
            ]
        ],
        {"Education": ["noEd"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Education", "Cohorts"],
    ).values
    value.loc[["primary"], :] = xr.DataArray(
        [
            [
                1.00000e00,
                1.00000e00,
                1.72850e07,
                1.53523e07,
                1.33732e07,
                1.13930e07,
                9.70604e06,
                8.06182e06,
                6.50638e06,
                5.08364e06,
                3.83048e06,
                2.77211e06,
                1.82764e06,
                9.67337e05,
                4.40096e05,
                1.69592e05,
                5.99130e04,
                1.62150e04,
                4.38900e03,
                9.98000e02,
                2.03000e02,
            ]
        ],
        {"Education": ["primary"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Education", "Cohorts"],
    ).values
    value.loc[["secondary"], :] = xr.DataArray(
        [
            [
                1.00000e00,
                1.00000e00,
                1.00000e00,
                1.30365e07,
                1.13560e07,
                9.67449e06,
                8.24197e06,
                6.84576e06,
                5.52495e06,
                4.31682e06,
                3.25268e06,
                2.35396e06,
                1.55196e06,
                8.21423e05,
                3.73712e05,
                1.44011e05,
                5.08760e04,
                1.37690e04,
                3.72600e03,
                8.48000e02,
                1.72000e02,
            ]
        ],
        {"Education": ["secondary"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Education", "Cohorts"],
    ).values
    value.loc[["tertiary"], :] = xr.DataArray(
        [
            [
                1.00000e00,
                1.00000e00,
                1.00000e00,
                1.00000e00,
                2.27120e06,
                1.93490e06,
                1.64839e06,
                1.36915e06,
                1.10499e06,
                8.63363e05,
                6.50536e05,
                4.70793e05,
                3.10392e05,
                1.64285e05,
                7.47420e04,
                2.88020e04,
                1.01750e04,
                2.75300e03,
                7.45000e02,
                1.70000e02,
                3.40000e01,
            ]
        ],
        {"Education": ["tertiary"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Education", "Cohorts"],
    ).values
    return value


@component.add(
    name="Initial Pop Ed",
    units="People",
    subscripts=["Gender", "Cohorts", "Education"],
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_initial_pop_ed": 1},
    other_deps={
        "_initial_initial_pop_ed": {
            "initial": {"population_wrt_education": 1},
            "step": {},
        }
    },
)
def initial_pop_ed():
    return _initial_initial_pop_ed()


_initial_initial_pop_ed = Initial(
    lambda: population_wrt_education(), "_initial_initial_pop_ed"
)


@component.add(
    name="Initial Vegetarian Diet Followers",
    units="People",
    subscripts=["Gender", "Cohorts", "Education"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_vegetarian_diet_followers_male": 1,
        "initial_vegetarian_diet_followers_female": 1,
    },
)
def initial_vegetarian_diet_followers():
    """
    these are the 2010 population values, with the assumption that meat-vegetarioan ratio is 1-2.
    """
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "Cohorts": _subscript_dict["Cohorts"],
            "Education": _subscript_dict["Education"],
        },
        ["Gender", "Cohorts", "Education"],
    )
    value.loc[["male"], :, :] = (
        initial_vegetarian_diet_followers_male()
        .transpose("Cohorts", "Education")
        .expand_dims({"Gender": ["male"]}, 0)
        .values
    )
    value.loc[["female"], :, :] = (
        initial_vegetarian_diet_followers_female()
        .transpose("Cohorts", "Education")
        .expand_dims({"Gender": ["female"]}, 0)
        .values
    )
    return value


@component.add(
    name="Initial Vegetarian Diet Followers Female",
    subscripts=["Education", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_vegetarian_diet_followers_female():
    """
    Original data please see the excel file 'InitialValues.xlsx','Diet','I26' Added by Q. Ye in June 2024
    """
    value = xr.DataArray(
        np.nan,
        {
            "Education": _subscript_dict["Education"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["Education", "Cohorts"],
    )
    value.loc[["noEd"], :] = xr.DataArray(
        [
            [
                2.56150e07,
                2.23130e07,
                1.64974e07,
                1.19257e07,
                9.49150e06,
                8.08607e06,
                6.88874e06,
                5.72178e06,
                4.61782e06,
                3.60805e06,
                2.71863e06,
                1.96747e06,
                1.29715e06,
                6.86556e05,
                3.12353e05,
                1.20366e05,
                4.25230e04,
                1.15080e04,
                3.11500e03,
                7.08000e02,
                1.44000e02,
            ]
        ],
        {"Education": ["noEd"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Education", "Cohorts"],
    ).values
    value.loc[["primary"], :] = xr.DataArray(
        [
            [
                1.00000e00,
                1.00000e00,
                3.32061e06,
                2.94931e06,
                2.56912e06,
                2.18871e06,
                1.86462e06,
                1.54875e06,
                1.24994e06,
                9.76614e05,
                7.35869e05,
                5.32548e05,
                3.51107e05,
                1.85834e05,
                8.45470e04,
                3.25800e04,
                1.15100e04,
                3.11500e03,
                8.43000e02,
                1.92000e02,
                3.90000e01,
            ]
        ],
        {"Education": ["primary"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Education", "Cohorts"],
    ).values
    value.loc[["secondary"], :] = xr.DataArray(
        [
            [
                1.00000e00,
                1.00000e00,
                1.00000e00,
                3.13054e06,
                2.72699e06,
                2.32320e06,
                1.97920e06,
                1.64392e06,
                1.32674e06,
                1.03662e06,
                7.81087e05,
                5.65272e05,
                3.72682e05,
                1.97254e05,
                8.97420e04,
                3.45820e04,
                1.22170e04,
                3.30600e03,
                8.95000e02,
                2.04000e02,
                4.10000e01,
            ]
        ],
        {"Education": ["secondary"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Education", "Cohorts"],
    ).values
    value.loc[["tertiary"], :] = xr.DataArray(
        [
            [
                1.00000e00,
                1.00000e00,
                1.00000e00,
                1.00000e00,
                5.45398e05,
                4.64640e05,
                3.95839e05,
                3.28783e05,
                2.65348e05,
                2.07325e05,
                1.56217e05,
                1.13054e05,
                7.45360e04,
                3.94510e04,
                1.79480e04,
                6.91600e03,
                2.44300e03,
                6.61000e02,
                1.79000e02,
                4.10000e01,
                8.00000e00,
            ]
        ],
        {"Education": ["tertiary"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Education", "Cohorts"],
    ).values
    return value


@component.add(
    name="Initial Vegetarian Diet Followers Male",
    subscripts=["Education", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_vegetarian_diet_followers_male():
    """
    Original data please see the excel file 'InitialValues.xlsx','Diet','C26' Added by Q. Ye in June 2024
    """
    value = xr.DataArray(
        np.nan,
        {
            "Education": _subscript_dict["Education"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["Education", "Cohorts"],
    )
    value.loc[["noEd"], :] = xr.DataArray(
        [
            [
                2.58962e07,
                2.25580e07,
                1.52170e07,
                1.03498e07,
                7.97436e06,
                6.79358e06,
                5.78764e06,
                4.80720e06,
                3.87970e06,
                3.03134e06,
                2.28408e06,
                1.65299e06,
                1.08981e06,
                5.76816e05,
                2.62426e05,
                1.01126e05,
                3.57260e04,
                9.66900e03,
                2.61700e03,
                5.95000e02,
                1.21000e02,
            ]
        ],
        {"Education": ["noEd"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Education", "Cohorts"],
    ).values
    value.loc[["primary"], :] = xr.DataArray(
        [
            [
                1.00000e00,
                1.00000e00,
                4.81859e06,
                4.27979e06,
                3.72809e06,
                3.17606e06,
                2.70578e06,
                2.24741e06,
                1.81380e06,
                1.41718e06,
                1.06783e06,
                7.72788e05,
                5.09497e05,
                2.69667e05,
                1.22687e05,
                4.72770e04,
                1.67020e04,
                4.52000e03,
                1.22300e03,
                2.78000e02,
                5.70000e01,
            ]
        ],
        {"Education": ["primary"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Education", "Cohorts"],
    ).values
    value.loc[["secondary"], :] = xr.DataArray(
        [
            [
                1.00000e00,
                1.00000e00,
                1.00000e00,
                3.63422e06,
                3.16574e06,
                2.69698e06,
                2.29763e06,
                1.90841e06,
                1.54020e06,
                1.20341e06,
                9.06758e05,
                6.56220e05,
                4.32644e05,
                2.28990e05,
                1.04180e05,
                4.01460e04,
                1.41830e04,
                3.83800e03,
                1.03900e03,
                2.36000e02,
                4.80000e01,
            ]
        ],
        {"Education": ["secondary"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Education", "Cohorts"],
    ).values
    value.loc[["tertiary"], :] = xr.DataArray(
        [
            [
                1.00000e00,
                1.00000e00,
                1.00000e00,
                1.00000e00,
                6.33148e05,
                5.39397e05,
                4.59527e05,
                3.81682e05,
                3.08041e05,
                2.40682e05,
                1.81352e05,
                1.31244e05,
                8.65290e04,
                4.57980e04,
                2.08360e04,
                8.02900e03,
                2.83700e03,
                7.68000e02,
                2.08000e02,
                4.70000e01,
                1.00000e01,
            ]
        ],
        {"Education": ["tertiary"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Education", "Cohorts"],
    ).values
    return value


@component.add(
    name="Intention Delay", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def intention_delay():
    return 3


@component.add(
    name="k risk attitude",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_k_risk_attitude": 1, "time": 1},
)
def k_risk_attitude():
    """
    .5
    """
    return 0.9 + step(__data["time"], sa_k_risk_attitude() - 0.9, 2020)


@component.add(
    name="k social norm",
    units="Dmnl",
    subscripts=["Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_k_social_norm": 4, "time": 4},
)
def k_social_norm():
    value = xr.DataArray(np.nan, {"Cohorts": _subscript_dict["Cohorts"]}, ["Cohorts"])
    value.loc[_subscript_dict["Childhood"]] = 5 + step(
        __data["time"], float(sa_k_social_norm().loc['"10-14"']) - 5, 2020
    )
    value.loc[_subscript_dict["Young"]] = 8 + step(
        __data["time"], float(sa_k_social_norm().loc['"20-24"']) - 8, 2020
    )
    value.loc[_subscript_dict["MiddleAged"]] = 8 + step(
        __data["time"], float(sa_k_social_norm().loc['"40-44"']) - 8, 2020
    )
    value.loc[_subscript_dict["OldAge"]] = 5 + step(
        __data["time"], float(sa_k_social_norm().loc['"80-84"']) - 5, 2020
    )
    return value


@component.add(
    name="kcal to Mkcal",
    units="Mkcal/kcal",
    comp_type="Constant",
    comp_subtype="Normal",
)
def kcal_to_mkcal():
    return 1e-06


@component.add(
    name="L risk attitude",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_l_risk_attitude": 1, "time": 1},
)
def l_risk_attitude():
    return 2 + step(__data["time"], sa_l_risk_attitude() - 2, 2020)


@component.add(
    name="L social norm",
    units="Dmnl",
    subscripts=["Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_l_social_norm": 4, "time": 4},
)
def l_social_norm():
    value = xr.DataArray(np.nan, {"Cohorts": _subscript_dict["Cohorts"]}, ["Cohorts"])
    value.loc[_subscript_dict["Childhood"]] = 1.2 + step(
        __data["time"], float(sa_l_social_norm().loc['"10-14"']) - 1.2, 2020
    )
    value.loc[_subscript_dict["Young"]] = 1.5 + step(
        __data["time"], float(sa_l_social_norm().loc['"20-24"']) - 1.5, 2020
    )
    value.loc[_subscript_dict["MiddleAged"]] = 1.5 + step(
        __data["time"], float(sa_l_social_norm().loc['"40-44"']) - 1.5, 2020
    )
    value.loc[_subscript_dict["OldAge"]] = 1.2 + step(
        __data["time"], float(sa_l_social_norm().loc['"80-84"']) - 1.2, 2020
    )
    return value


@component.add(
    name="Lactoovo Vegetarian Diet Followers",
    units="People",
    subscripts=["Gender", "Cohorts", "Education"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_lactoovo_vegetarian_diet_followers": 1},
    other_deps={
        "_integ_lactoovo_vegetarian_diet_followers": {
            "initial": {"initial_vegetarian_diet_followers": 1},
            "step": {
                "shift_from_meatbased_to_vegetarian": 1,
                "shift_from_vegetarian_to_meatbased": 1,
                "population_increase_rate": 1,
            },
        }
    },
)
def lactoovo_vegetarian_diet_followers():
    return _integ_lactoovo_vegetarian_diet_followers()


_integ_lactoovo_vegetarian_diet_followers = Integ(
    lambda: shift_from_meatbased_to_vegetarian()
    - shift_from_vegetarian_to_meatbased()
    + population_increase_rate(),
    lambda: initial_vegetarian_diet_followers(),
    "_integ_lactoovo_vegetarian_diet_followers",
)


@component.add(
    name="Market share of alternative proteins",
    units="percent",
    subscripts=["AltProteins"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "switch_alternative_protein_scenario": 1,
        "time": 1,
        "market_share_of_alternative_proteins_until_2050": 1,
        "market_share_of_alternative_proteins_until_2100": 1,
    },
)
def market_share_of_alternative_proteins():
    return if_then_else(
        switch_alternative_protein_scenario() == 0,
        lambda: xr.DataArray(
            0, {"AltProteins": _subscript_dict["AltProteins"]}, ["AltProteins"]
        ),
        lambda: if_then_else(
            time() <= 2050,
            lambda: market_share_of_alternative_proteins_until_2050(),
            lambda: market_share_of_alternative_proteins_until_2100(),
        ),
    )


@component.add(
    name="Market share of alternative proteins in 2050",
    units="percent",
    subscripts=["AltProteins"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def market_share_of_alternative_proteins_in_2050():
    return xr.DataArray(
        [15.0, 25.0, 50.0, 5.0],
        {"AltProteins": _subscript_dict["AltProteins"]},
        ["AltProteins"],
    )


@component.add(
    name="Market share of alternative proteins in 2100",
    units="percent",
    subscripts=["AltProteins"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def market_share_of_alternative_proteins_in_2100():
    return xr.DataArray(
        [60.0, 80.0, 80.0, 20.0],
        {"AltProteins": _subscript_dict["AltProteins"]},
        ["AltProteins"],
    )


@component.add(
    name="Market share of alternative proteins until 2050",
    units="percent",
    subscripts=["AltProteins"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "market_share_of_alternative_proteins_in_2050": 1,
        "year2050": 2,
        "current_year": 2,
        "time": 1,
    },
)
def market_share_of_alternative_proteins_until_2050():
    return ramp(
        __data["time"],
        market_share_of_alternative_proteins_in_2050() / (year2050() - current_year()),
        current_year(),
        year2050(),
    )


@component.add(
    name="Market share of alternative proteins until 2100",
    units="percent",
    subscripts=["AltProteins"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "market_share_of_alternative_proteins_in_2050": 2,
        "time": 1,
        "year2100": 2,
        "year2050": 2,
        "market_share_of_alternative_proteins_in_2100": 1,
    },
)
def market_share_of_alternative_proteins_until_2100():
    return market_share_of_alternative_proteins_in_2050() + ramp(
        __data["time"],
        (
            market_share_of_alternative_proteins_in_2100()
            - market_share_of_alternative_proteins_in_2050()
        )
        / (year2100() - year2050()),
        year2050(),
        year2100(),
    )


@component.add(
    name="Meat Based Diet Followers Indicator",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"percentage_of_meatbased_diet_followers": 1},
)
def meat_based_diet_followers_indicator():
    return float(np.maximum(0, percentage_of_meatbased_diet_followers()))


@component.add(
    name="Meat diet composition multiplier",
    units="Dmnl",
    subscripts=["FoodCategories", "Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_meat_diet_decomposition_multiplier": 4,
        "variable_smooth_meat_diet_switch_fnc": 1,
        "meat_diet_composition_switch": 3,
        "flexitarian_diet_decomposition_multiplier": 1,
        "healthy_diet_decomposition_multiplier": 1,
        "target_percentage_of_meat_eaters": 1,
    },
)
def meat_diet_composition_multiplier():
    """
    0 = Ref 1 = Healthy 2 = Flexitarian Else = Ref
    """
    return (
        reference_meat_diet_decomposition_multiplier()
        + variable_smooth_meat_diet_switch_fnc()
        * target_percentage_of_meat_eaters()
        * (
            if_then_else(
                meat_diet_composition_switch() == 0,
                lambda: reference_meat_diet_decomposition_multiplier(),
                lambda: if_then_else(
                    meat_diet_composition_switch() == 1,
                    lambda: healthy_diet_decomposition_multiplier(),
                    lambda: if_then_else(
                        meat_diet_composition_switch() == 2,
                        lambda: flexitarian_diet_decomposition_multiplier(),
                        lambda: reference_meat_diet_decomposition_multiplier(),
                    ),
                ),
            )
            - reference_meat_diet_decomposition_multiplier()
        )
    )


@component.add(
    name="Meat Diet Composition Switch",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def meat_diet_composition_switch():
    return 0


@component.add(
    name='"Meat-based Diet Followers"',
    units="People",
    subscripts=["Gender", "Cohorts", "Education"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "population_wrt_education": 1,
        "lactoovo_vegetarian_diet_followers": 1,
        "shift_from_meatbased_to_vegetarian": 1,
        "shift_from_vegetarian_to_meatbased": 1,
    },
)
def meatbased_diet_followers():
    return (
        np.maximum(0, population_wrt_education() - lactoovo_vegetarian_diet_followers())
        + 0 * shift_from_meatbased_to_vegetarian()
        + 0 * shift_from_vegetarian_to_meatbased()
    )


@component.add(
    name="Normal fraction intended to change diet",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"normal_fraction_intended_to_change_diet_variation": 1, "time": 1},
)
def normal_fraction_intended_to_change_diet():
    """
    BaseRun: 0.04 HigherIntention: 0.08
    """
    return 0.04 + step(
        __data["time"], normal_fraction_intended_to_change_diet_variation() - 0.04, 2020
    )


@component.add(
    name="Normal fraction intended to change diet stepped",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"normal_fraction_intended_to_change_diet": 1, "time": 1},
)
def normal_fraction_intended_to_change_diet_stepped():
    return 0 + step(__data["time"], normal_fraction_intended_to_change_diet(), 2010)


@component.add(
    name="Normal Fraction Intended to Change Diet Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_fraction_intended_to_change_diet_variation():
    return 0.04


@component.add(
    name="Normal shift fraction from meat to vegetarianism",
    units="1/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_normal_shift_fraction_from_meat_to_vegetarianism": 1},
    other_deps={
        "_smooth_normal_shift_fraction_from_meat_to_vegetarianism": {
            "initial": {
                "normal_shift_fraction_from_meat_to_vegetarianism_variation": 1,
                "time": 1,
            },
            "step": {
                "normal_shift_fraction_from_meat_to_vegetarianism_variation": 1,
                "time": 1,
                "ssp_food_and_diet_variation_time": 1,
            },
        }
    },
)
def normal_shift_fraction_from_meat_to_vegetarianism():
    return 0.003 + _smooth_normal_shift_fraction_from_meat_to_vegetarianism()


_smooth_normal_shift_fraction_from_meat_to_vegetarianism = Smooth(
    lambda: step(
        __data["time"],
        normal_shift_fraction_from_meat_to_vegetarianism_variation() - 0.003,
        2020,
    ),
    lambda: ssp_food_and_diet_variation_time(),
    lambda: step(
        __data["time"],
        normal_shift_fraction_from_meat_to_vegetarianism_variation() - 0.003,
        2020,
    ),
    lambda: 1,
    "_smooth_normal_shift_fraction_from_meat_to_vegetarianism",
)


@component.add(
    name="Normal Shift Fraction from Meat to Vegetarianism Variation",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_shift_fraction_from_meat_to_vegetarianism_variation():
    return 0.003


@component.add(
    name="Normal Shift Fraction from Vegetarianism to Meat",
    units="1/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "vm_var_s": 1,
        "_smooth_normal_shift_fraction_from_vegetarianism_to_meat": 1,
    },
    other_deps={
        "_smooth_normal_shift_fraction_from_vegetarianism_to_meat": {
            "initial": {
                "normal_shift_fraction_from_vegetarianism_to_meat_variation": 1,
                "vm_var_s": 1,
                "l_var_t": 1,
                "time": 1,
            },
            "step": {
                "normal_shift_fraction_from_vegetarianism_to_meat_variation": 1,
                "vm_var_s": 1,
                "l_var_t": 1,
                "time": 1,
                "ssp_food_and_diet_variation_time": 1,
            },
        }
    },
)
def normal_shift_fraction_from_vegetarianism_to_meat():
    return vm_var_s() + _smooth_normal_shift_fraction_from_vegetarianism_to_meat()


_smooth_normal_shift_fraction_from_vegetarianism_to_meat = Smooth(
    lambda: step(
        __data["time"],
        normal_shift_fraction_from_vegetarianism_to_meat_variation() - vm_var_s(),
        2020 + l_var_t(),
    ),
    lambda: ssp_food_and_diet_variation_time(),
    lambda: step(
        __data["time"],
        normal_shift_fraction_from_vegetarianism_to_meat_variation() - vm_var_s(),
        2020 + l_var_t(),
    ),
    lambda: 1,
    "_smooth_normal_shift_fraction_from_vegetarianism_to_meat",
)


@component.add(
    name="Normal Shift Fraction from Vegetarianism to Meat Variation",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_shift_fraction_from_vegetarianism_to_meat_variation():
    return 0.01


@component.add(
    name="Outflow PVA",
    units="People",
    subscripts=["Gender", "Cohorts", "Education"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"potential_vegetarians_accumulative": 1},
)
def outflow_pva():
    return potential_vegetarians_accumulative() / 1


@component.add(
    name="Percentage of animal calories",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"diet_composition_percentage": 1},
)
def percentage_of_animal_calories():
    return sum(
        diet_composition_percentage()
        .loc[_subscript_dict["AnimalFood"]]
        .rename({"FoodCategories": "AnimalFood!"}),
        dim=["AnimalFood!"],
    )


@component.add(
    name='"Percentage of meat-based diet followers"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_meat_eaters": 1, "population": 1},
)
def percentage_of_meatbased_diet_followers():
    return total_meat_eaters() / population()


@component.add(
    name="Percentage of Population with Flexitarian Diet from Meat Diet",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "meat_diet_composition_switch": 1,
        "percentage_of_meatbased_diet_followers": 1,
        "target_percentage_of_meat_eaters": 1,
    },
)
def percentage_of_population_with_flexitarian_diet_from_meat_diet():
    return if_then_else(
        meat_diet_composition_switch() == 1,
        lambda: target_percentage_of_meat_eaters()
        * percentage_of_meatbased_diet_followers(),
        lambda: 0,
    )


@component.add(
    name="Percentage of Population with Flexitarian Diet from Vegetarian Diet",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "vegetarian_diet_composition_switch": 1,
        "target_percentage_of_vegetarians": 1,
        "percentage_of_vegetarian_diet_followers": 1,
    },
)
def percentage_of_population_with_flexitarian_diet_from_vegetarian_diet():
    return if_then_else(
        vegetarian_diet_composition_switch() == 2,
        lambda: target_percentage_of_vegetarians()
        * percentage_of_vegetarian_diet_followers(),
        lambda: 0,
    )


@component.add(
    name="Percentage of vegetarian diet followers",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_vegetarians": 1, "population": 1},
)
def percentage_of_vegetarian_diet_followers():
    return total_vegetarians() / population()


@component.add(
    name="Percentage of vegetarians",
    units="Dmnl",
    subscripts=["Gender", "Cohorts", "Education"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lactoovo_vegetarian_diet_followers": 1, "population_wrt_education": 1},
)
def percentage_of_vegetarians():
    return zidz(lactoovo_vegetarian_diet_followers(), population_wrt_education())


@component.add(
    name="Plant Based Diet Followers Indicator",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"percentage_of_vegetarian_diet_followers": 1},
)
def plant_based_diet_followers_indicator():
    return float(np.maximum(0, percentage_of_vegetarian_diet_followers()))


@component.add(
    name="Plant Based Food Caloric Intake per Person",
    units="kcal/(Person*Day)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"average_kcal_intake_per_person": 4},
)
def plant_based_food_caloric_intake_per_person():
    return (
        float(average_kcal_intake_per_person().loc["Pulses"])
        + float(average_kcal_intake_per_person().loc["Grains"])
        + float(average_kcal_intake_per_person().loc["VegFruits"])
        + float(average_kcal_intake_per_person().loc["OtherCrops"])
    )


@component.add(
    name="Population increase rate",
    units="People/Year",
    subscripts=["Gender", "Cohorts", "Education"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "population_wrt_education": 1,
        "previous_population": 1,
        "percentage_of_vegetarians": 1,
    },
)
def population_increase_rate():
    return (
        population_wrt_education() - previous_population()
    ) * percentage_of_vegetarians()


@component.add(
    name="Potential vegetarians",
    units="People",
    subscripts=["Gender", "Cohorts", "Education"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_pva": 1},
)
def potential_vegetarians():
    return outflow_pva()


@component.add(
    name="Potential Vegetarians Accumulative",
    units="People",
    subscripts=["Gender", "Cohorts", "Education"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_potential_vegetarians_accumulative": 1},
    other_deps={
        "_integ_potential_vegetarians_accumulative": {
            "initial": {"initial_meatbased_diet_followers": 1},
            "step": {"inflow_pva": 1, "outflow_pva": 1},
        }
    },
)
def potential_vegetarians_accumulative():
    """
    For coverting DELAY1I function only. Added by Q Ye in July 2024
    """
    return _integ_potential_vegetarians_accumulative()


_integ_potential_vegetarians_accumulative = Integ(
    lambda: inflow_pva() - outflow_pva(),
    lambda: initial_meatbased_diet_followers(),
    "_integ_potential_vegetarians_accumulative",
)


@component.add(
    name="Previous population",
    units="People",
    subscripts=["Gender", "Cohorts", "Education"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_previous_population": 1},
    other_deps={
        "_delayfixed_previous_population": {
            "initial": {"initial_pop_ed": 1},
            "step": {"population_wrt_education": 1},
        }
    },
)
def previous_population():
    return _delayfixed_previous_population()


_delayfixed_previous_population = DelayFixed(
    lambda: population_wrt_education(),
    lambda: 1,
    lambda: initial_pop_ed(),
    time_step,
    "_delayfixed_previous_population",
)


@component.add(
    name="Ratio Young",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"young_population": 1, "population": 1},
)
def ratio_young():
    return young_population() / population()


@component.add(
    name="Reference Daily Caloric Intake",
    units="kcal/(Person*Day)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ci_s": 2, "time": 1, "reference_daily_caloric_intake_variation": 1},
)
def reference_daily_caloric_intake():
    """
    1961 World average, from FAO data - 2194 kcal Calibrated 1672.6 kcal 1970 value, when gdp effect=1:2325
    """
    return ci_s() + ramp(
        __data["time"],
        (reference_daily_caloric_intake_variation() - ci_s()) / 78,
        2022,
        2100,
    )


@component.add(
    name="Reference Daily Caloric Intake Variation",
    units="kcal/(Person*Day)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_daily_caloric_intake_variation():
    """
    1961 World average, from FAO data - 2194 kcal Calibrated 1672.6 kcal 1970 value, when gdp effect=1:2325
    """
    return 1672.6


@component.add(
    name="Reference GWP per Capita",
    units="$/(Year*Person)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_gwp_per_capita():
    """
    GWP per capita in 1961. (Felix model, matches the historical data 1980-2010 well.) 3342.7 Calibrated: 4000
    """
    return 4000


@component.add(
    name="Reference meat diet decomposition multiplier",
    units="Dmnl",
    subscripts=["FoodCategories", "Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_meat_diet_decomposition_multiplier_male": 1,
        "reference_meat_diet_decomposition_multiplier_female": 1,
    },
)
def reference_meat_diet_decomposition_multiplier():
    value = xr.DataArray(
        np.nan,
        {
            "FoodCategories": _subscript_dict["FoodCategories"],
            "Gender": _subscript_dict["Gender"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["FoodCategories", "Gender", "Cohorts"],
    )
    value.loc[:, ["male"], :] = (
        reference_meat_diet_decomposition_multiplier_male()
        .expand_dims({"Gender": ["male"]}, 1)
        .values
    )
    value.loc[:, ["female"], :] = (
        reference_meat_diet_decomposition_multiplier_female()
        .expand_dims({"Gender": ["female"]}, 1)
        .values
    )
    return value


@component.add(
    name="Reference meat diet decomposition multiplier female",
    subscripts=["FoodCategories", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_meat_diet_decomposition_multiplier_female():
    """
    Original data please see the excel file 'New_DietData.xlsx' , 'Model Input' , 'b22' added by Q. Ye in June 2024
    """
    value = xr.DataArray(
        np.nan,
        {
            "FoodCategories": _subscript_dict["FoodCategories"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["FoodCategories", "Cohorts"],
    )
    value.loc[["PasMeat"], :] = xr.DataArray(
        [
            [
                0.0133507,
                0.0169109,
                0.0213612,
                0.0226963,
                0.0244764,
                0.0222512,
                0.0222512,
                0.0222512,
                0.0222512,
                0.0222512,
                0.0200261,
                0.0200261,
                0.0200261,
                0.0200261,
                0.0200261,
                0.0200261,
                0.0200261,
                0.0200261,
                0.0200261,
                0.0200261,
                0.0200261,
            ]
        ],
        {"FoodCategories": ["PasMeat"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["CropMeat"], :] = xr.DataArray(
        [
            [
                0.0417936,
                0.0529386,
                0.0668698,
                0.0710491,
                0.0766216,
                0.069656,
                0.069656,
                0.069656,
                0.069656,
                0.069656,
                0.0626904,
                0.0626904,
                0.0626904,
                0.0626904,
                0.0626904,
                0.0626904,
                0.0626904,
                0.0626904,
                0.0626904,
                0.0626904,
                0.0626904,
            ]
        ],
        {"FoodCategories": ["CropMeat"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Dairy"], :] = xr.DataArray(
        [
            [
                0.0388913,
                0.0492623,
                0.062226,
                0.0661152,
                0.0713007,
                0.0648188,
                0.0648188,
                0.0648188,
                0.0648188,
                0.0648188,
                0.0583369,
                0.0583369,
                0.0583369,
                0.0583369,
                0.0583369,
                0.0583369,
                0.0583369,
                0.0583369,
                0.0583369,
                0.0583369,
                0.0583369,
            ]
        ],
        {"FoodCategories": ["Dairy"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Eggs"], :] = xr.DataArray(
        [
            [
                0.00580467,
                0.00735258,
                0.00928747,
                0.00986794,
                0.0106419,
                0.00967445,
                0.00967445,
                0.00967445,
                0.00967445,
                0.00967445,
                0.008707,
                0.008707,
                0.008707,
                0.008707,
                0.008707,
                0.008707,
                0.008707,
                0.008707,
                0.008707,
                0.008707,
                0.008707,
            ]
        ],
        {"FoodCategories": ["Eggs"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Pulses"], :] = xr.DataArray(
        [
            [
                0.0116093,
                0.0147052,
                0.0185749,
                0.0197359,
                0.0212838,
                0.0193489,
                0.0193489,
                0.0193489,
                0.0193489,
                0.0193489,
                0.017414,
                0.017414,
                0.017414,
                0.017414,
                0.017414,
                0.017414,
                0.017414,
                0.017414,
                0.017414,
                0.017414,
                0.017414,
            ]
        ],
        {"FoodCategories": ["Pulses"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Grains"], :] = xr.DataArray(
        [
            [
                0.271658,
                0.344101,
                0.434654,
                0.461819,
                0.498041,
                0.452764,
                0.452764,
                0.452764,
                0.452764,
                0.452764,
                0.407488,
                0.407488,
                0.407488,
                0.407488,
                0.407488,
                0.407488,
                0.407488,
                0.407488,
                0.407488,
                0.407488,
                0.407488,
            ]
        ],
        {"FoodCategories": ["Grains"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["VegFruits"], :] = xr.DataArray(
        [
            [
                0.0464373,
                0.0588206,
                0.0742998,
                0.0789435,
                0.0851351,
                0.0773956,
                0.0773956,
                0.0773956,
                0.0773956,
                0.0773956,
                0.069656,
                0.069656,
                0.069656,
                0.069656,
                0.069656,
                0.069656,
                0.069656,
                0.069656,
                0.069656,
                0.069656,
                0.069656,
            ]
        ],
        {"FoodCategories": ["VegFruits"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["OtherCrops"], :] = xr.DataArray(
        [
            [
                0.150921,
                0.191167,
                0.241474,
                0.256566,
                0.276689,
                0.251536,
                0.251536,
                0.251536,
                0.251536,
                0.251536,
                0.226382,
                0.226382,
                0.226382,
                0.226382,
                0.226382,
                0.226382,
                0.226382,
                0.226382,
                0.226382,
                0.226382,
                0.226382,
            ]
        ],
        {"FoodCategories": ["OtherCrops"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    return value


@component.add(
    name="Reference meat diet decomposition multiplier male",
    subscripts=["FoodCategories", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_meat_diet_decomposition_multiplier_male():
    """
    Original data please see the excel file 'New_DietData.xlsx' , 'Model Input' , 'b22' added by Q. Ye in June 2024
    """
    value = xr.DataArray(
        np.nan,
        {
            "FoodCategories": _subscript_dict["FoodCategories"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["FoodCategories", "Cohorts"],
    )
    value.loc[["PasMeat"], :] = xr.DataArray(
        [
            [
                0.0140924,
                0.017801,
                0.0235863,
                0.0307067,
                0.0311517,
                0.0289266,
                0.0289266,
                0.0289266,
                0.0289266,
                0.0267015,
                0.0267015,
                0.0267015,
                0.0267015,
                0.0244764,
                0.0244764,
                0.0244764,
                0.0244764,
                0.0244764,
                0.0244764,
                0.0244764,
                0.0244764,
            ]
        ],
        {"FoodCategories": ["PasMeat"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["CropMeat"], :] = xr.DataArray(
        [
            [
                0.0441155,
                0.0557248,
                0.0738354,
                0.0961253,
                0.0975184,
                0.0905528,
                0.0905528,
                0.0905528,
                0.0905528,
                0.0835872,
                0.0835872,
                0.0835872,
                0.0835872,
                0.0766216,
                0.0766216,
                0.0766216,
                0.0766216,
                0.0766216,
                0.0766216,
                0.0766216,
                0.0766216,
            ]
        ],
        {"FoodCategories": ["CropMeat"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Dairy"], :] = xr.DataArray(
        [
            [
                0.0410519,
                0.051855,
                0.0687079,
                0.0894499,
                0.0907463,
                0.0842644,
                0.0842644,
                0.0842644,
                0.0842644,
                0.0777826,
                0.0777826,
                0.0777826,
                0.0777826,
                0.0713007,
                0.0713007,
                0.0713007,
                0.0713007,
                0.0713007,
                0.0713007,
                0.0713007,
                0.0713007,
            ]
        ],
        {"FoodCategories": ["Dairy"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Eggs"], :] = xr.DataArray(
        [
            [
                0.00612715,
                0.00773956,
                0.0102549,
                0.0133507,
                0.0135442,
                0.0125768,
                0.0125768,
                0.0125768,
                0.0125768,
                0.0116093,
                0.0116093,
                0.0116093,
                0.0116093,
                0.0106419,
                0.0106419,
                0.0106419,
                0.0106419,
                0.0106419,
                0.0106419,
                0.0106419,
                0.0106419,
            ]
        ],
        {"FoodCategories": ["Eggs"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Pulses"], :] = xr.DataArray(
        [
            [
                0.0122543,
                0.0154791,
                0.0205098,
                0.0267015,
                0.0270885,
                0.0251536,
                0.0251536,
                0.0251536,
                0.0251536,
                0.0232187,
                0.0232187,
                0.0232187,
                0.0232187,
                0.0212838,
                0.0212838,
                0.0212838,
                0.0212838,
                0.0212838,
                0.0212838,
                0.0212838,
                0.0212838,
            ]
        ],
        {"FoodCategories": ["Pulses"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Grains"], :] = xr.DataArray(
        [
            [
                0.286751,
                0.362211,
                0.47993,
                0.624815,
                0.63387,
                0.588593,
                0.588593,
                0.588593,
                0.588593,
                0.543317,
                0.543317,
                0.543317,
                0.543317,
                0.498041,
                0.498041,
                0.498041,
                0.498041,
                0.498041,
                0.498041,
                0.498041,
                0.498041,
            ]
        ],
        {"FoodCategories": ["Grains"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["VegFruits"], :] = xr.DataArray(
        [
            [
                0.0490172,
                0.0619165,
                0.0820393,
                0.106806,
                0.108354,
                0.100614,
                0.100614,
                0.100614,
                0.100614,
                0.0928747,
                0.0928747,
                0.0928747,
                0.0928747,
                0.0851351,
                0.0851351,
                0.0851351,
                0.0851351,
                0.0851351,
                0.0851351,
                0.0851351,
                0.0851351,
            ]
        ],
        {"FoodCategories": ["VegFruits"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["OtherCrops"], :] = xr.DataArray(
        [
            [
                0.159306,
                0.201228,
                0.266628,
                0.347119,
                0.35215,
                0.326996,
                0.326996,
                0.326996,
                0.326996,
                0.301843,
                0.301843,
                0.301843,
                0.301843,
                0.276689,
                0.276689,
                0.276689,
                0.276689,
                0.276689,
                0.276689,
                0.276689,
                0.276689,
            ]
        ],
        {"FoodCategories": ["OtherCrops"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    return value


@component.add(
    name="Reference vegetarian diet decomposition multiplier",
    units="Dmnl",
    subscripts=["FoodCategories", "Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_vegetarian_diet_decomposition_multiplier_male": 1,
        "reference_vegetarian_diet_decomposition_multiplier_female": 1,
    },
)
def reference_vegetarian_diet_decomposition_multiplier():
    value = xr.DataArray(
        np.nan,
        {
            "FoodCategories": _subscript_dict["FoodCategories"],
            "Gender": _subscript_dict["Gender"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["FoodCategories", "Gender", "Cohorts"],
    )
    value.loc[:, ["male"], :] = (
        reference_vegetarian_diet_decomposition_multiplier_male()
        .expand_dims({"Gender": ["male"]}, 1)
        .values
    )
    value.loc[:, ["female"], :] = (
        reference_vegetarian_diet_decomposition_multiplier_female()
        .expand_dims({"Gender": ["female"]}, 1)
        .values
    )
    return value


@component.add(
    name="Reference vegetarian diet decomposition multiplier female",
    subscripts=["FoodCategories", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_vegetarian_diet_decomposition_multiplier_female():
    """
    Original data please see the excel file 'New_DietData.xlsx' , 'Model Input' , 'b48' Added by Q. Ye in June 2024
    """
    value = xr.DataArray(
        np.nan,
        {
            "FoodCategories": _subscript_dict["FoodCategories"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["FoodCategories", "Cohorts"],
    )
    value.loc[["PasMeat"], :] = 0
    value.loc[["CropMeat"], :] = 0
    value.loc[["Dairy"], :] = xr.DataArray(
        [
            [
                0.0406327,
                0.0514681,
                0.0650123,
                0.0690756,
                0.0744932,
                0.0677211,
                0.0677211,
                0.0677211,
                0.0677211,
                0.0677211,
                0.060949,
                0.060949,
                0.060949,
                0.060949,
                0.060949,
                0.060949,
                0.060949,
                0.060949,
                0.060949,
                0.060949,
                0.060949,
            ]
        ],
        {"FoodCategories": ["Dairy"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Eggs"], :] = xr.DataArray(
        [
            [
                0.0116093,
                0.0147052,
                0.0185749,
                0.0197359,
                0.0212838,
                0.0193489,
                0.0193489,
                0.0193489,
                0.0193489,
                0.0193489,
                0.017414,
                0.017414,
                0.017414,
                0.017414,
                0.017414,
                0.017414,
                0.017414,
                0.017414,
                0.017414,
                0.017414,
                0.017414,
            ]
        ],
        {"FoodCategories": ["Eggs"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Pulses"], :] = xr.DataArray(
        [
            [
                0.0220577,
                0.0279398,
                0.0352924,
                0.0374982,
                0.0404392,
                0.0367629,
                0.0367629,
                0.0367629,
                0.0367629,
                0.0367629,
                0.0330866,
                0.0330866,
                0.0330866,
                0.0330866,
                0.0330866,
                0.0330866,
                0.0330866,
                0.0330866,
                0.0330866,
                0.0330866,
                0.0330866,
            ]
        ],
        {"FoodCategories": ["Pulses"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Grains"], :] = xr.DataArray(
        [
            [
                0.301843,
                0.382334,
                0.482948,
                0.513133,
                0.553378,
                0.503071,
                0.503071,
                0.503071,
                0.503071,
                0.503071,
                0.452764,
                0.452764,
                0.452764,
                0.452764,
                0.452764,
                0.452764,
                0.452764,
                0.452764,
                0.452764,
                0.452764,
                0.452764,
            ]
        ],
        {"FoodCategories": ["Grains"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["VegFruits"], :] = xr.DataArray(
        [
            [
                0.0534029,
                0.0676437,
                0.0854447,
                0.090785,
                0.0979054,
                0.0890049,
                0.0890049,
                0.0890049,
                0.0890049,
                0.0890049,
                0.0801044,
                0.0801044,
                0.0801044,
                0.0801044,
                0.0801044,
                0.0801044,
                0.0801044,
                0.0801044,
                0.0801044,
                0.0801044,
                0.0801044,
            ]
        ],
        {"FoodCategories": ["VegFruits"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["OtherCrops"], :] = xr.DataArray(
        [
            [
                0.150921,
                0.191167,
                0.241474,
                0.256566,
                0.276689,
                0.251536,
                0.251536,
                0.251536,
                0.251536,
                0.251536,
                0.226382,
                0.226382,
                0.226382,
                0.226382,
                0.226382,
                0.226382,
                0.226382,
                0.226382,
                0.226382,
                0.226382,
                0.226382,
            ]
        ],
        {"FoodCategories": ["OtherCrops"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    return value


@component.add(
    name="Reference vegetarian diet decomposition multiplier male",
    subscripts=["FoodCategories", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_vegetarian_diet_decomposition_multiplier_male():
    """
    Original data please see the excel file 'New_DietData.xlsx' , 'Model Input' , 'b48' Added by Q. Ye in June 2024
    """
    value = xr.DataArray(
        np.nan,
        {
            "FoodCategories": _subscript_dict["FoodCategories"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["FoodCategories", "Cohorts"],
    )
    value.loc[["PasMeat"], :] = 0
    value.loc[["CropMeat"], :] = 0
    value.loc[["Dairy"], :] = xr.DataArray(
        [
            [
                0.04289,
                0.0541769,
                0.0717844,
                0.0934552,
                0.0948096,
                0.0880375,
                0.0880375,
                0.0880375,
                0.0880375,
                0.0812654,
                0.0812654,
                0.0812654,
                0.0812654,
                0.0744932,
                0.0744932,
                0.0744932,
                0.0744932,
                0.0744932,
                0.0744932,
                0.0744932,
                0.0744932,
            ]
        ],
        {"FoodCategories": ["Dairy"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Eggs"], :] = xr.DataArray(
        [
            [
                0.0122543,
                0.0154791,
                0.0205098,
                0.0267015,
                0.0270885,
                0.0251536,
                0.0251536,
                0.0251536,
                0.0251536,
                0.0232187,
                0.0232187,
                0.0232187,
                0.0232187,
                0.0212838,
                0.0212838,
                0.0212838,
                0.0212838,
                0.0212838,
                0.0212838,
                0.0212838,
                0.0212838,
            ]
        ],
        {"FoodCategories": ["Eggs"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Pulses"], :] = xr.DataArray(
        [
            [
                0.0232832,
                0.0294103,
                0.0389687,
                0.0507328,
                0.0514681,
                0.0477918,
                0.0477918,
                0.0477918,
                0.0477918,
                0.0441155,
                0.0441155,
                0.0441155,
                0.0441155,
                0.0404392,
                0.0404392,
                0.0404392,
                0.0404392,
                0.0404392,
                0.0404392,
                0.0404392,
                0.0404392,
            ]
        ],
        {"FoodCategories": ["Pulses"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Grains"], :] = xr.DataArray(
        [
            [
                0.318612,
                0.402457,
                0.533256,
                0.694238,
                0.7043,
                0.653993,
                0.653993,
                0.653993,
                0.653993,
                0.603685,
                0.603685,
                0.603685,
                0.603685,
                0.553378,
                0.553378,
                0.553378,
                0.553378,
                0.553378,
                0.553378,
                0.553378,
                0.553378,
            ]
        ],
        {"FoodCategories": ["Grains"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["VegFruits"], :] = xr.DataArray(
        [
            [
                0.0563698,
                0.0712039,
                0.0943452,
                0.122827,
                0.124607,
                0.115706,
                0.115706,
                0.115706,
                0.115706,
                0.106806,
                0.106806,
                0.106806,
                0.106806,
                0.0979054,
                0.0979054,
                0.0979054,
                0.0979054,
                0.0979054,
                0.0979054,
                0.0979054,
                0.0979054,
            ]
        ],
        {"FoodCategories": ["VegFruits"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["OtherCrops"], :] = xr.DataArray(
        [
            [
                0.159306,
                0.201228,
                0.266628,
                0.347119,
                0.35215,
                0.326996,
                0.326996,
                0.326996,
                0.326996,
                0.301843,
                0.301843,
                0.301843,
                0.301843,
                0.276689,
                0.276689,
                0.276689,
                0.276689,
                0.276689,
                0.276689,
                0.276689,
                0.276689,
            ]
        ],
        {"FoodCategories": ["OtherCrops"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    return value


@component.add(
    name="Relative GWP per Capita",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"smoothed_gwp_per_capita": 1, "reference_gwp_per_capita": 1},
)
def relative_gwp_per_capita():
    return smoothed_gwp_per_capita() / reference_gwp_per_capita()


@component.add(
    name="Response efficacy multiplier",
    units="Dmnl",
    subscripts=["Education"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "response_efficacy_multiplier_noed_variation": 1,
        "time": 4,
        "response_efficacy_multiplier_primary_variation": 1,
        "response_efficacy_multiplier_secondary_variation": 1,
        "response_efficacy_multiplier_tertiary_variation": 1,
    },
)
def response_efficacy_multiplier():
    """
    Base: 0.8, 0.9, 1, 1.2
    """
    value = xr.DataArray(
        np.nan, {"Education": _subscript_dict["Education"]}, ["Education"]
    )
    value.loc[["noEd"]] = 0.8 + step(
        __data["time"], response_efficacy_multiplier_noed_variation() - 0.8, 2020
    )
    value.loc[["primary"]] = 0.9 + step(
        __data["time"], response_efficacy_multiplier_primary_variation() - 0.9, 2020
    )
    value.loc[["secondary"]] = 1 + step(
        __data["time"], response_efficacy_multiplier_secondary_variation() - 1, 2020
    )
    value.loc[["tertiary"]] = 1.2 + step(
        __data["time"], response_efficacy_multiplier_tertiary_variation() - 1.2, 2020
    )
    return value


@component.add(
    name="Response Efficacy Multiplier NoEd Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def response_efficacy_multiplier_noed_variation():
    """
    Base: 0.8, 0.9, 1, 1.2
    """
    return 0.8


@component.add(
    name="Response Efficacy Multiplier Primary Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def response_efficacy_multiplier_primary_variation():
    """
    Base: 0.8, 0.9, 1, 1.2
    """
    return 0.9


@component.add(
    name="Response Efficacy Multiplier Secondary Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def response_efficacy_multiplier_secondary_variation():
    """
    Base: 0.8, 0.9, 1, 1.2
    """
    return 1


@component.add(
    name="Response Efficacy Multiplier Tertiary Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def response_efficacy_multiplier_tertiary_variation():
    """
    Base: 0.8, 0.9, 1, 1.2
    """
    return 1.2


@component.add(
    name="Response Efficacy Multiplier Variation",
    units="Dmnl",
    subscripts=["Education"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def response_efficacy_multiplier_variation():
    """
    Base: 0.8, 0.9, 1, 1.2
    """
    return xr.DataArray(
        [0.8, 0.9, 1.0, 1.2], {"Education": _subscript_dict["Education"]}, ["Education"]
    )


@component.add(
    name="SA k risk attitude", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def sa_k_risk_attitude():
    return 0.9


@component.add(
    name="SA k social norm",
    units="Dmnl",
    subscripts=["PrimaryEdButOldest"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_k_social_norm():
    value = xr.DataArray(
        np.nan,
        {"PrimaryEdButOldest": _subscript_dict["PrimaryEdButOldest"]},
        ["PrimaryEdButOldest"],
    )
    value.loc[['"10-14"']] = 5
    value.loc[['"20-24"']] = 8
    value.loc[['"40-44"']] = 8
    value.loc[['"80-84"']] = 5
    return value


@component.add(
    name="SA L risk attitude", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def sa_l_risk_attitude():
    return 2


@component.add(
    name="SA L social norm",
    units="Dmnl",
    subscripts=["PrimaryEdButOldest"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_l_social_norm():
    """
    1.7
    """
    value = xr.DataArray(
        np.nan,
        {"PrimaryEdButOldest": _subscript_dict["PrimaryEdButOldest"]},
        ["PrimaryEdButOldest"],
    )
    value.loc[['"10-14"']] = 1.2
    value.loc[['"20-24"']] = 1.5
    value.loc[['"40-44"']] = 1.5
    value.loc[['"80-84"']] = 1.2
    return value


@component.add(
    name="SA x0 risk attitude",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_x0_risk_attitude():
    return 5


@component.add(
    name="SA x0 social norm",
    units="Dmnl",
    subscripts=["PrimaryEdButOldest"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_x0_social_norm():
    """
    20-24: .35 40-44 : .5
    """
    value = xr.DataArray(
        np.nan,
        {"PrimaryEdButOldest": _subscript_dict["PrimaryEdButOldest"]},
        ["PrimaryEdButOldest"],
    )
    value.loc[['"10-14"']] = 0.6
    value.loc[['"20-24"']] = 0.45
    value.loc[['"40-44"']] = 0.55
    value.loc[['"80-84"']] = 0.7
    return value


@component.add(
    name="Self efficacy multiplier",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "self_efficacy_multiplier_male_variation": 1,
        "time": 2,
        "self_efficacy_multiplier_female_variation": 1,
    },
)
def self_efficacy_multiplier():
    """
    Is it also dependent on age?
    """
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["male"]] = 0.8 + step(
        __data["time"], self_efficacy_multiplier_male_variation() - 0.8, 2020
    )
    value.loc[["female"]] = 1.2 + step(
        __data["time"], self_efficacy_multiplier_female_variation() - 1.2, 2020
    )
    return value


@component.add(
    name="Self Efficacy Multiplier Female Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def self_efficacy_multiplier_female_variation():
    """
    Is it also dependent on age?
    """
    return 1.2


@component.add(
    name="Self Efficacy Multiplier Male Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def self_efficacy_multiplier_male_variation():
    """
    Is it also dependent on age?
    """
    return 0.8


@component.add(
    name="Self Efficacy Multiplier Variation",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def self_efficacy_multiplier_variation():
    """
    Is it also dependent on age?
    """
    return xr.DataArray([0.8, 1.2], {"Gender": _subscript_dict["Gender"]}, ["Gender"])


@component.add(
    name="Shift fraction of meat eaters to vegetarianism",
    units="1/Year",
    subscripts=["Gender", "Cohorts", "Education"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_shift_fraction_from_meat_to_vegetarianism": 1,
        "fraction_intended_to_change_diet": 1,
        "self_efficacy_multiplier": 1,
        "response_efficacy_multiplier": 1,
    },
)
def shift_fraction_of_meat_eaters_to_vegetarianism():
    """
    *Personal willingness multiplier for diet shift[Gender,Cohorts,Education]*Social impact multiplier for diet shift[Gender,Cohorts,Education]
    """
    return (
        normal_shift_fraction_from_meat_to_vegetarianism()
        + fraction_intended_to_change_diet()
        * response_efficacy_multiplier()
        * self_efficacy_multiplier()
    ).transpose("Gender", "Cohorts", "Education")


@component.add(
    name="Shift Fraction Vegetarians to Meat",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_shift_fraction_from_vegetarianism_to_meat": 1,
        "effect_of_gwp_on_meat_consumption": 1,
    },
)
def shift_fraction_vegetarians_to_meat():
    return (
        normal_shift_fraction_from_vegetarianism_to_meat()
        * effect_of_gwp_on_meat_consumption()
    )


@component.add(
    name='"Shift from meat-based to vegetarian"',
    units="People/Year",
    subscripts=["Gender", "Cohorts", "Education"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "potential_vegetarians": 1,
        "shift_fraction_of_meat_eaters_to_vegetarianism": 1,
    },
)
def shift_from_meatbased_to_vegetarian():
    return potential_vegetarians() * shift_fraction_of_meat_eaters_to_vegetarianism()


@component.add(
    name='"Shift from vegetarian to meat-based"',
    units="People/Year",
    subscripts=["Gender", "Cohorts", "Education"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "shift_fraction_vegetarians_to_meat": 1,
        "lactoovo_vegetarian_diet_followers": 1,
    },
)
def shift_from_vegetarian_to_meatbased():
    return shift_fraction_vegetarians_to_meat() * lactoovo_vegetarian_diet_followers()


@component.add(
    name="Smooth Diet Switch Fnc",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def smooth_diet_switch_fnc():
    return np.interp(
        time(),
        [
            2020.0,
            2023.0,
            2026.0,
            2029.0,
            2032.0,
            2035.0,
            2038.0,
            2041.0,
            2044.0,
            2047.0,
            2050.0,
        ],
        [0.0, 0.02, 0.05, 0.15, 0.3, 0.5, 0.7, 0.85, 0.95, 0.98, 1.0],
    )


@component.add(
    name="Start Year of Meat Diet Switch",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def start_year_of_meat_diet_switch():
    return 2020


@component.add(
    name="Start Year of Vegetarian Diet Switch",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def start_year_of_vegetarian_diet_switch():
    return 2020


@component.add(
    name="Subjective norm multiplier for diet change",
    units="Dmnl",
    subscripts=["Gender", "Cohorts", "Education"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "l_social_norm": 1,
        "percentage_of_vegetarians": 1,
        "x0_social_norm": 1,
        "k_social_norm": 1,
    },
)
def subjective_norm_multiplier_for_diet_change():
    return (
        l_social_norm()
        / (
            1
            + np.exp(
                (-k_social_norm())
                * (percentage_of_vegetarians() - x0_social_norm()).transpose(
                    "Cohorts", "Gender", "Education"
                )
            )
        )
    ).transpose("Gender", "Cohorts", "Education")


@component.add(
    name="Sum of diet followers",
    units="People",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_vegetarians": 1, "total_meat_eaters": 1},
)
def sum_of_diet_followers():
    return total_vegetarians() + total_meat_eaters()


@component.add(
    name="SWITCH Alternative Protein Scenario",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def switch_alternative_protein_scenario():
    """
    0 : No alternative protein scenario is taken into acocunt 1 : Global average diet composition includes alternative proteins, and multiplied by the total population, hence no dietary shifts
    """
    return 0


@component.add(
    name="Target Percentage of Meat Eaters",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def target_percentage_of_meat_eaters():
    return 1


@component.add(
    name="Target Percentage of Vegetarians",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def target_percentage_of_vegetarians():
    return 1


@component.add(
    name="Total eater value cohort",
    units="People",
    subscripts=["Gender", "Cohorts", "Education"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lactoovo_vegetarian_diet_followers": 1, "meatbased_diet_followers": 1},
)
def total_eater_value_cohort():
    return lactoovo_vegetarian_diet_followers() + meatbased_diet_followers()


@component.add(
    name="Total Kcal Intake per Person AP",
    units="kcal/(Person*Day)",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_kcal_intake_per_person_from_conventional_food": 1,
        "average_kcal_intake_per_person_from_alternative_proteins": 1,
    },
)
def total_kcal_intake_per_person_ap():
    return (
        average_kcal_intake_per_person_from_conventional_food()
        + average_kcal_intake_per_person_from_alternative_proteins()
    )


@component.add(
    name="Total Meat Eaters",
    units="People",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_meat_eaters_by_gender": 1},
)
def total_meat_eaters():
    return sum(
        total_meat_eaters_by_gender().rename({"Gender": "Gender!"}), dim=["Gender!"]
    )


@component.add(
    name="Total Meat Eaters by Gender",
    units="People",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"meatbased_diet_followers": 1},
)
def total_meat_eaters_by_gender():
    return sum(
        meatbased_diet_followers().rename(
            {"Cohorts": "Cohorts!", "Education": "Education!"}
        ),
        dim=["Cohorts!", "Education!"],
    )


@component.add(
    name='"Total shift from meat-based to vegetarian diet"',
    units="People/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"shift_from_meatbased_to_vegetarian": 1},
)
def total_shift_from_meatbased_to_vegetarian_diet():
    return sum(
        shift_from_meatbased_to_vegetarian().rename(
            {"Gender": "Gender!", "Cohorts": "Cohorts!", "Education": "Education!"}
        ),
        dim=["Gender!", "Cohorts!", "Education!"],
    )


@component.add(
    name="Total Vegetarians",
    units="People",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_vegetarians_by_gender": 1},
)
def total_vegetarians():
    return sum(
        total_vegetarians_by_gender().rename({"Gender": "Gender!"}), dim=["Gender!"]
    )


@component.add(
    name="Total Vegetarians by Gender",
    units="People",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lactoovo_vegetarian_diet_followers": 1},
)
def total_vegetarians_by_gender():
    return sum(
        lactoovo_vegetarian_diet_followers().rename(
            {"Cohorts": "Cohorts!", "Education": "Education!"}
        ),
        dim=["Cohorts!", "Education!"],
    )


@component.add(
    name="Unit feedstock demand for alternative proteins",
    units="Ton/Ton",
    subscripts=["AltProteins", "AltProteinTech", "PlantFood"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def unit_feedstock_demand_for_alternative_proteins():
    """
    This parameter represents the crop demand of each alternative protein (replacing beef, pork, poultry, eggs, milk) by each AP technology. For cultivated meat, only PasMeat and CropMeat can be replaced, requiring soybeans and corn. For precision fermentation, all can be replaced, requiring only sugar cane. For plant-based alternatives, all except eggs are replaced, based on average recipes. See "New_DietData.xlsx/Alt protein type vs tech" for the estimation of these parameters and their uncertainty ranges.
    """
    value = xr.DataArray(
        np.nan,
        {
            "AltProteins": _subscript_dict["AltProteins"],
            "AltProteinTech": _subscript_dict["AltProteinTech"],
            "PlantFood": _subscript_dict["PlantFood"],
        },
        ["AltProteins", "AltProteinTech", "PlantFood"],
    )
    value.loc[:, ["PrecFerm"], ["OtherCrops"]] = xr.DataArray(
        [[[4.725]], [[4.725]], [[4.725]], [[4.725]]],
        {
            "AltProteins": _subscript_dict["AltProteins"],
            "AltProteinTech": ["PrecFerm"],
            "PlantFood": ["OtherCrops"],
        },
        ["AltProteins", "AltProteinTech", "PlantFood"],
    ).values
    value.loc[:, ["Cult"], ["Grains"]] = 0.483
    value.loc[["AltPasMeat"], ["Plant"], :] = xr.DataArray(
        [[[0.36, 0.0, 2.804, 0.414]]],
        {
            "AltProteins": ["AltPasMeat"],
            "AltProteinTech": ["Plant"],
            "PlantFood": _subscript_dict["PlantFood"],
        },
        ["AltProteins", "AltProteinTech", "PlantFood"],
    ).values
    value.loc[:, ["PrecFerm"], _subscript_dict["AllPlantButOther"]] = 0
    value.loc[:, ["Cult"], _subscript_dict["PlantsPulsesVeg"]] = 0
    value.loc[["AltCropMeat"], ["Plant"], :] = xr.DataArray(
        [[[0.14, 0.0, 0.0, 0.504]]],
        {
            "AltProteins": ["AltCropMeat"],
            "AltProteinTech": ["Plant"],
            "PlantFood": _subscript_dict["PlantFood"],
        },
        ["AltProteins", "AltProteinTech", "PlantFood"],
    ).values
    value.loc[["AltDairy"], ["Plant"], :] = xr.DataArray(
        [[[0.0, 0.0, 0.0, 0.137]]],
        {
            "AltProteins": ["AltDairy"],
            "AltProteinTech": ["Plant"],
            "PlantFood": _subscript_dict["PlantFood"],
        },
        ["AltProteins", "AltProteinTech", "PlantFood"],
    ).values
    value.loc[["AltEggs"], ["Plant"], :] = 0
    value.loc[:, ["Cult"], ["OtherCrops"]] = 0.5
    return value


@component.add(
    name="Variable Smooth Meat Diet Switch Fnc",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "end_year_of_meat_diet_switch": 3,
        "start_year_of_meat_diet_switch": 4,
        "time": 2,
    },
)
def variable_smooth_meat_diet_switch_fnc():
    """
    Logistic Curve
    """
    return if_then_else(
        end_year_of_meat_diet_switch() - start_year_of_meat_diet_switch() > 0,
        lambda: 1
        / (
            1
            + float(
                np.exp(
                    -10
                    / (
                        end_year_of_meat_diet_switch()
                        - start_year_of_meat_diet_switch()
                    )
                    * (
                        time()
                        - (
                            start_year_of_meat_diet_switch()
                            + end_year_of_meat_diet_switch()
                        )
                        / 2
                    )
                )
            )
        ),
        lambda: step(__data["time"], 1, start_year_of_meat_diet_switch()),
    )


@component.add(
    name="Variable Smooth Vegetarian Diet Switch Fnc",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "end_year_of_vegetarian_diet_switch": 3,
        "start_year_of_vegetarian_diet_switch": 4,
        "time": 2,
    },
)
def variable_smooth_vegetarian_diet_switch_fnc():
    """
    Logistic Curve
    """
    return if_then_else(
        end_year_of_vegetarian_diet_switch() - start_year_of_vegetarian_diet_switch()
        > 0,
        lambda: 1
        / (
            1
            + float(
                np.exp(
                    -10
                    / (
                        end_year_of_vegetarian_diet_switch()
                        - start_year_of_vegetarian_diet_switch()
                    )
                    * (
                        time()
                        - (
                            start_year_of_vegetarian_diet_switch()
                            + end_year_of_vegetarian_diet_switch()
                        )
                        / 2
                    )
                )
            )
        ),
        lambda: step(__data["time"], 1, start_year_of_vegetarian_diet_switch()),
    )


@component.add(
    name="Vegan diet decomposition multiplier",
    units="Dmnl",
    subscripts=["FoodCategories", "Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "vegan_diet_decomposition_multiplier_male": 1,
        "vegan_diet_decomposition_multiplier_female": 1,
    },
)
def vegan_diet_decomposition_multiplier():
    value = xr.DataArray(
        np.nan,
        {
            "FoodCategories": _subscript_dict["FoodCategories"],
            "Gender": _subscript_dict["Gender"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["FoodCategories", "Gender", "Cohorts"],
    )
    value.loc[:, ["male"], :] = (
        vegan_diet_decomposition_multiplier_male()
        .expand_dims({"Gender": ["male"]}, 1)
        .values
    )
    value.loc[:, ["female"], :] = (
        vegan_diet_decomposition_multiplier_female()
        .expand_dims({"Gender": ["female"]}, 1)
        .values
    )
    return value


@component.add(
    name="Vegan diet decomposition multiplier female",
    subscripts=["FoodCategories", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def vegan_diet_decomposition_multiplier_female():
    """
    Original data please see the excel file 'New_DietData.xlsx' , 'Model Input' , 'y48' Added by Q. Ye in June 2024
    """
    value = xr.DataArray(
        np.nan,
        {
            "FoodCategories": _subscript_dict["FoodCategories"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["FoodCategories", "Cohorts"],
    )
    value.loc[["PasMeat"], :] = 0
    value.loc[["CropMeat"], :] = 0
    value.loc[["Dairy"], :] = 0
    value.loc[["Eggs"], :] = 0
    value.loc[["Pulses"], :] = xr.DataArray(
        [
            [
                0.058047,
                0.073526,
                0.092875,
                0.098679,
                0.106419,
                0.096744,
                0.096744,
                0.096744,
                0.096744,
                0.096744,
                0.08707,
                0.08707,
                0.08707,
                0.08707,
                0.08707,
                0.08707,
                0.08707,
                0.08707,
                0.08707,
                0.08707,
                0.08707,
            ]
        ],
        {"FoodCategories": ["Pulses"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Grains"], :] = xr.DataArray(
        [
            [
                0.17414,
                0.220577,
                0.278624,
                0.296038,
                0.319257,
                0.290233,
                0.290233,
                0.290233,
                0.290233,
                0.290233,
                0.26121,
                0.26121,
                0.26121,
                0.26121,
                0.26121,
                0.26121,
                0.26121,
                0.26121,
                0.26121,
                0.26121,
                0.26121,
            ]
        ],
        {"FoodCategories": ["Grains"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["VegFruits"], :] = xr.DataArray(
        [
            [
                0.116093,
                0.147052,
                0.185749,
                0.197359,
                0.212838,
                0.193489,
                0.193489,
                0.193489,
                0.193489,
                0.193489,
                0.17414,
                0.17414,
                0.17414,
                0.17414,
                0.17414,
                0.17414,
                0.17414,
                0.17414,
                0.17414,
                0.17414,
                0.17414,
            ]
        ],
        {"FoodCategories": ["VegFruits"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["OtherCrops"], :] = xr.DataArray(
        [
            [
                0.232187,
                0.294103,
                0.371499,
                0.394717,
                0.425676,
                0.386978,
                0.386978,
                0.386978,
                0.386978,
                0.386978,
                0.34828,
                0.34828,
                0.34828,
                0.34828,
                0.34828,
                0.34828,
                0.34828,
                0.34828,
                0.34828,
                0.34828,
                0.34828,
            ]
        ],
        {"FoodCategories": ["OtherCrops"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    return value


@component.add(
    name="Vegan diet decomposition multiplier male",
    subscripts=["FoodCategories", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def vegan_diet_decomposition_multiplier_male():
    """
    Original data please see the excel file 'New_DietData.xlsx' , 'Model Input' , 'y48' Added by Q. Ye in June 2024
    """
    value = xr.DataArray(
        np.nan,
        {
            "FoodCategories": _subscript_dict["FoodCategories"],
            "Cohorts": _subscript_dict["Cohorts"],
        },
        ["FoodCategories", "Cohorts"],
    )
    value.loc[["PasMeat"], :] = 0
    value.loc[["CropMeat"], :] = 0
    value.loc[["Dairy"], :] = 0
    value.loc[["Eggs"], :] = 0
    value.loc[["Pulses"], :] = xr.DataArray(
        [
            [
                0.061271,
                0.077396,
                0.102549,
                0.133507,
                0.135442,
                0.125768,
                0.125768,
                0.125768,
                0.125768,
                0.116093,
                0.116093,
                0.116093,
                0.116093,
                0.106419,
                0.106419,
                0.106419,
                0.106419,
                0.106419,
                0.106419,
                0.106419,
                0.106419,
            ]
        ],
        {"FoodCategories": ["Pulses"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["Grains"], :] = xr.DataArray(
        [
            [
                0.183814,
                0.232187,
                0.307647,
                0.400522,
                0.406327,
                0.377303,
                0.377303,
                0.377303,
                0.377303,
                0.34828,
                0.34828,
                0.34828,
                0.34828,
                0.319257,
                0.319257,
                0.319257,
                0.319257,
                0.319257,
                0.319257,
                0.319257,
                0.319257,
            ]
        ],
        {"FoodCategories": ["Grains"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["VegFruits"], :] = xr.DataArray(
        [
            [
                0.122543,
                0.154791,
                0.205098,
                0.267015,
                0.270885,
                0.251536,
                0.251536,
                0.251536,
                0.251536,
                0.232187,
                0.232187,
                0.232187,
                0.232187,
                0.212838,
                0.212838,
                0.212838,
                0.212838,
                0.212838,
                0.212838,
                0.212838,
                0.212838,
            ]
        ],
        {"FoodCategories": ["VegFruits"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    value.loc[["OtherCrops"], :] = xr.DataArray(
        [
            [
                0.245086,
                0.309582,
                0.410197,
                0.534029,
                0.541769,
                0.503071,
                0.503071,
                0.503071,
                0.503071,
                0.464373,
                0.464373,
                0.464373,
                0.464373,
                0.425676,
                0.425676,
                0.425676,
                0.425676,
                0.425676,
                0.425676,
                0.425676,
                0.425676,
            ]
        ],
        {"FoodCategories": ["OtherCrops"], "Cohorts": _subscript_dict["Cohorts"]},
        ["FoodCategories", "Cohorts"],
    ).values
    return value


@component.add(
    name="Vegetarian diet composition multipliers",
    units="Dmnl",
    subscripts=["FoodCategories", "Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_vegetarian_diet_decomposition_multiplier": 4,
        "variable_smooth_vegetarian_diet_switch_fnc": 1,
        "target_percentage_of_vegetarians": 1,
        "flexitarian_diet_decomposition_multiplier": 1,
        "vegetarian_diet_composition_switch": 3,
        "vegan_diet_decomposition_multiplier": 1,
    },
)
def vegetarian_diet_composition_multipliers():
    """
    0 = Ref 1 = Vegan 2 = Flexitarian
    """
    return (
        reference_vegetarian_diet_decomposition_multiplier()
        + variable_smooth_vegetarian_diet_switch_fnc()
        * target_percentage_of_vegetarians()
        * (
            if_then_else(
                vegetarian_diet_composition_switch() == 0,
                lambda: reference_vegetarian_diet_decomposition_multiplier(),
                lambda: if_then_else(
                    vegetarian_diet_composition_switch() == 1,
                    lambda: vegan_diet_decomposition_multiplier(),
                    lambda: if_then_else(
                        vegetarian_diet_composition_switch() == 2,
                        lambda: flexitarian_diet_decomposition_multiplier(),
                        lambda: reference_vegetarian_diet_decomposition_multiplier(),
                    ),
                ),
            )
            - reference_vegetarian_diet_decomposition_multiplier()
        )
    )


@component.add(
    name="Vegetarian Diet Composition Switch",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def vegetarian_diet_composition_switch():
    return 0


@component.add(name="VM S", units="1/Year", comp_type="Constant", comp_subtype="Normal")
def vm_s():
    return 0.01


@component.add(
    name="VM Var S",
    units="1/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_vm_var_s": 1},
    other_deps={
        "_smooth_vm_var_s": {
            "initial": {"vm_s": 1, "time": 1},
            "step": {"vm_s": 1, "time": 1},
        }
    },
)
def vm_var_s():
    return 0.01 + _smooth_vm_var_s()


_smooth_vm_var_s = Smooth(
    lambda: step(__data["time"], vm_s() - 0.01, 2020),
    lambda: 1,
    lambda: step(__data["time"], vm_s() - 0.01, 2020),
    lambda: 1,
    "_smooth_vm_var_s",
)


@component.add(
    name="x0 risk attitude",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_x0_risk_attitude": 1, "time": 1},
)
def x0_risk_attitude():
    return 5 + step(__data["time"], sa_x0_risk_attitude() - 5, 2020)


@component.add(
    name="x0 social norm",
    units="Dmnl",
    subscripts=["Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_x0_social_norm": 4, "time": 4},
)
def x0_social_norm():
    value = xr.DataArray(np.nan, {"Cohorts": _subscript_dict["Cohorts"]}, ["Cohorts"])
    value.loc[_subscript_dict["Childhood"]] = 0.6 + step(
        __data["time"], float(sa_x0_social_norm().loc['"10-14"']) - 0.6, 2020
    )
    value.loc[_subscript_dict["Young"]] = 0.45 + step(
        __data["time"], float(sa_x0_social_norm().loc['"20-24"']) - 0.45, 2020
    )
    value.loc[_subscript_dict["MiddleAged"]] = 0.55 + step(
        __data["time"], float(sa_x0_social_norm().loc['"40-44"']) - 0.55, 2020
    )
    value.loc[_subscript_dict["OldAge"]] = 0.7 + step(
        __data["time"], float(sa_x0_social_norm().loc['"80-84"']) - 0.7, 2020
    )
    return value


@component.add(
    name="Year2050", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def year2050():
    return 2050


@component.add(
    name="Young population",
    units="People",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_cohorts": 1},
)
def young_population():
    return sum(
        population_cohorts()
        .loc[:, _subscript_dict["Young"]]
        .rename({"Gender": "Gender!", "Cohorts": "Young!"}),
        dim=["Gender!", "Young!"],
    )
