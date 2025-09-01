"""
Module fertilizer_use
Translated using PySD version 3.14.3
"""

@component.add(
    name="a price", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def a_price():
    """
    Calibrated
    """
    return 2


@component.add(
    name="a price sensitivity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def a_price_sensitivity():
    return 1.5


@component.add(
    name="a reserve", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def a_reserve():
    return 3


@component.add(
    name="a reserve sensitivity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def a_reserve_sensitivity():
    return 10


@component.add(
    name="Area Harvested Accumulative",
    units="ha",
    subscripts=["PlantFood"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_area_harvested_accumulative": 1},
    other_deps={
        "_integ_area_harvested_accumulative": {
            "initial": {"init_aha": 1},
            "step": {"inflow_aha": 1, "outflow_aha": 1},
        }
    },
)
def area_harvested_accumulative():
    return _integ_area_harvested_accumulative()


_integ_area_harvested_accumulative = Integ(
    lambda: inflow_aha() - outflow_aha(),
    lambda: init_aha(),
    "_integ_area_harvested_accumulative",
)


@component.add(
    name="Average N content",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def average_n_content():
    return xr.DataArray(
        [0.0289, 0.0148, 0.0051, 0.0201, 0.036, 0.0155, 0.0021, 0.0113],
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )


@component.add(
    name="Average P content",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def average_p_content():
    return xr.DataArray(
        [0.0016, 0.0009, 0.0009, 0.002, 0.0037, 0.0023, 0.0004, 0.0016],
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )


@component.add(
    name="Average P demand rate",
    units="Ton/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_average_p_demand_rate": 1},
    other_deps={
        "_smooth_average_p_demand_rate": {
            "initial": {},
            "step": {"desired_phosphate_rock_production_rate": 1},
        }
    },
)
def average_p_demand_rate():
    return _smooth_average_p_demand_rate()


_smooth_average_p_demand_rate = Smooth(
    lambda: desired_phosphate_rock_production_rate(),
    lambda: 5,
    lambda: 30350000.0,
    lambda: 1,
    "_smooth_average_p_demand_rate",
)


@component.add(
    name="b price", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def b_price():
    """
    Calibrated, 0.09
    """
    return 0.35


@component.add(
    name="b price sensitivity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def b_price_sensitivity():
    return 0.5


@component.add(
    name="b reserve", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def b_reserve():
    return 1.5


@component.add(
    name="b reserve sensitivity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def b_reserve_sensitivity():
    return 2


@component.add(
    name="Commercial N application for agriculture",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_nitrogen_consumption_2010": 1,
        "effect_of_income_on_fertilizer_use": 1,
        "effect_of_technology_on_fertilizer_consumption": 1,
        "effect_of_land_availability_on_fertilizer_use": 1,
    },
)
def commercial_n_application_for_agriculture():
    """
    Application of N fertilizers, aligning with the "agricultural use" of "total nutrient nitrogen" in the FAO database.
    """
    return (
        reference_nitrogen_consumption_2010()
        * effect_of_income_on_fertilizer_use()
        * effect_of_technology_on_fertilizer_consumption()
        * effect_of_land_availability_on_fertilizer_use()
    )


@component.add(
    name="Commercial N application for each category",
    units="Ton/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "commercial_n_application_for_agriculture": 2,
        "n_fertilizer_shares_normalized": 2,
    },
)
def commercial_n_application_for_each_category():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = (
        commercial_n_application_for_agriculture()
        * n_fertilizer_shares_normalized()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
    ).values
    value.loc[["PasMeat"]] = commercial_n_application_for_agriculture() * float(
        n_fertilizer_shares_normalized().loc["PasMeat"]
    )
    return value


@component.add(
    name="Commercial Nitrogen Application per ha",
    units="Ton/(ha*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"commercial_n_application_for_agriculture": 1, "agricultural_land": 1},
)
def commercial_nitrogen_application_per_ha():
    return commercial_n_application_for_agriculture() / agricultural_land()


@component.add(
    name="Commercial P2O5 application for agriculture",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"p2o5_demand_from_agriculture": 1, "p2o5_supply_for_agriculture": 1},
)
def commercial_p2o5_application_for_agriculture():
    return float(
        np.minimum(p2o5_demand_from_agriculture(), p2o5_supply_for_agriculture())
    )


@component.add(
    name="Commercial P application for agriculture",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "commercial_p2o5_application_for_agriculture": 1,
        "p2o5_to_p_conversion_factor": 1,
    },
)
def commercial_p_application_for_agriculture():
    """
    The amount of elemental P in the applied P2O5 fertilizers
    """
    return commercial_p2o5_application_for_agriculture() * p2o5_to_p_conversion_factor()


@component.add(
    name="Commercial P application for each category",
    units="Ton/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "commercial_p_application_for_agriculture": 2,
        "p_fertilizer_shares_normalized": 2,
    },
)
def commercial_p_application_for_each_category():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = (
        commercial_p_application_for_agriculture()
        * p_fertilizer_shares_normalized()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
    ).values
    value.loc[["PasMeat"]] = commercial_p_application_for_agriculture() * float(
        p_fertilizer_shares_normalized().loc["PasMeat"]
    )
    return value


@component.add(
    name="Commercial Phosphorus Application per ha",
    units="Ton/(ha*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "commercial_p2o5_application_for_agriculture": 1,
        "agricultural_land": 1,
    },
)
def commercial_phosphorus_application_per_ha():
    return commercial_p2o5_application_for_agriculture() / agricultural_land()


@component.add(
    name="Delayed area harvested",
    units="ha",
    subscripts=["PlantFood"],
    comp_type="Stateful",
    comp_subtype="DelayFixed",
    depends_on={"_delayfixed_delayed_area_harvested": 1},
    other_deps={
        "_delayfixed_delayed_area_harvested": {
            "initial": {"initial_area_harvested": 1},
            "step": {"area_harvested": 1},
        }
    },
)
def delayed_area_harvested():
    return _delayfixed_delayed_area_harvested()


_delayfixed_delayed_area_harvested = DelayFixed(
    lambda: area_harvested(),
    lambda: 1,
    lambda: initial_area_harvested(),
    time_step,
    "_delayfixed_delayed_area_harvested",
)


@component.add(
    name="Denitrification fraction",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def denitrification_fraction():
    """
    Denitrification rate is the rate of nitrate that is released back to the atmosphere. Ammonium also vaporizes. In this case, this flow covers both! The value is calibrated according to the "Denitrification Rate" data and estimates in Reay et al. 2012 and Mosier 2000. BASE:0.087
    """
    return 0.087


@component.add(
    name="Denitrification Rate",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nitrogen": 1, "denitrification_fraction": 1},
)
def denitrification_rate():
    return nitrogen() * denitrification_fraction()


@component.add(
    name="deposition",
    units="Ton/(Year*ha)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def deposition():
    """
    Depositing atmosheric N in the soil, e.g. by legumes. Excluded for now.
    """
    return 0


@component.add(
    name="Desired P205 production rate",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effect_of_price_on_p_production": 1, "total_p205_demand": 1},
)
def desired_p205_production_rate():
    return effect_of_price_on_p_production() * total_p205_demand()


@component.add(
    name="Desired phosphate rock production rate",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_p205_production_rate": 1, "p2o5_content_in_phosphate_rock": 1},
)
def desired_phosphate_rock_production_rate():
    return desired_p205_production_rate() / p2o5_content_in_phosphate_rock()


@component.add(
    name="Discovery amount", units="Ton", comp_type="Constant", comp_subtype="Normal"
)
def discovery_amount():
    """
    4.5e+010
    """
    return 45000000000.0


@component.add(
    name="Discovery amount sensitivity",
    units="Ton",
    comp_type="Constant",
    comp_subtype="Normal",
)
def discovery_amount_sensitivity():
    return 20000000000.0


@component.add(
    name="Discovery year", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def discovery_year():
    return 2010


@component.add(
    name="Effect of fertilizer on yield",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"effect_of_n_on_yield_2": 2, "effect_of_p_on_yield_2": 2},
)
def effect_of_fertilizer_on_yield():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = np.minimum(
        effect_of_n_on_yield_2()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"}),
        effect_of_p_on_yield_2()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"}),
    ).values
    value.loc[["PasMeat"]] = float(
        np.minimum(
            float(effect_of_n_on_yield_2().loc["PasMeat"]),
            float(effect_of_p_on_yield_2().loc["PasMeat"]),
        )
    )
    return value


@component.add(
    name="Effect of Income on Fertilizer Use",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "l_gwp_fert": 1,
        "relative_gwp_per_capita": 1,
        "x0_gwp_fert": 1,
        "k_gwp_fert": 1,
    },
)
def effect_of_income_on_fertilizer_use():
    """
    L gwp fert / (1 + EXP(-k gwp fert * (Relative GWP per Capita - x0 gwp fert)) )
    """
    return l_gwp_fert() / (
        1 + float(np.exp(-k_gwp_fert() * (relative_gwp_per_capita() - x0_gwp_fert())))
    )


@component.add(
    name="Effect of Income on Fertilizer Use LOOKUP",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_effect_of_income_on_fertilizer_use_lookup"
    },
)
def effect_of_income_on_fertilizer_use_lookup(x, final_subs=None):
    return _hardcodedlookup_effect_of_income_on_fertilizer_use_lookup(x, final_subs)


_hardcodedlookup_effect_of_income_on_fertilizer_use_lookup = HardcodedLookups(
    [0.0, 0.4, 1.0, 1.88, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
    [0.0, 0.1, 0.5, 1.0, 1.05, 1.25, 1.35, 1.42, 1.47, 1.5, 1.5, 1.5, 1.5],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_effect_of_income_on_fertilizer_use_lookup",
)


@component.add(
    name="Effect of Land Availability on Fertilizer Use",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "l_land_fert": 1,
        "x0_land_fert": 1,
        "k_land_fert": 1,
        "relative_demsupply_ratio_agrland": 1,
    },
)
def effect_of_land_availability_on_fertilizer_use():
    """
    L land fert / ( 1 + EXP(-k land fert * (Relative DemSupply Ratio AgrLand - x0 land fert)) )
    """
    return l_land_fert() / (
        1
        + float(
            np.exp(
                -k_land_fert() * (relative_demsupply_ratio_agrland() - x0_land_fert())
            )
        )
    )


@component.add(
    name="Effect of Land Availability on Fertilizer UseLOOKUP",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_effect_of_land_availability_on_fertilizer_uselookup"
    },
)
def effect_of_land_availability_on_fertilizer_uselookup(x, final_subs=None):
    return _hardcodedlookup_effect_of_land_availability_on_fertilizer_uselookup(
        x, final_subs
    )


_hardcodedlookup_effect_of_land_availability_on_fertilizer_uselookup = HardcodedLookups(
    [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0],
    [0.0, 0.2, 0.45, 0.75, 1.0, 1.25, 1.4, 1.45, 1.5],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_effect_of_land_availability_on_fertilizer_uselookup",
)


@component.add(
    name="Effect of N on Yield 2",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "l_fertilizer": 2,
        "n_ratio_applied_to_reference": 2,
        "x0_fertilizer": 2,
        "k_fertilizer": 2,
    },
)
def effect_of_n_on_yield_2():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = (
        l_fertilizer()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        / (
            1
            + np.exp(
                -k_fertilizer()
                .loc[_subscript_dict["PlantFood"]]
                .rename({"FoodCategories": "PlantFood"})
                * (
                    n_ratio_applied_to_reference()
                    .loc[_subscript_dict["PlantFood"]]
                    .rename({"FoodCategories": "PlantFood"})
                    - x0_fertilizer()
                    .loc[_subscript_dict["PlantFood"]]
                    .rename({"FoodCategories": "PlantFood"})
                )
            )
        )
    ).values
    value.loc[["PasMeat"]] = float(l_fertilizer().loc["PasMeat"]) / (
        1
        + float(
            np.exp(
                -float(k_fertilizer().loc["PasMeat"])
                * (
                    float(n_ratio_applied_to_reference().loc["PasMeat"])
                    - float(x0_fertilizer().loc["PasMeat"])
                )
            )
        )
    )
    return value


@component.add(
    name="Effect of P on Yield 2",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "l_fertilizer": 2,
        "x0_fertilizer": 2,
        "p_ratio_applied_to_reference": 2,
        "k_fertilizer": 2,
    },
)
def effect_of_p_on_yield_2():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = (
        l_fertilizer()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        / (
            1
            + np.exp(
                -k_fertilizer()
                .loc[_subscript_dict["PlantFood"]]
                .rename({"FoodCategories": "PlantFood"})
                * (
                    p_ratio_applied_to_reference()
                    .loc[_subscript_dict["PlantFood"]]
                    .rename({"FoodCategories": "PlantFood"})
                    - x0_fertilizer()
                    .loc[_subscript_dict["PlantFood"]]
                    .rename({"FoodCategories": "PlantFood"})
                )
            )
        )
    ).values
    value.loc[["PasMeat"]] = float(l_fertilizer().loc["PasMeat"]) / (
        1
        + float(
            np.exp(
                -float(k_fertilizer().loc["PasMeat"])
                * (
                    float(p_ratio_applied_to_reference().loc["PasMeat"])
                    - float(x0_fertilizer().loc["PasMeat"])
                )
            )
        )
    )
    return value


@component.add(
    name="Effect of price on P production",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"a_price": 1, "relative_p_price": 1, "b_price": 1},
)
def effect_of_price_on_p_production():
    return a_price() * float(np.exp(-b_price() * relative_p_price()))


