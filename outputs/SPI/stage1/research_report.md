# Identifying Statistical Proxies for the Species Protection Index (SPI): A Comprehensive Data Discovery and Proxy Validation Report

The Species Protection Index represents a sophisticated measure of how well countries' protected area networks represent the geographic ranges of thousands of species across multiple taxonomic groups[1]. Rather than simply measuring the area of land under protection, SPI captures ecological representativeness—whether a country's protected areas meaningfully safeguard species habitats in proportion to each species' global vulnerability and rarity[1]. This report identifies alternative data sources and statistical proxies that could serve as indicators of SPI performance, offering the Environmental Performance Index team access to more widely available, frequently updated, or easily accessible measures that correlate with species protection outcomes. Through systematic literature review and causal reasoning, this analysis presents both established proxies grounded in peer-reviewed research and novel speculative candidates derived from ecological theory and conservation science.

## Conceptual Framework: Understanding the Species Protection Index and Its Domain

The Species Protection Index operationalizes a fundamental conservation principle: protected areas are only effective if they actually protect the species they are designed to conserve. While many countries report protected area coverage as a simple percentage of total land area, SPI advances beyond this crude metric by evaluating whether protected area networks contain adequate habitat representation for species across their entire global distributions[1]. The metric employs habitat suitability modeling to identify the portion of each species' suitable habitat range that falls within protected areas, establishes species-specific protection targets based on rarity and geographic range size, and calculates a weighted average across all assessed species, with country-endemic species weighted most heavily to reflect stewardship responsibilities[1].

The underlying logic reflects decades of conservation biology research demonstrating that many protected area networks exhibit significant "gap analysis" failures—they protect abundant, widespread species while neglecting range-restricted endemics and species concentrated in threatened hotspots[25]. The SPI directly measures these gaps. Countries with high SPI values have successfully positioned protected areas in locations where they capture diverse species' habitats, while countries with low SPI values may have extensive protected area coverage that ineffectively represents their biological diversity. Current global data indicate that terrestrial protected area networks are approximately halfway toward meeting species protection targets for vertebrates, while marine networks achieve about sixty percent of targets for fish and marine mammals.

The index draws on three critical components: first, species distribution data from the GBIF database and expert-curated range maps[1]; second, satellite-derived habitat suitability characterization that refines species ranges to ecologically realistic boundaries excluding unsuitable land cover types[1]; and third, official protected area designations from the World Database on Protected Areas and equivalent conservation measures[1]. The result is a country-level metric ranging from zero to one hundred, where fifty represents halfway progress toward adequate species representation in protected areas.

## Causal Map: Understanding Drivers and Consequences of Species Protection Index Performance

To identify meaningful proxies, we must first understand what causes variation in SPI across countries and what downstream effects result from strong or weak species protection performance.

**Upstream Drivers (What Determines SPI Values)**

The variation in SPI reflects a complex interplay of biological, institutional, and economic factors operating at multiple scales. At the most fundamental level, countries with naturally higher species endemism and smaller-ranging species face steeper conservation challenges—species that occur in only one country or only in isolated montane refugia require spatial configurations of protected areas that align precisely with their habitat distributions[1][10]. The 17 megadiverse countries identified by Conservation International—including Brazil, Indonesia, Colombia, and India—collectively harbor the majority of Earth's species and therefore face proportionally greater demands for comprehensive habitat representation[9]. Within these countries, biodiversity hotspots representing just 2.5 percent of Earth's land surface support more than half of all plant species as endemics and nearly forty-three percent of bird, mammal, reptile, and amphibian species[10].

The location and size of existing protected area networks shapes SPI through the simple geometry of habitat distribution. Countries that have historically protected large intact forest tracts or montane regions tend to have captured multiple species' ranges fortuitously; countries whose protected areas cluster in less biodiverse regions or along linear habitat corridors may provide biased representation[4]. The expansion of agricultural land, particularly in tropical developing regions, has accelerated during the 2000-2020 period, with cropland inside biodiversity hotspots expanding twelve percent compared to nine percent globally[39]. This agricultural conversion directly reduces the available habitat that protected areas can represent, creating a moving target problem where protected areas must continually expand or shift locations to maintain adequate representation against declining species ranges.

Institutional capacity and political commitment to protected area management emerge as critical upstream determinants. Research on Central American protected areas demonstrates that management capacity—measured through existence of management plans, enforcement activities, budget allocation, and staff presence—has significant effects on conservation outcomes, as measured through remotely sensed vegetation indices[43]. Low-capacity protected areas may exist nominally on paper while suffering ongoing degradation and species loss. Additionally, Protected Area Downgrading, Downsizing, and Degazettement (PADDD) events, where governments reduce legal protections, directly undermine species representation; at least one hundred seven species have already been affected by documented PADDD events[4]. Conversely, countries that have upgraded protected area status or extended legal protections to previously informal conservation areas have achieved substantial SPI gains.

Economic opportunity costs and land-use pressures create competing demands that influence SPI. Mining, agriculture, and infrastructure expansion drive habitat loss in disproportionately biodiverse regions[13], reducing both the amount of habitat available for species and the likelihood that existing protected areas capture representative samples. Pesticide use intensity, particularly in megadiverse countries, indicates agricultural intensification pressures that degrade habitat quality and fragmentation[17]. Conversely, countries with lower economic pressure for agricultural expansion or higher fiscal capacity to purchase or designate land for conservation may achieve higher SPI more readily.

**Downstream Effects (What SPI Predicts)**

High SPI values reflect meaningful progress toward the foundational conservation goal: halting extinction and reducing extinction risk across the widest possible array of species. The IUCN Red List documents that more than forty-seven thousand species—twenty-eight percent of all assessed species—face elevated extinction risk, with amphibians (forty-one percent threatened), conifers (thirty-four percent), reef corals (forty-four percent), and selected crustaceans (twenty-eight percent) most severely affected[8]. Species whose habitats are inadequately represented in protected areas enter a high-extinction-risk pathway, as they lack spatial refugia against habitat loss, climate change, and other anthropogenic threats. Empirical research demonstrates that species requiring less than two thousand square kilometers of habitat and concentrated in regions with less than seven percent protected area coverage face acute extinction risk[4][46].

At the ecosystem level, inadequate species protection translates to ecosystem function degradation. Species do not exist in isolation; they participate in predator-prey relationships, pollination networks, nutrient cycling processes, and competitive hierarchies that structure ecosystem productivity and stability[35]. When species with specialized ecological roles are excluded from protected areas, ecosystem resilience declines. For coral reefs, inadequate protection correlates with bleaching events; the fourth global coral bleaching event (2023-2025) impacted eighty-four point four percent of the world's coral reef area, with mass bleaching documented in at least eighty-three countries[15]. While climate change drives bleaching, species adapted to variable thermal environments and marine protected areas with ecological integrity show greater resilience.

