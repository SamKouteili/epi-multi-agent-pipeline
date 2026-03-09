# Alternative Data Sources (Proxies) for Ozone Exposure in Key Biodiversity Areas: A Comprehensive Research Assessment

This report presents a thorough investigation of alternative indicators and datasets that could serve as statistical proxies for mean annual ozone exposure across countries' Key Biodiversity Areas (OEB). The analysis integrates published research on ozone formation mechanisms, empirical correlations with environmental and industrial variables, and novel data sources that have emerged in remote sensing and environmental monitoring networks. The goal is to identify concrete, directly-measurable signals that correlate with ground-level ozone concentrations in biodiversity-sensitive regions, offering the Yale Environmental Performance Index team pathways to validate, supplement, or potentially replace the current Copernicus/CAMS-based measurement approach with more accessible, frequently-updated, or geographically-comprehensive alternatives.

## Understanding the Causal Architecture of Ground-Level Ozone Exposure in Biodiversity Areas

Ground-level ozone concentration, and specifically its exposure levels across Key Biodiversity Areas, emerges from a complex cascade of atmospheric chemistry, emission patterns, and physical transport processes. To systematically identify meaningful proxies, we must first map the upstream drivers and downstream consequences of this indicator, recognizing that ozone is not directly emitted but is instead a secondary pollutant formed through photochemical reactions in the troposphere.

### Upstream Causal Drivers of Ozone Exposure

The fundamental drivers of ground-level ozone concentration operate at multiple scales and through distinct mechanistic pathways. At the emission level, the primary precursors to ozone formation are nitrogen oxides (NOx) and volatile organic compounds (VOCs)[1][8]. These precursors undergo complex chemical reactions in the presence of sunlight, with the reaction rates strongly dependent on ambient temperature and humidity conditions[1]. Vehicle emissions represent a particularly significant source of NOx in regions with high traffic density, especially in urban cores where morning and evening commutes generate sharp peaks in nitrogen dioxide concentrations[21]. Industrial boilers, refineries, chemical plants, and power plants contribute additional NOx and VOC loads[1]. In rural areas, agricultural operations—particularly livestock management and soil microbial processes—emit ammonia and other nitrogen compounds that interact with anthropogenic NOx to form secondary organic aerosols and ozone[30]. Importantly, the agricultural and industrial sectors in rapidly developing economies represent rapidly expanding sources of these precursors[7].

A critical mechanistic feature of ozone formation is its non-linear dependence on precursor concentrations. In NOx-limited environments (typically rural and remote areas), reducing NOx emissions will decrease ground-level ozone, whereas in VOC-limited environments (typically dense urban centers), reducing VOCs is more effective at decreasing ozone, and paradoxically, reducing NOx in VOC-limited regimes can sometimes increase ozone because NOx acts as a sink for ozone through the reaction \(NO + O_3 \rightarrow NO_2 + O_2\)[43]. This non-linearity means that the relationship between any single precursor emission source and ozone concentration is context-dependent and cannot be assumed to be monotonic across all geographic contexts.

Biogenic sources of VOCs add significant complexity to the causal system. Plants, particularly in forested regions and ecosystems during warm months, emit isoprene and monoterpenes that react with anthropogenic NOx to form ozone[47]. The emission rates of these biogenic compounds are temperature-dependent and vegetation-type-dependent, with different tree species, crops, and grasslands exhibiting substantial variation in emission potentials[47]. This means that regions with high forest productivity and biodiverse vegetation communities may paradoxically experience elevated ozone exposure not due to local pollution sources, but due to the interaction of biogenic emissions with background NOx from distant anthropogenic sources.

Regional and long-range transport patterns fundamentally shape where ozone exposure occurs. Wind patterns, topography, and anticyclonic weather conditions determine whether ozone accumulates locally or is transported to downwind regions[22]. The Mediterranean summertime ozone maximum—where eastern Mediterranean coastal regions experience ozone concentrations exceeding 85 ppbv in the lower troposphere—illustrates how dominant anticyclonic circulation patterns suppress vertical mixing and concentrate ozone in the boundary layer, while also importing polluted air masses from continental Europe[22]. This transport mechanism means that Key Biodiversity Areas in downwind regions may experience significant ozone exposure despite having minimal local emission sources, making local precursor inventories poor proxies for actual exposure.

### Downstream Consequences and Feedback Loops

Ozone exposure within Key Biodiversity Areas produces cascading effects on plant physiology, ecosystem function, and ultimately biodiversity. At the leaf level, ozone penetrates the stomata and causes oxidative stress, reducing net photosynthesis and accelerating leaf senescence[2][6][7][24][50]. This physiological damage translates to reduced carbon uptake and biomass accumulation across plant functional types, though with substantial variation in sensitivity. Deciduous trees and agricultural crops show markedly higher sensitivity to ozone damage than evergreen conifers, with sensitivity mechanistically linked to leaf mass per area (LMA) traits—species with high maximum photosynthetic rates and low-density leaves are particularly vulnerable. Current ground-level ozone concentrations in many regions suppress yields of sensitive crops by 5-15%, with greater impacts expected if ozone levels continue rising[2]. In field experiments, soybean yields have demonstrated 10% reductions across five-year periods in regions with ambient ozone exposure[50].

Forest productivity reductions under ozone stress operate through both direct physiological effects and indirect ecosystem-level changes. A meta-analysis of 263 articles on elevated ozone effects in northern temperate and boreal trees found an 11% decrease in tree biomass compared with trees at ambient ozone levels, alongside significant reductions in root-to-shoot ratio, leaf area, photosynthetic capacity, and transpiration rates[50]. Importantly, ozone effects offset the growth stimulation normally expected from elevated atmospheric CO₂[50], suggesting that regions expecting carbon sequestration benefits from rising CO₂ may instead experience net productivity losses if ozone continues to increase. In specific forest types, the damage can be severe: stem volume growth in European beech has decreased by 44% under elevated ozone exposure[50].

These productivity losses have direct implications for ecosystem services provision to human communities dependent on these landscapes. Ozone-induced reductions in forest water cycling have been documented to decrease late-season stream flow in forested watersheds by as much as 23% based on 18-26 year data records from the southeastern United States[50]. In agricultural regions, the economic losses are quantifiable: global risk assessment modeling estimates yield losses of staple crops between 3-16% with economic losses between US$14-26 billion in the year 2000[7][50]. Current day ozone levels are reducing soybean seed protein yield by approximately 200 kg protein per hectare compared with pre-industrial levels[50].

Beyond productivity losses, ozone exposure alters ecosystem composition and structure, potentially reducing biodiversity even where overall biomass is partially maintained. Evidence from simulated plant community experiments shows that ozone induces changes in species composition, with the biomass and cover of typical woodland species being reduced compared with non-shade-adapted, invasive species[6]. This compositional shift has cascading effects: altered plant communities change insect herbivore populations, modify soil microbial activity and mite populations, and shift forest successional pathways, ultimately reducing structural complexity and the microhabitat diversity that supports vertebrate and invertebrate species[6][50].

### Conceptual Causal Diagram

The upstream-to-downstream causal architecture can be schematized as follows:

