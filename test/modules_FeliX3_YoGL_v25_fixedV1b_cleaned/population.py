"""
Module population
Translated using PySD version 3.14.3
"""

@component.add(
    name="a fertility", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def a_fertility():
    """
    Calibrated according to Total Fertility and Population data 1.013 + STEP(SA a fertility-1.013, 2020)
    """
    return 2.26591


@component.add(
    name="Age Specific Fertility Rate",
    units="Dmnl",
    subscripts=["Fertile"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "l_age_fertility": 1,
        "ramp_for_fertility_variation": 1,
        "k_age_fertility": 1,
        "total_fertility": 1,
        "x0_age_fertility": 1,
    },
)
def age_specific_fertility_rate():
    """
    Age-specific fertility rate is formulated as a LOGISTIC function, derived from the Total Fertility - Age-Specific Fertility Rate relationship observed in the data from Wittgenstein Center for Population and Human Capital.
    """
    return (l_age_fertility() + ramp_for_fertility_variation()) / (
        1 + np.exp(-k_age_fertility() * (total_fertility() - x0_age_fertility()))
    )


@component.add(
    name="Age Specific Fertility Rate LOOKUP",
    units="Dmnl",
    subscripts=["Fertile"],
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"total_fertility": 7},
)
def age_specific_fertility_rate_lookup():
    """
    Age-specific fertility rate is formulated as a lookup function, derived from the Total Fertility - Age-Specific Fertility Rate relationship observed in the data from Wittgenstein Center for Population and Human Capital.
    """
    value = xr.DataArray(np.nan, {"Fertile": _subscript_dict["Fertile"]}, ["Fertile"])
    value.loc[['"15-19"']] = np.interp(
        total_fertility(),
        [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0],
        [
            0.00231122,
            0.00680381,
            0.0195977,
            0.0531867,
            0.125327,
            0.230181,
            0.320135,
            0.368499,
            0.388196,
            0.395292,
            0.397733,
            0.39856,
            0.398839,
            0.398932,
            0.398964,
        ],
    )
    value.loc[['"20-24"']] = np.interp(
        total_fertility(),
        [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0],
        [
            0.0266555,
            0.0594449,
            0.12812,
            0.258001,
            0.46215,
            0.705352,
            0.915218,
            1.05155,
            1.12455,
            1.15962,
            1.1756,
            1.1827,
            1.18583,
            1.18719,
            1.18779,
        ],
    )
    value.loc[['"25-29"']] = np.interp(
        total_fertility(),
        [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0],
        [
            0.210634,
            0.279671,
            0.365239,
            0.467472,
            0.584396,
            0.711621,
            0.842765,
            0.970622,
            1.08868,
            1.19234,
            1.27942,
            1.34989,
            1.40521,
            1.44762,
            1.47953,
        ],
    )
    value.loc[['"30-34"']] = np.interp(
        total_fertility(),
        [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0],
        [
            0.273372,
            0.312879,
            0.357669,
            0.408321,
            0.465437,
            0.529636,
            0.601533,
            0.681725,
            0.770763,
            0.869128,
            0.977194,
            1.09519,
            1.22319,
            1.36101,
            1.50829,
        ],
    )
    value.loc[['"35-39"']] = np.interp(
        total_fertility(),
        [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0],
        [
            0.113701,
            0.13669,
            0.164174,
            0.196963,
            0.235986,
            0.282292,
            0.337053,
            0.401546,
            0.477137,
            0.565236,
            0.667241,
            0.784453,
            0.917966,
            1.06854,
            1.23647,
        ],
    )
    value.loc[['"40-44"']] = np.interp(
        total_fertility(),
        [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0],
        [
            0.0203251,
            0.0275252,
            0.0371859,
            0.0500752,
            0.0671434,
            0.0895213,
            0.118481,
            0.155333,
            0.201238,
            0.25692,
            0.322328,
            0.396327,
            0.476563,
            0.559657,
            0.641715,
        ],
    )
    value.loc[['"45-49"']] = np.interp(
        total_fertility(),
        [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0],
        [
            0.00157971,
            0.00275537,
            0.00475806,
            0.00807914,
            0.0133486,
            0.0211505,
            0.0315942,
            0.043836,
            0.0561379,
            0.0667288,
            0.0746992,
            0.0801109,
            0.0835335,
            0.0856019,
            0.0868177,
        ],
    )
    return value


@component.add(
    name="Average duration of primary education",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_average_duration_of_primary_education": 1},
    other_deps={
        "_smooth_average_duration_of_primary_education": {
            "initial": {"time": 1, "lookup_primary_education_duration": 1},
            "step": {"time": 1, "lookup_primary_education_duration": 1},
        }
    },
)
def average_duration_of_primary_education():
    """
    In current International Standard Classification of Education (ISCED), this is considered 6 years, but assumed to have changed over time, starting from 2 years at the beginning of the century. Smoothed to avoid sharpe changes.
    """
    return _smooth_average_duration_of_primary_education()


_smooth_average_duration_of_primary_education = Smooth(
    lambda: lookup_primary_education_duration(time()),
    lambda: 1,
    lambda: lookup_primary_education_duration(time()),
    lambda: 1,
    "_smooth_average_duration_of_primary_education",
)


@component.add(
    name="Average duration of secondary education",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_average_duration_of_secondary_education": 1},
    other_deps={
        "_smooth_average_duration_of_secondary_education": {
            "initial": {"time": 1, "lookup_secondary_education_duration": 1},
            "step": {"time": 1, "lookup_secondary_education_duration": 1},
        }
    },
)
def average_duration_of_secondary_education():
    """
    In current International Standard Classification of Education (ISCED), this is considered 6 years, but assumed to have changed over time, starting from 2 years at the beginning of the century. Smoothed to avoid sharpe changes. More information is needed!!!
    """
    return _smooth_average_duration_of_secondary_education()


_smooth_average_duration_of_secondary_education = Smooth(
    lambda: lookup_secondary_education_duration(time()),
    lambda: 1,
    lambda: lookup_secondary_education_duration(time()),
    lambda: 1,
    "_smooth_average_duration_of_secondary_education",
)


@component.add(
    name="Average duration of tertiary education",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "lookup_tertiary_education_duration": 1},
)
def average_duration_of_tertiary_education():
    """
    In current International Standard Classification of Education (ISCED), this is considered 5 years, but assumed to have changed over time, starting from 2 years at the beginning of the century.
    """
    return lookup_tertiary_education_duration(time())