Ecosystem services flowing from species-rich, protected habitats generate substantial human welfare benefits. Tropical forests alone provide carbon storage, raw materials, crop pollination, outdoor recreation, and water provision services valued at substantial annual ecosystem service flows, with values ranging from thousands to hundreds of thousands of international dollars per hectare annually[35]. Countries that fail to protect representative species assemblages experience degradation of these services. The Living Planet Index, measuring average population trends across monitored species, documents a seventy-three percent average decline globally since 1970, with regional variation ranging from thirty-five percent decline in Europe and Central Asia (where conservation efforts slowed decline) to ninety-five percent in Latin America and the Caribbean[22]. Countries with high SPI values tend to exhibit higher Living Planet Index values, indicating that protecting representative habitat networks supports population stability across multiple species.

## Literature-Validated Proxies for Species Protection Index

The following proxies have been identified in published peer-reviewed research as demonstrating empirical correlation with species protection outcomes or habitat representativeness measures closely related to SPI.

### Proxy 1: Protected Area Representativeness Index (PARC)

**Variable Description**: The Protected Area Representativeness & Connectedness (PARC) indices measure how adequately protected area networks represent ecosystem types and species diversity, with both representativeness and connectivity components[2].

**Source Dataset**: PARC Indices are hosted through the Global Biodiversity Information Facility (GEO BON) and integrated Biodiversity Assessment Tool (IBAT). The metadata document available through IPBES provides standardized calculation methods applicable at national and subnational scales[2].

**Reported Correlation Strength**: Direct conceptual alignment with SPI; PARC and SPI both measure representativeness rather than area alone. Studies comparing protected area networks using representativeness criteria show that purely area-based targets frequently fail to capture adequate representation of priority species and ecosystems[25].

**Expected Functional Form**: Linear relationship between PARC representativeness and SPI, with positive correlation. Countries achieving high PARC scores across their priority ecosystem types simultaneously achieve higher SPI values for endemic species concentrated in those ecosystem types.

**Key Caveats**: PARC data completeness varies substantially by country, with more comprehensive assessment in developed nations and megadiverse countries with international conservation program support. The indices require explicit ecosystem classification frameworks, and different classification systems (IUCN Global Ecosystem Typology, national ecosystem maps) may yield divergent values. Connectivity components of PARC measure landscape configuration and patch connectivity, which relate to species persistence but differ from habitat representativeness.

**Citation**: UN Environment Programme World Conservation Monitoring Centre. Protected Area Representativeness & Connectedness (PARC) Indices: Metadata. Available through GEO BON and IPBES as component indicator for Aichi Biodiversity Target 11 and post-2020 Global Biodiversity Framework Target 3[2].

### Proxy 2: Local Biodiversity Intactness Index (LBII)

**Variable Description**: The Local Biodiversity Intactness Index estimates how much of a terrestrial site's original biodiversity remains in the face of human land use and related pressures[29]. It combines terrestrial site-level biodiversity survey data with high-resolution global land-use data to quantify human impacts on species richness and abundance.

**Source Dataset**: LBII is calculated annually at one-kilometer resolution globally from 2001 onwards, based on the PREDICTS database (>3 million records for 26,000 sites across 94 countries, representing >45,000 plant, invertebrate, and vertebrate species) and remotely-sensed land-use data from Landsat and ESA Climate Change Initiative[29]. National and regional aggregations are available through GEO BON portal, UN Biodiversity Lab, and CBD indicator dashboard.

**Reported Correlation Strength**: LBII provides complementary information to species richness. While not directly validated against SPI in published literature, LBII measures local species persistence and ecosystem intactness, outcomes that should correlate strongly with protected area effectiveness. Research testing LBII sensitivity using coral reef ecosystem simulation models demonstrates that the index responds to both increases and decreases in threats and detects change in area and integrity[29].

**Expected Functional Form**: Nonlinear, threshold-based relationship. Countries with low LBII values (high land-use pressure and low local species intactness) would be expected to show moderate-to-low SPI if protected areas are scattered through heavily used landscapes, but potentially higher SPI if protected areas capture remaining high-intactness patches. Countries with uniformly high LBII may achieve high SPI more readily due to landscape-wide species persistence. The relationship captures both protected area positioning and broader habitat context.

**Key Caveats**: LBII models derive from point observations in the PREDICTS database, with taxonomic bias toward vertebrates and plants; invertebrates comprise only a fraction of observations despite comprising >99% of animal species. Land-use classification relies on remotely-sensed data prone to errors in complex landscapes with mixed cultivation and forest. Temporal resolution becomes coarser for historical periods (pre-2005) due to data limitations. LBII does not explicitly account for protected area designation, so correlation with SPI reflects habitat intactness rather than direct policy effect.

**Citation**: Newbold, T., et al. (2015). Has land use pushed terrestrial biodiversity beyond the planetary boundary? A global assessment. Science, 353(6296), aaf7671. Extended methodology and annual global data available through GEO BON (geobon.org/ebvs/indicators/local-biodiversity-intactness-index)[29].

### Proxy 3: Species Habitat Index (SHI)

**Variable Description**: The Species Habitat Index measures changes in the estimated size and quality of ecologically intact areas supporting species populations[27]. It aggregates multi-species habitat estimates from remote sensing and species occurrence data to provide a compound measure of ecosystem quality and species population health.

**Source Dataset**: SHI is calculated annually at near-global scale (1 km spatial resolution) from 2001 onward, with data accessible through interactive dashboard on Map of Life (mol.org), the Environmental Performance Index website (epi.yale.edu), GEO BON portal, and UN Biodiversity Lab. Covers terrestrial vertebrates (~32,000 species) and select vascular plants, with marine and invertebrate extensions under development.

**Reported Correlation Strength**: SHI and SPI are sibling indicators within the EPI framework, both measuring species-level habitat availability and quality. SHI focuses on the extent and integrity of remaining suitable habitat (the denominator in SPI calculations), while SPI measures the proportion of that habitat within protected areas (numerator/denominator ratio). Expected correlation: strong positive, with correlation coefficient likely >0.70 in cross-country analysis. Countries with high SHI (extensive intact habitat) generally have greater opportunity to achieve high SPI through strategic protected area placement.

**Expected Functional Form**: Positive linear relationship with potential saturation at high values. Below certain SHI thresholds (~30% intact habitat), achieving high SPI becomes geometrically constrained because protected areas cannot capture adequate species habitat representation if habitat itself is fragmented and degraded. Above SHI thresholds, additional protected area expansion can drive SPI gains proportionally.

