"""
Module carbon_cycle
Translated using PySD version 3.14.3
"""

@component.add(
    name="Atmospheric CH4 Concentration 1900 AR6",
    units="ppb",
    comp_type="Constant",
    comp_subtype="Normal",
)
def atmospheric_ch4_concentration_1900_ar6():
    """
    https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_AnnexIII.p df pg 2141
    """
    return 925


@component.add(
    name="Atmospheric CO2 Concentration 1900 AR6",
    units="ppm",
    comp_type="Constant",
    comp_subtype="Normal",
)
def atmospheric_co2_concentration_1900_ar6():
    return 296.4


@component.add(
    name="Atmospheric CO2 Law Dome 1850",
    units="ppm",
    comp_type="Constant",
    comp_subtype="Normal",
)
def atmospheric_co2_law_dome_1850():
    """
    Historical CO2 record derived from a spline fit (20 year cutoff) of the Law Dome DE08 and DE08-2 ice cores for year 1850 https://www.ncei.noaa.gov/pub/data/paleo/icecore/antarctica/law/law_co2.txt
    """
    return 284.7


@component.add(
    name="Atmospheric Concentration CH4",
    units="ppb",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_in_atmosphere": 1, "tonch4_to_ppb": 1},
)
def atmospheric_concentration_ch4():
    return ch4_in_atmosphere() * tonch4_to_ppb()


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
    name="Atmospheric Concentration N2O",
    units="ppb",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n2o_in_atmosphere": 1, "tonn2o_to_ppb": 1},
)
def atmospheric_concentration_n2o():
    return n2o_in_atmosphere() * tonn2o_to_ppb()