@component.add(
    name="Average Primary Education Duration",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def average_primary_education_duration():
    """
    https://data.worldbank.org/indicator/SE.PRM.DURS
    """
    return 6


@component.add(
    name="Average Primary Education Ratio",
    units="Dmnl",
    subscripts=["Gender", "PrimaryEdCohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"primary_education_graduates": 1, "population_cohorts": 1},
)
def average_primary_education_ratio():
    return primary_education_graduates().loc[
        :, _subscript_dict["PrimaryEdCohorts"]
    ].rename({"Cohorts": "PrimaryEdCohorts"}) / population_cohorts().loc[
        :, _subscript_dict["PrimaryEdCohorts"]
    ].rename(
        {"Cohorts": "PrimaryEdCohorts"}
    )


@component.add(
    name="Average Secondary Education Duration",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def average_secondary_education_duration():
    """
    https://data.worldbank.org/indicator/SE.SEC.DURS
    """
    return 5.5


@component.add(
    name="Average Secondary Education Level",
    units="Dmnl",
    subscripts=["Gender", "SecondaryEdCohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"secondary_education_graduates": 1, "population_cohorts": 1},
)
def average_secondary_education_level():
    return secondary_education_graduates().loc[
        :, _subscript_dict["SecondaryEdCohorts"]
    ].rename({"Cohorts": "SecondaryEdCohorts"}) / population_cohorts().loc[
        :, _subscript_dict["SecondaryEdCohorts"]
    ].rename(
        {"Cohorts": "SecondaryEdCohorts"}
    )


@component.add(
    name="Average Tertiary Education Duration",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def average_tertiary_education_duration():
    return 4


@component.add(
    name="Average Tertiary Education Level",
    units="Dmnl",
    subscripts=["Gender", "TertiaryEdCohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tertiary_education_graduates": 1, "population_cohorts": 1},
)
def average_tertiary_education_level():
    return tertiary_education_graduates().loc[
        :, _subscript_dict["TertiaryEdCohorts"]
    ].rename({"Cohorts": "TertiaryEdCohorts"}) / population_cohorts().loc[
        :, _subscript_dict["TertiaryEdCohorts"]
    ].rename(
        {"Cohorts": "TertiaryEdCohorts"}
    )


@component.add(
    name="b fertility", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def b_fertility():
    """
    Calibrated according to Total Fertility and Population data 0.0648 + STEP(SA b fertility-0.0648, 2020)
    """
    return 0.129381


@component.add(
    name="Birth Gender Fraction",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Stateful, Auxiliary",
    comp_subtype="Smooth, Normal",
    depends_on={
        "birth_gender_fraction_init": 1,
        "_smooth_birth_gender_fraction": 1,
        "birth_gender_fraction": 1,
    },
    other_deps={
        "_smooth_birth_gender_fraction": {
            "initial": {
                "birth_gender_fraction_variation": 1,
                "birth_gender_fraction_init": 1,
                "current_year": 1,
                "time": 1,
            },
            "step": {
                "birth_gender_fraction_variation": 1,
                "birth_gender_fraction_init": 1,
                "current_year": 1,
                "time": 1,
                "ssp_demographic_variation_time": 1,
            },
        }
    },
)
def birth_gender_fraction():
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["male"]] = (
        birth_gender_fraction_init() + _smooth_birth_gender_fraction()
    ).values
    value.loc[["female"]] = 1 - float(birth_gender_fraction().loc["male"])
    return value


_smooth_birth_gender_fraction = Smooth(
    lambda: xr.DataArray(
        step(
            __data["time"],
            birth_gender_fraction_variation() - birth_gender_fraction_init(),
            current_year(),
        ),
        {"Gender": ["male"]},
        ["Gender"],
    ),
    lambda: xr.DataArray(
        ssp_demographic_variation_time(), {"Gender": ["male"]}, ["Gender"]
    ),
    lambda: xr.DataArray(
        step(
            __data["time"],
            birth_gender_fraction_variation() - birth_gender_fraction_init(),
            current_year(),
        ),
        {"Gender": ["male"]},
        ["Gender"],
    ),
    lambda: 3,
    "_smooth_birth_gender_fraction",
)


@component.add(
    name="Birth Gender Fraction Init",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def birth_gender_fraction_init():
    return 0.515


@component.add(
    name="Birth Gender Fraction Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def birth_gender_fraction_variation():
    return 0.515


@component.add(
    name="Birth Rate",
    units="People/Year",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "birth_gender_fraction": 1,
        "age_specific_fertility_rate": 1,
        "population_cohorts": 1,
        "interval_duration": 1,
    },
)
def birth_rate():
    """
    Formulation with total fertility: Birth Gender Fraction[Gender]*Total Fertility*Fertile Population/Reproductive Lifetime
    """
    return (
        birth_gender_fraction()
        * sum(
            age_specific_fertility_rate().rename({"Fertile": "Fertile!"})
            * population_cohorts()
            .loc["female", _subscript_dict["Fertile"]]
            .reset_coords(drop=True)
            .rename({"Cohorts": "Fertile!"}),
            dim=["Fertile!"],
        )
        / interval_duration()
    )


@component.add(
    name="Change in Labor Force",
    units="Dmnl",
    subscripts=["Gender", "WorkingAge", "Labor force type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"labor_force": 1, "initial_labor_force": 1},
)
def change_in_labor_force():
    return labor_force() / initial_labor_force()


@component.add(
    name="Climate mortality inflection",
    units="DegreesC",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "climate_mortality_inflection_0": 1,
        "_smooth_climate_mortality_inflection": 1,
    },
    other_deps={
        "_smooth_climate_mortality_inflection": {
            "initial": {
                "climate_mortality_inflection_sa": 1,
                "climate_mortality_inflection_0": 1,
                "current_year": 1,
                "time": 1,
            },
            "step": {
                "climate_mortality_inflection_sa": 1,
                "climate_mortality_inflection_0": 1,
                "current_year": 1,
                "time": 1,
                "sa_effective_change_delay": 1,
            },
        }
    },
)
def climate_mortality_inflection():
    """
    The parameter that defines the inflection of the logistic function representing temperature-mortality relation. "..0" is the value that defines the original function calibrated to Bressler et al. 2021, "... SA" is the value that can be user-set to cover the uncertainty range after the current year.
    """
    return climate_mortality_inflection_0() + _smooth_climate_mortality_inflection()


_smooth_climate_mortality_inflection = Smooth(
    lambda: step(
        __data["time"],
        climate_mortality_inflection_sa() - climate_mortality_inflection_0(),
        current_year(),
    ),
    lambda: sa_effective_change_delay(),
    lambda: step(
        __data["time"],
        climate_mortality_inflection_sa() - climate_mortality_inflection_0(),
        current_year(),
    ),
    lambda: 3,
    "_smooth_climate_mortality_inflection",
)


@component.add(
    name="Climate mortality inflection 0",
    units="DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_mortality_inflection_0():
    return 7.75615


@component.add(
    name="Climate mortality inflection SA",
    units="DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_mortality_inflection_sa():
    return 7.75615


@component.add(
    name="Climate mortality saturation",
    units="percent",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "climate_mortality_saturation_0": 1,
        "_smooth_climate_mortality_saturation": 1,
    },
    other_deps={
        "_smooth_climate_mortality_saturation": {
            "initial": {
                "climate_mortality_saturation_sa": 1,
                "climate_mortality_saturation_0": 1,
                "current_year": 1,
                "time": 1,
            },
            "step": {
                "climate_mortality_saturation_sa": 1,
                "climate_mortality_saturation_0": 1,
                "current_year": 1,
                "time": 1,
                "sa_effective_change_delay": 1,
            },
        }
    },
)
def climate_mortality_saturation():
    """
    The parameter that defines the saturation level of the logistic function representing temperature-mortality relation. "..0" is the value that defines the original function calibrated to Bressler et al. 2021, "... SA" is the value that can be user-set to cover the uncertainty range after the current year.
    """
    return climate_mortality_saturation_0() + _smooth_climate_mortality_saturation()


_smooth_climate_mortality_saturation = Smooth(
    lambda: step(
        __data["time"],
        climate_mortality_saturation_sa() - climate_mortality_saturation_0(),
        current_year(),
    ),
    lambda: sa_effective_change_delay(),
    lambda: step(
        __data["time"],
        climate_mortality_saturation_sa() - climate_mortality_saturation_0(),
        current_year(),
    ),
    lambda: 3,
    "_smooth_climate_mortality_saturation",
)


@component.add(
    name="Climate mortality saturation 0",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_mortality_saturation_0():
    """
    The parameter that defines the saturation level of the logistic function representing temperature-mortality relation. Calibrated to Bressler et al. 2021.
    """
    return 0.684457


@component.add(
    name="Climate mortality saturation SA",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_mortality_saturation_sa():
    return 0.684457


@component.add(
    name="Climate mortality steepness",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "switch_impact_of_education_on_climate_mortality": 2,
        "climate_mortality_steepness_0": 1,
        "lookup_for_the_impact_of_mys_on_climate_mortality": 1,
        "lookup_for_the_impact_of_female_education_on_climate_mortality": 1,
        "share_of_females_aged_2039_with_sec_plus_education": 1,
        "mean_years_of_schooling": 1,
    },
)
def climate_mortality_steepness():
    """
    The parameter that defines the steepness of the logistic function representing temperature-mortality relation. It is assumed to depend on education, as education is a mediating factor for the climate impacts on mortality. Imapct of education can be driven by two alternative indicators, MYS or the female education.
    """
    return if_then_else(
        switch_impact_of_education_on_climate_mortality() == 0,
        lambda: climate_mortality_steepness_0(),
        lambda: if_then_else(
            switch_impact_of_education_on_climate_mortality() == 1,
            lambda: lookup_for_the_impact_of_mys_on_climate_mortality(
                mean_years_of_schooling()
            ),
            lambda: lookup_for_the_impact_of_female_education_on_climate_mortality(
                share_of_females_aged_2039_with_sec_plus_education()
            ),
        ),
    )


@component.add(
    name="Climate mortality steepness 0",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_mortality_steepness_0():
    """
    The parameter that defines the steepness of the logistic function representing temperature-mortality relation. Calibrated to Bressler et al. 2021.
    """
    return 0.257497


@component.add(
    name="Climate mortality steepness SA",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_mortality_steepness_sa():
    return 0.257497


@component.add(
    name="CLIMATE MORTALITY SWITCH",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def climate_mortality_switch():
    """
    0: Only temperature-dependent impact 1: Education mediated temperature impact - based on MYS 2: Education mediated temperature impact - based on female secondary 3: No impact
    """
    return 0


@component.add(
    name="Current year", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def current_year():
    return 2023


@component.add(
    name="Death Rate",
    units="People/Year",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_cohorts": 1, "mortality_fraction": 1},
)
def death_rate():
    return population_cohorts() * mortality_fraction()


@component.add(
    name="Death Rate of Primary Education Graduates",
    units="People/Year",
    subscripts=["Gender", "PrimaryEdCohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"primary_education_graduates": 1, "mortality_fraction": 1},
)
def death_rate_of_primary_education_graduates():
    """
    Death Rate[Gender,PrimaryEdCohorts]*Average Primary Education Ratio[Gender,PrimaryEdCohorts]
    """
    return primary_education_graduates().loc[
        :, _subscript_dict["PrimaryEdCohorts"]
    ].rename({"Cohorts": "PrimaryEdCohorts"}) * mortality_fraction().loc[
        :, _subscript_dict["PrimaryEdCohorts"]
    ].rename(
        {"Cohorts": "PrimaryEdCohorts"}
    )


@component.add(
    name="Death Rate of Secondary Education Graduates",
    units="People/Year",
    subscripts=["Gender", "SecondaryEdCohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"secondary_education_graduates": 1, "mortality_fraction": 1},
)
def death_rate_of_secondary_education_graduates():
    """
    Death Rate[Gender,SecondaryEdCohorts]*Average Secondary Education Level[Gender,SecondaryEdCohorts]
    """
    return secondary_education_graduates().loc[
        :, _subscript_dict["SecondaryEdCohorts"]
    ].rename({"Cohorts": "SecondaryEdCohorts"}) * mortality_fraction().loc[
        :, _subscript_dict["SecondaryEdCohorts"]
    ].rename(
        {"Cohorts": "SecondaryEdCohorts"}
    )


@component.add(
    name="Death Rate of Tertiary Education Graduates",
    units="People/Year",
    subscripts=["Gender", "TertiaryEdCohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tertiary_education_graduates": 1, "mortality_fraction": 1},
)
def death_rate_of_tertiary_education_graduates():
    """
    Death Rate[Gender,TertiaryEdCohorts]*Average Tertiary Education Level[Gender,TertiaryEdCohorts]
    """
    return tertiary_education_graduates().loc[
        :, _subscript_dict["TertiaryEdCohorts"]
    ].rename({"Cohorts": "TertiaryEdCohorts"}) * mortality_fraction().loc[
        :, _subscript_dict["TertiaryEdCohorts"]
    ].rename(
        {"Cohorts": "TertiaryEdCohorts"}
    )


@component.add(name="Delay Time PERPA", comp_type="Constant", comp_subtype="Normal")
def delay_time_perpa():
    return 1


@component.add(
    name="Effect of GWP per capita on primary enrollment",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"p1": 1, "gwp_per_capita_ratio_for_enrollment": 1, "p2": 1, "p0": 1},
)
def effect_of_gwp_per_capita_on_primary_enrollment():
    """
    Based on Net enrollment rate (noramlzied wrt max) vs. GWP per capita (normalized wrt 2000 value) data. Needs regression! IF THEN ELSE function is used to ensure the value of the primary education enrollment fraction <=1. The eventual value is constrained to be non-negative.
    """
    return np.maximum(
        p1() / (1 + np.exp(-p2() * (gwp_per_capita_ratio_for_enrollment() - p0()))), 0
    )


@component.add(
    name="Effect of GWP per capita on secondary enrollment",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"s1": 1, "gwp_per_capita_ratio_for_enrollment": 1, "s2": 1, "s0": 1},
)
def effect_of_gwp_per_capita_on_secondary_enrollment():
    """
    Based on gross enrollment rate (noramlzied wrt max) vs. GWP per capita (normalized wrt 2000 value) data. Needs regression! IF THEN ELSE function is used to ensure the value of the secondary education enrollment fraction is during [0,1].The eventual value is constrained to be non-negative.
    """
    return np.maximum(
        s1() / (1 + np.exp(-s2() * (gwp_per_capita_ratio_for_enrollment() - s0()))), 0
    )


@component.add(
    name="Effect of GWP per capita on tertiary enrollment",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"t1": 1, "gwp_per_capita_ratio_for_enrollment": 1, "t2": 1, "t0": 1},
)
def effect_of_gwp_per_capita_on_tertiary_enrollment():
    """
    Based on gross enrollment rate (noramlzied wrt max) vs. GWP per capita (normalized wrt 2000 value) data. Needs regression! IF THEN ELSE function is used to ensure the value of the tertiary education enrollment fraction is during [0,1] The eventual value is constrained to be non-negative.
    """
    return np.maximum(
        t1() / (1 + np.exp(-t2() * (gwp_per_capita_ratio_for_enrollment() - t0()))), 0
    )


@component.add(
    name="Enrollment rate to primary education",
    units="People/Year",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "primary_education_enrollment_fraction": 1,
        "primary_enrollment_rate_previous": 1,
        "population_cohorts": 1,
    },
)
def enrollment_rate_to_primary_education():
    """
    Primary education enrollment fraction[Gender]*Maturation Rate[Gender,"0-4"]
    """
    return primary_education_enrollment_fraction() * (
        population_cohorts().loc[:, '"5-9"'].reset_coords(drop=True)
        - primary_enrollment_rate_previous()
    )


@component.add(
    name="Enrollment Rate to Primary Education Accumulative",
    units="People",
    subscripts=["Gender"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_enrollment_rate_to_primary_education_accumulative": 1},
    other_deps={
        "_integ_enrollment_rate_to_primary_education_accumulative": {
            "initial": {"inflow_erpea": 1, "average_primary_education_duration": 1},
            "step": {"inflow_erpea": 1, "outflow_erpea": 1},
        }
    },
)
def enrollment_rate_to_primary_education_accumulative():
    """
    For coverting DELAY1 function only. Added by Q Ye in July 2024
    """
    return _integ_enrollment_rate_to_primary_education_accumulative()


_integ_enrollment_rate_to_primary_education_accumulative = Integ(
    lambda: inflow_erpea() - outflow_erpea(),
    lambda: inflow_erpea() * average_primary_education_duration(),
    "_integ_enrollment_rate_to_primary_education_accumulative",
)


@component.add(
    name="Enrollment Rate to Secondary Education",
    units="People/Year",
    subscripts=["Gender", "PrimaryEdCohorts"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={
        "primary_education_graduates": 2,
        "secondary_education_enrollment_fraction": 2,
    },
)
def enrollment_rate_to_secondary_education():
    """
    A fraction of total population rather than primary graduates at 10-14 and 15-19 enroll to secondary education.
    """
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "PrimaryEdCohorts": _subscript_dict["PrimaryEdCohorts"],
        },
        ["Gender", "PrimaryEdCohorts"],
    )
    value.loc[:, ['"10-14"']] = (
        (
            primary_education_graduates().loc[:, '"10-14"'].reset_coords(drop=True)
            * secondary_education_enrollment_fraction()
            .loc[:, '"10-14"']
            .reset_coords(drop=True)
        )
        .expand_dims({"SchoolEnrollment": ['"10-14"']}, 1)
        .values
    )
    value.loc[:, _subscript_dict["PrimaryEdButYoungest"]] = 0
    value.loc[:, ['"15-19"']] = (
        (
            primary_education_graduates().loc[:, '"15-19"'].reset_coords(drop=True)
            * secondary_education_enrollment_fraction()
            .loc[:, '"15-19"']
            .reset_coords(drop=True)
        )
        .expand_dims({"SchoolEnrollment": ['"15-19"']}, 1)
        .values
    )
    return value


@component.add(
    name="Enrollment Rate to Secondary Education Accumulative",
    units="People",
    subscripts=["Gender", "SchoolEnrollment"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_enrollment_rate_to_secondary_education_accumulative": 1,
        "_integ_enrollment_rate_to_secondary_education_accumulative_1": 1,
    },
    other_deps={
        "_integ_enrollment_rate_to_secondary_education_accumulative": {
            "initial": {"inflow_ersea": 1, "average_secondary_education_duration": 1},
            "step": {"inflow_ersea": 1, "outflow_ersea": 1},
        },
        "_integ_enrollment_rate_to_secondary_education_accumulative_1": {
            "initial": {"inflow_ersea": 1, "average_secondary_education_duration": 1},
            "step": {"inflow_ersea": 1, "outflow_ersea": 1},
        },
    },
)
def enrollment_rate_to_secondary_education_accumulative():
    """
    For coverting DELAY1 function only. Added by Q Ye in July 2024
    """
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "SchoolEnrollment": _subscript_dict["SchoolEnrollment"],
        },
        ["Gender", "SchoolEnrollment"],
    )
    value.loc[:, ['"10-14"']] = (
        _integ_enrollment_rate_to_secondary_education_accumulative().values
    )
    value.loc[:, ['"15-19"']] = (
        _integ_enrollment_rate_to_secondary_education_accumulative_1().values
    )
    return value


_integ_enrollment_rate_to_secondary_education_accumulative = Integ(
    lambda: (
        inflow_ersea().loc[:, '"10-14"'].reset_coords(drop=True)
        - outflow_ersea().loc[:, '"10-14"'].reset_coords(drop=True)
    ).expand_dims({"SchoolEnrollment": ['"10-14"']}, 1),
    lambda: (
        inflow_ersea().loc[:, '"10-14"'].reset_coords(drop=True)
        * average_secondary_education_duration()
    ).expand_dims({"SchoolEnrollment": ['"10-14"']}, 1),
    "_integ_enrollment_rate_to_secondary_education_accumulative",
)

_integ_enrollment_rate_to_secondary_education_accumulative_1 = Integ(
    lambda: (
        inflow_ersea().loc[:, '"15-19"'].reset_coords(drop=True)
        - outflow_ersea().loc[:, '"15-19"'].reset_coords(drop=True)
    ).expand_dims({"SchoolEnrollment": ['"15-19"']}, 1),
    lambda: (
        inflow_ersea().loc[:, '"15-19"'].reset_coords(drop=True)
        * average_secondary_education_duration()
    ).expand_dims({"SchoolEnrollment": ['"15-19"']}, 1),
    "_integ_enrollment_rate_to_secondary_education_accumulative_1",
)


@component.add(
    name="Enrollment Rate to Tertiary Education",
    units="People/Year",
    subscripts=["Gender", "MYS"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={
        "secondary_education_graduates": 3,
        "tertiary_education_enrollment_fraction": 3,
    },
)
def enrollment_rate_to_tertiary_education():
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "MYS": _subscript_dict["MYS"]},
        ["Gender", "MYS"],
    )
    value.loc[:, ['"15-19"']] = (
        (
            secondary_education_graduates().loc[:, '"15-19"'].reset_coords(drop=True)
            * tertiary_education_enrollment_fraction()
            .loc[:, '"15-19"']
            .reset_coords(drop=True)
        )
        .expand_dims({"SchoolEnrollment": ['"15-19"']}, 1)
        .values
    )
    value.loc[:, _subscript_dict["SecondaryEdButYoungest"]] = 0
    value.loc[:, ['"20-24"']] = (
        (
            tertiary_education_enrollment_fraction()
            .loc[:, '"20-24"']
            .reset_coords(drop=True)
            * secondary_education_graduates().loc[:, '"20-24"'].reset_coords(drop=True)
        )
        .expand_dims({"YoGL cohorts": ['"20-24"']}, 1)
        .values
    )
    value.loc[:, ['"25-29"']] = (
        (
            tertiary_education_enrollment_fraction()
            .loc[:, '"25-29"']
            .reset_coords(drop=True)
            * secondary_education_graduates().loc[:, '"25-29"'].reset_coords(drop=True)
        )
        .expand_dims({"YoGL cohorts": ['"25-29"']}, 1)
        .values
    )
    return value


@component.add(
    name="Enrollment Rate to Tertiary Education Accumulative",
    units="People",
    subscripts=["Gender", "SecondaryGraduation"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_enrollment_rate_to_tertiary_education_accumulative": 1},
    other_deps={
        "_integ_enrollment_rate_to_tertiary_education_accumulative": {
            "initial": {"inflow_ertea": 1, "average_tertiary_education_duration": 1},
            "step": {"inflow_ertea": 1, "outflow_ertea": 1},
        }
    },
)
def enrollment_rate_to_tertiary_education_accumulative():
    """
    For coverting DELAY1 function only. Added by Q Ye in July 2024
    """
    return _integ_enrollment_rate_to_tertiary_education_accumulative()


_integ_enrollment_rate_to_tertiary_education_accumulative = Integ(
    lambda: inflow_ertea() - outflow_ertea(),
    lambda: inflow_ertea() * average_tertiary_education_duration(),
    "_integ_enrollment_rate_to_tertiary_education_accumulative",
)


@component.add(
    name="Fertile Population",
    units="People",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_cohorts": 1},
)
def fertile_population():
    return sum(
        population_cohorts()
        .loc["female", _subscript_dict["Fertile"]]
        .reset_coords(drop=True)
        .rename({"Cohorts": "Fertile!"}),
        dim=["Fertile!"],
    )


@component.add(
    name="Food Ratio",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_daily_calorie_supply_per_capita": 1,
        "subsistence_food_per_capita": 1,
    },
)
def food_ratio():
    """
    Available food to subsistence food per capita ratio.
    """
    return total_daily_calorie_supply_per_capita() / subsistence_food_per_capita()


@component.add(
    name="Fractional1", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def fractional1():
    return 1


@component.add(
    name="Future fertility GDP",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def future_fertility_gdp():
    return 0


@component.add(
    name="Future fertility MYS",
    units="Dmnl",
    limits=(-1.0, 1.0, 0.05),
    comp_type="Constant",
    comp_subtype="Normal",
)
def future_fertility_mys():
    return 0


@component.add(
    name="GDP per Capita 2000",
    units="$/(Year*Person)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def gdp_per_capita_2000():
    return 6576


@component.add(
    name="Graduation Rate from Primary Education",
    units="People/Year",
    subscripts=["Gender", "SchoolEnrollment"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "outflow_erpea": 2,
        "interval_duration": 5,
        "average_primary_education_duration": 2,
        "maturation_rate": 2,
    },
)
def graduation_rate_from_primary_education():
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "SchoolEnrollment": _subscript_dict["SchoolEnrollment"],
        },
        ["Gender", "SchoolEnrollment"],
    )
    value.loc[:, ['"10-14"']] = (
        np.minimum(
            outflow_erpea()
            * (
                interval_duration()
                + interval_duration()
                - average_primary_education_duration()
            )
            / interval_duration(),
            maturation_rate().loc[:, '"10-14"'].reset_coords(drop=True),
        )
        .expand_dims({"SchoolEnrollment": ['"10-14"']}, 1)
        .values
    )
    value.loc[:, ['"15-19"']] = (
        np.minimum(
            outflow_erpea()
            * (average_primary_education_duration() - interval_duration())
            / interval_duration(),
            maturation_rate().loc[:, '"15-19"'].reset_coords(drop=True),
        )
        .expand_dims({"SchoolEnrollment": ['"15-19"']}, 1)
        .values
    )
    return value


@component.add(
    name="Graduation Rate from Secondary Education",
    units="People/Year",
    subscripts=["Gender", "SecondaryGraduation"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "outflow_ersea": 4,
        "interval_duration": 10,
        "average_secondary_education_duration": 4,
        "maturation_rate": 3,
    },
)
def graduation_rate_from_secondary_education():
    """
    Conidering that the average secondary education duration is 6 yrs, 4/5 of the students enrolled when aged 10-14 graduate when they are 15-19. 1/5 of thm graduate at the 20-24 interval. The same goes for the students enrolled when 15-19.
    """
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "SecondaryGraduation": _subscript_dict["SecondaryGraduation"],
        },
        ["Gender", "SecondaryGraduation"],
    )
    value.loc[:, ['"15-19"']] = (
        np.minimum(
            outflow_ersea().loc[:, '"10-14"'].reset_coords(drop=True)
            * (
                interval_duration()
                + interval_duration()
                - average_secondary_education_duration()
            )
            / interval_duration(),
            maturation_rate().loc[:, '"15-19"'].reset_coords(drop=True),
        )
        .expand_dims({"SchoolEnrollment": ['"15-19"']}, 1)
        .values
    )
    value.loc[:, ['"20-24"']] = (
        np.minimum(
            outflow_ersea().loc[:, '"10-14"'].reset_coords(drop=True)
            * (average_secondary_education_duration() - interval_duration())
            / interval_duration()
            + outflow_ersea().loc[:, '"15-19"'].reset_coords(drop=True)
            * (
                interval_duration()
                + interval_duration()
                - average_secondary_education_duration()
            )
            / interval_duration(),
            maturation_rate().loc[:, '"20-24"'].reset_coords(drop=True),
        )
        .expand_dims({"YoGL cohorts": ['"20-24"']}, 1)
        .values
    )
    value.loc[:, ['"25-29"']] = (
        np.minimum(
            outflow_ersea().loc[:, '"15-19"'].reset_coords(drop=True)
            * (average_secondary_education_duration() - interval_duration())
            / interval_duration(),
            maturation_rate().loc[:, '"25-29"'].reset_coords(drop=True),
        )
        .expand_dims({"YoGL cohorts": ['"25-29"']}, 1)
        .values
    )
    return value


@component.add(
    name="Graduation Rate from Tertiary Education",
    units="People/Year",
    subscripts=["Gender", "TertiaryGraduation"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_ertea": 3, "persistence_tertiary": 3, "maturation_rate": 3},
)
def graduation_rate_from_tertiary_education():
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "TertiaryGraduation": _subscript_dict["TertiaryGraduation"],
        },
        ["Gender", "TertiaryGraduation"],
    )
    value.loc[:, ['"20-24"']] = (
        np.minimum(
            outflow_ertea().loc[:, '"15-19"'].reset_coords(drop=True)
            * persistence_tertiary(),
            maturation_rate().loc[:, '"20-24"'].reset_coords(drop=True),
        )
        .expand_dims({"YoGL cohorts": ['"20-24"']}, 1)
        .values
    )
    value.loc[:, ['"25-29"']] = (
        np.minimum(
            outflow_ertea().loc[:, '"20-24"'].reset_coords(drop=True)
            * persistence_tertiary(),
            maturation_rate().loc[:, '"25-29"'].reset_coords(drop=True),
        )
        .expand_dims({"YoGL cohorts": ['"25-29"']}, 1)
        .values
    )
    value.loc[:, ['"30-34"']] = (
        np.minimum(
            outflow_ertea().loc[:, '"25-29"'].reset_coords(drop=True)
            * persistence_tertiary(),
            maturation_rate().loc[:, '"30-34"'].reset_coords(drop=True),
        )
        .expand_dims({"YoGL cohorts": ['"30-34"']}, 1)
        .values
    )
    return value


@component.add(
    name="Gross enrollment tertiary",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"enrollment_rate_to_tertiary_education": 1, "population_cohorts": 1},
)
def gross_enrollment_tertiary():
    return sum(
        enrollment_rate_to_tertiary_education()
        .loc[:, _subscript_dict["SecondaryGraduation"]]
        .rename({"MYS": "SecondaryGraduation!"}),
        dim=["SecondaryGraduation!"],
    ) / sum(
        population_cohorts()
        .loc[:, _subscript_dict["SecondaryGraduation"]]
        .rename({"Cohorts": "SecondaryGraduation!"}),
        dim=["SecondaryGraduation!"],
    )


@component.add(
    name="Gross enrolment primary historical",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 2},
)
def gross_enrolment_primary_historical():
    """
    Gross enrollment ratio is the ratio of total enrollment, regardless of age, to the population of the age group that officially corresponds to the level of education shown.
    """
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["female"]] = np.interp(
        time(),
        [
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
        ],
        [
            0.789667,
            0.791487,
            0.799756,
            0.822901,
            0.829701,
            0.858518,
            0.874188,
            0.876437,
            0.864985,
            0.870171,
            0.883556,
            0.892587,
            0.895741,
            0.894957,
            0.901066,
            0.907526,
            0.927891,
            0.923714,
            0.930934,
            0.933864,
            0.933188,
            0.931766,
            0.929245,
            0.931433,
            0.932693,
            0.934539,
            0.928554,
            0.926184,
            0.934147,
            0.938938,
            0.94733,
            0.957706,
            0.961468,
            0.987499,
            0.992846,
            0.99731,
            1.00048,
            1.00932,
            1.01666,
            1.01808,
            1.01776,
            1.02241,
            1.03118,
            1.03902,
            1.02666,
            1.02483,
            1.04383,
            1.03934,
            1.04135,
        ],
    )
    value.loc[["male"]] = np.interp(
        time(),
        [
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
        ],
        [
            0.888884,
            0.891472,
            0.90122,
            0.928758,
            0.939005,
            0.95208,
            0.95845,
            0.958429,
            0.946258,
            0.951834,
            0.964922,
            0.974303,
            0.978953,
            0.980087,
            0.983832,
            0.987683,
            1.00156,
            0.993557,
            0.999319,
            1.00118,
            0.997266,
            0.990826,
            0.984419,
            0.983493,
            0.982491,
            0.98321,
            0.975608,
            0.970018,
            0.976927,
            0.979367,
            0.987694,
            0.995646,
            0.998421,
            1.01385,
            1.01879,
            1.02193,
            1.02282,
            1.03056,
            1.03418,
            1.03301,
            1.03151,
            1.03487,
            1.04173,
            1.04019,
            1.02781,
            1.02512,
            1.0395,
            1.03654,
            1.03946,
        ],
    )
    return value


@component.add(
    name="Gross enrolment secondary historical",
    units="1/Year",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 2},
)
def gross_enrolment_secondary_historical():
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["female"]] = np.interp(
        time(),
        [
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
        ],
        [
            0.34457,
            0.368595,
            0.384467,
            0.39894,
            0.404453,
            0.412452,
            0.42842,
            0.439239,
            0.442274,
            0.452968,
            0.446433,
            0.437467,
            0.428865,
            0.430829,
            0.430789,
            0.418928,
            0.449067,
            0.458918,
            0.463141,
            0.465038,
            0.468862,
            0.480682,
            0.494722,
            0.509032,
            0.521684,
            0.533777,
            0.545408,
            0.551277,
            0.562265,
            0.566647,
            0.573569,
            0.578331,
            0.587613,
            0.601736,
            0.611679,
            0.623131,
            0.635747,
            0.654191,
            0.672312,
            0.684076,
            0.698406,
            0.711148,
            0.720403,
            0.738959,
            0.748815,
            0.749424,
            0.752362,
            0.748956,
            0.751078,
        ],
    )
    value.loc[["male"]] = np.interp(
        time(),
        [
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
        ],
        [
            0.454185,
            0.483164,
            0.504075,
            0.517345,
            0.51627,
            0.518016,
            0.534599,
            0.544126,
            0.538723,
            0.547448,
            0.541275,
            0.533601,
            0.525185,
            0.52172,
            0.527531,
            0.516484,
            0.542618,
            0.549203,
            0.552441,
            0.551409,
            0.554988,
            0.565614,
            0.578468,
            0.592727,
            0.599428,
            0.607112,
            0.616237,
            0.617314,
            0.620208,
            0.618089,
            0.623769,
            0.62736,
            0.635166,
            0.641059,
            0.650569,
            0.657811,
            0.668973,
            0.683907,
            0.698357,
            0.703291,
            0.721982,
            0.733254,
            0.740379,
            0.750608,
            0.757288,
            0.758608,
            0.760396,
            0.758266,
            0.759837,
        ],
    )
    return value


@component.add(
    name="Gross enrolment tertiary historical",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 2},
)
def gross_enrolment_tertiary_historical():
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["female"]] = np.interp(
        time(),
        [
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
        ],
        [
            0.082582,
            0.083288,
            0.0853796,
            0.0883727,
            0.0919498,
            0.0969259,
            0.101497,
            0.104095,
            0.107493,
            0.109522,
            0.111657,
            0.114511,
            0.116839,
            0.118544,
            0.121834,
            0.122753,
            0.121486,
            0.122613,
            0.122856,
            0.124838,
            0.12811,
            0.130651,
            0.134324,
            0.135856,
            0.144311,
            0.151232,
            0.153217,
            0.162019,
            0.170839,
            0.18284,
            0.190277,
            0.201123,
            0.219423,
            0.23163,
            0.241317,
            0.24943,
            0.260055,
            0.269373,
            0.280611,
            0.29195,
            0.306915,
            0.325764,
            0.342551,
            0.351806,
            0.377782,
            0.388985,
            0.396611,
            0.402733,
            0.40605,
        ],
    )
    value.loc[["male"]] = np.interp(
        time(),
        [
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
        ],
        [
            0.111699,
            0.114442,
            0.116193,
            0.11771,
            0.120519,
            0.12525,
            0.130942,
            0.130087,
            0.132478,
            0.133644,
            0.135137,
            0.138185,
            0.138976,
            0.141022,
            0.144521,
            0.144824,
            0.144298,
            0.145107,
            0.142477,
            0.143054,
            0.143916,
            0.145122,
            0.146149,
            0.1451,
            0.154218,
            0.159389,
            0.16044,
            0.167417,
            0.175415,
            0.184979,
            0.191291,
            0.201544,
            0.214189,
            0.225431,
            0.232511,
            0.237646,
            0.244118,
            0.251772,
            0.261057,
            0.271237,
            0.284959,
            0.30279,
            0.312664,
            0.317939,
            0.338862,
            0.34828,
            0.352668,
            0.355997,
            0.356392,
        ],
    )
    return value


@component.add(
    name="GWP per Capita 2000",
    units="$*Thousand/(Person*Year)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def gwp_per_capita_2000():
    return 5.50746 * 1000


@component.add(
    name="GWP per capita ratio for enrollment",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gwp_per_capita": 1, "gwp_per_capita_2000": 1},
)
def gwp_per_capita_ratio_for_enrollment():
    return gwp_per_capita() / gwp_per_capita_2000()


@component.add(
    name="Health Impact Delay",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def health_impact_delay():
    """
    Time delay to account for impact of health services on life expectancy.
    """
    return 1


@component.add(
    name="Impact of Biodiversity on Health",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "min_impact_of_biodiversity_on_health": 2,
        "init_species_abundance": 1,
        "mean_species_abundance": 1,
        "max_impact_of_biodiversity_on_health": 1,
    },
)
def impact_of_biodiversity_on_health():
    """
    Impact of changes in biodiversity on health. Scaled between minimum and maximum impact.
    """
    return min_impact_of_biodiversity_on_health() + (
        max_impact_of_biodiversity_on_health() - min_impact_of_biodiversity_on_health()
    ) * (mean_species_abundance() / init_species_abundance())


@component.add(
    name="Impact of climate change on mortality fraction",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "climate_mortality_switch": 3,
        "impact_of_climate_change_on_mortality_opt0": 1,
        "impact_of_climate_change_on_mortality_opt2": 1,
        "impact_of_climate_change_on_mortality_opt1": 1,
    },
)
def impact_of_climate_change_on_mortality_fraction():
    return if_then_else(
        climate_mortality_switch() == 0,
        lambda: impact_of_climate_change_on_mortality_opt0(),
        lambda: if_then_else(
            climate_mortality_switch() == 1,
            lambda: impact_of_climate_change_on_mortality_opt1(),
            lambda: if_then_else(
                climate_mortality_switch() == 2,
                lambda: impact_of_climate_change_on_mortality_opt2(),
                lambda: 0,
            ),
        ),
    )


