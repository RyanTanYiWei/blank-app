"""
Module climate
Translated using PySD version 3.14.3
"""

@component.add(
    name="Area", units="Meter*Meter", comp_type="Constant", comp_subtype="Normal"
)
def area():
    """
    Global surface area.
    """
    return 510000000000000.0


@component.add(
    name="Atmospheric and Upper Ocean Heat Capacity",
    units="Year*W/(Meter*Meter*DegreesC)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"upper_layer_volume_vu": 1, "volumetric_heat_capacity": 1, "area": 1},
)
def atmospheric_and_upper_ocean_heat_capacity():
    """
    Volumetric heat capacity for the land, atmosphere, and, upper ocean layer.
    """
    return upper_layer_volume_vu() * volumetric_heat_capacity() / area()


@component.add(
    name="CH4 Radiative Forcing",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "ch4_radiative_forcing_history": 1,
        "ch4_radiative_forcing_rcp34": 1,
        "ch4_radiative_forcing_rcp45": 1,
        "ch4_radiative_forcing_rcp19": 1,
        "ch4_radiative_forcing_rcp26": 1,
        "ch4_radiative_forcing_rcp85": 1,
        "ch4_radiative_forcing_rcp60": 1,
        "rcp_scenario": 5,
    },
)
def ch4_radiative_forcing():
    """
    Radiative forcing from CH4 in the atmosphere.
    """
    return if_then_else(
        time() <= 2010,
        lambda: ch4_radiative_forcing_history(),
        lambda: if_then_else(
            rcp_scenario() == 0,
            lambda: ch4_radiative_forcing_rcp19(),
            lambda: if_then_else(
                rcp_scenario() == 1,
                lambda: ch4_radiative_forcing_rcp26(),
                lambda: if_then_else(
                    rcp_scenario() == 2,
                    lambda: ch4_radiative_forcing_rcp34(),
                    lambda: if_then_else(
                        rcp_scenario() == 3,
                        lambda: ch4_radiative_forcing_rcp45(),
                        lambda: if_then_else(
                            rcp_scenario() == 4,
                            lambda: ch4_radiative_forcing_rcp60(),
                            lambda: ch4_radiative_forcing_rcp85(),
                        ),
                    ),
                ),
            ),
        ),
    )


@component.add(
    name="CH4 Radiative Forcing History",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "dimensionless_time": 1, "table_ch4_radiative_forcing": 1},
)
def ch4_radiative_forcing_history():
    """
    Historical data for radiative forcing from CH4 in the atmosphere.
    """
    return table_ch4_radiative_forcing(time() * dimensionless_time())


@component.add(
    name="CH4 Radiative Forcing RCP19",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_ch4_radiative_forcing_ssp2_rcp19": 1,
    },
)
def ch4_radiative_forcing_rcp19():
    """
    Future projections of CH4 radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE-GLOBIOM (RCP 1.9).
    """
    return table_ch4_radiative_forcing_ssp2_rcp19(time() * dimensionless_time())


@component.add(
    name="CH4 Radiative Forcing RCP26",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_ch4_radiative_forcing_ssp2_rcp26": 1,
    },
)
def ch4_radiative_forcing_rcp26():
    """
    Future projections of CH4 radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE-GLOBIOM (RCP 2.6).
    """
    return table_ch4_radiative_forcing_ssp2_rcp26(time() * dimensionless_time())


@component.add(
    name="CH4 Radiative Forcing RCP34",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_ch4_radiative_forcing_ssp2_rcp34": 1,
    },
)
def ch4_radiative_forcing_rcp34():
    """
    Future projections of CH4 radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE (RCP 8.5).
    """
    return table_ch4_radiative_forcing_ssp2_rcp34(time() * dimensionless_time())


@component.add(
    name="CH4 Radiative Forcing RCP45",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_ch4_radiative_forcing_ssp2_rcp45": 1,
    },
)
def ch4_radiative_forcing_rcp45():
    """
    Future projections of CH4 radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE-GLOBIOM (RCP 4.5).
    """
    return table_ch4_radiative_forcing_ssp2_rcp45(time() * dimensionless_time())


@component.add(
    name="CH4 Radiative Forcing RCP60",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_ch4_radiative_forcing_ssp2_rcp60": 1,
    },
)
def ch4_radiative_forcing_rcp60():
    """
    Future projections of CH4 radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE-GLOBIOM (RCP 6.0).
    """
    return table_ch4_radiative_forcing_ssp2_rcp60(time() * dimensionless_time())


@component.add(
    name="CH4 Radiative Forcing RCP85",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_ch4_radiative_forcing_ssp2_rcp85": 1,
    },
)
def ch4_radiative_forcing_rcp85():
    """
    Future projections of CH4 radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE (RCP 8.5).
    """
    return table_ch4_radiative_forcing_ssp2_rcp85(time() * dimensionless_time())


@component.add(
    name="Climate Feedback Parameter",
    units="Watt/(Meter*Meter)/DegreesC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"nvs_2xco2_forcing": 1, "climate_sensitivity_to_2xco2": 1},
)
def climate_feedback_parameter():
    """
    Determines feedback effect from temperature increase.
    """
    return nvs_2xco2_forcing() / climate_sensitivity_to_2xco2()


@component.add(
    name="Climate Sensitivity to 2xCO2",
    units="DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_sensitivity_to_2xco2():
    """
    Equilibrium temperature change in response to a 2xCO2 equivalent change in radiative forcing. Deterministic = 3, Low=2, High =4.5.
    """
    return 3


@component.add(
    name="CO2 Radiative Forcing",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_radiative_forcing_coefficient": 1,
        "c_in_atmosphere": 1,
        "preindustrial_c_in_atmosphere": 1,
    },
)
def co2_radiative_forcing():
    """
    Radiative forcing from CO2 in the atmosphere. Source of Historical Data: IIASA RCP Database https://tntcat.iiasa.ac.at:8743/RcpDb/dsd?Action=htmlpage&page=welcome
    """
    return co2_radiative_forcing_coefficient() * float(
        np.log(c_in_atmosphere() / preindustrial_c_in_atmosphere())
    )


@component.add(
    name="CO2 Radiative Forcing AIM RCP60",
    units="W/(Meter*Meter)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def co2_radiative_forcing_aim_rcp60():
    """
    Future projections of CO2 radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by AIM (RCP 6.0).
    """
    return 0


@component.add(
    name="CO2 Radiative Forcing Coefficient",
    units="W/(m*m)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def co2_radiative_forcing_coefficient():
    """
    Coefficient to calculate forcing due to atmospheric gas using first-order approximation expression for carbon dioxide.
    """
    return 5.35


@component.add(
    name="CO2 Radiative Forcing IMAGE RCP26",
    units="W/(Meter*Meter)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def co2_radiative_forcing_image_rcp26():
    """
    Future projections of CO2 radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by IMAGE (RCP 2.6).
    """
    return 0


@component.add(
    name="CO2 Radiative Forcing Indicator",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_radiative_forcing": 1},
)
def co2_radiative_forcing_indicator():
    return co2_radiative_forcing()


@component.add(
    name="CO2 Radiative Forcing MESSAGE RCP85",
    units="W/(Meter*Meter)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def co2_radiative_forcing_message_rcp85():
    """
    Future projections of CO2 radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE (RCP 8.5).
    """
    return 0


@component.add(
    name="CO2 Radiative Forcing MiniCAM RCP45",
    units="W/(Meter*Meter)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def co2_radiative_forcing_minicam_rcp45():
    """
    Future projections of CO2 radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MiniCAM (RCP 4.5).
    """
    return 0


@component.add(
    name="Deep Ocean 1 Heat Capacity",
    units="Year*W/(Meter*Meter*DegreesC)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lower_layer_volume_vu_1": 1, "volumetric_heat_capacity": 1, "area": 1},
)
def deep_ocean_1_heat_capacity():
    """
    Volumetric heat capacity for the first layer of the deep ocean.
    """
    return lower_layer_volume_vu_1() * volumetric_heat_capacity() / area()


@component.add(
    name="Deep Ocean 2 Heat Capacity",
    units="Year*W/(Meter*Meter*DegreesC)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lower_layer_volume_vu_2": 1, "volumetric_heat_capacity": 1, "area": 1},
)
def deep_ocean_2_heat_capacity():
    """
    Volumetric heat capacity for the second layer of the deep ocean.
    """
    return lower_layer_volume_vu_2() * volumetric_heat_capacity() / area()


@component.add(
    name="Deep Ocean 3 Heat Capacity",
    units="Year*W/(Meter*Meter*DegreesC)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lower_layer_volume_vu_3": 1, "volumetric_heat_capacity": 1, "area": 1},
)
def deep_ocean_3_heat_capacity():
    """
    Volumetric heat capacity for the third layer of the deep ocean.
    """
    return lower_layer_volume_vu_3() * volumetric_heat_capacity() / area()


@component.add(
    name="Deep Ocean 4 Heat Capacity",
    units="Year*W/(Meter*Meter*DegreesC)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lower_layer_volume_vu_4": 1, "volumetric_heat_capacity": 1, "area": 1},
)
def deep_ocean_4_heat_capacity():
    """
    Volumetric heat capacity for the fourth layer of the deep ocean.
    """
    return lower_layer_volume_vu_4() * volumetric_heat_capacity() / area()


@component.add(
    name="Density", units="kg/(m*m*m)", comp_type="Constant", comp_subtype="Normal"
)
def density():
    """
    Density of water, i.e., mass per volume of water.
    """
    return 1000


@component.add(
    name="Dimensionless Time",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def dimensionless_time():
    """
    Parameter to make table data dimensionless.
    """
    return 1


@component.add(
    name="Effective Radiative Forcing",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_radiative_forcing": 1},
)
def effective_radiative_forcing():
    """
    Total radiative forcing from various factors in the atmosphere.
    """
    return total_radiative_forcing()


@component.add(
    name="Equilibrium Temperature",
    units="DegreesC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_radiative_forcing": 1, "climate_feedback_parameter": 1},
)
def equilibrium_temperature():
    """
    Ratio of Radiative Forcing to the Climate Feedback Parameter
    """
    return co2_radiative_forcing() / (climate_feedback_parameter() * float(np.log(2)))


@component.add(
    name="F Gases Radiative Forcing",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "f_gases_radiative_forcing_history": 1,
        "f_gases_radiative_forcing_rcp85": 1,
        "f_gases_radiative_forcing_rcp34": 1,
        "f_gases_radiative_forcing_rcp26": 1,
        "f_gases_radiative_forcing_rcp19": 1,
        "f_gases_radiative_forcing_rcp60": 1,
        "rcp_scenario": 5,
        "f_gases_radiative_forcing_rcp45": 1,
    },
)
def f_gases_radiative_forcing():
    """
    Radiative forcing from F-gases (HFC and others) in the atmosphere.
    """
    return if_then_else(
        time() <= 2010,
        lambda: f_gases_radiative_forcing_history(),
        lambda: if_then_else(
            rcp_scenario() == 0,
            lambda: f_gases_radiative_forcing_rcp19(),
            lambda: if_then_else(
                rcp_scenario() == 1,
                lambda: f_gases_radiative_forcing_rcp26(),
                lambda: if_then_else(
                    rcp_scenario() == 2,
                    lambda: f_gases_radiative_forcing_rcp34(),
                    lambda: if_then_else(
                        rcp_scenario() == 3,
                        lambda: f_gases_radiative_forcing_rcp45(),
                        lambda: if_then_else(
                            rcp_scenario() == 4,
                            lambda: f_gases_radiative_forcing_rcp60(),
                            lambda: f_gases_radiative_forcing_rcp85(),
                        ),
                    ),
                ),
            ),
        ),
    )