@component.add(
    name="Atmospheric Lifetime of CH4",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def atmospheric_lifetime_of_ch4():
    """
    9-12 Years 9.3
    """
    return 9.3


@component.add(
    name="Atmospheric Lifetime of N2O",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def atmospheric_lifetime_of_n2o():
    return 120


@component.add(
    name="Atmospheric N2O Concentration 1900 AR6",
    units="ppb",
    limits=(270.0, 290.0, 1.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def atmospheric_n2o_concentration_1900_ar6():
    """
    https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_AnnexIII.pdf pg 2141 278.9
    """
    return 278.9


@component.add(
    name="Baseline Natural Flux",
    units="TonN2O/Year",
    limits=(10000000.0, 20000000.0, 1000000.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def baseline_natural_flux():
    return 16500000.0


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
    name="C in Atmosphere",
    units="TonC",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_c_in_atmosphere": 1},
    other_deps={
        "_integ_c_in_atmosphere": {
            "initial": {"init_c_in_atmosphere": 1},
            "step": {
                "ch4_oxidation": 1,
                "flux_biomass_to_atmosphere": 1,
                "flux_humus_to_atmosphere": 1,
                "total_c_emission": 1,
                "carbon_removal_rate": 1,
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
    lambda: ch4_oxidation()
    + flux_biomass_to_atmosphere()
    + flux_humus_to_atmosphere()
    + total_c_emission()
    - carbon_removal_rate()
    - flux_atmosphere_to_biomass()
    - flux_atmosphere_to_ocean(),
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
                "flux_biomass_to_ch4": 1,
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
    - flux_biomass_to_ch4()
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
            "step": {
                "flux_biomass_to_humus": 1,
                "flux_humus_to_atmosphere": 1,
                "flux_humus_to_ch4": 1,
            },
        }
    },
)
def c_in_humus():
    """
    Carbon in humus.
    """
    return _integ_c_in_humus()


_integ_c_in_humus = Integ(
    lambda: flux_biomass_to_humus() - flux_humus_to_atmosphere() - flux_humus_to_ch4(),
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
    name="C to CH4", units="TonCH4/TonC", comp_type="Constant", comp_subtype="Normal"
)
def c_to_ch4():
    return 16 / 12


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
    name="CDR Policy Transition Period",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def cdr_policy_transition_period():
    return 1


@component.add(
    name="CH4 Concentration Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_in_atmosphere": 1, "init_ch4_in_atmosphere": 1},
)
def ch4_concentration_ratio():
    return ch4_in_atmosphere() / init_ch4_in_atmosphere()


@component.add(
    name="CH4 in Atmosphere",
    units="TonCH4",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_ch4_in_atmosphere": 1},
    other_deps={
        "_integ_ch4_in_atmosphere": {
            "initial": {"init_ch4_in_atmosphere": 1},
            "step": {"total_ch4_emission": 1, "total_ch4_breakdown": 1},
        }
    },
)
def ch4_in_atmosphere():
    return _integ_ch4_in_atmosphere()


_integ_ch4_in_atmosphere = Integ(
    lambda: total_ch4_emission() - total_ch4_breakdown(),
    lambda: init_ch4_in_atmosphere(),
    "_integ_ch4_in_atmosphere",
)


@component.add(
    name="CH4 Oxidation",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_to_co2_via_oxidation_in_tonc": 1},
)
def ch4_oxidation():
    return ch4_to_co2_via_oxidation_in_tonc()


@component.add(
    name="CH4 to CO2 via Oxidation in TonC",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "molar_mass_of_c": 1,
        "molar_mass_of_ch4": 1,
        "dmnl_adjustment_tonco2": 1,
        "total_ch4_breakdown": 1,
    },
)
def ch4_to_co2_via_oxidation_in_tonc():
    return (
        molar_mass_of_c() / molar_mass_of_ch4() / dmnl_adjustment_tonco2()
    ) * total_ch4_breakdown()


@component.add(
    name="CO2 to C", units="TonCO2/TonC", comp_type="Constant", comp_subtype="Normal"
)
def co2_to_c():
    return 3.664


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
    name="Dmnl Adjustment TonCO2",
    units="gC*TonCH4/(gCH4*TonC)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def dmnl_adjustment_tonco2():
    return 1


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
    name="Effect of Temperature on Land CH4 Flux",
    units="1/DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effect_of_temperature_on_land_ch4_flux():
    return 0.01


@component.add(
    name="Effect of Warming on CH4 Release from Biological Activity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effect_of_temperature_on_land_ch4_flux": 1,
        "temperature_change_from_preindustrial": 1,
    },
)
def effect_of_warming_on_ch4_release_from_biological_activity():
    return 1 / (
        1
        - effect_of_temperature_on_land_ch4_flux()
        * temperature_change_from_preindustrial()
    )


@component.add(
    name="Effect of Warming on N2O Release from Biological Activity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effective_sensitivity_of_temperature_on_n2o_flux": 1,
        "temperature_change_from_preindustrial": 1,
    },
)
def effect_of_warming_on_n2o_release_from_biological_activity():
    return (
        1
        + effective_sensitivity_of_temperature_on_n2o_flux()
        * temperature_change_from_preindustrial()
    )


@component.add(
    name="Effective Sensitivity of Temperature on N2O Flux",
    units="1/DegreesC",
    limits=(0.0, 0.04, 0.001),
    comp_type="Constant",
    comp_subtype="Normal",
)
def effective_sensitivity_of_temperature_on_n2o_flux():
    return 0.01


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
    name="Flux Biomass to CH4",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_biomass": 1,
        "effect_of_warming_on_ch4_release_from_biological_activity": 1,
        "fractional_rate_of_ch4_released_from_biomass_to_atm": 1,
    },
)
def flux_biomass_to_ch4():
    return (
        c_in_biomass()
        * effect_of_warming_on_ch4_release_from_biological_activity()
        * fractional_rate_of_ch4_released_from_biomass_to_atm()
    )


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
    name="Flux Humus to CH4",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "c_in_humus": 1,
        "fractional_rate_of_ch4_released_from_humus_to_atm": 1,
        "effect_of_warming_on_ch4_release_from_biological_activity": 1,
    },
)
def flux_humus_to_ch4():
    """
    Does not factor C release from Permafrost and Clathrate
    """
    return c_in_humus() * (
        fractional_rate_of_ch4_released_from_humus_to_atm()
        * effect_of_warming_on_ch4_release_from_biological_activity()
    )