```
UPSTREAM DRIVERS:
├─ Anthropogenic Emissions
│  ├─ Traffic (NOx, direct correlation with vehicle fleet size, fuel consumption)
│  ├─ Energy generation (NOx, coal/fossil fuel use)
│  ├─ Industrial processes (NOx, VOCs, chemical production, refining)
│  └─ Agricultural activities (NH3, soil emissions)
├─ Biogenic Sources
│  ├─ Forest emissions (temperature-dependent isoprene, monoterpenes)
│  ├─ Crop emissions (isoprene, monoterpenes)
│  └─ Vegetation type and productivity
└─ Physical-Chemical Transport
   ├─ Solar radiation (drives photochemical reactions)
   ├─ Temperature (increases reaction rates)
   ├─ Humidity (affects chemistry)
   ├─ Wind patterns (advection, mixing height)
   └─ Topography (valley trapping, boundary layer dynamics)

↓ [PHOTOCHEMICAL REACTIONS: NOx + VOC + sunlight → O₃]

GROUND-LEVEL OZONE CONCENTRATIONS IN KBAs
(OEB indicator)

↓

DOWNSTREAM EFFECTS:
├─ Plant Physiological Damage
│  ├─ Reduced photosynthesis
│  ├─ Accelerated senescence
│  ├─ Impaired growth and biomass allocation
│  └─ Reduced pollen fertility
├─ Ecosystem-Level Consequences
│  ├─ Reduced net primary productivity (4.8% global mean)
│  ├─ Altered species composition (invasive species favored)
│  ├─ Reduced biodiversity (ozone-sensitive species decline)
│  ├─ Altered nutrient cycling
│  └─ Reduced water cycling (stream flow reductions ~23%)
├─ Agricultural/Economic Losses
│  ├─ Crop yield reductions (3-16% for staple crops)
│  ├─ Protein yield losses (200 kg/ha for soybeans)
│  └─ Economic damage ($14-26 billion annually)
└─ Biodiversity Outcomes
   ├─ Species extinction risk increases
   ├─ Ecosystem service provision declines
   └─ Resilience to other stressors (drought, pests) decreases
```

This causal architecture reveals that effective proxies for OEB need not be direct measurements of ozone itself. Rather, they could capture any point in this causal chain: precursor emissions, meteorological conditions facilitating ozone formation, transport patterns, biogenic emission potentials, or even the downstream ecological consequences that reflect integrated ozone exposure over time.

## Literature-Validated Proxies for Ground-Level Ozone Exposure

### Satellite-Derived Nitrogen Dioxide Columns

**Variable Name and Description**: Tropospheric column nitrogen dioxide (NO₂) concentration, measured in molecules cm⁻², derived from satellite instruments including the Ozone Monitoring Instrument (OMI), TROPOMI/Sentinel-5P, and GOME-2. These measurements represent the integrated NO₂ concentration in the troposphere above each ground location.

**Source Dataset**: The Resource Watch Air Quality dataset provides global monthly averages of NO₂ density in the troposphere from satellite measurements[11]. Additionally, the CAMS global reanalysis provides 3-dimensional atmospheric composition fields including NO₂, with approximately 80 km resolution and sub-daily temporal frequency, covering 2003 to December 2024[4]. The OMI/MLS L3 1x1 degree monthly tropospheric column ozone measurements from NASA's Earth Observing System Aura satellite offer high-quality, validated NO₂ retrievals globally[42].

**Reported Correlation Strength and Sample**: Vehicle NOx emissions have direct correlation with ground-level ozone formation[1][8]. The non-linear relationship means that correlation strength will depend on local NOx vs. VOC sensitivity regimes. In NOx-limited rural areas, tropospheric NO₂ columns should correlate strongly and positively with ground-level ozone (r > 0.6 expected). In VOC-limited urban areas, the relationship may be weaker or even slightly inverse due to NO's role as an ozone sink. No single published study specifically correlates satellite NO₂ columns with ozone exposure in Key Biodiversity Areas; this represents a gap where the proxy would need to be validated.

**Expected Functional Form**: The relationship is expected to be approximately linear in NOx-limited regimes (most rural KBAs and global background ozone), with a threshold or saturation effect possible in heavily polluted urban areas. The functional form would be: \(OEB \approx \alpha \cdot NO_2_{column} + \beta + \epsilon\), where \(\alpha\) is positive in NOx-limited regimes and potentially near zero or slightly negative in VOC-limited urban cores.

**Key Caveats and Limitations**: (1) Satellite NO₂ retrievals have systematic uncertainties of ±15-20%, particularly over complex terrain and at high latitudes[11]. (2) Column measurements integrate through the entire troposphere, which may not capture the boundary-layer dynamics most relevant to surface ozone formation. (3) The relationship depends critically on local VOC availability; without knowing whether a region is NOx-limited or VOC-limited, the sign and magnitude of the correlation is ambiguous. (4) Stratospheric NO₂ must be separated from tropospheric NO₂ for accurate surface ozone prediction, adding processing complexity. (5) Satellite instruments have limited temporal coverage in some regions (e.g., high latitudes during winter).

**Citation**: Resource Watch data infrastructure and CAMS Copernicus Atmosphere Monitoring Service[4][11].

---

### Biomass-Based Volatile Organic Compound Emission Potential

**Variable Name and Description**: Biogenic volatile organic compound (BVOC) emission potential, calculated as isoprene and monoterpene emissions (in units of nmol m⁻² s⁻¹) at standard temperature and light conditions, aggregated to country or KBA level. This reflects the VOC-emitting capacity of vegetation in the region.

**Source Dataset**: The MEGAN 2.1 model (Model of Emissions of Gases and Aerosols from Nature) provides gridded estimates of biogenic VOC emissions at 0.5° resolution globally[47]. Monthly isoprene and monoterpene emissions can be derived from this model. Ground-based measurements of BVOC emissions from individual species and plant functional types are available from experimental studies, such as those measuring emissions from hybrid aspen, Italian alder, and Sitka spruce in short-rotation forestry trials[47]. Satellite-derived vegetation indices (normalized difference vegetation index, NDVI) from MODIS and VIIRS provide spatially-continuous proxies for vegetation productivity and emission potential[15].

**Reported Correlation Strength and Sample**: Experimental work on Mediterranean summertime ozone has shown that a 20% reduction in biogenic VOC emissions leads to widespread reductions in ozone over the Mediterranean basin, with average reduction of 0.96 ppbv near the surface[22]. This demonstrates sensitivity of ozone to biogenic VOC availability. However, the mechanistic relationship is complex: in NOx-limited regions, increased biogenic VOCs lead to increased ozone (positive correlation); in VOC-limited regions, biogenic VOCs have less impact because ozone formation is already VOC-saturated. Studies on short-rotation forestry expansions in the UK project that BVOC emissions could increase by <1% to 35% nationally depending on tree species planted, with larger regional impacts expected[47]. The correlation between BVOC potential and actual ozone exposure is expected to be moderate (r = 0.3-0.6) and regionally heterogeneous.

**Expected Functional Form**: Threshold-dependent or interaction-dependent. In NOx-limited KBAs: \(OEB \approx \gamma \cdot BVOC_{potential} + \delta\), with \(\gamma > 0\) (increasing vegetation emissions increase ozone). In VOC-limited KBAs, the relationship flattens. A more realistic form would incorporate both NOx and BVOC: \(OEB \approx f(NOx, BVOC)\) with interaction terms reflecting chemistry.

**Key Caveats and Limitations**: (1) MEGAN 2.1 estimates depend on temperature and light parameterization; in regions with uncertain climate data, emission estimates have high uncertainty. (2) BVOC emissions vary substantially within plant functional types based on species identity, age structure, and environmental stress; country-level aggregation may obscure important heterogeneity. (3) The relationship between BVOC and ground-level ozone is indirect, requiring knowledge of NOx availability and local NO₂/NOx ratios. (4) Satellite NDVI data can be obscured by clouds, limiting applicability in tropical regions during wet seasons.

**Citation**: MEGAN model development and application literature[47]; MODIS and VIIRS vegetation products[15].

---

### Vehicle Fleet Size and Fuel Consumption

**Variable Name and Description**: National vehicle ownership rate (vehicles per 1,000 people) and total vehicle miles traveled or fuel consumption (e.g., total annual gasoline and diesel consumption, in metric tonnes or liters). These capture the primary anthropogenic source of NOx in most countries.

**Source Dataset**: Global vehicle ownership statistics by country are maintained by automotive industry databases and the International Organization of Motor Vehicle Manufacturers (OICA). As of 2025, global vehicle ownership averages 203 cars per 1,000 people, with high variance across regions[48]. North America leads with 710 cars per 1,000 people, Europe with 520 per 1,000, while Africa has only 58 per 1,000[48]. Fuel consumption by country can be obtained from the International Energy Agency (IEA) energy balances, available annually with global coverage. The U.S. Energy Information Administration (EIA) provides detailed energy use by sector, with transportation data publicly available[18].

