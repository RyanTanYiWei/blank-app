"""
Module scenarios
Translated using PySD version 3.14.3
"""

@component.add(
    name="Average Wind Capacity per SqMeter Final Change Rate Variation",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def average_wind_capacity_per_sqmeter_final_change_rate_variation():
    """
    Final Educational Attainment Change Rate
    """
    return 0.35


@component.add(
    name="Biomass Conversion Efficiency Final Change Rate Variation",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biomass_conversion_efficiency_final_change_rate_variation():
    """
    Final Educational Attainment Change Rate
    """
    return 3.17e-07


@component.add(
    name="Change Rate Finish",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start": 1, "ramp_period": 1},
)
def change_rate_finish():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start() + ramp_period()


@component.add(
    name="Change Rate Finish1",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start1": 1, "ramp_period1": 1},
)
def change_rate_finish1():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start1() + ramp_period1()


@component.add(
    name="Change Rate Finish10",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start10": 1, "ramp_period10": 1},
)
def change_rate_finish10():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start10() + ramp_period10()


@component.add(
    name="Change Rate Finish11",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start11": 1, "ramp_period11": 1},
)
def change_rate_finish11():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start11() + ramp_period11()


@component.add(
    name="Change Rate Finish12",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start12": 1, "ramp_period12": 1},
)
def change_rate_finish12():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start12() + ramp_period12()


@component.add(
    name="Change Rate Finish13",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start13": 1, "ramp_period13": 1},
)
def change_rate_finish13():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start13() + ramp_period13()


@component.add(
    name="Change Rate Finish14",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start14": 1, "ramp_period14": 1},
)
def change_rate_finish14():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start14() + ramp_period14()


@component.add(
    name="Change Rate Finish15",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start15": 1, "ramp_period15": 1},
)
def change_rate_finish15():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start15() + ramp_period15()


@component.add(
    name="Change Rate Finish16",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start16": 1, "ramp_period16": 1},
)
def change_rate_finish16():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start16() + ramp_period16()


@component.add(
    name="Change Rate Finish2",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start2": 1, "ramp_period2": 1},
)
def change_rate_finish2():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start2() + ramp_period2()


@component.add(
    name="Change Rate Finish3",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start3": 1, "ramp_period3": 1},
)
def change_rate_finish3():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start3() + ramp_period3()


@component.add(
    name="Change Rate Finish4",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start4": 1, "ramp_period4": 1},
)
def change_rate_finish4():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start4() + ramp_period4()


@component.add(
    name="Change Rate Finish5",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start5": 1, "ramp_period5": 1},
)
def change_rate_finish5():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start5() + ramp_period5()


@component.add(
    name="Change Rate Finish6",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start6": 1, "ramp_period6": 1},
)
def change_rate_finish6():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start6() + ramp_period6()


@component.add(
    name="Change Rate Finish7",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start7": 1, "ramp_period7": 1},
)
def change_rate_finish7():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start7() + ramp_period7()


@component.add(
    name="Change Rate Finish8",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start8": 1, "ramp_period8": 1},
)
def change_rate_finish8():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start8() + ramp_period8()


@component.add(
    name="Change Rate Finish9",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start9": 1, "ramp_period9": 1},
)
def change_rate_finish9():
    """
    End of fractional investments in Educational Attainment.
    """
    return ramp_start9() + ramp_period9()


@component.add(
    name="Change Rate Slope",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"final_change_rate": 1, "initial_change_rate": 1, "ramp_period": 1},
)
def change_rate_slope():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return float(np.abs(final_change_rate() - initial_change_rate())) / ramp_period()


@component.add(
    name="Change Rate Slope1",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"final_change_rate1": 1, "initial_change_rate1": 1, "ramp_period1": 1},
)
def change_rate_slope1():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return float(np.abs(final_change_rate1() - initial_change_rate1())) / ramp_period1()


@component.add(
    name="Change Rate Slope10",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "final_change_rate10": 1,
        "initial_change_rate10": 1,
        "ramp_period10": 1,
    },
)
def change_rate_slope10():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return (final_change_rate10() - initial_change_rate10()) / ramp_period10()


@component.add(
    name="Change Rate Slope11",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "final_change_rate11": 1,
        "initial_change_rate11": 1,
        "ramp_period11": 1,
    },
)
def change_rate_slope11():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return (final_change_rate11() - initial_change_rate11()) / ramp_period11()


@component.add(
    name="Change Rate Slope12",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "final_change_rate12": 1,
        "initial_change_rate12": 1,
        "ramp_period12": 1,
    },
)
def change_rate_slope12():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return (
        float(np.abs(final_change_rate12() - initial_change_rate12())) / ramp_period12()
    )


@component.add(
    name="Change Rate Slope13",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "final_change_rate13": 1,
        "initial_change_rate13": 1,
        "ramp_period13": 1,
    },
)
def change_rate_slope13():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return (final_change_rate13() - initial_change_rate13()) / ramp_period13()