@component.add(
    name="Fractional Rate of CH4 Released from Biomass to Atm",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fractional_rate_of_ch4_released_from_biomass_to_atm():
    return 1e-05


@component.add(
    name="Fractional Rate of CH4 Released from Humus to Atm",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def fractional_rate_of_ch4_released_from_humus_to_atm():
    return 0.00015


@component.add(
    name="GtC to TonC", units="TonC/GtC", comp_type="Constant", comp_subtype="Normal"
)
def gtc_to_tonc():
    """
    1 GtC equals 1000000000 tons of carbon
    """
    return 1000000000.0


@component.add(
    name="Hist Conc N2O",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def hist_conc_n2o():
    return np.interp(
        time(),
        [
            1900.0,
            1901.0,
            1902.0,
            1903.0,
            1904.0,
            1905.0,
            1906.0,
            1907.0,
            1908.0,
            1909.0,
            1910.0,
            1911.0,
            1912.0,
            1913.0,
            1914.0,
            1915.0,
            1916.0,
            1917.0,
            1918.0,
            1919.0,
            1920.0,
            1921.0,
            1922.0,
            1923.0,
            1924.0,
            1925.0,
            1926.0,
            1927.0,
            1928.0,
            1929.0,
            1930.0,
            1931.0,
            1932.0,
            1933.0,
            1934.0,
            1935.0,
            1936.0,
            1937.0,
            1938.0,
            1939.0,
            1940.0,
            1941.0,
            1942.0,
            1943.0,
            1944.0,
            1945.0,
            1946.0,
            1947.0,
            1948.0,
            1949.0,
            1950.0,
            1951.0,
            1952.0,
            1953.0,
            1954.0,
            1955.0,
            1956.0,
            1957.0,
            1958.0,
            1959.0,
            1960.0,
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
            2014.0,
        ],
        [
            279.454,
            279.613,
            279.861,
            280.156,
            280.432,
            280.705,
            280.98,
            281.276,
            281.611,
            281.95,
            282.314,
            282.721,
            283.019,
            283.362,
            283.716,
            284.047,
            284.312,
            284.615,
            284.805,
            284.851,
            284.929,
            285.039,
            285.17,
            285.467,
            285.605,
            285.652,
            285.692,
            285.74,
            285.833,
            285.891,
            285.938,
            286.124,
            286.222,
            286.371,
            286.467,
            286.587,
            286.747,
            286.951,
            287.191,
            287.387,
            287.619,
            287.864,
            288.138,
            288.781,
            289.0,
            289.227,
            289.427,
            289.511,
            289.556,
            289.598,
            289.739,
            289.86,
            290.025,
            290.334,
            290.548,
            290.844,
            291.187,
            291.512,
            291.772,
            291.987,
            292.283,
            292.602,
            292.945,
            293.327,
            293.685,
            294.045,
            294.453,
            294.86,
            295.269,
            295.681,
            296.098,
            296.522,
            296.955,
            297.399,
            297.855,
            298.326,
            298.814,
            299.319,
            299.845,
            300.393,
            300.965,
            301.562,
            302.187,
            302.842,
            303.528,
            304.247,
            305.002,
            305.793,
            306.624,
            307.831,
            308.683,
            309.233,
            309.725,
            310.099,
            310.808,
            311.279,
            312.298,
            313.183,
            313.907,
            314.709,
            315.759,
            316.493,
            317.101,
            317.73,
            318.357,
            319.13,
            319.933,
            320.646,
            321.575,
            322.275,
            323.141,
            324.159,
            325.005,
            325.919,
            326.988,
        ],
    )


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


@component.add(
    name="INIT CH4 in Atmosphere",
    units="TonCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"atmospheric_ch4_concentration_1900_ar6": 1, "tonch4_to_ppb": 1},
)
def init_ch4_in_atmosphere():
    return atmospheric_ch4_concentration_1900_ar6() / tonch4_to_ppb()


@component.add(
    name="INIT N2O in Atmosphere",
    units="TonN2O",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"atmospheric_n2o_concentration_1900_ar6": 1, "tonn2o_to_ppb": 1},
)
def init_n2o_in_atmosphere():
    return atmospheric_n2o_concentration_1900_ar6() / tonn2o_to_ppb()


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
    name="KtN2O to tN2O",
    units="TonN2O/KTonN2O",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ktn2o_to_tn2o():
    return 1000


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
    name="Molar mass of C", units="gC/mol", comp_type="Constant", comp_subtype="Normal"
)
def molar_mass_of_c():
    return 12.01


@component.add(
    name="Molar mass of CH4",
    units="gCH4/mol",
    comp_type="Constant",
    comp_subtype="Normal",
)
def molar_mass_of_ch4():
    return 16.04


@component.add(
    name="Molar mass of N2O",
    units="gN2O/mol",
    comp_type="Constant",
    comp_subtype="Normal",
)
def molar_mass_of_n2o():
    return 44.013


@component.add(
    name="Mt CH4 to tCH4",
    units="TonCH4/MTonCH4",
    comp_type="Constant",
    comp_subtype="Normal",
)
def mt_ch4_to_tch4():
    return 1000000.0


@component.add(
    name="N2O Concentration Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n2o_in_atmosphere": 1, "init_n2o_in_atmosphere": 1},
)
def n2o_concentration_ratio():
    return n2o_in_atmosphere() / init_n2o_in_atmosphere()


