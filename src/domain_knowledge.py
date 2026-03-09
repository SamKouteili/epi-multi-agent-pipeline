"""Domain knowledge for EPI indicators, validated against the 2024 Technical Appendix.

Provides context to Stage 1 so the research agent focuses on novel proxies
rather than rediscovering known facts about each indicator.

Validation source: docs/2024epitechnicalappendix20241207.pdf
See also: docs/domain_knowledge_process.txt for cross-referencing methodology.
"""

DOMAIN_KNOWLEDGE: dict[str, str] = {
    # =========================================================================
    # ENVIRONMENTAL HEALTH — Air Quality (AIR)
    # =========================================================================
    "HPE": """\
HPE (Anthropogenic PM2.5 Exposure) measures population-weighted average fine particulate \
matter concentration from human sources. Calculated as HPE = PME x FHP, where PME is \
satellite-derived total PM2.5 and FHP is the anthropogenic fraction (excluding dust, sea \
spray, volcanoes). Units: ug/m3. Data from Washington University in St. Louis (PME) and \
GBD Major Air Pollution Sources (FHP), 1998-2022. Transformation: ln(x). Polarity: \
negative (lower = better). Targets: best=2.5, worst=28.58 (95th pctl).

IHME/satellite data provides near-full global coverage — no imputation model documented. \
Natural PM2.5 sources are explicitly removed via FHP fraction; wildfires are included as \
anthropogenic. Key confounders: industrialization level, urbanization, energy mix.

Sibling indicators: HFD (household solid fuels, also particulate-related). SOE, COE, VOE \
(Copernicus-sourced pollutant exposures). Weight: 6.5% of EPI.""",

    "HFD": """\
HFD (Household Air Pollution from Solid Fuels) measures age-standardized DALYs per 100k \
from household air pollution due to solid fuel use (wood, charcoal, dung, coal for cooking/ \
heating). Units: DALYs/100k. Data from IHME Global Burden of Disease, 1990-2021. \
Transformation: ln(x). Polarity: negative (lower = better). Targets: best=0.05, worst=10000.

IHME provides modeled estimates for all countries — no imputation needed. Strongly \
correlated with GDP/income (wealthier countries use cleaner fuels) and urbanization (urban \
populations less likely to use solid fuels). Actual indoor air quality monitoring is sparse \
in developing countries.

Sibling indicators: HPE (both measure particulate health burden). OZD, NOD (fellow IHME \
DALY air quality indicators). Weight: 6.5% of EPI.""",

    "OZD": """\
OZD (Ozone Exposure DALYs) measures age-standardized DALYs per 100k from ground-level \
ozone pollution. Units: DALYs/100k. Data from IHME, 1990-2021. Transformation: ln(x). \
Polarity: negative (lower = better). Targets: best=1, worst=250.

IHME modeled estimates — no imputation needed. Ozone formation depends on temperature, UV \
radiation, and NOx/VOC precursors from industry and transport. Can be higher in rural \
downwind areas than urban centers. Ozone health effects are less well-characterized than \
PM2.5.

Sibling indicators: HFD, NOD (IHME DALY air quality). VOE (VOCs are ozone precursors). \
Weight: 1.5% of EPI.""",

    "NOD": """\
NOD (NO2 Exposure DALYs) measures age-standardized DALYs per 100k from NO2 pollution. \
Units: DALYs/100k. Data from IHME, 1990-2021. Transformation: ln(x). Polarity: negative \
(lower = better). Targets: best=0.025 (5th pctl), worst=17.08 (99th pctl).

IHME modeled estimates — no imputation needed. Strongly tied to traffic density and fossil \
fuel combustion; highly correlated with urbanization and industrial activity. NO2 is \
spatially variable (roadside vs background), so national averages mask exposure heterogeneity.

Sibling indicators: HFD, OZD (IHME DALY). SOE, COE (combustion-related). Weight: 1% of EPI.""",

    "SOE": """\
SOE (SO2 Exposure) measures population-weighted annual average SO2 concentration at ground \
level. Units: ppm. Data from Copernicus Atmosphere Monitoring Service (CAMS reanalysis), \
2003-2022. Transformation: ln(x). Polarity: negative (lower = better). Targets: \
best=0.000282 (5th pctl), worst=0.0609 (95th pctl).

Copernicus reanalysis provides global coverage — no imputation needed. Strongly associated \
with coal-burning power plants, heavy industry, and volcanic activity. Shorter time series \
than IHME indicators (starts 2003 vs 1990).

Sibling indicators: COE, VOE (fellow Copernicus pollutant exposures, same Wolf et al. 2022 \
methodology). Weight: 0.5% of EPI.""",

    "COE": """\
COE (CO Exposure) measures population-weighted annual average carbon monoxide concentration \
at ground level. Units: ppm. Data from Copernicus/CAMS, 2003-2022. Transformation: ln(x). \
Polarity: negative (lower = better). Targets: best=0.0505 (1st pctl), worst=0.753 (99th pctl).

Copernicus reanalysis — no imputation needed. Associated with incomplete combustion \
(vehicles, biomass burning, industry). Correlates with HFD (solid fuel use is a major CO \
source). Shorter time series starting 2003.

Sibling indicators: SOE, VOE (Copernicus pollutants). HFD (solid fuels = major CO source). \
Weight: 0.5% of EPI.""",

    "VOE": """\
VOE (VOC Exposure) measures population-weighted annual average volatile organic compound \
concentration at ground level. Units: ppm. Data from Copernicus/CAMS, 2003-2022. \
Transformation: ln(x). Polarity: negative (lower = better). Targets: best=0.000732 \
(5th pctl), worst=0.0972 (95th pctl).

Copernicus reanalysis — no imputation needed. VOCs come from both anthropogenic sources \
(solvents, fuels, industry) and biogenic sources (tropical forests emit large amounts of \
isoprene). Biogenic VOCs may dominate in tropical/forested countries, confounding the \
policy-relevant signal. CAMS measures: Ethane, Propane, Formaldehyde, Isoprene.

Sibling indicators: SOE, COE (Copernicus). OZD (VOCs are ozone precursors). \
Weight: 0.5% of EPI.""",

    # =========================================================================
    # ENVIRONMENTAL HEALTH — Sanitation & Drinking Water (H2O)
    # =========================================================================
    "UWD": """\
UWD (Unsafe Drinking Water) measures age-standardized disability-adjusted life-years \
(DALYs) lost per 100,000 persons due to unsafe drinking water. Units: DALYs/100k. \
Data from IHME Global Burden of Disease study, 1990-2021, ~195 countries. \
Polarity: negative (lower = better). Transformation: ln(x).

UWD sits under Sanitation & Drinking Water (Environmental Health). IHME provides near-full \
global coverage so no cross-sectional imputation model is documented — only temporal \
interpolation/extrapolation via the standard EPI pipeline. Key confounders for any proxy \
analysis: GDP per capita, urbanization, and healthcare access all strongly predict UWD.

Sibling indicators: USD (unsafe sanitation DALYs) and HFD (household air pollution from \
solid fuels DALYs) share the same IHME methodology. WWT/WWC/WWG (wastewater indicators) are mechanistically \
related but use different data sources.""",

    "USD": """\
USD (Unsafe Sanitation) measures age-standardized DALYs per 100k from exposure to \
inadequate sanitation facilities. Units: DALYs/100k. Data from IHME Global Burden of \
Disease, 1990-2021. Transformation: ln(x). Polarity: negative (lower = better). Targets: \
best=0.757 (1st pctl), worst=7064.66 (99th pctl).

IHME modeled estimates for all countries — no imputation needed. Strongly correlated with \
GDP, urbanization, and governance quality. Sanitation infrastructure investment lags \
economic development. DALY attribution depends on epidemiological assumptions about \
sanitation-disease pathways.

Sibling indicators: UWD (unsafe drinking water — same issue category and IHME methodology). \
HFD, OZD, NOD, LED (fellow IHME DALY health burden indicators). Weight: 2% of EPI.""",

    # =========================================================================
    # ENVIRONMENTAL HEALTH — Heavy Metals (HMT)
    # =========================================================================
    "LED": """\
LED (Lead Exposure) measures age-standardized DALYs per 100k from lead contamination. \
Units: DALYs/100k. Data from IHME, 1990-2021. Transformation: ln(x). Polarity: negative \
(lower = better). Targets: best=62.32 (1st pctl), worst=2058.33 (99th pctl).

IHME modeled estimates — no imputation needed. Known confounders: historical leaded gasoline \
use, lead paint prevalence, lead smelting/mining, lead water pipes. Strongly correlated with \
regulatory history and industrial legacy. Lead exposure pathways are complex (paint, soil, \
water, air, food) and vary dramatically by country. Blood lead level monitoring is sparse in \
many developing countries.

Sibling indicators: USD, UWD (IHME DALY health burden). Only indicator in Heavy Metals \
issue category. Weight: 2% of EPI (sole indicator = 100% of HMT).""",

    # =========================================================================
    # ENVIRONMENTAL HEALTH — Waste Management (WMG)
    # =========================================================================
    "WRR": """\
WRR (Waste Recovery Rate) = (COM + INE + WRE) / MWG, where COM=composted, \
INE=incinerated with energy recovery, WRE=recycled, MWG=total municipal waste generated. \
Units: proportion (0-1). Data from Kaza et al. 2018 (What a Waste 2.0), UNEP/UNSD, OECD, \
Eurostat (2016-2022). No transformation applied. Polarity: positive (higher recovery = better).

56 of 180 countries are imputed using a cross-sectional regression: \
ln(WRR) = alpha + beta*GPC + gamma*R + epsilon (R^2=0.42), where GPC=GDP per capita and \
R=EPI region. A 25% penalty is applied to imputed values to incentivize reporting: \
WRR_imputed = exp(predicted) * 0.75. GDP and region are therefore KNOWN confounders — \
proxies must add information beyond these. The log-linear imputation model suggests \
proxies may relate log-linearly.

Key data quality issue: cross-country definitions of "municipal solid waste" vary (some \
include commercial/industrial, others household only). Eurostat data covers only households \
for Cyprus, Kosovo, Malta, Montenegro, Serbia.

Sibling indicators SMW and WPC use the same underlying waste data ecosystem.""",

    "SMW": """\
SMW (Controlled Solid Waste) = (LFU + LFC + INC + COM + INE + WRE) / MWG, where \
LFU=landfilled (unspecified), LFC=controlled landfill, INC=incinerated (without energy \
recovery), COM=composted, INE=incinerated (with energy recovery), WRE=recycled, \
MWG=total municipal waste generated. Units: proportion (0-1). \
Data from Kaza et al. 2018 (What a Waste 2.0), UNEP/UNSD, OECD, Eurostat (2016-2022). \
No transformation applied. Polarity: positive (higher controlled proportion = better).

Note: SMW includes ALL controlled disposal (landfill + incineration + recovery), while \
WRR only counts recovery methods (composting + recycling + energy-recovery incineration). \
SMW >= WRR by definition. No separate cross-sectional imputation model is documented for \
SMW in the Technical Appendix (only WRR has a documented regression model).

Key issue: the distinction between "controlled" and "uncontrolled" disposal is poorly \
defined across countries. Some define sanitary landfill narrowly (engineered liner + \
leachate collection), while others include any designated dump site. \
Eritrea is assigned zero due to lack of formal waste management infrastructure.

Sibling indicators WRR and WPC use the same underlying waste data.""",

    "WPC": """\
WPC (Waste per Capita) = MWG / POP (total municipal waste generated divided by population). \
Units: tonnes/person/year. Data from Kaza et al. 2018 (What a Waste 2.0), UNEP/UNSD, \
OECD, Eurostat (2016-2022). Transformation: ln(x). Polarity: negative (more waste = worse).

WPC is positively correlated with GDP per capita (richer countries generate more waste). \
No separate cross-sectional imputation model is documented in the Technical Appendix \
(only WRR has a documented regression model). Performance targets use 1st/99th percentiles.

Shares the same data quality issues as WRR and SMW: variable definitions of "municipal \
solid waste" across countries and temporal coverage gaps.

Sibling indicators WRR and SMW use the same underlying waste data.""",

    # =========================================================================
    # ECOSYSTEM VITALITY — Biodiversity & Habitat (BDH)
    # =========================================================================
    "MKP": """\
MKP (Marine KBA Protection) measures the percentage of marine Key Biodiversity Areas in \
a country's EEZ covered by marine protected areas. Units: %. Data from WDPA and World \
Database of KBAs, 2010-2024. No transformation. Polarity: positive (higher = better). \
Targets: best=100, worst=0.

No imputation documented. Only applies to coastal/island nations — landlocked countries \
excluded (materiality=SEA). Calculation: rasterize MPA and KBA polygons, compute \
intersection area ratio.

Sibling indicators: TKP (terrestrial equivalent), MHP, MPE (marine cluster). \
Weight: 3% of EPI.""",

    "MHP": """\
MHP (Marine Habitat Protection) measures the percentage of important marine/coastal \
habitats under protection. Covers 6 habitat types: sea grass, salt marshes, coral reefs, \
cold-water corals, seamounts/knolls, mangroves. Equal to the "Local Proportion of Habitats \
Protected Index" (Kumagai et al. 2022). Units: %. Data from WDPA, UNEP-WCMC, Global \
Mangrove Watch, 2010-2024. No transformation. Polarity: positive. Targets: best=100, worst=0.

No imputation. Coastal nations only (materiality=SEA). MHP = simple average of % protected \
across the 6 habitat types. Depends on habitat distribution map completeness.

Sibling indicators: MKP, MPE (marine cluster). Weight: 3% of EPI.""",

    "MPE": """\
MPE (Marine Protection Effectiveness) measures the ratio of industrial fishing effort \
(hours/km2) inside MPAs vs the entire EEZ. Lower ratio = more effective protection. \
Units: unitless ratio. Data from WDPA + Global Fishing Watch (AIS-based), 2012-2020. \
Transformation: ln(x). Polarity: negative (lower = better). Targets: best=0.01, worst=100.

No imputation. Coastal nations only. Limited to 2012-2020 (satellite AIS data). Only \
captures industrial vessels broadcasting AIS — misses small-scale fishing. Excludes \
pole-and-line and pots-and-traps gear types. Small constant (0.00001) added to handle \
zero-fishing cases.

Sibling indicators: MKP, MHP (marine cluster). Weight: 0.5% of EPI.""",

    "PAR": """\
PAR (Protected Areas Representativeness) measures how well protected areas represent the \
full range of environmental conditions and biodiversity within a country. Uses remote \
sensing, biodiversity informatics, and species distribution modeling for plants, vertebrates, \
and invertebrates. Units: unitless. Data from CSIRO (personal communication), single year \
2024 only. No transformation. Polarity: positive (higher = better). Targets: 95th/5th pctl.

No imputation. SINGLE SNAPSHOT (2024) — no temporal trend possible. Data is from personal \
communication and not publicly downloadable, making independent verification difficult.

Sibling indicators: TBN, TKP, SPI (protection coverage). Weight: 3% of EPI.""",

    "SPI": """\
SPI (Species Protection Index) measures species-level ecological representativeness of a \
country's protected area network. Uses habitat suitability modeling for 30,000+ species \
at high resolution. Units: %. Data from Map of Life (personal communication), 1980-2024. \
No transformation. Polarity: positive. Targets: best=100, worst=0.

No imputation. Data from personal communication (not publicly available). Relies on \
habitat suitability modeling.

Sibling indicators: SHI, PAR (species/representativeness cluster). Weight: 4% of EPI.""",

    "TBN": """\
TBN (Terrestrial Biome Protection) measures the percentage of each biome type in a country \
covered by protected areas, weighted by biome prevalence. Evaluates progress toward the \
Kunming-Montreal "30x30" target. Units: %. Data from WDPA + WWF biome areas, 1990-2024. \
No transformation. Polarity: positive. Targets: best=30, worst=0.

No imputation. Credit is capped at 30% per biome (aligned with 30x30 target). Calculation: \
for each biome, compute % protected, cap at 30%, weight by biome's share of country area.

Sibling indicators: TKP (terrestrial KBA counterpart), MKP/MHP (marine equivalents). \
Weight: 2.5% of EPI.""",

    "TKP": """\
TKP (Terrestrial KBA Protection) measures the percentage of terrestrial Key Biodiversity \
Areas covered by protected areas. Units: %. Data from WDPA + WDKBA, 2010-2024. \
No transformation. Polarity: positive. Targets: best=100, worst=0.

No imputation. Calculation: rasterize PA and KBA polygons, compute intersection ratio.

Sibling indicators: MKP (marine equivalent), TBN, PAR. Weight: 2.5% of EPI.""",

    "PAE": """\
PAE (Protected Area Effectiveness) measures the percentage of protected areas where \
cropland/built environment growth is below 0.25% between 2017 and 2022. Units: %. \
Data from WDPA + DynamicWorld v1 (Sentinel-2 AI-driven 10m LULC), single year 2022 \
(comparing 2017 vs 2022). No transformation. Polarity: positive. Targets: best=100, \
worst=30.3 (5th pctl).

No imputation. Pilot indicator. Only covers protected areas >100 km2. Single temporal \
comparison (2017 vs 2022). Relies on AI-driven satellite classification (DynamicWorld).

Sibling indicators: PHL (related PA integrity indicator). Weight: 0.5% of EPI.""",

    "PHL": """\
PHL (Protected Human Land) measures the percentage of protected area NOT covered by \
cropland and buildings. Units: %. Data from WDPA + DynamicWorld v1 (Sentinel-2), single \
year 2022. No transformation. Polarity: positive (higher = better). Targets: best=100, \
worst=82.4 (5th pctl).

No imputation. Only covers PAs >100 km2. Single snapshot (2022). Relies on DynamicWorld \
AI classification with 9 LULC classes.

Sibling indicators: PAE (related PA integrity indicator). Weight: 0.5% of EPI.""",

    "RLI": """\
RLI (Red List Index) measures overall extinction risk for species in a country, weighting \
species by the fraction of their range within the country. Units: proportion (0-1). \
Data from IUCN, 2000-2024. No transformation. Polarity: positive (higher = better, 1 = no \
species threatened). Targets: best=1.0, worst=0.69 (5th pctl).

No imputation. Known confounders: assessment effort bias (countries with more assessed \
species may appear worse); taxonomic coverage differences across groups.

Sibling indicators: SHI, SPI, BER (biodiversity status). Weight: 3% of EPI.""",

    "SHI": """\
SHI (Species Habitat Index) measures the proportion of suitable habitat remaining intact \
for each species relative to a 2001 baseline. Estimates potential population losses using \
habitat loss as proxy. Units: %. Data from Map of Life (personal communication), 2001-2022. \
No transformation. Polarity: positive. Targets: best=100, worst=96.6 (5th pctl).

No imputation. VERY NARROW range of variation (worst=96.6, best=100.0) — small differences \
are amplified in scoring. Data from personal communication; relies on habitat modeling.

Sibling indicators: SPI, RLI, BER. Weight: 2% of EPI.""",

    "BER": """\
BER (Bioclimatic Ecosystem Resilience) measures the capacity of natural ecosystems to \
retain species diversity under climate change, as a function of ecosystem area, connectivity, \
and integrity. Units: unitless. Data from CSIRO, only 5 data points: 2000, 2005, 2010, \
2015, 2020. No transformation. Polarity: positive (higher = better). Targets: 95th/5th pctl.

No imputation. VERY SPARSE TEMPORAL DATA — only 5 time points over 20 years makes trend \
analysis unreliable. Percentile-based targets. Relies on CSIRO modeling.

Sibling indicators: SHI, RLI, PAR. Weight: 0.5% of EPI.""",

    # =========================================================================
    # ECOSYSTEM VITALITY — Forests (ECS)
    # =========================================================================
    "PFL": """\
PFL (Primary Forest Loss) measures the 5-year moving average of the proportion of primary \
(humid tropical) forest lost relative to extent in 2001. Units: proportion. Data from \
Global Forest Watch, 2006-2022. Transformation: ln(x + 0.001). Polarity: negative \
(lower = better). Targets: best=0, worst=0.0484 (99th pctl).

No imputation. Forest = areas with >30% canopy cover. Calculation: PFL = PF5 / (5 * PFA), \
where PF5 = 5-year cumulative loss, PFA = primary forest area in 2001. Loss detection \
accuracy varies by region.

Sibling indicators: IFL, FCL, TCG, FLI (all Forests). Weight: 1.5% of EPI.""",

    "IFL": """\
IFL (Intact Forest Landscape Loss) measures the 5-year moving average of the proportion of \
intact forest landscape lost relative to extent in 2000. Intact forest landscapes are large \
undisturbed forest expanses with disproportionate biodiversity and carbon value. Units: \
proportion. Data from Global Forest Watch, 2005-2022. Transformation: ln(x + 0.0001). \
Polarity: negative. Targets: best=0, worst=0.0191 (99th pctl).

No imputation. Subset of primary forest — only countries with intact forest landscapes in \
2000 receive scores. Calculation: IFL = IF5 / (5 * IFA).

Sibling indicators: PFL, FCL, TCG, FLI. Weight: 1.5% of EPI.""",

    "FCL": """\
FCL (Tree Cover Loss weighted by Permanency) measures forest loss weighted by the likely \
permanency of deforestation drivers. 5-year moving average as proportion of 2000 extent. \
Units: proportion. Data from Global Forest Watch, 2005-2022. Transformation: ln(x + 0.001). \
Polarity: negative. Targets: best=0, worst=0.0169 (99th pctl).

No imputation. Permanency weights by driver: Commodity=1.0, Urbanization=1.0, Shifting \
agriculture=0.75, Forestry=0.50, Wildfire=0.25, Unknown=1.0. FCL = TCL * w_bar where \
w_bar is the weighted average driver adjustment.

Sibling indicators: PFL, IFL, TCG, FLI. Weight: 1.25% of EPI.""",

    "TCG": """\
TCG (Net Tree Cover Change) measures net change in forest cover from 2000 to 2020. Unlike \
other forest indicators, uses tree height data (not canopy cover). Units: %. Data from \
Global Forest Watch, SINGLE YEAR 2020 only. No transformation. Polarity: positive \
(higher = better). Targets: best=10, worst=-10.

No imputation. SINGLE SNAPSHOT — no temporal trend possible. Based on tree height rather \
than canopy data, so not directly comparable to PFL/IFL/FCL.

Sibling indicators: PFL, IFL, FCL, FLI. Weight: 0.5% of EPI.""",

    "FLI": """\
FLI (Forest Landscape Integrity) measures the mean Forest Landscape Integrity Index across \
a country's territory, based on observed/inferred human disturbances and connectivity loss. \
Units: % (0-100). Data from Grantham et al. 2020 (Nature Communications), SINGLE YEAR \
2020 only. No transformation. Polarity: positive. Targets: best=100, worst=0.

No imputation. SINGLE SNAPSHOT — no temporal trend possible. The underlying study found \
only 40% of remaining forests have high ecosystem integrity.

Sibling indicators: PFL, IFL, FCL, TCG. Weight: 0.25% of EPI.""",

    # =========================================================================
    # ECOSYSTEM VITALITY — Fisheries (FSH)
    # =========================================================================
    "FSS": """\
FSS (Fish Stock Status) measures the percentage of total catch from collapsed stocks within \
a country's EEZs. Units: %. Data from Sea Around Us, 1950-2019. Transformation: \
ln(x + 0.1). Polarity: negative (lower = better). Targets: best=0, worst=17.39 (99th pctl).

No imputation. Coastal nations only (materiality=SEA). Stock classification: \
collapsed/over-exploited/exploited/developing/rebuilding. May lag real conditions.

Sibling indicators: FCD, BTZ, BTO, RMS (all Fisheries). Weight: 0.3% of EPI.""",

    "FCD": """\
FCD (Fish Catch Discarded) measures the proportion of total catch discarded at sea. Proxy \
for bycatch rates and wasteful fishing. Units: proportion. Data from Sea Around Us, \
1950-2019. Transformation: ln(x + 0.01). Polarity: negative. Targets: best=0, \
worst=0.674 (99th pctl).

No imputation. Coastal nations only. Discard reporting is notoriously unreliable — likely \
underestimates true discards.

Sibling indicators: FSS, BTZ, BTO, RMS. Weight: 0.4% of EPI.""",

    "BTZ": """\
BTZ (Bottom Trawling in EEZ) measures the fraction of catch in a country's EEZ captured \
by bottom trawling or dredging — indiscriminate practices that damage marine ecosystems. \
Units: proportion. Data from Sea Around Us, 1950-2019. Transformation: ln(x + 0.1). \
Polarity: negative. Targets: best=0, worst=0.822 (99th pctl).

No imputation. Coastal nations only. Gear-type classification accuracy varies by region.

Sibling indicators: BTO (global ocean version), FSS, FCD, RMS. Weight: 0.5% of EPI.""",

    "BTO": """\
BTO (Bottom Trawling in Global Ocean) measures the fraction of a country's entire fleet \
catch (globally) captured by bottom trawling or dredging. Units: proportion. Data from \
Sea Around Us, 1950-2019. Transformation: ln(x + 0.1). Polarity: negative. Targets: \
best=0, worst=0.921 (99th pctl).

No imputation. Coastal nations only. Same gear-type classification concerns as BTZ.

Sibling indicators: BTZ (EEZ version), FSS, FCD, RMS. Weight: 0.7% of EPI.""",

    "RMS": """\
RMS (Regional Marine Trophic Index) measures "fishing down the food web" — the slope of \
the Marine Trophic Index over a decade, excluding species below trophic level 3.2. Positive \
slope = trophic level recovering. Units: unitless. Data from Sea Around Us, 1989-2019. \
No transformation. Polarity: positive. Targets: best=0.015, worst=-0.015.

No imputation. Coastal nations only. Geographic expansion of fishing can mask trophic \
decline. MTI is catch-weighted, so shifts in target species matter. Requires 10+ years \
of data per EEZ. RMS = catch-weighted average of MTI slopes across EEZs.

Sibling indicators: FSS, FCD, BTZ, BTO. Weight: 0.1% of EPI.""",

    # =========================================================================
    # ECOSYSTEM VITALITY — Air Pollution (APO)
    # =========================================================================
    "OEB": """\
OEB (Ozone Exposure in KBAs) measures average ground-level ozone concentration across a \
country's Key Biodiversity Areas. Units: ppm. Data from Copernicus/CAMS + WDKBA, 2003-2022. \
No transformation. Polarity: negative (lower = better). Targets: 5th/95th pctl.

No imputation. Copernicus reanalysis provides global coverage. Spatial average over KBAs.

Sibling indicators: OEC (cropland version), NXA, SDA (emission trends). \
Weight: 0.5% of EPI.""",

    "OEC": """\
OEC (Ozone Exposure in Croplands) measures average ground-level ozone concentration across \
a country's croplands. Units: ppm. Data from Copernicus/CAMS + U. Maryland GLAD cropland \
maps, 2003-2022. No transformation. Polarity: negative. Targets: 5th/95th pctl.

No imputation. Requires overlay of ozone data with cropland extent maps — cropland \
classification accuracy matters.

Sibling indicators: OEB (KBA version), NXA, SDA. Weight: 0.5% of EPI.""",

    "NXA": """\
NXA (NOx Intensity Trend) measures the average annual rate of change in NOx emissions over \
10 years, adjusted for economic trends to isolate policy-driven change. Units: unitless. \
Data from CEDS, 1999-2022. No transformation. Polarity: negative (lower = better). \
Targets: best=-0.0394, worst=0.0758 (95th pctl).

No imputation. Uses the standard EPI "adjusted emissions growth rate" methodology: \
(1) NXR = Spearman corr(NOX, GDP). (2) Log-linear regression for slope. (3) NXB = exp(beta)-1. \
(4) If NXB < 0: NXA = NXB * (1 - NXR), discounting recession-driven declines. \
GDP is the primary confounder — explicitly adjusted for.

Sibling indicators: SDA (SO2 version, identical methodology), OEB, OEC. \
Weight: 2.5% of EPI.""",

    "SDA": """\
SDA (SO2 Intensity Trend) measures the average annual rate of change in SO2 emissions over \
10 years, adjusted for economic trends. Units: unitless. Data from CEDS, 1999-2022. \
No transformation. Polarity: negative. Targets: best=-0.0394, worst=0.0956 (95th pctl).

No imputation. Identical "adjusted emissions growth rate" methodology as NXA but for SO2. \
GDP explicitly adjusted for.

Sibling indicators: NXA (NOx version), OEB, OEC. Weight: 2.5% of EPI.""",

    # =========================================================================
    # ECOSYSTEM VITALITY — Agriculture (AGR)
    # =========================================================================
    "SNM": """\
SNM (Sustainable Nitrogen Management Index) balances efficient nitrogen use with maximum \
crop yields. Euclidean distance from optimal point where both NUE (nitrogen use efficiency) \
and NCR (nitrogen crop removal) are ideal. Units: unitless. Data from FAOSTAT, 1965-2021. \
No transformation. Polarity: negative (lower = better). Targets: best=0, worst=1.316 (99th pctl).

No imputation. Calculation: NUE = NCR/NTI (efficiency, capped at 1 via normalization). \
NCR normalized against 90 kg/ha target (Zhang et al. 2022). SNM = sqrt((1-NCR_norm)^2 + \
(1-NUE_norm)^2). 5-year moving average applied. NUE > 1 indicates soil mining (insufficient \
inputs); NUE < 1 indicates excess nitrogen runoff.

Sibling indicators: PSU, PRS, RCY (all Agriculture). Weight: 1.2% of EPI.""",

    "PSU": """\
PSU (Phosphorus Surplus) measures the difference between phosphorus inputs and crop removal. \
Proxy for potential water pollution from excessive P use. Units: kg/ha. Data from FAOSTAT, \
1965-2021. Transformation: ln(x + 0.09). Polarity: negative (lower = better). Targets: \
best=0, worst=223.09 (99th pctl).

No imputation. If crop removal > inputs (soil mining), PSU = 0. 5-year moving average. \
Reference: Zou et al. 2022, Nature 611:81-87.

Sibling indicators: SNM, PRS, RCY. Weight: 0.1% of EPI.""",

    "PRS": """\
PRS (Pesticide Pollution Risk) measures biodiversity risk from pesticide pollution, as the \
geometric mean of pesticide risk scores. Units: unitless. Data from Tang et al. 2021 \
(Nature Geoscience) + Maggi and Tang 2024 (PESTCHEMGRIDS v2.01). ONLY 2 TIME POINTS: \
2015 and 2018. No transformation. Polarity: negative. Targets: best=0, worst=4.5.

No imputation. VERY SPARSE TEMPORAL DATA — only 2 observations. The 2024 EPI uses an \
updated PESTCHEMGRIDS dataset with finer spatial resolution vs original Tang et al. 2021.

Sibling indicators: SNM, PSU, RCY. Weight: 0.5% of EPI.""",

    "RCY": """\
RCY (Relative Crop Yield) measures area-weighted average yield of 17 major crops relative \
to country-specific maximum attainable yields (Mueller et al. 2012). Units: proportion \
(0-1, capped at 1). Data from FAOSTAT, 1961-2022. No transformation. Polarity: positive \
(higher = better). Targets: best=1.0, worst=0.135 (1st pctl).

IMPUTATION MODEL: Linear regression RCY = alpha + beta*GPC + gamma*NRY + delta*R + epsilon, \
where GPC=GDP per capita, NRY=nitrogen relative yield, R=EPI region. R^2=0.51. \
50 countries imputed (including small island states, some African/Central Asian countries, \
Belgium, Iceland, Singapore). Materiality filter: only calculated for 130 countries where \
the 17 major crops represent >=5% of total harvested area.

The 17 crops: barley, cassava, cotton, groundnut, maize, millet, oil palm, potato, \
rapeseed, rice, rye, sorghum, soybean, sugar beet, sugarcane, sunflower, wheat.

Sibling indicators: SNM, PSU, PRS. Weight: 1.2% of EPI.""",

    # =========================================================================
    # ECOSYSTEM VITALITY — Water Resources (WRS)
    # =========================================================================
    "WWG": """\
WWG (Wastewater Generated per Capita) measures wastewater produced per person per year. \
Units: m^3/person/year. Data from Jones et al. 2021 (published in PANGAEA) and UN \
Statistics Division (2015-2021). Transformation: ln(x). Polarity: negative (more = worse). \
Performance targets: 5th/95th percentile.

Part of the wastewater indicator cluster (WWG/WWC/WWT/WWR) under Water Resources \
(Ecosystem Vitality). These four indicators are hierarchically related: WWG is total \
generated, WWC is proportion collected, WWT is proportion treated, WWR is proportion reused.

Temporal coverage is highly variable — most countries have data only around 2015, with \
scattered observations through 2021. No cross-sectional imputation model is documented \
in the Technical Appendix for wastewater indicators.""",

    "WWC": """\
WWC (Wastewater Collected) measures the proportion of wastewater collected for treatment. \
Sometimes measured as the percentage of population connected to wastewater treatment \
facilities. Units: proportion (0-1). Data from Jones et al. 2021, Eurostat, UNSD, OECD \
(2015-2021). No transformation applied. Polarity: positive (higher collection = better).

WWC is strongly correlated with urbanization (sewer systems are urban infrastructure) and \
GDP per capita. No cross-sectional imputation model is documented in the Technical Appendix.

Key quality issue: some countries report "sewerage coverage" (population connected to \
sewers) rather than "wastewater collected" (volume); these are related but not identical.

Sibling indicators: WWG, WWT, WWR form a hierarchical chain.""",

    "WWT": """\
WWT (Wastewater Treated) measures the proportion of municipal wastewater that undergoes \
at least primary treatment. Units: proportion (0-1). Data from Jones et al. 2021, UNSD, \
OECD (2015-2021). No transformation applied. Polarity: positive (higher treatment = better).

WWT is the most policy-relevant wastewater indicator because treatment is where pollution \
reduction occurs. No cross-sectional imputation model is documented in the Technical Appendix.

Key issue: treatment level definitions vary across countries — "primary treatment" ranges \
from basic sedimentation to more advanced processes depending on national standards.

Sibling indicators: WWG, WWC, WWR form a hierarchical chain.""",

    "WWR": """\
WWR (Wastewater Reused) measures the proportion of wastewater reused after treatment, \
either for irrigation in agriculture or, when clean enough, in industry or as drinking \
water. Units: proportion (0-1). Data from Jones et al. 2021 (2015 only). \
No transformation applied. Polarity: positive (higher reuse = better).

WWR has the WORST temporal coverage of all wastewater indicators — data exists for a \
single year (2015) for most countries. This makes trend analysis impossible with official \
data alone.

WWR is driven by water scarcity: countries in arid/semi-arid regions (MENA, Central Asia) \
have the strongest incentives to reuse wastewater. GDP is a weaker predictor than for \
WWT/WWC because both very rich (Israel, Singapore) and middle-income (Jordan, Tunisia) \
countries lead in reuse.

Sibling indicators: WWG, WWC, WWT form a hierarchical chain.""",

    # =========================================================================
    # CLIMATE CHANGE — Climate Change Mitigation (CCH)
    # =========================================================================
    "CDA": """\
CDA (CO2 Intensity Trend) measures the average annual rate of change in CO2 emissions over \
2013-2022, adjusted for economic trends to isolate policy effect. Units: proportion. Data \
from Global Carbon Budget, 1999-2022. No transformation. Polarity: negative (lower = better). \
Targets: best=-0.13, worst=0.13.

No imputation (near-universal coverage). Uses the standard EPI "adjusted emissions growth \
rate" methodology: (1) CDR = Spearman corr(CO2, GDP) over 10 years. (2) Log-linear slope: \
ln(CDO) = alpha + beta*t. (3) CDB = exp(beta)-1. (4) If CDB < 0: CDA = CDB * (1-CDR), \
discounting recession-driven declines. If CDB >= 0: CDA = CDB (no adjustment for growing \
emissions). GDP is the primary confounder — explicitly adjusted.

Best target derived from global CO2 growth rate needed for near-zero by 2050 within 1.5C \
carbon budget (275 Gt remaining from 2024).

Sibling indicators: CDF (country-specific targets version), CHA/FGA/NDA/BCA (other gas \
trends), GHA (total GHG version), GTI/GTP (composites). Weight: 7.5% of EPI.""",

    "CDF": """\
CDF (CO2 Trend with Country-Specific Targets) uses the same growth rate as CDA but with \
country-specific best/worst targets based on allocated share of remaining carbon budget. \
Units: unitless. Data from Global Carbon Budget, 1999-2022. No transformation. Polarity: \
positive (higher = better). Targets: best=100, worst=0.

Budget allocation uses Raupach et al. (2014) blended approach: s_i = 0.5*(e_i/E) + \
0.5*(p_i/P), combining inertia (current emissions share) and equal-per-capita (population \
share). "Best" = growth rate at which country reaches 2050 within budget; "Worst" = \
exceeding budget by 10x.

Sibling indicators: CDA, CBP (also uses carbon budget). Weight: 0.5% of EPI.""",

    "CHA": """\
CHA (Methane Intensity Trend) measures average annual rate of change in CH4 emissions over \
2013-2022, adjusted for economic trends. Units: proportion. Data from PRIMAP-hist, \
1999-2022. No transformation. Polarity: negative. Targets: best=-0.05, worst=0.05.

No imputation. Same 4-step adjusted growth rate as CDA but for CH4. GDP explicitly \
adjusted. Best target based on Global Methane Pledge (30% reduction by 2030 vs 2020). \
CH4 sources include agriculture (livestock, rice) and fossil fuel extraction.

Sibling indicators: CDA, FGA, NDA, BCA (gas trends), GHA (total GHG). \
Weight: 3% of EPI.""",

    "FGA": """\
FGA (F-Gases Intensity Trend) measures average annual rate of change in fluorinated gas \
emissions over 2013-2022. Units: proportion. Data from PRIMAP-hist, 1999-2022. \
No transformation. Polarity: negative. Targets: best=-0.12, worst=0.12.

No imputation. SIMPLER than other gas trends — NO GDP adjustment because F-gas emissions \
are largely uncorrelated with GDP. Just: FGB = exp(beta)-1 from log-linear regression. \
F-gas data in PRIMAP-hist already in CO2-eq (AR4 GWP basis).

Sibling indicators: CDA, CHA, NDA, BCA (gas trends). Weight: 2% of EPI.""",

    "NDA": """\
NDA (N2O Intensity Trend) measures average annual rate of change in N2O emissions over \
2013-2022, adjusted for economic trends. Units: proportion. Data from PRIMAP-hist, \
1999-2022. No transformation. Polarity: negative. Targets: best=-0.05, worst=0.05.

No imputation. Same 4-step adjusted growth rate as CDA but for N2O. GDP explicitly \
adjusted. N2O emissions are heavily linked to agriculture (fertilizer use, livestock), \
so agricultural GDP may be more specific confounder than total GDP.

Sibling indicators: CDA, CHA, FGA, BCA (gas trends), GHA (aggregate). \
Weight: 1% of EPI.""",

    "BCA": """\
BCA (Black Carbon Intensity Trend) measures average annual rate of change in black carbon \
emissions over 2013-2022, adjusted for economic trends. Units: proportion. Data from CEDS \
(different source than PRIMAP-hist), 1999-2022. No transformation. Polarity: negative. \
Targets: best=-0.05, worst=0.05.

No imputation. Same 4-step adjusted growth rate as CDA. GDP explicitly adjusted. Black \
carbon linked to incomplete combustion (cookstoves, diesel, biomass burning) — development \
level is a strong confounder. Note: BC is NOT included in the total GHG aggregate (GHA).

Sibling indicators: CDA, CHA, FGA, NDA (gas trends). Weight: 1.5% of EPI.""",

    "LUF": """\
LUF (Net Carbon Fluxes from Land Cover Change) measures net carbon fluxes from LULCF over \
the last decade, normalized by forested area in 2000. Negative = net sink. Units: Gg CO2 \
per hectare of forest. Data from Global Carbon Budget (fluxes) + GFW (forest area), \
1999-2022. No transformation. Polarity: negative (lower = better). Targets: best=-0.5, \
worst=0.5.

No imputation. Calculation: LUF = 10-year sum of net LULCF fluxes / TCA (forest area in \
2000). LULCF flux estimates have high uncertainty. Natural disturbances (fires, storms) \
affect net fluxes independently of policy.

Sibling indicators: related to forest indicators (FLI, TCG). Weight: 1% of EPI.""",

    "GTI": """\
GTI (GHG Trend Adjusted by Emissions Intensity) creates a curved scoring surface combining \
a trend component (GHA = adjusted GHG growth rate) with a level component (GHI = GHG/GDP). \
Countries with high emissions intensity are penalized even if their trend is improving. \
Units: unitless. Data from GCB + PRIMAP-hist, 1999-2022. No transformation. Polarity: \
positive (higher = better). Targets: best=100, worst=0.

No imputation. Formula: if GHI >= 80: GTI = 50 + (GHA + ((GHI-80)/100)^2)/0.04; \
if GHI < 80: GTI = 50 + (GHA - ((80-GHI)/80)^2)/0.04. This is a COMPOSITE — not a \
simple linear metric. GHG = CDO + FOG + 273*NOT + 27.2*CH4 (AR6 GWPs).

Sibling indicators: GTP (per-capita version), GHA (trend component). \
Weight: 6% of EPI.""",

    "GTP": """\
GTP (GHG Trend Adjusted by Per Capita Emissions) same concept as GTI but uses per-capita \
emissions instead of intensity. High per-capita emitters need to decarbonize faster. \
Units: unitless. Data from GCB + PRIMAP-hist, 1999-2022. No transformation. Polarity: \
positive. Targets: best=100, worst=0.

No imputation. Same curved formula as GTI but substituting GHP (per-capita level) for GHI. \
Example: US and India both score ~35 — US has slowly falling emissions but high per capita; \
India has rising emissions but low per capita.

Sibling indicators: GTI (intensity version), GHA, GHP. Weight: 6% of EPI.""",

    "GHN": """\
GHN (Projected 2050 GHG Emissions) extrapolates each country's emissions trajectory to 2050 \
using 10-year trend. Units: Gg CO2-eq. Data from GCB + PRIMAP-hist, 1999-2022. \
Transformation: ln(x + 1). Polarity: negative (lower = better). Targets: best=0, \
worst=1,072,273 (95th pctl).

No imputation. Uses adjusted slope (same GDP correction as GHA). GHG = CDO + FOG + \
273*NOT + 27.2*CH4 (AR6 GWPs). E50 = GHG_current + adjusted_slope * (2050 - t).

Sibling indicators: CBP (cumulative budget version), GHP, GHA. Weight: 1% of EPI.""",

    "CBP": """\
CBP (Projected Cumulative Emissions to 2050 vs Carbon Budget) compares cumulative projected \
emissions (2023-2050) to each country's allocated share of remaining carbon budget. Units: \
ratio (unitless). Data from GCB + PRIMAP-hist, baseline 2022. No transformation. Polarity: \
negative (lower = better). Targets: best=1, worst=10.

No imputation. SINGLE SNAPSHOT — based on 2022 baseline + forward projections. Budget \
allocation: Raupach blended 50/50 inertia-equity (same as CDF). Remaining budget = \
325.42 Gt CO2-eq. Allocation method is normative (50/50 weighting is arbitrary).

Sibling indicators: CDF (also uses carbon budget), GHN (projected level). \
Weight: 0.5% of EPI.""",
}