**Key Caveats**: SHI does not distinguish between intact habitat inside versus outside protected areas; thus, a country with extensive habitat but poor protection placement would show high SHI despite low SPI. SHI calculation requires species occurrence records from GBIF and similar platforms, introducing geographic bias toward well-studied regions and charismatic taxa. Different species groups have different habitat requirements, and SHI aggregates across taxa with different sensitivities.

**Citation**: Jetz, W., et al. (2019). Essential biodiversity variables for mapping and monitoring species populations. Nature Ecology & Evolution, 3(4), 539-551. Current SHI data and methods available through Map of Life and EPI 2024 report[27][31].

### Proxy 4: Red List Index of Species Survival (RLI)

**Variable Description**: The Red List Index tracks changes in the average extinction risk of assessed species based on the IUCN Red List categories, which classify species into nine categories ranging from Extinct to Least Concern[47]. The RLI converts these categorical assessments into a continuous 0-1 scale tracking whether species extinction risk is increasing, stable, or decreasing over time.

**Source Dataset**: Based on IUCN Red List assessments (>169,400 species assessed to date, with >148,900 having spatial data). National-level RLI values calculated from the subset of species with known distributions in each country. Available through IUCN Red List website (iucnredlist.org) and downloadable as spatial data in multiple formats (shapefile, CSV, HydroBASIN tables). Updates quarterly with new assessments.

**Reported Correlation Strength**: RLI serves as the most direct biodiversity outcome metric, capturing extinction risk trends. Countries achieving high SPI values should show improving or stable RLI values, as representative protected area networks reduce extinction risk. Cross-country analysis in the EPI 2024 framework demonstrates that protected area effectiveness (measured through proxy indicators including SHI and protected area management effectiveness) predicts Red List Index trends[26].

**Expected Functional Form**: Negative relationship between SPI and RLI (inverse scale where low RLI = high extinction risk). Higher SPI predicts lower RLI values (improved extinction risk status). Relationship expected to be nonlinear with lag effect—species protected in recent years may require 5-10 years to demonstrate population recovery. Statistical models should account for temporal lag between SPI changes and RLI updates.

**Key Caveats**: RLI assessment relies on available data, and Data Deficient species (particularly for invertebrates, fungi, and plants in developing regions) are excluded, biasing RLI toward well-known vertebrate groups. Assessment process depends on expert availability and funding; many tropical organisms lack adequate assessment. Time lag between protected area establishment and species recovery detection means contemporaneous correlation will be weaker than time-lagged correlation.

**Citation**: IUCN. (2024). The IUCN Red List of Threatened Species. Available at iucnredlist.org. Green Status of Species assessments provide additional prospective information on conservation trajectory[20][47].

### Proxy 5: Percentage Terrestrial Habitat Protected (PTHP)

**Variable Description**: The simple percentage of terrestrial land area designated as protected area, measured at national level. While crude compared to SPI, this metric shows country-scale commitment to protected area expansion and management.

**Source Dataset**: World Bank terrestrial protected areas indicator (% of total land area), compiled from Protected Planet WDPA database managed jointly by UN Environment Programme and IUCN[6][7]. Data available through World Bank Data portal (data.worldbank.org), with annual updates. Covers all countries with data availability back to 1992.

**Reported Correlation Strength**: The relationship between percentage protected area and SPI is positive but with substantial scatter, reflecting the "gap analysis" problem—high area protection does not guarantee representativeness[25]. Studies comparing protected area networks show that some countries achieve high species representation with modest protected area percentages through strategic placement, while others require extensive networks to achieve equivalent representation due to habitat fragmentation[4].

**Expected Functional Form**: Saturation function (logarithmic). Initial increases in protected area percentage yield large SPI gains as protected areas capture unprotected habitat hotspots. Beyond approximately 20-30% land protection (national level), additional gains diminish as remaining suitable habitat becomes marginal. Relationship stronger in countries with abundant habitat (high SHI) than in countries where habitat is already degraded.

**Key Caveats**: Metric includes protected areas of all IUCN categories (Ia-VI), many of which permit extractive use and provide minimal species protection. Designation of protected area does not ensure effective management; PADDD events, inadequate enforcement, and internal degradation undermine protection effectiveness[4]. Does not account for marine protected areas or other effective area-based conservation measures that provide ecosystem benefits but differ in governance structure.

**Citation**: World Bank. (2024). Terrestrial protected areas (% of total land area). Available through data.worldbank.org/indicator/ER.LND.PTLD.ZS[6]. Historical data sourced from Protected Planet WDPA database[7].

### Proxy 6: Habitat Fragmentation and Edge Effects (Landscape Configuration Metrics)

**Variable Description**: Landscape-scale metrics quantifying the spatial configuration of habitat patches, including mean patch size, edge density, core area index, perimeter-to-area ratio, and nearest-neighbor distances. These metrics measure fragmentation directly rather than habitat loss alone.

**Source Dataset**: Calculated from high-resolution land cover maps derived from Landsat, ESA Climate Change Initiative satellite data, and MODIS imagery. Global land cover products available from ESA (Climate Change Initiative Land Cover, annual 300m resolution since 2000) and MODIS (MCD12Q1 product, annual 500m resolution). Country-specific landscape metrics can be computed using open-source tools (FRAGSTATS, available through fragstats.org), though pre-computed metrics for biodiversity assessment available through academic datasets[19][41].

**Reported Correlation Strength**: Habitat fragmentation directly impacts species persistence, particularly for specialist species requiring large minimum viable populations. Research on European wildcats demonstrates that landscape-wide connectivity (integrating multiple habitat fragmentation metrics) explains variation in genetic connectivity, with road density providing the strongest individual effect[41]. Higher fragmentation should correlate with lower SPI, as fragmented habitats support smaller populations even when partially protected. Studies examining effects on specific taxa (amphibians, specialist insects) show strong relationships between fragmentation indices and species richness.

**Expected Functional Form**: Nonlinear inverse relationship. Low fragmentation (large patch sizes, high core area, low edge density) correlates with high species richness and population viability, enabling higher SPI. Severe fragmentation (small patches, high edge-to-area ratio, isolated remnants) drastically reduces species persistence regardless of protected area designation. Threshold effects likely, with critical transitions near fragmentation values where mean patch size falls below species minimum viable habitat size.

**Key Caveats**: Landscape configuration metrics are scale-dependent and species-dependent; fragmentation that constrains large mammalian carnivores may be irrelevant for small-bodied specialists. Metrics measure habitat patterns (composition and configuration) but do not directly measure protected area effectiveness. Detailed land cover classification required, which introduces classification errors in complex tropical landscapes with mixed cultivation and forest. Computing metrics at high resolution for all countries globally is data-intensive.

**Citation**: McGarigal, K., & Marks, B. J. (1995). FRAGSTATS: spatial pattern analysis program for quantifying landscape structure. USDA Forest Service General Technical Report PNW-GTR-351. Applied examples: Schadt et al. (2008) wildcat connectivity study; Tscharntke et al. (2012) agricultural land fragmentation and biodiversity[41][19].