@component.add(
    name="Impact of climate change on mortality opt0",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "y_climate_mortality": 1,
        "climate_mortality_inflection": 1,
        "temperature_change_from_preindustrial": 1,
        "nvs_100_percent": 1,
        "climate_mortality_steepness": 1,
        "climate_mortality_saturation": 1,
    },
)
def impact_of_climate_change_on_mortality_opt0():
    return -y_climate_mortality() + nvs_100_percent() * (
        climate_mortality_saturation()
        / (
            1
            + float(
                np.exp(
                    -climate_mortality_steepness()
                    * (
                        temperature_change_from_preindustrial()
                        - climate_mortality_inflection()
                    )
                )
            )
        )
    )


@component.add(
    name="Impact of climate change on mortality opt1",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "mean_years_of_schooling": 2,
        "opt1_mys_coeff": 1,
        "temperature_change_from_preindustrial": 2,
        "opt1_temperature_coeff": 2,
        "opt1_constant": 2,
    },
)
def impact_of_climate_change_on_mortality_opt1():
    return if_then_else(
        mean_years_of_schooling() > 8.5,
        lambda: opt1_temperature_coeff() * temperature_change_from_preindustrial()
        + opt1_mys_coeff() * mean_years_of_schooling()
        + opt1_constant(),
        lambda: opt1_temperature_coeff() * temperature_change_from_preindustrial()
        + opt1_constant(),
    )


@component.add(
    name="Impact of climate change on mortality opt2",
    units="percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "opt2_temperature_coeff": 1,
        "temperature_change_from_preindustrial": 1,
        "opt2_edu_coeff": 1,
        "share_of_females_aged_2039_with_sec_plus_education": 1,
        "opt2_constant": 1,
    },
)
def impact_of_climate_change_on_mortality_opt2():
    return (
        opt2_temperature_coeff() * temperature_change_from_preindustrial()
        + opt2_edu_coeff() * share_of_females_aged_2039_with_sec_plus_education()
        + opt2_constant()
    )


@component.add(
    name="Impact of Education on Fertility",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "l0_edu_fer": 1,
        "k_edu_fer": 1,
        "x0_edu_fer": 1,
        "mean_years_of_schooling": 1,
        "l_edu_fer": 1,
        "mys2000": 1,
    },
)
def impact_of_education_on_fertility():
    """
    Decreasong logistic function of which parameters are estimated from the global average MYS - Total Fertility relationship, also considering the impact of GDP.
    """
    return l0_edu_fer() + l_edu_fer() / (
        1
        + float(
            np.exp(
                -k_edu_fer() * (mean_years_of_schooling() / mys2000() - x0_edu_fer())
            )
        )
    )


@component.add(
    name="Impact of Education on Life Expectancy",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "l_le_mys": 1,
        "x0_le_mys": 1,
        "ratio_of_mys_to_the_reference": 1,
        "k_le_mys": 1,
    },
)
def impact_of_education_on_life_expectancy():
    """
    Impact of wealth on health services availability.
    """
    return l_le_mys() / (
        1 + float(np.exp(-k_le_mys() * (ratio_of_mys_to_the_reference() - x0_le_mys())))
    )


@component.add(
    name="Impact of Food on Life Expectancy",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"l_food_pop": 1, "k_food_pop": 1, "x0_food_pop": 1, "food_ratio": 1},
)
def impact_of_food_on_life_expectancy():
    """
    Impact of food availability on life expectancy.
    """
    return l_food_pop() / (
        1 + float(np.exp(-k_food_pop() * (food_ratio() - x0_food_pop())))
    )


@component.add(
    name="Impact of GDP on Fertility",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "l0_gdp_fer": 1,
        "k_gdp_fer": 1,
        "l_gdp_fer": 1,
        "x0_gdp_fer": 1,
        "gdp_per_capita_2000": 1,
        "gwp_per_capita": 1,
    },
)
def impact_of_gdp_on_fertility():
    """
    Decreasing logistic function of which parameters are estimated from the global average GDP per capita - Total Fertility relationship, also considering the impact of Mean Years of Schooling.
    """
    return l0_gdp_fer() + l_gdp_fer() / (
        1
        + float(
            np.exp(
                k_gdp_fer() * (gwp_per_capita() / gdp_per_capita_2000() - x0_gdp_fer())
            )
        )
    )


@component.add(
    name="Impact of GDP on Fertility Inflection",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def impact_of_gdp_on_fertility_inflection():
    """
    A parameter determining the inflection point of the nonlinear function representing the impact of population wealth on fertility.5.5
    """
    return 2.00035


@component.add(
    name="Impact of GDP on Fertility Steepness",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def impact_of_gdp_on_fertility_steepness():
    """
    A parameter determining the isteepness of the nonlinear function representing the impact of population wealth on fertility.
    """
    return 0.3


@component.add(
    name="Impact of GWP on Health",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "l_le_gdp": 1,
        "ratio_of_gdp_pc_to_the_reference": 1,
        "k_le_gdp": 1,
        "x0_le_gdp": 1,
    },
)
def impact_of_gwp_on_health():
    """
    Impact of wealth on health services availability.
    """
    return l_le_gdp() / (
        1
        + float(
            np.exp(-k_le_gdp() * (ratio_of_gdp_pc_to_the_reference() - x0_le_gdp()))
        )
    )


@component.add(
    name="Impact of Water Quality on Health",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"quality_of_domestic_water": 1},
)
def impact_of_water_quality_on_health():
    """
    Impact of changes in water quality on health.
    """
    return quality_of_domestic_water()


@component.add(
    name="Impact of Wealth on Health",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_impact_of_wealth_on_health": 1},
    other_deps={
        "_smooth_impact_of_wealth_on_health": {
            "initial": {"impact_of_gwp_on_health": 1},
            "step": {"impact_of_gwp_on_health": 1, "health_impact_delay": 1},
        }
    },
)
def impact_of_wealth_on_health():
    """
    Impact of health services availability on health taking into account delay.
    """
    return _smooth_impact_of_wealth_on_health()


_smooth_impact_of_wealth_on_health = Smooth(
    lambda: impact_of_gwp_on_health(),
    lambda: health_impact_delay(),
    lambda: impact_of_gwp_on_health(),
    lambda: 1,
    "_smooth_impact_of_wealth_on_health",
)


@component.add(
    name="Indicative Labor Force Participation Fraction",
    units="Dmnl",
    subscripts=["Gender", "WorkingAge"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={"time": 3},
)
def indicative_labor_force_participation_fraction():
    """
    LF S + RAMP((Labor Force Participation Fraction Variation-LF S)/78, 2022, 2100) Assumptions from the World Bank data. (Labor force participation rate data from WB.xlsx)
    """
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "WorkingAge": _subscript_dict["WorkingAge"],
        },
        ["Gender", "WorkingAge"],
    )
    value.loc[["male"], _subscript_dict['"15 to 24"']] = float(
        np.minimum(float(np.maximum(-0.6039 * (time() - 1989) + 66.308, 10)) / 100, 0.8)
    )
    value.loc[["male"], _subscript_dict['"25 to 54"']] = 0.929
    value.loc[["male"], _subscript_dict['"55 to 64"']] = 0.72
    value.loc[["female"], _subscript_dict['"15 to 24"']] = float(
        np.minimum(
            float(np.maximum(-0.5743 * (time() - 1989) + 49.044, 10)) / 100, 0.62
        )
    )
    value.loc[["female"], _subscript_dict['"55 to 64"']] = float(
        np.maximum(0.1, float(np.minimum(0.3743 * (time() - 1989) + 34.797, 62)) / 100)
    )
    value.loc[["female"], _subscript_dict['"25 to 54"']] = 0.629
    return value


@component.add(
    name="Inflow ERPEA",
    units="People/Year",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"enrollment_rate_to_primary_education": 1},
)
def inflow_erpea():
    return enrollment_rate_to_primary_education()


@component.add(
    name="Inflow ERSEA",
    units="People/Year",
    subscripts=["Gender", "SchoolEnrollment"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"enrollment_rate_to_secondary_education": 2},
)
def inflow_ersea():
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "SchoolEnrollment": _subscript_dict["SchoolEnrollment"],
        },
        ["Gender", "SchoolEnrollment"],
    )
    value.loc[:, ['"10-14"']] = (
        enrollment_rate_to_secondary_education()
        .loc[:, '"10-14"']
        .reset_coords(drop=True)
        .expand_dims({"SchoolEnrollment": ['"10-14"']}, 1)
        .values
    )
    value.loc[:, ['"15-19"']] = (
        enrollment_rate_to_secondary_education()
        .loc[:, '"15-19"']
        .reset_coords(drop=True)
        .expand_dims({"SchoolEnrollment": ['"15-19"']}, 1)
        .values
    )
    return value


@component.add(
    name="Inflow ERTEA",
    units="People/Year",
    subscripts=["Gender", "SecondaryGraduation"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"enrollment_rate_to_tertiary_education": 1},
)
def inflow_ertea():
    return (
        enrollment_rate_to_tertiary_education()
        .loc[:, _subscript_dict["SecondaryGraduation"]]
        .rename({"MYS": "SecondaryGraduation"})
    )


@component.add(
    name="Inflow PERPA",
    units="People/Year",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"enrollment_rate_to_primary_education": 1},
)
def inflow_perpa():
    return enrollment_rate_to_primary_education()


@component.add(name='"init 10-14"', comp_type="Constant", comp_subtype="Normal")
def init_1014():
    return 44000000.0


@component.add(
    name="Init PERPA", units="People", comp_type="Constant", comp_subtype="Normal"
)
def init_perpa():
    return 0


@component.add(
    name="Initial Labor Force",
    units="Person",
    subscripts=["Gender", "WorkingAge", "Labor force type"],
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_initial_labor_force": 1},
    other_deps={
        "_initial_initial_labor_force": {"initial": {"labor_force": 1}, "step": {}}
    },
)
def initial_labor_force():
    return _initial_initial_labor_force()


_initial_initial_labor_force = Initial(
    lambda: labor_force(), "_initial_initial_labor_force"
)


