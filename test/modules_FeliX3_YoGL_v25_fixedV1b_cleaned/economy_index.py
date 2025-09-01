"""
Module economy_index
Translated using PySD version 3.14.3
"""

@component.add(
    name="Cropland Ecosystem Value",
    units="$/ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def cropland_ecosystem_value():
    """
    Ecosystem value of unit area of cropland.
    """
    return 90


@component.add(
    name="Education index",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "mean_years_of_schooling_index": 1,
        "expected_years_of_schooling_index": 1,
    },
)
def education_index():
    return (mean_years_of_schooling_index() + expected_years_of_schooling_index()) / 2


@component.add(
    name="Expected years in primary education",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_primary_education_duration": 1,
        "total_enrollment_rate_to_primary_education": 1,
        "population_cohorts": 1,
        "interval_duration": 1,
    },
)
def expected_years_in_primary_education():
    return (
        average_primary_education_duration()
        * (
            total_enrollment_rate_to_primary_education()
            / sum(
                population_cohorts()
                .loc[:, '"5-9"']
                .reset_coords(drop=True)
                .rename({"Gender": "Gender!"}),
                dim=["Gender!"],
            )
        )
        * interval_duration()
    )


@component.add(
    name="Expected years in secondary education",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_secondary_education_duration": 1,
        "interval_duration": 1,
        "total_enrollment_rate_to_secondary_education": 1,
        "population_cohorts": 2,
    },
)
def expected_years_in_secondary_education():
    return average_secondary_education_duration() * (
        total_enrollment_rate_to_secondary_education()
        * interval_duration()
        / (
            sum(
                population_cohorts()
                .loc[:, '"10-14"']
                .reset_coords(drop=True)
                .rename({"Gender": "Gender!"}),
                dim=["Gender!"],
            )
            + sum(
                population_cohorts()
                .loc[:, '"15-19"']
                .reset_coords(drop=True)
                .rename({"Gender": "Gender!"}),
                dim=["Gender!"],
            )
        )
    )


@component.add(
    name="Expected years in tertiary education",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_tertiary_education_duration": 1,
        "interval_duration": 1,
        "enrollment_rate_to_tertiary_education": 2,
        "population_cohorts": 2,
    },
)
def expected_years_in_tertiary_education():
    return (
        average_tertiary_education_duration()
        * interval_duration()
        * (
            (
                sum(
                    enrollment_rate_to_tertiary_education()
                    .loc[:, '"15-19"']
                    .reset_coords(drop=True)
                    .rename({"Gender": "Gender!"}),
                    dim=["Gender!"],
                )
                + sum(
                    enrollment_rate_to_tertiary_education()
                    .loc[:, '"20-24"']
                    .reset_coords(drop=True)
                    .rename({"Gender": "Gender!"}),
                    dim=["Gender!"],
                )
            )
            / (
                sum(
                    population_cohorts()
                    .loc[:, '"15-19"']
                    .reset_coords(drop=True)
                    .rename({"Gender": "Gender!"}),
                    dim=["Gender!"],
                )
                + sum(
                    population_cohorts()
                    .loc[:, '"20-24"']
                    .reset_coords(drop=True)
                    .rename({"Gender": "Gender!"}),
                    dim=["Gender!"],
                )
            )
        )
    )


@component.add(
    name="Expected Years of Schooling",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "expected_years_in_primary_education": 1,
        "expected_years_in_secondary_education": 1,
        "expected_years_in_tertiary_education": 1,
    },
)
def expected_years_of_schooling():
    """
    Expected years fo schooling at school entry age (5-9), calculated by the total population at all school enrolment ages divided by the enrollment rates. EYS is calculated for the ages 5-24 (Human Development Report 2021-2022 Technical Notes), but in the FeliX 25-29 can enroll to tertiary education. therefore removing it fro mthe calculation.
    """
    return (
        expected_years_in_primary_education()
        + expected_years_in_secondary_education()
        + expected_years_in_tertiary_education()
    )


@component.add(
    name="Expected Years of Schooling Index",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"expected_years_of_schooling": 1, "max_expected_years_of_schooling": 1},
)
def expected_years_of_schooling_index():
    """
    (Expected Years of Schooling-Min Expected Years of Schooling)/(Max Expected Years of Schooling-Min Expected Years of Schooling)
    """
    return expected_years_of_schooling() / max_expected_years_of_schooling()


@component.add(
    name="Forest Ecosystem Value",
    units="$/ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def forest_ecosystem_value():
    """
    Ecosystem value of unit area of forest.
    """
    return 700


@component.add(
    name="Health index",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "life_expectancy_at_birth": 1,
        "min_life_expectancy": 2,
        "max_life_expectancy": 1,
    },
)
def health_index():
    """
    Index of achievement in Life Expectancy. Source of historical data: http://hdr.undp.org/en/reports/global/hdr2011/
    """
    return (life_expectancy_at_birth() - min_life_expectancy()) / (
        max_life_expectancy() - min_life_expectancy()
    )


@component.add(
    name="Human Development Index",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"health_index": 1, "income_index": 1, "education_index": 1},
)
def human_development_index():
    """
    Human Development Index as an average of three indexes of achievement.
    """
    return (
        health_index() ** (1 / 3)
        * income_index() ** (1 / 3)
        * education_index() ** (1 / 3)
    )