@component.add(
    name="F Gases Radiative Forcing History",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_f_gases_radiative_forcing": 1,
    },
)
def f_gases_radiative_forcing_history():
    """
    Historical data for radiative forcing from CH4 in the atmosphere.
    """
    return table_f_gases_radiative_forcing(time() * dimensionless_time())


@component.add(
    name="F Gases Radiative Forcing RCP19",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_f_gases_radiative_forcing_ssp2_rcp19": 1,
    },
)
def f_gases_radiative_forcing_rcp19():
    """
    Future projections of f-gases radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE-GLOBIOM (RCP 1.9).
    """
    return table_f_gases_radiative_forcing_ssp2_rcp19(time() * dimensionless_time())


@component.add(
    name="F Gases Radiative Forcing RCP26",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_f_gases_radiative_forcing_ssp2_rcp26": 1,
    },
)
def f_gases_radiative_forcing_rcp26():
    """
    Future projections of f-gases radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE-GLOBIOM (RCP 2.6).
    """
    return table_f_gases_radiative_forcing_ssp2_rcp26(time() * dimensionless_time())


@component.add(
    name="F Gases Radiative Forcing RCP34",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_f_gases_radiative_forcing_ssp2_rcp34": 1,
    },
)
def f_gases_radiative_forcing_rcp34():
    """
    Future projections of f gases radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE (RCP 8.5).
    """
    return table_f_gases_radiative_forcing_ssp2_rcp34(time() * dimensionless_time())


@component.add(
    name="F Gases Radiative Forcing RCP45",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_f_gases_radiative_forcing_ssp2_rcp45": 1,
    },
)
def f_gases_radiative_forcing_rcp45():
    """
    Future projections of f gases radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE-GLOBIOM (RCP 4.5).
    """
    return table_f_gases_radiative_forcing_ssp2_rcp45(time() * dimensionless_time())


@component.add(
    name="F Gases Radiative Forcing RCP60",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_f_gases_radiative_forcing_ssp2_rcp60": 1,
    },
)
def f_gases_radiative_forcing_rcp60():
    """
    Future projections of CH4 radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE-GLOBIOM (RCP 6.0).
    """
    return table_f_gases_radiative_forcing_ssp2_rcp60(time() * dimensionless_time())


@component.add(
    name="F Gases Radiative Forcing RCP85",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_f_gases_radiative_forcing_ssp2_rcp85": 1,
    },
)
def f_gases_radiative_forcing_rcp85():
    """
    Future projections of f gases radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE (RCP 8.5).
    """
    return table_f_gases_radiative_forcing_ssp2_rcp85(time() * dimensionless_time())


@component.add(
    name="Feedback Cooling",
    units="Watt/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "temperature_change_from_preindustrial": 1,
        "climate_feedback_parameter": 1,
    },
)
def feedback_cooling():
    """
    Feedback cooling of atmosphere/upper ocean system due to blackbody radiation.
    """
    return temperature_change_from_preindustrial() * climate_feedback_parameter()


@component.add(
    name="Heat Diffusion Covar",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def heat_diffusion_covar():
    """
    Heat transfer coefficient parameter.
    """
    return 1


@component.add(
    name="Heat in Atmosphere and Upper Ocean",
    units="Year*Watt/(Meter*Meter)",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_heat_in_atmosphere_and_upper_ocean": 1},
    other_deps={
        "_integ_heat_in_atmosphere_and_upper_ocean": {
            "initial": {
                "init_atmospheric_and_upper_ocean_temperature": 1,
                "atmospheric_and_upper_ocean_heat_capacity": 1,
            },
            "step": {
                "effective_radiative_forcing": 1,
                "feedback_cooling": 1,
                "heat_transfer_1": 1,
            },
        }
    },
)
def heat_in_atmosphere_and_upper_ocean():
    """
    Temperature of the atmosphere and the mixed ocean layer.
    """
    return _integ_heat_in_atmosphere_and_upper_ocean()


_integ_heat_in_atmosphere_and_upper_ocean = Integ(
    lambda: effective_radiative_forcing() - feedback_cooling() - heat_transfer_1(),
    lambda: init_atmospheric_and_upper_ocean_temperature()
    * atmospheric_and_upper_ocean_heat_capacity(),
    "_integ_heat_in_atmosphere_and_upper_ocean",
)


@component.add(
    name="Heat in Deep Ocean 1",
    units="Year*Watt/(Meter*Meter)",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_heat_in_deep_ocean_1": 1},
    other_deps={
        "_integ_heat_in_deep_ocean_1": {
            "initial": {
                "init_deep_ocean_1_temperature": 1,
                "deep_ocean_1_heat_capacity": 1,
            },
            "step": {"heat_transfer_1": 1, "heat_transfer_2": 1},
        }
    },
)
def heat_in_deep_ocean_1():
    """
    Heat content of the first layer of the deep ocean.
    """
    return _integ_heat_in_deep_ocean_1()


_integ_heat_in_deep_ocean_1 = Integ(
    lambda: heat_transfer_1() - heat_transfer_2(),
    lambda: init_deep_ocean_1_temperature() * deep_ocean_1_heat_capacity(),
    "_integ_heat_in_deep_ocean_1",
)


@component.add(
    name="Heat in Deep Ocean 2",
    units="Year*Watt/(Meter*Meter)",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_heat_in_deep_ocean_2": 1},
    other_deps={
        "_integ_heat_in_deep_ocean_2": {
            "initial": {
                "init_deep_ocean_2_temperature": 1,
                "deep_ocean_2_heat_capacity": 1,
            },
            "step": {"heat_transfer_2": 1, "heat_transfer_3": 1},
        }
    },
)
def heat_in_deep_ocean_2():
    """
    Heat content of the second layer of the deep ocean.
    """
    return _integ_heat_in_deep_ocean_2()


_integ_heat_in_deep_ocean_2 = Integ(
    lambda: heat_transfer_2() - heat_transfer_3(),
    lambda: init_deep_ocean_2_temperature() * deep_ocean_2_heat_capacity(),
    "_integ_heat_in_deep_ocean_2",
)


@component.add(
    name="Heat in Deep Ocean 3",
    units="Year*Watt/(Meter*Meter)",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_heat_in_deep_ocean_3": 1},
    other_deps={
        "_integ_heat_in_deep_ocean_3": {
            "initial": {
                "init_deep_ocean_3_temperature": 1,
                "deep_ocean_3_heat_capacity": 1,
            },
            "step": {"heat_transfer_3": 1, "heat_transfer_4": 1},
        }
    },
)
def heat_in_deep_ocean_3():
    """
    Heat content of the third layer of the deep ocean.
    """
    return _integ_heat_in_deep_ocean_3()


_integ_heat_in_deep_ocean_3 = Integ(
    lambda: heat_transfer_3() - heat_transfer_4(),
    lambda: init_deep_ocean_3_temperature() * deep_ocean_3_heat_capacity(),
    "_integ_heat_in_deep_ocean_3",
)


@component.add(
    name="Heat in Deep Ocean 4",
    units="Year*Watt/(Meter*Meter)",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_heat_in_deep_ocean_4": 1},
    other_deps={
        "_integ_heat_in_deep_ocean_4": {
            "initial": {
                "init_deep_ocean_4_temperature": 1,
                "deep_ocean_4_heat_capacity": 1,
            },
            "step": {"heat_transfer_4": 1},
        }
    },
)
def heat_in_deep_ocean_4():
    """
    Heat content of the fourth layer of the deep ocean.
    """
    return _integ_heat_in_deep_ocean_4()


_integ_heat_in_deep_ocean_4 = Integ(
    lambda: heat_transfer_4(),
    lambda: init_deep_ocean_4_temperature() * deep_ocean_4_heat_capacity(),
    "_integ_heat_in_deep_ocean_4",
)


@component.add(
    name="Heat to 2000m",
    units="Year*W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"heat_to_700m": 1, "heat_in_deep_ocean_3": 1},
)
def heat_to_2000m():
    """
    Heat to 2000m in deep ocean. Assumes default layer thicknesses, i.e., 100 m for the mixed ocean, 300 m each for layers 1 and 2, and 1300 m for layer 3.
    """
    return heat_to_700m() + heat_in_deep_ocean_3()


@component.add(
    name="Heat to 2000m J",
    units="Je22",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "heat_to_2000m": 1,
        "j_per_w_year": 1,
        "land_area_fraction": 1,
        "area": 1,
    },
)
def heat_to_2000m_j():
    """
    Heat to 2000m in Joules*1e22 for the area covered by water.
    """
    return heat_to_2000m() * j_per_w_year() * (area() * (1 - land_area_fraction()))


@component.add(
    name="Heat to 700m",
    units="Year*W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "heat_in_atmosphere_and_upper_ocean": 1,
        "land_area_fraction": 1,
        "heat_in_deep_ocean_1": 1,
        "heat_in_deep_ocean_2": 1,
    },
)
def heat_to_700m():
    """
    Sum of the heat in the atmosphere and upper ocean and that in the top two layers of the deep ocean. Assumes default layer thicknesses, i.e., 100 m for the mixed ocean and 300 m each for layers 1 and 2.
    """
    return (
        heat_in_atmosphere_and_upper_ocean() * (1 - land_area_fraction())
        + heat_in_deep_ocean_1()
        + heat_in_deep_ocean_2()
    )


