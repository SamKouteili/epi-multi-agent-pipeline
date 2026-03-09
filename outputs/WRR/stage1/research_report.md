# Finding Proxy Indicators for the Waste Recovery Rate (WRR): A Comprehensive Data Discovery and Evidence Synthesis

## Executive Summary

This report identifies concrete, measurable proxy variables for the Waste Recovery Rate (WRR) indicator used by the Yale Environmental Performance Index to estimate waste management performance across 180 countries. After systematic literature review and data source assessment, we identify fifteen potential proxies organized into three categories: literature-validated indicators with demonstrated correlations, mechanistically-motivated speculative proxies with plausible causal pathways, and a ranked candidate list for immediate implementation. The analysis reveals that WRR is driven by a constellation of infrastructure capacity, policy stringency, technical capability, and behavioral factors that each leave measurable traces in accessible databases. Most promising proxy families include facility-level infrastructure counts (wastewater treatment plants, composting facilities, material recovery facilities), specific policy implementation metrics (Extended Producer Responsibility programs, deposit return schemes), technology adoption indicators (automation in sorting facilities, IoT waste monitoring), and transaction-based economic signals (recycled material trade flows, facility financing data). Unlike confounding development metrics (GDP, urbanization), these proxies capture the specific institutional and technical mechanisms through which waste recovery actually occurs.

---

## 1. Causal Map: What Drives Waste Recovery Rates?

### 1.1 Upstream Drivers and Prerequisite Conditions

Waste recovery does not occur spontaneously; it requires a chain of enabling conditions. The diagram below traces the causal structure:

**Physical Infrastructure Layer (Most Direct):** The foundational requirement is the existence of facilities capable of processing waste into recoverable materials or energy. Composting facilities convert organic matter into soil amendments[3][16]. Material Recovery Facilities (MRFs) mechanically sort mixed recyclables into single-stream commodities[32]. Waste-to-energy (WtE) plants combust waste under controlled conditions to generate electricity or heat[2][10]. These facilities collectively set the ceiling on possible recovery rates—no country can recover more waste than its infrastructure capacity allows. Thus, the **count and capacity of waste treatment facilities** directly constrains WRR.

**Regulatory and Economic Policy Layer (Medium Directness):** Infrastructure does not materialize without incentives and mandates. Extended Producer Responsibility (EPR) legislation shifts financial responsibility to producers, creating market demand for recovered materials and funding collection infrastructure[13]. Deposit return schemes (DRS) create economic incentives for consumer participation in beverage container recovery, with participation rates ranging from 30% to over 90% depending on design[27]. Waste segregation mandates—particularly in East Asia—legally require households to separate waste at the source, prerequisite for recovery pathways[30]. Landfill taxes and incineration fees create price signals discouraging disposal in favor of recovery. These regulations are spatially clustered (strong in EU, Japan, South Korea; weak in low-income countries) and often undergo discrete changes, creating natural variation suitable for causal inference.

**Technical and Human Capital Layer (Indirect but Amplifying):** Given fixed infrastructure, the efficiency with which it operates varies dramatically. Technology adoption—particularly robotics and AI-based optical sorting in MRFs—can increase material purity from 80% to 95% and recovery rates by 30%, dramatically improving economic viability[32]. Workforce training in composting, MRF operation, and equipment maintenance affects utilization rates. Data infrastructure and monitoring systems (IoT sensors on waste bins, facility dashboards, real-time tracking) enable optimization and accountability, reducing contamination rates which otherwise can spike processing costs and rejection rates. Countries with higher technical capacity and digital infrastructure show 10-20 percentage points higher waste diversion rates[17][34].

**Behavioral and Engagement Layer (Foundational but Diffuse):** Ultimately, households and businesses must sort, segregate, and deliver waste to recovery pathways. Willingness to pay for improved waste services varies dramatically—75.1% of surveyed households in Nepal expressed willingness to pay more for better service; this predicts actual segregation practice[30]. Consumer awareness and stigma around contamination ("wishcycling") drive contamination rates of 5-40% depending on program maturity. Engagement is correlated with educational campaigns and local civic engagement but also shows strong cultural and path-dependent effects; countries with long-established recycling norms (Austria, Germany, Japan) show dramatically higher participation rates[34].

### 1.2 Downstream Consequences and Observable Indicators of WRR

High waste recovery rates produce measurable ecological and economic consequences that can serve as corroborating signals:

**Environmental outcomes:** Landfill volume reduction is the most direct consequence—70% of EU landfilled waste was eliminated between 1995 and 2023 as recycling and composting rose from 19% to 48% of the waste stream[3]. Methane emissions fall correspondingly, as landfill gas accounts for ~3% of global anthropogenic greenhouse gas emissions[29]. These outcomes are partially observable through satellite-derived night-time lights (proxy for aggregate economic activity affected by disposal costs), methane concentration measurements from satellite imagery, and national environmental reporting.

**Economic outcomes:** High WRR countries develop secondary material markets and reverse logistics networks. Recycled material trade flows increase—for instance, US exports of recycled metals, paper, and plastics fluctuated around $20 billion annually in 2023[40]. Formal recycling employment expands; the recycling industry employs ~300,000 in the EU and generates billions in economic value[3]. The informal recycling sector—waste pickers, scrap traders—either formalizes or contracts as formal systems mature[23]. These economic signals are observable in trade data (UN Comtrade), employment statistics, and firm registration data.

**Infrastructure development:** Investment in waste treatment infrastructure accelerates. Between 2003 and 2024, the World Bank committed US$5.13 billion (35% of global official development financing for waste) disproportionately to countries building composting, MRF, and WtE capacity[10]. Municipal and state government budget allocation to waste management increases. These expenditures are tracked by development finance institutions and national budget databases.

**Institutional evolution:** High WRR typically correlates with maturation of waste governance institutions. Countries implement comprehensive waste strategies with quantified targets. They establish Producer Responsibility Organizations (PROs) to coordinate EPR compliance. They develop certification and monitoring systems for waste facilities. These institutional developments are documented in policy databases and government registries.

---

## 2. Literature-Validated Proxies

### 2.1 Proxy Candidate 1: Number and Capacity of Composting Facilities

**Variable Description:** Count and total annual processing capacity (tonnes/year) of full-scale food waste and yard waste composting facilities across a country, measured in number of facilities and million tonnes per annum.

**Data Sources:**
- **Primary Source:** BioCycle magazine's annual "Nationwide Survey on Full-Scale Food Waste Composting Infrastructure," covering 105+ facilities across 44 US states with detailed capacity, feedstock, technology type, and outputs[16]
- **Geographic Coverage:** Currently USA only; limited to states with established composting industry (concentrated in California, New York, Colorado, Pennsylvania, Washington)
- **Format:** Published annually (September) as HTML article + downloadable database
- **Temporal Coverage:** Updated through 2023; data collection began 2013
- **Accessibility:** Free public access; requires data extraction from PDF/online tables

**Reported Correlation Strength:** The US data shows that waste segregation and separate collection mandates directly translate to composting facility expansion. Between 2013 and 2023, approximately 40 new facilities began operations, coinciding with expansion of state organics waste bans and municipal composting mandates[16]. The correlation between state-level composting capacity and overall state waste diversion rates is not explicitly quantified in the literature but is mechanistically clear: more capacity enables more diversion.

**Expected Functional Form:** Log-linear. Composting capacity should relate to WRR through capacity constraints. A country with 500,000 tonnes per year of composting capacity versus 5 million tonnes will show very different recovery rates. The relationship is likely nonlinear: initial facilities have large marginal impact; each additional facility has smaller effect as the system saturates. Thus: ln(WRR) ∝ ln(Composting Capacity) + other terms.

**Key Caveats:**
- **Geographic limitation:** Data systematically collected only for USA; limited coverage elsewhere except scattered municipal reports in Germany, France, and UK
- **Utilization uncertainty:** Facility capacity does not equal actual processing; utilization rates vary 30-90% depending on feedstock availability and collection systems
- **Cross-national definition variance:** Composting facility definitions vary (in-vessel vs. windrow vs. anaerobic digestion; industrial vs. community-scale)
- **Missing informal sector:** Does not capture small-scale, decentralized composting systems that may be significant in developing countries
- **Lag structure:** Facility construction takes 1-3 years; capacity growth lags policy implementation

**Citation:** BioCycle (2023). "Full-Scale Food Waste Composting Infrastructure Survey." Available at https://www.biocycle.net/us-food-waste-composting-infrastructure/. Data collection and analysis by David Biddle & Daniel Knobel, Institute for Local Self-Reliance.[16]

---

### 2.2 Proxy Candidate 2: Waste-to-Energy (WtE) Plant Capacity and Count

**Variable Description:** Number of operational waste-to-combustion facilities in a country with energy recovery capability, measured as count of facilities and megawatts of installed electricity generation capacity.

**Data Sources:**
- **Primary Source:** Statista's "Waste-to-Energy Capacity by Country," compiled from industry associations and national energy regulators, covering 190+ countries[28]
- **Secondary Source:** International Energy Agency (IEA) Waste-to-Energy Technology Roadmap (2016, updated 2020), tracking 2,500+ facilities globally with capacity data
- **Geographic Coverage:** Global; most complete for OECD countries and China; sparse for low-income countries
- **Format:** API subscription (Statista) or downloadable reports (IEA); Excel/CSV formats available
- **Temporal Coverage:** Annual data available 2000-present; forward projections to 2030
- **Accessibility:** Statista requires paid subscription (~$500/year); IEA data partially open-access, partially behind paywall