@component.add(
    name="Effect of reserves on P price",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "a_reserve": 1,
        "b_reserve": 1,
        "initial_p_reserve_production_ratio": 1,
        "reserve_demand_ratio": 1,
    },
)
def effect_of_reserves_on_p_price():
    return a_reserve() * float(
        np.exp(
            -b_reserve()
            * (reserve_demand_ratio() / initial_p_reserve_production_ratio())
        )
    )


@component.add(
    name="Effect of scarcity on P production",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={
        "phosphate_rock_proven_reserves": 1,
        "desired_phosphate_rock_production_rate": 1,
    },
)
def effect_of_scarcity_on_p_production():
    return np.interp(
        phosphate_rock_proven_reserves() / desired_phosphate_rock_production_rate(),
        [0.0, 0.5, 1.0, 1.5, 2.0],
        [0.0, 0.5, 0.9, 0.95, 1.0],
    )


@component.add(
    name="Effect of Technology on Fertilizer Consumption",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "k_tech_fert": 1, "l_tech_fert": 1, "x0_tech_fert": 1},
)
def effect_of_technology_on_fertilizer_consumption():
    """
    MAKE IT 1+ (L / ....)
    """
    return if_then_else(
        time() < 2020,
        lambda: 1,
        lambda: l_tech_fert()
        / (1 + float(np.exp(-k_tech_fert() * ((time() - 2020) - x0_tech_fert())))),
    )


