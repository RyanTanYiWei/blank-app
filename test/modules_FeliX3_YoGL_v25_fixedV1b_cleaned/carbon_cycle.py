"""
Module carbon_cycle
Translated using PySD version 3.14.3
"""

@component.add(
    name="Agricultural Land Change",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"agricultural_land": 1, "init_agricultural_land": 1},
)
def agricultural_land_change():
    """
    Ratio of agricultural land area change compared to its initial area in year 1900.
    """
    return agricultural_land() / init_agricultural_land()


@component.add(
    name="Atmospheric CO2 Law Dome 1850",
    units="ppm",
    comp_type="Constant",
    comp_subtype="Normal",
)
def atmospheric_co2_law_dome_1850():
    """
    Historical CO2 record derived from a spline fit (20 year cutoff) of the Law Dome DE08 and DE08-2 ice cores for year 1850
    """
    return 284.7


@component.add(
    name="Atmospheric Concentration CO2",
    units="ppm",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_atmosphere": 1, "gtc_to_tonc": 1, "ppm_to_gtc": 1},
)
def atmospheric_concentration_co2():
    """
    Converts weight of CO2 in atmosphere to concentration (ppm CO2). Source of Historical Data: Etheridge, D.M., Steele, L.P., Langenfelds, R.L., Francey, R.J., Barnola, J.-M., Morgan, V.I. 1998. Historical CO2 records from the Law Dome DE08, DE08-2, and DSS ice cores. In Trends: A Compendium of Data on Global Change. Carbon Dioxide Information Analysis Center, Oak Ridge National Laboratory, U.S. Department of Energy, Oak Ridge, Tenn., U.S.A
    """
    return c_in_atmosphere() / gtc_to_tonc() / ppm_to_gtc()


@component.add(
    name="Biomass Res Time", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def biomass_res_time():
    """
    Average residence time of carbon in biomass.
    """
    return 10.6


@component.add(
    name="Biostimulation Coefficient",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biostimulation_coefficient():
    """
    Coefficient for response of primary production to carbon concentration.
    """
    return 0.35


@component.add(
    name="Buff C Coeff", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def buff_c_coeff():
    """
    Coefficient of carbon concentration influence on buffer factor.
    """
    return 3.92


@component.add(
    name="Buffer Factor",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ref_buffer_factor": 1,
        "c_in_mixed_layer": 1,
        "buff_c_coeff": 1,
        "preindustrial_c_in_mixed_layer": 1,
    },
)
def buffer_factor():
    """
    Buffer factor for atmosphere/mixed ocean carbon equilibration.
    """
    return (
        ref_buffer_factor()
        * (c_in_mixed_layer() / preindustrial_c_in_mixed_layer()) ** buff_c_coeff()
    )


@component.add(
    name="C Concentration Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_atmosphere": 1, "init_c_in_atmosphere": 1},
)
def c_concentration_ratio():
    """
    Current to initial carbon concentration in atmosphere.
    """
    return c_in_atmosphere() / init_c_in_atmosphere()


@component.add(
    name="C Emission from Biomass Energy",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_energy_production": 1,
        "c_intensity_of_emission_from_biomass_energy": 1,
    },
)
def c_emission_from_biomass_energy():
    """
    Total carbon emission from biomass energy production and it use.
    """
    return biomass_energy_production() * c_intensity_of_emission_from_biomass_energy()


@component.add(
    name="C Emission from Coal Energy",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"coal_production": 1, "c_intensity_of_emission_from_coal": 1},
)
def c_emission_from_coal_energy():
    """
    Total carbon emission from coal energy production and it use.
    """
    return coal_production() * c_intensity_of_emission_from_coal()


@component.add(
    name="C Emission from Gas Energy",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gas_production": 1, "c_intensity_of_emission_from_gas": 1},
)
def c_emission_from_gas_energy():
    """
    Total carbon emission from gas energy production and it use.
    """
    return gas_production() * c_intensity_of_emission_from_gas()


@component.add(
    name="C Emission from Land Use",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_intensity_of_emissions_from_agricultural_land_use": 1,
        "agricultural_land_change": 1,
        "forest_land_change": 1,
        "c_intensity_of_emissions_from_forest_land_use": 1,
    },
)
def c_emission_from_land_use():
    """
    Total carbon emission from forest and agricultural land use change. Source of Historical Data: Houghton, R.A. 2008. Carbon Flux to the Atmosphere from Land-Use Changes: 1850-2005. In TRENDS: A Compendium of Data on Global Change. Carbon Dioxide Information Analysis Center, Oak Ridge National Laboratory, U.S. Department of Energy, Oak Ridge, Tenn., U.S.A.
    """
    return (
        c_intensity_of_emissions_from_agricultural_land_use()
        * agricultural_land_change()
        + (2 - forest_land_change()) * c_intensity_of_emissions_from_forest_land_use()
    )


@component.add(
    name="C Emission from Oil Energy",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"oil_production": 1, "c_intensity_of_emission_from_oil": 1},
)
def c_emission_from_oil_energy():
    """
    Total carbon emission from oil production and it use.
    """
    return oil_production() * c_intensity_of_emission_from_oil()


@component.add(
    name="C Emission from Solar Energy",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "solar_energy_production": 1,
        "c_intensity_of_emission_from_solar_energy": 1,
    },
)
def c_emission_from_solar_energy():
    """
    Total carbon emission from solar energy production and it use.
    """
    return solar_energy_production() * c_intensity_of_emission_from_solar_energy()


@component.add(
    name="C Emission from Wind Energy",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "wind_energy_production": 1,
        "c_intensity_of_emission_from_wind_energy": 1,
    },
)
def c_emission_from_wind_energy():
    """
    Total carbon emission from wind energy production and it use.
    """
    return wind_energy_production() * c_intensity_of_emission_from_wind_energy()


@component.add(
    name="C in Atmosphere",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_atmosphere": 1},
    other_deps={
        "_integ_c_in_atmosphere": {
            "initial": {"init_c_in_atmosphere": 1},
            "step": {
                "flux_biomass_to_atmosphere": 1,
                "flux_humus_to_atmosphere": 1,
                "total_c_emission": 1,
                "carbon_removal_rate": 2,
                "flux_atmosphere_to_biomass": 1,
                "flux_atmosphere_to_ocean": 1,
            },
        }
    },
)
def c_in_atmosphere():
    """
    Carbon in atmosphere.
    """
    return _integ_c_in_atmosphere()


_integ_c_in_atmosphere = Integ(
    lambda: flux_biomass_to_atmosphere()
    + flux_humus_to_atmosphere()
    + total_c_emission()
    - carbon_removal_rate()
    - flux_atmosphere_to_biomass()
    - flux_atmosphere_to_ocean()
    - carbon_removal_rate(),
    lambda: init_c_in_atmosphere(),
    "_integ_c_in_atmosphere",
)


@component.add(
    name="C in Biomass",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_biomass": 1},
    other_deps={
        "_integ_c_in_biomass": {
            "initial": {"init_c_in_biomass": 1},
            "step": {
                "flux_atmosphere_to_biomass": 1,
                "flux_biomass_to_atmosphere": 1,
                "flux_biomass_to_humus": 1,
            },
        }
    },
)
def c_in_biomass():
    """
    Carbon in biosphere (biomass, litter, and humus)
    """
    return _integ_c_in_biomass()


_integ_c_in_biomass = Integ(
    lambda: flux_atmosphere_to_biomass()
    - flux_biomass_to_atmosphere()
    - flux_biomass_to_humus(),
    lambda: init_c_in_biomass(),
    "_integ_c_in_biomass",
)