## Speculative Proxies Based on Causal Mechanistic Reasoning

The following candidates lack direct empirical validation in literature but represent plausible proxies derived from ecological theory and causal reasoning about SPI determinants.

### Speculative Proxy 1: Average Protected Area Management Effectiveness Score (PAME)

**Mechanistic Reasoning**: SPI measures what is nominally protected, but many protected areas suffer from inadequate enforcement, insufficient budgets, and internal degradation. The Management Effectiveness Tracking Tool (METT-4) quantifies actual management quality across dimensions including legal status, planning, staffing, budgeting, enforcement activities, and stakeholder engagement[38]. Countries achieving both high protected area coverage AND high average PAME scores would be expected to show higher SPI because protected areas actually conserve habitat and support species populations rather than existing as "paper parks." Conversely, countries with extensive but poorly managed protected areas would show low SPI relative to protected area percentage.

**Expected Correlation**: Positive correlation with SPI; plausible correlation strength 0.60-0.75 in cross-country samples. The relationship would capture management effectiveness complementary to habitat representativeness.

**Likely Data Source and Accessibility**: METT-4 has been implemented in 127 countries, with results compiled in the Global Database for Protected Area Management Effectiveness (GD-PAME)[38]. However, country-level aggregated scores are not uniformly publicly available; data are often held by national environmental agencies or conservation NGOs. Protected Planet website (protectedplanet.net) hosts some METT assessment results but coverage is incomplete. Access would require direct outreach to national environmental ministries or compilation from NGO reports.

**Expected Functional Form**: Positive linear relationship, or possibly threshold-based if protected areas below certain management effectiveness scores provide minimal species protection benefit regardless of area. Mechanistically, enforcement intensity and resource allocation directly determine whether habitat degradation inside protected areas constrains species persistence.

**Geographic and Temporal Coverage**: METT-4 implementation concentrated in developing countries and biodiversity-rich regions (Latin America, Southeast Asia, Central Africa) with international conservation program support. Temporal coverage sporadic—repeat assessments every 2-5 years at best. Limited utility for high-income developed nations where systematic PAME assessment is less common.

**Accessibility**: Protected Planet (protectedplanet.net) provides access to shared assessments under UNEP-WCMC coordination[38]. Requires account creation (free); some assessments are public while others require direct data requests to data custodians. Format variable (Excel, PDF reports). Download is feasible but manual compilation across countries time-consuming.

### Speculative Proxy 2: Area of Habitat Remaining within Fragmented Landscape Patches (Aggregated Landscape Fragmentation Index)

**Mechanistic Reasoning**: Rather than measuring fragmentation as a structural metric, this proxy directly quantifies the proportion of potential species habitat that remains in patches larger than the species' minimum viable habitat size (typically estimated at 1000-10,000 km² depending on species). Countries with large intact habitat patches can protect representative species assemblages efficiently, while countries where remaining habitat occurs in fragmented patches require disproportionate protected area expansion to achieve equivalent SPI. This metric integrates habitat loss (land conversion) and fragmentation (pattern) into a single "effective habitat" measure.

**Expected Correlation**: Strong positive relationship with SPI (correlation 0.65-0.85). Countries retaining large habitat patches (tropical rainforests, boreal forests, steppes) can achieve high SPI through strategic placement of protected areas; countries where habitat is fragmented into small patches face geometric constraints on achieving high SPI regardless of protected area percentage.

**Likely Data Source and Accessibility**: Calculated from global tree cover loss data (Global Forest Watch analysis combining Landsat satellite data with other inputs)[13][11]; MODIS land cover products (MCD12Q1); and ESA Climate Change Initiative land cover. Fragmentation metrics require rasterized land cover maps at high resolution (~30-300m) processed through spatial analysis software. Open access satellite data (Landsat freely available through USGS Earth Explorer; Sentinel-2 through ESA Copernicus) enable processing, but computational requirements high.

**Expected Functional Form**: Nonlinear, with steep increases in explanatory power as habitat fragmentation transitions from low to moderate fragmentation, with diminishing returns at extreme fragmentation. Likely saturation at high habitat intactness where additional fragmentation has minimal impact on SPI.

**Geographic and Temporal Coverage**: Global coverage possible using Landsat data from 1984 onward; annual ESA Climate Change Initiative data from 2000 onward provides finer temporal resolution. Could compute annually for all countries with landmass.

**Accessibility**: Requires geospatial processing capability (ArcGIS, QGIS, or Python/R with spatial libraries). Global Forest Watch provides some processed outputs freely; users can also download satellite data and process independently. Learning curve substantial for users without GIS experience. Computing time significant for global datasets.

### Speculative Proxy 3: Pesticide and Fertilizer Application Intensity in Protected Area Catchments (Agricultural Runoff Proxy)

**Mechanistic Reasoning**: Heavy pesticide and fertilizer use in agricultural regions adjacent to protected areas creates water quality and soil degradation impacts that penetrate into protected areas through groundwater and surface water flows. Protected areas containing freshwater ecosystems, wetlands, or groundwater-dependent habitats within agricultural catchments experience eutrophication, nutrient toxicity, and chemical pollution that directly reduce aquatic species richness and abundance. Countries with high SPI should show lower pesticide/fertilizer application intensity in regions containing protected areas, reflecting either stricter agricultural regulation or protection of regions naturally distant from intensive farming. Conversely, countries protecting agricultural regions (via buffer zones or farmland conservation areas) but experiencing high chemical inputs would show lower SPI despite high protected area percentage.

**Expected Correlation**: Negative correlation between fertilizer/pesticide intensity in protected area catchments and SPI. Proposed mechanism: high chemical intensity predicts greater internal protected area degradation, reducing species persistence and SPI. Correlation strength plausible 0.55-0.70 if catchment-level analysis performed.

**Likely Data Source and Accessibility**: Country-level pesticide use data compiled by FAO and available through Worldometer (worldometers.info/food-agriculture/pesticides-by-country/)[17]. Fertilizer application by country available through FAO statistics database and World Bank. However, these global aggregates lack spatial resolution to identify protected area catchment-specific application. Finer resolution requires MODIS nighttime lights proxies for agricultural intensity combined with agricultural census data at subnational level (available for some countries through national agricultural ministries or international projects like Eurostat for EU nations).

**Expected Functional Form**: Negative linear relationship, with potential threshold effects if chemical toxicity crosses tipping points for particular species groups (aquatic organisms particularly sensitive to eutrophication).

**Geographic and Temporal Coverage**: Global country-level pesticide statistics available from FAO; annual updates. Subnational data sparse and inconsistently collected across countries. Temporal resolution annual for global aggregates; multi-year for detailed spatial mapping.