@component.add(
    name="Heat to 700m J",
    units="Je22",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "heat_to_700m": 1,
        "j_per_w_year": 1,
        "land_area_fraction": 1,
        "area": 1,
        "offset_700m_heat": 1,
    },
)
def heat_to_700m_j():
    """
    Heat to 700 m in Joules*1e22 for the area covered by water. Source of Historical Data: NOAA – Ocean heat content anomalies; http://www.nodc.noaa.gov/OC5/3M_HEAT_CONTENT/ Levitus S., J. I. Antonov, T. P. Boyer, R. A. Locarnini, H. E. Garcia, and A. V. Mishonov, 2009. Global ocean heat content 1955-2008 in light of recently revealed instrumentation problems GRL, 36, L07608, doi:10.1029/2008GL037155.
    """
    return (
        heat_to_700m() * j_per_w_year() * (area() * (1 - land_area_fraction()))
        + offset_700m_heat()
    )


@component.add(
    name="Heat Transfer 1",
    units="Watt/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "temperature_change_from_preindustrial": 1,
        "relative_deep_1_ocean_temperature": 1,
        "heat_transfer_coefficient_1": 1,
        "mean_depth_of_adjacent_m_1_layers": 1,
    },
)
def heat_transfer_1():
    """
    Heat transfer from the atmosphere & upper ocean to the first layer of the deep ocean.
    """
    return (
        (temperature_change_from_preindustrial() - relative_deep_1_ocean_temperature())
        * heat_transfer_coefficient_1()
        / mean_depth_of_adjacent_m_1_layers()
    )


@component.add(
    name="Heat Transfer 2",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "relative_deep_1_ocean_temperature": 1,
        "relative_deep_2_ocean_temperature": 1,
        "heat_transfer_coefficient_2": 1,
        "mean_depth_of_adjacent_1_2_layers": 1,
    },
)
def heat_transfer_2():
    """
    Heat transfer from the first to the second layer of the deep ocean.
    """
    return (
        (relative_deep_1_ocean_temperature() - relative_deep_2_ocean_temperature())
        * heat_transfer_coefficient_2()
        / mean_depth_of_adjacent_1_2_layers()
    )


@component.add(
    name="Heat Transfer 3",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "relative_deep_2_ocean_temperature": 1,
        "relative_deep_3_ocean_temperature": 1,
        "heat_transfer_coefficient_3": 1,
        "mean_depth_of_adjacent_2_3_layers": 1,
    },
)
def heat_transfer_3():
    """
    Heat transfer from the second to the third layer of the deep ocean.
    """
    return (
        (relative_deep_2_ocean_temperature() - relative_deep_3_ocean_temperature())
        * heat_transfer_coefficient_3()
        / mean_depth_of_adjacent_2_3_layers()
    )


@component.add(
    name="Heat Transfer 4",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "relative_deep_3_ocean_temperature": 1,
        "relative_deep_4_ocean_temperature": 1,
        "heat_transfer_coefficient_4": 1,
        "mean_depth_of_adjacent_3_4_layers": 1,
    },
)
def heat_transfer_4():
    """
    Heat transfer from the third to the fourth layer of the deep ocean.
    """
    return (
        (relative_deep_3_ocean_temperature() - relative_deep_4_ocean_temperature())
        * heat_transfer_coefficient_4()
        / mean_depth_of_adjacent_3_4_layers()
    )


@component.add(
    name="Heat Transfer Coefficient 1",
    units="W/(Meter*DegreesC)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "heat_transfer_rate": 1,
        "mean_depth_of_adjacent_m_1_layers": 1,
        "eddy_diff_coeff_m_1": 1,
        "eddy_diff_coeff_mean_m_1": 1,
        "heat_diffusion_covar": 2,
    },
)
def heat_transfer_coefficient_1():
    """
    The ratio of the actual to the mean of the heat transfer coefficient, which controls the movement of heat through the climate sector.
    """
    return (heat_transfer_rate() * mean_depth_of_adjacent_m_1_layers()) * (
        heat_diffusion_covar() * (eddy_diff_coeff_m_1() / eddy_diff_coeff_mean_m_1())
        + (1 - heat_diffusion_covar())
    )


@component.add(
    name="Heat Transfer Coefficient 2",
    units="W/(Meter*DegreesC)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "heat_transfer_rate": 1,
        "mean_depth_of_adjacent_1_2_layers": 1,
        "heat_diffusion_covar": 2,
        "eddy_diff_coeff_mean_1_2": 1,
        "eddy_diff_coeff_1_2": 1,
    },
)
def heat_transfer_coefficient_2():
    """
    The ratio of the actual to the mean of the heat transfer coefficient, which controls the movement of heat through the climate sector.
    """
    return (heat_transfer_rate() * mean_depth_of_adjacent_1_2_layers()) * (
        heat_diffusion_covar() * (eddy_diff_coeff_1_2() / eddy_diff_coeff_mean_1_2())
        + (1 - heat_diffusion_covar())
    )


@component.add(
    name="Heat Transfer Coefficient 3",
    units="W/(Meter*DegreesC)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "heat_transfer_rate": 1,
        "mean_depth_of_adjacent_2_3_layers": 1,
        "eddy_diff_coeff_2_3": 1,
        "heat_diffusion_covar": 2,
        "eddy_diff_coeff_mean_2_3": 1,
    },
)
def heat_transfer_coefficient_3():
    """
    The ratio of the actual to the mean of the heat transfer coefficient, which controls the movement of heat through the climate sector.
    """
    return (heat_transfer_rate() * mean_depth_of_adjacent_2_3_layers()) * (
        heat_diffusion_covar() * (eddy_diff_coeff_2_3() / eddy_diff_coeff_mean_2_3())
        + (1 - heat_diffusion_covar())
    )


@component.add(
    name="Heat Transfer Coefficient 4",
    units="W/(Meter*DegreesC)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "heat_transfer_rate": 1,
        "mean_depth_of_adjacent_3_4_layers": 1,
        "eddy_diff_coeff_mean_3_4": 1,
        "eddy_diff_coeff_3_4": 1,
        "heat_diffusion_covar": 2,
    },
)
def heat_transfer_coefficient_4():
    """
    The ratio of the actual to the mean of the heat transfer coefficient, which controls the movement of heat through the climate sector.
    """
    return (heat_transfer_rate() * mean_depth_of_adjacent_3_4_layers()) * (
        heat_diffusion_covar() * (eddy_diff_coeff_3_4() / eddy_diff_coeff_mean_3_4())
        + (1 - heat_diffusion_covar())
    )


@component.add(
    name="Heat Transfer Rate",
    units="Watt/(Meter*Meter)/DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def heat_transfer_rate():
    """
    Rate of heat transfer between the surface and deep ocean.
    """
    return 1.23


@component.add(
    name="HFC Radiative Forcing",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "hfc_radiative_forcing_history": 1,
        "hfc_radiative_forcing_aim_rcp60": 1,
        "hfc_radiative_forcing_minicam_rcp45": 1,
        "hfc_radiative_forcing_image_rcp26": 1,
        "hfc_radiative_forcing_aim_rcp7": 1,
        "rcp_scenario": 4,
        "hfc_radiative_forcing_message_rcp85": 1,
    },
)
def hfc_radiative_forcing():
    """
    Radiative forcing from HFC in the atmosphere.
    """
    return if_then_else(
        time() < 2005,
        lambda: hfc_radiative_forcing_history(),
        lambda: if_then_else(
            rcp_scenario() == 1,
            lambda: hfc_radiative_forcing_image_rcp26(),
            lambda: if_then_else(
                rcp_scenario() == 2,
                lambda: hfc_radiative_forcing_minicam_rcp45(),
                lambda: if_then_else(
                    rcp_scenario() == 3,
                    lambda: hfc_radiative_forcing_aim_rcp60(),
                    lambda: if_then_else(
                        rcp_scenario() == 4,
                        lambda: hfc_radiative_forcing_message_rcp85(),
                        lambda: hfc_radiative_forcing_aim_rcp7(),
                    ),
                ),
            ),
        ),
    )


@component.add(
    name="HFC Radiative Forcing AIM RCP60",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_hfc_radiative_forcing_aim_rcp60": 1,
    },
)
def hfc_radiative_forcing_aim_rcp60():
    """
    Future projections of HFC radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by AIM (RCP 6.0).
    """
    return table_hfc_radiative_forcing_aim_rcp60(time() * dimensionless_time())


@component.add(
    name="HFC Radiative Forcing AIM RCP7",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_hfc_radiative_forcing_aim_ssp3_rcp7": 1,
    },
)
def hfc_radiative_forcing_aim_rcp7():
    """
    Future projections of CO2 radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE (RCP 8.5).
    """
    return table_hfc_radiative_forcing_aim_ssp3_rcp7(time() * dimensionless_time())


@component.add(
    name="HFC Radiative Forcing History",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "dimensionless_time": 1, "table_hfc_radiative_forcing": 1},
)
def hfc_radiative_forcing_history():
    """
    Historical data for radiative forcing from HFC in the atmosphere.
    """
    return table_hfc_radiative_forcing(time() * dimensionless_time())


@component.add(
    name="HFC Radiative Forcing IMAGE RCP26",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_hfc_radiative_forcing_image_rcp26": 1,
    },
)
def hfc_radiative_forcing_image_rcp26():
    """
    Future projections of HFC radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by IMAGE (RCP 2.6).
    """
    return table_hfc_radiative_forcing_image_rcp26(time() * dimensionless_time())


@component.add(
    name="HFC Radiative Forcing MESSAGE RCP85",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_hfc_radiative_forcing_message_rcp85": 1,
    },
)
def hfc_radiative_forcing_message_rcp85():
    """
    Future projections of CO2 radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE (RCP 8.5).
    """
    return table_hfc_radiative_forcing_message_rcp85(time() * dimensionless_time())


@component.add(
    name="HFC Radiative Forcing MiniCAM RCP45",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_hfc_radiative_forcing_minicam_rcp45": 1,
    },
)
def hfc_radiative_forcing_minicam_rcp45():
    """
    Future projections of HFC radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MiniCAM (RCP 4.5).
    """
    return table_hfc_radiative_forcing_minicam_rcp45(time() * dimensionless_time())