@component.add(
    name="C in Deep Ocean 1",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_deep_ocean_1": 1},
    other_deps={
        "_integ_c_in_deep_ocean_1": {
            "initial": {"init_c_in_deep_ocean_1": 1},
            "step": {"diffusion_flux_1": 1, "diffusion_flux_2": 1},
        }
    },
)
def c_in_deep_ocean_1():
    """
    Carbon in the first layer of deep ocean.
    """
    return _integ_c_in_deep_ocean_1()


_integ_c_in_deep_ocean_1 = Integ(
    lambda: diffusion_flux_1() - diffusion_flux_2(),
    lambda: init_c_in_deep_ocean_1(),
    "_integ_c_in_deep_ocean_1",
)


@component.add(
    name="C in Deep Ocean 1 per meter",
    units="TonC/Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_deep_ocean_1": 1, "layer_depth_1": 1},
)
def c_in_deep_ocean_1_per_meter():
    """
    Carbon in the first ocean layer per its meter.
    """
    return c_in_deep_ocean_1() / layer_depth_1()


@component.add(
    name="C in Deep Ocean 2",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_deep_ocean_2": 1},
    other_deps={
        "_integ_c_in_deep_ocean_2": {
            "initial": {"init_c_in_deep_ocean_2": 1},
            "step": {"diffusion_flux_2": 1, "diffusion_flux_3": 1},
        }
    },
)
def c_in_deep_ocean_2():
    """
    Carbon in the second layer of deep ocean.
    """
    return _integ_c_in_deep_ocean_2()


_integ_c_in_deep_ocean_2 = Integ(
    lambda: diffusion_flux_2() - diffusion_flux_3(),
    lambda: init_c_in_deep_ocean_2(),
    "_integ_c_in_deep_ocean_2",
)


@component.add(
    name="C in Deep Ocean 2 per meter",
    units="TonC/Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_deep_ocean_2": 1, "layer_depth_2": 1},
)
def c_in_deep_ocean_2_per_meter():
    """
    Carbon in the second ocean layer per its meter.
    """
    return c_in_deep_ocean_2() / layer_depth_2()


@component.add(
    name="C in Deep Ocean 3",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_deep_ocean_3": 1},
    other_deps={
        "_integ_c_in_deep_ocean_3": {
            "initial": {"init_c_in_deep_ocean_3": 1},
            "step": {"diffusion_flux_3": 1, "diffusion_flux_4": 1},
        }
    },
)
def c_in_deep_ocean_3():
    """
    Carbon in the third layer of deep ocean.
    """
    return _integ_c_in_deep_ocean_3()


_integ_c_in_deep_ocean_3 = Integ(
    lambda: diffusion_flux_3() - diffusion_flux_4(),
    lambda: init_c_in_deep_ocean_3(),
    "_integ_c_in_deep_ocean_3",
)


@component.add(
    name="C in Deep Ocean 3 per meter",
    units="TonC/Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_deep_ocean_3": 1, "layer_depth_3": 1},
)
def c_in_deep_ocean_3_per_meter():
    """
    Carbon in the third ocean layer per its meter.
    """
    return c_in_deep_ocean_3() / layer_depth_3()


@component.add(
    name="C in Deep Ocean 4",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_deep_ocean_4": 1},
    other_deps={
        "_integ_c_in_deep_ocean_4": {
            "initial": {"init_c_in_deep_ocean_4": 1},
            "step": {"diffusion_flux_4": 1},
        }
    },
)
def c_in_deep_ocean_4():
    """
    Carbon in the fourth layer of deep ocean.
    """
    return _integ_c_in_deep_ocean_4()


_integ_c_in_deep_ocean_4 = Integ(
    lambda: diffusion_flux_4(),
    lambda: init_c_in_deep_ocean_4(),
    "_integ_c_in_deep_ocean_4",
)


@component.add(
    name="C in Deep Ocean 4 per meter",
    units="TonC/Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_deep_ocean_4": 1, "layer_depth_4": 1},
)
def c_in_deep_ocean_4_per_meter():
    """
    Carbon in the fourth ocean layer per its meter.
    """
    return c_in_deep_ocean_4() / layer_depth_4()


@component.add(
    name="C in Humus",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_humus": 1},
    other_deps={
        "_integ_c_in_humus": {
            "initial": {"init_c_in_humus": 1},
            "step": {"flux_biomass_to_humus": 1, "flux_humus_to_atmosphere": 1},
        }
    },
)
def c_in_humus():
    """
    Carbon in humus.
    """
    return _integ_c_in_humus()


_integ_c_in_humus = Integ(
    lambda: flux_biomass_to_humus() - flux_humus_to_atmosphere(),
    lambda: init_c_in_humus(),
    "_integ_c_in_humus",
)


@component.add(
    name="C in Mixed Layer",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_mixed_layer": 1},
    other_deps={
        "_integ_c_in_mixed_layer": {
            "initial": {"init_c_in_mixed_ocean": 1},
            "step": {"flux_atmosphere_to_ocean": 1, "diffusion_flux_1": 1},
        }
    },
)
def c_in_mixed_layer():
    """
    Carbon in mixed layer.
    """
    return _integ_c_in_mixed_layer()


_integ_c_in_mixed_layer = Integ(
    lambda: flux_atmosphere_to_ocean() - diffusion_flux_1(),
    lambda: init_c_in_mixed_ocean(),
    "_integ_c_in_mixed_layer",
)


@component.add(
    name="C in Mixed Layer per meter",
    units="TonC/Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_mixed_layer": 1, "mixed_layer_depth": 1},
)
def c_in_mixed_layer_per_meter():
    """
    Carbon in mixed layer per its meter.
    """
    return c_in_mixed_layer() / mixed_layer_depth()


@component.add(
    name="C Intensity of Emission from Biomass Energy",
    units="TonC/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_improvement_factor": 1},
)
def c_intensity_of_emission_from_biomass_energy():
    """
    Carbon intensity from biomass energy production and it use. Felix1: 1.278e+006 IPCC: med: 2.6749e+006 min:1511900
    """
    return 1511900.0 * (1 - ccs_improvement_factor())


@component.add(
    name="C Intensity of Emission from Coal",
    units="TonC/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_c_intensity_of_emission_from_coal": 1,
        "ccs_improvement_factor": 1,
    },
)
def c_intensity_of_emission_from_coal():
    """
    Carbon intensity from coal energy production and it use.
    """
    return normal_c_intensity_of_emission_from_coal() * (1 - ccs_improvement_factor())


@component.add(
    name="C Intensity of Emission from Gas",
    units="TonC/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_c_intensity_of_emission_from_gas": 1,
        "ccs_improvement_factor": 1,
    },
)
def c_intensity_of_emission_from_gas():
    """
    Carbon intensity from gas energy production and it use.
    """
    return normal_c_intensity_of_emission_from_gas() * (1 - ccs_improvement_factor())


@component.add(
    name="C Intensity of Emission from Oil",
    units="TonC/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_c_intensity_of_emission_from_oil": 1,
        "ccs_improvement_factor": 1,
    },
)
def c_intensity_of_emission_from_oil():
    """
    Carbon intensity from oil energy production and it use.
    """
    return normal_c_intensity_of_emission_from_oil() * (1 - ccs_improvement_factor())