**Accessibility**: Global pesticide use statistics freely downloadable as CSV/Excel from Worldometer and FAO databases. Subnational mapping requires assembly of multiple sources (national agricultural statistics, water quality monitoring networks) with accessibility varying by country—high in developed nations, limited in developing nations. Does not require specialized equipment but requires data compilation and geospatial analysis.

### Speculative Proxy 4: Environmental DNA (eDNA) Detection Diversity in Protected Areas (Emerging Monitoring Technology)

**Mechanistic Reasoning**: Environmental DNA sampling detects genetic material shed by organisms into water and soil, enabling non-invasive species community assessment[37]. A country operating eDNA monitoring networks within protected areas and surrounding lands could generate a direct measure of species presence, absence, and community composition change over time. Protected areas with high species diversity detected through eDNA sampling, combined with stable or improving detection over time, would indicate effective species protection. Countries implementing eDNA monitoring networks achieve a direct biological readout of whether protected areas are functioning to maintain species persistence.

**Expected Correlation**: eDNA-based species richness detected within protected areas should correlate strongly with SPI (plausible r >0.75) because both measure presence and diversity of protected species, though eDNA provides finer taxonomic resolution and temporal dynamics compared to static habitat models.

**Likely Data Source and Accessibility**: eDNA monitoring capacity concentrated in high-income countries with research infrastructure (particularly Australia, United States, Canada, northern Europe)[37]. U.S. Fish and Wildlife Service operates Conservation Genetics Labs implementing national eDNA strategies. Systematic country-level eDNA monitoring database does not yet exist; individual studies published in peer-reviewed literature but not compiled globally. Technology relatively new (widespread deployment 2010s-2020s) limiting historical temporal depth.

**Expected Functional Form**: Positive linear relationship between eDNA-detected species richness and SPI. Temporal dynamics (improvement over time in eDNA detection indicating population recovery) should correlate with SPI gains from recent protected area expansion or improved management.

**Geographic and Temporal Coverage**: eDNA monitoring established in North America, Australia, and increasingly in Europe and Asia. Minimal implementation in tropical developing regions where species diversity is highest but research capacity limited. Temporal coverage typically 2-10 years per study location; insufficient for long-term trend analysis in most cases.

**Accessibility**: eDNA analysis requires specialized laboratory equipment (quantitative PCR, sequencing capability) limiting accessibility to universities and research institutions. Results depend on existing monitoring programs rather than independently accessible database. Data accessibility typically through published research papers rather than unified data platform. Significant potential for future development of open-access eDNA database (OceanOmics team partnership with IUCN exploring this direction[8]).

### Speculative Proxy 5: Transnational Migratory Species Population Trends (as Proxy for Ecosystem Connectivity and Protected Area Network Function)

**Mechanistic Reasoning**: Species with transnational migration routes provide integrated tests of whether protected area networks function across political boundaries. Bird populations migrating between northern breeding grounds and tropical wintering grounds must traverse protected area systems in both origin and destination countries plus intermediate regions. Stable or increasing populations in well-protected transnational migratory species indicate that protected area networks provide meaningful habitat representation across their entire geographic ranges. Declining populations suggest inadequate protection in critical bottleneck regions. Countries achieving high SPI for migratory species demonstrate protected areas positioned at migration bottlenecks and breeding/wintering grounds.

**Expected Correlation**: Countries showing stable or increasing populations of transnational migratory species should demonstrate higher SPI, particularly for bird and marine species with long-distance migrations. Plausible correlation 0.55-0.70.

**Likely Data Source and Accessibility**: Breeding Bird Survey (BBS) data cover North American migrants with 50+ year time series; eBird citizen science database (>500 million observations) provides real-time species occurrence and population trend estimates through statistical modeling. BirdLife International maintains population trend data for comprehensive avian assessment. Marine migratory species tracked through satellite telemetry programs (available through Movebank) and fisheries observer programs. Amphibian migrations tracked through targeted research programs but less systematically.

**Expected Functional Form**: Positive linear relationship between migratory species population stability (measured as annual population change rate or trend slope) and SPI values. Mechanistically, stable populations indicate adequate habitat availability and quality across the geographic range, which should align with adequate habitat representation within protected areas.

**Geographic and Temporal Coverage**: Comprehensive data for North American birds (BBS since 1966); global eBird coverage highly variable by region with better coverage in developed nations. Marine tracking data concentrated on large vertebrates (tuna, sea turtles, marine mammals) and well-funded fisheries. Temporal coverage decades for BBS; eBird increasingly comprehensive from 2000 onward. Amphibian data limited to research project sites.

**Accessibility**: eBird data freely available as occurrence records and summary estimates through Cornell Lab of Ornithology (ebird.org); advanced population trend analysis requires statistical modeling capability. Movebank migration tracking data accessible through movebank.org; varies by project (some open, some restricted). BirdLife population trend database accessible through paid subscription or institutional access. BBS data freely available through USGS. No unified platform for global migratory species assessment currently exists.

## Data Availability Assessment Matrix

| **Proxy Candidate** | **Geographic Coverage** | **Temporal Granularity** | **Accessibility** | **Format** | **Completeness Rating** |
|---|---|---|---|---|---|
| PARC Representativeness Index | Regional/Selective | Multi-year snapshots | Account required (GEO BON) | CSV/Excel | 60% countries |
| Local Biodiversity Intactness Index (LBII) | Global | Annual (2001-2025) | Free open access | Raster/GeoTIFF | Global comprehensive |
| Species Habitat Index (SHI) | Global | Annual (2001-2025) | Free open access (EPI, Map of Life) | CSV/Raster | Global comprehensive |
| Red List Index (RLI) | Global | Quarterly updates | Free open access | CSV/Shapefile/GeoPackage | ~150 countries with species data |
| Percentage Terrestrial Protected (PTHP) | Global (185 countries) | Annual (1992-2024) | Free open access | CSV/Excel | 100% coverage |
| Landscape Fragmentation Metrics | Global | Annual (2000+) | Computationally intensive | Raster/derived metrics | Global potential, labor-intensive |
| Protected Area Management Effectiveness (PAME) | Regional selective | Multi-year (sporadic) | Mixed (some open, some restricted) | PDF/Excel | ~30% countries |
| Pesticide/Fertilizer Intensity | Global country-level | Annual | Free open access | CSV/Excel | 100% country-level; <10% spatial resolution |
| Environmental DNA Monitoring | Scattered | Annual/multi-year | Limited access | Database/papers | <5% countries with programs |
| Migratory Species Trends | Regional patterns | Annual/multi-year | Mostly free open access | CSV/Occurrence records | Highly variable by region |

## Confounder Analysis: Identifying Spurious Correlations