@component.add(
    name="N2O in Atmosphere",
    units="TonN2O",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_n2o_in_atmosphere": 1},
    other_deps={
        "_integ_n2o_in_atmosphere": {
            "initial": {"init_n2o_in_atmosphere": 1},
            "step": {"total_n2o_emission": 1, "total_n2o_breakdown": 1},
        }
    },
)
def n2o_in_atmosphere():
    return _integ_n2o_in_atmosphere()


_integ_n2o_in_atmosphere = Integ(
    lambda: total_n2o_emission() - total_n2o_breakdown(),
    lambda: init_n2o_in_atmosphere(),
    "_integ_n2o_in_atmosphere",
)


@component.add(
    name="Natural CH4 Emissions",
    units="TonCH4/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def natural_ch4_emissions():
    """
    There is a substantial discrepancy between estimates of natural global annual methane emissions from bottom-up and top-down methods, which yield values of 370 Mt and 215 Mt, respectively (Saunois et al. 2020). UNEP Global Methane Assessment 2030 Baseline Report
    """
    return 230000000.0


@component.add(
    name="Natural CH4 Emissions Flux Biosphere to CH4 Natural",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"flux_biomass_to_ch4": 1, "flux_humus_to_ch4": 1, "c_to_ch4": 1},
)
def natural_ch4_emissions_flux_biosphere_to_ch4_natural():
    return (flux_biomass_to_ch4() + flux_humus_to_ch4()) * c_to_ch4()


@component.add(
    name="Natural N2O Emission",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "baseline_natural_flux": 1,
        "effect_of_warming_on_n2o_release_from_biological_activity": 1,
    },
)
def natural_n2o_emission():
    return (
        baseline_natural_flux()
        * effect_of_warming_on_n2o_release_from_biological_activity()
    )


@component.add(
    name='"Non-Linear Lifetime of CH4"',
    units="Years",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2},
)
def nonlinear_lifetime_of_ch4():
    return (
        8
        + ramp(__data["time"], 0.01, 1900, 2000)
        - ramp(__data["time"], 0.02, 2000, 2100)
    )


@component.add(
    name='"Non-Linear Lifetime of N2O"',
    units="Years",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1},
)
def nonlinear_lifetime_of_n2o():
    return 135 - ramp(__data["time"], 0.3, 1900, 1950)