**Reported Correlation Strength and Sample**: Vehicle emissions contribute the majority of NOx in most developed countries[8]. Studies on ozone formation consistently identify traffic as the dominant NOx source in urban areas[21]. However, the correlation between total vehicle ownership and ozone exposure in KBAs is complex because: (1) KBAs are often in protected, rural areas far from traffic; (2) vehicle emissions in one region can be transported long distances; (3) fleet composition (proportion of diesel vs. gasoline, age, emission control standards) varies dramatically between countries, affecting actual NOx emissions per vehicle. Expected correlation strength between vehicle ownership and KBA ozone exposure is moderate (r = 0.3-0.5), with high geographic heterogeneity.

**Expected Functional Form**: Approximately linear at the country level, with potential interaction terms for vehicle fleet age composition and emission control stringency. \(OEB \approx \eta \cdot VehicleOwnership_{rate} + \theta \cdot EUStandard_{adoption} + \epsilon\). However, this relationship would likely only hold for countries where vehicle emissions dominate and KBAs are close to traffic corridors.

**Key Caveats and Limitations**: (1) Vehicle ownership is a lagging indicator of actual emissions—a country with high vehicle ownership but strict emission standards (e.g., new Euro 6 diesel standards) may have lower actual NOx emissions than a country with lower vehicle ownership but older, less-controlled vehicles. (2) Fuel consumption statistics are often collected with long reporting lags and may not be available annually for all countries. (3) The relationship breaks down in regions where vehicle emissions are not the dominant source (e.g., regions with very high coal consumption for power generation, major industrial complexes, or volcanic outgassing of natural NOx). (4) This proxy tells us nothing about ozone in regions where transboundary transport dominates the ozone signal.

**Citation**: OICA and IEA statistics[18][48].

---

### Industrial Production Statistics and Energy Consumption

**Variable Name and Description**: Sectoral fuel consumption (coal, oil, natural gas) and industrial production metrics including cement production (tonnes per year), petroleum refining capacity, chemical manufacturing capacity, and iron/steel production. These capture non-vehicular NOx and VOC emission sources.

**Source Dataset**: The World Economic Forum's cement production data indicates that global cement manufacturing produced 1.6 billion metric tonnes of CO₂ in 2022, constituting ~8% of global CO₂ emissions[28]. Cement manufacturing is energy-intensive and correlated with NOx emissions from kiln fuel combustion. Industrial sector energy consumption data are available from the IEA, World Bank, and national statistics agencies. The EDGAR emissions inventory provides sector-specific and country-specific emissions time series from 1970-2022 for air pollutants including NOx, NMVOC, and speciated VOCs[20]. Copper, aluminum, and steel production statistics are available from the U.S. Geological Survey and the International Energy Agency.

**Reported Correlation Strength and Sample**: Industrial production—particularly energy-intensive sectors like cement, steel, refining, and chemicals—directly produces NOx and VOCs[1][8]. The EPA 1996 ozone criteria document estimated national-level losses to major crops exceeding $1 billion annually, with loss severity linked to industrial NOx emissions in agricultural regions[2]. The EDGAR database quantifies this relationship: industrial fuel combustion is a major sectoral contributor to NOx emissions, and national industrial emissions correlate with ozone exposure metrics in multiple regions. Expected correlation strength is moderate to high (r = 0.4-0.7), particularly for countries where industrial activity is spatially concentrated relative to KBAs.

**Expected Functional Form**: Approximately linear with potential interaction terms for technology adoption and emission controls. \(OEB \approx \iota \cdot IndustrialEnergy_{consumption} + \kappa \cdot AbatementCapacity + \epsilon\), where abatement capacity reflects pollution control investments.

**Key Caveats and Limitations**: (1) Sectoral energy consumption data often have significant reporting delays and methodological differences between countries. (2) Industrial facilities are often concentrated in specific regions, meaning country-level aggregation obscures important spatial heterogeneity. (3) Similar to vehicles, the relationship depends on emission control technology adoption: a country with high industrial production but advanced selective catalytic reduction (SCR) on power plants will have lower NOx emissions than expected from production volume alone. (4) Transboundary transport again confounds the relationship: ozone in a KBA may reflect industrial emissions from a neighboring country.

**Citation**: EDGAR emissions inventory[20]; World Economic Forum and IEA statistics[28].

---

### Satellite-Derived Cloud-Free Days and Solar Radiation

**Variable Name and Description**: Annual count of cloud-free days or direct normal irradiance (DNI) measurements in Watts per square meter (W m⁻²), derived from satellite instruments (CERES, MODIS) or ground-based solar stations. This captures the availability of photochemically-active radiation necessary for ozone formation.

**Source Dataset**: NASA's CERES (Clouds and Earth's Radiant Energy System) instruments on Terra and Aqua satellites provide monthly and annual averages of surface solar radiation globally at 1° resolution[37]. The NASA OMI instrument also provides photolysis-rate diagnostic information[42]. Ground-based measurements of total and direct solar irradiance are available from national meteorological services and the GCOS Surface Radiation Budget Network.

**Reported Correlation Strength and Sample**: Solar radiation intensity directly drives the photochemical reactions that produce ozone from NOx and VOCs[1][21]. Ozone is "most likely to reach unhealthy levels on hot sunny days," indicating strong sensitivity to radiation availability[1]. Regions with high cloud cover naturally experience lower ozone formation rates due to reduced photochemical activity[22]. However, the relationship is non-linear: above a threshold of radiation intensity, the reaction kinetics saturate and further increases in radiation have diminishing ozone-formation effects. Expected correlation strength is moderate (r = 0.4-0.6).

**Expected Functional Form**: Saturating or threshold relationship: ozone increases with radiation up to ~600 W m⁻² annual average, then plateaus. A functional form: \(OEB \approx \mu \cdot \min(RadiationIntensity, Threshold) + \nu + \epsilon\).

**Key Caveats and Limitations**: (1) Satellite solar radiation estimates have typical uncertainty of ±5-10% due to atmospheric correction uncertainties. (2) The relationship assumes NOx and VOC are available; in regions where precursors are extremely scarce (e.g., pristine remote regions), high radiation does not translate to high ozone. (3) Temporal variability in cloudiness from year to year can create noise in the proxy. (4) This is a climate variable, not specific to ozone formation chemistry, so its use as a proxy requires statistical validation rather than mechanistic justification alone.

**Citation**: NASA CERES and OMI instrument data[37][42].

---

### Atmospheric Boundary Layer Height and Meteorological Stagnation Indices

**Variable Name and Description**: Mean annual planetary boundary layer (PBL) height in meters, or stagnation indices capturing the frequency and intensity of weather conditions that suppress vertical mixing (e.g., anticyclonic days, temperature inversion frequency). PBL height determines the volume of air available for pollutant dispersion.

**Source Dataset**: PBL height estimates are derived from radiosonde profiles (routine balloon-launched atmospheric soundings) available through NOAA's RAOB database and international meteorological centers. Satellite-based PBL height estimates are available from CALIOP lidar aboard CALIPSO and from reanalysis products including MERRA-2 and ERA5[4]. Reanalysis products provide globally-gridded daily PBL heights at 1-hour temporal resolution and ~30-80 km spatial resolution. Stagnation indices (characterized by persistent anticyclonic conditions, temperature inversions, and weak winds) can be calculated from reanalysis data and have been linked to ozone episodes in published literature.

**Reported Correlation Strength and Sample**: Suppressed vertical mixing and shallow mixing heights lead to accumulated surface-level ozone, as demonstrated in boundary layer transport and mixing studies. The Mediterranean summertime ozone maximum is explicitly attributed to "suppressed vertical mixing and shallow mixing heights" caused by dominant anticyclonic conditions[22]. Studies quantify that ozone transport and mixing processes in boundary layers critically determine surface ozone exposure, with shallower mixing heights concentrating ozone near the surface. Expected correlation is strong and negative: lower PBL height → higher surface ozone concentration (r = -0.5 to -0.7).