@component.add(
    name="C Intensity of Emission from Solar Energy",
    units="TonC/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def c_intensity_of_emission_from_solar_energy():
    """
    Carbon intensity from solar energy production and it use. fELIX1: 43200 IPCC: med: 476830 min:302380
    """
    return 43200


@component.add(
    name="C Intensity of Emission from Wind Energy",
    units="TonC/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def c_intensity_of_emission_from_wind_energy():
    """
    Carbon intensity from wind energy production and it use. Felix1: 27000 IPCC: med: 139560 min: 93040
    """
    return 27000


@component.add(
    name="C Intensity of Emissions from Agricultural Land Use",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"reference_c_emission_from_agricultural_land_use": 1},
)
def c_intensity_of_emissions_from_agricultural_land_use():
    return reference_c_emission_from_agricultural_land_use()


@component.add(
    name="C Intensity of Emissions from Forest Land Use",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"reference_c_emission_from_forest_land_use": 1},
)
def c_intensity_of_emissions_from_forest_land_use():
    return reference_c_emission_from_forest_land_use()


@component.add(
    name="Carbon Removal Impact Slope", comp_type="Constant", comp_subtype="Normal"
)
def carbon_removal_impact_slope():
    return 1.1


@component.add(
    name="Carbon Removal Rate",
    units="TonC/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"climate_policy_scenario": 1, "_smooth_carbon_removal_rate": 1},
    other_deps={
        "_smooth_carbon_removal_rate": {
            "initial": {
                "reference_co2_removal_rate": 1,
                "climate_action_year": 1,
                "time": 1,
            },
            "step": {
                "reference_co2_removal_rate": 1,
                "climate_action_year": 1,
                "time": 1,
                "cdr_policy_transition_period": 1,
            },
        }
    },
)
def carbon_removal_rate():
    """
    Climate Policy Scenario*SMOOTH(STEP(Carbon Removal Impact Slope*Reference Removal Rate, Climate Action Year), Climate Policy Transition Period)
    """
    return climate_policy_scenario() * _smooth_carbon_removal_rate()


_smooth_carbon_removal_rate = Smooth(
    lambda: ramp(
        __data["time"], reference_co2_removal_rate(), climate_action_year(), 2100
    ),
    lambda: cdr_policy_transition_period(),
    lambda: ramp(
        __data["time"], reference_co2_removal_rate(), climate_action_year(), 2100
    ),
    lambda: 1,
    "_smooth_carbon_removal_rate",
)


@component.add(
    name="CCS Improvement",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ccs_improvement": 1},
    other_deps={
        "_integ_ccs_improvement": {
            "initial": {"init_ccs_improvement": 1},
            "step": {"ccs_improvement_change": 1},
        }
    },
)
def ccs_improvement():
    """
    Accumulated improvement of carbon capture and storage technology.
    """
    return _integ_ccs_improvement()


_integ_ccs_improvement = Integ(
    lambda: ccs_improvement_change(),
    lambda: init_ccs_improvement(),
    "_integ_ccs_improvement",
)


@component.add(
    name="CCS Improvement Change",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ccsiclv3": 1},
)
def ccs_improvement_change():
    """
    Change in improvement of carbon capture and storage technology.
    """
    return outflow_ccsiclv3()


@component.add(
    name="CCS Improvement Change LV1",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ccs_improvement_change_lv1": 1},
    other_deps={
        "_integ_ccs_improvement_change_lv1": {
            "initial": {"ccs_improvement_change_lv3": 1},
            "step": {"inflow_ccsiclv1": 1, "outflow_ccsiclv1": 1},
        }
    },
)
def ccs_improvement_change_lv1():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_ccs_improvement_change_lv1()


_integ_ccs_improvement_change_lv1 = Integ(
    lambda: inflow_ccsiclv1() - outflow_ccsiclv1(),
    lambda: ccs_improvement_change_lv3(),
    "_integ_ccs_improvement_change_lv1",
)


@component.add(
    name="CCS Improvement Change LV2",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ccs_improvement_change_lv2": 1},
    other_deps={
        "_integ_ccs_improvement_change_lv2": {
            "initial": {"ccs_improvement_change_lv3": 1},
            "step": {"inflow_ccsiclv2": 1, "outflow_ccsiclv2": 1},
        }
    },
)
def ccs_improvement_change_lv2():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_ccs_improvement_change_lv2()


_integ_ccs_improvement_change_lv2 = Integ(
    lambda: inflow_ccsiclv2() - outflow_ccsiclv2(),
    lambda: ccs_improvement_change_lv3(),
    "_integ_ccs_improvement_change_lv2",
)


@component.add(
    name="CCS Improvement Change LV3",
    units="1",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ccs_improvement_change_lv3": 1},
    other_deps={
        "_integ_ccs_improvement_change_lv3": {
            "initial": {"delay_time_ccsic": 1, "pressure_ccsic": 1},
            "step": {"inflow_ccsiclv3": 1, "outflow_ccsiclv3": 1},
        }
    },
)
def ccs_improvement_change_lv3():
    """
    For coverting DELAY3 function only. Added by Q Ye in July 2024
    """
    return _integ_ccs_improvement_change_lv3()


_integ_ccs_improvement_change_lv3 = Integ(
    lambda: inflow_ccsiclv3() - outflow_ccsiclv3(),
    lambda: delay_time_ccsic() * pressure_ccsic(),
    "_integ_ccs_improvement_change_lv3",
)


@component.add(
    name="CCS Improvement Factor",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "min_ccs_improvement_factor": 2,
        "max_ccs_improvement_factor": 1,
        "ccs_improvement": 2,
    },
)
def ccs_improvement_factor():
    """
    Impact of carbon capture and storage on carbon intensity of emissions from fossil fuels. Scaled between min and max improvement factor.
    """
    return min_ccs_improvement_factor() + (
        max_ccs_improvement_factor() - min_ccs_improvement_factor()
    ) * (ccs_improvement() / (ccs_improvement() + 1))


@component.add(
    name="CCS Scenario",
    units="Dmnl",
    limits=(0.0, 1.0, 1.0),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_scenario_switch_variation": 1, "time": 1},
)
def ccs_scenario():
    """
    Carbon capture and storage scenario trigger
    """
    return 0 + step(__data["time"], ccs_scenario_switch_variation(), 2020)


@component.add(
    name="CCS Scenario Switch Variation",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_scenario_variation": 4},
)
def ccs_scenario_switch_variation():
    """
    IF THEN ELSE(0 <= CCS Scenario Variation :AND: CCS Scenario Variation < 1, 0 , 0) + IF THEN ELSE(1 <= CCS Scenario Variation :AND: CCS Scenario Variation < 2, 1 , 0)
    """
    return if_then_else(
        np.logical_and(0 <= ccs_scenario_variation(), ccs_scenario_variation() < 1),
        lambda: 0,
        lambda: 0,
    ) + if_then_else(
        np.logical_and(1 <= ccs_scenario_variation(), ccs_scenario_variation() < 2),
        lambda: 1,
        lambda: 0,
    )