@component.add(
    name="Income index",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gwp_per_capita": 1, "min_gwp_per_capita": 2, "max_gwp_per_capita": 1},
)
def income_index():
    """
    Index of achievement in GWP per Capita, formulation used in Human Development Report 2022/2022, https://hdr.undp.org/sites/default/files/2021-22_HDR/hdr2021-22_technical_n otes.pdf
    """
    return (float(np.log(gwp_per_capita())) - float(np.log(min_gwp_per_capita()))) / (
        float(np.log(max_gwp_per_capita())) - float(np.log(min_gwp_per_capita()))
    )


@component.add(
    name="Max Expected Years of Schooling",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_expected_years_of_schooling():
    """
    from the Human Development Report 2011/2022 https://hdr.undp.org/sites/default/files/2021-22_HDR/hdr2021-22_technical_n otes.pdf
    """
    return 18


@component.add(
    name="Max GWP per Capita",
    units="$/(Year*Person)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_gwp_per_capita():
    """
    Maximal reference Gross World Product per Capita in 2017 internationla $ PPP, from Human Development Report 2022/2022, https://hdr.undp.org/sites/default/files/2021-22_HDR/hdr2021-22_technical_n otes.pdf
    """
    return 75000


@component.add(
    name="Max Life Expectancy",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_life_expectancy():
    """
    Maximal reference Life Expectancy, from Human Development Report 2021-2022 https://hdr.undp.org/sites/default/files/2021-22_HDR/hdr2021-22_technical_n otes.pdf
    """
    return 85


@component.add(
    name="Max Mean Years of Schooling",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_mean_years_of_schooling():
    """
    from the Human Developmenr Report 2021/2022 https://hdr.undp.org/sites/default/files/2021-22_HDR/hdr2021-22_technical_n otes.pdf
    """
    return 15


@component.add(
    name="Mean Years of Schooling Index",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mean_years_of_schooling": 1, "max_mean_years_of_schooling": 1},
)
def mean_years_of_schooling_index():
    """
    (Average Duration in Education-Min Mean Years of Schooling)/(Max Mean Years of Schooling-Min Mean Years of Schooling), Min MYS=0
    """
    return mean_years_of_schooling() / max_mean_years_of_schooling()


@component.add(
    name="Min GWP per Capita",
    units="$/(Year*Person)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def min_gwp_per_capita():
    """
    Minimal reference Gross World Product per Capita in 2017 internationla $ PPP, from Human Development Report 2022/2022, https://hdr.undp.org/sites/default/files/2021-22_HDR/hdr2021-22_technical_n otes.pdf
    """
    return 100


@component.add(
    name="Min Life Expectancy",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def min_life_expectancy():
    """
    Minimal reference Life Expectancy, from Human Development Report 2021/2022 https://hdr.undp.org/sites/default/files/2021-22_HDR/hdr2021-22_technical_n otes.pdf
    """
    return 20


@component.add(
    name="Other Land Ecosystem Value",
    units="$/ha",
    comp_type="Constant",
    comp_subtype="Normal",
)
def other_land_ecosystem_value():
    """
    Ecosystem value of unit area of other land.
    """
    return 230


@component.add(
    name="Reference GWP per Capita for Income Index",
    units="$/(Year*Person)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_gwp_per_capita_for_income_index():
    """
    Auxilary variable to eliminate units and make the Income index dimensionless.
    """
    return 1


@component.add(
    name="Total Change in Cropland Ecosystem Value",
    units="$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agricultural_land": 1,
        "init_agricultural_land": 1,
        "cropland_ecosystem_value": 1,
    },
)
def total_change_in_cropland_ecosystem_value():
    """
    Total ecosystem value of cropland.
    """
    return (agricultural_land() - init_agricultural_land()) * cropland_ecosystem_value()


@component.add(
    name="Total Change in Forest Ecosystem Value",
    units="$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"forest_land": 1, "init_forest_land": 1, "forest_ecosystem_value": 1},
)
def total_change_in_forest_ecosystem_value():
    """
    Total ecosystem value of forest.
    """
    return (forest_land() - init_forest_land()) * forest_ecosystem_value()


@component.add(
    name="Total Change in Other Land Ecosystem Value",
    units="$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"other_land": 1, "init_other_land": 1, "other_land_ecosystem_value": 1},
)
def total_change_in_other_land_ecosystem_value():
    """
    Total ecosystem value of other land.
    """
    return (other_land() - init_other_land()) * other_land_ecosystem_value()


@component.add(
    name="Total Lost Value of Ecosystems",
    units="$",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_change_in_forest_ecosystem_value": 1,
        "total_change_in_cropland_ecosystem_value": 1,
        "total_change_in_other_land_ecosystem_value": 1,
    },
)
def total_lost_value_of_ecosystems():
    """
    Total ecosystem value of all considered areas - forest, cropland and other land like woodland and grassland.
    """
    return -(
        total_change_in_forest_ecosystem_value()
        + total_change_in_cropland_ecosystem_value()
        + total_change_in_other_land_ecosystem_value()
    )
