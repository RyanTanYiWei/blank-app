"""
Module ssp_calibration
Translated using PySD version 3.14.3
"""

@component.add(
    name="Agricultural Land Area",
    units="Million ha",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pasture_land_indicator": 1, "total_croplands_indicator": 1},
)
def agricultural_land_area():
    return pasture_land_indicator() + total_croplands_indicator()


@component.add(
    name="Fossil Energy Production Indicator",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "coal_production_indicator": 1,
        "gas_production_indicator": 1,
        "oil_production_indicator": 1,
    },
)
def fossil_energy_production_indicator():
    return (
        coal_production_indicator()
        + gas_production_indicator()
        + oil_production_indicator()
    )


@component.add(
    name="Renewable Energy Production Indicator",
    units="EJ/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biomass_energy_production_indicator": 1,
        "solar_energy_production_indicator": 1,
        "wind_energy_production_indicator": 1,
    },
)
def renewable_energy_production_indicator():
    return (
        biomass_energy_production_indicator()
        + solar_energy_production_indicator()
        + wind_energy_production_indicator()
    )


@component.add(
    name="Total Food Production",
    units="Million tDM/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "livestock_production_indicator": 1,
        "nonenergy_crops_production_indicator": 1,
    },
)
def total_food_production():
    return livestock_production_indicator() + nonenergy_crops_production_indicator()