@component.add(
    name="CCS Scenario Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ccs_scenario_variation():
    return 0


@component.add(
    name="CDR Policy Transition Period",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def cdr_policy_transition_period():
    return 1


@component.add(
    name="Climate Action Year",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_action_year():
    return 2020


@component.add(
    name="Climate Policy Scenario",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_policy_scenario():
    """
    0: No climate policy 1: Climate policy
    """
    return 0


@component.add(
    name="DE S", units="TonC/Year", comp_type="Constant", comp_subtype="Normal"
)
def de_s():
    """
    The upper level of acceptable total carbon emission from fossil fuels.
    """
    return 7500000000.0


@component.add(
    name="DE Var S",
    units="TonC/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_de_var_s": 1},
    other_deps={
        "_smooth_de_var_s": {
            "initial": {"de_s": 1, "time": 1},
            "step": {"de_s": 1, "time": 1},
        }
    },
)
def de_var_s():
    """
    The upper level of acceptable total carbon emission from fossil fuels.
    """
    return 7500000000.0 + _smooth_de_var_s()


_smooth_de_var_s = Smooth(
    lambda: step(__data["time"], de_s() - 7500000000.0, 2020),
    lambda: 1,
    lambda: step(__data["time"], de_s() - 7500000000.0, 2020),
    lambda: 1,
    "_smooth_de_var_s",
)


@component.add(
    name="Default C Intensity of Emission from Biomass",
    units="kgCO2/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_intensity_of_emission_from_biomass_energy": 1,
        "ton_c_to_kg_co2": 1,
        "mtoe_to_gj": 1,
    },
)
def default_c_intensity_of_emission_from_biomass():
    """
    Carbon intensity from biomass energy production and it use.
    """
    return (
        c_intensity_of_emission_from_biomass_energy() * ton_c_to_kg_co2() / mtoe_to_gj()
    )


@component.add(
    name="Default C Intensity of Emission from Coal",
    units="kgCO2/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_c_intensity_of_emission_from_coal": 1,
        "ton_c_to_kg_co2": 1,
        "mtoe_to_gj": 1,
    },
)
def default_c_intensity_of_emission_from_coal():
    """
    Initial carbon intensity of production from coal technologies.
    """
    return normal_c_intensity_of_emission_from_coal() * ton_c_to_kg_co2() / mtoe_to_gj()


@component.add(
    name="Default C Intensity of Emission from Gas",
    units="kgCO2/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_c_intensity_of_emission_from_gas": 1,
        "ton_c_to_kg_co2": 1,
        "mtoe_to_gj": 1,
    },
)
def default_c_intensity_of_emission_from_gas():
    """
    Initial carbon intensity of production from gas technologies.
    """
    return normal_c_intensity_of_emission_from_gas() * ton_c_to_kg_co2() / mtoe_to_gj()


@component.add(
    name="Default C Intensity of Emission from Oil",
    units="kgCO2/GJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_c_intensity_of_emission_from_oil": 1,
        "ton_c_to_kg_co2": 1,
        "mtoe_to_gj": 1,
    },
)
def default_c_intensity_of_emission_from_oil():
    """
    Initial carbon intensity of production from oil technologies.
    """
    return normal_c_intensity_of_emission_from_oil() * ton_c_to_kg_co2() / mtoe_to_gj()


@component.add(
    name="Delay Time CCSIC",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_to_improve_ccs": 1},
)
def delay_time_ccsic():
    return time_to_improve_ccs() / 3


@component.add(
    name="Desired Total C Emission from Fossil Fuels",
    units="TonC/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"de_var_s": 1, "_smooth_desired_total_c_emission_from_fossil_fuels": 1},
    other_deps={
        "_smooth_desired_total_c_emission_from_fossil_fuels": {
            "initial": {
                "desired_total_c_emission_from_fossil_fuels_variation": 1,
                "de_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "desired_total_c_emission_from_fossil_fuels_variation": 1,
                "de_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_production_variation_time": 1,
            },
        }
    },
)
def desired_total_c_emission_from_fossil_fuels():
    """
    The upper level of acceptable total carbon emission from fossil fuels.
    """
    return de_var_s() + _smooth_desired_total_c_emission_from_fossil_fuels()


_smooth_desired_total_c_emission_from_fossil_fuels = Smooth(
    lambda: step(
        __data["time"],
        desired_total_c_emission_from_fossil_fuels_variation() - de_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_production_variation_time(),
    lambda: step(
        __data["time"],
        desired_total_c_emission_from_fossil_fuels_variation() - de_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_desired_total_c_emission_from_fossil_fuels",
)


@component.add(
    name="Desired Total C Emission from Fossil Fuels Variation",
    units="TonC/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def desired_total_c_emission_from_fossil_fuels_variation():
    """
    The upper level of acceptable total carbon emission from fossil fuels.
    """
    return 7500000000.0


@component.add(
    name="Diffusion Flux 1",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_mixed_layer_per_meter": 1,
        "c_in_deep_ocean_1_per_meter": 1,
        "eddy_diff_coeff_m_1": 1,
        "mean_depth_of_adjacent_m_1_layers": 1,
    },
)
def diffusion_flux_1():
    """
    Diffusion flux between mixed and the first ocean layers.
    """
    return (
        (c_in_mixed_layer_per_meter() - c_in_deep_ocean_1_per_meter())
        * eddy_diff_coeff_m_1()
        / mean_depth_of_adjacent_m_1_layers()
    )


@component.add(
    name="Diffusion Flux 2",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_deep_ocean_1_per_meter": 1,
        "c_in_deep_ocean_2_per_meter": 1,
        "eddy_diff_coeff_1_2": 1,
        "mean_depth_of_adjacent_1_2_layers": 1,
    },
)
def diffusion_flux_2():
    """
    Diffusion flux between the first and the second ocean layers.
    """
    return (
        (c_in_deep_ocean_1_per_meter() - c_in_deep_ocean_2_per_meter())
        * eddy_diff_coeff_1_2()
        / mean_depth_of_adjacent_1_2_layers()
    )


@component.add(
    name="Diffusion Flux 3",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_deep_ocean_2_per_meter": 1,
        "c_in_deep_ocean_3_per_meter": 1,
        "eddy_diff_coeff_2_3": 1,
        "mean_depth_of_adjacent_2_3_layers": 1,
    },
)
def diffusion_flux_3():
    """
    Diffusion flux between the second and the third ocean layers.
    """
    return (
        (c_in_deep_ocean_2_per_meter() - c_in_deep_ocean_3_per_meter())
        * eddy_diff_coeff_2_3()
        / mean_depth_of_adjacent_2_3_layers()
    )


@component.add(
    name="Diffusion Flux 4",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_deep_ocean_3_per_meter": 1,
        "c_in_deep_ocean_4_per_meter": 1,
        "eddy_diff_coeff_3_4": 1,
        "mean_depth_of_adjacent_3_4_layers": 1,
    },
)
def diffusion_flux_4():
    """
    Diffusion flux between the third and the fourth ocean layers.
    """
    return (
        (c_in_deep_ocean_3_per_meter() - c_in_deep_ocean_4_per_meter())
        * eddy_diff_coeff_3_4()
        / mean_depth_of_adjacent_3_4_layers()
    )


@component.add(
    name="Eddy diff coeff 1 2",
    units="Meter*Meter/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"eddy_diff_coeff_index_1_2": 1, "eddy_diff_coeff_mean_1_2": 1},
)
def eddy_diff_coeff_1_2():
    """
    Coefficient of carbon diffusion to the second layer of deep ocean.
    """
    return eddy_diff_coeff_index_1_2() * eddy_diff_coeff_mean_1_2()


@component.add(
    name="Eddy diff coeff 2 3",
    units="Meter*Meter/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"eddy_diff_coeff_index_2_3": 1, "eddy_diff_coeff_mean_2_3": 1},
)
def eddy_diff_coeff_2_3():
    """
    Coefficient of carbon diffusion to the third layer of deep ocean.
    """
    return eddy_diff_coeff_index_2_3() * eddy_diff_coeff_mean_2_3()


@component.add(
    name="Eddy diff coeff 3 4",
    units="Meter*Meter/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"eddy_diff_coeff_index_3_4": 1, "eddy_diff_coeff_mean_3_4": 1},
)
def eddy_diff_coeff_3_4():
    """
    Coefficient of carbon diffusion to the fourth layer of deep ocean.
    """
    return eddy_diff_coeff_index_3_4() * eddy_diff_coeff_mean_3_4()


