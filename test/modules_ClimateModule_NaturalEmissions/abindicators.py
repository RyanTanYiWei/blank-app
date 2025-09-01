"""
Module abindicators
Translated using PySD version 3.14.3
"""

@component.add(
    name="Airborne Fraction",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_c_emission": 2,
        "ch4_oxidation": 1,
        "flux_humus_to_atmosphere": 1,
        "flux_biomass_to_atmosphere": 1,
        "flux_atmosphere_to_biomass": 1,
        "flux_atmosphere_to_ocean": 1,
    },
)
def airborne_fraction():
    return (
        total_c_emission()
        + ch4_oxidation()
        + flux_humus_to_atmosphere()
        + flux_biomass_to_atmosphere()
        - flux_atmosphere_to_biomass()
        - flux_atmosphere_to_ocean()
    ) / float(np.maximum(total_c_emission(), 1))


@component.add(
    name="Carbon Pool Atmosphere",
    units="MTonCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_atmosphere": 1, "co2_to_c": 1, "tonco2_to_mtonco2": 1},
)
def carbon_pool_atmosphere():
    return c_in_atmosphere() * co2_to_c() * tonco2_to_mtonco2()


@component.add(
    name="Carbon Pool Plant",
    units="MTonCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_biomass": 1, "co2_to_c": 1, "tonco2_to_mtonco2": 1},
)
def carbon_pool_plant():
    return c_in_biomass() * co2_to_c() * tonco2_to_mtonco2()


@component.add(
    name="Carbon Pool Soil",
    units="MTonCO2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"c_in_humus": 1, "co2_to_c": 1, "tonco2_to_mtonco2": 1},
)
def carbon_pool_soil():
    return c_in_humus() * co2_to_c() * tonco2_to_mtonco2()


@component.add(
    name="Conversion to ZJ",
    units="m*m*ZJ/(W*Year)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "earth_surface_area": 1,
        "second_to_years": 1,
        "unit_w_to_js": 1,
        "j_to_zj": 1,
    },
)
def conversion_to_zj():
    return earth_surface_area() * second_to_years() * unit_w_to_js() / j_to_zj()


@component.add(
    name="Earth Surface Area", units="m*m", comp_type="Constant", comp_subtype="Normal"
)
def earth_surface_area():
    return 510064000000000.0


@component.add(
    name="Heat Content 0 700m",
    units="ZJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"heat_in_deep_ocean_1": 1, "conversion_to_zj": 1},
)
def heat_content_0_700m():
    return heat_in_deep_ocean_1() * conversion_to_zj()


@component.add(
    name="Heat Content 700 2000m",
    units="ZJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"heat_in_deep_ocean_2": 1, "conversion_to_zj": 1},
)
def heat_content_700_2000m():
    return heat_in_deep_ocean_2() * conversion_to_zj()


@component.add(
    name="Heat Content Ocean",
    units="ZJ",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "heat_in_deep_ocean_1": 1,
        "heat_in_deep_ocean_2": 1,
        "heat_in_deep_ocean_3": 1,
        "conversion_to_zj": 1,
    },
)
def heat_content_ocean():
    return (
        heat_in_deep_ocean_1() + heat_in_deep_ocean_2() + heat_in_deep_ocean_3()
    ) * conversion_to_zj()


@component.add(
    name="Heat Uptake",
    units="ZJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effective_radiative_forcing": 1,
        "feedback_cooling": 1,
        "conversion_to_zj": 1,
    },
)
def heat_uptake():
    return (effective_radiative_forcing() - feedback_cooling()) * conversion_to_zj()


@component.add(
    name="J to ZJ", units="J/ZJ", comp_type="Constant", comp_subtype="Normal"
)
def j_to_zj():
    return 1e21


@component.add(
    name="Net CH4 Emissions in MTonCH4",
    units="MTonCH4/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "natural_ch4_emissions": 1,
        "total_ch4_breakdown": 1,
        "mt_ch4_to_tch4": 1,
    },
)
def net_ch4_emissions_in_mtonch4():
    return (natural_ch4_emissions() - total_ch4_breakdown()) / mt_ch4_to_tch4()


@component.add(
    name="Net Land to Atmosphere Flux CO2",
    units="MTonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "flux_biomass_to_atmosphere": 1,
        "flux_humus_to_atmosphere": 1,
        "flux_atmosphere_to_biomass": 1,
        "tonco2_to_mtonco2": 1,
        "co2_to_c": 1,
    },
)
def net_land_to_atmosphere_flux_co2():
    return (
        (
            flux_biomass_to_atmosphere()
            + flux_humus_to_atmosphere()
            - flux_atmosphere_to_biomass()
        )
        * tonco2_to_mtonco2()
        * co2_to_c()
    )


@component.add(
    name="Net Ocean to Atmosphere Flux CO2",
    units="MTonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"flux_atmosphere_to_ocean": 1, "tonco2_to_mtonco2": 1, "co2_to_c": 1},
)
def net_ocean_to_atmosphere_flux_co2():
    return -flux_atmosphere_to_ocean() * tonco2_to_mtonco2() * co2_to_c()


@component.add(
    name="Net Primary Productivity",
    units="MTonCO2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "co2_to_c": 1,
        "flux_atmosphere_to_biomass": 1,
        "flux_biomass_to_humus": 1,
        "tonco2_to_mtonco2": 1,
    },
)
def net_primary_productivity():
    return (
        co2_to_c()
        * (flux_atmosphere_to_biomass() - flux_biomass_to_humus())
        * tonco2_to_mtonco2()
    )


@component.add(
    name="second to years",
    units="sec/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def second_to_years():
    return 60 * 60 * 24 * 365.24


@component.add(
    name="TonCO2 to MTonCO2",
    units="MTonCO2/TonCO2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def tonco2_to_mtonco2():
    return 1e-06


@component.add(
    name='"unit W to J/s"', units="J/sec/W", comp_type="Constant", comp_subtype="Normal"
)
def unit_w_to_js():
    return 1
