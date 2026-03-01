"""Domain knowledge for EPI indicators, validated against the 2024 Technical Appendix.

Provides context to Stage 1 so the research agent focuses on novel proxies
rather than rediscovering known facts about each indicator.

Validation source: docs/2024epitechnicalappendix20241207.pdf
See also: docs/domain_knowledge_process.txt for cross-referencing methodology.
"""

DOMAIN_KNOWLEDGE: dict[str, str] = {
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
}