@component.add(
    name="Eddy diff coeff index 1 2",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def eddy_diff_coeff_index_1_2():
    """
    Index of coefficient for rate at which carbon is mixed in the ocean due to eddy motion, where 1 is equivalent to the expected value of 4400 meter/meter/year.
    """
    return 1


@component.add(
    name="Eddy diff coeff index 2 3",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def eddy_diff_coeff_index_2_3():
    """
    Index of coefficient for rate at which carbon is mixed in the ocean due to eddy motion, where 1 is equivalent to the expected value of 4400 meter/meter/year.
    """
    return 1


@component.add(
    name="Eddy diff coeff index 3 4",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def eddy_diff_coeff_index_3_4():
    """
    Index of coefficient for rate at which carbon is mixed in the ocean due to eddy motion, where 1 is equivalent to the expected value of 4400 meter/meter/year.
    """
    return 1


@component.add(
    name="Eddy diff coeff index M 1",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def eddy_diff_coeff_index_m_1():
    """
    Index of coefficient for rate at which carbon is mixed in the ocean due to eddy motion, where 1 is equivalent to the expected value of 4400 meter/meter/year.
    """
    return 1


@component.add(
    name="Eddy diff coeff M 1",
    units="Meter*Meter/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"eddy_diff_coeff_index_m_1": 1, "eddy_diff_coeff_mean_m_1": 1},
)
def eddy_diff_coeff_m_1():
    """
    Coefficient of carbon diffusion to the first layer of deep ocean.
    """
    return eddy_diff_coeff_index_m_1() * eddy_diff_coeff_mean_m_1()


@component.add(
    name="Eddy diff coeff mean 1 2",
    units="Meter*Meter/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def eddy_diff_coeff_mean_1_2():
    """
    Expected value at which carbon is mixed in the ocean due to eddy motion.
    """
    return 4400


@component.add(
    name="Eddy diff coeff mean 2 3",
    units="Meter*Meter/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def eddy_diff_coeff_mean_2_3():
    """
    Expected value at which carbon is mixed in the ocean due to eddy motion.
    """
    return 4400


@component.add(
    name="Eddy diff coeff mean 3 4",
    units="Meter*Meter/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def eddy_diff_coeff_mean_3_4():
    """
    Expected value at which carbon is mixed in the ocean due to eddy motion.
    """
    return 4400


@component.add(
    name="Eddy diff coeff mean M 1",
    units="Meter*Meter/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def eddy_diff_coeff_mean_m_1():
    """
    Expected value at which carbon is mixed in the ocean due to eddy motion.
    """
    return 4400


@component.add(
    name="Effect of Temp on C Flux Atm ML",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "sensitivity_of_c_flux_to_temp": 1,
        "temperature_change_from_preindustrial": 1,
    },
)
def effect_of_temp_on_c_flux_atm_ml():
    return 1 - sensitivity_of_c_flux_to_temp() * temperature_change_from_preindustrial()


@component.add(
    name="Effectiveness of Pressure to Adjust C Emission",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effectiveness_of_pressure_to_adjust_c_emission_variation": 1,
        "time": 1,
    },
)
def effectiveness_of_pressure_to_adjust_c_emission():
    """
    Rate at which the gap between acceptable and current carbon emission from fossil fuels level is addressed.
    """
    return 0.07 + step(
        __data["time"],
        effectiveness_of_pressure_to_adjust_c_emission_variation() - 0.07,
        2020,
    )


@component.add(
    name="Effectiveness of Pressure to Adjust C Emission Variation",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effectiveness_of_pressure_to_adjust_c_emission_variation():
    """
    Rate at which the gap between acceptable and current carbon emission from fossil fuels level is addressed.
    """
    return 0.07


@component.add(
    name="Emission from Fossil Fuels per Capita",
    units="TonC/(Year*Person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_c_emission_from_fossil_fuels": 1, "population": 1},
)
def emission_from_fossil_fuels_per_capita():
    """
    Carbon emission from energy production and it use per capita.
    """
    return total_c_emission_from_fossil_fuels() / population()


@component.add(
    name="Emission per Capita",
    units="TonC/(Year*Person)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_c_emission": 1, "population": 1},
)
def emission_per_capita():
    """
    Emissions of carbon from energy use and other sources per capita.
    """
    return total_c_emission() / population()


@component.add(
    name="Emission shock year",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_shock_year():
    return 2020


@component.add(
    name="Equil C in Mixed Layer",
    units="TonC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "preindustrial_c_in_mixed_layer": 1,
        "effect_of_temp_on_c_flux_atm_ml": 1,
        "c_in_atmosphere": 1,
        "preindustrial_c_in_atmosphere": 1,
        "buffer_factor": 1,
    },
)
def equil_c_in_mixed_layer():
    """
    Equilibrium carbon content of mixed layer.
    """
    return (
        preindustrial_c_in_mixed_layer()
        * effect_of_temp_on_c_flux_atm_ml()
        * (c_in_atmosphere() / preindustrial_c_in_atmosphere()) ** (1 / buffer_factor())
    )


@component.add(
    name="Equilibrium C per meter in Mixed Layer",
    units="TonC/Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"equil_c_in_mixed_layer": 1, "mixed_layer_depth": 1},
)
def equilibrium_c_per_meter_in_mixed_layer():
    return equil_c_in_mixed_layer() / mixed_layer_depth()


@component.add(
    name="Flux Atmosphere to Biomass",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_net_primary_production": 1,
        "c_in_atmosphere": 1,
        "biostimulation_coefficient": 1,
        "preindustrial_c_in_atmosphere": 1,
    },
)
def flux_atmosphere_to_biomass():
    """
    Carbon flux from atmosphere to biosphere (from primary production)
    """
    return initial_net_primary_production() * (
        1
        + biostimulation_coefficient()
        * float(np.log(c_in_atmosphere() / preindustrial_c_in_atmosphere()))
    )


@component.add(
    name="Flux Atmosphere to Ocean",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"equil_c_in_mixed_layer": 1, "c_in_mixed_layer": 1, "mixing_time": 1},
)
def flux_atmosphere_to_ocean():
    """
    Carbon flux from atmosphere to mixed ocean layer.
    """
    return (equil_c_in_mixed_layer() - c_in_mixed_layer()) / mixing_time()


@component.add(
    name="Flux Biomass to Atmosphere",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_biomass": 1, "biomass_res_time": 1, "humification_fraction": 1},
)
def flux_biomass_to_atmosphere():
    """
    Carbon flux from biomass to atmosphere.
    """
    return (c_in_biomass() / biomass_res_time()) * (1 - humification_fraction())


@component.add(
    name="Flux Biomass to Humus",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_biomass": 1, "biomass_res_time": 1, "humification_fraction": 1},
)
def flux_biomass_to_humus():
    """
    Carbon flux from biomass to humus.
    """
    return (c_in_biomass() / biomass_res_time()) * humification_fraction()


@component.add(
    name="Flux Humus to Atmosphere",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_humus": 1, "humus_res_time": 1},
)
def flux_humus_to_atmosphere():
    """
    Carbon flux from humus to atmosphere.
    """
    return c_in_humus() / humus_res_time()


@component.add(
    name="Forest Land Change",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"forest_land": 1, "init_forest_land": 1},
)
def forest_land_change():
    """
    Ratio of forest land area change compared to its initial area in year 1900.
    """
    return forest_land() / init_forest_land()


@component.add(
    name="GtC to TonC", units="TonC/GtC", comp_type="Constant", comp_subtype="Normal"
)
def gtc_to_tonc():
    """
    1 GtC equals 1000000000 tons of carbon
    """
    return 1000000000.0


@component.add(
    name="Humification Fraction",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def humification_fraction():
    """
    Fraction of carbon outflow from biomass that enters humus stock.
    """
    return 0.428


@component.add(
    name="Humus Res Time", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def humus_res_time():
    """
    Average carbon residence time in humus.
    """
    return 27.8


@component.add(
    name="Inflow CCSICLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pressure_ccsic": 1},
)
def inflow_ccsiclv1():
    return pressure_ccsic()


@component.add(
    name="Inflow CCSICLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ccsiclv1": 1},
)
def inflow_ccsiclv2():
    return outflow_ccsiclv1()


@component.add(
    name="Inflow CCSICLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ccsiclv2": 1},
)
def inflow_ccsiclv3():
    return outflow_ccsiclv2()


@component.add(
    name="INIT C in Atmosphere",
    units="TonC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"atmospheric_co2_law_dome_1850": 1, "gtc_to_tonc": 1, "ppm_to_gtc": 1},
)
def init_c_in_atmosphere():
    """
    Initial carbon in atmosphere.
    """
    return atmospheric_co2_law_dome_1850() * gtc_to_tonc() * ppm_to_gtc()


@component.add(
    name="INIT C in Biomass",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_init_c_in_biomass": 1},
    other_deps={
        "_initial_init_c_in_biomass": {
            "initial": {"flux_atmosphere_to_biomass": 1, "biomass_res_time": 1},
            "step": {},
        }
    },
)
def init_c_in_biomass():
    """
    Initial carbon in biomass.
    """
    return _initial_init_c_in_biomass()


_initial_init_c_in_biomass = Initial(
    lambda: flux_atmosphere_to_biomass() * biomass_res_time(),
    "_initial_init_c_in_biomass",
)


@component.add(
    name="INIT C in Deep Ocean 1",
    units="TonC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"init_c_in_deep_ocean_per_meter": 1, "layer_depth_1": 1},
)
def init_c_in_deep_ocean_1():
    """
    Initial carbon in the first layer of deep ocean. was constant at 3.115e+012 in the earlier versions of the model.
    """
    return init_c_in_deep_ocean_per_meter() * layer_depth_1()


@component.add(
    name="INIT C in Deep Ocean 2",
    units="TonC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"init_c_in_deep_ocean_per_meter": 1, "layer_depth_2": 1},
)
def init_c_in_deep_ocean_2():
    """
    Initial carbon in the second layer of deep ocean. was constant at 3.099e+012 in earlier versions of the model
    """
    return init_c_in_deep_ocean_per_meter() * layer_depth_2()


@component.add(
    name="INIT C in Deep Ocean 3",
    units="TonC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"init_c_in_deep_ocean_per_meter": 1, "layer_depth_3": 1},
)
def init_c_in_deep_ocean_3():
    """
    Initial carbon in the third layer of deep ocean. was constant at 1.3356e+013 in earlier versions of the model
    """
    return init_c_in_deep_ocean_per_meter() * layer_depth_3()


@component.add(
    name="INIT C in Deep Ocean 4",
    units="TonC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"init_c_in_deep_ocean_per_meter": 1, "layer_depth_4": 1},
)
def init_c_in_deep_ocean_4():
    """
    Initial carbon in the fourth layer of deep ocean. was constant at 1.8477e+013 in earlier versions of the model.
    """
    return init_c_in_deep_ocean_per_meter() * layer_depth_4()


@component.add(
    name="Init C in Deep Ocean per meter",
    units="TonC/Meter",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_init_c_in_deep_ocean_per_meter": 1},
    other_deps={
        "_initial_init_c_in_deep_ocean_per_meter": {
            "initial": {"equilibrium_c_per_meter_in_mixed_layer": 1},
            "step": {},
        }
    },
)
def init_c_in_deep_ocean_per_meter():
    return _initial_init_c_in_deep_ocean_per_meter()


_initial_init_c_in_deep_ocean_per_meter = Initial(
    lambda: equilibrium_c_per_meter_in_mixed_layer(),
    "_initial_init_c_in_deep_ocean_per_meter",
)


@component.add(
    name="INIT C in Humus",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_init_c_in_humus": 1},
    other_deps={
        "_initial_init_c_in_humus": {
            "initial": {"flux_biomass_to_humus": 1, "humus_res_time": 1},
            "step": {},
        }
    },
)
def init_c_in_humus():
    """
    Inital carbon in humus.
    """
    return _initial_init_c_in_humus()


_initial_init_c_in_humus = Initial(
    lambda: flux_biomass_to_humus() * humus_res_time(), "_initial_init_c_in_humus"
)


@component.add(
    name="INIT C in Mixed Ocean",
    units="TonC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_c_in_mixed_ocean():
    """
    Initial carbon in mixed ocean layer.
    """
    return 901800000000.0


@component.add(name="INIT CCS Improvement", comp_type="Constant", comp_subtype="Normal")
def init_ccs_improvement():
    return 0


@component.add(
    name="Initial Net Primary Production",
    units="TonC/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_net_primary_production():
    """
    Initial net primary production.
    """
    return 85177100000.0


@component.add(
    name="Land Mitigation Policy Multiplier",
    units="1",
    comp_type="Constant",
    comp_subtype="Normal",
)
def land_mitigation_policy_multiplier():
    return 0.5


@component.add(
    name="Land Mitigation Policy Transition Period",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def land_mitigation_policy_transition_period():
    return 20


@component.add(
    name="Land Use as Share of Total C Emission",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_emission_from_land_use": 1, "total_c_emission": 1},
)
def land_use_as_share_of_total_c_emission():
    """
    Carbon emission from forest and agricultural land use change as a percentage of total carbon emission.
    """
    return (c_emission_from_land_use() / total_c_emission()) * 100


@component.add(
    name="Layer Depth 1", units="Meter", comp_type="Constant", comp_subtype="Normal"
)
def layer_depth_1():
    """
    Depth of the first ocean layer.
    """
    return 300


@component.add(
    name="Layer Depth 2", units="Meter", comp_type="Constant", comp_subtype="Normal"
)
def layer_depth_2():
    """
    Depth of the second ocean layer.
    """
    return 300


@component.add(
    name="Layer Depth 3", units="Meter", comp_type="Constant", comp_subtype="Normal"
)
def layer_depth_3():
    """
    Depth of the third ocean layer.
    """
    return 1300


@component.add(
    name="Layer Depth 4", units="Meter", comp_type="Constant", comp_subtype="Normal"
)
def layer_depth_4():
    """
    Depth of the fourth ocean layer.
    """
    return 1800


@component.add(
    name="Layer Time Constant 1 2",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"layer_depth_2": 2, "layer_depth_1": 1, "eddy_diff_coeff_1_2": 1},
)
def layer_time_constant_1_2():
    """
    Time constant of exchange between the first and the second ocean layers.
    """
    return layer_depth_2() / (
        eddy_diff_coeff_1_2() / ((layer_depth_1() + layer_depth_2()) / 2)
    )


@component.add(
    name="Layer Time Constant 2 3",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"layer_depth_3": 2, "layer_depth_2": 1, "eddy_diff_coeff_2_3": 1},
)
def layer_time_constant_2_3():
    """
    Time constant of exchange between the second and the third ocean layers.
    """
    return layer_depth_3() / (
        eddy_diff_coeff_2_3() / ((layer_depth_2() + layer_depth_3()) / 2)
    )


@component.add(
    name="Layer Time Constant 3 4",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"layer_depth_4": 2, "layer_depth_3": 1, "eddy_diff_coeff_3_4": 1},
)
def layer_time_constant_3_4():
    """
    Time constant of exchange between the third and the fourth ocean layers.
    """
    return layer_depth_4() / (
        eddy_diff_coeff_3_4() / ((layer_depth_3() + layer_depth_4()) / 2)
    )


@component.add(
    name="Layer Time Constant M 1",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"layer_depth_1": 2, "eddy_diff_coeff_m_1": 1, "mixed_layer_depth": 1},
)
def layer_time_constant_m_1():
    """
    Time constant of exchange between mixed and the first ocean layers.
    """
    return layer_depth_1() / (
        eddy_diff_coeff_m_1() / ((mixed_layer_depth() + layer_depth_1()) / 2)
    )