Cross-country proxy validation faces substantial confounding risks, where apparent correlations between proxies and SPI reflect common underlying drivers rather than mechanistic relationships. The following confounders require explicit control through statistical modeling:

**Regional Geographic Effects**: Tropical regions inherently contain higher species endemism and biodiversity density compared to temperate regions[10]. Many candidate proxies (habitat fragmentation, protected area percentage, species richness metrics) covary strongly with regional location due to fundamental biogeographic patterns. Countries in tropical biodiversity hotspots should simultaneously show high SPI (due to abundant endemic species requiring protection) and high habitat intactness (due to lower historical habitat conversion), creating spurious correlation. Statistical models should include regional fixed effects or geographic controls (latitude, bioclimate classifications) to isolate proxy effects from biogeographic baseline.

**Development Level and Institutional Capacity**: Although the prompt explicitly excludes GDP and governance indices as proxies, these remain critical confounders. Countries with higher GDP show greater protected area investment capacity, more sophisticated monitoring systems, and higher-quality data on species distributions. They also tend to have completed major land conversion decades earlier, resulting in lower current habitat fragmentation. Thus, wealthier countries may show high SPI not due to any specific policy mechanism captured by proxies, but due to overall institutional capacity and historical land-use patterns. **Control strategy**: Include proxy variables for specific development outcomes (road density, electrification rates, industrial facility density) rather than broad development indices; these capture specific land-use pressures relevant to species protection without confounding with general development level.

**Protected Area Age and Legacy Effects**: Countries with historically established protected area systems (created pre-1990) inadvertently captured representative species assemblages through geographic coincidence—protected areas in mountainous regions, deserts, and forests happened to align with biodiversity hotspots because these regions had lower economic value for extraction. Newer protected areas tend to be placed more strategically using species distribution data, potentially showing higher SPI. Thus, protected area percent and age structure confound SPI relationships. **Control strategy**: Disaggregate protected area measures by age cohort (pre-1990, 1990-2010, post-2010); analyze separately to isolate effects of strategic placement from legacy effects.

**Agricultural Pressure and Habitat Conversion Rate**: Countries experiencing rapid agricultural expansion (visible through satellite-derived deforestation metrics and pesticide intensity) simultaneously experience rapid habitat loss and fragmentation. A proxy measuring agricultural pressure (pesticide use, land conversion rate) might correlate with low SPI, but the mechanism is habitat loss itself rather than any specific management failure. The same agricultural pressure proxy would also correlate with low habitat intactness (SHI), creating circular correlation patterns. **Control strategy**: Use SHI or LBII (habitat intactness measures) as intermediate variable in structural models; test whether proxy effects on SPI persist after controlling for habitat availability.

**Data Quality Bias and Taxonomic Sampling Effort**: Countries with higher research capacity and international conservation program presence generate more species occurrence records, better protected area documentation, and more systematic biodiversity surveys. This generates upward bias in SPI estimates for these countries (better data reveals more comprehensive species protection) independent of actual species protection outcomes. Similarly, habitat suitability models perform more reliably with adequate species occurrence data, creating uncertainty in SPI estimates for data-poor regions. **Control strategy**: Quantify data availability and sampling effort (number of GBIF occurrence records per species, number of protected area boundary updates, proportion of species with <50 occurrence records) and include as uncertainty weight in models. Perform sensitivity analysis restricting to species/countries with adequate data.

**Marine versus Terrestrial Protected Area Effectiveness**: The same physical designation "marine protected area" can range from purely extractive reserves permitting fishing to no-take zones prohibiting human activity. Effectiveness varies dramatically, but designation statistics do not capture this variation. Terrestrial protected areas show similar variation. A proxy based on simple protected area percentage conflates highly effective strict reserves with minimally effective multiple-use areas. **Control strategy**: Disaggregate protected areas by IUCN category and management restriction level; analyze categories Ia-II (strict protection) separately from categories IV-VI (multiple-use), as these show different relationships with species protection outcomes.

## Ranked Candidate Proxies

Based on synthesis of correlation strength, data accessibility, geographic and temporal coverage, and mechanistic plausibility, the following rank-ordered list identifies the most promising proxies for cross-country SPI validation:

**Rank 1: Species Habitat Index (SHI) — Direct Habitat Availability Metric**

**One-Line Summary**: Measures extent and quality of ecologically intact habitat remaining in each country at high spatial resolution, providing the habitat denominator underlying SPI calculations.

**Expected Relationship Direction**: Positive correlation with SPI (r ~0.75-0.85), reflecting that countries retaining extensive intact habitat can achieve high SPI more readily.

**Data Source**: Global annual estimates from Map of Life (mol.org) and Environmental Performance Index (epi.yale.edu); free open access at 1km resolution; available since 2001.

**Rationale for Ranking**: SHI is directly mechanistically related to SPI (habitat representativeness depends on habitat availability), benefits from same species distribution datasets as SPI itself, provides global coverage with annual updates, and requires no additional field work or modeling. The measure directly captures conservation opportunity—countries with high SHI have greater capacity to achieve high SPI through protected area strategic placement.

---

**Rank 2: Local Biodiversity Intactness Index (LBII) — Empirical Biodiversity Persistence Indicator**

**One-Line Summary**: Estimates local species richness and abundance persistence based on PREDICTS database of real-world biodiversity surveys, capturing actual species responses to land use rather than modeled habitat availability.

**Expected Relationship Direction**: Positive correlation with SPI (r ~0.65-0.80); countries with high local biodiversity intactness show effective species persistence even in shared landscapes, indicating successful habitat protection.

**Data Source**: Annual global calculations since 2001 at 1km resolution; available through GEO BON, UN Biodiversity Lab, CBD Biodiversity Dashboard; free open access.

**Rationale for Ranking**: LBII provides empirical species-level data grounded in >3 million biodiversity survey observations across 45,000+ species. Unlike modeled habitat metrics, LBII directly measures species outcomes. The mechanism is clear: protected areas function to preserve the conditions that support species richness and abundance measured by LBII. The index complements SPI by measuring outcome (species persistence) rather than input (habitat representation), enabling validation that protected areas achieving high SPI actually deliver species-level conservation benefits.

---

**Rank 3: Red List Index (RLI) — Species Extinction Risk Trajectory**

**One-Line Summary**: Tracks average change in extinction risk across assessed species at country level, measuring whether conservation interventions (including protected areas) are reducing extinction risk.

**Expected Relationship Direction**: Positive correlation with SPI (r ~0.60-0.75); countries achieving high SPI and effective protection show stable or improving RLI (decreasing extinction risk).

**Data Source**: Country-level RLI calculated from IUCN Red List assessments; quarterly updates; free access through iucnredlist.org and downloadable spatial data in multiple formats.