**Expected Functional Form**: Approximately inverse or power-law relationship: \(OEB \approx \xi / PBL_{height} + \omicron\) or \(OEB \approx \pi \cdot PBL_{height}^{-\alpha} + \epsilon\), with \(\alpha > 0\).

**Key Caveats and Limitations**: (1) Radiosonde networks are spatially sparse and concentrated in developed countries; coverage over Africa, Southeast Asia, and the Pacific is limited. (2) Satellite-based PBL estimates from CALIOP are cloud-dependent and therefore unavailable during cloudy periods. (3) Reanalysis PBL heights may be biased high or low depending on the assimilation system; ERA5 and MERRA-2 show systematic differences in PBL height estimates. (4) PBL height is a meteorological variable influenced by climate/weather, making it a confounder that correlates with many other environmental indicators rather than a mechanistically-distinct proxy.

**Citation**: CALIOP lidar and reanalysis products; Ozone transport and mixing literature.

---

### Crop Yield Observations and Agricultural Productivity Indices

**Variable Name and Description**: National average crop yields for ozone-sensitive crops including wheat, soybeans, rice, and maize (measured in tonnes per hectare), available from national agricultural statistics or FAO databases. These represent the integrated impact of ozone and other environmental stressors on plant productivity.

**Source Dataset**: The Food and Agriculture Organization (FAO) maintains country-level crop production and yield data for all major crops at annual resolution since 1961, available through the FAO FAOSTAT database[44]. "Our World in Data" provides cleaned and visualized crop yield time series for global analysis[44]. National agricultural ministries provide detailed sub-national yield data in most countries. The USDA National Agricultural Statistics Service (NASS) provides U.S. crop yield data at county resolution.

**Reported Correlation Strength and Sample**: Crop yield reductions from current ambient ozone are well-established: wheat yield losses are 8.4% when comparing ambient vs. pre-industrial ozone[50]; soybean yield reductions of 10% over 5-year periods in the U.S. mid-west; global staple crop yield losses of 3-16% attributed to ozone[7][50]. A direct mechanistic link exists: ground-level ozone in agricultural areas reduces net photosynthesis, accelerates senescence, and reduces biomass allocation to grain, thereby reducing harvestable yield[2][50]. However, crop yield is also affected by water availability, soil nutrients, pest pressure, and other environmental variables; ozone is only one of multiple factors. Expected correlation between ozone exposure and crop yield is moderate (r = -0.3 to -0.5), with substantial residual variance from other factors.

**Expected Functional Form**: Approximately linear or log-linear decline in yield with increasing ozone: \(Yield \approx Y_0 - \beta \cdot OEB + \epsilon\), with \(\beta > 0\). Alternatively, the AOT40 threshold-dose relationship: yields decline above ozone exposure thresholds, with magnitude depending on crop type[16].

**Key Caveats and Limitations**: (1) Crop yield time series reflect integrated effects of all environmental variables (water, nutrients, pests, temperature, ozone); isolating ozone's contribution statistically requires advanced causal inference methods or experimental designs. (2) Crop yields in developed countries have been rising over time due to breeding for pest resistance and high-input agricultural practices, potentially masking ozone damage. (3) Yield data are reported at national or regional levels, not specifically for Key Biodiversity Areas (which are typically protected areas separate from agricultural land). (4) The relationship is only applicable in agricultural regions; most KBAs are non-agricultural. (5) Using downstream effects as proxies introduces reverse-causality concerns: if we use crop yields to infer ozone, we are using ozone's damage to predict ozone, which is circular.

**Citation**: FAO FAOSTAT, Our World in Data, USDA NASS[44].

---

### Photosynthetic Capacity and Forest Productivity Measurements

**Variable Name and Description**: Net Primary Productivity (NPP) derived from satellite MODIS data, measured as grams of carbon fixed per square meter per day (g C m⁻² day⁻¹). This reflects the photosynthetic capacity of vegetation and its responsiveness to ozone stress.

**Source Dataset**: NASA's MODIS instrument aboard Terra satellite provides monthly Net Primary Productivity estimates at 1 km resolution globally[19][45]. The data span from February 2000 to the present and reflect the cumulative carbon uptake by vegetation during photosynthesis minus respiration losses. Ground-based measurements of NPP are available through the National Ecological Observatory Network (NEON) at ten distributed forest sites in the eastern United States[45].

**Reported Correlation Strength and Sample**: Ozone impairs growth primarily by inhibiting net photosynthesis and photosynthate translocation processes[2]. Ozone exposure leads to reductions in leaf area, reduced transpiration, accelerated senescence, and ultimately reduced biomass accumulation and NPP[2][50]. The correlation between ozone exposure and NPP is expected to be strong and negative (r = -0.5 to -0.8), particularly in regions where ozone is elevated above background levels. Studies on elevated ozone in fumigation experiments show 11% reductions in tree biomass and, by extension, NPP[50].

**Expected Functional Form**: Approximately linear decline: \(NPP \approx NPP_0 - \rho \cdot OEB + \epsilon\), with \(\rho > 0\).

**Key Caveats and Limitations**: (1) MODIS NPP estimates have typical uncertainty of ±20-30% due to uncertainties in light-use efficiency parameterization and respiration estimates[45]. (2) NPP is affected by multiple environmental variables including water stress, nutrient availability, and temperature; ozone is only one driver. (3) MODIS NPP temporal resolution is monthly, creating smoothing that obscures acute ozone damage. (4) The relationship is potentially reversed for inference: NPP is a downstream consequence of ozone exposure, so using it as a proxy requires assuming that the causal pathway is unidirectional and that other confounders are controlled. (5) Satellite NPP estimates are difficult to validate at the pixel level due to spatial scale mismatches with ground measurements.

**Citation**: NASA MODIS NPP and NEON productivity measurements[19][45].

---

## Speculative Proxies: Novel Candidates Based on Causal Reasoning

Beyond the literature-validated proxies identified above, the causal map suggests several novel data sources that have not been extensively studied but that plausibly correlate with OEB. These represent opportunities for hypothesis-driven research.

### Ammonia Emissions and Livestock Stocking Density

**Variable Name and Description**: National or regional ammonia (NH₃) emissions from livestock and agricultural soils, measured in kilotonnes per year (kt yr⁻¹). Livestock stocking density (animals per hectare of pasture land) or total livestock population by country.

**Mechanistic Reasoning**: Ammonia emissions react with NOx to form ammonium nitrate aerosols and volatile compounds that can participate in ozone formation chemistry. Livestock systems contribute over 32% of total global N₂O emissions and are closely associated with ammonia releases from manure management and soil processes[30]. In regions with intensive animal agriculture adjacent to or affecting Key Biodiversity Areas, ammonia emissions could serve as a proxy for total reactive nitrogen availability that drives ozone formation. The correlation would be strongest in agricultural regions where livestock density is high and where wind patterns carry ammonia-rich air toward protected areas.

**Likely Data Source and Accessibility**: The EDGAR emissions inventory provides sector-specific ammonia emissions by country from 1970-2022, available openly at 0.1° × 0.1° gridded resolution[20]. The FAO provides livestock population statistics by country and year. National environmental agencies in Europe (under the National Emission Ceilings Directive) report ammonia emissions with high precision.

**Expected Direction and Strength of Correlation**: Positive correlation between ammonia emissions and ozone in agricultural KBAs (r = 0.2-0.4), particularly in regions where agriculture is intense (e.g., Indo-Gangetic Plain, parts of Europe, East Asia). In non-agricultural regions or regions with minimal livestock, the correlation would be weak or absent.

**Expected Functional Form**: Linear or threshold relationship: \(OEB \approx \sigma \cdot NH_3Emissions + \tau + \epsilon\), with stronger slopes in agricultural regions.

---

### Deforestation Rate and Forest Conversion to Agriculture