@component.add(
    name="Marginal emission",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"emission_shock_year": 1, "year_period": 1, "time": 1},
)
def marginal_emission():
    return 1000000000.0 * pulse(
        __data["time"], emission_shock_year(), width=year_period()
    )


@component.add(
    name="MAX CCS Improvement Factor",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_ccs_improvement_factor():
    """
    Max impact of carbon capture and storage on carbon intensity of emissions from fossil fuels.
    """
    return 1


@component.add(
    name="Mean Depth of Adjacent 1 2 Layers",
    units="Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"layer_depth_1": 1, "layer_depth_2": 1},
)
def mean_depth_of_adjacent_1_2_layers():
    """
    Mean depth of the first and the second ocean layers.
    """
    return (layer_depth_1() + layer_depth_2()) / 2


@component.add(
    name="Mean Depth of Adjacent 2 3 Layers",
    units="Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"layer_depth_2": 1, "layer_depth_3": 1},
)
def mean_depth_of_adjacent_2_3_layers():
    """
    Mean depth of the second and the third ocean layers.
    """
    return (layer_depth_2() + layer_depth_3()) / 2


@component.add(
    name="Mean Depth of Adjacent 3 4 Layers",
    units="Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"layer_depth_3": 1, "layer_depth_4": 1},
)
def mean_depth_of_adjacent_3_4_layers():
    """
    Mean depth of the third and the fourth ocean layers.
    """
    return (layer_depth_3() + layer_depth_4()) / 2


@component.add(
    name="Mean Depth of Adjacent M 1 Layers",
    units="Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mixed_layer_depth": 1, "layer_depth_1": 1},
)
def mean_depth_of_adjacent_m_1_layers():
    """
    Mean depth of mixed and the first ocean layers.
    """
    return (mixed_layer_depth() + layer_depth_1()) / 2