@component.add(name="ppb", units="ppb", comp_type="Constant", comp_subtype="Normal")
def ppb():
    return 1000000000.0


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
    name="Ref Buffer Factor", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def ref_buffer_factor():
    """
    Normal buffer factor.
    """
    return 9.7


@component.add(
    name="Reference CO2 Removal Rate",
    units="TonC/Year/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_co2_removal_rate():
    return 37000000.0


@component.add(
    name="Sensitivity of C flux to temp",
    units="1/DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sensitivity_of_c_flux_to_temp():
    return 0.003


@component.add(
    name="ss370 Conc CH4",
    units="ppb",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def ss370_conc_ch4():
    return np.interp(
        time(),
        [
            1900.0,
            1901.0,
            1902.0,
            1903.0,
            1904.0,
            1905.0,
            1906.0,
            1907.0,
            1908.0,
            1909.0,
            1910.0,
            1911.0,
            1912.0,
            1913.0,
            1914.0,
            1915.0,
            1916.0,
            1917.0,
            1918.0,
            1919.0,
            1920.0,
            1921.0,
            1922.0,
            1923.0,
            1924.0,
            1925.0,
            1926.0,
            1927.0,
            1928.0,
            1929.0,
            1930.0,
            1931.0,
            1932.0,
            1933.0,
            1934.0,
            1935.0,
            1936.0,
            1937.0,
            1938.0,
            1939.0,
            1940.0,
            1941.0,
            1942.0,
            1943.0,
            1944.0,
            1945.0,
            1946.0,
            1947.0,
            1948.0,
            1949.0,
            1950.0,
            1951.0,
            1952.0,
            1953.0,
            1954.0,
            1955.0,
            1956.0,
            1957.0,
            1958.0,
            1959.0,
            1960.0,
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
            2014.0,
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
            2100.0,
        ],
        [
            925.552,
            928.8,
            932.731,
            936.783,
            942.114,
            947.443,
            953.092,
            959.156,
            964.085,
            969.398,
            974.787,
            979.465,
            983.606,
            986.242,
            988.611,
            991.461,
            998.454,
            1003.57,
            1010.13,
            1017.63,
            1025.07,
            1032.2,
            1039.1,
            1045.13,
            1049.45,
            1052.16,
            1053.6,
            1055.77,
            1060.64,
            1066.66,
            1072.64,
            1077.49,
            1081.96,
            1086.54,
            1091.77,
            1097.08,
            1101.83,
            1106.32,
            1110.63,
            1116.91,
            1120.12,
            1123.24,
            1128.19,
            1132.66,
            1136.27,
            1139.32,
            1143.66,
            1149.64,
            1155.63,
            1160.35,
            1163.82,
            1168.81,
            1174.31,
            1183.36,
            1194.43,
            1206.65,
            1221.1,
            1235.8,
            1247.42,
            1257.32,
            1264.12,
            1269.46,
            1282.57,
            1300.79,
            1317.37,
            1331.06,
            1342.24,
            1354.27,
            1371.65,
            1389.34,
            1411.1,
            1431.12,
            1449.29,
            1462.86,
            1476.14,
            1491.74,
            1509.11,
            1527.68,
            1546.89,
            1566.16,
            1584.94,
            1602.65,
            1618.73,
            1632.62,
            1643.5,
            1655.91,
            1668.79,
            1683.75,
            1693.94,
            1705.63,
            1717.4,
            1729.33,
            1740.14,
            1743.1,
            1748.62,
            1755.23,
            1757.19,
            1761.5,
            1770.29,
            1778.2,
            1778.01,
            1776.53,
            1778.96,
            1783.59,
            1784.23,
            1783.36,
            1783.42,
            1788.95,
            1798.42,
            1802.1,
            1807.85,
            1813.07,
            1815.26,
            1822.58,
            1831.47,
            1841.93,
            1851.59,
            1874.51,
            1889.79,
            1905.45,
            1921.44,
            1937.74,
            1954.37,
            1971.4,
            1988.79,
            2006.51,
            2024.53,
            2042.82,
            2061.37,
            2080.15,
            2099.14,
            2118.32,
            2137.55,
            2156.7,
            2175.76,
            2194.75,
            2213.66,
            2232.5,
            2251.27,
            2269.97,
            2288.59,
            2307.15,
            2325.65,
            2344.1,
            2362.51,
            2380.87,
            2399.19,
            2417.46,
            2435.69,
            2453.87,
            2472.0,
            2490.08,
            2508.18,
            2526.34,
            2544.55,
            2562.82,
            2581.13,
            2599.48,
            2617.86,
            2636.26,
            2654.69,
            2673.13,
            2691.61,
            2710.12,
            2728.68,
            2747.26,
            2765.87,
            2784.5,
            2803.14,
            2821.8,
            2840.45,
            2859.11,
            2877.79,
            2896.52,
            2915.29,
            2934.08,
            2952.91,
            2971.75,
            2990.61,
            3009.48,
            3028.35,
            3047.22,
            3065.96,
            3084.46,
            3102.73,
            3120.78,
            3138.62,
            3156.25,
            3173.7,
            3190.97,
            3208.07,
            3225.01,
            3241.8,
            3258.48,
            3275.04,
            3291.48,
            3307.83,
            3324.06,
            3340.2,
            3356.24,
            3372.18,
        ],
    )


@component.add(
    name="ss370 Conc N2O",
    units="ppb",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def ss370_conc_n2o():
    return np.interp(
        time(),
        [
            1900.0,
            1901.0,
            1902.0,
            1903.0,
            1904.0,
            1905.0,
            1906.0,
            1907.0,
            1908.0,
            1909.0,
            1910.0,
            1911.0,
            1912.0,
            1913.0,
            1914.0,
            1915.0,
            1916.0,
            1917.0,
            1918.0,
            1919.0,
            1920.0,
            1921.0,
            1922.0,
            1923.0,
            1924.0,
            1925.0,
            1926.0,
            1927.0,
            1928.0,
            1929.0,
            1930.0,
            1931.0,
            1932.0,
            1933.0,
            1934.0,
            1935.0,
            1936.0,
            1937.0,
            1938.0,
            1939.0,
            1940.0,
            1941.0,
            1942.0,
            1943.0,
            1944.0,
            1945.0,
            1946.0,
            1947.0,
            1948.0,
            1949.0,
            1950.0,
            1951.0,
            1952.0,
            1953.0,
            1954.0,
            1955.0,
            1956.0,
            1957.0,
            1958.0,
            1959.0,
            1960.0,
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
            2014.0,
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
            2100.0,
        ],
        [
            279.454,
            279.613,
            279.861,
            280.156,
            280.432,
            280.705,
            280.98,
            281.276,
            281.611,
            281.95,
            282.314,
            282.721,
            283.019,
            283.362,
            283.716,
            284.047,
            284.312,
            284.615,
            284.805,
            284.851,
            284.929,
            285.039,
            285.17,
            285.467,
            285.605,
            285.652,
            285.692,
            285.74,
            285.833,
            285.891,
            285.938,
            286.124,
            286.222,
            286.371,
            286.467,
            286.587,
            286.747,
            286.951,
            287.191,
            287.387,
            287.619,
            287.864,
            288.138,
            288.781,
            289.0,
            289.227,
            289.427,
            289.511,
            289.556,
            289.598,
            289.739,
            289.86,
            290.025,
            290.334,
            290.548,
            290.844,
            291.187,
            291.512,
            291.772,
            291.987,
            292.283,
            292.602,
            292.945,
            293.327,
            293.685,
            294.045,
            294.453,
            294.86,
            295.269,
            295.681,
            296.098,
            296.522,
            296.955,
            297.399,
            297.855,
            298.326,
            298.814,
            299.319,
            299.845,
            300.393,
            300.965,
            301.562,
            302.187,
            302.842,
            303.528,
            304.247,
            305.002,
            305.793,
            306.624,
            307.831,
            308.683,
            309.233,
            309.725,
            310.099,
            310.808,
            311.279,
            312.298,
            313.183,
            313.907,
            314.709,
            315.759,
            316.493,
            317.101,
            317.73,
            318.357,
            319.13,
            319.933,
            320.646,
            321.575,
            322.275,
            323.141,
            324.159,
            325.005,
            325.919,
            326.988,
            328.18,
            329.076,
            329.791,
            330.565,
            331.356,
            332.164,
            332.989,
            333.83,
            334.684,
            335.552,
            336.432,
            337.327,
            338.234,
            339.154,
            340.088,
            341.034,
            341.993,
            342.963,
            343.941,
            344.928,
            345.924,
            346.928,
            347.941,
            348.962,
            349.991,
            351.029,
            352.075,
            353.128,
            354.187,
            355.253,
            356.325,
            357.403,
            358.487,
            359.577,
            360.674,
            361.776,
            362.884,
            363.998,
            365.116,
            366.238,
            367.364,
            368.495,
            369.63,
            370.77,
            371.913,
            373.061,
            374.212,
            375.368,
            376.528,
            377.691,
            378.858,
            380.028,
            381.203,
            382.38,
            383.562,
            384.747,
            385.935,
            387.127,
            388.322,
            389.52,
            390.721,
            391.924,
            393.131,
            394.341,
            395.553,
            396.769,
            397.987,
            399.208,
            400.434,
            401.663,
            402.897,
            404.134,
            405.375,
            406.62,
            407.868,
            409.12,
            410.376,
            411.636,
            412.898,
            414.165,
            415.434,
            416.707,
            417.982,
            419.261,
            420.544,
            421.829,
        ],
    )


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
    name="Ton to G CH4",
    units="gCH4/TonCH4",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ton_to_g_ch4():
    return 1000000.0


@component.add(
    name="Ton to g N2O",
    units="gN2O/TonN2O",
    comp_type="Constant",
    comp_subtype="Normal",
)
def ton_to_g_n2o():
    return 1000000.0


@component.add(
    name="TonCH4 to ppb",
    units="ppb/TonCH4",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ppb": 1,
        "ton_to_g_ch4": 1,
        "molar_mass_of_ch4": 1,
        "total_moles_of_air_in_atmosphere": 1,
    },
)
def tonch4_to_ppb():
    return (
        ppb()
        * ton_to_g_ch4()
        / molar_mass_of_ch4()
        / total_moles_of_air_in_atmosphere()
    )


@component.add(
    name="TonN2O to ppb",
    units="ppb/TonN2O",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ppb": 1,
        "ton_to_g_n2o": 1,
        "molar_mass_of_n2o": 1,
        "total_moles_of_air_in_atmosphere": 1,
    },
)
def tonn2o_to_ppb():
    return (
        ppb()
        * ton_to_g_n2o()
        / molar_mass_of_n2o()
        / total_moles_of_air_in_atmosphere()
    )


@component.add(
    name="Total C Emission",
    units="TonC/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_co2_emissions": 1, "co2_to_c": 1},
)
def total_c_emission():
    """
    Emissions of carbon from energy use and other sources.
    """
    return total_co2_emissions() * 1000000.0 / co2_to_c()


@component.add(
    name="Total CH4 Breakdown",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ch4_in_atmosphere": 1, "atmospheric_lifetime_of_ch4": 1},
)
def total_ch4_breakdown():
    """
    Oxidation Losses
    """
    return ch4_in_atmosphere() / atmospheric_lifetime_of_ch4()


@component.add(
    name="Total CH4 Emission",
    units="TonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_ch4_emissions": 1,
        "mt_ch4_to_tch4": 1,
        "natural_ch4_emissions_flux_biosphere_to_ch4_natural": 1,
    },
)
def total_ch4_emission():
    return (
        total_ch4_emissions() * mt_ch4_to_tch4()
        + natural_ch4_emissions_flux_biosphere_to_ch4_natural()
    )