@component.add(
    name="Change Rate Slope14",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "final_change_rate14": 1,
        "initial_change_rate14": 1,
        "ramp_period14": 1,
    },
)
def change_rate_slope14():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return (final_change_rate14() - initial_change_rate14()) / ramp_period14()


@component.add(
    name="Change Rate Slope15",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "final_change_rate15": 1,
        "initial_change_rate15": 1,
        "ramp_period15": 1,
    },
)
def change_rate_slope15():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return (final_change_rate15() - initial_change_rate15()) / ramp_period15()


@component.add(
    name="Change Rate Slope16",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "final_change_rate16": 1,
        "initial_change_rate16": 1,
        "ramp_period16": 1,
    },
)
def change_rate_slope16():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return (
        float(np.abs(final_change_rate16() - initial_change_rate16())) / ramp_period16()
    )


@component.add(
    name="Change Rate Slope2",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"final_change_rate2": 1, "initial_change_rate2": 1, "ramp_period2": 1},
)
def change_rate_slope2():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return float(np.abs(final_change_rate2() - initial_change_rate2())) / ramp_period2()


@component.add(
    name="Change Rate Slope3",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"final_change_rate3": 1, "initial_change_rate3": 1, "ramp_period3": 1},
)
def change_rate_slope3():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return float(np.abs(final_change_rate3() - initial_change_rate3())) / ramp_period3()


@component.add(
    name="Change Rate Slope4",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reduced_carbon_emissions_of_oil": 1,
        "normal_carbon_emissions_of_oil": 1,
        "ramp_period4": 1,
    },
)
def change_rate_slope4():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return (
        reduced_carbon_emissions_of_oil() - normal_carbon_emissions_of_oil()
    ) / ramp_period4()


@component.add(
    name="Change Rate Slope5",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reduced_c_emissions_of_gas": 1,
        "normal_carbon_emissions_of_gas": 1,
        "ramp_period5": 1,
    },
)
def change_rate_slope5():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return (
        reduced_c_emissions_of_gas() - normal_carbon_emissions_of_gas()
    ) / ramp_period5()


@component.add(
    name="Change Rate Slope6",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reduced_c_emissions_of_coal": 1,
        "normal_carbon_emissions_of_coal": 1,
        "ramp_period6": 1,
    },
)
def change_rate_slope6():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return (
        reduced_c_emissions_of_coal() - normal_carbon_emissions_of_coal()
    ) / ramp_period6()


@component.add(
    name="Change Rate Slope7",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"final_change_rate7": 1, "initial_change_rate7": 1, "ramp_period7": 1},
)
def change_rate_slope7():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return float(np.abs(final_change_rate7() - initial_change_rate7())) / ramp_period7()


@component.add(
    name="Change Rate Slope8",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"final_change_rate8": 1, "initial_change_rate8": 1, "ramp_period8": 1},
)
def change_rate_slope8():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return float(np.abs(final_change_rate8() - initial_change_rate8())) / ramp_period8()


@component.add(
    name="Change Rate Slope9",
    units="1/(Year*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"final_change_rate9": 1, "initial_change_rate9": 1, "ramp_period9": 1},
)
def change_rate_slope9():
    """
    Intensity of Educational Attainment Change Rate.
    """
    return float(np.abs(final_change_rate9() - initial_change_rate9())) / ramp_period9()


@component.add(
    name="Change Rate Start",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start": 1},
)
def change_rate_start():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start()


@component.add(
    name="Change Rate Start1",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start1": 1},
)
def change_rate_start1():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start1()


@component.add(
    name="Change Rate Start10",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start10": 1},
)
def change_rate_start10():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start10()


@component.add(
    name="Change Rate Start11",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start11": 1},
)
def change_rate_start11():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start11()


@component.add(
    name="Change Rate Start12",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start12": 1},
)
def change_rate_start12():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start12()


@component.add(
    name="Change Rate Start13",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start13": 1},
)
def change_rate_start13():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start13()


@component.add(
    name="Change Rate Start14",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start14": 1},
)
def change_rate_start14():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start14()


@component.add(
    name="Change Rate Start15",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start15": 1},
)
def change_rate_start15():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start15()


@component.add(
    name="Change Rate Start16",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start16": 1},
)
def change_rate_start16():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start16()


@component.add(
    name="Change Rate Start2",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start2": 1},
)
def change_rate_start2():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start2()


@component.add(
    name="Change Rate Start3",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start3": 1},
)
def change_rate_start3():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start3()


@component.add(
    name="Change Rate Start4",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start4": 1},
)
def change_rate_start4():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start4()


@component.add(
    name="Change Rate Start5",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start5": 1},
)
def change_rate_start5():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start5()


@component.add(
    name="Change Rate Start6",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start6": 1},
)
def change_rate_start6():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start6()


@component.add(
    name="Change Rate Start7",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start7": 1},
)
def change_rate_start7():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start7()


@component.add(
    name="Change Rate Start8",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start8": 1},
)
def change_rate_start8():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start8()