@component.add(
    name="Inflow AHA",
    units="ha",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"area_harvested": 1},
)
def inflow_aha():
    return area_harvested()


@component.add(
    name="Init AHA",
    units="ha",
    subscripts=["PlantFood"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_aha():
    return xr.DataArray(
        [2.19830e07, 2.83354e08, 4.06016e07, 6.32654e07],
        {"PlantFood": _subscript_dict["PlantFood"]},
        ["PlantFood"],
    )


@component.add(
    name="INIT P proven reserves",
    units="Ton",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_p_proven_reserves():
    return 16000000000.0


@component.add(
    name="Initial Area harvested",
    units="ha",
    subscripts=["PlantFood"],
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_initial_area_harvested": 1},
    other_deps={
        "_initial_initial_area_harvested": {
            "initial": {"area_harvested": 1},
            "step": {},
        }
    },
)
def initial_area_harvested():
    return _initial_initial_area_harvested()


_initial_initial_area_harvested = Initial(
    lambda: area_harvested(), "_initial_initial_area_harvested"
)


@component.add(
    name="Initial Mobile Nitrogen",
    units="Ton",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_mobile_nitrogen():
    return 0


@component.add(
    name="Initial P reserve production ratio",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_p_reserve_production_ratio():
    """
    265, 527
    """
    return 527


@component.add(
    name="Initial Phosphorus", units="Ton", comp_type="Constant", comp_subtype="Normal"
)
def initial_phosphorus():
    return 500000


@component.add(
    name="k fertilizer",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={"sa_k_fertilizer": 4, "time": 4},
)
def k_fertilizer():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[["Pulses"]] = 0.2 + step(
        __data["time"], float(sa_k_fertilizer().loc["Pulses"]) - 0.2, 2020
    )
    value.loc[["PasMeat"]] = 1
    value.loc[["Grains"]] = 0.8 + step(
        __data["time"], float(sa_k_fertilizer().loc["Grains"]) - 0.8, 2020
    )
    value.loc[["VegFruits"]] = 0.25 + step(
        __data["time"], float(sa_k_fertilizer().loc["VegFruits"]) - 0.25, 2020
    )
    value.loc[["OtherCrops"]] = 1 + step(
        __data["time"], float(sa_k_fertilizer().loc["OtherCrops"]) - 1, 2020
    )
    return value


@component.add(
    name="k gwp fert", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def k_gwp_fert():
    """
    1.5 3 + STEP(SA k gwp fert-3, 2020)
    """
    return 3.85


@component.add(
    name="k land fert",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_k_land_fert": 1, "time": 1},
)
def k_land_fert():
    return 1.6 + step(__data["time"], sa_k_land_fert() - 1.6, 2020)


@component.add(
    name="k tech fert", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def k_tech_fert():
    return 0


@component.add(
    name="L fertilizer",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={"sa_l_fertilizer": 4, "time": 4},
)
def l_fertilizer():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[["Pulses"]] = 1.56 + step(
        __data["time"], float(sa_l_fertilizer().loc["Pulses"]) - 1.56, 2020
    )
    value.loc[["PasMeat"]] = 1.8
    value.loc[["Grains"]] = 1.6 + step(
        __data["time"], float(sa_l_fertilizer().loc["Grains"]) - 1.6, 2020
    )
    value.loc[["VegFruits"]] = 1.5 + step(
        __data["time"], float(sa_l_fertilizer().loc["VegFruits"]) - 1.5, 2020
    )
    value.loc[["OtherCrops"]] = 2.5 + step(
        __data["time"], float(sa_l_fertilizer().loc["OtherCrops"]) - 2.5, 2020
    )
    return value


@component.add(
    name="L gwp fert", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def l_gwp_fert():
    """
    Calibrated simultaneously for Eff of GWP and Eff of Land. See FertilizerLookups.xlsx/Calibration... 1.25 + STEP(SA L gwp fert-1.25, 2020)
    """
    return 1.25206


@component.add(
    name="L land fert",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_l_land_fert": 1, "time": 1},
)
def l_land_fert():
    return 2.2 + step(__data["time"], sa_l_land_fert() - 2.2, 2020)


@component.add(
    name="L tech fert", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def l_tech_fert():
    return 2


@component.add(
    name="mineralization",
    units="Ton/(Year*ha)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def mineralization():
    """
    with the degradation of organic matter in soil. Excluded from this model for now.
    """
    return 0


@component.add(
    name="N application per ha",
    units="Ton/(Year*ha)",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "commercial_n_application_for_each_category": 2,
        "delayed_area_harvested": 1,
        "grassland_allocated_for_food_production": 1,
    },
)
def n_application_per_ha():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = (
        commercial_n_application_for_each_category()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        / delayed_area_harvested()
    ).values
    value.loc[["PasMeat"]] = (
        float(commercial_n_application_for_each_category().loc["PasMeat"])
        / grassland_allocated_for_food_production()
    )
    return value


@component.add(
    name="N fertilizer shares",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={"n_fertilizer_shares_data": 1, "time": 1, "sa_n_fertilizer_shares": 1},
)
def n_fertilizer_shares():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = (
        n_fertilizer_shares_data()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        * (1 + step(__data["time"], sa_n_fertilizer_shares() - 1, 2020))
    ).values
    value.loc[["PasMeat"]] = 0.047
    return value


@component.add(
    name="N fertilizer shares2",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={
        "n_fertilizer_shares_data": 3,
        "time": 2,
        "sa_n_fertilizer_shares": 2,
        "n_fertilizer_shares2": 4,
    },
)
def n_fertilizer_shares2():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[["Grains"]] = float(n_fertilizer_shares_data().loc["Grains"]) * (
        1
        + step(__data["time"], float(sa_n_fertilizer_shares().loc["Grains"]) - 1, 2020)
    )
    value.loc[["PasMeat"]] = 0.047
    value.loc[["OtherCrops"]] = float(n_fertilizer_shares_data().loc["OtherCrops"]) * (
        1
        + step(
            __data["time"], float(sa_n_fertilizer_shares().loc["OtherCrops"]) - 1, 2020
        )
    )
    value.loc[["VegFruits"]] = 1 - (
        float(n_fertilizer_shares2().loc["Grains"])
        + float(n_fertilizer_shares2().loc["Pulses"])
        + float(n_fertilizer_shares2().loc["OtherCrops"])
        + float(n_fertilizer_shares2().loc["PasMeat"])
    )
    value.loc[["Pulses"]] = float(n_fertilizer_shares_data().loc["Pulses"])
    return value


@component.add(
    name="N fertilizer shares Data",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def n_fertilizer_shares_data():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = xr.DataArray(
        [0.083, 0.559, 0.155, 0.155],
        {"FoodCategories": _subscript_dict["PlantFood"]},
        ["FoodCategories"],
    ).values
    value.loc[["PasMeat"]] = 0.047
    return value


@component.add(
    name="N fertilizer shares normalized",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n_fertilizer_shares": 6},
)
def n_fertilizer_shares_normalized():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = (
        n_fertilizer_shares()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        / (
            sum(
                n_fertilizer_shares()
                .loc[_subscript_dict["PlantFood"]]
                .rename({"FoodCategories": "PlantFood!"}),
                dim=["PlantFood!"],
            )
            + float(n_fertilizer_shares().loc["PasMeat"])
        )
    ).values
    value.loc[["PasMeat"]] = float(n_fertilizer_shares().loc["PasMeat"]) / (
        sum(
            n_fertilizer_shares()
            .loc[_subscript_dict["PlantFood"]]
            .rename({"FoodCategories": "PlantFood!"}),
            dim=["PlantFood!"],
        )
        + float(n_fertilizer_shares().loc["PasMeat"])
    )
    return value


@component.add(
    name="N leaching and runoff fraction",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_n_leaching_and_runoff_fraction": 1, "time": 1},
)
def n_leaching_and_runoff_fraction():
    """
    Nitrate washed away. Especially going to the rivers and lakes. Runoff is 23% of "applied" N, not the stock as I use her. Leaching is around 12-15 M ton/year. In total, 46 M ton/year. The fraction is calibrated accordingly.
    """
    return 0.8 + step(__data["time"], sa_n_leaching_and_runoff_fraction() - 0.8, 2020)


@component.add(
    name="n per ha",
    units="Ton/(ha*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "commercial_n_application_for_agriculture": 1,
        "total_area_harvested": 1,
    },
)
def n_per_ha():
    return commercial_n_application_for_agriculture() / total_area_harvested()


@component.add(
    name='"N produced in the manure of crop-based animals"',
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "unit_n_production_via_manure_crop_based": 1,
        "production_rate_of_animal_food": 2,
    },
)
def n_produced_in_the_manure_of_cropbased_animals():
    return unit_n_production_via_manure_crop_based() * (
        float(production_rate_of_animal_food().loc["CropMeat"])
        + float(production_rate_of_animal_food().loc["Eggs"])
    )


@component.add(
    name='"N produced in the manure of pasture-based animals"',
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "unit_n_production_via_manure_pasture_based": 1,
        "production_rate_of_animal_food": 2,
    },
)
def n_produced_in_the_manure_of_pasturebased_animals():
    return unit_n_production_via_manure_pasture_based() * (
        float(production_rate_of_animal_food().loc["PasMeat"])
        + float(production_rate_of_animal_food().loc["Dairy"])
    )


@component.add(
    name="N ratio applied to reference",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n_application_per_ha": 2, "reference_n_uptake_per_ha": 2},
)
def n_ratio_applied_to_reference():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = (
        n_application_per_ha()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        / reference_n_uptake_per_ha()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
    ).values
    value.loc[["PasMeat"]] = float(n_application_per_ha().loc["PasMeat"]) / float(
        reference_n_uptake_per_ha().loc["PasMeat"]
    )
    return value


@component.add(
    name="N Uptake for crop type",
    units="Ton/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"average_n_content": 2, "food_production_rate": 2},
)
def n_uptake_for_crop_type():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = (
        average_n_content()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        * food_production_rate()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
    ).values
    value.loc[["PasMeat"]] = float(food_production_rate().loc["PasMeat"]) * float(
        average_n_content().loc["PasMeat"]
    )
    return value


@component.add(
    name="N use efficiency",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_n_uptake_rate": 1},
)
def n_use_efficiency():
    return 0 * total_n_uptake_rate()


@component.add(
    name="Nitrogen",
    units="Ton",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_nitrogen": 1},
    other_deps={
        "_integ_nitrogen": {
            "initial": {"initial_mobile_nitrogen": 1},
            "step": {
                "commercial_n_application_for_agriculture": 1,
                "deposition": 1,
                "mineralization": 1,
                "nitrogen_application_with_manure": 1,
                "denitrification_rate": 1,
                "nitrogen_leaching_and_runoff_rate": 1,
                "total_n_uptake_rate": 1,
            },
        }
    },
)
def nitrogen():
    """
    "Mobile" elemental nitrogen in soil.
    """
    return _integ_nitrogen()


_integ_nitrogen = Integ(
    lambda: commercial_n_application_for_agriculture()
    + deposition()
    + mineralization()
    + nitrogen_application_with_manure()
    - denitrification_rate()
    - nitrogen_leaching_and_runoff_rate()
    - total_n_uptake_rate(),
    lambda: initial_mobile_nitrogen(),
    "_integ_nitrogen",
)


@component.add(
    name="Nitrogen application with manure",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "recoverable_n_generated_in_crop_based_manure": 1,
        "recoverable_n_generated_in_pasture_based_manure": 1,
    },
)
def nitrogen_application_with_manure():
    return (
        recoverable_n_generated_in_crop_based_manure()
        + recoverable_n_generated_in_pasture_based_manure()
    )


@component.add(
    name="Nitrogen Leaching and Runoff Rate",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nitrogen": 1, "n_leaching_and_runoff_fraction": 1},
)
def nitrogen_leaching_and_runoff_rate():
    return nitrogen() * n_leaching_and_runoff_fraction()


@component.add(
    name="NTotal P produced in manure",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "n_produced_in_the_manure_of_cropbased_animals": 1,
        "n_produced_in_the_manure_of_pasturebased_animals": 1,
    },
)
def ntotal_p_produced_in_manure():
    return (
        n_produced_in_the_manure_of_cropbased_animals()
        + n_produced_in_the_manure_of_pasturebased_animals()
    )


@component.add(
    name="Outflow AHA",
    subscripts=["PlantFood"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "inflow_aha": 1, "area_harvested_accumulative": 1},
)
def outflow_aha():
    return if_then_else(
        time() == 1900, lambda: inflow_aha(), lambda: area_harvested_accumulative()
    )


@component.add(
    name="P2O5 agriculture fraction",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def p2o5_agriculture_fraction():
    """
    Based on the FAO consumption andproduction data, on average (2002-2015) 10% of production is for other uses, 90% for agriculture. See P_Prod_Cons_FAOSTAT_data_5-3-2018.csv
    """
    return 0.9


@component.add(
    name="P2O5 content in phosphate rock",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def p2o5_content_in_phosphate_rock():
    """
    This is the average ratio of P205 content in the total global phosphate rock produced between 2011 and 2015. Based on USGS data. See USGS_p_ROCKmyb1-2015-phosp.xlx
    """
    return 0.306


@component.add(
    name="P2O5 demand from agriculture",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_phosphate_consumption_2010": 1,
        "effect_of_income_on_fertilizer_use": 1,
        "effect_of_technology_on_fertilizer_consumption": 1,
        "effect_of_land_availability_on_fertilizer_use": 1,
    },
)
def p2o5_demand_from_agriculture():
    return (
        reference_phosphate_consumption_2010()
        * effect_of_income_on_fertilizer_use()
        * effect_of_technology_on_fertilizer_consumption()
        * effect_of_land_availability_on_fertilizer_use()
    )


@component.add(
    name="P2O5 production rate",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"p_rock_production_rate": 1, "p2o5_content_in_phosphate_rock": 1},
)
def p2o5_production_rate():
    """
    P205 content
    """
    return p_rock_production_rate() * p2o5_content_in_phosphate_rock()


@component.add(
    name="P2O5 supply for agriculture",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"p2o5_agriculture_fraction": 1, "p2o5_production_rate": 1},
)
def p2o5_supply_for_agriculture():
    return p2o5_agriculture_fraction() * p2o5_production_rate()


@component.add(
    name="P2O5 to P conversion factor",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def p2o5_to_p_conversion_factor():
    """
    Found on Researchgate. Check with Lei! (https://www.researchgate.net/post/How_to_calculate_phosphorous_from_P2O5_w hich_has_been_recommended_at_the_standard_dose_of_45_kg_ha)
    """
    return 0.4364


@component.add(
    name="P application per ha",
    units="Ton/(Year*ha)",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "commercial_p_application_for_each_category": 2,
        "area_harvested": 1,
        "grassland_allocated_for_food_production": 1,
    },
)
def p_application_per_ha():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = (
        commercial_p_application_for_each_category()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        / area_harvested()
    ).values
    value.loc[["PasMeat"]] = (
        float(commercial_p_application_for_each_category().loc["PasMeat"])
        / grassland_allocated_for_food_production()
    )
    return value


@component.add(
    name="P budget",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "commercial_p_application_for_agriculture": 1,
        "phosphorus_application_with_manure": 1,
        "phosphorus_erosion_leaching_and_runoff_rate": 1,
        "total_p_uptake_rate": 1,
    },
)
def p_budget():
    return (
        commercial_p_application_for_agriculture()
        + phosphorus_application_with_manure()
        - phosphorus_erosion_leaching_and_runoff_rate()
        - total_p_uptake_rate()
    )


@component.add(
    name="P cost", units="$/Ton", comp_type="Constant", comp_subtype="Normal"
)
def p_cost():
    return 60


@component.add(
    name="P discovery rate",
    units="Ton/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_p_discovery_rate": 1},
    other_deps={
        "_smooth_p_discovery_rate": {
            "initial": {"discovery_amount": 1, "time": 1, "discovery_year": 1},
            "step": {"discovery_amount": 1, "time": 1, "discovery_year": 1},
        }
    },
)
def p_discovery_rate():
    return _smooth_p_discovery_rate()


_smooth_p_discovery_rate = Smooth(
    lambda: discovery_amount() * pulse(__data["time"], discovery_year(), width=1),
    lambda: 2,
    lambda: discovery_amount() * pulse(__data["time"], discovery_year(), width=1),
    lambda: 1,
    "_smooth_p_discovery_rate",
)


@component.add(
    name="P fertilizer shares",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={"p_fertilizer_shares_data": 1, "time": 1, "sa_p_fertilizer_shares": 1},
)
def p_fertilizer_shares():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = (
        p_fertilizer_shares_data()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        * (
            1
            + step(
                __data["time"],
                sa_p_fertilizer_shares()
                .loc[_subscript_dict["PlantFood"]]
                .rename({"FoodCategories": "PlantFood"})
                - 1,
                2020,
            )
        )
    ).values
    value.loc[["PasMeat"]] = 0.04
    return value


@component.add(
    name="P fertilizer shares Data",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def p_fertilizer_shares_data():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = xr.DataArray(
        [0.067, 0.446, 0.212, 0.235],
        {"FoodCategories": _subscript_dict["PlantFood"]},
        ["FoodCategories"],
    ).values
    value.loc[["PasMeat"]] = 0.04
    return value


@component.add(
    name="P fertilizer shares normalized",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"p_fertilizer_shares": 6},
)
def p_fertilizer_shares_normalized():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = (
        p_fertilizer_shares()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        / (
            sum(
                p_fertilizer_shares()
                .loc[_subscript_dict["PlantFood"]]
                .rename({"FoodCategories": "PlantFood!"}),
                dim=["PlantFood!"],
            )
            + float(p_fertilizer_shares().loc["PasMeat"])
        )
    ).values
    value.loc[["PasMeat"]] = float(p_fertilizer_shares().loc["PasMeat"]) / (
        sum(
            p_fertilizer_shares()
            .loc[_subscript_dict["PlantFood"]]
            .rename({"FoodCategories": "PlantFood!"}),
            dim=["PlantFood!"],
        )
        + float(p_fertilizer_shares().loc["PasMeat"])
    )
    return value


@component.add(
    name="P leaching fraction",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_p_leaching_fraction": 1, "time": 1},
)
def p_leaching_fraction():
    """
    When parameter: 0.25 Calibrated: 0.06
    """
    return 0.3 + step(__data["time"], sa_p_leaching_fraction() - 0.3, 2020)


@component.add(
    name="P loss to inputs",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "phosphorus_erosion_leaching_and_runoff_rate": 1,
        "phosphorus_application_with_manure": 1,
        "commercial_p_application_for_agriculture": 1,
    },
)
def p_loss_to_inputs():
    return phosphorus_erosion_leaching_and_runoff_rate() / (
        phosphorus_application_with_manure()
        + commercial_p_application_for_agriculture()
    )


@component.add(
    name="P price",
    units="$/Ton",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"p_cost": 1, "p_price_margin": 1, "_smooth_p_price": 1},
    other_deps={
        "_smooth_p_price": {
            "initial": {"effect_of_reserves_on_p_price": 1},
            "step": {"effect_of_reserves_on_p_price": 1},
        }
    },
)
def p_price():
    return p_cost() * p_price_margin() * _smooth_p_price()