**Variable Name and Description**: Annual deforestation rate (hectares per year) or net forest loss (hectares per year), derived from satellite monitoring. The proportion of country land area that has been converted to agriculture or human use in recent decades.

**Mechanistic Reasoning**: Deforestation reduces biogenic VOC emission potential (fewer trees = fewer isoprene-emitting plants), which could lower ozone formation in VOC-limited regimes. However, deforestation is typically accompanied by land-use conversion to agriculture and increased human economic activity (roads, farming), which increases anthropogenic NOx and VOC emissions. The net effect is ambiguous: deforestation could either increase or decrease ozone depending on whether the loss of biogenic emissions outweighs the increase in anthropogenic activity. Additionally, deforested land often has higher surface temperatures and more exposed soil, which could intensify photochemical ozone formation. The causal mechanism is mechanistically plausible but directionally ambiguous.

**Likely Data Source and Accessibility**: Global Forest Watch provides satellite-derived forest loss data at 30 m resolution annually since 2000, available freely through NASA's GLAD database and WRI platforms. NASA's MODIS instruments provide forest cover change products. National forest monitoring systems provide official deforestation statistics in most tropical countries.

**Expected Direction and Strength of Correlation**: Unclear sign; possibly weak overall (r = |0.2-0.3|). In tropical regions with extensive forest loss and minimal industrial NOx sources, deforestation could correlate with reduced ozone. In regions converting forest to intensive agriculture or urban development, deforestation could correlate with increased ozone due to accompanying industrial activity.

**Expected Functional Form**: Potentially threshold-dependent or interaction-based, requiring decomposition of deforestation into types (forest to agriculture, forest to urban, forest degradation vs. complete conversion).

---

### Meteorological and Climate Extremes: Heat Waves, Drought, and Stagnation Episodes

**Variable Name and Description**: Frequency and intensity of extreme heat events (days with maximum temperature >35°C or >2 standard deviations above historical normal), drought severity indices (Standardized Precipitation Index, Palmer Drought Severity Index, or U.S. Drought Monitor classifications), and stagnation episode frequency (anticyclonic days or days with wind speeds <1.5 m/s).

**Mechanistic Reasoning**: Photochemical ozone formation accelerates at higher temperatures, and ozone concentrations reach unhealthy levels on hot sunny days[1]. Heat extremes often coincide with high solar radiation and suppressed vertical mixing (anticyclonic conditions), which are ideal for ozone accumulation[22]. Drought stress on vegetation can alter stomatal conductance and VOC emission rates, potentially affecting local ozone formation and uptake by plants. Stagnation events that suppress vertical mixing allow surface ozone and precursors to accumulate. Thus, frequency of heat waves and stagnation episodes should correlate with ozone exposure in KBAs.

**Likely Data Source and Accessibility**: Climate model output from CMIP6 and CMIP5 ensembles provides projections of heat waves and drought frequency under different emissions scenarios. The U.S. Drought Monitor provides observed drought classification data weekly for the United States with high spatial detail[36]. NOAA and national meteorological services provide historical records of extreme temperature and wind events. The C2ES Climate Center synthesizes heat-wave trend data for the United States[35].

**Expected Direction and Strength of Correlation**: Positive correlation between heat-wave frequency and ozone exposure (r = 0.4-0.6). Positive correlation between stagnation episode frequency and ozone (r = 0.5-0.7), particularly for episodic ozone concentrations. Drought effects are more ambiguous due to complex plant physiological responses.

**Expected Functional Form**: Approximately linear: \(OEB \approx \upsilon \cdot HeatWaveFrequency + \phi \cdot StagnationDays + \epsilon\). For drought: non-monotonic or threshold-dependent.

---

### Nighttime Lights and Economic Activity Proxy

**Variable Name and Description**: Annual average nighttime lights (radiance in nanoWatts per steradian per cm²) derived from satellite instruments (NOAA VIIRS DNB, DMSP-OLS), aggregated to country or gridded 1 km resolution. This serves as a spatially-explicit proxy for human economic activity and energy use.

**Mechanistic Reasoning**: Nighttime lights are correlated with urbanization, industrial activity, vehicle traffic, and electricity consumption—all sources of NOx and VOCs[11][14]. However, nighttime lights are also correlated with GDP per capita, which we have explicitly excluded as a confounder. The mechanistic link is indirect: lights → energy use → emissions → ozone. The proxy would only be useful if lights capture spatial variation in economic activity not explained by GDP at the country level.

**Likely Data Source and Accessibility**: NOAA's Earth Observation Group provides monthly, annual, and multi-year composites of VIIRS nighttime lights data at 15 arc-second (~500 m) resolution, freely available through Google Earth Engine and NOAA servers. DMSP-OLS historical data (1992-2013) are archived at NOAA and NOAA's National Centers for Environmental Information.

**Expected Direction and Strength of Correlation**: Positive correlation between nighttime lights intensity and ozone in regions with bright night lights indicating high economic activity (r = 0.4-0.6). However, this correlation may be confounded by GDP per capita and urbanization, limiting its independent predictive value.

**Expected Functional Form**: Log-linear: \(OEB \approx \chi \cdot \log(NighttimeLights) + \psi + \epsilon\).

---

### Air Pollutant Co-concentrations: NO₂, PM₂.₅, and SO₂

**Variable Name and Description**: Annual mean concentrations of nitrogen dioxide (NO₂ in ppb), fine particulate matter (PM₂.₅ in μg m⁻³), and sulfur dioxide (SO₂ in ppb) measured at ground-based air quality monitoring stations or estimated from satellite instruments and chemical transport models.

**Mechanistic Reasoning**: NOx and ozone are chemically coupled—NO reacts with ozone, affecting the ozone concentration. PM₂.₅ and ozone co-occur in photochemical smog episodes. SO₂ is emitted alongside NOx from fossil fuel combustion and is an independent marker of combustion activity. If air quality monitoring stations in or near KBAs measure NO₂, PM₂.₅, and SO₂, these co-pollutants would likely correlate strongly with ozone because they share common emission sources and atmospheric conditions. This would be the most direct measurement-based proxy possible.

**Likely Data Source and Accessibility**: The World Air Quality Index (WAQI) aggregates real-time and historical air quality data from >10,000 monitoring stations globally, covering PM₂.₅, PM₁₀, NO₂, SO₂, CO, and O₃[17][17]. The data are updated hourly but are more complete in developed countries and urban areas; coverage in rural KBAs is sparse. The CAMS global reanalysis provides 3D fields of NO₂, SO₂, and other pollutants at 80 km resolution from 2003-2024[4]. EPA's interactive map of air quality monitors provides access to U.S. data[41].

**Expected Direction and Strength of Correlation**: Strong positive correlations: NO₂ ↔ O₃ (r = 0.6-0.8, with some negative correlation in NO-dominated regimes), PM₂.₅ ↔ O₃ (r = 0.5-0.7), SO₂ ↔ O₃ (r = 0.4-0.6). This would be an excellent proxy in regions with dense monitoring networks.

**Expected Functional Form**: Approximately linear for NO₂ and SO₂; potential non-linearity for PM₂.₅ due to interactions with humidity and optical effects.

---

### Carbon Sequestration Rate and Forest Biomass Accumulation

**Variable Name and Description**: Change in forest above-ground biomass per year (tonnes C ha⁻¹ yr⁻¹) or estimates of carbon sequestration potential from optical remote sensing and allometric models.

**Mechanistic Reasoning**: Ozone reduces net carbon assimilation by impairing photosynthesis, which should translate to reduced biomass accumulation and carbon sequestration. Forests in high-ozone regions should accumulate biomass more slowly than those in low-ozone regions. This is a direct physiological consequence of ozone damage to photosynthetic apparatus[7][24][50]. However, many other factors affect biomass accumulation (water availability, temperature, nutrients, forest age, fire, pest outbreaks), creating substantial noise in this relationship.