@component.add(
    name="INIT Atmospheric and Upper Ocean Temperature",
    units="DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_atmospheric_and_upper_ocean_temperature():
    """
    Initial value of Atmospheric and Upper Ocean Temperature.
    """
    return 0


@component.add(
    name="INIT Deep Ocean 1 Temperature",
    units="DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_deep_ocean_1_temperature():
    """
    Initial value of temperature in the first layer of deep ocean.
    """
    return 0


@component.add(
    name="INIT Deep Ocean 2 Temperature",
    units="DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_deep_ocean_2_temperature():
    """
    Initial value of temperature in the second layer of deep ocean.
    """
    return 0


@component.add(
    name="INIT Deep Ocean 3 Temperature",
    units="DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_deep_ocean_3_temperature():
    """
    Initial value of temperature in the third layer of deep ocean.
    """
    return 0


@component.add(
    name="INIT Deep Ocean 4 Temperature",
    units="DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_deep_ocean_4_temperature():
    """
    Initial value of temperature in the fourth layer of deep ocean.
    """
    return 0


@component.add(
    name="J per W Year",
    units="Je22/Watt/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def j_per_w_year():
    """
    Convertion from watts*year to Joules*1e22.
    """
    return 365 * 24 * 60 * 60 / 1e22


@component.add(
    name="Land Area Fraction", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def land_area_fraction():
    """
    Fraction of global surface area that is land.
    """
    return 0.292


@component.add(
    name="Land Thickness", units="Meter", comp_type="Constant", comp_subtype="Normal"
)
def land_thickness():
    """
    Effective land area heat capacity, expressed as equivalent water layer thickness.
    """
    return 8.4


@component.add(
    name="Lower Layer Volume Vu 1",
    units="Meter*Meter*Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"area": 1, "land_area_fraction": 1, "layer_depth_1": 1},
)
def lower_layer_volume_vu_1():
    """
    Water equivalent volume of the first layer of deep ocean.
    """
    return area() * (1 - land_area_fraction()) * layer_depth_1()


@component.add(
    name="Lower Layer Volume Vu 2",
    units="Meter*Meter*Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"area": 1, "land_area_fraction": 1, "layer_depth_2": 1},
)
def lower_layer_volume_vu_2():
    """
    Water equivalent volume of the second layer of deep ocean.
    """
    return area() * (1 - land_area_fraction()) * layer_depth_2()


@component.add(
    name="Lower Layer Volume Vu 3",
    units="Meter*Meter*Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"area": 1, "land_area_fraction": 1, "layer_depth_3": 1},
)
def lower_layer_volume_vu_3():
    """
    Water equivalent volume of the third layer of deep ocean.
    """
    return area() * (1 - land_area_fraction()) * layer_depth_3()


@component.add(
    name="Lower Layer Volume Vu 4",
    units="Meter*Meter*Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"area": 1, "land_area_fraction": 1, "layer_depth_4": 1},
)
def lower_layer_volume_vu_4():
    """
    Water equivalent volume of the fourth layer of deep ocean.
    """
    return area() * (1 - land_area_fraction()) * layer_depth_4()


@component.add(
    name="Mass Heat Capacity",
    units="J/kg/DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def mass_heat_capacity():
    """
    Specific heat of water, i.e., amount of heat in Joules per kg water required to raise the temperature by one C degree.
    """
    return 4186


@component.add(
    name="N2O Radiative Forcing",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "n2o_radiative_forcing_history": 1,
        "n2o_radiative_forcing_rcp34": 1,
        "n2o_radiative_forcing_rcp60": 1,
        "n2o_radiative_forcing_rcp85": 1,
        "n2o_radiative_forcing_rcp45": 1,
        "n2o_radiative_forcing_rcp19": 1,
        "rcp_scenario": 5,
        "n2o_radiative_forcing_rcp26": 1,
    },
)
def n2o_radiative_forcing():
    """
    Radiative forcing from N2O in the atmosphere.
    """
    return if_then_else(
        time() <= 2010,
        lambda: n2o_radiative_forcing_history(),
        lambda: if_then_else(
            rcp_scenario() == 0,
            lambda: n2o_radiative_forcing_rcp19(),
            lambda: if_then_else(
                rcp_scenario() == 1,
                lambda: n2o_radiative_forcing_rcp26(),
                lambda: if_then_else(
                    rcp_scenario() == 2,
                    lambda: n2o_radiative_forcing_rcp34(),
                    lambda: if_then_else(
                        rcp_scenario() == 3,
                        lambda: n2o_radiative_forcing_rcp45(),
                        lambda: if_then_else(
                            rcp_scenario() == 4,
                            lambda: n2o_radiative_forcing_rcp60(),
                            lambda: n2o_radiative_forcing_rcp85(),
                        ),
                    ),
                ),
            ),
        ),
    )


@component.add(
    name="N2O Radiative Forcing History",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "dimensionless_time": 1, "table_n2o_radiative_forcing": 1},
)
def n2o_radiative_forcing_history():
    """
    Historical data for radiative forcing from N2O in the atmosphere.
    """
    return table_n2o_radiative_forcing(time() * dimensionless_time())


@component.add(
    name="N2O Radiative Forcing RCP19",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_n2o_radiative_forcing_ssp2_rcp19": 1,
    },
)
def n2o_radiative_forcing_rcp19():
    """
    Future projections of N2O radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE-GLOBIOM (RCP 1.9).
    """
    return table_n2o_radiative_forcing_ssp2_rcp19(time() * dimensionless_time())


@component.add(
    name="N2O Radiative Forcing RCP26",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_n2o_radiative_forcing_ssp2_rcp26": 1,
    },
)
def n2o_radiative_forcing_rcp26():
    """
    Future projections of N2O radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE-GLOBIOM (RCP 2.6).
    """
    return table_n2o_radiative_forcing_ssp2_rcp26(time() * dimensionless_time())


@component.add(
    name="N2O Radiative Forcing RCP34",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_n2o_radiative_forcing_ssp2_rcp34": 1,
    },
)
def n2o_radiative_forcing_rcp34():
    """
    Future projections of N2O radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE-GLOBIOM (SSP2 RCP 3.4).
    """
    return table_n2o_radiative_forcing_ssp2_rcp34(time() * dimensionless_time())


@component.add(
    name="N2O Radiative Forcing RCP45",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_n2o_radiative_forcing_ssp2_rcp45": 1,
    },
)
def n2o_radiative_forcing_rcp45():
    """
    Future projections of N2O radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE-GLOBIOM (RCP 4.5).
    """
    return table_n2o_radiative_forcing_ssp2_rcp45(time() * dimensionless_time())


@component.add(
    name="N2O Radiative Forcing RCP60",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_n2o_radiative_forcing_ssp2_rcp60": 1,
    },
)
def n2o_radiative_forcing_rcp60():
    """
    Future projections of N2O radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE-GLOBIOM (RCP 6.0).
    """
    return table_n2o_radiative_forcing_ssp2_rcp60(time() * dimensionless_time())


@component.add(
    name="N2O Radiative Forcing RCP85",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_n2o_radiative_forcing_ssp2_rcp85": 1,
    },
)
def n2o_radiative_forcing_rcp85():
    """
    Future projections of N2O radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE (RCP 8.5).
    """
    return table_n2o_radiative_forcing_ssp2_rcp85(time() * dimensionless_time())


@component.add(
    name='"2xCO2 Forcing"',
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_radiative_forcing_coefficient": 1},
)
def nvs_2xco2_forcing():
    """
    Radiative forcing at 2x CO2 equivalent.
    """
    return co2_radiative_forcing_coefficient() * float(np.log(2))


@component.add(
    name="Offset 700m Heat", units="Je22", comp_type="Constant", comp_subtype="Normal"
)
def offset_700m_heat():
    """
    Calibration offset.
    """
    return -16


@component.add(
    name="Other Anhtropogenic Radiative Forcing RCP60",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_other_anthropogenic_radiative_forcing_ssp2_rcp60": 1,
    },
)
def other_anhtropogenic_radiative_forcing_rcp60():
    return table_other_anthropogenic_radiative_forcing_ssp2_rcp60(
        time() * dimensionless_time()
    )


@component.add(
    name="Other Anthropogenic Radiative Forcing",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "other_anthropogenic_radiative_forcing_history": 1,
        "other_anhtropogenic_radiative_forcing_rcp60": 1,
        "other_anthropogenic_radiative_forcing_rcp85": 1,
        "other_anthropogenic_radiative_forcing_rcp34": 1,
        "other_anthropogenic_radiative_forcing_rcp26": 1,
        "other_anthropogenic_radiative_forcing_rcp45": 1,
        "rcp_scenario": 5,
        "other_anthropogenic_radiative_forcing_rcp19": 1,
    },
)
def other_anthropogenic_radiative_forcing():
    """
    Radiative forcing from other anthropogenic gases in the atmosphere. Calculated fro mthe SSP2 database as total forcing - (forcing from C02, CH4, N2O, F-Gases)
    """
    return if_then_else(
        time() <= 2010,
        lambda: other_anthropogenic_radiative_forcing_history(),
        lambda: if_then_else(
            rcp_scenario() == 0,
            lambda: other_anthropogenic_radiative_forcing_rcp19(),
            lambda: if_then_else(
                rcp_scenario() == 1,
                lambda: other_anthropogenic_radiative_forcing_rcp26(),
                lambda: if_then_else(
                    rcp_scenario() == 2,
                    lambda: other_anthropogenic_radiative_forcing_rcp34(),
                    lambda: if_then_else(
                        rcp_scenario() == 3,
                        lambda: other_anthropogenic_radiative_forcing_rcp45(),
                        lambda: if_then_else(
                            rcp_scenario() == 4,
                            lambda: other_anhtropogenic_radiative_forcing_rcp60(),
                            lambda: other_anthropogenic_radiative_forcing_rcp85(),
                        ),
                    ),
                ),
            ),
        ),
    )


@component.add(
    name="Other Anthropogenic Radiative Forcing History",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_other_anthropogenic_radiative_forcing": 1,
    },
)
def other_anthropogenic_radiative_forcing_history():
    """
    Historical data for radiative forcing from CH4 in the atmosphere.
    """
    return table_other_anthropogenic_radiative_forcing(time() * dimensionless_time())


@component.add(
    name="Other Anthropogenic Radiative Forcing RCP19",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_other_anthropogenic_radiative_forcing_ssp2_rcp19": 1,
    },
)
def other_anthropogenic_radiative_forcing_rcp19():
    """
    MESSAGE-GLOBIOM (RCP 1.9).
    """
    return table_other_anthropogenic_radiative_forcing_ssp2_rcp19(
        time() * dimensionless_time()
    )


@component.add(
    name="Other Anthropogenic Radiative Forcing RCP26",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_other_anthropogenic_radiative_forcing_ssp2_rcp26": 1,
    },
)
def other_anthropogenic_radiative_forcing_rcp26():
    return table_other_anthropogenic_radiative_forcing_ssp2_rcp26(
        time() * dimensionless_time()
    )


@component.add(
    name="Other Anthropogenic Radiative Forcing RCP34",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_other_anthropogenic_radiative_forcing_ssp2_rcp34": 1,
    },
)
def other_anthropogenic_radiative_forcing_rcp34():
    return table_other_anthropogenic_radiative_forcing_ssp2_rcp34(
        time() * dimensionless_time()
    )


@component.add(
    name="Other Anthropogenic Radiative Forcing RCP45",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_other_anthropogenic_radiative_forcing_ssp2_rcp45": 1,
    },
)
def other_anthropogenic_radiative_forcing_rcp45():
    return table_other_anthropogenic_radiative_forcing_ssp2_rcp45(
        time() * dimensionless_time()
    )