_smooth_p_price = Smooth(
    lambda: effect_of_reserves_on_p_price(),
    lambda: 3,
    lambda: effect_of_reserves_on_p_price(),
    lambda: 1,
    "_smooth_p_price",
)


@component.add(
    name="P price margin", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def p_price_margin():
    return 1.1


@component.add(
    name='"P produced in the manure of crop-based animals"',
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "unit_p_production_via_manure_crop_based": 1,
        "production_rate_of_animal_food": 2,
    },
)
def p_produced_in_the_manure_of_cropbased_animals():
    return unit_p_production_via_manure_crop_based() * (
        float(production_rate_of_animal_food().loc["CropMeat"])
        + float(production_rate_of_animal_food().loc["Eggs"])
    )


@component.add(
    name='"P produced in the manure of pasture-based animals"',
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "unit_p_production_via_manure_pasture_based": 1,
        "production_rate_of_animal_food": 2,
    },
)
def p_produced_in_the_manure_of_pasturebased_animals():
    return unit_p_production_via_manure_pasture_based() * (
        float(production_rate_of_animal_food().loc["PasMeat"])
        + float(production_rate_of_animal_food().loc["Dairy"])
    )


@component.add(
    name="P production rate FAO",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"p_rock_production_rate": 1},
)
def p_production_rate_fao():
    return p_rock_production_rate()