@component.add(
    name="Initial Population",
    units="People",
    subscripts=["Gender", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_population():
    """
    Population values in year 1900. Taken fro mthe previous version of the Felix.
    """
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )
    value.loc[["male"], :] = xr.DataArray(
        [
            [
                1.18790e08,
                1.03477e08,
                9.19065e07,
                8.16297e07,
                7.11071e07,
                6.05781e07,
                5.16081e07,
                4.28656e07,
                3.45952e07,
                2.70303e07,
                2.03671e07,
                1.47396e07,
                9.71780e06,
                5.14344e06,
                2.34004e06,
                9.01739e05,
                3.18566e05,
                8.62150e04,
                2.33330e04,
                5.30700e03,
                1.07900e03,
            ]
        ],
        {"Gender": ["male"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    ).values
    value.loc[["female"], :] = xr.DataArray(
        [
            [
                1.17500e08,
                1.02353e08,
                9.09085e07,
                8.07433e07,
                7.03349e07,
                5.99202e07,
                5.10477e07,
                4.24001e07,
                3.42195e07,
                2.67368e07,
                2.01459e07,
                1.45796e07,
                9.61227e06,
                5.08759e06,
                2.31463e06,
                8.91947e05,
                3.15106e05,
                8.52790e04,
                2.30800e04,
                5.24900e03,
                1.06800e03,
            ]
        ],
        {"Gender": ["female"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    ).values
    return value


@component.add(
    name="Initial Primary Education Graduates",
    units="People",
    subscripts=["Gender", "PrimaryEdCohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_primary_education_graduates():
    """
    Felix Model Initial Values
    """
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "PrimaryEdCohorts": _subscript_dict["PrimaryEdCohorts"],
        },
        ["Gender", "PrimaryEdCohorts"],
    )
    value.loc[["male"], :] = xr.DataArray(
        [
            [
                3.02875e07,
                2.69008e07,
                2.34331e07,
                1.99633e07,
                1.70073e07,
                1.41262e07,
                1.14007e07,
                8.90774e06,
                6.71190e06,
                4.85740e06,
                3.20247e06,
                1.69500e06,
                7.71153e05,
                2.97165e05,
                1.04982e05,
                2.84121e04,
                7.68984e03,
                1.74844e03,
                3.56265e02,
            ]
        ],
        {"Gender": ["male"], "PrimaryEdCohorts": _subscript_dict["PrimaryEdCohorts"]},
        ["Gender", "PrimaryEdCohorts"],
    ).values
    value.loc[["female"], :] = xr.DataArray(
        [
            [
                2.08719e07,
                1.85380e07,
                1.61483e07,
                1.37572e07,
                1.17201e07,
                9.73473e06,
                7.85653e06,
                6.13855e06,
                4.62534e06,
                3.34736e06,
                2.20690e06,
                1.16807e06,
                5.31421e05,
                2.04784e05,
                7.23464e04,
                1.95795e04,
                5.29875e03,
                1.20582e03,
                2.45275e02,
            ]
        ],
        {"Gender": ["female"], "PrimaryEdCohorts": _subscript_dict["PrimaryEdCohorts"]},
        ["Gender", "PrimaryEdCohorts"],
    ).values
    return value


@component.add(
    name="Initial Secondary Education Graduates",
    units="People",
    subscripts=["Gender", "SecondaryEdCohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_secondary_education_graduates():
    """
    Estimated wrt 37% of world population having min primary aducation in 1900
    """
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "SecondaryEdCohorts": _subscript_dict["SecondaryEdCohorts"],
        },
        ["Gender", "SecondaryEdCohorts"],
    )
    value.loc[["male"], :] = xr.DataArray(
        [
            [
                2.28430e07,
                1.98984e07,
                1.69520e07,
                1.44419e07,
                1.19954e07,
                9.68102e06,
                7.56408e06,
                5.69947e06,
                4.12470e06,
                2.71940e06,
                1.43933e06,
                6.54831e05,
                2.52341e05,
                8.91470e04,
                2.41260e04,
                6.52924e03,
                1.48535e03,
                3.01455e02,
            ]
        ],
        {
            "Gender": ["male"],
            "SecondaryEdCohorts": _subscript_dict["SecondaryEdCohorts"],
        },
        ["Gender", "SecondaryEdCohorts"],
    ).values
    value.loc[["female"], :] = xr.DataArray(
        [
            [
                1.96771e07,
                1.71406e07,
                1.46026e07,
                1.24403e07,
                1.03329e07,
                8.33930e06,
                6.51575e06,
                4.90956e06,
                3.55304e06,
                2.34251e06,
                1.23985e06,
                5.64077e05,
                2.17368e05,
                7.67915e04,
                2.07826e04,
                5.62487e03,
                1.27981e03,
                2.60347e02,
            ]
        ],
        {
            "Gender": ["female"],
            "SecondaryEdCohorts": _subscript_dict["SecondaryEdCohorts"],
        },
        ["Gender", "SecondaryEdCohorts"],
    ).values
    return value


@component.add(
    name="Initial Tertiary Education Graduates",
    units="People",
    subscripts=["Gender", "TertiaryEdCohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_tertiary_education_graduates():
    """
    Felix Model Initial Values
    """
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "TertiaryEdCohorts": _subscript_dict["TertiaryEdCohorts"],
        },
        ["Gender", "TertiaryEdCohorts"],
    )
    value.loc[["male"], :] = xr.DataArray(
        [
            [
                3.97968e06,
                3.39040e06,
                2.88838e06,
                2.39908e06,
                1.93620e06,
                1.51282e06,
                1.13989e06,
                8.24941e05,
                5.43881e05,
                2.87866e05,
                1.30966e05,
                5.04676e04,
                1.78297e04,
                4.82465e03,
                1.30585e03,
                2.97344e02,
                6.02910e01,
            ]
        ],
        {"Gender": ["male"], "TertiaryEdCohorts": _subscript_dict["TertiaryEdCohorts"]},
        ["Gender", "TertiaryEdCohorts"],
    ).values
    value.loc[["female"], :] = xr.DataArray(
        [
            [
                3.42812e06,
                2.92051e06,
                2.48807e06,
                2.06658e06,
                1.66786e06,
                1.30315e06,
                9.81912e05,
                7.10608e05,
                4.68502e05,
                2.47970e05,
                1.12815e05,
                4.34739e04,
                1.53578e04,
                4.15596e03,
                1.12497e03,
                2.56237e02,
                5.20695e01,
            ]
        ],
        {
            "Gender": ["female"],
            "TertiaryEdCohorts": _subscript_dict["TertiaryEdCohorts"],
        },
        ["Gender", "TertiaryEdCohorts"],
    ).values
    return value


@component.add(
    name="Interval duration", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def interval_duration():
    return 5


@component.add(
    name="k age fertility",
    units="Dmnl",
    subscripts=["Fertile"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def k_age_fertility():
    return xr.DataArray(
        [2.18219, 1.66138, 0.67154, 0.286501, 0.377578, 0.620179, 1.13987],
        {"Fertile": _subscript_dict["Fertile"]},
        ["Fertile"],
    )


@component.add(
    name="k edu fer", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def k_edu_fer():
    return -1.56


@component.add(
    name="k food pop",
    units="Dmnl",
    limits=(0.0, 1.0, 0.05),
    comp_type="Constant",
    comp_subtype="Normal",
)
def k_food_pop():
    return 0.2


@component.add(
    name="k gdp fer", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def k_gdp_fer():
    return 5


@component.add(
    name="k LE gdp",
    units="Dmnl",
    limits=(2.0, 3.0, 0.05),
    comp_type="Constant",
    comp_subtype="Normal",
)
def k_le_gdp():
    """
    Parameter determining intensity of impact of wealth on health services availability.
    """
    return 3


@component.add(
    name="k LE mys",
    units="Dmnl",
    limits=(0.2, 2.0, 0.05),
    comp_type="Constant",
    comp_subtype="Normal",
)
def k_le_mys():
    """
    Parameter determining intensity of impact of wealth on health services availability. 1.6716
    """
    return 0.44


@component.add(
    name="k mor",
    units="Dmnl",
    subscripts=["Gender", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def k_mor():
    """
    Original data please see the excel file 'InitialValues.xlsx','Mortality fractions parameters' , 'B4' and 'B10'
    """
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )
    value.loc[["male"], :] = xr.DataArray(
        [
            [
                -3.44922,
                -1.75539,
                -1.75366,
                -1.84241,
                -1.89654,
                -1.8639,
                -1.85398,
                -1.87063,
                -1.87805,
                -1.7974,
                -1.79172,
                -1.7048,
                -1.50713,
                -1.35385,
                -1.20004,
                -0.994761,
                -1.30636,
                -0.645272,
                -0.481138,
                -0.503644,
                -0.476095,
            ]
        ],
        {"Gender": ["male"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    ).values
    value.loc[["female"], :] = xr.DataArray(
        [
            [
                -3.45935,
                -1.55494,
                -1.57052,
                -1.62198,
                -1.68503,
                -1.70428,
                -1.7422,
                -1.80566,
                -1.87732,
                -1.85916,
                -1.89039,
                -1.87757,
                -1.83041,
                -1.83335,
                -1.82329,
                -1.82707,
                -1.84615,
                -0.833733,
                -0.652701,
                -0.565132,
                -0.250929,
            ]
        ],
        {"Gender": ["female"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    ).values
    return value


@component.add(
    name="L0 edu Fer",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"future_fertility_mys": 1, "time": 1},
)
def l0_edu_fer():
    return 0.8 + ramp(__data["time"], future_fertility_mys() / 78, 2022, 2100)


@component.add(
    name="L0 gdp Fer",
    units="Dmnl",
    limits=(-1.0, 1.0, 0.05),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"future_fertility_gdp": 1, "time": 1},
)
def l0_gdp_fer():
    return 0.8 + ramp(__data["time"], future_fertility_gdp() / 78, 2022, 2100)


@component.add(
    name="L age fertility",
    units="Dmnl",
    subscripts=["Fertile"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def l_age_fertility():
    return xr.DataArray(
        [0.39898, 1.18825, 1.56606, 5.07083, 5.07464, 1.07546, 0.0884531],
        {"Fertile": _subscript_dict["Fertile"]},
        ["Fertile"],
    )


@component.add(
    name="L edu fer", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def l_edu_fer():
    return 0.86261


@component.add(
    name="L Fertility Variation",
    units="Dmnl",
    subscripts=["Fertile"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def l_fertility_variation():
    return xr.DataArray(0, {"Fertile": _subscript_dict["Fertile"]}, ["Fertile"])


@component.add(
    name="L food pop",
    units="Dmnl",
    limits=(1.5, 3.0, 0.05),
    comp_type="Constant",
    comp_subtype="Normal",
)
def l_food_pop():
    return 2


@component.add(
    name="L gdp fer", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def l_gdp_fer():
    return 0.554


@component.add(
    name="L LE gdp",
    units="Dmnl",
    limits=(1.0, 2.0, 0.05),
    comp_type="Constant",
    comp_subtype="Normal",
)
def l_le_gdp():
    """
    1.15384
    """
    return 1.5


@component.add(
    name="L LE mys",
    units="Dmnl",
    limits=(1.0, 2.0, 0.05),
    comp_type="Constant",
    comp_subtype="Normal",
)
def l_le_mys():
    """
    1.44349
    """
    return 1.288


@component.add(
    name="L Mor",
    units="Dmnl",
    subscripts=["Gender", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def l_mor():
    """
    Original data please see the excel file 'InitialValues.xlsx','Mortality fractions parameters' , 'B3' and 'B9'
    """
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )
    value.loc[["male"], :] = xr.DataArray(
        [
            [
                6.03844e-02,
                4.61801e02,
                9.12577e02,
                1.35528e03,
                1.47798e03,
                1.54542e03,
                1.81552e03,
                1.52019e03,
                1.43606e03,
                2.36577e03,
                2.87879e03,
                3.95270e03,
                3.57025e03,
                2.01686e03,
                1.91046e03,
                9.26379e02,
                1.38198e04,
                3.27625e03,
                7.11867e03,
                1.32140e04,
                9.12106e03,
            ]
        ],
        {"Gender": ["male"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    ).values
    value.loc[["female"], :] = xr.DataArray(
        [
            [
                7.12513e-02,
                8.38039e02,
                7.35463e02,
                9.34156e02,
                8.38751e02,
                7.53234e02,
                9.15538e02,
                1.41484e03,
                1.23892e03,
                1.27042e03,
                2.16974e03,
                2.23017e03,
                2.11336e03,
                3.00327e03,
                4.50907e03,
                9.52346e03,
                2.10012e04,
                5.87382e03,
                1.24882e04,
                1.67264e04,
                3.04897e03,
            ]
        ],
        {"Gender": ["female"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    ).values
    return value


@component.add(
    name="Labor Force",
    units="Person",
    subscripts=["Gender", "WorkingAge", "Labor force type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fraction_of_skilled_secondary_education_graduates": 2,
        "secondary_education": 2,
        "tertiary_education": 1,
        "noneducated": 1,
        "primary_education": 1,
    },
)
def labor_force():
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "WorkingAge": _subscript_dict["WorkingAge"],
            "Labor force type": _subscript_dict["Labor force type"],
        },
        ["Gender", "WorkingAge", "Labor force type"],
    )
    value.loc[:, :, ["skill"]] = (
        (
            fraction_of_skilled_secondary_education_graduates() * secondary_education()
            + tertiary_education()
        )
        .expand_dims({"Labor force type": ["skill"]}, 2)
        .values
    )
    value.loc[:, :, ["unskill"]] = (
        (
            noneducated()
            + primary_education()
            + (1 - fraction_of_skilled_secondary_education_graduates())
            * secondary_education()
        )
        .expand_dims({"Labor force type": ["unskill"]}, 2)
        .values
    )
    return value


@component.add(
    name="Labor Force input",
    units="Dmnl",
    subscripts=["Gender", "WorkingAge", "Labor force type"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"change_in_labor_force": 1, "labor_force_participation_fraction": 1},
)
def labor_force_input():
    return change_in_labor_force() * labor_force_participation_fraction()


@component.add(
    name="Labor Force Participation Fraction",
    units="Dmnl",
    subscripts=["Gender", "WorkingAge"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "indicative_labor_force_participation_fraction": 1,
        "labor_force_ramp": 1,
    },
)
def labor_force_participation_fraction():
    """
    RAMP formulation is for policy implementation. The MIN formulation keeps the eventual fraction below 1
    """
    return np.minimum(
        indicative_labor_force_participation_fraction() * labor_force_ramp(), 1
    )


@component.add(
    name="Labor Force Participation Fraction Variation",
    units="Dmnl",
    subscripts=["Gender", "WorkingAge"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={"labor_force_participation_fraction_variation": 6},
)
def labor_force_participation_fraction_variation():
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "WorkingAge": _subscript_dict["WorkingAge"],
        },
        ["Gender", "WorkingAge"],
    )
    value.loc[:, _subscript_dict['"15 to 24"']] = 0
    value.loc[["male"], _subscript_dict['"25 to 54"']] = 0
    value.loc[["male"], _subscript_dict['"55 to 64"']] = 0
    value.loc[["female"], ['"55-59"']] = 0
    value.loc[["female"], ['"60-64"']] = float(
        labor_force_participation_fraction_variation().loc["female", '"55-59"']
    )
    value.loc[["female"], ['"25-29"']] = 0
    value.loc[["female"], ['"30-34"']] = float(
        labor_force_participation_fraction_variation().loc["female", '"25-29"']
    )
    value.loc[["female"], ['"35-39"']] = float(
        labor_force_participation_fraction_variation().loc["female", '"25-29"']
    )
    value.loc[["female"], ['"40-44"']] = float(
        labor_force_participation_fraction_variation().loc["female", '"25-29"']
    )
    value.loc[["female"], ['"45-49"']] = float(
        labor_force_participation_fraction_variation().loc["female", '"25-29"']
    )
    value.loc[["female"], ['"50-54"']] = float(
        labor_force_participation_fraction_variation().loc["female", '"25-29"']
    )
    return value


@component.add(
    name="Labor force RAMP",
    subscripts=["Gender", "WorkingAge"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fractional1": 1,
        "time": 1,
        "labor_force_participation_fraction_variation": 1,
        "current_year": 2,
        "demofelix_target_year": 2,
    },
)
def labor_force_ramp():
    return fractional1() + ramp(
        __data["time"],
        labor_force_participation_fraction_variation()
        / (demofelix_target_year() - current_year()),
        current_year(),
        demofelix_target_year(),
    )


@component.add(name="LF S", units="Dmnl", comp_type="Constant", comp_subtype="Normal")
def lf_s():
    return 0.75


@component.add(
    name="Life Expectancy 2000",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def life_expectancy_2000():
    return 65.68


@component.add(
    name="Life Expectancy at Birth",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_life_expectancy_at_birth": 1,
        "impact_of_wealth_on_health": 1,
        "impact_of_education_on_life_expectancy": 1,
        "lifetime_multiplier_from_food": 1,
        "lifetime_multiplier_from_climate_risk": 1,
    },
)
def life_expectancy_at_birth():
    """
    The global average life expectancy at birth. Source of historical data: Wittgenstein center
    """
    return (
        reference_life_expectancy_at_birth()
        * impact_of_wealth_on_health()
        * impact_of_education_on_life_expectancy()
        * lifetime_multiplier_from_food()
        * lifetime_multiplier_from_climate_risk()
    )


@component.add(
    name="Life Expectancy Normal",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def life_expectancy_normal():
    return 28.785


@component.add(
    name="Life Expectancy Normal Variation 1",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def life_expectancy_normal_variation_1():
    return 28


@component.add(
    name="Life Expectancy Variation",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def life_expectancy_variation():
    return 65.68


@component.add(
    name="Lifetime Multiplier from Climate Risk",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "_smooth_lifetime_multiplier_from_climate_risk": 1,
        "nvs_100_percent": 1,
    },
    other_deps={
        "_smooth_lifetime_multiplier_from_climate_risk": {
            "initial": {"impact_of_climate_change_on_mortality_fraction": 1},
            "step": {"impact_of_climate_change_on_mortality_fraction": 1},
        }
    },
)
def lifetime_multiplier_from_climate_risk():
    """
    Multiplier to account for changes in life expectancy at birth, depending on the impact of climate change on mortality fractions. Based on the equation that annual average mortality fraction = 1 / LE at birth.
    """
    return 1 / (1 + _smooth_lifetime_multiplier_from_climate_risk() / nvs_100_percent())


_smooth_lifetime_multiplier_from_climate_risk = Smooth(
    lambda: impact_of_climate_change_on_mortality_fraction(),
    lambda: 2,
    lambda: impact_of_climate_change_on_mortality_fraction(),
    lambda: 1,
    "_smooth_lifetime_multiplier_from_climate_risk",
)


@component.add(
    name="Lifetime Multiplier from Food",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"impact_of_food_on_life_expectancy": 1},
)
def lifetime_multiplier_from_food():
    """
    Multiplier to account for changes in life expectancy due to food availability.
    """
    return impact_of_food_on_life_expectancy()


@component.add(
    name="Lifetime Multiplier from Health Services",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "impact_of_wealth_on_health": 1,
        "impact_of_biodiversity_on_health": 1,
        "impact_of_water_quality_on_health": 1,
    },
)
def lifetime_multiplier_from_health_services():
    """
    Multiplier to account for changes in life expectancy due to health factors related to biodiversity, health services and water quality.
    """
    return (
        impact_of_wealth_on_health()
        * impact_of_biodiversity_on_health()
        * impact_of_water_quality_on_health()
    )


@component.add(
    name="Lookup for the Impact of Female Education on Climate Mortality",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_lookup_for_the_impact_of_female_education_on_climate_mortality"
    },
)
def lookup_for_the_impact_of_female_education_on_climate_mortality(x, final_subs=None):
    """
    Note that values for x<=0.7 are set to the value of stepeness in the case of no education impact
    """
    return (
        _hardcodedlookup_lookup_for_the_impact_of_female_education_on_climate_mortality(
            x, final_subs
        )
    )


_hardcodedlookup_lookup_for_the_impact_of_female_education_on_climate_mortality = HardcodedLookups(
    [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    [0.257497, 0.257497, 0.257497, 0.258934, 0.268012, 0.277423],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_lookup_for_the_impact_of_female_education_on_climate_mortality",
)


@component.add(
    name="Lookup for the Impact of MYS on Climate Mortality",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={
        "__lookup__": "_hardcodedlookup_lookup_for_the_impact_of_mys_on_climate_mortality"
    },
)
def lookup_for_the_impact_of_mys_on_climate_mortality(x, final_subs=None):
    """
    Note that the values for <10 rs of MYS are set to the value of steepness where education impact wasn ot taken into account.
    """
    return _hardcodedlookup_lookup_for_the_impact_of_mys_on_climate_mortality(
        x, final_subs
    )


_hardcodedlookup_lookup_for_the_impact_of_mys_on_climate_mortality = HardcodedLookups(
    [8.5, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0],
    [0.257497, 0.257497, 0.257497, 0.261932, 0.270401, 0.279158, 0.288224, 0.297621],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_lookup_for_the_impact_of_mys_on_climate_mortality",
)


@component.add(
    name="Lookup primary education duration",
    units="Year",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_lookup_primary_education_duration"},
)
def lookup_primary_education_duration(x, final_subs=None):
    """
    This is an estimate aligned with Mean Years of Schooling, and rough information such as a school year was less than 150 days in the US in 1905. More information is needed for the historucal educaion duration!!!
    """
    return _hardcodedlookup_lookup_primary_education_duration(x, final_subs)


_hardcodedlookup_lookup_primary_education_duration = HardcodedLookups(
    [1900.0, 1950.0, 2000.0, 2020.0],
    [2.0, 3.5, 5.0, 6.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_lookup_primary_education_duration",
)


@component.add(
    name="Lookup secondary education duration",
    units="Year",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_lookup_secondary_education_duration"},
)
def lookup_secondary_education_duration(x, final_subs=None):
    return _hardcodedlookup_lookup_secondary_education_duration(x, final_subs)


_hardcodedlookup_lookup_secondary_education_duration = HardcodedLookups(
    [1900.0, 1950.0, 2000.0, 2020.0],
    [2.0, 2.2, 4.0, 5.5],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_lookup_secondary_education_duration",
)


@component.add(
    name="Lookup tertiary education duration",
    units="Year",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_lookup_tertiary_education_duration"},
)
def lookup_tertiary_education_duration(x, final_subs=None):
    return _hardcodedlookup_lookup_tertiary_education_duration(x, final_subs)


_hardcodedlookup_lookup_tertiary_education_duration = HardcodedLookups(
    [1900.0, 1960.0, 2020.0],
    [2.0, 2.5, 4.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_lookup_tertiary_education_duration",
)


@component.add(
    name="M0",
    units="Dmnl",
    subscripts=["Gender", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def m0():
    """
    Original data please see 'InitialValues.xlsx','Mortality fractions parameters' , 'B2' and 'B8'
    """
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )
    value.loc[["male"], :] = xr.DataArray(
        [
            [
                4.71215e-04,
                -1.86121e-04,
                -7.68665e-05,
                1.32963e-04,
                3.36230e-04,
                3.06806e-04,
                3.45889e-04,
                4.52813e-04,
                5.86715e-04,
                5.60399e-04,
                8.92254e-04,
                1.00933e-03,
                -1.15189e-03,
                -4.77844e-03,
                -1.25876e-02,
                -3.25788e-02,
                -1.87939e-02,
                -1.68090e-01,
                -3.31592e-01,
                -2.11468e-01,
                -1.74159e-02,
            ]
        ],
        {"Gender": ["male"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    ).values
    value.loc[["female"], :] = xr.DataArray(
        [
            [
                -5.84927e-05,
                -7.32123e-04,
                -3.27784e-04,
                -3.33430e-04,
                -2.85692e-04,
                -1.82898e-04,
                -4.56964e-05,
                1.59498e-04,
                4.53778e-04,
                6.04678e-04,
                1.06245e-03,
                1.32983e-03,
                1.33262e-03,
                2.13453e-03,
                3.39337e-03,
                6.23944e-03,
                1.20705e-02,
                -6.68816e-02,
                -1.46500e-01,
                -1.74494e-01,
                -6.61378e-01,
            ]
        ],
        {"Gender": ["female"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    ).values
    return value


@component.add(
    name="Maturation of Primary Education Graduates",
    units="People/Year",
    subscripts=["Gender", "PrimaryEdCohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"primary_education_graduates": 1, "interval_duration": 1},
)
def maturation_of_primary_education_graduates():
    """
    Average Primary Education Ratio[Gender,PrimaryEdCohorts]*Maturation Rate[Gender ,PrimaryEdCohorts]
    """
    return if_then_else(
        (
            xr.DataArray(
                np.arange(3, len(_subscript_dict["PrimaryEdCohorts"]) + 3),
                {"PrimaryEdCohorts": _subscript_dict["PrimaryEdCohorts"]},
                ["PrimaryEdCohorts"],
            )
            == 21
        ).expand_dims({"Gender": _subscript_dict["Gender"]}, 1),
        lambda: xr.DataArray(
            0,
            {
                "PrimaryEdCohorts": _subscript_dict["PrimaryEdCohorts"],
                "Gender": _subscript_dict["Gender"],
            },
            ["PrimaryEdCohorts", "Gender"],
        ),
        lambda: (
            primary_education_graduates()
            .loc[:, _subscript_dict["PrimaryEdCohorts"]]
            .rename({"Cohorts": "PrimaryEdCohorts"})
            / interval_duration()
        ).transpose("PrimaryEdCohorts", "Gender"),
    ).transpose("Gender", "PrimaryEdCohorts")


@component.add(
    name="Maturation of Secondary Education Graduates",
    units="People/Year",
    subscripts=["Gender", "SecondaryEdCohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"secondary_education_graduates": 1, "interval_duration": 1},
)
def maturation_of_secondary_education_graduates():
    """
    Average Secondary Education Level[Gender,SecondaryEdCohorts]*Maturation Rate [Gender,SecondaryEdCohorts]
    """
    return if_then_else(
        (
            xr.DataArray(
                np.arange(4, len(_subscript_dict["SecondaryEdCohorts"]) + 4),
                {"SecondaryEdCohorts": _subscript_dict["SecondaryEdCohorts"]},
                ["SecondaryEdCohorts"],
            )
            == 21
        ).expand_dims({"Gender": _subscript_dict["Gender"]}, 1),
        lambda: xr.DataArray(
            0,
            {
                "SecondaryEdCohorts": _subscript_dict["SecondaryEdCohorts"],
                "Gender": _subscript_dict["Gender"],
            },
            ["SecondaryEdCohorts", "Gender"],
        ),
        lambda: (
            secondary_education_graduates()
            .loc[:, _subscript_dict["SecondaryEdCohorts"]]
            .rename({"Cohorts": "SecondaryEdCohorts"})
            / interval_duration()
        ).transpose("SecondaryEdCohorts", "Gender"),
    ).transpose("Gender", "SecondaryEdCohorts")


@component.add(
    name="Maturation of Tertiary Education Graduates",
    units="People/Year",
    subscripts=["Gender", "TertiaryEdCohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tertiary_education_graduates": 1, "interval_duration": 1},
)
def maturation_of_tertiary_education_graduates():
    """
    Average Tertiary Education Level[Gender,TertiaryEdCohorts]*Maturation Rate [Gender,TertiaryEdCohorts]
    """
    return if_then_else(
        (
            xr.DataArray(
                np.arange(5, len(_subscript_dict["TertiaryEdCohorts"]) + 5),
                {"TertiaryEdCohorts": _subscript_dict["TertiaryEdCohorts"]},
                ["TertiaryEdCohorts"],
            )
            == 21
        ).expand_dims({"Gender": _subscript_dict["Gender"]}, 1),
        lambda: xr.DataArray(
            0,
            {
                "TertiaryEdCohorts": _subscript_dict["TertiaryEdCohorts"],
                "Gender": _subscript_dict["Gender"],
            },
            ["TertiaryEdCohorts", "Gender"],
        ),
        lambda: (
            tertiary_education_graduates()
            .loc[:, _subscript_dict["TertiaryEdCohorts"]]
            .rename({"Cohorts": "TertiaryEdCohorts"})
            / interval_duration()
        ).transpose("TertiaryEdCohorts", "Gender"),
    ).transpose("Gender", "TertiaryEdCohorts")


@component.add(
    name="Maturation Rate",
    units="People/Year",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary, Constant",
    comp_subtype="Normal",
    depends_on={"population_cohorts": 1, "interval_duration": 1},
)
def maturation_rate():
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )
    value.loc[:, _subscript_dict["AllButOldest"]] = (
        population_cohorts()
        .loc[:, _subscript_dict["AllButOldest"]]
        .rename({"Cohorts": "AllButOldest"})
        / interval_duration()
    ).values
    value.loc[:, ['"100+"']] = 0
    return value


@component.add(
    name="Max Impact of Biodiversity on Health",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_max_impact_of_biodiversity_on_health": 1, "time": 1},
)
def max_impact_of_biodiversity_on_health():
    """
    Max impact of biodiversity on health and thus life expectancy.
    """
    return 1 + step(__data["time"], sa_max_impact_of_biodiversity_on_health() - 1, 2020)


@component.add(
    name="Mean Years of Schooling",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_duration_of_primary_education": 3,
        "primary_education_graduates": 1,
        "average_duration_of_secondary_education": 2,
        "secondary_education_graduates": 1,
        "average_duration_of_tertiary_education": 1,
        "tertiary_education_graduates": 1,
        "population_cohorts": 1,
    },
)
def mean_years_of_schooling():
    return (
        average_duration_of_primary_education()
        * sum(
            primary_education_graduates()
            .loc[:, _subscript_dict["MYS"]]
            .rename({"Gender": "Gender!", "Cohorts": "MYS!"}),
            dim=["Gender!", "MYS!"],
        )
        + (
            average_duration_of_secondary_education()
            + average_duration_of_primary_education()
        )
        * sum(
            secondary_education_graduates()
            .loc[:, _subscript_dict["MYS"]]
            .rename({"Gender": "Gender!", "Cohorts": "MYS!"}),
            dim=["Gender!", "MYS!"],
        )
        + (
            average_duration_of_tertiary_education()
            + average_duration_of_secondary_education()
            + average_duration_of_primary_education()
        )
        * sum(
            tertiary_education_graduates()
            .loc[:, _subscript_dict["MYS"]]
            .rename({"Gender": "Gender!", "Cohorts": "MYS!"}),
            dim=["Gender!", "MYS!"],
        )
    ) / sum(
        population_cohorts()
        .loc[:, _subscript_dict["MYS"]]
        .rename({"Gender": "Gender!", "Cohorts": "MYS!"}),
        dim=["Gender!", "MYS!"],
    )


@component.add(
    name="Mean Years of Schooling OLD",
    units="Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_duration_in_primary": 1,
        "total_duration_in_secondary": 1,
        "total_duration_in_tertiary": 1,
        "population_cohorts": 1,
    },
)
def mean_years_of_schooling_old():
    return (
        total_duration_in_primary()
        + total_duration_in_secondary()
        + total_duration_in_tertiary()
    ) / sum(
        population_cohorts()
        .loc[:, _subscript_dict["MYS"]]
        .rename({"Gender": "Gender!", "Cohorts": "MYS!"}),
        dim=["Gender!", "MYS!"],
    )


@component.add(
    name="Min Impact of Biodiversity on Health",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_min_impact_of_biodiversity_on_health": 1, "time": 1},
)
def min_impact_of_biodiversity_on_health():
    """
    Minimal impact of biodiversity on health and thus life expectancy.
    """
    return 0.95 + step(
        __data["time"], sa_min_impact_of_biodiversity_on_health() - 0.95, 2020
    )


@component.add(
    name="Mortality fraction",
    units="1/Year",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "m0": 1,
        "k_mor": 1,
        "ratio_of_life_expectancy_to_its_reference_value": 1,
        "x0_mor": 1,
        "l_mor": 1,
    },
)
def mortality_fraction():
    return m0() + l_mor() / (
        1
        + np.exp(
            -k_mor() * (ratio_of_life_expectancy_to_its_reference_value() - x0_mor())
        )
    )


@component.add(
    name="MYS2000", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def mys2000():
    return 7.38


@component.add(
    name="Net enrollment primary",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"enrollment_rate_to_primary_education": 1, "population_cohorts": 1},
)
def net_enrollment_primary():
    return enrollment_rate_to_primary_education() / population_cohorts().loc[
        :, '"5-9"'
    ].reset_coords(drop=True)


@component.add(
    name="Net enrollment secondary",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"enrollment_rate_to_secondary_education": 2, "population_cohorts": 2},
)
def net_enrollment_secondary():
    return (
        enrollment_rate_to_secondary_education()
        .loc[:, '"10-14"']
        .reset_coords(drop=True)
        + enrollment_rate_to_secondary_education()
        .loc[:, '"15-19"']
        .reset_coords(drop=True)
    ) / (
        population_cohorts().loc[:, '"10-14"'].reset_coords(drop=True)
        + population_cohorts().loc[:, '"15-19"'].reset_coords(drop=True)
    )


@component.add(
    name="Net enrolment primary historical",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 2},
)
def net_enrolment_primary_historical():
    """
    WB data indicators: Net enrollment rate is the ratio of children of official school age who are enrolled in school to the population of the corresponding official school age.
    """
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["female"]] = np.interp(
        time(),
        [
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
        ],
        [
            0.642132,
            0.638255,
            0.648587,
            0.678352,
            0.687001,
            0.702434,
            0.708253,
            0.70584,
            0.688695,
            0.690386,
            0.704107,
            0.715603,
            0.720626,
            0.724776,
            0.729434,
            0.740194,
            0.752776,
            0.757928,
            0.766022,
            0.775644,
            0.77249,
            0.777546,
            0.776501,
            0.779925,
            0.782502,
            0.779782,
            0.779119,
            0.781425,
            0.788885,
            0.798993,
            0.80683,
            0.810111,
            0.813975,
            0.835393,
            0.847214,
            0.854408,
            0.860111,
            0.871624,
            0.876232,
            0.878541,
            0.878841,
            0.88066,
            0.88194,
            0.882025,
            0.883301,
            0.881737,
            0.883363,
            0.881706,
            0.882163,
        ],
    )
    value.loc[["male"]] = np.interp(
        time(),
        [
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
        ],
        [
            0.78823,
            0.789945,
            0.796934,
            0.811367,
            0.816814,
            0.823521,
            0.830323,
            0.833386,
            0.829753,
            0.834347,
            0.84292,
            0.848162,
            0.851865,
            0.852753,
            0.853031,
            0.855005,
            0.858035,
            0.859186,
            0.864358,
            0.868385,
            0.864827,
            0.8658,
            0.862339,
            0.860039,
            0.857402,
            0.852783,
            0.847991,
            0.846462,
            0.850446,
            0.854332,
            0.859007,
            0.860553,
            0.861181,
            0.86629,
            0.875184,
            0.88054,
            0.883334,
            0.896384,
            0.896258,
            0.893531,
            0.893335,
            0.892029,
            0.89765,
            0.897401,
            0.900623,
            0.901001,
            0.904264,
            0.902825,
            0.905316,
        ],
    )
    return value


@component.add(
    name="Net intake rate in grade 1",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 2},
)
def net_intake_rate_in_grade_1():
    """
    Net intake rate in grade 1 is the number of new entrants in the first grade of primary education who are of official primary school entrance age, expressed as a percentage of the population of the corresponding age.
    """
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["male"]] = np.interp(
        time(),
        [
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
        ],
        [
            0.651358,
            0.659823,
            0.659946,
            0.658728,
            0.662043,
            0.671791,
            0.672977,
            0.677231,
            0.686237,
            0.697164,
            0.705859,
            0.702615,
            0.703141,
        ],
    )
    value.loc[["female"]] = np.interp(
        time(),
        [
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
        ],
        [
            0.641848,
            0.646937,
            0.656432,
            0.656568,
            0.654965,
            0.655178,
            0.66343,
            0.664672,
            0.669069,
            0.677505,
            0.68797,
            0.696344,
            0.694619,
            0.694762,
        ],
    )
    return value


@component.add(
    name="net to gross ter",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def net_to_gross_ter():
    return xr.DataArray([0.6, 0.6], {"Gender": _subscript_dict["Gender"]}, ["Gender"])


@component.add(
    name="NonEducated",
    units="Person",
    subscripts=["Gender", "WorkingAge"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_with_no_or_incomplete_education": 1},
)
def noneducated():
    return (
        population_with_no_or_incomplete_education()
        .loc[:, _subscript_dict["WorkingAge"]]
        .rename({"Cohorts": "WorkingAge"})
    )


@component.add(
    name="Normal Fertility",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"normal_fertility_init": 1, "_smooth_normal_fertility": 1},
    other_deps={
        "_smooth_normal_fertility": {
            "initial": {
                "normal_fertility_variation": 1,
                "normal_fertility_init": 1,
                "current_year": 1,
                "time": 1,
            },
            "step": {
                "normal_fertility_variation": 1,
                "normal_fertility_init": 1,
                "current_year": 1,
                "time": 1,
                "ssp_demographic_variation_time": 1,
            },
        }
    },
)
def normal_fertility():
    """
    The initial reference parameter is gradually adjusted to the "variation" value after the current year.
    """
    return normal_fertility_init() + _smooth_normal_fertility()


_smooth_normal_fertility = Smooth(
    lambda: step(
        __data["time"],
        normal_fertility_variation() - normal_fertility_init(),
        current_year(),
    ),
    lambda: ssp_demographic_variation_time(),
    lambda: step(
        __data["time"],
        normal_fertility_variation() - normal_fertility_init(),
        current_year(),
    ),
    lambda: 3,
    "_smooth_normal_fertility",
)


@component.add(
    name="Normal Fertility Init",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_fertility_init():
    """
    Reference fertility of reproductive fraction of population as estimated for year 2000.
    """
    return 2.63


@component.add(
    name="Normal Fertility Variation",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def normal_fertility_variation():
    """
    Fertility parameter to be adjusted for future scenario settings
    """
    return 2.63


@component.add(
    name="Opt1 constant", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def opt1_constant():
    return 4.95


@component.add(
    name="Opt1 MYS coeff",
    units="percent/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def opt1_mys_coeff():
    return -0.422


@component.add(
    name="Opt1 temperature coeff",
    units="percent/DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def opt1_temperature_coeff():
    return 2.513


@component.add(
    name="Opt2 constant", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def opt2_constant():
    return 4.167


@component.add(
    name="Opt2 edu coeff", units="percent", comp_type="Constant", comp_subtype="Normal"
)
def opt2_edu_coeff():
    return -4.56


@component.add(
    name="Opt2 temperature coeff",
    units="percent/DegreesC",
    comp_type="Constant",
    comp_subtype="Normal",
)
def opt2_temperature_coeff():
    return 2.494


@component.add(
    name="Outflow ERPEA",
    units="People/Year",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "enrollment_rate_to_primary_education_accumulative": 1,
        "average_primary_education_duration": 1,
    },
)
def outflow_erpea():
    return (
        enrollment_rate_to_primary_education_accumulative()
        / average_primary_education_duration()
    )


@component.add(
    name="Outflow ERSEA",
    units="People/Year",
    subscripts=["Gender", "SchoolEnrollment"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "enrollment_rate_to_secondary_education_accumulative": 2,
        "average_secondary_education_duration": 2,
    },
)
def outflow_ersea():
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "SchoolEnrollment": _subscript_dict["SchoolEnrollment"],
        },
        ["Gender", "SchoolEnrollment"],
    )
    value.loc[:, ['"10-14"']] = (
        (
            enrollment_rate_to_secondary_education_accumulative()
            .loc[:, '"10-14"']
            .reset_coords(drop=True)
            / average_secondary_education_duration()
        )
        .expand_dims({"SchoolEnrollment": ['"10-14"']}, 1)
        .values
    )
    value.loc[:, ['"15-19"']] = (
        (
            enrollment_rate_to_secondary_education_accumulative()
            .loc[:, '"15-19"']
            .reset_coords(drop=True)
            / average_secondary_education_duration()
        )
        .expand_dims({"SchoolEnrollment": ['"15-19"']}, 1)
        .values
    )
    return value


@component.add(
    name="Outflow ERTEA",
    units="People/Year",
    subscripts=["Gender", "SecondaryGraduation"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "enrollment_rate_to_tertiary_education_accumulative": 1,
        "average_tertiary_education_duration": 1,
    },
)
def outflow_ertea():
    return (
        enrollment_rate_to_tertiary_education_accumulative()
        / average_tertiary_education_duration()
    )


@component.add(
    name="Outflow PERPA",
    units="People/Year",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "primary_enrollment_rate_previous_accumulative": 1,
        "delay_time_perpa": 1,
    },
)
def outflow_perpa():
    return primary_enrollment_rate_previous_accumulative() / delay_time_perpa()


@component.add(
    name="P0",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"p0_sa": 2, "current_year": 2, "time": 2},
)
def p0():
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["male"]] = 1.2 + step(
        __data["time"], float(p0_sa().loc["male"]) - 1.2, current_year()
    )
    value.loc[["female"]] = 3 + step(
        __data["time"], float(p0_sa().loc["female"]) - 3, current_year()
    )
    return value


@component.add(
    name="P0 SA",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def p0_sa():
    return xr.DataArray([1.2, 3.0], {"Gender": _subscript_dict["Gender"]}, ["Gender"])


@component.add(
    name="P1",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"p1_sa": 2, "current_year": 2, "time": 2},
)
def p1():
    """
    v15 pre-recalibration 0.692643,0.711052
    """
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["male"]] = 0.87 + step(
        __data["time"], float(p1_sa().loc["male"]) - 0.87, current_year()
    )
    value.loc[["female"]] = 0.81047 + step(
        __data["time"], float(p1_sa().loc["female"]) - 0.81047, current_year()
    )
    return value


@component.add(
    name="P1 SA",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def p1_sa():
    return xr.DataArray(
        [0.87, 0.81047], {"Gender": _subscript_dict["Gender"]}, ["Gender"]
    )


@component.add(
    name="P2",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"p2_sa": 2, "current_year": 2, "time": 2},
)
def p2():
    """
    v15 pre-recalibration: 0.0665895,0.0262134
    """
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["male"]] = 0.03 + step(
        __data["time"], float(p2_sa().loc["male"]) - 0.03, current_year()
    )
    value.loc[["female"]] = 0.06 + step(
        __data["time"], float(p2_sa().loc["female"]) - 0.06, current_year()
    )
    return value


@component.add(
    name="P2 SA",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def p2_sa():
    return xr.DataArray([0.03, 0.06], {"Gender": _subscript_dict["Gender"]}, ["Gender"])


@component.add(
    name="People to Million People",
    units="Million",
    comp_type="Constant",
    comp_subtype="Normal",
)
def people_to_million_people():
    return 1 / 1000000.0


@component.add(
    name="Persistence",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 2},
)
def persistence():
    """
    WORLD BANK DATA INDICATORS: Persistence to last grade of primary is the percentage of children enrolled in the first grade of primary school who eventually reach the last grade of primary education. The estimate is based on the reconstructed cohort method.
    """
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["male"]] = np.interp(
        time(),
        [
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
        ],
        [
            0.672027,
            0.666965,
            0.664065,
            0.660664,
            0.663916,
            0.669295,
            0.677297,
            0.688329,
            0.686798,
            0.688356,
            0.684377,
            0.689278,
            0.689136,
            0.69319,
            0.692022,
            0.700484,
            0.711609,
            0.727936,
            0.730575,
            0.730886,
            0.742719,
            0.744286,
            0.748626,
            0.752946,
            0.754012,
            0.762202,
            0.761068,
            0.761713,
            0.763965,
            0.764819,
            0.757996,
            0.767335,
            0.758975,
            0.749462,
            0.746309,
            0.741466,
            0.747464,
            0.754092,
            0.772682,
            0.76853,
            0.765765,
            0.767346,
            0.753631,
            0.750484,
            0.797371,
            0.796902,
            0.798215,
            0.805835,
        ],
    )
    value.loc[["female"]] = np.interp(
        time(),
        [
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
        ],
        [
            0.679114,
            0.673352,
            0.670841,
            0.665051,
            0.667718,
            0.674349,
            0.685076,
            0.698729,
            0.695744,
            0.697124,
            0.692872,
            0.695902,
            0.700734,
            0.70389,
            0.702634,
            0.709909,
            0.719057,
            0.732887,
            0.733325,
            0.733855,
            0.746166,
            0.747999,
            0.752023,
            0.756935,
            0.759732,
            0.769925,
            0.770275,
            0.771772,
            0.775036,
            0.773736,
            0.771029,
            0.786615,
            0.771629,
            0.761558,
            0.758142,
            0.757387,
            0.76093,
            0.766676,
            0.784083,
            0.781961,
            0.778424,
            0.781395,
            0.767328,
            0.767567,
            0.818997,
            0.821234,
            0.814776,
            0.829103,
        ],
    )
    return value


@component.add(
    name="Persistence tertiary",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"persistence": 1, "_smooth_persistence_tertiary": 1},
    other_deps={
        "_smooth_persistence_tertiary": {
            "initial": {
                "persistence_tertiary_variation": 1,
                "persistence_tertiary_init": 1,
                "current_year": 1,
                "time": 1,
            },
            "step": {
                "persistence_tertiary_variation": 1,
                "persistence_tertiary_init": 1,
                "current_year": 1,
                "time": 1,
                "ssp_demographic_variation_time": 1,
            },
        }
    },
)
def persistence_tertiary():
    return persistence() + _smooth_persistence_tertiary()


_smooth_persistence_tertiary = Smooth(
    lambda: step(
        __data["time"],
        persistence_tertiary_variation() - persistence_tertiary_init(),
        current_year(),
    ),
    lambda: xr.DataArray(
        ssp_demographic_variation_time(),
        {"Gender": _subscript_dict["Gender"]},
        ["Gender"],
    ),
    lambda: step(
        __data["time"],
        persistence_tertiary_variation() - persistence_tertiary_init(),
        current_year(),
    ),
    lambda: 3,
    "_smooth_persistence_tertiary",
)


@component.add(
    name="Persistence Tertiary Init",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def persistence_tertiary_init():
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["female"]] = 0.829103
    value.loc[["male"]] = 0.805835
    return value


@component.add(
    name="Persistence Tertiary Variation",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def persistence_tertiary_variation():
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["female"]] = 0.829103
    value.loc[["male"]] = 0.805835
    return value


@component.add(
    name="Policy Ramp Primary Education",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fractional1": 1,
        "time": 1,
        "primary_education_variation": 1,
        "current_year": 2,
        "demofelix_target_year": 2,
    },
)
def policy_ramp_primary_education():
    return fractional1() + ramp(
        __data["time"],
        primary_education_variation() / (demofelix_target_year() - current_year()),
        current_year(),
        demofelix_target_year(),
    )


@component.add(
    name="Policy Ramp Sec Education",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "fractional1": 1,
        "time": 1,
        "secondary_education_variation": 1,
        "current_year": 2,
        "demofelix_target_year": 2,
    },
)
def policy_ramp_sec_education():
    return fractional1() + ramp(
        __data["time"],
        secondary_education_variation() / (demofelix_target_year() - current_year()),
        current_year(),
        demofelix_target_year(),
    )


@component.add(
    name="Population",
    units="People",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_by_gender": 1},
)
def population():
    return sum(population_by_gender().rename({"Gender": "Gender!"}), dim=["Gender!"])


@component.add(
    name='"Population 0-19"',
    units="People",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_cohorts": 1},
)
def population_019():
    return sum(
        population_cohorts()
        .loc[:, _subscript_dict['"0 to 19"']]
        .rename({"Gender": "Gender!", "Cohorts": '"0 to 19"!'}),
        dim=["Gender!", '"0 to 19"!'],
    )


@component.add(
    name='"Population 20-39"',
    units="People",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_cohorts": 1},
)
def population_2039():
    return sum(
        population_cohorts()
        .loc[:, _subscript_dict['"20 to 39"']]
        .rename({"Gender": "Gender!", "Cohorts": '"20 to 39"!'}),
        dim=["Gender!", '"20 to 39"!'],
    )


@component.add(
    name='"Population 40-64"',
    units="People",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_cohorts": 1},
)
def population_4064():
    return sum(
        population_cohorts()
        .loc[:, _subscript_dict['"40 to 64"']]
        .rename({"Gender": "Gender!", "Cohorts": '"40 to 64"!'}),
        dim=["Gender!", '"40 to 64"!'],
    )


@component.add(
    name="Population by Gender",
    units="People",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_cohorts": 1},
)
def population_by_gender():
    return sum(population_cohorts().rename({"Cohorts": "Cohorts!"}), dim=["Cohorts!"])


@component.add(
    name="Population Cohorts",
    units="People",
    subscripts=["Gender", "Cohorts"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_population_cohorts": 1, "_integ_population_cohorts_1": 1},
    other_deps={
        "_integ_population_cohorts": {
            "initial": {"initial_population": 1},
            "step": {"maturation_rate": 2, "death_rate": 1},
        },
        "_integ_population_cohorts_1": {
            "initial": {"initial_population": 1},
            "step": {"birth_rate": 1, "maturation_rate": 1, "death_rate": 1},
        },
    },
)
def population_cohorts():
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )
    value.loc[:, _subscript_dict["AllButYoungest"]] = _integ_population_cohorts().values
    value.loc[:, ['"0-4"']] = _integ_population_cohorts_1().values
    return value


_integ_population_cohorts = Integ(
    lambda: xr.DataArray(
        maturation_rate()
        .loc[:, _subscript_dict["PreviousCohort"]]
        .rename({"Cohorts": "PreviousCohort"})
        .values,
        {
            "Gender": _subscript_dict["Gender"],
            "AllButYoungest": _subscript_dict["AllButYoungest"],
        },
        ["Gender", "AllButYoungest"],
    )
    - maturation_rate()
    .loc[:, _subscript_dict["AllButYoungest"]]
    .rename({"Cohorts": "AllButYoungest"})
    - death_rate()
    .loc[:, _subscript_dict["AllButYoungest"]]
    .rename({"Cohorts": "AllButYoungest"}),
    lambda: initial_population()
    .loc[:, _subscript_dict["AllButYoungest"]]
    .rename({"Cohorts": "AllButYoungest"}),
    "_integ_population_cohorts",
)

_integ_population_cohorts_1 = Integ(
    lambda: (
        birth_rate()
        - maturation_rate().loc[:, '"0-4"'].reset_coords(drop=True)
        - death_rate().loc[:, '"0-4"'].reset_coords(drop=True)
    ).expand_dims({'"0 to 19"': ['"0-4"']}, 1),
    lambda: initial_population()
    .loc[:, '"0-4"']
    .reset_coords(drop=True)
    .expand_dims({'"0 to 19"': ['"0-4"']}, 1),
    "_integ_population_cohorts_1",
)


@component.add(
    name="Population Female",
    units="Person*Million",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_by_gender": 1, "people_to_million_people": 1},
)
def population_female():
    return float(population_by_gender().loc["female"]) * people_to_million_people()


@component.add(
    name="Population fraction with secondary and higher education",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_secondary_education_graduates": 1,
        "total_tertiary_education_graduates": 1,
        "population": 1,
    },
)
def population_fraction_with_secondary_and_higher_education():
    return (
        total_secondary_education_graduates() + total_tertiary_education_graduates()
    ) / population()


@component.add(
    name="Population fraction with secondary and higher education by gender",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "secondary_education_graduates_by_gender": 1,
        "tertiary_education_graduates_by_gender": 1,
        "population_by_gender": 1,
    },
)
def population_fraction_with_secondary_and_higher_education_by_gender():
    return (
        secondary_education_graduates_by_gender()
        + tertiary_education_graduates_by_gender()
    ) / population_by_gender()


@component.add(
    name="Population Growth Rate",
    units="Person/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_birth_rate": 1, "total_death_rate": 1},
)
def population_growth_rate():
    return total_birth_rate() - total_death_rate()


@component.add(
    name="Population Male",
    units="Person*Million",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_by_gender": 1, "people_to_million_people": 1},
)
def population_male():
    return float(population_by_gender().loc["male"]) * people_to_million_people()


@component.add(
    name="Population SSP1",
    units="People",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def population_ssp1():
    return np.interp(
        time(),
        [
            1970.0,
            1975.0,
            1980.0,
            1985.0,
            1990.0,
            1995.0,
            2000.0,
            2005.0,
            2010.0,
            2015.0,
            2020.0,
            2025.0,
            2030.0,
            2035.0,
            2040.0,
            2045.0,
            2050.0,
            2055.0,
            2060.0,
            2065.0,
            2070.0,
            2075.0,
            2080.0,
            2085.0,
            2090.0,
            2095.0,
            2100.0,
        ],
        [
            3.68074e09,
            4.05941e09,
            4.43414e09,
            4.79669e09,
            5.28493e09,
            5.70370e09,
            6.09965e09,
            6.48224e09,
            6.87086e09,
            7.22354e09,
            7.53499e09,
            7.80413e09,
            8.02440e09,
            8.21115e09,
            8.35685e09,
            8.45538e09,
            8.50423e09,
            8.50888e09,
            8.47265e09,
            8.39950e09,
            8.29207e09,
            8.15223e09,
            7.98198e09,
            7.78445e09,
            7.56537e09,
            7.33031e09,
            7.08389e09,
        ],
    )


@component.add(
    name="Population SSP2",
    units="People",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def population_ssp2():
    return np.interp(
        time(),
        [
            1970.0,
            1975.0,
            1980.0,
            1985.0,
            1990.0,
            1995.0,
            2000.0,
            2005.0,
            2010.0,
            2015.0,
            2020.0,
            2025.0,
            2030.0,
            2035.0,
            2040.0,
            2045.0,
            2050.0,
            2055.0,
            2060.0,
            2065.0,
            2070.0,
            2075.0,
            2080.0,
            2085.0,
            2090.0,
            2095.0,
            2100.0,
        ],
        [
            3.68074e09,
            4.05941e09,
            4.43414e09,
            4.79669e09,
            5.28493e09,
            5.70370e09,
            6.09965e09,
            6.48224e09,
            6.87086e09,
            7.24792e09,
            7.61173e09,
            7.94973e09,
            8.25612e09,
            8.53101e09,
            8.77220e09,
            8.97649e09,
            9.14040e09,
            9.26159e09,
            9.34085e09,
            9.38442e09,
            9.39716e09,
            9.38021e09,
            9.33460e09,
            9.26382e09,
            9.17313e09,
            9.06635e09,
            8.94823e09,
        ],
    )


@component.add(
    name="Population SSP3",
    units="People",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def population_ssp3():
    return np.interp(
        time(),
        [
            1970.0,
            1975.0,
            1980.0,
            1985.0,
            1990.0,
            1995.0,
            2000.0,
            2005.0,
            2010.0,
            2015.0,
            2020.0,
            2025.0,
            2030.0,
            2035.0,
            2040.0,
            2045.0,
            2050.0,
            2055.0,
            2060.0,
            2065.0,
            2070.0,
            2075.0,
            2080.0,
            2085.0,
            2090.0,
            2095.0,
            2100.0,
        ],
        [
            3.68074e09,
            4.05941e09,
            4.43414e09,
            4.79669e09,
            5.28493e09,
            5.70370e09,
            6.09965e09,
            6.48224e09,
            6.87086e09,
            7.27824e09,
            7.69384e09,
            8.10623e09,
            8.51113e09,
            8.89247e09,
            9.25997e09,
            9.61812e09,
            9.96610e09,
            1.02924e10,
            1.05964e10,
            1.08827e10,
            1.11599e10,
            1.14322e10,
            1.17018e10,
            1.19679e10,
            1.22331e10,
            1.24941e10,
            1.27517e10,
        ],
    )


@component.add(
    name="Population SSP4",
    units="People",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def population_ssp4():
    return np.interp(
        time(),
        [
            1970.0,
            1975.0,
            1980.0,
            1985.0,
            1990.0,
            1995.0,
            2000.0,
            2005.0,
            2010.0,
            2015.0,
            2020.0,
            2025.0,
            2030.0,
            2035.0,
            2040.0,
            2045.0,
            2050.0,
            2055.0,
            2060.0,
            2065.0,
            2070.0,
            2075.0,
            2080.0,
            2085.0,
            2090.0,
            2095.0,
            2100.0,
        ],
        [
            3.68074e09,
            4.05941e09,
            4.43414e09,
            4.79669e09,
            5.28493e09,
            5.70370e09,
            6.09965e09,
            6.48224e09,
            6.87086e09,
            7.24797e09,
            7.60818e09,
            7.94136e09,
            8.24256e09,
            8.51377e09,
            8.75486e09,
            8.96436e09,
            9.13967e09,
            9.27775e09,
            9.37804e09,
            9.44417e09,
            9.48298e09,
            9.49829e09,
            9.49356e09,
            9.47088e09,
            9.43664e09,
            9.39173e09,
            9.34039e09,
        ],
    )


@component.add(
    name="Population SSP5",
    units="People",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def population_ssp5():
    return np.interp(
        time(),
        [
            1970.0,
            1975.0,
            1980.0,
            1985.0,
            1990.0,
            1995.0,
            2000.0,
            2005.0,
            2010.0,
            2015.0,
            2020.0,
            2025.0,
            2030.0,
            2035.0,
            2040.0,
            2045.0,
            2050.0,
            2055.0,
            2060.0,
            2065.0,
            2070.0,
            2075.0,
            2080.0,
            2085.0,
            2090.0,
            2095.0,
            2100.0,
        ],
        [
            3.68074e09,
            4.05941e09,
            4.43414e09,
            4.79669e09,
            5.28493e09,
            5.70370e09,
            6.09965e09,
            6.48224e09,
            6.87086e09,
            7.22627e09,
            7.54328e09,
            7.82112e09,
            8.05357e09,
            8.25396e09,
            8.41534e09,
            8.53258e09,
            8.60428e09,
            8.63563e09,
            8.62990e09,
            8.59049e09,
            8.51970e09,
            8.41967e09,
            8.29287e09,
            8.14260e09,
            7.97431e09,
            7.79307e09,
            7.60303e09,
        ],
    )


@component.add(
    name="population sum of edu",
    units="People",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_wrt_education": 1},
)
def population_sum_of_edu():
    return sum(
        population_wrt_education().rename({"Education": "Education!"}),
        dim=["Education!"],
    )


@component.add(
    name="Population with No or Incomplete Education",
    units="People",
    subscripts=["Gender", "Cohorts"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "population_cohorts": 5,
        "primary_education_graduates": 3,
        "secondary_education_graduates": 2,
        "tertiary_education_graduates": 1,
    },
)
def population_with_no_or_incomplete_education():
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )
    value.loc[:, _subscript_dict["TertiaryEdCohorts"]] = np.maximum(
        0,
        population_cohorts()
        .loc[:, _subscript_dict["TertiaryEdCohorts"]]
        .rename({"Cohorts": "TertiaryEdCohorts"})
        - primary_education_graduates()
        .loc[:, _subscript_dict["TertiaryEdCohorts"]]
        .rename({"Cohorts": "TertiaryEdCohorts"})
        - secondary_education_graduates()
        .loc[:, _subscript_dict["TertiaryEdCohorts"]]
        .rename({"Cohorts": "TertiaryEdCohorts"})
        - tertiary_education_graduates()
        .loc[:, _subscript_dict["TertiaryEdCohorts"]]
        .rename({"Cohorts": "TertiaryEdCohorts"}),
    ).values
    value.loc[:, ['"15-19"']] = (
        np.maximum(
            0,
            population_cohorts().loc[:, '"15-19"'].reset_coords(drop=True)
            - primary_education_graduates().loc[:, '"15-19"'].reset_coords(drop=True)
            - secondary_education_graduates().loc[:, '"15-19"'].reset_coords(drop=True),
        )
        .expand_dims({"SchoolEnrollment": ['"15-19"']}, 1)
        .values
    )
    value.loc[:, ['"10-14"']] = (
        np.maximum(
            0,
            population_cohorts().loc[:, '"10-14"'].reset_coords(drop=True)
            - primary_education_graduates().loc[:, '"10-14"'].reset_coords(drop=True),
        )
        .expand_dims({"SchoolEnrollment": ['"10-14"']}, 1)
        .values
    )
    value.loc[:, ['"0-4"']] = (
        np.maximum(0, population_cohorts().loc[:, '"0-4"'].reset_coords(drop=True))
        .expand_dims({'"0 to 19"': ['"0-4"']}, 1)
        .values
    )
    value.loc[:, ['"5-9"']] = (
        population_cohorts()
        .loc[:, '"5-9"']
        .reset_coords(drop=True)
        .expand_dims({"SchoolEnrollment": ['"5-9"']}, 1)
        .values
    )
    return value


@component.add(
    name="Population with No or Incomplete Education Indicator",
    units="1",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_population_with_no_or_incomplete_education": 1, "population": 1},
)
def population_with_no_or_incomplete_education_indicator():
    return total_population_with_no_or_incomplete_education() / population()


@component.add(
    name="Population wrt Education",
    units="People",
    subscripts=["Gender", "Cohorts", "Education"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "population_with_no_or_incomplete_education": 1,
        "primary_education_graduates": 1,
        "secondary_education_graduates": 1,
        "tertiary_education_graduates": 1,
    },
)
def population_wrt_education():
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "Cohorts": _subscript_dict["Cohorts"],
            "Education": _subscript_dict["Education"],
        },
        ["Gender", "Cohorts", "Education"],
    )
    value.loc[:, :, ["noEd"]] = (
        population_with_no_or_incomplete_education()
        .expand_dims({"Education": ["noEd"]}, 2)
        .values
    )
    value.loc[:, :, ["primary"]] = (
        primary_education_graduates().expand_dims({"Education": ["primary"]}, 2).values
    )
    value.loc[:, :, ["secondary"]] = (
        secondary_education_graduates()
        .expand_dims({"Education": ["secondary"]}, 2)
        .values
    )
    value.loc[:, :, ["tertiary"]] = (
        tertiary_education_graduates()
        .expand_dims({"Education": ["tertiary"]}, 2)
        .values
    )
    return value


@component.add(
    name="Primary Education",
    units="Person",
    subscripts=["Gender", "WorkingAge"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"primary_education_graduates": 1},
)
def primary_education():
    return (
        primary_education_graduates()
        .loc[:, _subscript_dict["WorkingAge"]]
        .rename({"Cohorts": "WorkingAge"})
    )


@component.add(
    name="Primary education enrollment fraction",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_primary_education_enrollment_fraction": 1,
        "policy_ramp_primary_education": 1,
        "effect_of_gwp_per_capita_on_primary_enrollment": 1,
        "fractional1": 1,
    },
)
def primary_education_enrollment_fraction():
    return np.minimum(
        reference_primary_education_enrollment_fraction()
        * policy_ramp_primary_education()
        * effect_of_gwp_per_capita_on_primary_enrollment(),
        fractional1(),
    )


@component.add(
    name="Primary Education Graduates",
    units="People",
    subscripts=["Gender", "Cohorts"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_primary_education_graduates": 1,
        "_integ_primary_education_graduates_1": 1,
        "_integ_primary_education_graduates_2": 1,
        "_integ_primary_education_graduates_3": 1,
        "_integ_primary_education_graduates_4": 1,
    },
    other_deps={
        "_integ_primary_education_graduates": {
            "initial": {"initial_primary_education_graduates": 1},
            "step": {
                "graduation_rate_from_primary_education": 1,
                "death_rate_of_primary_education_graduates": 1,
                "maturation_of_primary_education_graduates": 1,
                "enrollment_rate_to_secondary_education": 1,
            },
        },
        "_integ_primary_education_graduates_1": {
            "initial": {"initial_primary_education_graduates": 1},
            "step": {
                "maturation_of_primary_education_graduates": 2,
                "death_rate_of_primary_education_graduates": 1,
            },
        },
        "_integ_primary_education_graduates_2": {"initial": {}, "step": {}},
        "_integ_primary_education_graduates_3": {"initial": {}, "step": {}},
        "_integ_primary_education_graduates_4": {
            "initial": {"initial_primary_education_graduates": 1},
            "step": {
                "graduation_rate_from_primary_education": 1,
                "death_rate_of_primary_education_graduates": 1,
                "maturation_of_primary_education_graduates": 1,
                "enrollment_rate_to_secondary_education": 1,
            },
        },
    },
)
def primary_education_graduates():
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )
    value.loc[:, ['"10-14"']] = _integ_primary_education_graduates().values
    value.loc[:, _subscript_dict["PrimaryEdButYoungest"]] = (
        _integ_primary_education_graduates_1().values
    )
    value.loc[:, ['"0-4"']] = _integ_primary_education_graduates_2().values
    value.loc[:, ['"5-9"']] = _integ_primary_education_graduates_3().values
    value.loc[:, ['"15-19"']] = _integ_primary_education_graduates_4().values
    return value


_integ_primary_education_graduates = Integ(
    lambda: (
        graduation_rate_from_primary_education()
        .loc[:, '"10-14"']
        .reset_coords(drop=True)
        - death_rate_of_primary_education_graduates()
        .loc[:, '"10-14"']
        .reset_coords(drop=True)
        - maturation_of_primary_education_graduates()
        .loc[:, '"10-14"']
        .reset_coords(drop=True)
        - enrollment_rate_to_secondary_education()
        .loc[:, '"10-14"']
        .reset_coords(drop=True)
    ).expand_dims({"SchoolEnrollment": ['"10-14"']}, 1),
    lambda: initial_primary_education_graduates()
    .loc[:, '"10-14"']
    .reset_coords(drop=True)
    .expand_dims({"SchoolEnrollment": ['"10-14"']}, 1),
    "_integ_primary_education_graduates",
)

_integ_primary_education_graduates_1 = Integ(
    lambda: xr.DataArray(
        maturation_of_primary_education_graduates()
        .loc[:, _subscript_dict["PrimaryEdPrevious"]]
        .rename({"PrimaryEdCohorts": "PrimaryEdPrevious"})
        .values,
        {
            "Gender": _subscript_dict["Gender"],
            "PrimaryEdButYoungest": _subscript_dict["PrimaryEdButYoungest"],
        },
        ["Gender", "PrimaryEdButYoungest"],
    )
    - death_rate_of_primary_education_graduates()
    .loc[:, _subscript_dict["PrimaryEdButYoungest"]]
    .rename({"PrimaryEdCohorts": "PrimaryEdButYoungest"})
    - maturation_of_primary_education_graduates()
    .loc[:, _subscript_dict["PrimaryEdButYoungest"]]
    .rename({"PrimaryEdCohorts": "PrimaryEdButYoungest"}),
    lambda: initial_primary_education_graduates()
    .loc[:, _subscript_dict["PrimaryEdButYoungest"]]
    .rename({"PrimaryEdCohorts": "PrimaryEdButYoungest"}),
    "_integ_primary_education_graduates_1",
)

_integ_primary_education_graduates_2 = Integ(
    lambda: xr.DataArray(
        0,
        {"Gender": _subscript_dict["Gender"], '"0 to 19"': ['"0-4"']},
        ["Gender", '"0 to 19"'],
    ),
    lambda: xr.DataArray(
        0,
        {"Gender": _subscript_dict["Gender"], '"0 to 19"': ['"0-4"']},
        ["Gender", '"0 to 19"'],
    ),
    "_integ_primary_education_graduates_2",
)

_integ_primary_education_graduates_3 = Integ(
    lambda: xr.DataArray(
        0,
        {"Gender": _subscript_dict["Gender"], "SchoolEnrollment": ['"5-9"']},
        ["Gender", "SchoolEnrollment"],
    ),
    lambda: xr.DataArray(
        0,
        {"Gender": _subscript_dict["Gender"], "SchoolEnrollment": ['"5-9"']},
        ["Gender", "SchoolEnrollment"],
    ),
    "_integ_primary_education_graduates_3",
)

_integ_primary_education_graduates_4 = Integ(
    lambda: (
        graduation_rate_from_primary_education()
        .loc[:, '"15-19"']
        .reset_coords(drop=True)
        - death_rate_of_primary_education_graduates()
        .loc[:, '"15-19"']
        .reset_coords(drop=True)
        - maturation_of_primary_education_graduates()
        .loc[:, '"15-19"']
        .reset_coords(drop=True)
        - enrollment_rate_to_secondary_education()
        .loc[:, '"15-19"']
        .reset_coords(drop=True)
    ).expand_dims({"SchoolEnrollment": ['"15-19"']}, 1),
    lambda: initial_primary_education_graduates()
    .loc[:, '"15-19"']
    .reset_coords(drop=True)
    .expand_dims({"SchoolEnrollment": ['"15-19"']}, 1),
    "_integ_primary_education_graduates_4",
)


@component.add(
    name="Primary Education Graduates by Gender",
    units="People",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"primary_education_graduates": 1},
)
def primary_education_graduates_by_gender():
    return sum(
        primary_education_graduates()
        .loc[:, _subscript_dict["PrimaryEdCohorts"]]
        .rename({"Cohorts": "PrimaryEdCohorts!"}),
        dim=["PrimaryEdCohorts!"],
    )


@component.add(
    name="Primary Education Variation",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def primary_education_variation():
    return xr.DataArray([0.0, 0.0], {"Gender": _subscript_dict["Gender"]}, ["Gender"])


@component.add(
    name="Primary enrollment rate previous",
    units="People/Year",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"outflow_perpa": 1},
)
def primary_enrollment_rate_previous():
    return outflow_perpa()


@component.add(
    name="Primary Enrollment Rate Previous Accumulative",
    units="People",
    subscripts=["Gender"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_primary_enrollment_rate_previous_accumulative": 1},
    other_deps={
        "_integ_primary_enrollment_rate_previous_accumulative": {
            "initial": {"delay_time_perpa": 1, "init_perpa": 1},
            "step": {"inflow_perpa": 1, "outflow_perpa": 1},
        }
    },
)
def primary_enrollment_rate_previous_accumulative():
    """
    For coverting DELAY1I function only. Added by Q Ye in July 2024
    """
    return _integ_primary_enrollment_rate_previous_accumulative()


_integ_primary_enrollment_rate_previous_accumulative = Integ(
    lambda: inflow_perpa() - outflow_perpa(),
    lambda: xr.DataArray(
        delay_time_perpa() * init_perpa(),
        {"Gender": _subscript_dict["Gender"]},
        ["Gender"],
    ),
    "_integ_primary_enrollment_rate_previous_accumulative",
)


@component.add(
    name="Ramp for fertility variation",
    units="Dmnl",
    subscripts=["Fertile"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"l_fertility_variation": 1, "time": 1},
)
def ramp_for_fertility_variation():
    return ramp(__data["time"], l_fertility_variation(), 2022, 2100)


@component.add(
    name="Ratio of GDP pc to the reference",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gwp_per_capita": 1, "gdp_per_capita_2000": 1},
)
def ratio_of_gdp_pc_to_the_reference():
    """
    Reference average world gross domestic product per capita. A reference value against which the GDP per Capita is compared to calculate the impact of wealth on health.
    """
    return gwp_per_capita() / gdp_per_capita_2000()


@component.add(
    name="Ratio of life expectancy to its reference value",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"life_expectancy_at_birth": 1, "life_expectancy_normal": 1},
)
def ratio_of_life_expectancy_to_its_reference_value():
    return life_expectancy_at_birth() / life_expectancy_normal()


@component.add(
    name="Ratio of MYS to the reference",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mean_years_of_schooling": 1, "mys2000": 1},
)
def ratio_of_mys_to_the_reference():
    """
    Reference average world gross domestic product per capita. A reference value against which the GDP per Capita is compared to calculate the impact of wealth on health.
    """
    return mean_years_of_schooling() / mys2000()


@component.add(
    name="Ratio of Secondary Education Graduates",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "secondary_education_graduates_by_gender": 1,
        "population_by_gender": 1,
    },
)
def ratio_of_secondary_education_graduates():
    return secondary_education_graduates_by_gender() / population_by_gender()


@component.add(
    name="Reference Life Expectancy at Birth",
    units="Year",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "life_expectancy_2000": 1,
        "_smooth_reference_life_expectancy_at_birth": 1,
    },
    other_deps={
        "_smooth_reference_life_expectancy_at_birth": {
            "initial": {
                "life_expectancy_variation": 1,
                "life_expectancy_2000": 1,
                "current_year": 1,
                "time": 1,
            },
            "step": {
                "life_expectancy_variation": 1,
                "life_expectancy_2000": 1,
                "current_year": 1,
                "time": 1,
                "ssp_demographic_variation_time": 1,
            },
        }
    },
)
def reference_life_expectancy_at_birth():
    return life_expectancy_2000() + _smooth_reference_life_expectancy_at_birth()


_smooth_reference_life_expectancy_at_birth = Smooth(
    lambda: step(
        __data["time"],
        life_expectancy_variation() - life_expectancy_2000(),
        current_year(),
    ),
    lambda: ssp_demographic_variation_time(),
    lambda: step(
        __data["time"],
        life_expectancy_variation() - life_expectancy_2000(),
        current_year(),
    ),
    lambda: 3,
    "_smooth_reference_life_expectancy_at_birth",
)


@component.add(
    name="Reference primary education enrollment fraction",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_primary_education_enrollment_fraction():
    """
    0.86,0.81
    """
    return xr.DataArray([1.0, 0.95], {"Gender": _subscript_dict["Gender"]}, ["Gender"])


@component.add(
    name="Reference secondary education enrollment fraction",
    units="Dmnl",
    subscripts=["Gender", "SchoolEnrollment"],
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "reference_secondary_education_enrollment_fraction_init": 2,
        "_smooth_reference_secondary_education_enrollment_fraction": 1,
        "_smooth_reference_secondary_education_enrollment_fraction_1": 1,
    },
    other_deps={
        "_smooth_reference_secondary_education_enrollment_fraction": {
            "initial": {
                "secondary_education_enrollment_variation": 1,
                "reference_secondary_education_enrollment_fraction_init": 1,
                "current_year": 1,
                "time": 1,
            },
            "step": {
                "secondary_education_enrollment_variation": 1,
                "reference_secondary_education_enrollment_fraction_init": 1,
                "current_year": 1,
                "time": 1,
                "ssp_demographic_variation_time": 1,
            },
        },
        "_smooth_reference_secondary_education_enrollment_fraction_1": {
            "initial": {
                "secondary_education_enrollment_variation": 1,
                "reference_secondary_education_enrollment_fraction_init": 1,
                "current_year": 1,
                "time": 1,
            },
            "step": {
                "secondary_education_enrollment_variation": 1,
                "reference_secondary_education_enrollment_fraction_init": 1,
                "current_year": 1,
                "time": 1,
                "ssp_demographic_variation_time": 1,
            },
        },
    },
)
def reference_secondary_education_enrollment_fraction():
    """
    Corresponding to 2000 values
    """
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "SchoolEnrollment": _subscript_dict["SchoolEnrollment"],
        },
        ["Gender", "SchoolEnrollment"],
    )
    value.loc[:, ['"10-14"']] = (
        reference_secondary_education_enrollment_fraction_init()
        .loc[:, '"10-14"']
        .reset_coords(drop=True)
        + _smooth_reference_secondary_education_enrollment_fraction()
    ).values
    value.loc[:, ['"15-19"']] = (
        reference_secondary_education_enrollment_fraction_init()
        .loc[:, '"15-19"']
        .reset_coords(drop=True)
        + _smooth_reference_secondary_education_enrollment_fraction_1()
    ).values
    return value


_smooth_reference_secondary_education_enrollment_fraction = Smooth(
    lambda: step(
        __data["time"],
        secondary_education_enrollment_variation()
        .loc[:, '"10-14"']
        .reset_coords(drop=True)
        - reference_secondary_education_enrollment_fraction_init()
        .loc[:, '"10-14"']
        .reset_coords(drop=True),
        current_year(),
    ).expand_dims({"SchoolEnrollment": ['"10-14"']}, 1),
    lambda: xr.DataArray(
        ssp_demographic_variation_time(),
        {"Gender": _subscript_dict["Gender"], "SchoolEnrollment": ['"10-14"']},
        ["Gender", "SchoolEnrollment"],
    ),
    lambda: step(
        __data["time"],
        secondary_education_enrollment_variation()
        .loc[:, '"10-14"']
        .reset_coords(drop=True)
        - reference_secondary_education_enrollment_fraction_init()
        .loc[:, '"10-14"']
        .reset_coords(drop=True),
        current_year(),
    ).expand_dims({"SchoolEnrollment": ['"10-14"']}, 1),
    lambda: 3,
    "_smooth_reference_secondary_education_enrollment_fraction",
)

_smooth_reference_secondary_education_enrollment_fraction_1 = Smooth(
    lambda: step(
        __data["time"],
        secondary_education_enrollment_variation()
        .loc[:, '"15-19"']
        .reset_coords(drop=True)
        - reference_secondary_education_enrollment_fraction_init()
        .loc[:, '"15-19"']
        .reset_coords(drop=True),
        current_year(),
    ).expand_dims({"SchoolEnrollment": ['"15-19"']}, 1),
    lambda: xr.DataArray(
        ssp_demographic_variation_time(),
        {"Gender": _subscript_dict["Gender"], "SchoolEnrollment": ['"15-19"']},
        ["Gender", "SchoolEnrollment"],
    ),
    lambda: step(
        __data["time"],
        secondary_education_enrollment_variation()
        .loc[:, '"15-19"']
        .reset_coords(drop=True)
        - reference_secondary_education_enrollment_fraction_init()
        .loc[:, '"15-19"']
        .reset_coords(drop=True),
        current_year(),
    ).expand_dims({"SchoolEnrollment": ['"15-19"']}, 1),
    lambda: 3,
    "_smooth_reference_secondary_education_enrollment_fraction_1",
)


@component.add(
    name="Reference secondary education enrollment fraction Init",
    units="Dmnl",
    subscripts=["Gender", "SchoolEnrollment"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_secondary_education_enrollment_fraction_init():
    """
    Corresponding to 2000 values
    """
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "SchoolEnrollment": _subscript_dict["SchoolEnrollment"],
        },
        ["Gender", "SchoolEnrollment"],
    )
    value.loc[:, ['"10-14"']] = xr.DataArray(
        [[1.0], [0.9]],
        {"Gender": _subscript_dict["Gender"], "SchoolEnrollment": ['"10-14"']},
        ["Gender", "SchoolEnrollment"],
    ).values
    value.loc[:, ['"15-19"']] = xr.DataArray(
        [[0.85], [0.85]],
        {"Gender": _subscript_dict["Gender"], "SchoolEnrollment": ['"15-19"']},
        ["Gender", "SchoolEnrollment"],
    ).values
    return value


@component.add(
    name="Reference tertiary education enrollment fraction",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={
        "reference_tertiary_education_enrollment_fraction_init": 1,
        "_smooth_reference_tertiary_education_enrollment_fraction": 1,
    },
    other_deps={
        "_smooth_reference_tertiary_education_enrollment_fraction": {
            "initial": {
                "tertiary_education_enrollment_variation": 1,
                "reference_tertiary_education_enrollment_fraction_init": 1,
                "current_year": 1,
                "time": 1,
            },
            "step": {
                "tertiary_education_enrollment_variation": 1,
                "reference_tertiary_education_enrollment_fraction_init": 1,
                "current_year": 1,
                "time": 1,
                "ssp_demographic_variation_time": 1,
            },
        }
    },
)
def reference_tertiary_education_enrollment_fraction():
    """
    Corresponding to 2000 values of the fraction of seondary education graduates aged 15-19 enrolling at tertiary education
    """
    return (
        reference_tertiary_education_enrollment_fraction_init()
        + _smooth_reference_tertiary_education_enrollment_fraction()
    )


_smooth_reference_tertiary_education_enrollment_fraction = Smooth(
    lambda: step(
        __data["time"],
        tertiary_education_enrollment_variation()
        - reference_tertiary_education_enrollment_fraction_init(),
        current_year(),
    ),
    lambda: xr.DataArray(
        ssp_demographic_variation_time(),
        {"Gender": _subscript_dict["Gender"]},
        ["Gender"],
    ),
    lambda: step(
        __data["time"],
        tertiary_education_enrollment_variation()
        - reference_tertiary_education_enrollment_fraction_init(),
        current_year(),
    ),
    lambda: 3,
    "_smooth_reference_tertiary_education_enrollment_fraction",
)


@component.add(
    name="Reference tertiary education enrollment fraction Init",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_tertiary_education_enrollment_fraction_init():
    """
    Corresponding to 2000 values of the fraction of seondary education graduates aged 15-19 enrolling at tertiary education
    """
    return xr.DataArray([0.39, 0.4], {"Gender": _subscript_dict["Gender"]}, ["Gender"])


@component.add(
    name="Reproductive Lifetime",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reproductive_lifetime():
    return 35


@component.add(
    name="S0",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"s0_sa": 2, "current_year": 2, "time": 2},
)
def s0():
    """
    v15 pre-recalibration: 2,2.49553
    """
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["male"]] = 1.9 + step(
        __data["time"], float(s0_sa().loc["male"]) - 1.9, current_year()
    )
    value.loc[["female"]] = 1.5 + step(
        __data["time"], float(s0_sa().loc["female"]) - 1.5, current_year()
    )
    return value


@component.add(
    name="S0 SA",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def s0_sa():
    return xr.DataArray([1.9, 1.5], {"Gender": _subscript_dict["Gender"]}, ["Gender"])


@component.add(
    name="S1",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"s1_sa": 2, "current_year": 2, "time": 2},
)
def s1():
    """
    The effect function is a logistic function that saturates at 1, meaning that enrollment fraction does not become higher than its reference value v15 pre-recalibration 1.04703,1.65163
    """
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["male"]] = 1.4 + step(
        __data["time"], float(s1_sa().loc["male"]) - 1.4, current_year()
    )
    value.loc[["female"]] = 1 + step(
        __data["time"], float(s1_sa().loc["female"]) - 1, current_year()
    )
    return value


@component.add(
    name="S1 SA",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def s1_sa():
    return xr.DataArray([1.4, 1.0], {"Gender": _subscript_dict["Gender"]}, ["Gender"])


@component.add(
    name="S2",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"s2_sa": 2, "current_year": 2, "time": 2},
)
def s2():
    """
    v15 pre-recalibration: 0.904801,1.16551
    """
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["male"]] = 1.15 + step(
        __data["time"], float(s2_sa().loc["male"]) - 1.15, current_year()
    )
    value.loc[["female"]] = 1.5 + step(
        __data["time"], float(s2_sa().loc["female"]) - 1.5, current_year()
    )
    return value


@component.add(
    name="S2 SA",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def s2_sa():
    return xr.DataArray([1.15, 1.5], {"Gender": _subscript_dict["Gender"]}, ["Gender"])


@component.add(
    name="SA effective change delay",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_effective_change_delay():
    return 30


@component.add(
    name="SA Max Impact of Biodiversity on Health",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_max_impact_of_biodiversity_on_health():
    return 1


@component.add(
    name="SA Min Impact of Biodiversity on Health",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_min_impact_of_biodiversity_on_health():
    return 0.95


@component.add(
    name="SA Subsistence Food per Capita",
    units="kcal/(Person*Day)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def sa_subsistence_food_per_capita():
    return 2000


@component.add(
    name="SE Var T", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def se_var_t():
    return 0


@component.add(
    name="Secondary Education",
    units="Person",
    subscripts=["Gender", "WorkingAge"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"secondary_education_graduates": 1},
)
def secondary_education():
    return (
        secondary_education_graduates()
        .loc[:, _subscript_dict["WorkingAge"]]
        .rename({"Cohorts": "WorkingAge"})
    )


@component.add(
    name="Secondary Education Enrollment Fraction",
    units="1/Year",
    subscripts=["Gender", "SchoolEnrollment"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_secondary_education_enrollment_fraction": 2,
        "policy_ramp_sec_education": 2,
        "effect_of_gwp_per_capita_on_secondary_enrollment": 2,
    },
)
def secondary_education_enrollment_fraction():
    """
    Fraction of Primary graduates enrolling to Secondary. The ramp function is for implementing scenarios as a fractional increase to 2100. Kept maximum at 1, to avoid enrolment >100%, and not to override the effect of GDP.
    """
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "SchoolEnrollment": _subscript_dict["SchoolEnrollment"],
        },
        ["Gender", "SchoolEnrollment"],
    )
    value.loc[:, ['"10-14"']] = (
        np.minimum(
            reference_secondary_education_enrollment_fraction()
            .loc[:, '"10-14"']
            .reset_coords(drop=True)
            * policy_ramp_sec_education()
            * effect_of_gwp_per_capita_on_secondary_enrollment(),
            1,
        )
        .expand_dims({"SchoolEnrollment": ['"10-14"']}, 1)
        .values
    )
    value.loc[:, ['"15-19"']] = (
        (
            (
                reference_secondary_education_enrollment_fraction()
                .loc[:, '"15-19"']
                .reset_coords(drop=True)
                * policy_ramp_sec_education()
            )
            * effect_of_gwp_per_capita_on_secondary_enrollment()
        )
        .expand_dims({"SchoolEnrollment": ['"15-19"']}, 1)
        .values
    )
    return value


@component.add(
    name="Secondary education enrollment Variation",
    units="Dmnl",
    subscripts=["Gender", "SchoolEnrollment"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def secondary_education_enrollment_variation():
    """
    Corresponding to 2000 values
    """
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "SchoolEnrollment": _subscript_dict["SchoolEnrollment"],
        },
        ["Gender", "SchoolEnrollment"],
    )
    value.loc[:, ['"10-14"']] = xr.DataArray(
        [[1.0], [0.9]],
        {"Gender": _subscript_dict["Gender"], "SchoolEnrollment": ['"10-14"']},
        ["Gender", "SchoolEnrollment"],
    ).values
    value.loc[:, ['"15-19"']] = xr.DataArray(
        [[0.85], [0.85]],
        {"Gender": _subscript_dict["Gender"], "SchoolEnrollment": ['"15-19"']},
        ["Gender", "SchoolEnrollment"],
    ).values
    return value


@component.add(
    name="Secondary Education Graduates",
    units="People",
    subscripts=["Gender", "Cohorts"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_secondary_education_graduates": 1,
        "_integ_secondary_education_graduates_1": 1,
        "_integ_secondary_education_graduates_2": 1,
        "_integ_secondary_education_graduates_3": 1,
        "_integ_secondary_education_graduates_4": 1,
        "_integ_secondary_education_graduates_5": 1,
        "_integ_secondary_education_graduates_6": 1,
    },
    other_deps={
        "_integ_secondary_education_graduates": {
            "initial": {"initial_secondary_education_graduates": 1},
            "step": {
                "graduation_rate_from_secondary_education": 1,
                "death_rate_of_secondary_education_graduates": 1,
                "maturation_of_secondary_education_graduates": 1,
                "enrollment_rate_to_tertiary_education": 1,
            },
        },
        "_integ_secondary_education_graduates_1": {
            "initial": {"initial_secondary_education_graduates": 1},
            "step": {
                "maturation_of_secondary_education_graduates": 2,
                "death_rate_of_secondary_education_graduates": 1,
            },
        },
        "_integ_secondary_education_graduates_2": {"initial": {}, "step": {}},
        "_integ_secondary_education_graduates_3": {"initial": {}, "step": {}},
        "_integ_secondary_education_graduates_4": {"initial": {}, "step": {}},
        "_integ_secondary_education_graduates_5": {
            "initial": {"initial_secondary_education_graduates": 1},
            "step": {
                "graduation_rate_from_secondary_education": 1,
                "death_rate_of_secondary_education_graduates": 1,
                "maturation_of_secondary_education_graduates": 2,
                "enrollment_rate_to_tertiary_education": 1,
            },
        },
        "_integ_secondary_education_graduates_6": {
            "initial": {"initial_secondary_education_graduates": 1},
            "step": {
                "graduation_rate_from_secondary_education": 1,
                "enrollment_rate_to_tertiary_education": 1,
                "death_rate_of_secondary_education_graduates": 1,
                "maturation_of_secondary_education_graduates": 2,
            },
        },
    },
)
def secondary_education_graduates():
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )
    value.loc[:, ['"15-19"']] = _integ_secondary_education_graduates().values
    value.loc[:, _subscript_dict["SecondaryEdButYoungest"]] = (
        _integ_secondary_education_graduates_1().values
    )
    value.loc[:, ['"0-4"']] = _integ_secondary_education_graduates_2().values
    value.loc[:, ['"5-9"']] = _integ_secondary_education_graduates_3().values
    value.loc[:, ['"10-14"']] = _integ_secondary_education_graduates_4().values
    value.loc[:, ['"20-24"']] = _integ_secondary_education_graduates_5().values
    value.loc[:, ['"25-29"']] = _integ_secondary_education_graduates_6().values
    return value


_integ_secondary_education_graduates = Integ(
    lambda: (
        graduation_rate_from_secondary_education()
        .loc[:, '"15-19"']
        .reset_coords(drop=True)
        - death_rate_of_secondary_education_graduates()
        .loc[:, '"15-19"']
        .reset_coords(drop=True)
        - maturation_of_secondary_education_graduates()
        .loc[:, '"15-19"']
        .reset_coords(drop=True)
        - enrollment_rate_to_tertiary_education()
        .loc[:, '"15-19"']
        .reset_coords(drop=True)
    ).expand_dims({"SchoolEnrollment": ['"15-19"']}, 1),
    lambda: initial_secondary_education_graduates()
    .loc[:, '"20-24"']
    .reset_coords(drop=True)
    .expand_dims({"SchoolEnrollment": ['"15-19"']}, 1),
    "_integ_secondary_education_graduates",
)

_integ_secondary_education_graduates_1 = Integ(
    lambda: xr.DataArray(
        maturation_of_secondary_education_graduates()
        .loc[:, _subscript_dict["SecondaryEdPrevious"]]
        .rename({"SecondaryEdCohorts": "SecondaryEdPrevious"})
        .values,
        {
            "Gender": _subscript_dict["Gender"],
            "SecondaryEdButYoungest": _subscript_dict["SecondaryEdButYoungest"],
        },
        ["Gender", "SecondaryEdButYoungest"],
    )
    - death_rate_of_secondary_education_graduates()
    .loc[:, _subscript_dict["SecondaryEdButYoungest"]]
    .rename({"SecondaryEdCohorts": "SecondaryEdButYoungest"})
    - maturation_of_secondary_education_graduates()
    .loc[:, _subscript_dict["SecondaryEdButYoungest"]]
    .rename({"SecondaryEdCohorts": "SecondaryEdButYoungest"}),
    lambda: initial_secondary_education_graduates()
    .loc[:, _subscript_dict["SecondaryEdButYoungest"]]
    .rename({"SecondaryEdCohorts": "SecondaryEdButYoungest"}),
    "_integ_secondary_education_graduates_1",
)

_integ_secondary_education_graduates_2 = Integ(
    lambda: xr.DataArray(
        0,
        {"Gender": _subscript_dict["Gender"], '"0 to 19"': ['"0-4"']},
        ["Gender", '"0 to 19"'],
    ),
    lambda: xr.DataArray(
        0,
        {"Gender": _subscript_dict["Gender"], '"0 to 19"': ['"0-4"']},
        ["Gender", '"0 to 19"'],
    ),
    "_integ_secondary_education_graduates_2",
)

_integ_secondary_education_graduates_3 = Integ(
    lambda: xr.DataArray(
        0,
        {"Gender": _subscript_dict["Gender"], "SchoolEnrollment": ['"5-9"']},
        ["Gender", "SchoolEnrollment"],
    ),
    lambda: xr.DataArray(
        0,
        {"Gender": _subscript_dict["Gender"], "SchoolEnrollment": ['"5-9"']},
        ["Gender", "SchoolEnrollment"],
    ),
    "_integ_secondary_education_graduates_3",
)

_integ_secondary_education_graduates_4 = Integ(
    lambda: xr.DataArray(
        0,
        {"Gender": _subscript_dict["Gender"], "SchoolEnrollment": ['"10-14"']},
        ["Gender", "SchoolEnrollment"],
    ),
    lambda: xr.DataArray(
        0,
        {"Gender": _subscript_dict["Gender"], "SchoolEnrollment": ['"10-14"']},
        ["Gender", "SchoolEnrollment"],
    ),
    "_integ_secondary_education_graduates_4",
)

_integ_secondary_education_graduates_5 = Integ(
    lambda: (
        graduation_rate_from_secondary_education()
        .loc[:, '"20-24"']
        .reset_coords(drop=True)
        - death_rate_of_secondary_education_graduates()
        .loc[:, '"20-24"']
        .reset_coords(drop=True)
        - maturation_of_secondary_education_graduates()
        .loc[:, '"20-24"']
        .reset_coords(drop=True)
        - enrollment_rate_to_tertiary_education()
        .loc[:, '"20-24"']
        .reset_coords(drop=True)
        + maturation_of_secondary_education_graduates()
        .loc[:, '"15-19"']
        .reset_coords(drop=True)
    ).expand_dims({"YoGL cohorts": ['"20-24"']}, 1),
    lambda: initial_secondary_education_graduates()
    .loc[:, '"20-24"']
    .reset_coords(drop=True)
    .expand_dims({"YoGL cohorts": ['"20-24"']}, 1),
    "_integ_secondary_education_graduates_5",
)

_integ_secondary_education_graduates_6 = Integ(
    lambda: (
        graduation_rate_from_secondary_education()
        .loc[:, '"25-29"']
        .reset_coords(drop=True)
        - enrollment_rate_to_tertiary_education()
        .loc[:, '"25-29"']
        .reset_coords(drop=True)
        - death_rate_of_secondary_education_graduates()
        .loc[:, '"25-29"']
        .reset_coords(drop=True)
        - maturation_of_secondary_education_graduates()
        .loc[:, '"25-29"']
        .reset_coords(drop=True)
        + maturation_of_secondary_education_graduates()
        .loc[:, '"20-24"']
        .reset_coords(drop=True)
    ).expand_dims({"YoGL cohorts": ['"25-29"']}, 1),
    lambda: initial_secondary_education_graduates()
    .loc[:, '"25-29"']
    .reset_coords(drop=True)
    .expand_dims({"YoGL cohorts": ['"25-29"']}, 1),
    "_integ_secondary_education_graduates_6",
)


@component.add(
    name="Secondary Education Graduates by Gender",
    units="People",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"secondary_education_graduates": 1},
)
def secondary_education_graduates_by_gender():
    return sum(
        secondary_education_graduates()
        .loc[:, _subscript_dict["SecondaryEdCohorts"]]
        .rename({"Cohorts": "SecondaryEdCohorts!"}),
        dim=["SecondaryEdCohorts!"],
    )


@component.add(
    name="Secondary Education Variation",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def secondary_education_variation():
    return xr.DataArray([0.0, 0.0], {"Gender": _subscript_dict["Gender"]}, ["Gender"])


@component.add(
    name="Smoothed Total Population",
    units="People",
    comp_type="Stateful",
    comp_subtype="Smooth",
    depends_on={"_smooth_smoothed_total_population": 1},
    other_deps={
        "_smooth_smoothed_total_population": {
            "initial": {"population": 1},
            "step": {"population": 1, "year_period": 1},
        }
    },
)
def smoothed_total_population():
    return _smooth_smoothed_total_population()


_smooth_smoothed_total_population = Smooth(
    lambda: population(),
    lambda: year_period(),
    lambda: population(),
    lambda: 1,
    "_smooth_smoothed_total_population",
)


@component.add(
    name="Subsistence Food per Capita",
    units="kcal/(Person*Day)",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"sa_subsistence_food_per_capita": 1, "time": 1},
)
def subsistence_food_per_capita():
    """
    Subsistence amount of food per person required to survive.
    """
    return 2000 + step(__data["time"], sa_subsistence_food_per_capita() - 2000, 2020)


@component.add(
    name="SWITCH Impact of Education on Climate Mortality",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def switch_impact_of_education_on_climate_mortality():
    """
    0 : No impact, hence a constant 1 : The driver is MYS 2 : The driver is Share of Females aged 20-39 with sec plus education
    """
    return 1


@component.add(
    name="T0",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"t0_sa": 2, "current_year": 2, "time": 2},
)
def t0():
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["male"]] = 1.4 + step(
        __data["time"], float(t0_sa().loc["male"]) - 1.4, current_year()
    )
    value.loc[["female"]] = 3.5 + step(
        __data["time"], float(t0_sa().loc["female"]) - 3.5, current_year()
    )
    return value


@component.add(
    name="T0 SA",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def t0_sa():
    return xr.DataArray([1.4, 3.5], {"Gender": _subscript_dict["Gender"]}, ["Gender"])


@component.add(
    name="T1",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"t1_sa": 2, "current_year": 2, "time": 2},
)
def t1():
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["male"]] = 0.7 + step(
        __data["time"], float(t1_sa().loc["male"]) - 0.7, current_year()
    )
    value.loc[["female"]] = 1.2 + step(
        __data["time"], float(t1_sa().loc["female"]) - 1.2, current_year()
    )
    return value


@component.add(
    name="T1 SA",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def t1_sa():
    return xr.DataArray([0.7, 1.2], {"Gender": _subscript_dict["Gender"]}, ["Gender"])


@component.add(
    name="T2",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"t2_sa": 2, "current_year": 2, "time": 2},
)
def t2():
    value = xr.DataArray(np.nan, {"Gender": _subscript_dict["Gender"]}, ["Gender"])
    value.loc[["male"]] = 0.6 + step(
        __data["time"], float(t2_sa().loc["male"]) - 0.6, current_year()
    )
    value.loc[["female"]] = 0.4 + step(
        __data["time"], float(t2_sa().loc["female"]) - 0.4, current_year()
    )
    return value


@component.add(
    name="T2 SA",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def t2_sa():
    return xr.DataArray([0.6, 0.4], {"Gender": _subscript_dict["Gender"]}, ["Gender"])


@component.add(
    name="Tertiary age distribution",
    subscripts=["SecondaryGraduation"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def tertiary_age_distribution():
    value = xr.DataArray(
        np.nan,
        {"SecondaryGraduation": _subscript_dict["SecondaryGraduation"]},
        ["SecondaryGraduation"],
    )
    value.loc[['"15-19"']] = 0.606804
    value.loc[['"20-24"']] = 0.36567
    value.loc[['"25-29"']] = 0.0625012
    return value


@component.add(
    name="Tertiary Education",
    units="Person",
    subscripts=["Gender", "WorkingAge"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tertiary_education_graduates": 1},
)
def tertiary_education():
    return (
        tertiary_education_graduates()
        .loc[:, _subscript_dict["WorkingAge"]]
        .rename({"Cohorts": "WorkingAge"})
    )


@component.add(
    name="Tertiary Education Enrollment Fraction",
    units="1/Year",
    subscripts=["Gender", "SecondaryGraduation"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "effect_of_gwp_per_capita_on_tertiary_enrollment": 3,
        "reference_tertiary_education_enrollment_fraction": 3,
        "tertiary_age_distribution": 3,
    },
)
def tertiary_education_enrollment_fraction():
    value = xr.DataArray(
        np.nan,
        {
            "Gender": _subscript_dict["Gender"],
            "SecondaryGraduation": _subscript_dict["SecondaryGraduation"],
        },
        ["Gender", "SecondaryGraduation"],
    )
    value.loc[:, ['"15-19"']] = (
        (
            effect_of_gwp_per_capita_on_tertiary_enrollment()
            * reference_tertiary_education_enrollment_fraction()
            * float(tertiary_age_distribution().loc['"15-19"'])
        )
        .expand_dims({"SchoolEnrollment": ['"15-19"']}, 1)
        .values
    )
    value.loc[:, ['"20-24"']] = (
        (
            effect_of_gwp_per_capita_on_tertiary_enrollment()
            * reference_tertiary_education_enrollment_fraction()
            * float(tertiary_age_distribution().loc['"20-24"'])
        )
        .expand_dims({"YoGL cohorts": ['"20-24"']}, 1)
        .values
    )
    value.loc[:, ['"25-29"']] = (
        (
            effect_of_gwp_per_capita_on_tertiary_enrollment()
            * reference_tertiary_education_enrollment_fraction()
            * float(tertiary_age_distribution().loc['"25-29"'])
        )
        .expand_dims({"YoGL cohorts": ['"25-29"']}, 1)
        .values
    )
    return value


@component.add(
    name="Tertiary education enrollment Variation",
    units="Dmnl",
    subscripts=["Gender"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def tertiary_education_enrollment_variation():
    """
    Corresponding to 2000 values of the fraction of seondary education graduates aged 15-19 enrolling at tertiary education
    """
    return xr.DataArray([0.39, 0.4], {"Gender": _subscript_dict["Gender"]}, ["Gender"])


@component.add(
    name="Tertiary Education Graduates",
    units="People",
    subscripts=["Gender", "Cohorts"],
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={
        "_integ_tertiary_education_graduates": 1,
        "_integ_tertiary_education_graduates_1": 1,
        "_integ_tertiary_education_graduates_2": 1,
        "_integ_tertiary_education_graduates_3": 1,
        "_integ_tertiary_education_graduates_4": 1,
        "_integ_tertiary_education_graduates_5": 1,
        "_integ_tertiary_education_graduates_6": 1,
        "_integ_tertiary_education_graduates_7": 1,
    },
    other_deps={
        "_integ_tertiary_education_graduates": {
            "initial": {"initial_tertiary_education_graduates": 1},
            "step": {
                "graduation_rate_from_tertiary_education": 1,
                "death_rate_of_tertiary_education_graduates": 1,
                "maturation_of_tertiary_education_graduates": 1,
            },
        },
        "_integ_tertiary_education_graduates_1": {
            "initial": {"initial_tertiary_education_graduates": 1},
            "step": {
                "maturation_of_tertiary_education_graduates": 2,
                "death_rate_of_tertiary_education_graduates": 1,
            },
        },
        "_integ_tertiary_education_graduates_2": {"initial": {}, "step": {}},
        "_integ_tertiary_education_graduates_3": {"initial": {}, "step": {}},
        "_integ_tertiary_education_graduates_4": {"initial": {}, "step": {}},
        "_integ_tertiary_education_graduates_5": {"initial": {}, "step": {}},
        "_integ_tertiary_education_graduates_6": {
            "initial": {"initial_tertiary_education_graduates": 1},
            "step": {
                "graduation_rate_from_tertiary_education": 1,
                "death_rate_of_tertiary_education_graduates": 1,
                "maturation_of_tertiary_education_graduates": 2,
            },
        },
        "_integ_tertiary_education_graduates_7": {
            "initial": {"initial_tertiary_education_graduates": 1},
            "step": {
                "graduation_rate_from_tertiary_education": 1,
                "death_rate_of_tertiary_education_graduates": 1,
                "maturation_of_tertiary_education_graduates": 2,
            },
        },
    },
)
def tertiary_education_graduates():
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )
    value.loc[:, ['"20-24"']] = _integ_tertiary_education_graduates().values
    value.loc[:, _subscript_dict["TertiaryEdButYoungest"]] = (
        _integ_tertiary_education_graduates_1().values
    )
    value.loc[:, ['"0-4"']] = _integ_tertiary_education_graduates_2().values
    value.loc[:, ['"5-9"']] = _integ_tertiary_education_graduates_3().values
    value.loc[:, ['"10-14"']] = _integ_tertiary_education_graduates_4().values
    value.loc[:, ['"15-19"']] = _integ_tertiary_education_graduates_5().values
    value.loc[:, ['"25-29"']] = _integ_tertiary_education_graduates_6().values
    value.loc[:, ['"30-34"']] = _integ_tertiary_education_graduates_7().values
    return value


_integ_tertiary_education_graduates = Integ(
    lambda: (
        graduation_rate_from_tertiary_education()
        .loc[:, '"20-24"']
        .reset_coords(drop=True)
        - death_rate_of_tertiary_education_graduates()
        .loc[:, '"20-24"']
        .reset_coords(drop=True)
        - maturation_of_tertiary_education_graduates()
        .loc[:, '"20-24"']
        .reset_coords(drop=True)
    ).expand_dims({"YoGL cohorts": ['"20-24"']}, 1),
    lambda: initial_tertiary_education_graduates()
    .loc[:, '"20-24"']
    .reset_coords(drop=True)
    .expand_dims({"YoGL cohorts": ['"20-24"']}, 1),
    "_integ_tertiary_education_graduates",
)

_integ_tertiary_education_graduates_1 = Integ(
    lambda: xr.DataArray(
        maturation_of_tertiary_education_graduates()
        .loc[:, _subscript_dict["TertiaryEdPrevious"]]
        .rename({"TertiaryEdCohorts": "TertiaryEdPrevious"})
        .values,
        {
            "Gender": _subscript_dict["Gender"],
            "TertiaryEdButYoungest": _subscript_dict["TertiaryEdButYoungest"],
        },
        ["Gender", "TertiaryEdButYoungest"],
    )
    - death_rate_of_tertiary_education_graduates()
    .loc[:, _subscript_dict["TertiaryEdButYoungest"]]
    .rename({"TertiaryEdCohorts": "TertiaryEdButYoungest"})
    - maturation_of_tertiary_education_graduates()
    .loc[:, _subscript_dict["TertiaryEdButYoungest"]]
    .rename({"TertiaryEdCohorts": "TertiaryEdButYoungest"}),
    lambda: initial_tertiary_education_graduates()
    .loc[:, _subscript_dict["TertiaryEdButYoungest"]]
    .rename({"TertiaryEdCohorts": "TertiaryEdButYoungest"}),
    "_integ_tertiary_education_graduates_1",
)

_integ_tertiary_education_graduates_2 = Integ(
    lambda: xr.DataArray(
        0,
        {"Gender": _subscript_dict["Gender"], '"0 to 19"': ['"0-4"']},
        ["Gender", '"0 to 19"'],
    ),
    lambda: xr.DataArray(
        0,
        {"Gender": _subscript_dict["Gender"], '"0 to 19"': ['"0-4"']},
        ["Gender", '"0 to 19"'],
    ),
    "_integ_tertiary_education_graduates_2",
)

_integ_tertiary_education_graduates_3 = Integ(
    lambda: xr.DataArray(
        0,
        {"Gender": _subscript_dict["Gender"], "SchoolEnrollment": ['"5-9"']},
        ["Gender", "SchoolEnrollment"],
    ),
    lambda: xr.DataArray(
        0,
        {"Gender": _subscript_dict["Gender"], "SchoolEnrollment": ['"5-9"']},
        ["Gender", "SchoolEnrollment"],
    ),
    "_integ_tertiary_education_graduates_3",
)

_integ_tertiary_education_graduates_4 = Integ(
    lambda: xr.DataArray(
        0,
        {"Gender": _subscript_dict["Gender"], "SchoolEnrollment": ['"10-14"']},
        ["Gender", "SchoolEnrollment"],
    ),
    lambda: xr.DataArray(
        0,
        {"Gender": _subscript_dict["Gender"], "SchoolEnrollment": ['"10-14"']},
        ["Gender", "SchoolEnrollment"],
    ),
    "_integ_tertiary_education_graduates_4",
)

_integ_tertiary_education_graduates_5 = Integ(
    lambda: xr.DataArray(
        0,
        {"Gender": _subscript_dict["Gender"], "SchoolEnrollment": ['"15-19"']},
        ["Gender", "SchoolEnrollment"],
    ),
    lambda: xr.DataArray(
        0,
        {"Gender": _subscript_dict["Gender"], "SchoolEnrollment": ['"15-19"']},
        ["Gender", "SchoolEnrollment"],
    ),
    "_integ_tertiary_education_graduates_5",
)

_integ_tertiary_education_graduates_6 = Integ(
    lambda: (
        graduation_rate_from_tertiary_education()
        .loc[:, '"25-29"']
        .reset_coords(drop=True)
        - death_rate_of_tertiary_education_graduates()
        .loc[:, '"25-29"']
        .reset_coords(drop=True)
        - maturation_of_tertiary_education_graduates()
        .loc[:, '"25-29"']
        .reset_coords(drop=True)
        + maturation_of_tertiary_education_graduates()
        .loc[:, '"20-24"']
        .reset_coords(drop=True)
    ).expand_dims({"YoGL cohorts": ['"25-29"']}, 1),
    lambda: initial_tertiary_education_graduates()
    .loc[:, '"25-29"']
    .reset_coords(drop=True)
    .expand_dims({"YoGL cohorts": ['"25-29"']}, 1),
    "_integ_tertiary_education_graduates_6",
)

_integ_tertiary_education_graduates_7 = Integ(
    lambda: (
        graduation_rate_from_tertiary_education()
        .loc[:, '"30-34"']
        .reset_coords(drop=True)
        - death_rate_of_tertiary_education_graduates()
        .loc[:, '"30-34"']
        .reset_coords(drop=True)
        - maturation_of_tertiary_education_graduates()
        .loc[:, '"30-34"']
        .reset_coords(drop=True)
        + maturation_of_tertiary_education_graduates()
        .loc[:, '"25-29"']
        .reset_coords(drop=True)
    ).expand_dims({"YoGL cohorts": ['"30-34"']}, 1),
    lambda: initial_tertiary_education_graduates()
    .loc[:, '"30-34"']
    .reset_coords(drop=True)
    .expand_dims({"YoGL cohorts": ['"30-34"']}, 1),
    "_integ_tertiary_education_graduates_7",
)


@component.add(
    name="Tertiary Education Graduates by Gender",
    units="People",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tertiary_education_graduates": 1},
)
def tertiary_education_graduates_by_gender():
    return sum(
        tertiary_education_graduates()
        .loc[:, _subscript_dict["TertiaryEdCohorts"]]
        .rename({"Cohorts": "TertiaryEdCohorts!"}),
        dim=["TertiaryEdCohorts!"],
    )


@component.add(
    name="Total Birth Rate",
    units="People/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"birth_rate": 1},
)
def total_birth_rate():
    return sum(birth_rate().rename({"Gender": "Gender!"}), dim=["Gender!"])


@component.add(
    name="Total Birth Rate Indicator",
    units="Person/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_birth_rate": 1},
)
def total_birth_rate_indicator():
    return total_birth_rate()


@component.add(
    name="Total Death Rate",
    units="People/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"death_rate": 1},
)
def total_death_rate():
    return sum(
        death_rate().rename({"Gender": "Gender!", "Cohorts": "Cohorts!"}),
        dim=["Gender!", "Cohorts!"],
    )


@component.add(
    name="Total Duration in Primary",
    units="Person*Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "primary_education_graduates": 1,
        "average_primary_education_duration": 1,
    },
)
def total_duration_in_primary():
    """
    sum(Primary Education Graduates[Gender!, "25-29"])*Years of Edu in Primary
    """
    return (
        sum(
            primary_education_graduates()
            .loc[:, _subscript_dict["MYS"]]
            .rename({"Gender": "Gender!", "Cohorts": "MYS!"}),
            dim=["Gender!", "MYS!"],
        )
        * average_primary_education_duration()
    )


@component.add(
    name="Total Duration in Secondary",
    units="Person*Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "secondary_education_graduates": 1,
        "average_secondary_education_duration": 1,
        "average_primary_education_duration": 1,
    },
)
def total_duration_in_secondary():
    return sum(
        secondary_education_graduates()
        .loc[:, _subscript_dict["MYS"]]
        .rename({"Gender": "Gender!", "Cohorts": "MYS!"}),
        dim=["Gender!", "MYS!"],
    ) * (average_primary_education_duration() + average_secondary_education_duration())


@component.add(
    name="Total Duration in Tertiary",
    units="Person*Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "tertiary_education_graduates": 1,
        "average_tertiary_education_duration": 1,
        "average_secondary_education_duration": 1,
        "average_primary_education_duration": 1,
    },
)
def total_duration_in_tertiary():
    return sum(
        tertiary_education_graduates()
        .loc[:, _subscript_dict["MYS"]]
        .rename({"Gender": "Gender!", "Cohorts": "MYS!"}),
        dim=["Gender!", "MYS!"],
    ) * (
        average_primary_education_duration()
        + average_secondary_education_duration()
        + average_tertiary_education_duration()
    )


@component.add(
    name="Total Enrollment Rate to Primary Education",
    units="People/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"enrollment_rate_to_primary_education": 1},
)
def total_enrollment_rate_to_primary_education():
    return sum(
        enrollment_rate_to_primary_education().rename({"Gender": "Gender!"}),
        dim=["Gender!"],
    )


@component.add(
    name="Total enrollment rate to secondary education",
    units="People/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"enrollment_rate_to_secondary_education": 2},
)
def total_enrollment_rate_to_secondary_education():
    return sum(
        enrollment_rate_to_secondary_education()
        .loc[:, '"10-14"']
        .reset_coords(drop=True)
        .rename({"Gender": "Gender!"}),
        dim=["Gender!"],
    ) + sum(
        enrollment_rate_to_secondary_education()
        .loc[:, '"15-19"']
        .reset_coords(drop=True)
        .rename({"Gender": "Gender!"}),
        dim=["Gender!"],
    )


@component.add(
    name="Total Enrollment Rate to Tertiary Education",
    units="People/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"enrollment_rate_to_tertiary_education": 3},
)
def total_enrollment_rate_to_tertiary_education():
    return (
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
        + sum(
            enrollment_rate_to_tertiary_education()
            .loc[:, '"25-29"']
            .reset_coords(drop=True)
            .rename({"Gender": "Gender!"}),
            dim=["Gender!"],
        )
    )


@component.add(
    name="Total Fertility",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "normal_fertility": 1,
        "impact_of_education_on_fertility": 1,
        "impact_of_gdp_on_fertility": 1,
    },
)
def total_fertility():
    """
    Total fertility of mature reproductive population. Source of historical data: http://esa.un.org/unpp
    """
    return (
        normal_fertility()
        * impact_of_education_on_fertility()
        * impact_of_gdp_on_fertility()
    )


@component.add(
    name="Total Labor Force",
    units="People",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"labor_force": 1},
)
def total_labor_force():
    return sum(
        labor_force()
        .loc[:, :, "skill"]
        .reset_coords(drop=True)
        .rename({"Gender": "Gender!", "WorkingAge": "WorkingAge!"}),
        dim=["Gender!", "WorkingAge!"],
    )


@component.add(
    name="Total Population Indicator",
    units="Person*Million",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_female": 1, "population_male": 1},
)
def total_population_indicator():
    return population_female() + population_male()


@component.add(
    name="Total Population with No or Incomplete Education",
    units="People",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_population_with_no_or_incomplete_education_by_gender": 1},
)
def total_population_with_no_or_incomplete_education():
    return sum(
        total_population_with_no_or_incomplete_education_by_gender().rename(
            {"Gender": "Gender!"}
        ),
        dim=["Gender!"],
    )


@component.add(
    name="Total Population with No or Incomplete Education by Gender",
    units="People",
    subscripts=["Gender"],
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_with_no_or_incomplete_education": 1},
)
def total_population_with_no_or_incomplete_education_by_gender():
    return sum(
        population_with_no_or_incomplete_education().rename({"Cohorts": "Cohorts!"}),
        dim=["Cohorts!"],
    )


@component.add(
    name="Total Primary Education Graduates",
    units="People",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"primary_education_graduates_by_gender": 1},
)
def total_primary_education_graduates():
    return sum(
        primary_education_graduates_by_gender().rename({"Gender": "Gender!"}),
        dim=["Gender!"],
    )


@component.add(
    name="Total Primary Education Graduates Indicator",
    units="Person*Million",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_primary_education_graduates": 1, "people_to_million_people": 1},
)
def total_primary_education_graduates_indicator():
    return total_primary_education_graduates() * people_to_million_people()


@component.add(
    name="Total Secondary Education Graduates",
    units="People",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"secondary_education_graduates_by_gender": 1},
)
def total_secondary_education_graduates():
    return sum(
        secondary_education_graduates_by_gender().rename({"Gender": "Gender!"}),
        dim=["Gender!"],
    )


@component.add(
    name="Total Secondary Education Graduates Indicator",
    units="Person*Million",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_secondary_education_graduates": 1,
        "people_to_million_people": 1,
    },
)
def total_secondary_education_graduates_indicator():
    return total_secondary_education_graduates() * people_to_million_people()


@component.add(
    name="Total Tertiary Education Graduates",
    units="People",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"tertiary_education_graduates_by_gender": 1},
)
def total_tertiary_education_graduates():
    return sum(
        tertiary_education_graduates_by_gender().rename({"Gender": "Gender!"}),
        dim=["Gender!"],
    )


@component.add(
    name="Total Tertiary Education Graduates Indicator",
    units="Person*Million",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_tertiary_education_graduates": 1, "people_to_million_people": 1},
)
def total_tertiary_education_graduates_indicator():
    return total_tertiary_education_graduates() * people_to_million_people()


@component.add(
    name="x0 age fertility",
    units="Dmnl",
    subscripts=["Fertile"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def x0_age_fertility():
    return xr.DataArray(
        [2.35787, 2.27194, 2.77236, 10.0, 10.0, 6.36842, 3.5155],
        {"Fertile": _subscript_dict["Fertile"]},
        ["Fertile"],
    )


@component.add(
    name="x0 edu fer", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def x0_edu_fer():
    return 0.6579


@component.add(
    name="x0 food pop",
    units="Dmnl",
    limits=(0.0, 1.0, 0.05),
    comp_type="Constant",
    comp_subtype="Normal",
)
def x0_food_pop():
    return 0.8


@component.add(
    name="x0 gdp fer", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def x0_gdp_fer():
    return 0.795


@component.add(
    name="x0 LE gdp",
    units="Dmnl",
    limits=(0.0, 1.0, 0.05),
    comp_type="Constant",
    comp_subtype="Normal",
)
def x0_le_gdp():
    """
    Parameter determining inflection point of impact of wealth on health services availability.
    """
    return 0.1


@component.add(
    name="x0 LE mys",
    units="Dmnl",
    limits=(0.2, 1.0, 0.05),
    comp_type="Constant",
    comp_subtype="Normal",
)
def x0_le_mys():
    """
    Parameter determining inflection point of impact of wealth on health services availability.
    """
    return 0.45


@component.add(
    name="x0 mor",
    units="Dmnl",
    subscripts=["Gender", "Cohorts"],
    comp_type="Constant",
    comp_subtype="Normal",
)
def x0_mor():
    """
    Original data please see the excel file 'InitialValues.xlsx','Mortality fractions parameters' , 'B5' and 'B11'
    """
    value = xr.DataArray(
        np.nan,
        {"Gender": _subscript_dict["Gender"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    )
    value.loc[["male"], :] = xr.DataArray(
        [
            [
                1.72915,
                -4.60988,
                -5.27428,
                -4.98716,
                -4.67178,
                -4.74645,
                -4.79642,
                -4.53575,
                -4.32483,
                -4.69609,
                -4.6186,
                -4.93752,
                -5.47145,
                -5.59146,
                -6.15601,
                -6.65474,
                -6.35979,
                -11.7132,
                -17.0173,
                -17.403,
                -18.081,
            ]
        ],
        {"Gender": ["male"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    ).values
    value.loc[["female"], :] = xr.DataArray(
        [
            [
                1.70094,
                -5.73244,
                -5.96389,
                -5.70503,
                -5.24789,
                -5.06949,
                -4.99958,
                -4.94269,
                -4.52645,
                -4.45661,
                -4.44679,
                -4.2957,
                -4.15355,
                -4.09055,
                -4.09125,
                -4.24153,
                -4.339,
                -9.85233,
                -13.5394,
                -15.9673,
                -29.0463,
            ]
        ],
        {"Gender": ["female"], "Cohorts": _subscript_dict["Cohorts"]},
        ["Gender", "Cohorts"],
    ).values
    return value


@component.add(
    name="y climate mortality",
    units="percent",
    comp_type="Constant",
    comp_subtype="Normal",
)
def y_climate_mortality():
    """
    The parameter that defines the negative values of mortality impact when T change is below 0. Obtained from the curve fit to the Bressler et al. 2021 function.
    """
    return 7.96458


@component.add(
    name="Year Period", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def year_period():
    return 1