@component.add(
    name="Total CO2 Emissions",
    units="TonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def total_co2_emissions():
    return np.interp(
        time(),
        [
            1900.0,
            1901.0,
            1902.0,
            1903.0,
            1904.0,
            1905.0,
            1906.0,
            1907.0,
            1908.0,
            1909.0,
            1910.0,
            1911.0,
            1912.0,
            1913.0,
            1914.0,
            1915.0,
            1916.0,
            1917.0,
            1918.0,
            1919.0,
            1920.0,
            1921.0,
            1922.0,
            1923.0,
            1924.0,
            1925.0,
            1926.0,
            1927.0,
            1928.0,
            1929.0,
            1930.0,
            1931.0,
            1932.0,
            1933.0,
            1934.0,
            1935.0,
            1936.0,
            1937.0,
            1938.0,
            1939.0,
            1940.0,
            1941.0,
            1942.0,
            1943.0,
            1944.0,
            1945.0,
            1946.0,
            1947.0,
            1948.0,
            1949.0,
            1950.0,
            1951.0,
            1952.0,
            1953.0,
            1954.0,
            1955.0,
            1956.0,
            1957.0,
            1958.0,
            1959.0,
            1960.0,
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
            2014.0,
            2100.0,
        ],
        [
            4465.96,
            4768.88,
            4835.69,
            5115.66,
            5244.75,
            5479.76,
            5710.02,
            6046.02,
            5993.61,
            6115.29,
            6271.03,
            6113.83,
            6122.58,
            6265.77,
            5938.95,
            5864.56,
            6101.45,
            6227.24,
            6205.49,
            5833.87,
            6290.31,
            6065.15,
            6219.54,
            6673.12,
            6735.34,
            6795.89,
            6766.33,
            7280.51,
            7308.5,
            7704.45,
            7679.53,
            7335.5,
            6651.92,
            6798.48,
            7038.37,
            7216.33,
            7612.65,
            7825.86,
            7580.8,
            7836.4,
            8156.9,
            8184.23,
            8268.32,
            8410.16,
            8377.77,
            7621.09,
            8344.52,
            9027.47,
            9393.94,
            9334.31,
            10044.7,
            11290.7,
            11518.8,
            11706.3,
            12085.4,
            12923.1,
            13695.2,
            14153.1,
            14642.0,
            14941.2,
            15353.9,
            15695.8,
            16083.7,
            16722.3,
            17266.3,
            17924.5,
            18518.2,
            19135.1,
            19720.5,
            20540.2,
            21457.0,
            21678.1,
            22109.2,
            23064.2,
            22861.4,
            22836.2,
            23873.4,
            24612.4,
            25215.4,
            25589.0,
            25266.7,
            24889.5,
            24681.5,
            25343.6,
            25945.1,
            26305.7,
            26803.4,
            27328.5,
            28027.4,
            28374.7,
            27966.7,
            28681.6,
            28688.8,
            28363.3,
            28376.7,
            28815.3,
            29248.0,
            32092.8,
            29798.2,
            29186.4,
            29661.9,
            29018.3,
            29933.4,
            30509.2,
            32433.5,
            33416.6,
            34631.9,
            35352.2,
            34451.2,
            34225.4,
            36133.8,
            37266.0,
            37953.9,
            38762.7,
            39630.9,
            39630.9,
        ],
    )


@component.add(
    name="Total moles of air in atmosphere",
    units="mol",
    comp_type="Constant",
    comp_subtype="Normal",
)
def total_moles_of_air_in_atmosphere():
    return 1.77e20


@component.add(
    name="Total N2O Breakdown",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"n2o_in_atmosphere": 1, "atmospheric_lifetime_of_n2o": 1},
)
def total_n2o_breakdown():
    return n2o_in_atmosphere() / atmospheric_lifetime_of_n2o()


@component.add(
    name="Total N2O Emission",
    units="TonN2O/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_n2o_emissions": 1,
        "ktn2o_to_tn2o": 1,
        "natural_n2o_emission": 1,
    },
)
def total_n2o_emission():
    return total_n2o_emissions() * ktn2o_to_tn2o() + natural_n2o_emission()