**Likely Data Source and Accessibility**: The NASA GEDI (Global Ecosystem Dynamics Investigation) lidar instrument provides estimates of forest structure and above-ground biomass globally at ~25 m resolution since 2019, available through NASA's Oak Ridge National Laboratory Distributed Active Archive Center (ORNL DAAC). Optical remote sensing-based biomass estimates are available from the ESA's Copernicus Climate Change Service (C3S) at 100 m resolution. The NEON program measures annual tree diameter growth at ten forest sites, from which biomass accumulation can be calculated[45].

**Expected Direction and Strength of Correlation**: Negative correlation between ozone exposure and biomass accumulation rate (r = -0.3 to -0.6), with high residual variance from other environmental drivers.

**Expected Functional Form**: Linear decline: \(BiomassAccumulation \approx B_0 - \omega \cdot OEB + \epsilon\).

---

### Wildfire Frequency and Biomass Burning Emissions

**Variable Name and Description**: Annual area burned by wildfires (hectares per year) or carbon emissions from biomass burning (megatonnes CO₂ yr⁻¹), derived from satellite burnt-area products or fire emission inventories.

**Mechanistic Reasoning**: Wildfires emit large quantities of NOx, VOCs, and organic aerosols that participate in ozone chemistry. In regions prone to wildfires, particularly during drought years, biomass burning can be a major source of ozone precursors and can contribute to elevated regional ozone concentrations[29]. Conversely, ozone-induced forest damage increases fuel load and fire susceptibility, creating a potential feedback loop. The relationship is mechanistically plausible but directionally ambiguous regarding causality.

**Likely Data Source and Accessibility**: NASA's Moderate Resolution Imaging Spectroradiometer (MODIS) instruments track global burnt area with the MCD64A1 product at 500 m resolution monthly since 2000, available from NASA's Land Processes DAAC[29]. The Global Fire Emissions Database (GFED) integrates satellite burnt area with emission factors to estimate carbon and trace gas emissions from wildfires[29]. The Copernicus Emergency Management Service provides rapid burnt area mapping for recent fires.

**Expected Direction and Strength of Correlation**: Positive correlation between wildfire area/emissions and ozone, particularly in regions with frequent wildfires (r = 0.3-0.5). Strongest in regions like Mediterranean, parts of western North America, and Australia where wildfires are tied to seasonal cycles and climate extremes.

**Expected Functional Form**: Approximately linear or log-linear: \(OEB \approx \gamma_{fire} \cdot \log(BurntArea + 1) + \epsilon\).

---

### Pollen Production and Allergenic Pollen Concentrations

**Variable Name and Description**: Annual pollen counts (grains per cubic meter) or estimated pollen production from models, particularly for ozone-sensitive allergenic taxa like ragweed, grasses, and oak. This serves as a biological indicator of plant reproductive output under ozone stress.

**Mechanistic Reasoning**: Ozone inhibits pollen tube growth and reduces pollen viability[2]. It also accelerates plant senescence, potentially shortening the breeding season. Therefore, regions with high ambient ozone should show reduced pollen production compared to low-ozone regions. Pollen concentrations are directly measured at aerobiological monitoring stations and are publicly available in many countries, making this a potentially accessible proxy. However, pollen production is affected by temperature, humidity, precipitation timing (which triggers flowering), and plant genotype diversity, creating substantial confounding.

**Likely Data Source and Accessibility**: Aerobiological monitoring networks across Europe, North America, and increasingly Asia maintain long-term pollen count records. The European Aerobiology Network and the International Association of Aerobiology coordinate these data. Country-specific pollen information is available from national allergy organizations and environmental health agencies. However, coverage is heterogeneous—Europe and North America have dense networks, while Africa, South America, and most of Asia have sparse coverage. Data are typically reported annually.

**Expected Direction and Strength of Correlation**: Negative correlation between ozone and pollen counts in ozone-sensitive taxa (r = -0.2 to -0.4), with high variability due to confounding by temperature and precipitation timing.

**Expected Functional Form**: Log-linear decline: \(PollenCount \approx P_0 \cdot e^{-\delta \cdot OEB} + \epsilon\).

---

## Data Availability Assessment

To operationalize proxy candidates, we must assess their geographic coverage, temporal resolution, accessibility, and format. This section provides a structured evaluation.

| **Proxy Variable** | **Geographic Coverage** | **Temporal Resolution** | **Accessibility** | **Format** | **Key Limitations** |
|---|---|---|---|---|---|
| **Satellite NO₂ Columns** (OMI, TROPOMI) | Global | Daily to monthly | Open (NASA, ESA) | NetCDF, HDF5 | Cloud contamination, retrieval uncertainty ±15-20% |
| **MEGAN BVOC Emissions** | Global | Monthly | Open (NCAR) | NetCDF, gridded | Model-dependent, high uncertainty in tropical regions |
| **Vehicle Ownership** | ~180 countries | Annual or 5-year | Restricted (OICA requires membership) | CSV, Excel | Reporting delays, incomplete for developing countries |
| **Industrial Energy Use** (IEA) | ~150 countries | Annual | Paid subscription | Excel, PDF | Significant reporting lags (2-3 years) |
| **EDGAR Emissions Inventory** | Global, ~250 countries | Annual (latest 2022) | Open | NetCDF, gridded | Methodological inconsistencies, 2-3 year lag |
| **Solar Radiation** (CERES) | Global | Monthly | Open (NASA) | NetCDF | ±5-10% uncertainty, cloud-dependent |
| **Boundary Layer Height** (ERA5, MERRA-2) | Global | Daily/hourly | Open (Copernicus, MERRA) | NetCDF, gridded | Systematic biases, validation challenges |
| **Crop Yields** (FAO FAOSTAT) | ~200 countries | Annual | Open | CSV, Excel | Multiple confounders, not KBA-specific |
| **MODIS NPP** | Global | Monthly | Open (NASA) | HDF4, GeoTIFF | ±20-30% uncertainty, 500 m resolution |
| **Forest Loss** (GFW, NASA GLAD) | Tropical regions primarily | Annual | Open | Raster, GeoTIFF | Limited coverage outside tropics; 30 m resolution |
| **Nighttime Lights** (VIIRS DNB) | Global | Monthly/annual | Open (NOAA) | GeoTIFF, NetCDF | Saturation in brightest urban areas |
| **Air Quality Monitoring** (WAQI, EPA) | Sparse globally, dense in developed countries | Hourly/daily | Open (real-time; historical may require registration) | JSON API, CSV | Highly heterogeneous spatial coverage |
| **GEDI Biomass** | ±51.6° latitude | 2019-present | Open (NASA ORNL DAAC) | HDF5 | Limited temporal depth; sparse in tropics |
| **Burnt Area** (MODIS MCD64A1) | Global | Monthly | Open | HDF4, GeoTIFF | 500 m resolution, commission/omission errors |
| **Pollen Counts** | Europe, North America; sparse elsewhere | Annual to weekly | Heterogeneous (some open, many restricted) | CSV, Excel, PDF | Extremely sparse coverage in KBAs and developing regions |

---

## Confounder Analysis

Several variables could create spurious correlations between proxy candidates and OEB, leading to false causal inference. Beyond GDP per capita, urbanization, and population (which we have explicitly excluded), the following confounders merit careful attention:

### Regional Geographic Clustering

Many environmental variables—including ozone, precursor emissions, climate, vegetation type, and development stage—are regionally clustered. Europe, North America, and East Asia all experience elevated ozone due to high precursor emissions concentrations. Tropical regions have naturally high temperatures that accelerate photochemical reactions. Regions with high forest productivity (Southeast Asia, Amazon) have naturally high biogenic emissions. This regional autocorrelation means that a proxy variable that correlates with ozone in one region (e.g., vehicle ownership in North America) may not generalize to other regions (e.g., vehicle ownership in Africa, where vehicles are scarce but ozone is still elevated due to transboundary transport from other regions). **Mitigation**: Include regional fixed effects or clustering in regression models.

### Transboundary Ozone Transport