@component.add(
    name="MIN CCS Improvement Factor",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def min_ccs_improvement_factor():
    """
    Min impact of carbon capture and storage on carbon intensity of emissions from fossil fuels.
    """
    return 0


@component.add(
    name="Mixed Layer Depth", units="Meter", comp_type="Constant", comp_subtype="Normal"
)
def mixed_layer_depth():
    """
    Mixed ocean layer depth.
    """
    return 100


@component.add(
    name="Mixing Time", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def mixing_time():
    """
    Atmosphere - mixed ocean layer mixing time.
    """
    return 1


@component.add(
    name="Mtoe to GJ", units="GJ/Mtoe", comp_type="Constant", comp_subtype="Normal"
)
def mtoe_to_gj():
    """
    Conversion from Mtoe to GJ.
    """
    return 41868000.0


@component.add(
    name="Normal C Intensity of Emission from Coal",
    units="TonC/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"normal_carbon_emissions_of_coal": 1},
)
def normal_c_intensity_of_emission_from_coal():
    """
    Initial carbon intensity of production from coal technologies.
    """
    return normal_carbon_emissions_of_coal()


@component.add(
    name="Normal C Intensity of Emission from Gas",
    units="TonC/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"normal_carbon_emissions_of_gas": 1},
)
def normal_c_intensity_of_emission_from_gas():
    """
    Initial carbon intensity of production from gas technologies.
    """
    return normal_carbon_emissions_of_gas()


@component.add(
    name="Normal C Intensity of Emission from Oil",
    units="TonC/Mtoe",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"normal_carbon_emissions_of_oil": 1},
)
def normal_c_intensity_of_emission_from_oil():
    """
    Initial carbon intensity of production from oil technologies.
    """
    return normal_carbon_emissions_of_oil()


@component.add(
    name="Normal Carbon Emissions of Coal",
    units="TonC/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_carbon_emissions_of_coal():
    """
    Felix1: 640000 IPCC: med: 9.5366e+006 min:8606200 Brian Felix 1.08e+006
    """
    return 1080000.0


@component.add(
    name="Normal Carbon Emissions of Gas",
    units="TonC/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_carbon_emissions_of_gas():
    """
    Felix1: 1.08e+006 IPCC: med: 5.6987e+006 min:4768300 Felix Brian: 640000
    """
    return 640000


@component.add(
    name="Normal Carbon Emissions of Oil",
    units="TonC/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_carbon_emissions_of_oil():
    """
    Felix1: 836500 IPCC: 9.04814e+006 co2
    """
    return 836500


@component.add(
    name="Outflow CCSICLV1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_improvement_change_lv1": 1, "delay_time_ccsic": 1},
)
def outflow_ccsiclv1():
    return ccs_improvement_change_lv1() / delay_time_ccsic()


@component.add(
    name="Outflow CCSICLV2",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_improvement_change_lv2": 1, "delay_time_ccsic": 1},
)
def outflow_ccsiclv2():
    return ccs_improvement_change_lv2() / delay_time_ccsic()


@component.add(
    name="Outflow CCSICLV3",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ccs_improvement_change_lv3": 1, "delay_time_ccsic": 1},
)
def outflow_ccsiclv3():
    return ccs_improvement_change_lv3() / delay_time_ccsic()


@component.add(
    name="ppm to GtC", units="GtC/ppm", comp_type="Constant", comp_subtype="Normal"
)
def ppm_to_gtc():
    """
    1 ppm by volume of atmosphere CO2 equals 2.13 GtC
    """
    return 2.13


@component.add(
    name="Preindustrial C in Atmosphere",
    units="TonC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def preindustrial_c_in_atmosphere():
    """
    Preindustrial carbon content of atmosphere.
    """
    return 590000000000.0


@component.add(
    name="Preindustrial C in Mixed Layer",
    units="TonC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"preindustrial_ocean_c_per_meter": 1, "mixed_layer_depth": 1},
)
def preindustrial_c_in_mixed_layer():
    """
    Initial carbon content of mixed ocean layer.
    """
    return preindustrial_ocean_c_per_meter() * mixed_layer_depth()


@component.add(
    name="Preindustrial Ocean C per meter",
    units="TonC/m",
    comp_type="Constant",
    comp_subtype="Normal",
)
def preindustrial_ocean_c_per_meter():
    """
    Preindustrial carbon content in ocean per meter.
    """
    return 9000000000.0


@component.add(
    name="Pressure CCSIC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "presure_to_adjust_total_c_emission_from_fossil_fuels": 1,
        "effectiveness_of_pressure_to_adjust_c_emission": 1,
    },
)
def pressure_ccsic():
    return (
        presure_to_adjust_total_c_emission_from_fossil_fuels()
        * effectiveness_of_pressure_to_adjust_c_emission()
    )


@component.add(
    name="Presure to Adjust Total C Emission from Fossil Fuels",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ccs_scenario": 1,
        "total_c_emission_from_fossil_fuels": 1,
        "desired_total_c_emission_from_fossil_fuels": 1,
        "c_emission_from_biomass_energy": 1,
    },
)
def presure_to_adjust_total_c_emission_from_fossil_fuels():
    """
    Pressure to adjust the level of carbon emission from fossil fuels is the emission level rises above the acceptable level.
    """
    return ccs_scenario() * float(
        np.maximum(
            0,
            (total_c_emission_from_fossil_fuels() + c_emission_from_biomass_energy())
            / desired_total_c_emission_from_fossil_fuels()
            - 1,
        )
    )


@component.add(
    name="Ref Buffer Factor", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def ref_buffer_factor():
    """
    Normal buffer factor.
    """
    return 9.7


@component.add(
    name="Reference C Emission from Agricultural Land Use",
    units="TonC/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_c_emission_from_agricultural_land_use():
    """
    Reference value of carbon emission from unit agricultural land change.
    """
    return 650000000.0


@component.add(
    name="Reference C Emission from Forest Land Use",
    units="TonC/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_c_emission_from_forest_land_use():
    """
    Reference value of carbon emission from unit forest land change.
    """
    return 450000000.0


@component.add(
    name="Reference CO2 Removal Rate",
    units="TonC/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_co2_removal_rate():
    return 37000000.0


@component.add(
    name="Sensitivity of C flux to temp",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sensitivity_of_c_flux_to_temp():
    return 0.003


@component.add(
    name="Shock emission addition",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"shock_scenario_switch": 1, "marginal_emission": 1, "co2_to_c": 1},
)
def shock_emission_addition():
    """
    1 Ton CO2 is equaivalent to 1 / 3.644
    """
    return if_then_else(
        shock_scenario_switch() == 0,
        lambda: 0,
        lambda: marginal_emission() / co2_to_c(),
    )


@component.add(
    name="Shock Scenario SWITCH",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def shock_scenario_switch():
    """
    0: no emission shock 1: there is an emission shock in the current year
    """
    return 0


@component.add(
    name="Terrestrial carbon sink",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"flux_atmosphere_to_biomass": 1, "flux_biomass_to_atmosphere": 1},
)
def terrestrial_carbon_sink():
    return flux_atmosphere_to_biomass() - flux_biomass_to_atmosphere()


@component.add(
    name="Time to Improve CCS",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_to_improve_ccs_variation": 1, "time": 1},
)
def time_to_improve_ccs():
    """
    Average CCS technology development lead time.
    """
    return 10 + step(__data["time"], time_to_improve_ccs_variation() - 10, 2020)


@component.add(
    name="Time to Improve CCS Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_to_improve_ccs_variation():
    """
    Average CCS technology development lead time.
    """
    return 10


@component.add(
    name="Ton C to kg CO2",
    units="kgCO2/TonC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ton_c_to_kg_co2():
    """
    Conversion from TonC to kgCO2.
    """
    return 3670


@component.add(
    name="TonCO2 to Million ton CO2",
    units="Million ton CO2/TonCO2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def tonco2_to_million_ton_co2():
    return 1 / 1000000.0


@component.add(
    name="Total Agirculture CO2 Emissions Indicator",
    units="Million ton CO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_co2_emissions_from_agriculture": 1,
        "tonco2_to_million_ton_co2": 1,
    },
)
def total_agirculture_co2_emissions_indicator():
    return total_co2_emissions_from_agriculture() * tonco2_to_million_ton_co2()


@component.add(
    name="Total Agricultural and Land Use C Emissions",
    units="TonC/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "c_emission_from_land_use": 1,
        "climate_policy_scenario": 1,
        "_smooth_total_agricultural_and_land_use_c_emissions": 1,
    },
    other_deps={
        "_smooth_total_agricultural_and_land_use_c_emissions": {
            "initial": {
                "land_mitigation_policy_multiplier": 1,
                "c_emission_from_land_use": 1,
                "climate_action_year": 2,
                "time": 1,
            },
            "step": {
                "land_mitigation_policy_multiplier": 1,
                "c_emission_from_land_use": 1,
                "climate_action_year": 2,
                "time": 1,
                "land_mitigation_policy_transition_period": 1,
            },
        }
    },
)
def total_agricultural_and_land_use_c_emissions():
    return float(
        np.maximum(
            0,
            c_emission_from_land_use()
            - climate_policy_scenario()
            * _smooth_total_agricultural_and_land_use_c_emissions(),
        )
    )


_smooth_total_agricultural_and_land_use_c_emissions = Smooth(
    lambda: ramp(
        __data["time"],
        land_mitigation_policy_multiplier() * c_emission_from_land_use(),
        climate_action_year(),
        climate_action_year() + 20,
    ),
    lambda: land_mitigation_policy_transition_period(),
    lambda: ramp(
        __data["time"],
        land_mitigation_policy_multiplier() * c_emission_from_land_use(),
        climate_action_year(),
        climate_action_year() + 20,
    ),
    lambda: 1,
    "_smooth_total_agricultural_and_land_use_c_emissions",
)


@component.add(
    name="Total C Emission",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_c_emission_from_the_energy_sector": 1,
        "total_agricultural_and_land_use_c_emissions": 1,
        "shock_emission_addition": 1,
    },
)
def total_c_emission():
    """
    Emissions of carbon from energy use and other sources.
    """
    return (
        total_c_emission_from_the_energy_sector()
        + total_agricultural_and_land_use_c_emissions()
        + shock_emission_addition()
    )


@component.add(
    name="Total C Emission from Fossil Fuels",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_emission_from_coal_energy": 1,
        "c_emission_from_gas_energy": 1,
        "c_emission_from_oil_energy": 1,
    },
)
def total_c_emission_from_fossil_fuels():
    """
    Source of historical data: Global Carbon Project 2020
    """
    return (
        c_emission_from_coal_energy()
        + c_emission_from_gas_energy()
        + c_emission_from_oil_energy()
    )


@component.add(
    name="Total C Emission from Renewables",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_emission_from_biomass_energy": 1,
        "c_emission_from_solar_energy": 1,
        "c_emission_from_wind_energy": 1,
    },
)
def total_c_emission_from_renewables():
    """
    Total carbon emission from renewable energy sources.
    """
    return (
        c_emission_from_biomass_energy()
        + c_emission_from_solar_energy()
        + c_emission_from_wind_energy()
    )


@component.add(
    name="Total C Emission from the Energy Sector",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_c_emission_from_fossil_fuels": 1,
        "total_c_emission_from_renewables": 1,
    },
)
def total_c_emission_from_the_energy_sector():
    """
    Total carbon emission from energy production and it use.
    """
    return total_c_emission_from_fossil_fuels() + total_c_emission_from_renewables()


@component.add(
    name="Total CO2 Emissions from Land Use",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_emission_from_land_use": 1, "co2_to_c": 1},
)
def total_co2_emissions_from_land_use():
    return c_emission_from_land_use() * co2_to_c()


@component.add(
    name="Total CO2 Emissions from the Energy Sector Indicator",
    units="Million ton CO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_c_emission_from_the_energy_sector": 1,
        "co2_to_c": 1,
        "tonco2_to_million_ton_co2": 1,
    },
)
def total_co2_emissions_from_the_energy_sector_indicator():
    return (
        total_c_emission_from_the_energy_sector()
        * co2_to_c()
        * tonco2_to_million_ton_co2()
    )


@component.add(
    name="Total CO2 Emissions Indicator",
    units="Million ton CO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_c_emission": 1,
        "carbon_removal_rate": 1,
        "co2_to_c": 1,
        "tonco2_to_million_ton_co2": 1,
    },
)
def total_co2_emissions_indicator():
    return (
        (total_c_emission() - carbon_removal_rate())
        * co2_to_c()
        * tonco2_to_million_ton_co2()
    )


@component.add(
    name="Total Land Use CO2 Emissions Indicator",
    units="Million ton CO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_emissions_from_land_use": 1, "tonco2_to_million_ton_co2": 1},
)
def total_land_use_co2_emissions_indicator():
    return total_co2_emissions_from_land_use() * tonco2_to_million_ton_co2()


@component.add(
    name="Total Renewable Energy Production",
    units="Mtoe/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_energy_production": 1,
        "solar_energy_production": 1,
        "wind_energy_production": 1,
    },
)
def total_renewable_energy_production():
    return (
        biomass_energy_production()
        + solar_energy_production()
        + wind_energy_production()
    )