@component.add(
    name="P ratio applied to reference",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"p_application_per_ha": 2, "reference_p_uptake_rate_per_ha": 2},
)
def p_ratio_applied_to_reference():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = (
        p_application_per_ha()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        / reference_p_uptake_rate_per_ha()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
    ).values
    value.loc[["PasMeat"]] = float(p_application_per_ha().loc["PasMeat"]) / float(
        reference_p_uptake_rate_per_ha().loc["PasMeat"]
    )
    return value


@component.add(
    name="P rock production rate",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "desired_phosphate_rock_production_rate": 1,
        "effect_of_scarcity_on_p_production": 1,
    },
)
def p_rock_production_rate():
    return (
        desired_phosphate_rock_production_rate() * effect_of_scarcity_on_p_production()
    )


@component.add(
    name="P Supply Scenario Switch",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def p_supply_scenario_switch():
    """
    0: Intended Amount 1: Intended amount is limited by the reserve availability 2: Supply shocks, therefore a timeseries exogenous application
    """
    return 1


@component.add(
    name="P Uptake for each crop type",
    units="Ton/Year",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"average_p_content": 2, "food_production_rate": 2},
)
def p_uptake_for_each_crop_type():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = (
        average_p_content()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        * food_production_rate()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
    ).values
    value.loc[["PasMeat"]] = float(average_p_content().loc["PasMeat"]) * float(
        food_production_rate().loc["PasMeat"]
    )
    return value