Ozone concentrations in many regions are dominated by long-range transport rather than local emissions. The eastern Mediterranean experiences ozone maxima driven by European anthropogenic emissions[22]. Rural areas in eastern North America experience ozone driven by upwind Midwestern industrial and power-generation NOx emissions. This means that local emission proxies will be poor predictors in regions where ozone is advected from distant sources. **Mitigation**: Account for prevailing wind patterns and upwind source regions; consider distance-weighted emission fields rather than local emissions alone.

### Climate and Meteorological Variability

Year-to-year variation in temperature, solar radiation, humidity, and wind speed drives substantial variation in photochemical ozone formation independent of emission changes. A country with constant emissions can experience 30-50% year-to-year variation in ozone concentrations due to meteorological fluctuations[12]. This creates noise in any proxy that does not account for inter-annual meteorological variation. **Mitigation**: Use meteorologically-normalized ozone metrics (e.g., ozone adjusted for temperature and wind anomalies) or include meteorological covariates in statistical models.

### Vegetation Type and Forest Productivity Feedback

Regions with naturally high forest productivity emit large quantities of biogenic VOCs that can feed back to increase ozone formation (in NOx-limited regimes). Thus, high NPP or NDVI could correlate with ozone not because NPP is damaged by ozone, but because high productivity generates high BVOC emissions. **Mitigation**: Separate background biogenic emissions from ozone-induced productivity losses using structural equation models or difference-in-differences designs comparing ozone-sensitive vs. ozone-resistant species.

### Technology Adoption and Emission Control

Emission controls (catalytic converters, SCR on diesel engines, industrial pollution control) can reduce NOx and VOCs dramatically without changing production volumes[8]. Thus, vehicle ownership or industrial production can be decoupled from actual emissions. A country with strict Euro 6 diesel standards and recent vehicle fleet turnover will have much lower ozone-precursor emissions than a country with the same vehicle ownership but older, less-controlled vehicles. **Mitigation**: Use satellite-derived NO₂ measurements (which reflect actual emissions) rather than activity indicators; or construct instrument variables for pollution control stringency (e.g., years since adoption of emission standards).

### Seasonal and Inter-annual Variability in Agricultural Practices

Crop yields vary substantially due to farmer responses to price signals, pest outbreaks, and weather—factors unrelated to ozone. Using crop yield as a proxy for ozone introduces this variability as noise. **Mitigation**: Use long-term (10+ year) detrended yield anomalies rather than raw yields; or use experimental yield loss estimates from controlled ozone fumigation studies, which isolate ozone effects.

---

## Ranked List of Top Proxy Candidates

Based on expected correlation strength, data availability, geographic coverage, mechanistic plausibility, and resistance to confounding, the following ranking emerges:

### **Rank 1: Satellite-Derived Tropospheric NO₂ Column Concentrations**
- **One-line Summary**: Satellite measurements of tropospheric NO₂ density (molecules cm⁻²) from OMI, TROPOMI, or CAMS reanalysis capture the primary NOx precursor for ozone formation.
- **Expected Relationship**: Positive correlation with OEB in NOx-limited regimes (most of the world); magnitude r = 0.5-0.7 in agricultural and rural KBAs. Weaker in VOC-limited urban areas.
- **Data Source**: CAMS global reanalysis (2003-2024, 80 km resolution, freely available); TROPOMI/S5P (2017-present, 5.5×3.5 km resolution, free); OMI (2004-present, 13×24 km resolution, free).
- **Justification**: This proxy is mechanistically most direct (NOx is a reactant in ozone formation), has global coverage, frequent updates, open access, and validation against ground measurements. The relationship is chemically understood. The only significant limitation is distinguishing NOx-limited from VOC-limited regimes, requiring regional context.

### **Rank 2: Boundary Layer Height and Stagnation Indices**
- **One-line Summary**: Planetary boundary layer height (PBL) derived from radiosonde profiles or reanalysis; lower PBL height suppresses vertical mixing and concentrates surface ozone.
- **Expected Relationship**: Negative correlation; lower PBL height → higher OEB. r = -0.5 to -0.7.
- **Data Source**: ERA5 reanalysis (globally gridded, daily, 31 km resolution, free via Copernicus Climate Data Store); MERRA-2 (free via GES DISC); radiosonde profiles (sparse network, particularly over oceans and developing countries).
- **Justification**: This captures the meteorological conditions that determine whether ozone accumulates at the surface or is dispersed. The mechanism is well-established. Reanalysis data are freely available globally at high temporal resolution. The limitation is that PBL height is a climate/weather variable correlated with many other environmental factors, reducing its independent explanatory power.

### **Rank 3: Air Quality Co-pollutant Measurements (NO₂, PM₂.₅, SO₂)**
- **One-line Summary**: Ground-based measurements of NO₂, PM₂.₅, and SO₂ from air quality monitoring stations or satellite/model estimates capture pollutants chemically and emissionally coupled to ozone.
- **Expected Relationship**: Strong positive correlations with OEB in regions with monitoring coverage. r = 0.6-0.8 for NO₂, r = 0.5-0.7 for PM₂.₅.
- **Data Source**: WAQI (real-time data from >10,000 stations, API access, free); CAMS reanalysis (global gridded, 80 km, 2003-2024); EPA AirData (U.S. only).
- **Justification**: This is the most direct measurement of ozone's chemical copollutants, making it mechanistically transparent. Data are readily accessible and frequently updated. The primary limitation is that monitoring stations are sparse in rural KBAs and developing countries, limiting global applicability.

### **Rank 4: Industrial Sector Energy Consumption and Cement Production**
- **One-line Summary**: National or sub-national fuel consumption in energy-intensive industries (power plants, cement, steel, chemicals) and production volumes capture anthropogenic NOx and VOC sources.
- **Expected Relationship**: Positive correlation with OEB in regions where industrial activity is concentrated near KBAs. r = 0.4-0.6. Weaker in regions where industrial emissions are geographically isolated from KBAs.
- **Data Source**: EDGAR emissions inventory (global, 0.1° × 0.1° gridded, 1970-2022, free); IEA energy statistics (150+ countries, annual, subscription-based); World Economic Forum cement data (free); national industrial statistics (heterogeneous availability).
- **Justification**: Industrial energy use directly drives NOx and VOC emissions. The spatial gridded nature of EDGAR allows matching to KBA locations. The limitations are reporting lags (2-3 years), methodological inconsistencies between countries, and the need to infer actual emissions from production volumes (confounded by pollution control adoption).

### **Rank 5: Biogenic VOC Emission Potential (MEGAN Model Outputs)**
- **One-line Summary**: Modeled isoprene and monoterpene emissions at standard conditions from MEGAN 2.1, reflecting the VOC-emitting capacity of vegetation in a region.
- **Expected Relationship**: Context-dependent; positive in NOx-limited regions (r = 0.3-0.5), near-zero or negative in VOC-limited regions.
- **Data Source**: MEGAN 2.1 outputs (gridded monthly, global, free from NCAR); satellite NDVI (free from NASA).
- **Justification**: BVOC emissions are mechanistically important in ozone formation and interact with anthropogenic NOx. MEGAN is the standard modeling framework. The limitation is that the relationship is strongly NOx-VOC regime dependent, requiring regional calibration, and MEGAN outputs have significant model uncertainty in tropical regions.

### **Rank 6: Meteorological Extremes: Heat-Wave Frequency and Stagnation Days**
- **One-line Summary**: Annual count of heat-wave days (temperature >2 SD above normal) or stagnation episodes (anticyclonic days, weak-wind days) that suppress vertical mixing and drive ozone formation.
- **Expected Relationship**: Positive correlation with OEB. r = 0.4-0.6.
- **Data Source**: Reanalysis data (ERA5, MERRA-2) from which extremes can be calculated (free); NOAA climate monitoring products (free); national meteorological services (variable accessibility).
- **Justification**: High temperature and suppressed mixing are direct drivers of photochemical ozone formation. Data are derived from freely-available reanalysis. The limitation is that these are climate/weather variables correlated with many other environmental outcomes, reducing specificity.