@component.add(
    name="Other Anthropogenic Radiative Forcing RCP85",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_other_anthropogenic_radiative_forcing_ssp2_rcp85": 1,
    },
)
def other_anthropogenic_radiative_forcing_rcp85():
    return table_other_anthropogenic_radiative_forcing_ssp2_rcp85(
        time() * dimensionless_time()
    )


@component.add(
    name="Other Forcings",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "ch4_radiative_forcing": 1,
        "n2o_radiative_forcing": 1,
        "f_gases_radiative_forcing": 1,
        "other_anthropogenic_radiative_forcing": 1,
    },
)
def other_forcings():
    """
    Radiative forcing from factors other than CO2 in the atmosphere.
    """
    return (
        ch4_radiative_forcing()
        + n2o_radiative_forcing()
        + f_gases_radiative_forcing()
        + other_anthropogenic_radiative_forcing()
    )


@component.add(
    name="Other Radiative Forcing",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "other_radiative_forcing_history": 1,
        "other_radiative_forcing_aim_rcp7": 1,
        "other_radiative_forcing_message_rcp85": 1,
        "other_radiative_forcing_image_rcp26": 1,
        "other_radiative_forcing_aim_rcp60": 1,
        "rcp_scenario": 4,
        "other_radiative_forcing_minicam_rcp45": 1,
    },
)
def other_radiative_forcing():
    """
    Radiative forcing from other factors than CO2, CH4, N2O and HFC in the atmosphere.
    """
    return if_then_else(
        time() < 2000,
        lambda: other_radiative_forcing_history(),
        lambda: if_then_else(
            rcp_scenario() == 1,
            lambda: other_radiative_forcing_image_rcp26(),
            lambda: if_then_else(
                rcp_scenario() == 2,
                lambda: other_radiative_forcing_minicam_rcp45(),
                lambda: if_then_else(
                    rcp_scenario() == 3,
                    lambda: other_radiative_forcing_aim_rcp60(),
                    lambda: if_then_else(
                        rcp_scenario() == 4,
                        lambda: other_radiative_forcing_message_rcp85(),
                        lambda: other_radiative_forcing_aim_rcp7(),
                    ),
                ),
            ),
        ),
    )


@component.add(
    name="Other Radiative Forcing AIM RCP60",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_other_radiative_forcing_aim_rcp60": 1,
    },
)
def other_radiative_forcing_aim_rcp60():
    """
    Future projections of other radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by AIM (RCP 6.0).
    """
    return table_other_radiative_forcing_aim_rcp60(time() * dimensionless_time())


@component.add(
    name="Other Radiative Forcing AIM RCP7",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_other_radiative_forcing_aim_ssp3_rcp7": 1,
    },
)
def other_radiative_forcing_aim_rcp7():
    """
    Future projections of other radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE (RCP 8.5).
    """
    return table_other_radiative_forcing_aim_ssp3_rcp7(time() * dimensionless_time())


@component.add(
    name="Other Radiative Forcing History",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "dimensionless_time": 1, "table_other_radiative_forcing": 1},
)
def other_radiative_forcing_history():
    """
    Historical data for radiative forcing from other factors in the atmosphere.
    """
    return table_other_radiative_forcing(time() * dimensionless_time())


@component.add(
    name="Other Radiative Forcing IMAGE RCP26",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_other_radiative_forcing_image_rcp26": 1,
    },
)
def other_radiative_forcing_image_rcp26():
    """
    Future projections of other radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by IMAGE (RCP 2.6).
    """
    return table_other_radiative_forcing_image_rcp26(time() * dimensionless_time())


@component.add(
    name="Other Radiative Forcing MESSAGE RCP85",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_other_radiative_forcing_message_rcp85": 1,
    },
)
def other_radiative_forcing_message_rcp85():
    """
    Future projections of other radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE (RCP 8.5).
    """
    return table_other_radiative_forcing_message_rcp85(time() * dimensionless_time())


@component.add(
    name="Other Radiative Forcing MiniCAM RCP45",
    units="W/(Meter*Meter)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "time": 1,
        "dimensionless_time": 1,
        "table_other_radiative_forcing_minicam_rcp45": 1,
    },
)
def other_radiative_forcing_minicam_rcp45():
    """
    Future projections of other radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MiniCAM (RCP 4.5).
    """
    return table_other_radiative_forcing_minicam_rcp45(time() * dimensionless_time())


@component.add(
    name="R",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_atmosphere": 1, "preindustrial_c_in_atmosphere": 1},
)
def r():
    """
    Ratio of the current carbon in atmosphere to its preindustrial content.
    """
    return c_in_atmosphere() / preindustrial_c_in_atmosphere()


@component.add(
    name="RCP Scenario",
    units="Dmnl",
    limits=(1.0, 4.0, 1.0),
    comp_type="Constant",
    comp_subtype="Normal",
)
def rcp_scenario():
    """
    Trigger for Representative Concentration Pathways scenarios. RCP Scenario=0, RCP1.9 RCP Scenario=1,RCP2.6, RCP Scenario=2,RCP3.4, RCP Scenario=3, RCP 4.5, RCP Scenario=4, RCP 6, RCP Scenario=5, RCP 8.5
    """
    return 3


@component.add(
    name="Relative Deep 1 Ocean Temperature",
    units="DegreesC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"heat_in_deep_ocean_1": 1, "deep_ocean_1_heat_capacity": 1},
)
def relative_deep_1_ocean_temperature():
    """
    Temperature of the first layer of the deep ocean.
    """
    return heat_in_deep_ocean_1() / deep_ocean_1_heat_capacity()


@component.add(
    name="Relative Deep 2 Ocean Temperature",
    units="DegreesC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"heat_in_deep_ocean_2": 1, "deep_ocean_2_heat_capacity": 1},
)
def relative_deep_2_ocean_temperature():
    """
    Temperature of the second layer of the deep ocean.
    """
    return heat_in_deep_ocean_2() / deep_ocean_2_heat_capacity()


@component.add(
    name="Relative Deep 3 Ocean Temperature",
    units="DegreesC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"heat_in_deep_ocean_3": 1, "deep_ocean_3_heat_capacity": 1},
)
def relative_deep_3_ocean_temperature():
    """
    Temperature of the third layer of the deep ocean.
    """
    return heat_in_deep_ocean_3() / deep_ocean_3_heat_capacity()


@component.add(
    name="Relative Deep 4 Ocean Temperature",
    units="DegreesC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"heat_in_deep_ocean_4": 1, "deep_ocean_4_heat_capacity": 1},
)
def relative_deep_4_ocean_temperature():
    """
    Temperature of the fourth layer of the deep ocean.
    """
    return heat_in_deep_ocean_4() / deep_ocean_4_heat_capacity()


@component.add(
    name="sec per Year", units="sec/Year", comp_type="Constant", comp_subtype="Normal"
)
def sec_per_year():
    """
    Conversion from year to sec.
    """
    return 31536000.0


@component.add(
    name="TABLE CH4 Radiative Forcing",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_table_ch4_radiative_forcing"},
)
def table_ch4_radiative_forcing(x, final_subs=None):
    """
    Data series for historical data of CH4 radiative forcing. Pre-2000 From AR5, 2005 AND 2010 from the SSP database, SSP2 Message-GLOBIOM (marker).
    """
    return _hardcodedlookup_table_ch4_radiative_forcing(x, final_subs)


_hardcodedlookup_table_ch4_radiative_forcing = HardcodedLookups(
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
        2005.0,
        2010.0,
    ],
    [
        0.097,
        0.121,
        0.15,
        0.179,
        0.205,
        0.233,
        0.28,
        0.342,
        0.409,
        0.465,
        0.485,
        0.562305,
        0.588276,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_ch4_radiative_forcing",
)


@component.add(
    name="TABLE CH4 Radiative Forcing SSP2 RCP19",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp19"
    },
)
def table_ch4_radiative_forcing_ssp2_rcp19(x, final_subs=None):
    """
    Data series for future projections of CH4 radiative forcing by Message-GLOBIOM (SSP2 marker model) in RCP 1.9.
    """
    return _hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp19(x, final_subs)


_hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp19 = HardcodedLookups(
    [2010.0, 2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0],
    [
        0.588276,
        0.61707,
        0.58715,
        0.509574,
        0.435621,
        0.380312,
        0.338259,
        0.301909,
        0.271782,
        0.249517,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp19",
)


@component.add(
    name="TABLE CH4 Radiative Forcing SSP2 RCP26",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp26"
    },
)
def table_ch4_radiative_forcing_ssp2_rcp26(x, final_subs=None):
    """
    Data series for future projections of CH4 radiative forcing by Message-GLOBIOM (SSP2 marker model) in RCP 2.6.
    """
    return _hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp26(x, final_subs)


_hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp26 = HardcodedLookups(
    [2010.0, 2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0],
    [
        0.588276,
        0.617437,
        0.60655,
        0.559263,
        0.496306,
        0.449361,
        0.420164,
        0.395895,
        0.366439,
        0.33553,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp26",
)


@component.add(
    name="TABLE CH4 Radiative Forcing SSP2 RCP34",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp34"
    },
)
def table_ch4_radiative_forcing_ssp2_rcp34(x, final_subs=None):
    """
    Data series for future projections of CH4 radiative forcing by MESSAGE-GLOBIOM (RCP 3.4).
    """
    return _hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp34(x, final_subs)


_hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp34 = HardcodedLookups(
    [2010.0, 2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0],
    [
        0.588276,
        0.618688,
        0.621345,
        0.592793,
        0.537515,
        0.488544,
        0.459203,
        0.441564,
        0.425481,
        0.405663,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp34",
)


@component.add(
    name="TABLE CH4 Radiative Forcing SSP2 RCP45",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp45"
    },
)
def table_ch4_radiative_forcing_ssp2_rcp45(x, final_subs=None):
    """
    Data series for future projections of CH4 radiative forcing by MESSAGE-GLOBIOM in SSP2 RCP 4.5.
    """
    return _hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp45(x, final_subs)


_hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp45 = HardcodedLookups(
    [2010.0, 2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0],
    [
        0.588276,
        0.619873,
        0.627489,
        0.614632,
        0.578009,
        0.532435,
        0.499299,
        0.477175,
        0.46059,
        0.449891,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp45",
)


@component.add(
    name="TABLE CH4 Radiative Forcing SSP2 RCP60",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp60"
    },
)
def table_ch4_radiative_forcing_ssp2_rcp60(x, final_subs=None):
    """
    Data series for future projections of CH4 radiative forcing by MESSAGE-GLOBIOM (RCP 6.0).
    """
    return _hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp60(x, final_subs)


_hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp60 = HardcodedLookups(
    [2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0],
    [
        0.621315,
        0.636997,
        0.6457,
        0.637477,
        0.614447,
        0.590103,
        0.56345,
        0.535615,
        0.507884,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp60",
)


@component.add(
    name="TABLE CH4 Radiative Forcing SSP2 RCP85",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp85"
    },
)
def table_ch4_radiative_forcing_ssp2_rcp85(x, final_subs=None):
    """
    Data series for future projections of CH4 radiative forcing by MESSAGE-GLOBIOM (RCP 8.5).
    """
    return _hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp85(x, final_subs)


_hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp85 = HardcodedLookups(
    [2010.0, 2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0],
    [
        0.588276,
        0.624748,
        0.647046,
        0.664906,
        0.676129,
        0.685959,
        0.695531,
        0.699882,
        0.698119,
        0.688933,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_ch4_radiative_forcing_ssp2_rcp85",
)


@component.add(
    name="TABLE F Gases Radiative Forcing",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_table_f_gases_radiative_forcing"},
)
def table_f_gases_radiative_forcing(x, final_subs=None):
    """
    Data series for historical data of F-gases radiative forcing. Pre-2000 From AR5, 2005 AND 2010 from the SSP database, SSP2 Message-GLOBIOM (marker).
    """
    return _hardcodedlookup_table_f_gases_radiative_forcing(x, final_subs)


_hardcodedlookup_table_f_gases_radiative_forcing = HardcodedLookups(
    [1900.0, 1950.0, 2005.0, 2010.0],
    [0.00000e00, 1.00000e-05, 2.11050e-02, 3.11024e-02],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_f_gases_radiative_forcing",
)


@component.add(
    name="TABLE F Gases Radiative Forcing SSP2 RCP19",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp19"
    },
)
def table_f_gases_radiative_forcing_ssp2_rcp19(x, final_subs=None):
    """
    Data series for future projections of f-gases radiative forcing by Message-GLOBIOM (SSP2 marker model) in RCP 1.9.
    """
    return _hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp19(x, final_subs)


_hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp19 = HardcodedLookups(
    [2010.0, 2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0],
    [
        0.0311024,
        0.0613296,
        0.0770876,
        0.0756992,
        0.0766076,
        0.0793937,
        0.0825332,
        0.0849748,
        0.0865851,
        0.0877894,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp19",
)


@component.add(
    name="TABLE F Gases Radiative Forcing SSP2 RCP26",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp26"
    },
)
def table_f_gases_radiative_forcing_ssp2_rcp26(x, final_subs=None):
    """
    Data series for future projections of f-gases radiative forcing by Message-GLOBIOM (SSP2 marker model) in RCP 2.6.
    """
    return _hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp26(x, final_subs)


_hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp26 = HardcodedLookups(
    [2010.0, 2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0],
    [
        0.0311024,
        0.061264,
        0.0782927,
        0.080345,
        0.0847037,
        0.0891935,
        0.0927838,
        0.0960691,
        0.0987984,
        0.101286,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp26",
)


@component.add(
    name="TABLE F Gases Radiative Forcing SSP2 RCP34",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp34"
    },
)
def table_f_gases_radiative_forcing_ssp2_rcp34(x, final_subs=None):
    """
    Data series for future projections of f-gases radiative forcing by MESSAGE-GLOBIOM (RCP 3.4).
    """
    return _hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp34(x, final_subs)


_hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp34 = HardcodedLookups(
    [2010.0, 2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0],
    [
        0.0311024,
        0.0612598,
        0.0836687,
        0.0909787,
        0.0942257,
        0.0980601,
        0.103224,
        0.106661,
        0.108445,
        0.110579,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp34",
)


@component.add(
    name="TABLE F Gases Radiative Forcing SSP2 RCP45",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp45"
    },
)
def table_f_gases_radiative_forcing_ssp2_rcp45(x, final_subs=None):
    """
    Data series for future projections of f-gases radiative forcing by MESSAGE-GLOBIOM in SSP2 RCP 4.5.
    """
    return _hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp45(x, final_subs)


_hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp45 = HardcodedLookups(
    [2010.0, 2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0],
    [
        0.0311024,
        0.0612728,
        0.0871134,
        0.0987915,
        0.101803,
        0.103702,
        0.108015,
        0.112576,
        0.116856,
        0.119682,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp45",
)


@component.add(
    name="TABLE F Gases Radiative Forcing SSP2 RCP60",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp60"
    },
)
def table_f_gases_radiative_forcing_ssp2_rcp60(x, final_subs=None):
    """
    Data series for future projections of f gases radiative forcing by MESSAGE-GLOBIOM (RCP 6.0).
    """
    return _hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp60(x, final_subs)


_hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp60 = HardcodedLookups(
    [2010.0, 2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0],
    [
        0.0311024,
        0.061275,
        0.091407,
        0.119426,
        0.148527,
        0.173135,
        0.183224,
        0.17176,
        0.157098,
        0.151042,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp60",
)


@component.add(
    name="TABLE F Gases Radiative Forcing SSP2 RCP85",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp85"
    },
)
def table_f_gases_radiative_forcing_ssp2_rcp85(x, final_subs=None):
    """
    Data series for future projections of f-gases radiative forcing by MESSAGE-GLOBIOM (RCP 8.5).
    """
    return _hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp85(x, final_subs)


_hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp85 = HardcodedLookups(
    [2010.0, 2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0],
    [
        0.0311024,
        0.061417,
        0.0930176,
        0.122854,
        0.156046,
        0.192871,
        0.23523,
        0.283043,
        0.334059,
        0.386994,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_f_gases_radiative_forcing_ssp2_rcp85",
)


@component.add(
    name="TABLE HFC Radiative Forcing",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_table_hfc_radiative_forcing"},
)
def table_hfc_radiative_forcing(x, final_subs=None):
    """
    Data series for historical data of HFC radiative forcing.
    """
    return _hardcodedlookup_table_hfc_radiative_forcing(x, final_subs)


_hardcodedlookup_table_hfc_radiative_forcing = HardcodedLookups(
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
        2005.0,
    ],
    [0.001, 0.001, 0.001, 0.002, 0.003, 0.008, 0.022, 0.069, 0.174, 0.288, 0.332, 0.34],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_hfc_radiative_forcing",
)


@component.add(
    name="TABLE HFC Radiative Forcing AIM RCP60",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_table_hfc_radiative_forcing_aim_rcp60"},
)
def table_hfc_radiative_forcing_aim_rcp60(x, final_subs=None):
    """
    Data series for future projections of HFC radiative forcing by AIM (RCP 6.0).
    """
    return _hardcodedlookup_table_hfc_radiative_forcing_aim_rcp60(x, final_subs)


_hardcodedlookup_table_hfc_radiative_forcing_aim_rcp60 = HardcodedLookups(
    [
        2005.0,
        2010.0,
        2020.0,
        2030.0,
        2040.0,
        2050.0,
        2060.0,
        2070.0,
        2080.0,
        2090.0,
        2100.0,
    ],
    [0.34, 0.344, 0.346, 0.339, 0.316, 0.272, 0.236, 0.211, 0.194, 0.18, 0.168],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_hfc_radiative_forcing_aim_rcp60",
)


@component.add(
    name="TABLE HFC Radiative Forcing AIM SSP3 RCP7",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_hfc_radiative_forcing_aim_ssp3_rcp7"
    },
)
def table_hfc_radiative_forcing_aim_ssp3_rcp7(x, final_subs=None):
    """
    Data series for future projections of HFC radiative forcing by AIM (RCP 7).
    """
    return _hardcodedlookup_table_hfc_radiative_forcing_aim_ssp3_rcp7(x, final_subs)


_hardcodedlookup_table_hfc_radiative_forcing_aim_ssp3_rcp7 = HardcodedLookups(
    [
        2005.0,
        2010.0,
        2020.0,
        2030.0,
        2040.0,
        2050.0,
        2060.0,
        2070.0,
        2080.0,
        2090.0,
        2100.0,
    ],
    [0.021, 0.031, 0.061, 0.096, 0.129, 0.16, 0.188, 0.211, 0.231, 0.251, 0.27],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_hfc_radiative_forcing_aim_ssp3_rcp7",
)


@component.add(
    name="TABLE HFC Radiative Forcing IMAGE RCP26",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_hfc_radiative_forcing_image_rcp26"
    },
)
def table_hfc_radiative_forcing_image_rcp26(x, final_subs=None):
    """
    Data series for future projections of HFC radiative forcing by IMAGE (RCP 2.6).
    """
    return _hardcodedlookup_table_hfc_radiative_forcing_image_rcp26(x, final_subs)


_hardcodedlookup_table_hfc_radiative_forcing_image_rcp26 = HardcodedLookups(
    [
        2005.0,
        2010.0,
        2020.0,
        2030.0,
        2040.0,
        2050.0,
        2060.0,
        2070.0,
        2080.0,
        2090.0,
        2100.0,
    ],
    [0.34, 0.344, 0.346, 0.329, 0.301, 0.273, 0.253, 0.243, 0.236, 0.229, 0.22],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_hfc_radiative_forcing_image_rcp26",
)


@component.add(
    name="TABLE HFC Radiative Forcing MESSAGE RCP85",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_hfc_radiative_forcing_message_rcp85"
    },
)
def table_hfc_radiative_forcing_message_rcp85(x, final_subs=None):
    """
    Data series for future projections of HFC radiative forcing by MESSAGE (RCP 8.5).
    """
    return _hardcodedlookup_table_hfc_radiative_forcing_message_rcp85(x, final_subs)


_hardcodedlookup_table_hfc_radiative_forcing_message_rcp85 = HardcodedLookups(
    [
        2005.0,
        2010.0,
        2020.0,
        2030.0,
        2040.0,
        2050.0,
        2060.0,
        2070.0,
        2080.0,
        2090.0,
        2100.0,
    ],
    [0.34, 0.345, 0.36, 0.371, 0.366, 0.339, 0.316, 0.303, 0.297, 0.294, 0.294],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_hfc_radiative_forcing_message_rcp85",
)


@component.add(
    name="TABLE HFC Radiative Forcing MiniCAM RCP45",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_hfc_radiative_forcing_minicam_rcp45"
    },
)
def table_hfc_radiative_forcing_minicam_rcp45(x, final_subs=None):
    """
    Data series for future projections of HFC radiative forcing by MiniCAM (RCP 4.5).
    """
    return _hardcodedlookup_table_hfc_radiative_forcing_minicam_rcp45(x, final_subs)