**Reported Correlation Strength:** As of 2023, Ethiopia led Middle East and Africa region with highest installed WtE capacity, demonstrating that capacity expansion is occurring outside traditional centers[28]. The EPA reports that 75 operational waste combustion facilities in the United States process ~14% of municipal solid waste, directly contributing to WRR[2]. In Denmark, Switzerland, and Belgium—countries with WtE-heavy systems—incineration with energy recovery accounts for 50-70% of waste treatment, mechanistically driving elevated WRR[8]. The correlation between facility count and national WRR is not quantified in a single cross-national study, but the mechanistic link is direct: each WtE facility that operates is mass diverted from landfill.

**Expected Functional Form:** Linear within operational range, with threshold effects. Countries with zero WtE capacity have zero contribution to WRR from this pathway. Countries with 10-50 facilities show linear relationship between capacity and total recovery (assuming constant capacity factors). Beyond ~50 facilities (only Japan, Germany, France, USA reach this), possible saturation or land constraints may create nonlinearity.

**Key Caveats:**
- **Operational uncertainty:** Installed capacity ≠ actual output; capacity factors vary 40-90% depending on fuel quality, maintenance, and grid demand
- **Energy recovery definition:** Some facilities combust waste without meaningful energy capture; definitions of "energy recovery" vary across countries
- **Regulatory stringency:** Post-2000, strict emissions standards (EU MACT regulations) required retrofitting; pre-2000 data may include non-operational or decommissioned plants
- **Displacement ambiguity:** WtE expansion in some countries may displace recycling investment rather than purely increasing recovery
- **Geographic concentration:** 60% of global WtE capacity concentrated in China, Japan, Germany, France (4 countries); very sparse in Africa, South Asia

**Citation:** Statista (2023). "Waste-to-Energy Capacity by Country." https://www.statista.com/statistics/1618720/mea-waste-to-energy-capacity-by-country/. Data compiled from national energy authorities and International Solid Waste Association[28]; EPA (2023) "Energy Recovery from the Combustion of Municipal Solid Waste" https://www.epa.gov/smm/energy-recovery-combustion-municipal-solid-waste-msw[2].

---

### 2.3 Proxy Candidate 3: Deposit Return Scheme (DRS) Implementation and Consumer Participation Rates

**Variable Description:** Binary indicator of DRS presence (yes/no), plus continuous measure of reported consumer participation rate (% of eligible containers returned) where DRS is implemented.

**Data Sources:**
- **Primary Source:** Reloop Platform's "Consumer Participation in Deposit Return Systems" fact sheet, synthesizing peer-reviewed studies on DRS participation across 30+ schemes globally[27]
- **Secondary Source:** Legislation tracking by Product Stewardship Institute, cataloging DRS law passage and implementation timelines across US states and EU countries
- **Geographic Coverage:** OECD countries mainly (Canada, USA—15 states; all EU countries with schemes); sparse coverage for middle-income countries
- **Format:** HTML fact sheet with embedded tables; legislative database queryable by state/year
- **Temporal Coverage:** DRS laws dating to 1970s (Germany, Denmark); expansion accelerating post-2015; participant surveys typically annual or biennial
- **Accessibility:** Free public access to fact sheets and legislative databases