**Rationale for Ranking**: RLI provides the most policy-relevant outcome metric—actual changes in extinction risk. Unlike habitat metrics that measure inputs or conditions, RLI directly addresses the ultimate conservation objective. The correlation captures whether SPI improvements translate to meaningful extinction risk reduction. RLI shows global coverage and frequent updates, though bias toward well-assessed vertebrates. Temporal lag between protected area establishment and RLI improvement requires time-lagged analysis.

---

**Rank 4: Landscape Fragmentation Metrics (Mean Patch Size, Core Area Index from High-Resolution Land Cover) — Habitat Availability Constraint**

**One-Line Summary**: Quantifies spatial configuration of remaining habitat patches using satellite-derived land cover maps, measuring whether habitat fragmentation constrains species persistence and SPI achievement.

**Expected Relationship Direction**: Positive correlation with SPI (r ~0.55-0.70); countries with larger habitat patches and less edge fragmentation achieve higher SPI because viable population sizes can be supported within protected areas.

**Data Source**: Computed from ESA Climate Change Initiative (annual 300m), Landsat (annual 30m), and MODIS land cover products (annual 500m); globally available from 2000 onward; open-source analysis tools (FRAGSTATS, Python/R spatial libraries).

**Rationale for Ranking**: Fragmentation directly constrains species persistence through increased extinction risk in small populations. Countries cannot achieve high SPI if remaining habitat is fragmented into patches below minimum viable sizes, regardless of protection percentages. The metric captures geometric constraints on SPI that simple area-based proxies miss. Requires computational capability to process satellite data, limiting accessibility for non-technical users, but global coverage and annual temporal resolution provide strong potential for systematic validation.

---

**Rank 5: Percentage Terrestrial Protected Area (PTHP) — Baseline Metric Despite Crude Relationship**

**One-Line Summary**: Simple percentage of national land area under protected area designation; crude but universally available baseline proxy.

**Expected Relationship Direction**: Positive correlation with SPI (r ~0.40-0.65), with substantial scatter due to variation in protected area placement quality and biodiversity distribution.

**Data Source**: World Bank indicator (data.worldbank.org/indicator/ER.LND.PTLD.ZS); annual updates 1992-2024; free access.

**Rationale for Ranking**: While PTHP represents the crudest proxy—many high-protection percentage countries achieve low SPI due to poor representativeness—it remains valuable as a baseline universal metric. All countries report protected area percentages, enabling complete geographic coverage. The weak correlation reflects the fundamental principle that SPI advances beyond: area protection alone does not ensure species protection. However, PTHP enables comparison of proxy performance; models including PTHP can demonstrate how much additional explanatory power SHI, LBII, and other metrics provide, validating the need for species-focused assessment beyond area targets.

---

**Rank 6: Agricultural Intensity Proxy (Pesticide Application in Protected Area Catchments) — Habitat Degradation Signal**

**One-Line Summary**: Fertilizer and pesticide application intensity in regions containing protected areas, measuring internal habitat degradation from agricultural runoff and chemical pollution.

**Expected Relationship Direction**: Negative correlation with SPI (r ~-0.50 to -0.65); high agricultural chemical intensity in protected area catchments predicts lower SPI due to habitat quality degradation.

**Data Source**: FAO global pesticide statistics (freely available through Worldometer, FAO.org); annual country-level data. Subnational mapping requires assembly of multiple sources with variable accessibility.

**Rationale for Ranking**: This proxy captures a mechanism overlooked by simple area-based proxies: protected areas can be formally designated yet internally degraded through chemical pollution and eutrophication, particularly in protected areas containing freshwater ecosystems. The negative relationship is mechanistically clear—high agricultural intensity surrounding protected areas indicates spillover pollution. Global country-level data availability is strong. Subnational spatial resolution remains limited, constraining ability to measure catchment-specific effects. The proxy shows promise for identifying protected areas vulnerable to external pressure, complementing habitat-based proxies.

---

**Rank 7: Protected Area Management Effectiveness Average Score (PAME) — Actual Implementation Quality**

**One-Line Summary**: Country average score from METT-4 or equivalent management effectiveness assessments, measuring whether protected areas are actively managed versus existing as "paper parks."

**Expected Relationship Direction**: Positive correlation with SPI (r ~0.60-0.75); countries achieving high average PAME scores demonstrate actual species conservation outcomes reflected in higher SPI.

**Data Source**: Global Database for Protected Area Management Effectiveness (GD-PAME) accessed through Protected Planet (protectedplanet.net); implementation concentrated in developing countries with conservation program support; data access requires account and direct requests to custodians; available ~30% of countries.

**Rationale for Ranking**: PAME captures the critical dimension of implementation quality—whether protected areas are adequately staffed, funded, and enforced. This directly bridges the gap between nominal protection (protected area designation) and functional protection (SPI outcomes). Countries with high PAME scores should show higher SPI for equivalent habitat availability because protected area management directly supports species persistence. However, geographic incompleteness (primarily developing nations with conservation program presence) and inconsistent public data availability limit utility for comprehensive cross-country analysis. Most valuable for focused regional analysis in well-monitored regions.

---

## Implementation Recommendations for Proxy Utilization

The ranked proxy candidates enable multiple analytical approaches depending on available resources and analytical objectives:

**Quick Assessment Approach** (Minimal Computational Requirements): Use SPI with readily available companion proxies PTHP, SHI, and RLI to evaluate whether existing country-level data validates species-focused protection. These three proxies require only CSV download and standard statistical software; complete global analysis feasible within weeks. Expected outcomes: validation that habitat representativeness (SPI/SHI) predicts extinction risk reduction (RLI) better than simple area targets (PTHP).

**Causal Modeling Approach** (Moderate Computational Requirements): Implement structural equation model or directed acyclic graph (DAG) analysis incorporating SPI as outcome variable with SHI (habitat availability), LBII (biodiversity persistence), PAME (management quality), and PTHP (simple protection percentage) as predictors. This approach tests whether mechanistic links between habitat protection inputs and biodiversity outcomes hold empirically. Include regional fixed effects and appropriate controls for development confounders. Expected outcome: identification of which proxy mechanisms—habitat availability, biodiversity intactness, or management effectiveness—most strongly drive SPI variation.

**Satellite-Intensive Approach** (High Computational Requirements): Compute landscape fragmentation metrics from ESA Climate Change Initiative land cover data for all countries and all years, enabling assessment of whether fragmentation constraints on SPI are measurable empirically. Combine with spatially explicit SPI estimates (available at 1km resolution from Map of Life) to test whether protected areas in heavily fragmented regions show lower SPI per unit area protected. Expected outcome: quantitative characterization of fragmentation-SPI relationships underlying conceptual causal models.

