"""
Module biodiversity
Translated using PySD version 3.14.3
"""

@component.add(
    name="Agriculture Biomass Production Land Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "land_allocated_for_energy_crops": 1,
        "land_allocated_for_food_crops": 1,
    },
)
def agriculture_biomass_production_land_ratio():
    """
    Ratio of agricultural land area being used for crops biomass production.
    """
    return land_allocated_for_energy_crops() / land_allocated_for_food_crops()


@component.add(
    name="Agriculture Biomass Production on Biodiversity Elasticity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def agriculture_biomass_production_on_biodiversity_elasticity():
    """
    Elasticity of impact of crops biomass production on species carrying capacity.
    """
    return 2


@component.add(
    name="Biodiversity Impact Climate Damage Nonlinearity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biodiversity_impact_climate_damage_nonlinearity():
    """
    Elasticity of impact of climate risk on species carrying capacity.
    """
    return 1.5


@component.add(
    name="Biodiversity Impact Climate Damage Scale",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biodiversity_impact_climate_damage_scale():
    """
    The maximum fractional impact of climate risk on species carrying capacity.
    """
    return 0.1


@component.add(
    name="Biodiversity Impact Fertilizer Consumption Nonlinearity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biodiversity_impact_fertilizer_consumption_nonlinearity():
    """
    Elasticity of impact of fertilization consumption on species carrying capacity.
    """
    return 1.5


@component.add(
    name="Biodiversity Impact Fertilizer Consumption Scale",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biodiversity_impact_fertilizer_consumption_scale():
    """
    The maximum fractional impact of fertilization practices on species carrying capacity.
    """
    return 0.2


@component.add(
    name="Biodiversity Impact Reference Fertilizer Consumption",
    units="TonNutrient/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biodiversity_impact_reference_fertilizer_consumption():
    """
    Value against which the fertilization consumption is compared to in order to determine its impact on species carrying capacity.: 4e+008
    """
    return 25000000.0


@component.add(
    name="Biodiversity Impact Reference Temperature",
    units="DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biodiversity_impact_reference_temperature():
    """
    Value against which the temperature anomalies are compared to in order to determine its impact on species carrying capacity.
    """
    return 3


@component.add(
    name="Extinction Factor",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def extinction_factor():
    """
    The minimum fractional extinction rate.
    """
    return 0.01


@component.add(
    name="Forest Biomass Production Land Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"actual_forest_land_harvested": 1, "forest_land": 1},
)
def forest_biomass_production_land_ratio():
    """
    Ratio of forest land area being used for biomass production.
    """
    return actual_forest_land_harvested() / forest_land()


@component.add(
    name="Forest Biomass Production on Biodiversity Elasticity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def forest_biomass_production_on_biodiversity_elasticity():
    """
    Elasticity of impact of forest biomass production on species carrying capacity.
    """
    return 2


@component.add(
    name="Impact of Agricultural Land Changes on Biodiversity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agricultural_land": 1,
        "init_agricultural_land": 1,
        "impact_of_agricultural_land_changes_on_biodiversity_elasticity": 1,
    },
)
def impact_of_agricultural_land_changes_on_biodiversity():
    """
    Nonlinear function representing impact of agricultural land use change on species carrying capacity.
    """
    return (
        1 / (agricultural_land() / init_agricultural_land())
    ) ** impact_of_agricultural_land_changes_on_biodiversity_elasticity()


@component.add(
    name="Impact of Agricultural Land Changes on Biodiversity Elasticity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def impact_of_agricultural_land_changes_on_biodiversity_elasticity():
    """
    Elasticity of impact of agricultural land use change on species carrying capacity.
    """
    return 0.1


@component.add(
    name="Impact of Agriculture Biomass Production on Biodiversity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agriculture_biomass_production_land_ratio": 1,
        "agriculture_biomass_production_on_biodiversity_elasticity": 1,
    },
)
def impact_of_agriculture_biomass_production_on_biodiversity():
    """
    Nonlinear function representing impact of crops biomass production on species carrying capacity.
    """
    return (
        1 - agriculture_biomass_production_land_ratio()
    ) ** agriculture_biomass_production_on_biodiversity_elasticity()


@component.add(
    name="Impact of Biomass Production on Biodiversity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "impact_of_agriculture_biomass_production_on_biodiversity": 1,
        "impact_of_forest_biomass_production_on_biodiversity": 1,
    },
)
def impact_of_biomass_production_on_biodiversity():
    """
    Total impact of forest and crops biomass production on species carrying capacity.
    """
    return (
        impact_of_agriculture_biomass_production_on_biodiversity()
        * impact_of_forest_biomass_production_on_biodiversity()
    )


@component.add(
    name="Impact of Climate Damage on Biodiversity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biodiversity_impact_climate_damage_scale": 1,
        "temperature_change_from_preindustrial": 1,
        "biodiversity_impact_reference_temperature": 1,
        "biodiversity_impact_climate_damage_nonlinearity": 1,
    },
)
def impact_of_climate_damage_on_biodiversity():
    """
    Nonlinear function representing impact of climate risk on species carrying capacity.
    """
    return 1 / (
        1
        + biodiversity_impact_climate_damage_scale()
        * (
            temperature_change_from_preindustrial()
            / biodiversity_impact_reference_temperature()
        )
        ** biodiversity_impact_climate_damage_nonlinearity()
    )


@component.add(
    name="Impact of Fertilizer Consumption on Biodiversity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biodiversity_impact_fertilizer_consumption_scale": 1,
        "biodiversity_impact_fertilizer_consumption_nonlinearity": 1,
        "biodiversity_impact_reference_fertilizer_consumption": 1,
        "total_fertilizer_runoff_and_leaching": 1,
    },
)
def impact_of_fertilizer_consumption_on_biodiversity():
    """
    Nonlinear function representing impact of fertilization practices on species carrying capacity.
    """
    return 1 / (
        1
        + biodiversity_impact_fertilizer_consumption_scale()
        * (
            total_fertilizer_runoff_and_leaching()
            / biodiversity_impact_reference_fertilizer_consumption()
        )
        ** biodiversity_impact_fertilizer_consumption_nonlinearity()
    )


@component.add(
    name="Impact of Forest Biomass Production on Biodiversity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "forest_biomass_production_land_ratio": 1,
        "forest_biomass_production_on_biodiversity_elasticity": 1,
    },
)
def impact_of_forest_biomass_production_on_biodiversity():
    """
    Nonlinear function representing impact of forest biomass production on species carrying capacity.
    """
    return (
        1 - forest_biomass_production_land_ratio()
    ) ** forest_biomass_production_on_biodiversity_elasticity()


@component.add(
    name="Impact of Forest Land Changes on Biodiversity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "forest_land": 1,
        "init_forest_land": 1,
        "impact_of_forest_land_changes_on_biodiversity_elasticity": 1,
    },
)
def impact_of_forest_land_changes_on_biodiversity():
    """
    Nonlinear function representing impact of forest land use change on species carrying capacity.
    """
    return (
        forest_land() / init_forest_land()
    ) ** impact_of_forest_land_changes_on_biodiversity_elasticity()


@component.add(
    name="Impact of Forest Land Changes on Biodiversity Elasticity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def impact_of_forest_land_changes_on_biodiversity_elasticity():
    """
    Elasticity of impact of forest land use change on species carrying capacity.
    """
    return 0.1


@component.add(
    name="Impact of Land Use Change on Biodiversity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "impact_of_agricultural_land_changes_on_biodiversity": 1,
        "impact_of_forest_land_changes_on_biodiversity": 1,
        "impact_of_other_land_changes_on_biodiversity": 1,
    },
)
def impact_of_land_use_change_on_biodiversity():
    """
    Total impact of land use change on species carrying capacity.
    """
    return (
        impact_of_agricultural_land_changes_on_biodiversity()
        * impact_of_forest_land_changes_on_biodiversity()
        * impact_of_other_land_changes_on_biodiversity()
    )


@component.add(
    name="Impact of Other Land Changes on Biodiversity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "other_land": 1,
        "init_other_land": 1,
        "impact_of_other_land_changes_on_biodiversity_elasticity": 1,
    },
)
def impact_of_other_land_changes_on_biodiversity():
    """
    Nonlinear function representing impact of other land use change on species carrying capacity.
    """
    return (
        other_land() / init_other_land()
    ) ** impact_of_other_land_changes_on_biodiversity_elasticity()


@component.add(
    name="Impact of Other Land Changes on Biodiversity Elasticity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def impact_of_other_land_changes_on_biodiversity_elasticity():
    """
    Elasticity of impact of other land use change on species carrying capacity.
    """
    return 0.1


@component.add(
    name="INIT Species Abundance",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def init_species_abundance():
    """
    Mean species abundance in year 1900.
    """
    return 85


@component.add(
    name="Mean Species Abundance",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_mean_species_abundance": 1},
    other_deps={
        "_integ_mean_species_abundance": {
            "initial": {"init_species_abundance": 1},
            "step": {"species_regeneration_rate": 1, "species_extinction_rate": 1},
        }
    },
)
def mean_species_abundance():
    """
    Mean abundance of original species relative to their abundance in undisturbed ecosystems. Source of Historical Data: Secretariat of the Convention for Biological Diversity (CBD), Cross-roads of Life on Earth - Exploring means to meet the 2010 Biodiversity Target, 2007
    """
    return _integ_mean_species_abundance()


_integ_mean_species_abundance = Integ(
    lambda: species_regeneration_rate() - species_extinction_rate(),
    lambda: init_species_abundance(),
    "_integ_mean_species_abundance",
)


@component.add(
    name="MSA2100",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mean_species_abundance": 1, "time": 1},
)
def msa2100():
    return 0 + step(__data["time"], mean_species_abundance(), 2100)


@component.add(
    name="MSA 2016",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="SampleIfTrue",
    depends_on={"_sampleiftrue_msa_2016": 1},
    other_deps={
        "_sampleiftrue_msa_2016": {
            "initial": {},
            "step": {"time": 1, "mean_species_abundance": 1},
        }
    },
)
def msa_2016():
    return _sampleiftrue_msa_2016()


_sampleiftrue_msa_2016 = SampleIfTrue(
    lambda: time() == 2016,
    lambda: mean_species_abundance(),
    lambda: 0,
    "_sampleiftrue_msa_2016",
)


@component.add(
    name="MSA change percentage",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "msa2100": 1, "msa_2016": 2},
)
def msa_change_percentage():
    """
    This is the percentage of change in MSA between 2016 and 2100. Therefore, it is zero all other times except 2100.
    """
    return if_then_else(
        time() == 2100, lambda: 100 * (msa2100() - msa_2016()) / msa_2016(), lambda: 0
    )


@component.add(
    name="Reference Species Carrying Capacity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_species_carrying_capacity():
    """
    Reference species carrying capacity for year 1900.
    """
    return 81


@component.add(
    name="Regeneration Factor",
    units="1/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def regeneration_factor():
    """
    The maximum fractional net regeneration rate.
    """
    return 0.04


@component.add(
    name="Species Abundance Realtive to Carrying Capacity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mean_species_abundance": 1, "species_carrying_capacity": 1},
)
def species_abundance_realtive_to_carrying_capacity():
    """
    The ratio of species abundance to carrying capacity determines the fractional regeneration and extinction rates.
    """
    return mean_species_abundance() / species_carrying_capacity()


@component.add(
    name="Species Carrying Capacity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_species_carrying_capacity": 1,
        "impact_of_biomass_production_on_biodiversity": 1,
        "impact_of_climate_damage_on_biodiversity": 1,
        "impact_of_fertilizer_consumption_on_biodiversity": 1,
        "impact_of_land_use_change_on_biodiversity": 1,
    },
)
def species_carrying_capacity():
    """
    The carrying capacity defines the equilibrium or maximum sustainable species population. It is impacted by fertilization, biomas production, climate risk and land use change.
    """
    return (
        reference_species_carrying_capacity()
        * impact_of_biomass_production_on_biodiversity()
        * impact_of_climate_damage_on_biodiversity()
        * impact_of_fertilizer_consumption_on_biodiversity()
        * impact_of_land_use_change_on_biodiversity()
    )


@component.add(
    name="Species Extinction",
    units="Dmnl/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "extinction_factor": 1,
        "species_abundance_realtive_to_carrying_capacity": 1,
    },
)
def species_extinction():
    """
    The fractional species extinctionrate is an increasing function of the ratio of species abundance carrying capacity. A power function is assumed.
    """
    return extinction_factor() * (
        1 + species_abundance_realtive_to_carrying_capacity() ** 2
    )


@component.add(
    name="Species Extinction Rate",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mean_species_abundance": 1, "species_extinction": 1},
)
def species_extinction_rate():
    """
    Average rate of species extinction.
    """
    return mean_species_abundance() * species_extinction()


@component.add(
    name="Species Regeneration",
    units="Dmnl/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "regeneration_factor": 1,
        "species_abundance_realtive_to_carrying_capacity": 1,
    },
)
def species_regeneration():
    """
    The fractional species regeneration rate is a declining function of the species abundance relative to the carrying capacity. A logistic function is used.
    """
    return regeneration_factor() * (
        1
        - 1
        / (
            1
            + float(
                np.exp(-7 * (species_abundance_realtive_to_carrying_capacity() - 1))
            )
        )
    )


@component.add(
    name="Species Regeneration Rate",
    units="1/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mean_species_abundance": 1, "species_regeneration": 1},
)
def species_regeneration_rate():
    """
    Average rate of species regeneration.
    """
    return mean_species_abundance() * species_regeneration()


@component.add(
    name="Total Fertilizer Runoff and Leaching",
    units="Ton/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "nitrogen_leaching_and_runoff_rate": 1,
        "phosphorus_erosion_leaching_and_runoff_rate": 1,
    },
)
def total_fertilizer_runoff_and_leaching():
    return (
        nitrogen_leaching_and_runoff_rate()
        + phosphorus_erosion_leaching_and_runoff_rate()
    )