_hardcodedlookup_table_hfc_radiative_forcing_minicam_rcp45 = HardcodedLookups(
    [
        2005.0,
        2010.0,
        2020.0,
        2030.0,
        2040.0,
        2050.0,
        2060.0,
        2070.0,
        2080.0,
        2090.0,
        2100.0,
    ],
    [0.34, 0.344, 0.348, 0.344, 0.323, 0.279, 0.242, 0.215, 0.197, 0.188, 0.183],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_hfc_radiative_forcing_minicam_rcp45",
)


@component.add(
    name="TABLE N2O Radiative Forcing",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_table_n2o_radiative_forcing"},
)
def table_n2o_radiative_forcing(x, final_subs=None):
    """
    Data series for historical data of N2O radiative forcing.
    """
    return _hardcodedlookup_table_n2o_radiative_forcing(x, final_subs)


_hardcodedlookup_table_n2o_radiative_forcing = HardcodedLookups(
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
        2005.0,
        2010.0,
    ],
    [
        0.025,
        0.029,
        0.036,
        0.043,
        0.048,
        0.056,
        0.064,
        0.077,
        0.098,
        0.124,
        0.145,
        0.155711,
        0.167804,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_n2o_radiative_forcing",
)


@component.add(
    name="TABLE N2O Radiative Forcing SSP2 RCP19",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp19"
    },
)
def table_n2o_radiative_forcing_ssp2_rcp19(x, final_subs=None):
    """
    Data series for future projections of N2O radiative forcing by MESSAGE-GLOBIOM (RCP 1.9).
    """
    return _hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp19(x, final_subs)


_hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp19 = HardcodedLookups(
    [2010.0, 2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0],
    [
        0.167804,
        0.190979,
        0.212475,
        0.22977,
        0.240821,
        0.246385,
        0.248219,
        0.247229,
        0.244504,
        0.240289,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp19",
)


@component.add(
    name="TABLE N2O Radiative Forcing SSP2 RCP26",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp26"
    },
)
def table_n2o_radiative_forcing_ssp2_rcp26(x, final_subs=None):
    """
    Data series for future projections of N2O radiative forcing by MESSAGE-GLOBIOM (RCP 2.6).
    """
    return _hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp26(x, final_subs)


_hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp26 = HardcodedLookups(
    [2010.0, 2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0],
    [
        0.167804,
        0.190994,
        0.213422,
        0.233756,
        0.249976,
        0.262045,
        0.270751,
        0.275577,
        0.277001,
        0.27603,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp26",
)


@component.add(
    name="TABLE N2O Radiative Forcing SSP2 RCP34",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp34"
    },
)
def table_n2o_radiative_forcing_ssp2_rcp34(x, final_subs=None):
    """
    Data series for future projections of N2O radiative forcing by MESSAGE-GLOBIOM (SSP 2 RCP 34).
    """
    return _hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp34(x, final_subs)


_hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp34 = HardcodedLookups(
    [2010.0, 2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0],
    [
        0.167804,
        0.191089,
        0.214084,
        0.235924,
        0.254871,
        0.270427,
        0.282841,
        0.291311,
        0.29594,
        0.298074,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp34",
)


@component.add(
    name="TABLE N2O Radiative Forcing SSP2 RCP45",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp45"
    },
)
def table_n2o_radiative_forcing_ssp2_rcp45(x, final_subs=None):
    """
    Data series for future projections of N2O radiative forcing by MESSAGE-GLOBIOM (SSP2 RCP 4.5).
    """
    return _hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp45(x, final_subs)


_hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp45 = HardcodedLookups(
    [2010.0, 2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0],
    [
        0.167804,
        0.191135,
        0.21432,
        0.236786,
        0.257099,
        0.274837,
        0.289969,
        0.301271,
        0.308584,
        0.312947,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp45",
)


@component.add(
    name="TABLE N2O Radiative Forcing SSP2 RCP60",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp60"
    },
)
def table_n2o_radiative_forcing_ssp2_rcp60(x, final_subs=None):
    """
    Data series for future projections of N2O radiative forcing by MESSAGE-GLOBIOM (SSP2 RCP 6.0).
    """
    return _hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp60(x, final_subs)


_hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp60 = HardcodedLookups(
    [2010.0, 2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0],
    [
        0.167804,
        0.191189,
        0.214542,
        0.237486,
        0.258855,
        0.278363,
        0.296147,
        0.311316,
        0.324115,
        0.335382,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp60",
)


@component.add(
    name="TABLE N2O Radiative Forcing SSP2 RCP85",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp85"
    },
)
def table_n2o_radiative_forcing_ssp2_rcp85(x, final_subs=None):
    """
    Data series for future projections of N2O radiative forcing by MESSAGE-GLOBIOM (SSP2 RCP 8.5).
    """
    return _hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp85(x, final_subs)


_hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp85 = HardcodedLookups(
    [2010.0, 2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0],
    [
        0.167804,
        0.191292,
        0.215286,
        0.239765,
        0.263741,
        0.286982,
        0.30948,
        0.331141,
        0.352599,
        0.374267,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_n2o_radiative_forcing_ssp2_rcp85",
)


@component.add(
    name="TABLE Other Anthropogenic Radiative Forcing",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_other_anthropogenic_radiative_forcing"
    },
)
def table_other_anthropogenic_radiative_forcing(x, final_subs=None):
    """
    Data series for historical data of other radiative forcing. 2005 AND 2010 from the SSP database, SSP2 Message-GLOBIOM (marker). Calculated as (total forcing) - (CO2, CH4, N2O and F-Gases forcings)
    """
    return _hardcodedlookup_table_other_anthropogenic_radiative_forcing(x, final_subs)


_hardcodedlookup_table_other_anthropogenic_radiative_forcing = HardcodedLookups(
    [1900.0, 2005.0],
    [0.0, -0.557989],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_other_anthropogenic_radiative_forcing",
)


@component.add(
    name="TABLE Other Anthropogenic Radiative Forcing SSP2 RCP19",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp19"
    },
)
def table_other_anthropogenic_radiative_forcing_ssp2_rcp19(x, final_subs=None):
    """
    Data series for future projections of other radiative forcing by Message-GLOBIOM (SSP2 marker model) in RCP 1.9.
    """
    return _hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp19(
        x, final_subs
    )


_hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp19 = (
    HardcodedLookups(
        [
            2005.0,
            2010.0,
            2020.0,
            2030.0,
            2040.0,
            2050.0,
            2060.0,
            2070.0,
            2080.0,
            2090.0,
            2100.0,
        ],
        [
            -0.557989,
            -0.487374,
            -0.397824,
            -0.230515,
            -0.210926,
            -0.27021,
            -0.319045,
            -0.350269,
            -0.372422,
            -0.388618,
            -0.39696,
        ],
        {},
        "interpolate",
        {},
        "_hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp19",
    )
)


@component.add(
    name="TABLE Other Anthropogenic Radiative Forcing SSP2 RCP26",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp26"
    },
)
def table_other_anthropogenic_radiative_forcing_ssp2_rcp26(x, final_subs=None):
    """
    Data series for future projections of other radiative forcing by Message-GLOBIOM (SSP2 marker model) in RCP 2.6.
    """
    return _hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp26(
        x, final_subs
    )


_hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp26 = (
    HardcodedLookups(
        [
            2005.0,
            2010.0,
            2020.0,
            2030.0,
            2040.0,
            2050.0,
            2060.0,
            2070.0,
            2080.0,
            2090.0,
            2100.0,
        ],
        [
            -0.557989,
            -0.487232,
            -0.399799,
            -0.306337,
            -0.244383,
            -0.274545,
            -0.331504,
            -0.375821,
            -0.401136,
            -0.411268,
            -0.411342,
        ],
        {},
        "interpolate",
        {},
        "_hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp26",
    )
)


@component.add(
    name="TABLE Other Anthropogenic Radiative Forcing SSP2 RCP34",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp34"
    },
)
def table_other_anthropogenic_radiative_forcing_ssp2_rcp34(x, final_subs=None):
    """
    Data series for future projections of other radiative forcing by MESSAGE-GLOBIOM (RCP 3.4).
    """
    return _hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp34(
        x, final_subs
    )


_hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp34 = (
    HardcodedLookups(
        [
            2005.0,
            2010.0,
            2020.0,
            2030.0,
            2040.0,
            2050.0,
            2060.0,
            2070.0,
            2080.0,
            2090.0,
            2100.0,
        ],
        [
            -0.557989,
            -0.487367,
            -0.405055,
            -0.362333,
            -0.311911,
            -0.331126,
            -0.356647,
            -0.378118,
            -0.400985,
            -0.420509,
            -0.426015,
        ],
        {},
        "interpolate",
        {},
        "_hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp34",
    )
)


@component.add(
    name="TABLE Other Anthropogenic Radiative Forcing SSP2 RCP45",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp45"
    },
)
def table_other_anthropogenic_radiative_forcing_ssp2_rcp45(x, final_subs=None):
    """
    Data series for future projections of other radiative forcing by MESSAGE-GLOBIOM in SSP2 RCP 4.5.
    """
    return _hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp45(
        x, final_subs
    )


_hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp45 = (
    HardcodedLookups(
        [
            2005.0,
            2010.0,
            2020.0,
            2030.0,
            2040.0,
            2050.0,
            2060.0,
            2070.0,
            2080.0,
            2090.0,
            2100.0,
        ],
        [
            -0.557989,
            -0.487489,
            -0.40917,
            -0.40208,
            -0.36824,
            -0.38091,
            -0.404117,
            -0.425465,
            -0.437686,
            -0.43453,
            -0.434378,
        ],
        {},
        "interpolate",
        {},
        "_hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp45",
    )
)


@component.add(
    name="TABLE Other Anthropogenic Radiative Forcing SSP2 RCP60",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp60"
    },
)
def table_other_anthropogenic_radiative_forcing_ssp2_rcp60(x, final_subs=None):
    """
    Data series for future projections of other radiative forcing by MESSAGE-GLOBIOM (RCP 6.0).
    """
    return _hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp60(
        x, final_subs
    )


_hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp60 = (
    HardcodedLookups(
        [
            2005.0,
            2010.0,
            2020.0,
            2030.0,
            2040.0,
            2050.0,
            2060.0,
            2070.0,
            2080.0,
            2090.0,
            2100.0,
        ],
        [
            -0.557989,
            -0.487543,
            -0.411289,
            -0.431191,
            -0.416421,
            -0.435845,
            -0.461476,
            -0.470064,
            -0.486857,
            -0.499783,
            -0.500466,
        ],
        {},
        "interpolate",
        {},
        "_hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp60",
    )
)


@component.add(
    name="TABLE Other Anthropogenic Radiative Forcing SSP2 RCP85",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp85"
    },
)
def table_other_anthropogenic_radiative_forcing_ssp2_rcp85(x, final_subs=None):
    """
    Data series for future projections of other radiative forcing by MESSAGE-GLOBIOM (RCP 8.5).
    """
    return _hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp85(
        x, final_subs
    )


_hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp85 = (
    HardcodedLookups(
        [
            2005.0,
            2010.0,
            2020.0,
            2030.0,
            2040.0,
            2050.0,
            2060.0,
            2070.0,
            2080.0,
            2090.0,
            2100.0,
        ],
        [
            -0.557989,
            -0.48777,
            -0.415208,
            -0.439654,
            -0.432948,
            -0.454012,
            -0.477328,
            -0.486185,
            -0.499955,
            -0.503879,
            -0.497409,
        ],
        {},
        "interpolate",
        {},
        "_hardcodedlookup_table_other_anthropogenic_radiative_forcing_ssp2_rcp85",
    )
)


@component.add(
    name="TABLE Other Radiative Forcing",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_table_other_radiative_forcing"},
)
def table_other_radiative_forcing(x, final_subs=None):
    """
    Data series for historical data of other factors radiative forcing.
    """
    return _hardcodedlookup_table_other_radiative_forcing(x, final_subs)


_hardcodedlookup_table_other_radiative_forcing = HardcodedLookups(
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
        2005.0,
    ],
    [
        -0.234,
        -0.282,
        -0.287,
        -0.301,
        -0.301,
        -0.369,
        -0.461,
        -0.523,
        -0.618,
        -0.681,
        -0.781,
        -0.766,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_other_radiative_forcing",
)


@component.add(
    name="TABLE Other Radiative Forcing AIM RCP60",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_other_radiative_forcing_aim_rcp60"
    },
)
def table_other_radiative_forcing_aim_rcp60(x, final_subs=None):
    """
    Data series for future projections of other factors radiative forcing by AIM (RCP 6.0).
    """
    return _hardcodedlookup_table_other_radiative_forcing_aim_rcp60(x, final_subs)


_hardcodedlookup_table_other_radiative_forcing_aim_rcp60 = HardcodedLookups(
    [
        2000.0,
        2010.0,
        2020.0,
        2030.0,
        2040.0,
        2050.0,
        2060.0,
        2070.0,
        2080.0,
        2090.0,
        2100.0,
    ],
    [
        -0.781,
        -0.751,
        -0.671,
        -0.573,
        -0.575,
        -0.521,
        -0.509,
        -0.386,
        -0.32,
        -0.322,
        -0.328,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_other_radiative_forcing_aim_rcp60",
)


@component.add(
    name="TABLE Other Radiative Forcing AIM SSP3 RCP7",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_other_radiative_forcing_aim_ssp3_rcp7"
    },
)
def table_other_radiative_forcing_aim_ssp3_rcp7(x, final_subs=None):
    """
    Data series for future projections of other factors radiative forcing by AIM (RCP 7).
    """
    return _hardcodedlookup_table_other_radiative_forcing_aim_ssp3_rcp7(x, final_subs)


_hardcodedlookup_table_other_radiative_forcing_aim_ssp3_rcp7 = HardcodedLookups(
    [
        2005.0,
        2010.0,
        2020.0,
        2030.0,
        2040.0,
        2050.0,
        2060.0,
        2070.0,
        2080.0,
        2090.0,
        2100.0,
    ],
    [
        -1.115,
        -1.06,
        -1.088,
        -1.09,
        -1.079,
        -1.081,
        -1.069,
        -1.057,
        -1.043,
        -1.017,
        -0.983,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_other_radiative_forcing_aim_ssp3_rcp7",
)


@component.add(
    name="TABLE Other Radiative Forcing IMAGE RCP26",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_other_radiative_forcing_image_rcp26"
    },
)
def table_other_radiative_forcing_image_rcp26(x, final_subs=None):
    """
    Data series for future projections of other factors radiative forcing by IMAGE (RCP 2.6).
    """
    return _hardcodedlookup_table_other_radiative_forcing_image_rcp26(x, final_subs)


_hardcodedlookup_table_other_radiative_forcing_image_rcp26 = HardcodedLookups(
    [
        2000.0,
        2010.0,
        2020.0,
        2030.0,
        2040.0,
        2050.0,
        2060.0,
        2070.0,
        2080.0,
        2090.0,
        2100.0,
    ],
    [
        -0.781,
        -0.717,
        -0.577,
        -0.489,
        -0.427,
        -0.413,
        -0.432,
        -0.418,
        -0.382,
        -0.353,
        -0.323,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_other_radiative_forcing_image_rcp26",
)


@component.add(
    name="TABLE Other Radiative Forcing MESSAGE RCP85",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_other_radiative_forcing_message_rcp85"
    },
)
def table_other_radiative_forcing_message_rcp85(x, final_subs=None):
    """
    Data series for future projections of other factors radiative forcing by MESSAGE (RCP 8.5).
    """
    return _hardcodedlookup_table_other_radiative_forcing_message_rcp85(x, final_subs)


_hardcodedlookup_table_other_radiative_forcing_message_rcp85 = HardcodedLookups(
    [
        2000.0,
        2010.0,
        2020.0,
        2030.0,
        2040.0,
        2050.0,
        2060.0,
        2070.0,
        2080.0,
        2090.0,
        2100.0,
    ],
    [
        -0.781,
        -0.696,
        -0.648,
        -0.573,
        -0.452,
        -0.341,
        -0.274,
        -0.226,
        -0.189,
        -0.121,
        -0.088,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_other_radiative_forcing_message_rcp85",
)


@component.add(
    name="TABLE Other Radiative Forcing MiniCAM RCP45",
    units="W/(Meter*Meter)",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_table_other_radiative_forcing_minicam_rcp45"
    },
)
def table_other_radiative_forcing_minicam_rcp45(x, final_subs=None):
    """
    Data series for future projections of other factors radiative forcing by MiniCAM (RCP 4.5).
    """
    return _hardcodedlookup_table_other_radiative_forcing_minicam_rcp45(x, final_subs)


_hardcodedlookup_table_other_radiative_forcing_minicam_rcp45 = HardcodedLookups(
    [
        2000.0,
        2010.0,
        2020.0,
        2030.0,
        2040.0,
        2050.0,
        2060.0,
        2070.0,
        2080.0,
        2090.0,
        2100.0,
    ],
    [
        -0.781,
        -0.713,
        -0.605,
        -0.518,
        -0.431,
        -0.344,
        -0.296,
        -0.257,
        -0.226,
        -0.227,
        -0.224,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_table_other_radiative_forcing_minicam_rcp45",
)


@component.add(
    name="Temperature Anomalies GISS v Preindustrial",
    units="DegreesC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"temperature_change_from_preindustrial": 1},
)
def temperature_anomalies_giss_v_preindustrial():
    """
    Historical values of temperature anomalies of the Atmosphere and Upper Ocean as by GISS. Source: NASA Goddard Institute for Space Studies, http://data.giss.nasa.gov/gistemp/graphs_v3/
    """
    return temperature_change_from_preindustrial()


@component.add(
    name="Temperature Anomalies HadCRUT4 v Preindustrial",
    units="DegreesC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"temperature_change_from_preindustrial": 1},
)
def temperature_anomalies_hadcrut4_v_preindustrial():
    """
    Historical values of temperature anomalies of the Atmosphere and Upper Ocean as by HadCRUT4. Source: Met Office Hadley Centre http://www.metoffice.gov.uk/hadobs/hadcrut4/data/versions/HadCRUT.4.1.1.0_r elease_notes.html
    """
    return temperature_change_from_preindustrial()


@component.add(
    name="Temperature Change from Preindustrial",
    units="DegreesC",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "heat_in_atmosphere_and_upper_ocean": 1,
        "atmospheric_and_upper_ocean_heat_capacity": 1,
    },
)
def temperature_change_from_preindustrial():
    """
    Temperature of the Atmosphere and Upper Ocean and how it has changed from preindustrial period.
    """
    return (
        heat_in_atmosphere_and_upper_ocean()
        / atmospheric_and_upper_ocean_heat_capacity()
    )


@component.add(
    name="Total Radiative Forcing",
    units="W/(m*m)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_radiative_forcing": 1, "other_forcings": 1},
)
def total_radiative_forcing():
    """
    Radiative forcing from various factors in the atmosphere. Source of Historical Data: IIASA RCP Database https://tntcat.iiasa.ac.at:8743/RcpDb/dsd?Action=htmlpage&page=welcome
    """
    return co2_radiative_forcing() + other_forcings()


@component.add(
    name="Total Radiative Forcing AIM RCP60",
    units="W/(Meter*Meter)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def total_radiative_forcing_aim_rcp60():
    """
    Future projections of total radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by AIM (RCP 6.0).
    """
    return 0


@component.add(
    name="Total Radiative Forcing IMAGE RCP26",
    units="W/(Meter*Meter)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def total_radiative_forcing_image_rcp26():
    """
    Future projections of total radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by IMAGE (RCP 2.6).
    """
    return 0


@component.add(
    name="Total Radiative Forcing MESSAGE RCP85",
    units="W/(Meter*Meter)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def total_radiative_forcing_message_rcp85():
    """
    Future projections of total radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MESSAGE (RCP 8.5).
    """
    return 0


@component.add(
    name="Total Radiative Forcing MiniCAM RCP45",
    units="W/(Meter*Meter)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def total_radiative_forcing_minicam_rcp45():
    """
    Future projections of total radiative forcing from Representative Concentration Pathways prepared for the Fifth Assessment Report of the United Nations Intergovernmental Panel on Climate Change by MiniCAM (RCP 4.5).
    """
    return 0


@component.add(
    name="Upper Layer Volume Vu",
    units="Meter*Meter*Meter",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "area": 1,
        "land_thickness": 1,
        "mixed_layer_depth": 1,
        "land_area_fraction": 2,
    },
)
def upper_layer_volume_vu():
    """
    Water equivalent volume of the upper box, which is a weighted combination of land, atmosphere,and upper ocean volumes.
    """
    return area() * (
        land_area_fraction() * land_thickness()
        + (1 - land_area_fraction()) * mixed_layer_depth()
    )


@component.add(
    name="Volumetric Heat Capacity",
    units="Year*W/(Meter*Meter*Meter*DegreesC)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "mass_heat_capacity": 1,
        "watt_per_j_s": 1,
        "sec_per_year": 1,
        "density": 1,
    },
)
def volumetric_heat_capacity():
    """
    Volumetric heat capacity of water, i.e., amount of heat in watt*year required to raise 1 cubic meter of water by one degree C.
    """
    return mass_heat_capacity() * watt_per_j_s() / sec_per_year() * density()


@component.add(
    name="Watt per J s", units="W/(J/sec)", comp_type="Constant", comp_subtype="Normal"
)
def watt_per_j_s():
    """
    Conversion from J/s to watts.
    """
    return 1