@component.add(
    name="P use efficiency",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_p_uptake_rate": 1,
        "commercial_p_application_for_agriculture": 1,
        "phosphorus_application_with_manure": 1,
    },
)
def p_use_efficiency():
    return total_p_uptake_rate() / (
        commercial_p_application_for_agriculture()
        + phosphorus_application_with_manure()
    )


@component.add(
    name="Phosphate Rock Proven Reserves",
    units="Ton",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_phosphate_rock_proven_reserves": 1},
    other_deps={
        "_integ_phosphate_rock_proven_reserves": {
            "initial": {"init_p_proven_reserves": 1},
            "step": {"p_discovery_rate": 1, "p_rock_production_rate": 1},
        }
    },
)
def phosphate_rock_proven_reserves():
    return _integ_phosphate_rock_proven_reserves()


_integ_phosphate_rock_proven_reserves = Integ(
    lambda: p_discovery_rate() - p_rock_production_rate(),
    lambda: init_p_proven_reserves(),
    "_integ_phosphate_rock_proven_reserves",
)


@component.add(
    name="Phosphorus",
    units="Ton",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_phosphorus": 1},
    other_deps={
        "_integ_phosphorus": {
            "initial": {"initial_phosphorus": 1},
            "step": {
                "phosphorus_erosion_leaching_and_runoff_rate": 1,
                "total_p_uptake_rate": 1,
                "commercial_p_application_for_agriculture": 1,
                "phosphorus_application_with_manure": 1,
            },
        }
    },
)
def phosphorus():
    """
    This is the total global amount of elemental phosphorus accumulating in the soil.
    """
    return _integ_phosphorus()


_integ_phosphorus = Integ(
    lambda: -phosphorus_erosion_leaching_and_runoff_rate()
    - total_p_uptake_rate()
    + commercial_p_application_for_agriculture()
    + phosphorus_application_with_manure(),
    lambda: initial_phosphorus(),
    "_integ_phosphorus",
)


@component.add(
    name="Phosphorus application with manure",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "recoverable_p_generated_in_pasture_based_manure": 1,
        "recoverable_p_generated_in_crop_based_manure": 1,
    },
)
def phosphorus_application_with_manure():
    return (
        recoverable_p_generated_in_pasture_based_manure()
        + recoverable_p_generated_in_crop_based_manure()
    )


@component.add(
    name="Phosphorus erosion leaching and runoff rate",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"p_leaching_fraction": 1, "phosphorus": 1},
)
def phosphorus_erosion_leaching_and_runoff_rate():
    """
    Agricultural topsoil erosion rate*Agricultural topsoil P concentration
    """
    return p_leaching_fraction() * phosphorus()


@component.add(
    name="Recoverable manure fraction crop based",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_recoverable_manure_fraction_crop_based": 1, "time": 1},
)
def recoverable_manure_fraction_crop_based():
    """
    Estimated based on FAO data and Scheldrick et al. 2003. See FAO...ProducingAnimals.xlsx
    """
    return 0.78 + step(
        __data["time"], sa_recoverable_manure_fraction_crop_based() - 0.78, 2020
    )