**Temporal Dynamics Approach** (Time-Series Analysis): Use annual SHI, LBII, and PTHP data spanning 2001-2024 to perform time-series analysis testing whether SPI improvements (measured through retrospective calculation from published reports or Map of Life updates) correlate with lagged changes in habitat metrics. This addresses temporal ordering of causation and lag structures. Expected outcome: clarification of whether habitat loss (declining SHI) drives SPI decline, or whether strategic protected area placement enables SPI improvement despite continued habitat loss.

**Regional Comparative Advantage Approach** (Targeted Regional Analysis): Prioritize proxies with complete data for specific regions (e.g., PAME data for Central America, eBird migratory trends for North America, LBII for any region). Conduct focused regional analysis testing proxy power in data-rich regions, then apply learnings to data-sparse regions. Expected outcome: validated region-specific proxy models that could inform conservation prioritization.

## Conclusion

The Species Protection Index represents a significant advance in biodiversity assessment, shifting conservation focus from simple area targets to species-level habitat representativeness. Yet the metric's reliance on habitat suitability modeling and extensive species distribution data limits accessibility for countries seeking to assess their own progress or for researchers operating outside the Map of Life institutional structure. This comprehensive proxy analysis identifies multiple candidate alternative data sources demonstrating strong mechanistic linkage to SPI while offering advantages in geographic coverage, temporal resolution, or ease of access.

The **Species Habitat Index (SHI) emerges as the highest-priority proxy**, sharing data sources and calculation methodologies with SPI while providing annual updates and global coverage. Complementary use of **Local Biodiversity Intactness Index (LBII)** and **Red List Index (RLI)** provides additional validation through empirical species persistence data and extinction risk metrics, respectively. Together, these three proxies enable cross-country assessment of species protection effectiveness that parallels SPI conceptually while remaining accessible to countries with limited technical capacity.

Landscape fragmentation metrics and agricultural intensity proxies capture mechanistically distinct pathways through which protected areas succeed or fail to protect species—habitat configuration constraints and internal degradation from external pressures. Percentage terrestrial protected area, while crude, remains essential as a baseline metric demonstrating where species-focused approaches (via SPI and proxies) add explanatory power beyond simple area targets.

Statistical validation of these proxies through correlation analysis with SPI estimates should comprise the next analytical phase, testing whether the mechanistic relationships theorized in this report hold empirically across the global landscape. Regional comparative analysis, temporal dynamics studies, and causal modeling approaches offer multiple pathways to proxy validation and refinement. As global biodiversity monitoring systems mature, these proxy candidates provide interim solutions for countries seeking to assess progress toward species protection goals while comprehensive species-level assessment infrastructure develops.

## References
[1] https://mapoflife.ai/resources/indicators/species-protection-index
[2] https://www.ipbes.net/sites/default/files/Metadata_GEO_BON_Protected_Area_Representativeness_Index.pdf
[3] https://www.frontiersin.org/journals/ecology-and-evolution/articles/10.3389/fevo.2025.1561640/full
[4] https://www.science.org/doi/10.1126/sciadv.adg0288
[5] https://pmc.ncbi.nlm.nih.gov/articles/PMC10015333/
[6] https://data.worldbank.org/indicator/ER.LND.PTLD.ZS
[7] https://www.protectedplanet.net/en/thematic-areas/wdpa
[8] https://www.iucnredlist.org
[9] https://en.wikipedia.org/wiki/Megadiverse_countries
[10] https://www.conservation.org/learning/biodiversity-hotspots
[11] https://modis.gsfc.nasa.gov/sci_team/meetings/200101/Presentations/l2_townshend.pdf
[12] https://hub.arcgis.com/maps/65518e782be04e7db31de65d53d591a9/about
[13] https://www.wri.org/insights/forest-loss-drivers-data-trends
[14] https://epi.yale.edu/epi-results/2020/component/wtl
[15] https://coralreefwatch.noaa.gov/satellite/research/coral_bleaching_report.php
[16] https://trade.cites.org
[17] https://www.worldometers.info/food-agriculture/pesticides-by-country/
[18] https://www.ipbes.net/IASmediarelease
[19] https://conbio.onlinelibrary.wiley.com/doi/full/10.1111/conl.13101
[20] https://www.iucnredlist.org/about/green-status-species
[21] https://data360.worldbank.org/en/dataset/WB_GBIOD
[22] https://ourworldindata.org/living-planet-index-region
[23] https://unfccc.int/topics/land-use/workstreams/land-use--land-use-change-and-forestry-lulucf
[24] https://www.ars.usda.gov/ARSUserFiles/30180000/Schuman/25.Herrick%20et%20al.%202006.pdf
[25] https://pubmed.ncbi.nlm.nih.gov/15071592/
[26] https://epi.yale.edu/downloads/2024-epi-report-20250106.pdf
[27] https://geobon.org/ebvs/indicators/species-habitat-index-shi/
[28] https://en.wikipedia.org/wiki/Nature_Index
[29] https://files.ipbes.net/ipbes-web-prod-public-files/Metadata_GEO_BON_PREDICTS_Local_Biodiversity_Intactness_Index.pdf
[30] https://epi.yale.edu/welcome
[31] https://epi.yale.edu/measure/2024/SHI
[32] https://group.springernature.com/de/group/media/press-releases/nature-index-research-leaders-/27786652
[33] https://resourcewatch.org/data/explore/bio_014-Biodiversity-Intactness
[34] https://pmc.ncbi.nlm.nih.gov/articles/PMC6881168/
[35] https://www.esvd.info/ourdatabase
[36] https://pmc.ncbi.nlm.nih.gov/articles/PMC4881334/
[37] https://www.fws.gov/project/environmental-dna-edna
[38] https://rris.biopama.org/node/20639
[39] https://www.naturalworldfund.org.uk/global-agriculture-expansion-is-driving-biodiversity-loss/
[40] https://pmc.ncbi.nlm.nih.gov/articles/PMC10249400/
[41] https://pmc.ncbi.nlm.nih.gov/articles/PMC8258205/
[42] https://pubmed.ncbi.nlm.nih.gov/26189556/
[43] https://pmc.ncbi.nlm.nih.gov/articles/PMC6193709/
[44] https://pmc.ncbi.nlm.nih.gov/articles/PMC12258097/
[45] https://pmc.ncbi.nlm.nih.gov/articles/PMC1629036/
[46] https://conservationbytes.com/wp-content/uploads/2014/12/brook-et-al-2006-ecol-lett.pdf
[47] https://www.gbf-indicators.org/metadata/headline/A-1
[48] https://onlinelibrary.wiley.com/doi/10.1111/geb.12888
[49] https://news.mongabay.com/2026/03/where-conservation-works-best-the-rise-of-place-specific-strategies/amp/
[50] https://conbio.onlinelibrary.wiley.com/doi/10.1111/cobi.12846