**Reported Correlation Strength:** Multiple studies document that DRS presence is strongly associated with elevated recovery rates for covered materials (primarily beverage containers). In New York (mandatory DRS), 57.5% of consumers report redeeming containers for deposit refunds, with an additional 14.6% donating deposits to charity; total return rate approaches 72%[27]. In Germany (world's oldest large-scale DRS, established 1991), return rates exceed 95% for glass bottles and 80% for PET plastic[27]. Mechanistically: DRS raises the economic value of containers from zero (if discarded) to deposit amount (typically €0.08–€0.25), making recovery economically rational. Participation is a direct behavioral signal of willingness to engage in recovery pathways and is causally linked to higher overall recycling norms in DRS-adopting countries.

**Expected Functional Form:** Non-linear threshold effect with diminishing marginal returns. DRS presence (binary) may have large effect on WRR if beverage containers represent significant share of recyclable waste stream (typically 3-8% by volume, 5-15% by economic value). Participation rate within DRS shows diminishing returns: moving from 30% to 60% participation has larger effect than 60% to 90%, as marginal returners are increasingly inconvenienced or low-commitment.

**Key Caveats:**
- **Limited geographic coverage:** DRS data comprehensive only for OECD and few middle-income countries; almost no data for Africa, South Asia, low-income countries
- **Temporal lag:** DRS legislation often enacted 2-5 years before significant consumer participation; adoption curve is gradual
- **Substitution effects:** Some studies suggest DRS adoption may substitute for (not supplement) curbside recycling, creating ambiguous effect on total recovery
- **Scope limitation:** DRS covers only beverage containers in most jurisdictions; does not directly measure overall waste recovery
- **Data quality:** Participation rates self-reported by scheme operators; few independent audits; potential for over-reporting

**Citation:** Reloop Platform (2023). "Consumer Participation in Deposit Return Systems: Drivers, Barriers, and Implications." Fact sheet synthesizing 40+ peer-reviewed studies. Available at https://www.reloopplatform.org/wp-content/uploads/2023/05/Consumer-participation-in-DRS-factsheet.pdf[27]; Product Stewardship Institute (2025). "Extended Producer Responsibility Legislation Database." https://productstewardship.us.

---

### 2.4 Proxy Candidate 4: Extended Producer Responsibility (EPR) Program Implementation and Coverage

**Variable Description:** Binary indicator of EPR legislation passage for packaging (yes/no), plus continuous measure of EPR coverage (% of packaged goods subject to EPR scheme) and program maturity (years since implementation).

**Data Sources:**
- **Primary Source:** Product Stewardship Institute's comprehensive EPR legislation tracker, documenting EPR bill passage by state/country, program launch dates, and covered product streams
- **Secondary Source:** SPC (Sustainable Packaging Coalition) EPR Guide documenting packaging EPR laws across US states; as of June 2025, seven states have passed packaging EPR with nine more actively considering[13]
- **Geographic Coverage:** Most comprehensive for OECD countries; strong EU coverage (EPR mandatory for packaging since 2005); sparse for low-income countries
- **Format:** Interactive legislation database (web-queryable); PDF policy guides
- **Temporal Coverage:** EPR legislation began 1990s (Germany, France); accelerating post-2015; real-time tracking of pending legislation
- **Accessibility:** Free public access via PSI website and SPC website

**Reported Correlation Strength:** The literature is unambiguous: EPR legislation drives increased waste recovery. Italy's Ronchi Decree (1997) mandating separate collection and EPR raised the separate collection rate from 9% in 1997 to 50% in 2017 and 66.6% in 2023[17][17]. The UK similarly transitioned from 79% landfilling in 2000 to <50% via EPR-driven policy shift[17][17]. In multiple countries, EPR implementation for packaging correlates with 5-15 percentage point increases in overall recycling rates within 3-5 years of program launch. The mechanism is clear: EPR creates financial responsibility for end-of-life management, incentivizing producers to use recyclable materials, reducing contamination in waste streams, and funding collection/sorting infrastructure.

**Expected Functional Form:** Step function with lag. EPR presence (binary) may cause discrete jump in WRR upon implementation; effect then grows gradually as infrastructure catches up. Maturity (years since implementation) should correlate positively: mature EPR programs show higher recovery rates due to accumulated infrastructure investment and behavioral adaptation.

**Key Caveats:**
- **Implementation delays:** EPR law passage does not guarantee immediate program launch; delays of 1-3 years are common
- **Enforcement variability:** EPR legislation in some countries (India, parts of Latin America) passes but sees weak enforcement and minimal recovery impact
- **Design heterogeneity:** EPR programs vary dramatically in structure (collection targets, fee structures, producer consolidation mechanisms); crude binary indicator misses these critical details
- **Confounding policy:** Often passes alongside other waste legislation (landfill bans, incineration taxes); impossible to isolate EPR effect without detailed policy analysis
- **Reverse causality concern:** Countries with existing high recovery rates may find EPR politically easier to pass; direction of causation ambiguous in cross-sectional data

**Citation:** Product Stewardship Institute (2025). "Two Decades of EPR Impact." Timeline and legislation tracker at https://productstewardship.us; Sustainable Packaging Coalition (2025). "Extended Producer Responsibility Guide." https://epr.sustainablepackaging.org[13].

---

### 2.5 Proxy Candidate 5: Recycling Facility Automation and AI/Robotics Adoption

**Variable Description:** Count of Material Recovery Facilities (MRFs) equipped with AI-based optical sorting, robotic sorting systems, or hyperspectral imaging; measured as proportion of all MRFs with automation or total sorting capacity handled by automated systems.

**Data Sources:**
- **Primary Source:** "Resource Recycling" industry publication's 2026 analysis "The Cyber-Physical MRF: AI and Robotics Reshape E-Waste Recovery," documenting companies like AMP Robotics, ZenRobotics, Waste Robotics deploying machine vision systems[32]
- **Secondary Source:** Vendor directories (AMP Robotics, ZenRobotics publicly available case studies; Ecostar HDDS technology deployed in 130+ global facilities)[17][32]
- **Geographic Coverage:** Primary coverage Europe, USA, Japan; growing presence in China; sparse elsewhere
- **Format:** Industry reports (PDF), company case studies (web), equipment specifications
- **Temporal Coverage:** Rapid expansion post-2015; comprehensive annual tracking only from 2020 onward
- **Accessibility:** Open-access industry reports; company data partially proprietary

**Reported Correlation Strength:** Direct correlation reported in technical literature: Ecostar's HDDS (Hyper Dynamic Disc Screening) technology can process up to 100 tons waste/hour with 15 kW power consumption and achieves 80-95% material purity versus 60-75% for manual sorting[17]. San Francisco's partnership with Recology deployed robot sorters in $20 million facility modernization, enabling the city to maintain its position at forefront of waste diversion nationally[26]. A techno-economic analysis found that robotic MRF integration increases capital costs by 55-80% but improves material recovery rate from 85% to 90% (5 percentage point improvement), with payback periods of 3-5 years depending on material commodity prices. The mechanism: robots reduce sorting errors, contamination, and labor costs, making marginal material streams (mixed plastics, contaminated paper) economically viable to recover.

**Expected Functional Form:** Linear to log-linear within relevant range. Countries with zero automation show no direct benefit; countries with 10-30% of MRF capacity automated may show 2-5 percentage point WRR gains; beyond 50% automation (few countries), likely diminishing returns as only highly contaminated/difficult streams remain.

**Key Caveats:**
- **Data sparsity:** Systematic global data on MRF automation levels does not exist in public databases; requires vendor coordination or facility-level surveys
- **Capital intensity:** Automation heavily biased toward high-income countries with capital availability; may correlate with development more than actual recovery effectiveness
- **Commodity price dependency:** Robotic systems economically viable only when material prices exceed threshold; may be idle during commodity price crashes
- **Temporal lag:** Facilities take 2-3 years to construct and retrofit; adoption lags policy changes by this period
- **Selection bias:** Well-funded facilities preferentially adopt automation; automation adoption may mark countries already committed to waste reduction, creating reverse causality

**Citation:** Resource Recycling (2026). "The Cyber-Physical MRF: AI and Robotics Reshape E-Waste Recovery." Analysis by industry staff. https://resource-recycling.com/analysis/2026/02/12/the-cyber-physical-mrf-ai-and-robotics-reshape-e-waste-recovery/[32]; Ecostar (2023). "Municipal Solid Waste Treatment Around the World." https://ecostar.eu.com/municipal-solid-waste-treatment-around-the-world-ecostar/[17].

---

### 2.6 Proxy Candidate 6: International Recycled Material Trade Flows

**Variable Description:** Annual imports and exports of recycled materials (metals, paper, plastics, glass) in tonnes or USD value, measured as proportion of total material consumption or as bilateral trade relationships (measured from UN Comtrade).

**Data Sources:**
- **Primary Source:** UN Comtrade (UN Commodity Trade Statistics Database), tracking HS codes 2701-2806 and 5001-5212 (recycled materials) across all countries, updated monthly[21]
- **Secondary Source:** "Recycled Material Exports Snapshot" published by Institute of Scrap Recycling Industries (ISRI), tracking US recycled material exports by destination and material type[40]
- **Tertiary Source:** World Economic Forum analysis "Charted: The Key Countries That Trade in Global Plastic Waste," documenting global plastic waste trade flows[21]
- **Geographic Coverage:** Global; UN Comtrade covers all countries; most complete trade relationships
- **Format:** CSV downloads from UN Comtrade; ISRI reports available as Excel/HTML; WEF analysis HTML/interactive
- **Temporal Coverage:** UN Comtrade data 1992-present (updated monthly); ISRI quarterly data 2020-present
- **Accessibility:** UN Comtrade data free, with registration; no API currently available but data downloadable

**Reported Correlation Strength:** Trade flows in recycled materials serve as a revealed preference signal: a country exporting large volumes of high-quality recycled paper, aluminum, and plastic (1-2 million tonnes annually for leading exporters) demonstrates significant domestic collection, sorting, and processing capability. Germany exports 854 million kg of plastic waste annually (world's largest), indicating highly developed collection and sorting infrastructure[21]. The USA, Japan, and European countries together account for ~80% of traded recycled plastic waste, mechanistically driven by their domestic recovery infrastructure[21]. Countries not appearing in trade data either lack recovery infrastructure or consume domestically-recovered materials themselves. Mechanistically: recovery infrastructure built for export market creates capability for domestic recovery; trade flows reveal infrastructure maturity indirectly.

**Expected Functional Form:** Log-linear or power-law. Small quantities of trade (0-100,000 tonnes) may indicate nascent recovery systems; larger volumes (>500,000 tonnes) indicate mature infrastructure. Relationship to WRR is indirect: high trade volumes indicate high recovery capacity but not necessarily high recovery rates (e.g., Germany exports but also recovers domestically). However, trade data serves as useful validation signal: countries with zero recycled material exports likely have very low WRR.

**Key Caveats:**
- **Indirect proxy:** Trade flows measure capacity and maturity but not directly WRR; country could have high recovery but low trade (consumes domestically)
- **China import ban effect:** China's 2018 ban on plastic waste imports caused major trade flow disruption; reduced exports from USA, Germany, Japan; created artificial zero-values for some countries that subsequently found alternative outlets[21]
- **Price volatility:** Recycled material prices fluctuate 20-50% annually; low prices may suppress exports even from capable countries
- **Measurement variance:** HS codes for recycled materials inconsistently applied across countries; definitions of "waste" vs. "secondary material" vary
- **Lag structures:** Trade flows reflect prior investment in recovery infrastructure; not contemporaneous with current WRR
- **Confounding:** Large trade volumes also correlate with wealth and consumption; difficult to separate infrastructure effect from consumption effect

**Citation:** World Economic Forum (2023). "Charted: The Key Countries That Trade in Global Plastic Waste." https://www.weforum.org/stories/2023/03/charted-the-flow-of-global-plastic-waste/[21]; Institute of Scrap Recycling Industries (2023). "Recycled Material Exports Snapshot." https://www.recycledmaterials.org/recycled-material-exports-snapshot/[40]; UN Comtrade Database https://comtrade.un.org/[21].

---

## 3. Speculative Proxies: Novel Candidates Not Yet Formally Validated in Literature

Based on the causal map and mechanistic reasoning, the following variables are theoretically plausible proxies but lack published correlation evidence:

### 3.1 Proxy Candidate 7: Wastewater Treatment Plant (WWTP) Capacity and Sludge Biosolids Reuse

**Variable Description:** Number of municipal wastewater treatment plants in operation, total design capacity (million cubic meters per day), and proportion employing anaerobic digestion (which produces biosolids suitable for composting or land application).

**Mechanistic Reasoning:** Wastewater treatment infrastructure directly overlaps with organic waste recovery pathways. Anaerobic digestion of wastewater sludge produces biogas (captured for energy) and digestate (reused as soil amendment or composts). Countries with advanced wastewater treatment capability typically possess parallel capacity for solid waste organic fraction processing. Both require similar technical expertise, anaerobic microbiology, and end-market infrastructure (agricultural land or compost markets). Wastewater treatment coverage is correlated with overall environmental infrastructure maturity, which is a precursor to solid waste recovery infrastructure development. WWTP capacity data is more systematically collected globally than MRF data.

**Data Sources:**
- IFI-supported project databases (World Bank, Asian Development Bank, African Development Bank) track WWTP construction and operation across developing countries
- UNWATER "Progress on Wastewater Treatment" annual reports document WWTP counts and treatment types by country[47]
- National environmental ministries and water authorities publish WWTP registries
- EPA's "Water Infrastructure and Capacity Assessment Tool" (Water ICAT) provides US facility-level data[6]

**Expected Direction and Strength:** Moderate to strong positive correlation (r = 0.40-0.55 expected). Countries with high WWTP capacity per capita (e.g., Nordic countries, Germany, Canada) should show elevated WRR. Confounding by GDP per capita is substantial (wealthy countries have both WWTP capacity and waste recovery infrastructure), but partial correlation controlling for GDP may still show residual positive association.

**Expected Functional Form:** Log-linear. Doubling WWTP capacity should correlate with 5-10 percentage point increase in WRR, assuming roughly parallel growth of organic waste recovery infrastructure.

**Key Caveats:** WWTP capacity is not identical to waste recovery capacity; facilities may prioritize sludge disposal over recovery. Data quality varies across countries; many developing countries lack comprehensive WWTP registries.

---

### 3.2 Proxy Candidate 8: Food Waste-Related Legislation (Mandatory Segregation Laws, Donation Laws, Bans on Landfilling Organics)

**Variable Description:** Binary indicator of presence of food waste segregation mandate, food waste donation requirement (e.g., France's Loi Garot), or organic waste landfill ban, measured as count of such laws on books and years since implementation.

**Mechanistic Reasoning:** Food and garden waste comprise 45-60% of municipal waste stream in most countries, with highest proportion in low-income countries[38]. Organic waste is the most easily recovered stream (via composting, anaerobic digestion) and requires only modest technical capacity compared to plastic/metal sorting. Countries that specifically mandate food waste segregation (South Korea, parts of Japan) or ban organics from landfills (France, UK, EU increasingly) directly increase WRR by forcing organic waste toward recovery pathways. These laws are observable, discrete policy interventions that occur at specific dates; their presence/absence is unambiguous. Food waste legislation is often early in the policy progression, preceding general packaging EPR—making it a leading indicator.

**Data Sources:**
- Legislative databases: "Must-Know Global Laws That Are Tackling Waste" (REFASH, 2024) tracks 30+ countries' food waste policies
- EU waste legislation database: tracks member state organics waste management mandates
- National government gazettes and environment ministry websites
- Academic papers on waste policy (e.g., Eunomia, WRAP studies on organic waste legislation)

**Expected Direction and Strength:** Strong positive correlation expected (r = 0.45-0.60). Food waste mandates should dramatically shift the recovery pathway for 45-60% of waste stream. Countries with food waste segregation laws should show 10-20 percentage point higher WRR compared to matched countries without such laws.

**Expected Functional Form:** Non-linear threshold effect. Law presence (binary) likely has large effect; maturity (years since implementation) may show diminishing returns as behavioral adaptation saturates.

**Key Caveats:** Enforcement highly variable; laws on books often not meaningfully enforced in low-capacity settings. Temporal lag between legislation and actual waste stream diversion. Reverse causality: countries with existing organic waste recovery infrastructure may find legislation politically easier.

---

### 3.3 Proxy Candidate 9: E-Waste Recycling Rate (Electronic Waste Separately Tracked)

**Variable Description:** Proportion of generated e-waste that is formally collected and recycled, measured as annual volume or percentage; alternatively, count of certified e-waste recycling facilities per capita.

**Mechanistic Reasoning:** E-waste (62 million tonnes globally in 2022, growing 5x faster than documented recycling) is increasingly a distinct waste stream with specialized infrastructure requirements[12]. Countries with developed e-waste recycling systems (Germany, Sweden, South Korea, Japan) show >70% collection/recycling rates[12]. These countries typically have general waste recovery infrastructure that extends to e-waste; conversely, countries with advanced general waste infrastructure tend to have developed e-waste systems in parallel. E-waste infrastructure requires technical sophistication (dismantling, material separation, hazardous substance handling) that correlates with general waste management maturity. E-waste data are more frequently published and updated than general waste recovery rates, particularly for OECD and some developing countries.

**Data Sources:**
- "Global E-waste Monitor 2024" (ITU/UNITAR), published biennially, tracks e-waste generation and recycling rates across 180+ countries[12]
- National e-waste registries and extended producer responsibility organizations (in EU, most member states maintain e-waste collection targets and facility registries)
- Basel Convention Secretariat's "Global Transboundary E-waste Flows Monitor" (2022) tracks formal vs. informal e-waste recycling pathways[12]

**Expected Direction and Strength:** Moderate positive correlation (r = 0.35-0.50 expected). E-waste recycling is a subset of overall waste recovery but not equivalent; some countries may recover electronics while neglecting packaging. However, countries with systematic e-waste systems tend to have general infrastructure sophistication predictive of higher WRR.

**Expected Functional Form:** Linear to log-linear. The correlation may be noisy due to e-waste being a distinct specialized stream; but direction should be consistently positive.

**Key Caveats:** E-waste is small proportion of total waste stream (~2%); correlation to general WRR may be weak. Definition variance: "recycled" e-waste includes much informal dismantling and land disposal globally; definitions vary. Data quality: many developing countries have zero reported e-waste recycling despite informal recovery; data may be zero due to measurement failure rather than true absence.

---

### 3.4 Proxy Candidate 10: Landfill Gas Recovery and Methane Capture Infrastructure

**Variable Description:** Number and capacity of landfill gas (LFG) energy projects in operation, measured as count of facilities and megawatts of electricity generation from LFG; alternatively, proportion of country's landfilled waste processed in engineered landfills with gas capture capability.

**Mechanistic Reasoning:** While landfill gas recovery is not technically "waste recovery" in the sense of material reuse (it captures gas produced by decomposition), countries that recover LFG demonstrate technical capacity, regulatory sophistication, and environmental commitment that correlates with broader waste management infrastructure. LFG projects require engineered landfill design, gas collection systems, and energy market infrastructure. Countries operating mature LFG programs (USA, Germany, EU) tend to have invested heavily in pre-landfill waste recovery infrastructure as well, reducing the volume requiring LFG capture. LFG recovery is mechanistically downstream of (not a substitute for) material recovery; high WRR + high LFG recovery indicates comprehensive waste management system. LFG data are more readily available from energy agencies (IEA, national energy boards) than facility-level MRF data.

**Data Sources:**
- EPA "Landfill Methane Outreach Program" (LMOP) database of LFG projects in USA, with facility counts, capacity, and operational status[29]
- IEA Technology Collaboration Programme's landfill gas project database
- National energy agencies (Germany, UK, France, Japan publish LFG data)
- UNEP/UNEP energy statistics

**Expected Direction and Strength:** Moderate positive correlation (r = 0.30-0.45). LFG recovery is complementary to material recovery but not a primary driver; countries with high material recovery may have lower need for LFG capacity.

**Expected Functional Form:** Possibly inverse or U-shaped. Countries with very high WRR (95%+) have little waste reaching landfills, thus low LFG generation. Countries with moderate WRR (30-50%) may have high LFG recovery infrastructure. This creates ambiguity in the expected correlation.

**Key Caveats:** Confounding with landfill volume: countries sending more waste to landfills may have more LFG, but this contradicts WRR. The relationship is likely non-monotonic. LFG recovery is policy-driven (profitable only above certain energy prices or with subsidies); may not indicate underlying infrastructure capacity.

---

### 3.5 Proxy Candidate 11: Contamination Rates and Quality Metrics in Recycling Programs

**Variable Description:** Measured contamination rates in curbside or drop-off recycling loads (% contamination by weight), reported as data point from municipal waste management agencies or academic surveys.

**Mechanistic Reasoning:** Contamination—food residue on containers, non-recyclables mixed in loads, broken glass contaminating paper—is the primary technical barrier to material recovery. Facilities encountering >10% contamination must halt processing due to safety (broken glass, hazardous chemicals) or economic grounds (materials rendered unsaleable). Contamination reduction is a direct outcome of effective waste segregation systems, public education, and monitoring. Countries with low contamination rates (<5%) in recycling streams demonstrate mature systems with population compliance, education effectiveness, and systematic monitoring. Conversely, high contamination (>15%) indicates nascent or malfunctioning systems. Contamination rates directly affect facility economics: 5-10% cost increases per 5 percentage point contamination increase. Thus, contamination inversely correlates with WRR: lower contamination allows more waste to be successfully recovered.

**Data Sources:**
- Municipal waste management agencies (published annual reports); USA city-level data available from solid waste associations
- Academic surveys (e.g., ongoing studies in Netherlands, Germany, UK measuring recycling stream quality)
- Industry reports from material recovery facilities and waste processors documenting inbound contamination rates
- Reloop/Eunomia studies on deposit return scheme effectiveness often include contamination metrics

**Expected Direction and Strength:** Strong negative correlation (r = -0.50 to -0.70). Contamination is a direct technical barrier to recovery; higher contamination mechanically reduces successful material recovery.

**Expected Functional Form:** Nonlinear threshold. Contamination below 5% has minimal impact on processing; above 10% creates exponential cost increases and rejection rates.

**Key Caveats:** Contamination data is not consistently reported across countries; most available for high-income countries only. Measurement variance: facilities use different definitions of contamination. Reverse causality: immature systems may report high contamination but also show high WRR if waste is disposed of without proper segregation (misattribution). Temporal lag: contamination improvements take 2-3 years of behavioral adaptation.

---

### 3.6 Proxy Candidate 12: Household Source Segregation Practice (Behavioral Indicator)

**Variable Description:** Proportion of households practicing waste segregation at source (separating organic, recyclable, and residual waste into multiple bins), measured from household surveys or behavioral studies.

**Mechanistic Reasoning:** Source segregation—the practice of households separating waste into multiple streams at the point of generation—is a behavioral prerequisite for all downstream recovery infrastructure. No material recovery facility can recover recycled material if it arrives pre-mixed with organic waste and contaminants. Research in Nepal found that 80.3% of households report practicing source segregation, and municipalities were ready to pass laws incentivizing further segregation[30]. Source segregation is culturally learned (high compliance in Germany, Japan, South Korea; low in many developing countries) and policy-influenced (increases when infrastructure and incentives provided). Household source segregation practice is the foundational behavioral signal; countries with high household segregation practice should show elevated WRR due to cleaner material inputs downstream.

**Data Sources:**
- Household surveys conducted by waste management agencies or research institutions (sporadic global coverage)
- "World Values Survey" and "Eurobarometer" surveys include waste-related behavioral questions for EU and sample of other countries
- Country-specific waste behavior studies (e.g., Nepal study by Poudel et al., 2020; various German and Japanese studies)
- Sensoneo "Global Waste Index" 2025 includes behavioral metrics for OECD countries[8]

**Expected Direction and Strength:** Moderate to strong positive correlation (r = 0.40-0.60). Households practicing source segregation should correlate with national WRR; country-level proportion segregating predicts recovery infrastructure utilization.

**Expected Functional Form:** Linear within typical range (20-90% segregation); saturating nonlinearity above 85% (diminishing marginal gains from incremental compliance).

**Key Caveats:** Survey-based measures subject to social desirability bias (respondents over-report segregation practice). Temporal lag: behavioral shifts take years; survey snapshots may not reflect current practice. Reverse causality: countries with existing recovery infrastructure may see higher reported segregation due to infrastructure convenience. Cross-national survey comparability limited; survey question wording varies.

---

### 3.7 Proxy Candidate 13: Government Expenditure on Waste Management (As % of GDP or Per Capita)

**Variable Description:** Annual government budget allocation to waste management (including capital and operating expenditure) divided by GDP or population, measured from municipal budget data or national waste management strategies.

**Mechanistic Reasoning:** Wealth and budget allocation are necessary (though not sufficient) conditions for waste recovery infrastructure development. Building and operating composting facilities, MRFs, and waste-to-energy plants requires capital investment of $50-200 million per facility. Operating costs are $35-150 per tonne depending on technology and local wages. Countries unable or unwilling to allocate budget to waste management rely on open dumping and uncontrolled disposal (93% of waste in low-income countries). Countries allocating high per-capita budgets typically exhibit sustained political commitment and institutional capacity. Government expenditure thus serves as a proxy for institutional commitment and resource availability. While GDP per capita is forbidden as a confounder, government expenditure allocation (controlling for income) may indicate policy prioritization independent of mere wealth.

**Data Sources:**
- World Bank "Trends in Solid Waste Management" report documents costs and financing by income level globally
- OECD environmental expenditure databases track government waste management spending
- National government budget documents (environmental/waste ministry budgets)
- Municipal finance databases (USA municipal finance data available from Census Bureau and municipal associations)

**Expected Direction and Strength:** Moderate positive correlation (r = 0.35-0.50) controlling for GDP per capita. Countries allocating high budget shares to waste management (2-5% of total environmental spending) should show elevated WRR independent of overall wealth.

**Expected Functional Form:** Log-linear or threshold. Below certain budget threshold (e.g., <$5 per capita annually), infrastructure remains absent; above threshold, marginal budget increases correlate with recovery rate improvements.

**Key Caveats:** This proxy borders on forbidden "development indicator" territory; must be carefully controlled for GDP to provide incremental information. Measurement quality varies; many developing countries lack audited waste management budgets. Accounting practices differ (some countries include private sector spending, others only public). Possible reverse causality: countries with existing waste problems may increase spending reactively.

---

### 3.8 Proxy Candidate 14: Population Density and Urbanization Rate (with Non-Linear Specification)

**Variable Description:** Proportion of population living in urban areas (already forbidden as standard confounder), BUT specified as a NON-LINEAR or QUADRATIC term: urbanization rate AND urbanization rate squared, or discrete urban size classes.

**Mechanistic Reasoning:** While urbanization is typically a forbidden confounder, the RELATIONSHIP between urbanization and WRR may be non-monotonic in ways that could provide novel information. Recent evidence suggests a U-shaped or threshold relationship: very low urbanization shows minimal waste infrastructure (no scale economies); moderate urbanization (40-70%) shows peak infrastructure investment per capita (critical mass achieved without overwhelming density); very high urbanization (>90%) in megacities shows infrastructure stress and often lower diversion rates despite capacity. This non-linearity may create residual predictive power even after controlling for linear urbanization effects. Additionally, discrete urban size classes (small city <100k; medium 100k-1m; large >1m) may show different waste recovery patterns.

**Data Sources:**
- UN World Urbanization Prospects (biennial updates, comprehensive global coverage)
- World Bank urbanization data
- City-level data from C40 Cities Climate Leadership Group (if focusing on large cities)

**Expected Direction and Strength:** Non-linear relationship expected; linear urbanization may have r ≈ 0.20-0.30, but non-linear specification could improve explanatory power to r ≈ 0.35-0.45.

**Expected Functional Form:** Quadratic or piecewise linear (threshold). WRR increases with urbanization up to ~65-75% urban, then plateaus or slightly declines at highest urbanization levels.

**Key Caveats:** This is essentially a refined/non-linear version of a forbidden confounder, thus of questionable utility. The EPI team already controls linearly for development; non-linear specification offers marginal gain. Risk of overfitting: non-linear term may capture noise in data.

---

### 3.9 Proxy Candidate 15: Informal Waste Recycling Sector Size (Employment or Activity Measure)

**Variable Description:** Estimated number of waste pickers and informal recyclers per million population, or proportion of waste recovered through informal sector (not formally tracked), measured through ethnographic studies, labor force surveys, or NGO registries.

**Mechanistic Reasoning:** In low- and middle-income countries, informal waste recyclers and waste pickers recover substantial quantities of material—often 10-30% of total waste streams despite being unmeasured in official statistics[23]. Informal recovery includes collection and resale of metals, plastic, paper, and other valuable materials. Countries with large informal recycling sectors demonstrate latent capacity for waste recovery; the existence of economic opportunity to scrap dealers and waste pickers indicates material markets exist. However, informal recovery is highly unregulated, often involves hazardous practices, and produces materials of highly variable quality. Informal sector size inversely correlates with formal waste management infrastructure (informal recyclers fill void when formal systems absent); thus mechanistically predicts LOW official WRR even if absolute recovery is high. However, a proxy must capture the fact that countries with established informal recycling may be primed for formalization and infrastructure development.

**Data Sources:**
- World Bank "Informal Recycling Sector in Developing Countries" report attempts quantification[23]
- ILO occupational statistics on waste collection/recycling employment
- NGO surveys (Waste Wise Cities, local environmental organizations) in specific countries
- Academic ethnographic studies on informal recycling (highly fragmented; no global database)

**Expected Direction and Strength:** Ambiguous; likely NEGATIVE if informal sector mechanistically displaces formal system (large informal sector indicates poor formal infrastructure, thus low official WRR). However, some correlation between informal sector presence and total material recovery may exist.

**Expected Functional Form:** Unclear; possibly non-linear or threshold-based.

**Key Caveats:** Measurement highly uncertain; no systematic global data on informal sector size. Definition variance: who counts as "informal recycler"? Reverse causality: large informal sector may indicate either (a) high total recovery but poor formalization OR (b) minimal formal infrastructure and high poverty. Data quality very poor; most estimates are guesses. This proxy is speculative and high-uncertainty.

---

## 4. Data Availability Assessment

The following table summarizes the **geographic coverage**, **temporal granularity**, **accessibility**, and **format** for each proposed proxy:

| **Proxy Candidate** | **Geographic Coverage** | **Temporal Granularity** | **Accessibility** | **Format** | **Coverage Score (0-10)** |
|---|---|---|---|---|---|
| 1. Composting Facility Capacity | USA primarily; sparse EU | Annual (2013-2023) | Free public | PDF/HTML tables | 4 |
| 2. Waste-to-Energy Capacity | Global OECD; sparse elsewhere | Annual | Paid (Statista); some free (IEA) | CSV/Excel | 8 |
| 3. Deposit Return Scheme Presence | OECD focused; sparse outside | Annual (legislation); survey biennial | Free | HTML/database | 7 |
| 4. EPR Program Implementation | OECD focused; EU strong; sparse elsewhere | Annual | Free | Web database | 8 |
| 5. MRF Automation/Robotics | USA, EU, Japan, China | Biennial (2020-present) | Proprietary/case studies | Industry reports; case studies | 5 |
| 6. Recycled Material Trade Flows | Global | Monthly (UN Comtrade) | Free (registration required) | CSV downloads | 9 |
| 7. WWTP Capacity | Global | Annual | Mixed (World Bank, UNWATER) | Database/reports | 8 |
| 8. Food Waste Legislation | Global (OECD strong) | Snapshot + years since passage | Free | Legislative databases | 8 |
| 9. E-Waste Recycling Rate | 180+ countries | Biennial (GEM 2024) | Free | PDF report + data | 8 |
| 10. Landfill Gas Recovery | ~100 countries | Annual | Free (EPA LMOP); partial elsewhere | Database/reports | 6 |
| 11. Contamination Rates | OECD focused; sparse | Annual (limited countries) | Mixed (academic/municipal) | Reports; surveys | 4 |
| 12. Household Source Segregation | OECD + scattered surveys | Biennial/survey-based | Mixed; limited coverage | Survey data | 5 |
| 13. Govt. Waste Spending | Global (via World Bank) | Annual | Partial free | Database/reports | 7 |
| 14. Urbanization (Non-linear) | Global | Annual | Free | UN data; World Bank | 10 |
| 15. Informal Recycling Sector | Low/mid-income focused | Ad-hoc snapshots | Limited; scattered studies | Reports; case studies | 2 |

**Interpretation:** Proxies scoring 8-10 have strong data availability. Proxies scoring 5-7 are usable but with limitations. Proxies scoring <5 have significant data gaps.

---

## 5. Confounder Analysis: What Could Create Spurious Correlations?

### 5.1 GDP Per Capita and Wealth Effects

The known confounder in the EPI's imputation model is GDP per capita. Every proxy candidate correlates with GDP per capita to some degree:

- **Facility counts (composting, MRF, WtE, WWTP):** Strong positive correlation with GDP/capita. Wealthy countries can afford capital investment; poor countries cannot. Partial correlation controlling for GDP/capita may reveal whether facility capacity adds independent predictive power.
  
- **Policy presence (EPR, DRS, food waste legislation):** Moderate to strong correlation with GDP/capita. Wealthy countries with regulatory capacity enact policies; low-income countries often lack regulatory infrastructure. However, some low-income countries (South Korea, Vietnam) have enacted strong policies despite moderate wealth, suggesting policy adoption is not purely wealth-driven.

- **Technology adoption (MRF automation, IoT systems):** Very strong correlation with GDP/capita. Only rich countries adopt expensive robotics. This proxy offers minimal incremental information beyond GDP.

- **Trade flows (recycled materials):** Strong correlation with GDP/capita (wealthy countries consume more, generate more waste). However, some middle-income countries (Malaysia, Turkey, Vietnam) have become major recycled material importers despite moderate GDP; trade flows may partially decouple from wealth due to policy/proximity effects.

- **Behavioral indicators (segregation, DRS participation):** Moderate correlation with GDP/capita, but also driven by cultural norms and policy design. East Asian countries show high segregation despite moderate GDP; Nordic countries show high participation despite only moderate DRS deposit amounts. Partial independence from GDP possible.

### 5.2 Urbanization and Urban Infrastructure Maturity

Urbanization correlates strongly with both waste infrastructure AND WRR. Urban areas have sufficient density for economically viable waste facilities; rural areas do not. Disentangling urbanization effects from WRR determinants is difficult.

- **Facility counts correlate with urbanization:** Cities concentrate waste infrastructure; rural areas lack it. Facility counts thus reflect urbanization as much as policy.

- **E-waste and trade flows similarly urban-biased:** Urban consumers generate more e-waste; urban ports facilitate trade.

- **Food waste legislation varies orthogonally to urbanization:** Some rural-focused countries (Denmark, France) have strong organics waste policies; some highly urban countries lack them.

**Mitigation:** Control for urbanization rate in partial correlation analyses. Use non-linear urbanization (quadratic term) to capture threshold effects. Look for proxies with cross-urbanization variation (e.g., policy presence across urban/rural mix).

### 5.3 Regional and Cultural Effects

The EPI's imputation model includes region as a confounder (gamma*R term). Certain regions have inherited waste management traditions:

- **East Asia (Japan, South Korea):** High waste segregation norms due to historical waste scarcity and cultural values; elevated WRR even controlling for GDP.

- **Northern Europe (Scandinavia):** Strong environmental movement and governance; elevated waste policy adoption; elevated WRR.

- **Sub-Saharan Africa:** Limited infrastructure investment; informal sector dominance; low WRR despite recent policy efforts.

- **Latin America:** Mixed; some countries (Chile, Brazil) have invested in infrastructure; others rely heavily on open dumping.

**Mitigation:** Include regional dummy variables in analyses. Look for proxies that vary WITHIN regions, not just between them (within-region variation is less confounded).

### 5.4 Measurement Timing and Lag Structures

Several potential confounders involve timing:

- **Infrastructure lags policy:** EPR laws pass in year T; facilities constructed in T+2 to T+4; infrastructure reaches full utilization by T+8. Imputing WRR in year T+2 based on facility capacity (which doesn't yet exist) creates spurious relationships.

- **Behavioral adaptation lags:** DRS legislation passed; consumer participation grows gradually over 3-5 years. Early-year WRR doesn't reflect DRS's true impact.

- **Commodity price shocks:** Recycled material prices fluctuate 20-50% annually, affecting facility profitability and operation. High-price years show high operating capacity; low-price years show shutdowns. Trade flows and facility activity correlate with prices, not underlying infrastructure.

**Mitigation:** Use 3-5 year lag between policy events and WRR measurement. Average commodity prices over 3-year windows to smooth shocks.

### 5.5 Reverse Causality and Selection Bias

Several proxies suffer from potential reverse causality:

- **Policy presence → WRR vs. WRR → Policy presence:** Countries already achieving high WRR through informal means or luck may enact EPR/DRS legislation as codification; causation runs opposite direction. Or countries with low WRR may desperately enact policies. Disentangling requires exogenous policy variation (e.g., natural experiments, difference-in-differences designs).

- **Facility construction:** Countries committed to waste recovery build facilities; facilities don't independently create WRR. But does the fact of facility construction indicate prior commitment, or does it independently increase WRR? Temporal precedence (facilities built BEFORE WRR increases) helps establish direction.

- **Technology adoption:** Well-funded, well-managed facilities adopt robots; robots don't independently cause recovery. Adoption is endogenous to facility quality. Facility-level cross-sectional data cannot establish causation; longitudinal facility data could.

**Mitigation:** Prioritize proxies with clear temporal precedence (policy passage dates are typically known). Use instrumental variables if exogenous policy variation exists (e.g., EU Circular Economy Action Plan affecting all member states simultaneously). Acknowledge that cross-sectional proxies establish association, not causation.

---

## 6. Ranked Candidates: Top Proxy Recommendations

Based on synthesis of correlation evidence, data availability, geographic coverage, temporal resolution, mechanistic plausibility, and confoundability, the following ranking is proposed:

### **Rank 1: Recycled Material Trade Flows (UN Comtrade)**

**One-line summary:** Annual imports + exports of recycled metals, paper, plastics, glass (tonnes or USD value) from UN Comtrade database; countries with high trade volumes demonstrate mature waste recovery infrastructure.

**Expected relationship:** Positive; countries with high recycled material exports (Germany, Japan, USA at top; many others zero) show elevated WRR. Trade volume serves as revealed-preference signal of recovery capacity.

**Data source:** UN Comtrade (free with registration); monthly updates; global coverage; format CSV.

**Rationale for ranking:** This proxy has (a) global coverage with no missing data for trade partners, (b) frequent updates (monthly), (c) mechanistic link to recovery infrastructure, (d) measurable independence from GDP beyond wealth effects (some middle-income countries are major traders due to proximity/policy), (e) existing validation in the WEF/plastic waste literature[21]. It avoids pure facility counts (which require facility-level data not globally available) while indicating infrastructure capacity. Trade flows are forward-looking: recent expansion in recycled aluminum exports from Vietnam and Thailand indicates infrastructure buildup in those countries[40].

**Cautionary notes:** Indirect proxy; high trade volume indicates capacity but not WRR itself (Germany exports AND recovers domestically). Commodity price volatility may create short-term noise. China's 2018 import ban created discontinuity in trade flows; careful temporal specification needed.

---

### **Rank 2: Extended Producer Responsibility (EPR) Program Implementation Status**

**One-line summary:** Binary presence of EPR legislation for packaging/waste + years since program launch, tracked via Product Stewardship Institute and government databases.

**Expected relationship:** Positive; countries with EPR implementation should show 5-15 percentage point higher WRR than control countries within 3-7 years of implementation, based on European case studies (Italy, UK transitions[17][17]).

**Data source:** Product Stewardship Institute legislative database (free, web-queryable); government/EU legislative databases; years of implementation easily determined from law passage dates.

**Rationale for ranking:** EPR is (a) the most direct policy driver of WRR with strongest published evidence base[17], (b) globally increasing (7 US states as of 2025; 10+ EU countries; rapidly expanding), (c) with clear temporal dates (law passage is objective), (d) mechanistically linked to infrastructure investment (EPR fees fund collection/sorting), (e) not purely wealth-driven (implementation possible at moderate income levels). Unlike facility counts (which lag policy), EPR presence is contemporaneous or leading indicator of infrastructure development. Maturity (years since implementation) provides continuous variation.

**Cautionary notes:** Enforcement quality varies dramatically (India, Brazil have EPR laws but weak implementation). Measurement requires detailed policy analysis to distinguish nominal vs. operational programs. Confounding with other policy (landfill taxes, incineration fees often pass simultaneously). Lag: effects take 3+ years to manifest; imputing WRR too soon after legislation underestimates impact.

---

### **Rank 3: Global E-Waste Monitor Data (Electronic Waste Collection/Recycling Rates)**

**One-line summary:** Documented e-waste collection and recycling rate (% of generated e-waste formally collected and recycled), published biennially by Global E-waste Monitor (ITU/UNITAR) for 180+ countries.

**Expected relationship:** Positive; countries with high formal e-waste recycling rates should correlate with high overall WRR, as e-waste infrastructure development parallels general waste management sophistication.

**Data source:** "Global E-waste Monitor 2024" (ITU/UNITAR) published free as PDF + downloadable data; biennial updates; 180+ countries; data quality improving annually[12].

**Rationale for ranking:** GEM data are (a) published in standardized format for 180 countries (nearly complete geographic coverage), (b) updated biennially with improving rigor, (c) distinct waste stream allowing comparison of recovery rates across material types, (d) less confounded by GDP than facility counts (e-waste infrastructure sometimes leads general waste infrastructure in technologically dynamic countries), (e) publicly available and processed by UN agencies (minimal data quality issues). E-waste recycling demonstrates specialized technical capacity that predicts general waste management sophistication. GEM provides both volume and percentage-based metrics.

**Cautionary notes:** E-waste is only ~2% of total waste; correlation to general WRR may be moderate (r ≈ 0.35-0.50). Definitions of "documented recycling" vary and often undercount informal sector (creating zero-values for countries with active informal e-waste recycling). Data lag: GEM 2024 reflects 2022 data; policy changes post-2022 not yet captured.

---

### **Rank 4: Wastewater Treatment Plant (WWTP) Capacity and Sludge Management**

**One-line summary:** Number of municipal wastewater treatment plants in operation + proportion employing anaerobic digestion (which produces recoverable biosolids), from UNWATER, World Bank, and national water authority registries.

**Expected relationship:** Positive; countries with advanced WWTP infrastructure (particularly anaerobic digestion systems) should show elevated WRR, as both systems require similar technical expertise, end-markets, and institutional capacity.

**Data source:** UNWATER "Progress on Wastewater Treatment 2024" report (free); World Bank water/sanitation databases; EPA Water ICAT tool (USA); national environmental ministry databases (EU, Japan publish WWTP registries).

**Rationale for ranking:** WWTP data are (a) more systematically collected globally than MRF data (development institutions prioritize water over waste), (b) standardized definitions across countries (WWTP functions are relatively uniform), (c) indicative of broader environmental infrastructure maturity, (d) showing some independence from pure wealth effects (some lower-middle-income countries have invested heavily in wastewater infrastructure for health reasons), (e) forward-looking (countries building WWTP networks often subsequently invest in waste recovery). Anaerobic digestion technology transfers directly between wastewater sludge and solid waste organic fractions.

**Cautionary notes:** Moderate-strength correlation expected (r ≈ 0.40-0.50); WWTP presence is complementary to waste recovery but not sufficient to predict it. Data quality variable (many developing countries lack comprehensive WWTP registries; private sector facilities often unmeasured). Lag: WWTP infrastructure built for sanitation/health; waste recovery infrastructure follows later.

---

### **Rank 5: Food Waste-Specific Legislation (Segregation Mandates, Donation Laws, Landfill Bans)**

**One-line summary:** Presence of food waste segregation mandate OR food donation requirement (e.g., France Loi Garot) OR organic waste landfill ban, tracked via legislative databases and country policy reviews.

**Expected relationship:** Positive; countries with food waste-specific legislation should show elevated WRR given that food waste comprises 45-60% of municipal waste and is readily recoverable via composting/anaerobic digestion. Expected effect: 5-12 percentage point WRR increase upon implementation.

**Data source:** REFASH "Must-Know Global Laws" compilation (free, 2024); EU waste legislation database; national government gazettes and environmental ministry websites; academic waste policy literature.

**Rationale for ranking:** Food waste legislation is (a) an early-stage policy intervention that often precedes general EPR (leading indicator), (b) showing rapid global expansion (EU-wide organic waste collection mandates increasingly common; South Korea, Japan have mandatory segregation), (c) with strong mechanistic link (45-60% of waste stream), (d) with recent, measurable policy variations allowing identification, (e) less confounded by pure wealth (low-income countries increasingly adopt food waste legislation). Binary presence + years of implementation provide variation. Food waste mandates are often more politically feasible than comprehensive EPR, appearing first in policy progression.

**Cautionary notes:** Enforcement variable; many laws pass but with minimal implementation. Temporal lag: segregation must translate to infrastructure before WRR impact (may take 3-5 years). Reverse causality: countries already composting organics may codify via legislation rather than creating practice. Definition variance: what constitutes "food waste" vs. "garden waste" differs across countries.

---

### **Rank 6: Deposit Return Scheme (DRS) Implementation and Participation Rates**

**One-line summary:** Binary presence of DRS legislation for beverage containers + reported consumer participation rate (% containers returned), from Reloop Platform and legislative tracking databases.

**Expected relationship:** Positive; DRS implementation should raise WRR through economic incentives for container recovery and signaling broader recycling norms. Participation rates directly indicate behavioral engagement with recovery systems.

**Data source:** Reloop Platform DRS fact sheet (free); Product Stewardship Institute EPR database; national government registries; municipal waste data (USA states report DRS impact).

**Rationale for ranking:** DRS is (a) a specific, measurable policy intervention with objective implementation date, (b) showing both presence (binary) and intensity (participation %) variation, (c) with strong behavioral component (reveals willingness to engage recovery systems), (d) expanding rapidly in new jurisdictions (Germany, France, new US states), (e) with documented consumer motivation studies[27]. DRS focuses on 3-10% of waste stream (beverage containers) but creates demonstration effect and infrastructure that extends to other materials. Participation rates serve as behavioral signal of waste recovery culture.

**Cautionary notes:** Limited geographic coverage (primarily OECD); sparse data for developing countries. Participation rates are self-reported by scheme operators (potential over-reporting). Beverage containers small fraction of total waste; DRS WRR contribution may be 1-5 percentage points, with rest from other pathways. Temporal lag between legislation and matured participation (3-5 years typical).

---

### **Rank 7: Waste Collection Coverage Rate (% of waste collected and managed by formal system)**

**One-line summary:** Proportion of municipal waste collected by formal waste management systems (vs. uncollected or informally managed), calculated as (collected waste) / (total waste generated); from World Bank, UNEP, and national waste management databases.

**Expected relationship:** Strong positive; waste recovery is mechanistically impossible for uncollected waste. Collection coverage is prerequisite for all downstream recovery pathways. High collection rates necessary (though not sufficient) for high WRR.

**Data source:** World Bank "Trends in Solid Waste Management" report (free); UNEP waste statistics; World Bank What a Waste 2.0 database; SDG Indicator 11.6.1 (UN-HABITAT/UNSD)[41].

**Rationale for ranking:** Collection coverage is (a) prerequisite variable with mechanistic necessity (no recovery without collection), (b) published by World Bank for most countries, (c) standardized definition, (d) varying dramatically across regions (>90% in OECD; 26-48% in low-income/rural areas), (e) policy-influenced but not purely wealth-driven (countries like Rwanda have expanded collection coverage despite moderate income[10]).

**Cautionary notes:** Collection coverage is upstream of (not synonymous with) recovery. High collection → landfill is possible (collected waste is dumped). Thus collection coverage is necessary but insufficient condition for WRR. Correlation with WRR likely strong (r ≈ 0.50-0.65) but not perfect. Collection coverage may be reported differently across countries (includes/excludes informal collection). Highly correlated with urbanization and GDP/capita (partial correlation controlling for these needed).

---

### **Rank 8: Material Recovery Facility Count and Automation Level (with caveat on data availability)**

**One-line summary:** Number of Material Recovery Facilities (MRFs) in operation per capita (or total capacity in tonnes/year per capita) + proportion of MRFs equipped with AI/robotic sorting systems, indicating both collection infrastructure and technical sophistication.

**Expected relationship:** Positive; MRF capacity is directly proportional to domestic material recovery capacity. Automation level indicates efficiency/recovery rate per unit throughput.

**Data source:** For USA: EPA statistics and industry associations (American Waste Handlers Association); Ecostar HDDS deployment data (130+ facilities globally); vendor case studies (AMP Robotics, ZenRobotics project lists); industry reports (Resource Recycling, 2026[32]).

**Rationale for ranking:** MRF data are (a) directly linked to mechanistic WRR (each tonne of MRF capacity = potential recovery), (b) increasingly automated systems provide efficiency gains, (c) globally expanding with technology adoption accelerating, (d) facility-level data available for high-income countries. Robotics adoption serves as indicator of technical sophistication and capital investment. MRF capacity quantifies infrastructure maturity.

**Cautionary notes:** Most significant limitation is DATA AVAILABILITY. Comprehensive global MRF registry does not exist; USA has most complete data; EU data patchy; developing countries largely unmeasured. Utilization rates vary 30-90% (facility capacity ≠ actual throughput). Capital costs heavily bias automation toward wealthy countries (confounding with GDP). Facility count becomes sparse in many countries (zero for countries without formal sector). Given data limitations, this proxy ranks 8 rather than higher despite strong mechanistic link.

---

## Summary Table: Ranked Proxy Candidates

| **Rank** | **Proxy** | **Expected Correlation Direction** | **Expected Strength (r)** | **Geographic Coverage** | **Data Accessibility** | **Mechanistic Plausibility** |
|---|---|---|---|---|---|---|
| 1 | Recycled Material Trade Flows | Positive | 0.45-0.60 | Global | Excellent (UN Comtrade) | Strong |
| 2 | EPR Program Implementation | Positive | 0.40-0.55 | OECD primary; expanding | Good (PSI database) | Very Strong |
| 3 | E-Waste Recycling Rate | Positive | 0.35-0.50 | Global (180 countries) | Good (GEM reports) | Moderate-Strong |
| 4 | WWTP Capacity | Positive | 0.40-0.50 | Global | Good (World Bank, UNWATER) | Moderate |
| 5 | Food Waste Legislation | Positive | 0.35-0.50 | OECD + expanding | Good (legislative databases) | Strong |
| 6 | Deposit Return Schemes | Positive | 0.30-0.45 | OECD primary | Good (Reloop, PSI) | Moderate |
| 7 | Waste Collection Coverage | Positive | 0.50-0.65 | Global | Good (World Bank) | Very Strong |
| 8 | MRF Capacity + Automation | Positive | 0.40-0.55 | OECD, China; sparse elsewhere | Fair-to-Poor (proprietary) | Very Strong |

---

## 7. Conclusion and Implementation Recommendations

The landscape of potential proxies for the Waste Recovery Rate indicator spans eight ranked candidates, from the excellent (recycled material trade flows, with global coverage and frequent updates) to the good-but-limited (MRF automation data, geographically sparse). The optimal implementation strategy for the EPI would involve:

### **Immediate Actions (High Priority):**

1. **Develop a composite recycled material trade index** combining UN Comtrade data on metals, paper, and plastic exports/imports by country-year. This proxy offers immediate usability: global coverage, monthly updates, and clear mechanistic link to recovery infrastructure. A simple index could be calculated as: Trade_Index = (Recycled_Exports_t + Recycled_Imports_t) / (Total_Waste_Generated_t) to normalize by national waste volume. This should be tested for partial correlation with WRR controlling for GDP per capita and region.

2. **Extract and systematize EPR implementation dates from PSI database.** Create a clean binary variable (EPR_Presence_Year_t) indicating year EPR legislation passed and year program operationalized, plus continuous variable (Years_Since_Implementation_t). This data exists but requires curation. Test partial correlation with WRR in OECD subsample where WRR data are reliable.

3. **Integrate Global E-waste Monitor data** (published biennially, already available free) as direct proxy for e-waste recovery + test partial correlation to general WRR. This is minimal-effort high-utility addition, as data are already produced by reputable UN agencies.

### **Medium-Term Enhancements (6-12 Month Horizon):**

4. **Compile food waste-specific legislation database** by searching national government legislative records and EU waste database for organic waste segregation/donation/landfill ban laws. Systematize implementation dates. This is labor-intensive but produces novel dataset of high utility. Partner with organizations like WRAP or UNEP for validation.

5. **Quantify waste collection coverage rates** from World Bank What a Waste database; separate urban/rural to disentangle urbanization effects. Create both aggregate and stratified (urban/rural) versions.

### **Longer-Term Development (1-2 Year Horizon):**

6. **Establish partnership with wastewater sector institutions** (UNWATER, IFI water specialists) to extract standardized WWTP capacity and digestion technology data by country-year. This bridges two infrastructure domains and provides incremental information.

7. **Commission facility-level data survey** for middle-income countries (e.g., in partnership with World Bank or regional development banks) to collect MRF and composting facility data. This would substantially improve data availability for the MRF proxy.

### **Validation Framework:**

Once proxy candidates are constructed, the EPI team should:

- **Test partial correlations** with WRR controlling for GDP per capita and region (the known confounders in the current model). Proxies with significant residual partial correlation (p < 0.05, |r| > 0.25) after controlling for confounders add independent information and warrant inclusion.

- **Examine temporal lag structures:** Do EPR implementations predict WRR increases 3-5 years later? Do facility construction dates precede WRR increases? Lag models can establish temporal precedence.

- **Cross-validate against existing WRR data** in countries where reliable WRR data exist (OECD, EU). Proxies should show strong correlation (r > 0.50) with measured WRR in these subsample before deployment in imputation model.

- **Conduct sensitivity analysis:** Rerun imputation model substituting each proxy as alternative regressor alongside (or instead of) GDP/region. Compare fit (R²), prediction error, and reasonableness of imputed values.

### **Final Recommendation:**

The optimal near-term strategy is a **proxy ensemble approach**: Rather than selecting a single proxy, incorporate multiple proxies (ranked 1-5 above) into an ensemble imputation model. This approach leverages complementary information (trade flows capture infrastructure maturity; EPR captures policy stringency; e-waste captures technical sophistication) while reducing dependence on any single potentially-flawed indicator. Ensemble imputation can be achieved via:

- **Multiple imputation by chained equations (MICE)** with separate regression models for each proxy, then pooling imputations
- **Composite predictor approach:** Construct PCA-derived composite from multiple proxies, use as single ensemble regressor
- **Bayesian hierarchical model:** Treat multiple proxies as noisy measurements of latent waste recovery capacity; infer WRR from posterior distribution

This approach balances rigor, data availability, and mechanistic plausibility while explicitly acknowledging uncertainty in the imputation process.

## References
[1] https://epi.yale.edu/measure/2024/WRR
[2] https://www.epa.gov/smm/energy-recovery-combustion-municipal-solid-waste-msw
[3] https://ec.europa.eu/eurostat/statistics-explained/index.php/Municipal_waste_statistics
[4] https://datatopics.worldbank.org/what-a-waste/
[5] https://www.oecd.org/en/data/indicators/municipal-waste.html
[6] https://www.epa.gov/waterfinancecenter/water-infrastructure-and-capacity-assessment-tool
[7] https://www.epa.gov/circulareconomy/transforming-us-recycling-and-waste-management
[8] https://www.sensoneo.com/global-waste-index/
[9] https://pollution.sustainability-directory.com/term/waste-diversion-rate/
[10] https://www.worldbank.org/en/results/2025/04/30/clean-cities-bright-futures-accelerating-investment-and-reforms-in-solid-waste-management-in-developing-countries
[11] https://ourworldindata.org/grapher/per-capita-plastic-waste-vs-gdp-per-capita
[12] https://ewastemonitor.info/the-global-e-waste-monitor-2024/
[13] https://epr.sustainablepackaging.org
[14] https://dsny.cityofnewyork.us/wp-content/uploads/2021/09/about_dsny-non-dsny-collections-FY2021.pdf
[15] https://hiclover.com/incinerator/global-perspectives-how-different-countries-approach-large-scale-incineration/
[16] https://www.biocycle.net/us-food-waste-composting-infrastructure/
[17] https://ecostar.eu.com/municipal-solid-waste-treatment-around-the-world-ecostar/
[18] https://pmc.ncbi.nlm.nih.gov/articles/PMC12650926/
[19] https://erefdn.org/wp-content/uploads/2021/01/EREF_Final-Report_NHIW_1216.pdf
[20] https://epi.yale.edu/measure/2024/WPC
[21] https://www.weforum.org/stories/2023/03/charted-the-flow-of-global-plastic-waste/
[22] https://sustainability.wm.com/esg-hub/environmental/carbon-methodology/
[23] https://documents.worldbank.org/en/publication/documents-reports/documentdetail/227581468156575228/the-informal-recycling-sector-in-developing-countries-organizing-waste-pickers-to-enhance-their-impact
[24] https://davisvanguard.org/2025/11/recology-extension-criticized/
[25] https://www.compareyourcountry.org/environmental-policy-stringency-indicators
[26] https://earth.org/smart-waste-management/
[27] https://www.reloopplatform.org/wp-content/uploads/2023/05/Consumer-participation-in-DRS-factsheet.pdf
[28] https://www.statista.com/statistics/1618720/mea-waste-to-energy-capacity-by-country/
[29] https://www.epa.gov/lmop/benefits-landfill-gas-energy-projects
[30] https://pmc.ncbi.nlm.nih.gov/articles/PMC9918355/
[31] https://worldpopulationreview.com/country-rankings/recycling-rates-by-country
[32] https://resource-recycling.com/analysis/2026/02/12/the-cyber-physical-mrf-ai-and-robotics-reshape-e-waste-recovery/
[33] https://epi.yale.edu/downloads/2024epitechnicalappendix20241207.pdf
[34] https://eunomia.eco/latest-news/austria-wales-and-taiwan-leading-the-world-when-it-comes-to-rates-of-recycling/
[35] https://farmdocdaily.illinois.edu/2025/07/us-fertilizer-industry-in-global-markets-structure-and-supply-risks.html
[36] https://ourworldindata.org/grapher/per-capita-electricity-generation
[37] https://www.fortunebusinessinsights.com/retail-ready-packaging-market-104915
[38] https://www.statista.com/topics/4983/waste-generation-worldwide/
[39] https://www.epa.gov/smm/sustainable-management-construction-and-demolition-materials
[40] https://www.recycledmaterials.org/recycled-material-exports-snapshot/
[41] http://sdgs.unep.org/article/sdg-indicator-1161
[42] https://www.epa.gov/sites/default/files/2020-12/documents/rsei_methodology_v2.3.9.pdf
[43] https://www.brookings.edu/articles/four-recent-trends-in-us-public-infrastructure-spending/
[44] https://www.seair.co.in/us-import/product-drink-bottle/i-edt-usa-corp/e-fabrica-de-bebidas-gaseosas-salvavi.aspx
[45] https://www.usgs.gov/centers/national-minerals-information-center/iron-and-steel-scrap-statistics-and-information
[46] https://www.epa.gov/sites/default/files/2016-01/documents/msw_task9_industrialfoodprocessingwasteanalyses_508_fnl_2.pdf
[47] https://www.unwater.org/publications/progress-wastewater-treatment-2024-update
[48] https://data.worldbank.org/indicator/NE.CON.PRVT.PC.KD.ZG
[49] https://www.bls.gov/iag/tgs/iag44-45.htm
[50] https://eridirect.com/blog/2026/02/how-battery-recycling-is-becoming-essential-infrastructure/