@component.add(
    name="Recoverable manure fraction pasture based",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_recoverable_manure_fraction_pasture_based": 1, "time": 1},
)
def recoverable_manure_fraction_pasture_based():
    """
    Estimated based on FAO data and Scheldrick et al. 2003. See FAO...ProducingAnimals.xlsx
    """
    return 0.24 + step(
        __data["time"], sa_recoverable_manure_fraction_pasture_based() - 0.24, 2020
    )


@component.add(
    name="Recoverable N generated in crop based manure",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "n_produced_in_the_manure_of_cropbased_animals": 1,
        "recoverable_manure_fraction_crop_based": 1,
    },
)
def recoverable_n_generated_in_crop_based_manure():
    return (
        n_produced_in_the_manure_of_cropbased_animals()
        * recoverable_manure_fraction_crop_based()
    )


@component.add(
    name="Recoverable N generated in pasture based manure",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "n_produced_in_the_manure_of_pasturebased_animals": 1,
        "recoverable_manure_fraction_pasture_based": 1,
    },
)
def recoverable_n_generated_in_pasture_based_manure():
    return (
        n_produced_in_the_manure_of_pasturebased_animals()
        * recoverable_manure_fraction_pasture_based()
    )


@component.add(
    name="Recoverable P generated in crop based manure",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "p_produced_in_the_manure_of_cropbased_animals": 1,
        "recoverable_manure_fraction_crop_based": 1,
    },
)
def recoverable_p_generated_in_crop_based_manure():
    return (
        p_produced_in_the_manure_of_cropbased_animals()
        * recoverable_manure_fraction_crop_based()
    )


@component.add(
    name="Recoverable P generated in pasture based manure",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "p_produced_in_the_manure_of_pasturebased_animals": 1,
        "recoverable_manure_fraction_pasture_based": 1,
    },
)
def recoverable_p_generated_in_pasture_based_manure():
    return (
        p_produced_in_the_manure_of_pasturebased_animals()
        * recoverable_manure_fraction_pasture_based()
    )


@component.add(
    name="Reference Dem Suppyl Ratio Agr Land 2010",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_dem_suppyl_ratio_agr_land_2010():
    return 0.53


@component.add(
    name="Reference N uptake per ha",
    units="Ton/(Year*ha)",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_crop_yield_2016": 1,
        "average_n_content": 2,
        "reference_meat_yield": 1,
    },
)
def reference_n_uptake_per_ha():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = (
        reference_crop_yield_2016()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        * average_n_content()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
    ).values
    value.loc[["PasMeat"]] = (
        float(average_n_content().loc["PasMeat"]) * reference_meat_yield()
    )
    return value


@component.add(
    name="Reference nitrogen consumption 2010",
    units="Ton/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_nitrogen_consumption_2010():
    """
    Calibrated parameter value
    """
    return 100000000.0


@component.add(
    name="Reference P price", units="$/Ton", comp_type="Constant", comp_subtype="Normal"
)
def reference_p_price():
    """
    Calibrated
    """
    return 87


@component.add(
    name="Reference P uptake rate per ha",
    units="Ton/(Year*ha)",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_crop_yield_2016": 1,
        "average_p_content": 2,
        "reference_meat_yield": 1,
    },
)
def reference_p_uptake_rate_per_ha():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = (
        reference_crop_yield_2016()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
        * average_p_content()
        .loc[_subscript_dict["PlantFood"]]
        .rename({"FoodCategories": "PlantFood"})
    ).values
    value.loc[["PasMeat"]] = reference_meat_yield() * float(
        average_p_content().loc["PasMeat"]
    )
    return value


@component.add(
    name="Reference phosphate consumption 2010",
    units="Ton/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_phosphate_consumption_2010():
    """
    Historical 2010 value
    """
    return 42900000.0


@component.add(
    name="Relative DemSupply Ratio AgrLand",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "smoothed_demand_supply_ratio_agr_land": 1,
        "reference_dem_suppyl_ratio_agr_land_2010": 1,
    },
)
def relative_demsupply_ratio_agrland():
    return (
        smoothed_demand_supply_ratio_agr_land()
        / reference_dem_suppyl_ratio_agr_land_2010()
    )


@component.add(
    name="Relative P price",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"p_price": 1, "reference_p_price": 1},
)
def relative_p_price():
    return p_price() / reference_p_price()


@component.add(
    name="Reserve demand ratio",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"phosphate_rock_proven_reserves": 1, "average_p_demand_rate": 1},
)
def reserve_demand_ratio():
    return phosphate_rock_proven_reserves() / average_p_demand_rate()