### **Rank 7: Nighttime Lights as an Economic Activity Proxy**
- **One-line Summary**: Annual average nighttime radiance (nanoWatts sr⁻¹ cm⁻²) from VIIRS DNB, indicating localized energy use and economic activity and thus precursor emissions.
- **Expected Relationship**: Positive correlation with OEB in regions with bright night lights indicating high economic activity. r = 0.3-0.5.
- **Data Source**: NOAA Earth Observation Group (VIIRS DNB, 500 m resolution, monthly/annual, free via Google Earth Engine and NOAA servers).
- **Justification**: Nighttime lights are a spatially-explicit proxy for emissions not available from national economic statistics. Google Earth Engine integration makes processing accessible. The limitations are that nighttime lights correlate strongly with GDP per capita (a confounder we want to exclude) and saturation in very bright urban areas.

---

## Synthesis and Recommendations for Integration

The identified proxy candidates fall into three categories with different strengths and use cases:

**Mechanistically-Direct Proxies** (Ranks 1-3: NO₂ columns, PBL height, co-pollutants) are most suitable for validation of the existing OEB indicator and for identifying regions where satellite-based ozone monitoring is consistent with precursor and meteorological data. These proxies would enable the EPI team to assess whether year-to-year variations in OEB align with expectations from photochemistry and meteorology.

**Emission-Source Proxies** (Ranks 4-5: industrial energy, BVOC emissions) are most suitable for forward-looking analysis of ozone trends in relation to economic development and land-use change. These proxies would enable scenario analysis: what ozone exposure would be expected if vehicle ownership increases by 50%? If forest productivity changes?

**Climate-Meteorological Proxies** (Ranks 6-7: heat waves, nighttime lights) are most suitable for separating ozone signal from climate noise and for understanding how climate change may alter future ozone exposure independent of emissions changes. These proxies would enable analysis of climate-ozone-biodiversity interactions.

For the EPI team's immediate objective of finding alternative data sources for hard-to-measure OEB, we recommend a **tiered validation approach**:

1. **Tier 1 (Immediate, 0-6 months)**: Validate existing OEB indicator against Rank 1 proxy (satellite NO₂ columns) at the country and regional level. Compute correlations, examine residuals, and identify regions where ozone and NO₂ diverge unexpectedly (potential indications of VOC limitation or transboundary transport).

2. **Tier 2 (Near-term, 6-18 months)**: Develop a **multi-source ozone exposure index** combining NO₂ columns, PBL height, and temperature from reanalysis to create a mechanistically-informed synthetic ozone estimate that is independent of direct ozone measurement. Compare this synthetic estimate to CAMS-based OEB to assess consistency.

3. **Tier 3 (Medium-term, 18-36 months)**: Construct spatial models linking OEB to precursor emissions (EDGAR), industrial activity (satellite nighttime lights), vehicle ownership, and meteorology (ERA5). Use these models to identify the spatial and temporal drivers of ozone variation and to project future ozone exposure under different development and climate scenarios.

4. **Tier 4 (Long-term)**: Develop mechanistic ozone models for specific regions (e.g., Indo-Gangetic Plain, eastern China, Mediterranean, eastern North America) that explicitly resolve NOx-VOC regimes and validate against KBA-specific ground measurements and ecosystem productivity data.

This tiered approach leverages the mechanistic understanding of ozone formation to progressively refine proxy selection and to develop a more robust, transparent methodology for OEB estimation that the EPI team can defend and update as new data become available.

## References
[1] https://www.epa.gov/ground-level-ozone-pollution/ground-level-ozone-basics
[2] https://www.nrcs.usda.gov/sites/default/files/2022-10/Ozone-Research-Review.pdf
[3] https://epi.yale.edu/measure/2024/OEB
[4] https://www.ecmwf.int/en/forecasts/dataset/cams-global-reanalysis
[5] https://wdkba.keybiodiversityareas.org
[6] https://data.jncc.gov.uk/data/6fc8a282-18bc-4c07-b197-6ff78f536fa7/JNCC-Report-403-FINAL-WEB.pdf
[7] https://pubmed.ncbi.nlm.nih.gov/32981434/
[8] https://theicct.org/stack/vehicle-nox-emissions-the-basics/
[9] https://www.epa.gov/indoor-air-quality-iaq/what-are-volatile-organic-compounds-vocs
[10] https://www.eea.europa.eu/en/analysis/maps-and-charts/emissions-of-ozone-precursors-eea-member-countries-1
[11] https://resourcewatch.org/data/explore/Air-Quality-Measurements-TROPOMI-NO
[12] https://pmc.ncbi.nlm.nih.gov/articles/PMC7721827/
[13] https://chem.libretexts.org/Bookshelves/General_Chemistry/Book:_Structure_and_Reactivity_in_Organic_Biological_and_Inorganic_Chemistry_(Schaller)/V:__Reactivity_in_Organic_Biological_and_Inorganic_Chemistry_3/08:_Photochemical_Reactions/8.05:_Atmospheric_Photochemistry-_Ozone
[14] https://pmc.ncbi.nlm.nih.gov/articles/PMC3454441/
[15] https://www.earthdata.nasa.gov/topics/normalized-difference-vegetation-index-ndvi
[16] https://pubmed.ncbi.nlm.nih.gov/15092541/
[17] https://waqi.info
[18] https://www.eia.gov/energyexplained/use-of-energy/industry.php
[19] https://svs.gsfc.nasa.gov/30380/
[20] https://edgar.jrc.ec.europa.eu/emissions_data_and_maps
[21] https://pollution.sustainability-directory.com/learn/why-is-photochemical-smog-considered-a-major-urban-pollution-problem/
[22] https://acp.copernicus.org/articles/13/2331/2013/acp-13-2331-2013.pdf
[23] https://onlinelibrary.wiley.com/doi/10.1111/opec.70000?af=R
[24] https://bg.copernicus.org/articles/15/6941/2018/
[25] https://pubmed.ncbi.nlm.nih.gov/15091514/
[26] https://amt.copernicus.org/articles/15/5563/2022/
[27] https://egusphere.copernicus.org/preprints/2024/egusphere-2024-2199/
[28] https://www.weforum.org/stories/2024/09/cement-production-sustainable-concrete-co2-emissions/
[29] https://pmc.ncbi.nlm.nih.gov/articles/PMC3763857/
[30] https://acsess.onlinelibrary.wiley.com/doi/10.1002/jeq2.20259
[31] https://pubs.er.usgs.gov/publication/70123822
[32] https://www.iucnredlist.org
[33] https://www.cbd.int/protected-old/pame.shtml
[34] https://ourworldindata.org/deforestation
[35] https://www.c2es.org/content/heat-waves-and-climate-change/
[36] https://droughtmonitor.unl.edu/About/AbouttheData/DroughtClassification.aspx
[37] https://www.ncei.noaa.gov/products/climate-data-records/total-solar-irradiance
[38] https://icpvegetation.ceh.ac.uk/sites/default/files/Flux-based%20critical%20levels%20of%20ozone%20pollution%20for%20vegetation.pdf
[39] https://bg.copernicus.org/articles/15/5395/2018/
[40] https://pubmed.ncbi.nlm.nih.gov/16815609/
[41] https://www.epa.gov/outdoor-air-quality-data/interactive-map-air-quality-monitors
[42] https://www.earthdata.nasa.gov/es/data/catalog/ges-disc-trco3-monthly-omimls-2
[43] https://pollution.sustainability-directory.com/learn/what-is-the-concept-of-nox-limited-vs-voc-limited-ozone-formation/
[44] https://ourworldindata.org/crop-yields
[45] https://www.neonscience.org/impact/observatory-blog/examining-drivers-forest-productivity
[46] https://pmc.ncbi.nlm.nih.gov/articles/PMC5621656/
[47] https://bg.copernicus.org/articles/18/2487/2021/
[48] https://electroiq.com/stats/car-ownership-statistics/
[49] https://svs.gsfc.nasa.gov/31253/
[50] https://pmc.ncbi.nlm.nih.gov/articles/PMC7536038/