@component.add(
    name="Change Rate Start9",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ramp_start9": 1},
)
def change_rate_start9():
    """
    Start of increased investments in Educational Attainment.
    """
    return ramp_start9()


@component.add(
    name="Effect of GDP on Cropland Management Practices Increment Final Change Rate Variation",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effect_of_gdp_on_cropland_management_practices_increment_final_change_rate_variation():
    """
    Final Educational Attainment Change Rate
    """
    return 10


@component.add(
    name="Effect of GDP on Cropland Management Practices Increment Ramp Period Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effect_of_gdp_on_cropland_management_practices_increment_ramp_period_variation():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50


@component.add(
    name="Effect of GDP on Forest Management Practices Increment Final Change Rate Variation",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effect_of_gdp_on_forest_management_practices_increment_final_change_rate_variation():
    """
    Final Educational Attainment Change Rate
    """
    return 1.5


@component.add(
    name="Effect of GDP on Forest Management Practices Increment Ramp Period Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def effect_of_gdp_on_forest_management_practices_increment_ramp_period_variation():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50


@component.add(
    name="Final Change Rate",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def final_change_rate():
    """
    Final Educational Attainment Change Rate
    """
    return 2


@component.add(
    name="Final Change Rate1",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_conversion_efficiency_final_change_rate_variation": 1,
        "time": 1,
    },
)
def final_change_rate1():
    """
    Final Educational Attainment Change Rate
    """
    return 3.17e-07 + step(
        __data["time"],
        biomass_conversion_efficiency_final_change_rate_variation() - 3.17e-07,
        2020,
    )


@component.add(
    name="Final Change Rate10",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def final_change_rate10():
    """
    Final Educational Attainment Change Rate
    """
    return 2000000000000.0


@component.add(
    name="Final Change Rate11",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def final_change_rate11():
    """
    Final Educational Attainment Change Rate
    """
    return 120


@component.add(
    name="Final Change Rate12",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def final_change_rate12():
    """
    Final Educational Attainment Change Rate
    """
    return 0.2


@component.add(
    name="Final Change Rate13",
    units="1/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"rcb_var_s": 1, "_smooth_final_change_rate13": 1},
    other_deps={
        "_smooth_final_change_rate13": {
            "initial": {
                "reference_cost_of_biomass_energy_production_final_change_rate_variation": 1,
                "rcb_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "reference_cost_of_biomass_energy_production_final_change_rate_variation": 1,
                "rcb_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def final_change_rate13():
    """
    Final Educational Attainment Change Rate
    """
    return rcb_var_s() + _smooth_final_change_rate13()


_smooth_final_change_rate13 = Smooth(
    lambda: step(
        __data["time"],
        reference_cost_of_biomass_energy_production_final_change_rate_variation()
        - rcb_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        reference_cost_of_biomass_energy_production_final_change_rate_variation()
        - rcb_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_final_change_rate13",
)


@component.add(
    name="Final Change Rate14",
    units="1/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"rcs_var_s": 1, "_smooth_final_change_rate14": 1},
    other_deps={
        "_smooth_final_change_rate14": {
            "initial": {
                "reference_cost_of_solar_energy_production_final_change_rate_variation": 1,
                "rcs_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "reference_cost_of_solar_energy_production_final_change_rate_variation": 1,
                "rcs_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def final_change_rate14():
    """
    Final Educational Attainment Change Rate
    """
    return rcs_var_s() + _smooth_final_change_rate14()


_smooth_final_change_rate14 = Smooth(
    lambda: step(
        __data["time"],
        reference_cost_of_solar_energy_production_final_change_rate_variation()
        - rcs_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        reference_cost_of_solar_energy_production_final_change_rate_variation()
        - rcs_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_final_change_rate14",
)


@component.add(
    name="Final Change Rate15",
    units="1/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"rcw_var_s": 1, "_smooth_final_change_rate15": 1},
    other_deps={
        "_smooth_final_change_rate15": {
            "initial": {
                "reference_cost_of_wind_energy_production_final_change_rate_variation": 1,
                "rcw_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "reference_cost_of_wind_energy_production_final_change_rate_variation": 1,
                "rcw_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def final_change_rate15():
    """
    Final Educational Attainment Change Rate
    """
    return rcw_var_s() + _smooth_final_change_rate15()


_smooth_final_change_rate15 = Smooth(
    lambda: step(
        __data["time"],
        reference_cost_of_wind_energy_production_final_change_rate_variation()
        - rcw_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        reference_cost_of_wind_energy_production_final_change_rate_variation()
        - rcw_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_final_change_rate15",
)


@component.add(
    name="Final Change Rate16",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"other_technology_steepness_final_change_rate_variation": 1, "time": 1},
)
def final_change_rate16():
    """
    Final Educational Attainment Change Rate
    """
    return 6 + step(
        __data["time"],
        other_technology_steepness_final_change_rate_variation() - 6,
        2020,
    )


@component.add(
    name="Final Change Rate2",
    units="1/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"sc_var_s": 1, "_smooth_final_change_rate2": 1},
    other_deps={
        "_smooth_final_change_rate2": {
            "initial": {
                "solar_conversion_efficiency_factor_final_change_rate_variation": 1,
                "sc_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "solar_conversion_efficiency_factor_final_change_rate_variation": 1,
                "sc_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def final_change_rate2():
    """
    Final Educational Attainment Change Rate
    """
    return sc_var_s() + _smooth_final_change_rate2()


_smooth_final_change_rate2 = Smooth(
    lambda: step(
        __data["time"],
        solar_conversion_efficiency_factor_final_change_rate_variation() - sc_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        solar_conversion_efficiency_factor_final_change_rate_variation() - sc_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_final_change_rate2",
)


@component.add(
    name="Final Change Rate3",
    units="1/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"wc_var_s": 1, "_smooth_final_change_rate3": 1},
    other_deps={
        "_smooth_final_change_rate3": {
            "initial": {
                "average_wind_capacity_per_sqmeter_final_change_rate_variation": 1,
                "wc_var_s": 1,
                "e_var_t": 1,
                "time": 1,
            },
            "step": {
                "average_wind_capacity_per_sqmeter_final_change_rate_variation": 1,
                "wc_var_s": 1,
                "e_var_t": 1,
                "time": 1,
                "ssp_energy_technology_variation_time": 1,
            },
        }
    },
)
def final_change_rate3():
    """
    Final Educational Attainment Change Rate
    """
    return wc_var_s() + _smooth_final_change_rate3()


_smooth_final_change_rate3 = Smooth(
    lambda: step(
        __data["time"],
        average_wind_capacity_per_sqmeter_final_change_rate_variation() - wc_var_s(),
        2020 + e_var_t(),
    ),
    lambda: ssp_energy_technology_variation_time(),
    lambda: step(
        __data["time"],
        average_wind_capacity_per_sqmeter_final_change_rate_variation() - wc_var_s(),
        2020 + e_var_t(),
    ),
    lambda: 1,
    "_smooth_final_change_rate3",
)


@component.add(
    name="Final Change Rate7",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effect_of_gdp_on_forest_management_practices_increment_final_change_rate_variation": 1,
        "time": 1,
    },
)
def final_change_rate7():
    """
    Final Educational Attainment Change Rate
    """
    return 1.5 + step(
        __data["time"],
        effect_of_gdp_on_forest_management_practices_increment_final_change_rate_variation()
        - 1.5,
        2020,
    )


@component.add(
    name="Final Change Rate8",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effect_of_gdp_on_cropland_management_practices_increment_final_change_rate_variation": 1,
        "time": 1,
    },
)
def final_change_rate8():
    """
    Final Educational Attainment Change Rate
    """
    return 10 + step(
        __data["time"],
        effect_of_gdp_on_cropland_management_practices_increment_final_change_rate_variation()
        - 10,
        2020,
    )


@component.add(
    name="Final Change Rate9",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def final_change_rate9():
    """
    Final Educational Attainment Change Rate
    """
    return 40


@component.add(
    name="Initial Change Rate",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_change_rate():
    """
    Initial Educational Attainment Change Rate
    """
    return 1


@component.add(
    name="Initial Change Rate1",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_change_rate1():
    """
    Initial Educational Attainment Change Rate
    """
    return 4.17e-07


@component.add(
    name="Initial Change Rate10",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_change_rate10():
    """
    Initial Educational Attainment Change Rate
    """
    return 3000000000000.0


@component.add(
    name="Initial Change Rate11",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_change_rate11():
    """
    Initial Educational Attainment Change Rate
    """
    return 140


@component.add(
    name="Initial Change Rate12",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_change_rate12():
    """
    Initial Educational Attainment Change Rate
    """
    return 0.1


@component.add(
    name="Initial Change Rate13",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_change_rate13():
    """
    Initial Educational Attainment Change Rate
    """
    return 50000000.0


@component.add(
    name="Initial Change Rate14",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_change_rate14():
    """
    Initial Educational Attainment Change Rate
    """
    return 40


@component.add(
    name="Initial Change Rate15",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_change_rate15():
    """
    Initial Educational Attainment Change Rate
    """
    return 12


@component.add(
    name="Initial Change Rate16",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_change_rate16():
    """
    Initial Educational Attainment Change Rate
    """
    return 3


@component.add(
    name="Initial Change Rate2",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_change_rate2():
    """
    Initial Educational Attainment Change Rate
    """
    return 1


@component.add(
    name="Initial Change Rate3",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_change_rate3():
    """
    Initial Educational Attainment Change Rate
    """
    return 0.009


@component.add(
    name="Initial Change Rate7",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_change_rate7():
    """
    Initial Educational Attainment Change Rate
    """
    return 1.2


@component.add(
    name="Initial Change Rate8",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_change_rate8():
    """
    Initial Educational Attainment Change Rate
    """
    return 7


@component.add(
    name="Initial Change Rate9",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_change_rate9():
    """
    Initial Educational Attainment Change Rate
    """
    return 30


@component.add(
    name="Other Technology Steepness Final Change Rate Variation",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def other_technology_steepness_final_change_rate_variation():
    """
    Final Educational Attainment Change Rate
    """
    return 6


@component.add(
    name="Other Technology Steepness Ramp Period Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def other_technology_steepness_ramp_period_variation():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50


@component.add(
    name="Ramp Period", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def ramp_period():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50


@component.add(
    name="Ramp Period1",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "renewable_cost_reduction_and_technology_improvement_ramp_period_variation": 1,
        "time": 1,
    },
)
def ramp_period1():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50 + step(
        __data["time"],
        renewable_cost_reduction_and_technology_improvement_ramp_period_variation()
        - 50,
        2020,
    )


@component.add(
    name="Ramp Period10", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def ramp_period10():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50


@component.add(
    name="Ramp Period11", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def ramp_period11():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50


@component.add(
    name="Ramp Period12", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def ramp_period12():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50


@component.add(
    name="Ramp Period13",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "renewable_cost_reduction_and_technology_improvement_ramp_period_variation": 1,
        "time": 1,
    },
)
def ramp_period13():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50 + step(
        __data["time"],
        renewable_cost_reduction_and_technology_improvement_ramp_period_variation()
        - 50,
        2020,
    )


@component.add(
    name="Ramp Period14",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "renewable_cost_reduction_and_technology_improvement_ramp_period_variation": 1,
        "time": 1,
    },
)
def ramp_period14():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50 + step(
        __data["time"],
        renewable_cost_reduction_and_technology_improvement_ramp_period_variation()
        - 50,
        2020,
    )


@component.add(
    name="Ramp Period15",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "renewable_cost_reduction_and_technology_improvement_ramp_period_variation": 1,
        "time": 1,
    },
)
def ramp_period15():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50 + step(
        __data["time"],
        renewable_cost_reduction_and_technology_improvement_ramp_period_variation()
        - 50,
        2020,
    )


@component.add(
    name="Ramp Period16",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"other_technology_steepness_ramp_period_variation": 1, "time": 1},
)
def ramp_period16():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50 + step(
        __data["time"], other_technology_steepness_ramp_period_variation() - 50, 2020
    )


@component.add(
    name="Ramp Period2",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "renewable_cost_reduction_and_technology_improvement_ramp_period_variation": 1,
        "time": 1,
    },
)
def ramp_period2():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50 + step(
        __data["time"],
        renewable_cost_reduction_and_technology_improvement_ramp_period_variation()
        - 50,
        2020,
    )


@component.add(
    name="Ramp Period3",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "renewable_cost_reduction_and_technology_improvement_ramp_period_variation": 1,
        "time": 1,
    },
)
def ramp_period3():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50 + step(
        __data["time"],
        renewable_cost_reduction_and_technology_improvement_ramp_period_variation()
        - 50,
        2020,
    )


@component.add(
    name="Ramp Period4", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def ramp_period4():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50


@component.add(
    name="Ramp Period5", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def ramp_period5():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50


@component.add(
    name="Ramp Period6", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def ramp_period6():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50


@component.add(
    name="Ramp Period7",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effect_of_gdp_on_forest_management_practices_increment_ramp_period_variation": 1,
        "time": 1,
    },
)
def ramp_period7():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50 + step(
        __data["time"],
        effect_of_gdp_on_forest_management_practices_increment_ramp_period_variation()
        - 50,
        2020,
    )


@component.add(
    name="Ramp Period8",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effect_of_gdp_on_cropland_management_practices_increment_ramp_period_variation": 1,
        "time": 1,
    },
)
def ramp_period8():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50 + step(
        __data["time"],
        effect_of_gdp_on_cropland_management_practices_increment_ramp_period_variation()
        - 50,
        2020,
    )


@component.add(
    name="Ramp Period9", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def ramp_period9():
    """
    Period of increasing investments in Educational Attainment.
    """
    return 50


@component.add(name="Ramp Start", comp_type="Constant", comp_subtype="Normal")
def ramp_start():
    return 2020


@component.add(name="Ramp Start1", comp_type="Constant", comp_subtype="Normal")
def ramp_start1():
    return 2020


@component.add(name="Ramp Start10", comp_type="Constant", comp_subtype="Normal")
def ramp_start10():
    return 2020


@component.add(name="Ramp Start11", comp_type="Constant", comp_subtype="Normal")
def ramp_start11():
    return 2020


@component.add(name="Ramp Start12", comp_type="Constant", comp_subtype="Normal")
def ramp_start12():
    return 2020


@component.add(name="Ramp Start13", comp_type="Constant", comp_subtype="Normal")
def ramp_start13():
    return 2020


@component.add(name="Ramp Start14", comp_type="Constant", comp_subtype="Normal")
def ramp_start14():
    return 2020


@component.add(name="Ramp Start15", comp_type="Constant", comp_subtype="Normal")
def ramp_start15():
    return 2020


@component.add(name="Ramp Start16", comp_type="Constant", comp_subtype="Normal")
def ramp_start16():
    return 2020


@component.add(name="Ramp Start2", comp_type="Constant", comp_subtype="Normal")
def ramp_start2():
    return 2020


@component.add(name="Ramp Start3", comp_type="Constant", comp_subtype="Normal")
def ramp_start3():
    return 2020


@component.add(name="Ramp Start4", comp_type="Constant", comp_subtype="Normal")
def ramp_start4():
    return 2020


@component.add(name="Ramp Start5", comp_type="Constant", comp_subtype="Normal")
def ramp_start5():
    return 2020


@component.add(name="Ramp Start6", comp_type="Constant", comp_subtype="Normal")
def ramp_start6():
    return 2020


@component.add(name="Ramp Start7", comp_type="Constant", comp_subtype="Normal")
def ramp_start7():
    return 2020


@component.add(name="Ramp Start8", comp_type="Constant", comp_subtype="Normal")
def ramp_start8():
    return 2020


@component.add(name="Ramp Start9", comp_type="Constant", comp_subtype="Normal")
def ramp_start9():
    return 2020


@component.add(
    name="RCB S", units="1/Year", comp_type="Constant", comp_subtype="Normal"
)
def rcb_s():
    """
    Final Educational Attainment Change Rate
    """
    return 30000000.0


@component.add(
    name="RCB Var S",
    units="1/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_rcb_var_s": 1},
    other_deps={
        "_smooth_rcb_var_s": {
            "initial": {"rcb_s": 1, "time": 1},
            "step": {"rcb_s": 1, "time": 1},
        }
    },
)
def rcb_var_s():
    """
    Final Educational Attainment Change Rate
    """
    return 30000000.0 + _smooth_rcb_var_s()


_smooth_rcb_var_s = Smooth(
    lambda: step(__data["time"], rcb_s() - 30000000.0, 2020),
    lambda: 1,
    lambda: step(__data["time"], rcb_s() - 30000000.0, 2020),
    lambda: 1,
    "_smooth_rcb_var_s",
)


@component.add(
    name="RCS S", units="1/Year", comp_type="Constant", comp_subtype="Normal"
)
def rcs_s():
    """
    Final Educational Attainment Change Rate
    """
    return 10


@component.add(
    name="RCS Var S",
    units="1/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_rcs_var_s": 1},
    other_deps={
        "_smooth_rcs_var_s": {
            "initial": {"rcs_s": 1, "time": 1},
            "step": {"rcs_s": 1, "time": 1},
        }
    },
)
def rcs_var_s():
    """
    Final Educational Attainment Change Rate
    """
    return 10 + _smooth_rcs_var_s()


_smooth_rcs_var_s = Smooth(
    lambda: step(__data["time"], rcs_s() - 10, 2020),
    lambda: 1,
    lambda: step(__data["time"], rcs_s() - 10, 2020),
    lambda: 1,
    "_smooth_rcs_var_s",
)


@component.add(
    name="RCW S", units="1/Year", comp_type="Constant", comp_subtype="Normal"
)
def rcw_s():
    """
    Final Educational Attainment Change Rate
    """
    return 7


@component.add(
    name="RCW Var S",
    units="1/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_rcw_var_s": 1},
    other_deps={
        "_smooth_rcw_var_s": {
            "initial": {"rcw_s": 1, "time": 1},
            "step": {"rcw_s": 1, "time": 1},
        }
    },
)
def rcw_var_s():
    """
    Final Educational Attainment Change Rate
    """
    return 7 + _smooth_rcw_var_s()


_smooth_rcw_var_s = Smooth(
    lambda: step(__data["time"], rcw_s() - 7, 2020),
    lambda: 1,
    lambda: step(__data["time"], rcw_s() - 7, 2020),
    lambda: 1,
    "_smooth_rcw_var_s",
)


@component.add(
    name="Reduced C Emissions of Coal",
    units="TonC/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reduced_c_emissions_of_coal():
    """
    64000
    """
    return 953660


@component.add(
    name="Reduced C Emissions of Gas",
    units="TonC/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reduced_c_emissions_of_gas():
    """
    Erlier Felix;108000
    """
    return 569870


@component.add(
    name="Reduced Carbon Emissions of Oil",
    units="TonC/Mtoe",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reduced_carbon_emissions_of_oil():
    """
    83650
    """
    return 904814


@component.add(
    name="Reference Cost of Biomass Energy Production Final Change Rate Variation",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_cost_of_biomass_energy_production_final_change_rate_variation():
    """
    Final Educational Attainment Change Rate
    """
    return 30000000.0


@component.add(
    name="Reference Cost of Solar Energy Production Final Change Rate Variation",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_cost_of_solar_energy_production_final_change_rate_variation():
    """
    Final Educational Attainment Change Rate
    """
    return 10


@component.add(
    name="Reference Cost of Wind Energy Production Final Change Rate Variation",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_cost_of_wind_energy_production_final_change_rate_variation():
    """
    Final Educational Attainment Change Rate
    """
    return 7


@component.add(
    name="Renewable Cost Reduction and Technology Improvement Ramp Period Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def renewable_cost_reduction_and_technology_improvement_ramp_period_variation():
    return 50


@component.add(name="SC S", units="1/Year", comp_type="Constant", comp_subtype="Normal")
def sc_s():
    """
    Final Educational Attainment Change Rate
    """
    return 2


@component.add(
    name="SC Var S",
    units="1/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_sc_var_s": 1},
    other_deps={
        "_smooth_sc_var_s": {
            "initial": {"sc_s": 1, "time": 1},
            "step": {"sc_s": 1, "time": 1},
        }
    },
)
def sc_var_s():
    """
    Final Educational Attainment Change Rate
    """
    return 2 + _smooth_sc_var_s()


_smooth_sc_var_s = Smooth(
    lambda: step(__data["time"], sc_s() - 2, 2020),
    lambda: 1,
    lambda: step(__data["time"], sc_s() - 2, 2020),
    lambda: 1,
    "_smooth_sc_var_s",
)


@component.add(
    name="SCENARIO ON",
    units="Dmnl",
    limits=(0.0, 1.0, 1.0),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1},
)
def scenario_on():
    """
    Scenario is on to consider the impact on GDP
    """
    return step(__data["time"], 1, 2010)


@component.add(
    name="Solar Conversion Efficiency Factor Final Change Rate Variation",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def solar_conversion_efficiency_factor_final_change_rate_variation():
    """
    Final Educational Attainment Change Rate
    """
    return 2


@component.add(
    name="Technological Improvement Scenario Switch Variation",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"technological_improvement_scenario_variation": 4},
)
def technological_improvement_scenario_switch_variation():
    return if_then_else(
        np.logical_and(
            0 <= technological_improvement_scenario_variation(),
            technological_improvement_scenario_variation() < 1,
        ),
        lambda: 0,
        lambda: 0,
    ) + if_then_else(
        np.logical_and(
            1 <= technological_improvement_scenario_variation(),
            technological_improvement_scenario_variation() < 2,
        ),
        lambda: 1,
        lambda: 0,
    )


@component.add(
    name="Technological Improvement Scenario Variation",
    comp_type="Constant",
    comp_subtype="Normal",
)
def technological_improvement_scenario_variation():
    return 1


@component.add(
    name="Variable",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_change_rate": 1,
        "time": 1,
        "change_rate_start": 1,
        "change_rate_finish": 1,
        "change_rate_slope": 1,
    },
)
def variable():
    """
    Educational Attainment Change Rate.
    """
    return initial_change_rate() + ramp(
        __data["time"], change_rate_slope(), change_rate_start(), change_rate_finish()
    )


@component.add(
    name="Variable10 Industrial Water",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_change_rate10": 1,
        "time": 1,
        "change_rate_start10": 1,
        "change_rate_finish10": 1,
        "scenario_on": 1,
        "change_rate_slope10": 1,
    },
)
def variable10_industrial_water():
    """
    Educational Attainment Change Rate.
    """
    return initial_change_rate10() + scenario_on() * ramp(
        __data["time"],
        change_rate_slope10(),
        change_rate_start10(),
        change_rate_finish10(),
    )


@component.add(
    name="Variable11 Domestic Water",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_change_rate11": 1,
        "time": 1,
        "change_rate_finish11": 1,
        "change_rate_start11": 1,
        "change_rate_slope11": 1,
        "scenario_on": 1,
    },
)
def variable11_domestic_water():
    """
    Educational Attainment Change Rate.
    """
    return initial_change_rate11() + scenario_on() * ramp(
        __data["time"],
        change_rate_slope11(),
        change_rate_start11(),
        change_rate_finish11(),
    )


@component.add(
    name="Variable12 Water Recovery",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_change_rate12": 1,
        "change_rate_start12": 1,
        "time": 1,
        "change_rate_finish12": 1,
        "scenario_on": 1,
        "change_rate_slope12": 1,
    },
)
def variable12_water_recovery():
    """
    Educational Attainment Change Rate.
    """
    return initial_change_rate12() + scenario_on() * ramp(
        __data["time"],
        change_rate_slope12(),
        change_rate_start12(),
        change_rate_finish12(),
    )


@component.add(
    name="Variable13 Biomas Cost",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_change_rate13": 1,
        "time": 1,
        "change_rate_slope13": 1,
        "change_rate_start13": 1,
        "scenario_on": 1,
        "change_rate_finish13": 1,
    },
)
def variable13_biomas_cost():
    """
    Educational Attainment Change Rate.
    """
    return initial_change_rate13() + scenario_on() * ramp(
        __data["time"],
        change_rate_slope13(),
        change_rate_start13(),
        change_rate_finish13(),
    )


@component.add(
    name="Variable14 Solar Cost",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_change_rate14": 1,
        "time": 1,
        "change_rate_finish14": 1,
        "change_rate_start14": 1,
        "change_rate_slope14": 1,
        "scenario_on": 1,
    },
)
def variable14_solar_cost():
    """
    Educational Attainment Change Rate.
    """
    return initial_change_rate14() + scenario_on() * ramp(
        __data["time"],
        change_rate_slope14(),
        change_rate_start14(),
        change_rate_finish14(),
    )


@component.add(
    name="Variable15 Wind Cost",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_change_rate15": 1,
        "change_rate_finish15": 1,
        "time": 1,
        "scenario_on": 1,
        "change_rate_slope15": 1,
        "change_rate_start15": 1,
    },
)
def variable15_wind_cost():
    """
    Educational Attainment Change Rate.
    """
    return initial_change_rate15() + scenario_on() * ramp(
        __data["time"],
        change_rate_slope15(),
        change_rate_start15(),
        change_rate_finish15(),
    )


@component.add(
    name="Variable1 Biomass",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_change_rate1": 1,
        "time": 1,
        "change_rate_slope1": 1,
        "change_rate_start1": 1,
        "change_rate_finish1": 1,
        "scenario_on": 1,
    },
)
def variable1_biomass():
    """
    Educational Attainment Change Rate.
    """
    return initial_change_rate1() + scenario_on() * ramp(
        __data["time"],
        change_rate_slope1(),
        change_rate_start1(),
        change_rate_finish1(),
    )


@component.add(
    name="Variable2 Solar",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_change_rate2": 1,
        "time": 1,
        "change_rate_slope2": 1,
        "change_rate_finish2": 1,
        "change_rate_start2": 1,
        "scenario_on": 1,
    },
)
def variable2_solar():
    """
    Educational Attainment Change Rate.
    """
    return initial_change_rate2() + scenario_on() * ramp(
        __data["time"],
        change_rate_slope2(),
        change_rate_start2(),
        change_rate_finish2(),
    )


@component.add(
    name="Variable3 Wind",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_change_rate3": 1,
        "time": 1,
        "change_rate_finish3": 1,
        "change_rate_start3": 1,
        "scenario_on": 1,
        "change_rate_slope3": 1,
    },
)
def variable3_wind():
    """
    Educational Attainment Change Rate.
    """
    return initial_change_rate3() + scenario_on() * ramp(
        __data["time"],
        change_rate_slope3(),
        change_rate_start3(),
        change_rate_finish3(),
    )


@component.add(
    name="Variable7 Forest MP",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_change_rate7": 1,
        "change_rate_slope7": 1,
        "time": 1,
        "change_rate_start7": 1,
        "scenario_on": 1,
        "change_rate_finish7": 1,
    },
)
def variable7_forest_mp():
    """
    Educational Attainment Change Rate.
    """
    return initial_change_rate7() + scenario_on() * ramp(
        __data["time"],
        change_rate_slope7(),
        change_rate_start7(),
        change_rate_finish7(),
    )


@component.add(
    name="Variable8 Cropland MP",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_change_rate8": 1,
        "time": 1,
        "change_rate_slope8": 1,
        "change_rate_finish8": 1,
        "change_rate_start8": 1,
        "scenario_on": 1,
    },
)
def variable8_cropland_mp():
    """
    Educational Attainment Change Rate.
    """
    return initial_change_rate8() + scenario_on() * ramp(
        __data["time"],
        change_rate_slope8(),
        change_rate_start8(),
        change_rate_finish8(),
    )


@component.add(
    name="Variable9 Food land MP",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_change_rate9": 1,
        "time": 1,
        "change_rate_finish9": 1,
        "change_rate_start9": 1,
        "change_rate_slope9": 1,
        "scenario_on": 1,
    },
)
def variable9_food_land_mp():
    """
    Educational Attainment Change Rate.
    """
    return initial_change_rate9() + scenario_on() * ramp(
        __data["time"],
        change_rate_slope9(),
        change_rate_start9(),
        change_rate_finish9(),
    )


@component.add(name="WC S", units="1/Year", comp_type="Constant", comp_subtype="Normal")
def wc_s():
    """
    Final Educational Attainment Change Rate
    """
    return 0.35


@component.add(
    name="WC Var S",
    units="1/Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_wc_var_s": 1},
    other_deps={
        "_smooth_wc_var_s": {
            "initial": {"wc_s": 1, "time": 1},
            "step": {"wc_s": 1, "time": 1},
        }
    },
)
def wc_var_s():
    """
    Final Educational Attainment Change Rate
    """
    return 0.35 + _smooth_wc_var_s()


_smooth_wc_var_s = Smooth(
    lambda: step(__data["time"], wc_s() - 0.35, 2020),
    lambda: 1,
    lambda: step(__data["time"], wc_s() - 0.35, 2020),
    lambda: 1,
    "_smooth_wc_var_s",
)