@component.add(
    name="SA k fertilizer",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_k_fertilizer():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = xr.DataArray(
        [0.2, 0.8, 0.25, 1.0],
        {"FoodCategories": _subscript_dict["PlantFood"]},
        ["FoodCategories"],
    ).values
    value.loc[["PasMeat"]] = 1
    return value


@component.add(
    name="SA k gwp fert", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def sa_k_gwp_fert():
    """
    1.5
    """
    return 3


@component.add(
    name="SA k land fert", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def sa_k_land_fert():
    return 1.6


@component.add(
    name="SA L fertilizer",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_l_fertilizer():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = xr.DataArray(
        [1.56, 1.6, 1.5, 2.5],
        {"FoodCategories": _subscript_dict["PlantFood"]},
        ["FoodCategories"],
    ).values
    value.loc[["PasMeat"]] = 1.8
    return value


@component.add(
    name="SA L gwp fert", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def sa_l_gwp_fert():
    """
    Calibrated simultaneously for Eff of GWP and Eff of Land. See FertilizerLookups.xlsx/Calibration...
    """
    return 1.25


@component.add(
    name="SA L land fert", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def sa_l_land_fert():
    return 2.2


@component.add(
    name="SA N fertilizer shares",
    units="Dmnl",
    subscripts=["PlantFood"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_n_fertilizer_shares():
    return xr.DataArray(
        [1.0, 1.0, 1.0, 1.0], {"PlantFood": _subscript_dict["PlantFood"]}, ["PlantFood"]
    )


@component.add(
    name="SA N leaching and runoff fraction",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_n_leaching_and_runoff_fraction():
    """
    Nitrate washed away. Especially going to the rivers and lakes. Runoff is 23% of "applied" N, not the stock as I use her. Leaching is around 12-15 M ton/year. In total, 46 M ton/year. The fraction is calibrated accordingly.
    """
    return 0.8


@component.add(
    name="SA P fertilizer shares",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_p_fertilizer_shares():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = xr.DataArray(
        [1.0, 1.0, 1.0, 1.0],
        {"FoodCategories": _subscript_dict["PlantFood"]},
        ["FoodCategories"],
    ).values
    value.loc[["PasMeat"]] = 0.04
    return value


@component.add(
    name="SA P leaching fraction",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_p_leaching_fraction():
    """
    When parameter: 0.25 Calibrated: 0.06
    """
    return 0.3


@component.add(
    name="SA Recoverable manure fraction crop based",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_recoverable_manure_fraction_crop_based():
    """
    Estimated based on FAO data and Scheldrick et al. 2003. See FAO...ProducingAnimals.xlsx
    """
    return 0.78


@component.add(
    name="SA Recoverable manure fraction pasture based",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_recoverable_manure_fraction_pasture_based():
    """
    Estimated based on FAO data and Scheldrick et al. 2003. See FAO...ProducingAnimals.xlsx
    """
    return 0.24


@component.add(
    name="SA x0 fertilizer",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_x0_fertilizer():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = xr.DataArray(
        [1.0, 1.0, 1.0, 1.0],
        {"FoodCategories": _subscript_dict["PlantFood"]},
        ["FoodCategories"],
    ).values
    value.loc[["PasMeat"]] = 1
    return value


@component.add(
    name="SA x0 gwp fert", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def sa_x0_gwp_fert():
    return 1.44


@component.add(
    name="SA x0 land fert", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def sa_x0_land_fert():
    return 1.13


@component.add(
    name="Smoothed Demand Supply Ratio Agr Land",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_smoothed_demand_supply_ratio_agr_land": 1},
    other_deps={
        "_smooth_smoothed_demand_supply_ratio_agr_land": {
            "initial": {"demand_supply_ratio_of_agricultural_land": 1},
            "step": {"demand_supply_ratio_of_agricultural_land": 1},
        }
    },
)
def smoothed_demand_supply_ratio_agr_land():
    return _smooth_smoothed_demand_supply_ratio_agr_land()


_smooth_smoothed_demand_supply_ratio_agr_land = Smooth(
    lambda: demand_supply_ratio_of_agricultural_land(),
    lambda: 10,
    lambda: demand_supply_ratio_of_agricultural_land(),
    lambda: 1,
    "_smooth_smoothed_demand_supply_ratio_agr_land",
)


@component.add(
    name="Total area harvested",
    units="ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"area_harvested": 1},
)
def total_area_harvested():
    return sum(area_harvested().rename({"PlantFood": "PlantFood!"}), dim=["PlantFood!"])


@component.add(
    name="Total N Emissions",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"denitrification_rate": 1, "nitrogen_leaching_and_runoff_rate": 1},
)
def total_n_emissions():
    return denitrification_rate() + nitrogen_leaching_and_runoff_rate()


@component.add(
    name="Total N uptake rate",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n_uptake_for_crop_type": 2, "nitrogen": 1, "time_step": 1},
)
def total_n_uptake_rate():
    return float(
        np.minimum(
            sum(
                n_uptake_for_crop_type()
                .loc[_subscript_dict["PlantFood"]]
                .rename({"FoodCategories": "PlantFood!"}),
                dim=["PlantFood!"],
            )
            + float(n_uptake_for_crop_type().loc["PasMeat"]),
            nitrogen() / time_step(),
        )
    )


@component.add(
    name="Total P205 demand",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"p2o5_demand_from_agriculture": 1, "p2o5_agriculture_fraction": 1},
)
def total_p205_demand():
    return p2o5_demand_from_agriculture() / p2o5_agriculture_fraction()


@component.add(
    name="Total P produced in manure",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "p_produced_in_the_manure_of_cropbased_animals": 1,
        "p_produced_in_the_manure_of_pasturebased_animals": 1,
    },
)
def total_p_produced_in_manure():
    return (
        p_produced_in_the_manure_of_cropbased_animals()
        + p_produced_in_the_manure_of_pasturebased_animals()
    )


@component.add(
    name="Total P uptake rate",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"p_uptake_for_each_crop_type": 2, "phosphorus": 1, "time_step": 1},
)
def total_p_uptake_rate():
    return float(
        np.minimum(
            sum(
                p_uptake_for_each_crop_type()
                .loc[_subscript_dict["PlantFood"]]
                .rename({"FoodCategories": "PlantFood!"}),
                dim=["PlantFood!"],
            )
            + float(p_uptake_for_each_crop_type().loc["PasMeat"]),
            phosphorus() / time_step(),
        )
    )


@component.add(
    name="Unit N production via manure crop based",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def unit_n_production_via_manure_crop_based():
    """
    See FAO...ProducingAnimals.xls - Estimated based on FAO data on food production and number of livestock; and Shildrick et al 2003 for unit N manure production values. It is ton/ton, so dimensionless.
    """
    return 0.0702


@component.add(
    name="Unit N production via manure pasture based",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def unit_n_production_via_manure_pasture_based():
    """
    See FAO...ProducingAnimals.xls - Estimated based on FAO data on animal calorie supply and number of livestock; and Shildrick et al 2003 for unit N manure production values. [Ton/ton]
    """
    return 0.0334


@component.add(
    name="Unit P production via manure crop based",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def unit_p_production_via_manure_crop_based():
    """
    See FAO...ProducingAnimals.xls - Estimated based on FAO data on food production and number of livestock; and Shildrick et al 2003 for unit P manure production values. It is ton/ton, so dimensionless.
    """
    return 0.0553


@component.add(
    name="Unit P production via manure pasture based",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def unit_p_production_via_manure_pasture_based():
    """
    See FAO...ProducingAnimals.xls - Estimated based on FAO data on animal calorie supply and number of livestock; and Shildrick et al 2003 for unit P manure production values. [Ton/ton]
    """
    return 0.0067


@component.add(
    name="x0 fertilizer",
    units="Dmnl",
    subscripts=["FoodCategories"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={"sa_x0_fertilizer": 1, "time": 1},
)
def x0_fertilizer():
    value = xr.DataArray(
        np.nan,
        {"FoodCategories": _subscript_dict["FoodCategories"]},
        ["FoodCategories"],
    )
    value.loc[_subscript_dict["PlantFood"]] = (
        1
        + step(
            __data["time"],
            sa_x0_fertilizer()
            .loc[_subscript_dict["PlantFood"]]
            .rename({"FoodCategories": "PlantFood"})
            - 1,
            2020,
        )
    ).values
    value.loc[["PasMeat"]] = 1
    return value


@component.add(
    name="x0 gwp fert", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def x0_gwp_fert():
    """
    1.44 + STEP(SA x0 gwp fert-1.44, 2020)
    """
    return 1.164


@component.add(
    name="x0 land fert",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_x0_land_fert": 1, "time": 1},
)
def x0_land_fert():
    return 1.13 + step(__data["time"], sa_x0_land_fert() - 1.13, 2020)


@component.add(
    name="x0 tech fert", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def x0_tech_fert():
    return 30
