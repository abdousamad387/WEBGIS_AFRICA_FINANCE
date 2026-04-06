# Africa Finance Observatory -- WebGIS Platform

## Table of Contents

1. [Introduction](#1-introduction)
2. [Context](#2-context)
3. [Justification](#3-justification)
4. [Study Objectives](#4-study-objectives)
5. [Methodology](#5-methodology)
6. [Technical Architecture](#6-technical-architecture)
7. [Data Description](#7-data-description)
8. [Functional Features](#8-functional-features)
9. [Results](#9-results)
10. [Discussion](#10-discussion)
11. [Limitations and Future Work](#11-limitations-and-future-work)
12. [Conclusion](#12-conclusion)
13. [Installation and Deployment](#13-installation-and-deployment)
14. [References](#14-references)

---

## 1. Introduction

The Africa Finance Observatory WebGIS is an interactive geospatial decision-support platform designed to visualize, analyze and explore the financial and macroeconomic landscape of the African continent. Covering 54 countries over a 25-year period (2000--2024), the platform integrates multidimensional financial data with geographic information systems to produce a comprehensive spatial analysis tool.

This project bridges the gap between traditional statistical reporting and modern geovisualization, enabling policymakers, researchers, financial analysts and development practitioners to examine spatial patterns, temporal dynamics and cross-country disparities in African financial development. The platform operates entirely in a web browser, requires no server-side processing for end users, and is deployed as a static site via GitHub Pages.

---

## 2. Context

Sub-Saharan Africa and North Africa constitute a heterogeneous financial space where banking penetration, capital market depth, mobile money adoption and macroeconomic stability vary enormously from one country to another. Over the past two decades, the continent has experienced rapid transformations: the mobile money revolution originating in East Africa, significant improvements in banking regulation across West Africa, sovereign debt challenges in several economies, and the emergence of fintech ecosystems in countries such as Nigeria, Kenya, South Africa and Egypt.

Despite these developments, available analytical tools for monitoring African financial systems remain fragmented. Data from international institutions (World Bank, IMF, African Development Bank) is typically presented in tabular format or through generic dashboards that lack spatial context. Geographic information systems, which are widely used in environmental science and urban planning, remain underutilized in the domain of financial analysis on the African continent.

This project responds to the need for a spatially explicit, temporally dynamic and analytically rich platform that synthesizes multiple dimensions of financial development into a single interactive interface.

---

## 3. Justification

The development of this WebGIS platform is justified by the following considerations:

**Analytical gap.** Existing financial monitoring tools for Africa rarely integrate geospatial analysis. Country-level data is typically presented in tables or static charts, which obscure spatial patterns such as regional clustering, neighborhood effects and geographic corridors of financial development.

**Decision-support requirements.** International organizations, central banks, ministries of finance and development agencies require tools that enable rapid visual comparison across countries and over time. A WebGIS satisfies this need by offering interactive choropleth mapping, temporal animation and on-the-fly spatial queries.

**Data integration complexity.** African financial data spans multiple domains (macroeconomics, banking, fintech, microfinance) with different sources, units and coverage. This platform performs the necessary harmonization, cross-referencing 53 countries across 6 thematic datasets and 16 core indicators.

**Accessibility.** By deploying the platform as a static website, it becomes accessible to any user with a web browser, without requiring software installation, database connections or specialized GIS training. The bilingual interface (English and French) further extends accessibility to the two major working languages of the African Union.

**Reproducibility.** The entire data pipeline, from raw Excel to GeoJSON and JSON payloads, is implemented in a single Python script. This ensures that the analysis can be reproduced, updated and audited.

---

## 4. Study Objectives

### 4.1 General Objective

To design and implement a professional-grade WebGIS platform for the spatial analysis and interactive visualization of financial and macroeconomic indicators across the African continent over the period 2000--2024.

### 4.2 Specific Objectives

1. To construct a structured geospatial database linking country-level financial indicators to geographic boundaries derived from Natural Earth data.
2. To develop an automated data pipeline (ETL) that extracts, transforms and loads multidimensional financial data from a structured Excel workbook into optimized JSON payloads suitable for web mapping.
3. To implement a feature-rich WebGIS application supporting thematic cartography (choropleth, proportional circles, heatmaps), temporal animation, spatial queries, attribute table exploration and statistical analytics.
4. To enable comparative analysis through interactive ranking systems, Top 10 charts, continental time-series and country-level detail panels.
5. To deploy the platform as a publicly accessible, self-contained static website requiring no backend infrastructure.
6. To provide a bilingual interface (English and French) to serve the diverse linguistic needs of African stakeholders.

---

## 5. Methodology

### 5.1 Data Collection

The primary data source is the **AfricaFinance Database 2000--2024**, a structured Excel workbook containing six thematic sheets:

| Sheet | Domain | Key Variables |
|---|---|---|
| Macroeconomics (Annual) | National accounts, trade, demographics | GDP, GDP/capita, growth rate, inflation, public debt, FDI, unemployment, HDI, current account balance, remittances, reserves, policy rate |
| Banking Sector (Annual) | Banking system performance | Banking rate, NPL ratio, CAR, ROE, ROA, NIM, credit-to-GDP, interest rate spread, number of banks, deposits-to-GDP, branches and ATMs per 100k |
| Fintech and Mobile Money | Digital financial services | Mobile money accounts, transaction volumes, population coverage, fintech startups, fintech investment, digital payment share, smartphone penetration |
| Microfinance and Inclusion | Financial inclusion | PAR30, operational self-sufficiency, financial inclusion score, active MFI clients, MFI count, microcredit portfolio, share of female clients |
| Country Profiles | Structural information | Currency, central bank name, stock exchange, population, geographic coordinates |
| Crises and Shocks | Financial disruptions | Crisis type, severity index (1--5), GDP impact, affected countries and years |

Geographic boundaries are sourced from **Natural Earth** (1:50m cultural vectors), providing high-resolution MultiPolygon geometries for all 55 African features (54 sovereign states plus Bir Tawil).

### 5.2 Data Processing Pipeline

The ETL pipeline is implemented in `build_webgis.py` (Python 3, pandas, numpy, openpyxl) and performs the following operations:

1. **GeoJSON preprocessing.** The raw Natural Earth GeoJSON (2.6 MB, approximately 160 properties per feature) is trimmed to retain only 16 essential properties (ISO_A3, NAME, ADMIN, REGION_WB, SUBREGION, POP_EST, GDP_MD, LABEL_X, LABEL_Y, etc.), reducing file size to approximately 2.3 MB.

2. **Excel ingestion.** Six thematic sheets are read with explicit column mapping dictionaries (MACRO_MAP, BANK_MAP, FINT_MAP, MFI_MAP) that translate French-language column headers from the original database into standardized internal keys.

3. **Country harmonization.** A comprehensive ISO3_MAP dictionary maps 53 French country names to ISO 3166-1 alpha-3 codes, enabling reliable joins between tabular data and geographic features.

4. **Indicator matrix construction.** For each year (2000--2024) and each country, the pipeline merges macroeconomic, banking, fintech and microfinance data into a single record containing up to 40 variables.

5. **Derived computations.** Continental KPIs (totals, averages), country-level time series, rankings (top and bottom 10 for 10 variables) and regional aggregations are computed programmatically.

6. **Type safety.** A custom JSON encoder (NpEncoder) handles numpy data types (int64, float64, bool_) to ensure serialization compatibility.

7. **Output.** Two files are produced: `africa.geojson` (geographic layer) and `indicators.json` (analytical payload containing indicators, KPIs, time series, rankings, country profiles and crisis records).

### 5.3 Cartographic Design

The WebGIS follows established principles of thematic cartography:

- **Choropleth mapping** with three classification methods (quantile, equal interval, natural breaks approximation) and configurable class counts (3 to 7). Color palettes are adapted to the semantic direction of each indicator: green for positive indicators (GDP/capita, banking rate), red for negative indicators (NPL, inflation, debt), blue for neutral indicators (credit-to-GDP, FDI), and a diverging palette for growth rates.
- **Proportional circles** scaled by the square root of indicator values, positioned at label coordinates from Natural Earth data.
- **Heatmap layer** using kernel density estimation to reveal spatial concentrations.
- **Label layer** with country names rendered as HTML div icons with text shadow for readability.
- **Capital cities layer** with geolocated markers sourced from country profile data.

### 5.4 Interface Design

The user interface adopts a dark theme optimized for analytical work, with the following design principles:

- Glassmorphism effects for floating elements (year display, tooltips).
- A left sidebar with four contextual tabs (Layers, Indicators, Analytics, Data).
- A right detail panel for country-level deep dives.
- Responsive controls using range sliders, select menus, checkboxes and action buttons.
- Typography based on Inter (UI text) and JetBrains Mono (numeric values).

### 5.5 Technology Stack

| Component | Technology | Version |
|---|---|---|
| Base mapping | Leaflet.js | 1.9.4 |
| Drawing tools | Leaflet.draw | 1.0.4 |
| Overview map | Leaflet-minimap | 3.6.1 |
| Heatmap rendering | Leaflet.heat | 0.2.0 |
| Charts | Chart.js | 4.4.7 |
| Spatial analysis | Turf.js | 7.x |
| Icons | Font Awesome | 6.5.1 |
| Data pipeline | Python, pandas, numpy | 3.x |
| Deployment | GitHub Pages | -- |

---

## 6. Technical Architecture

```
WEBGIS_AFRICA_FINANCE/
  build_webgis.py          Python ETL pipeline (data processing)
  index.html               Self-contained WebGIS application
  server.py                Local development server (port 9999)
  data/
    africa.geojson          Geographic boundaries (55 features, ~2.3 MB)
    indicators.json         Financial indicators payload (~1.2 MB)
```

The application is fully self-contained in a single HTML file that loads all dependencies from CDN. No build step, no package manager and no server-side code is required for deployment. The data files are fetched via standard HTTP GET requests at initialization.

### Data Flow

```
Excel Workbook (6 sheets, 15,000+ rows)
        |
        v
  build_webgis.py (pandas ETL)
        |
        +---> africa.geojson (geographic layer)
        +---> indicators.json (analytical payload)
                    |
                    v
            index.html (Leaflet + Chart.js)
                    |
                    v
            Browser (interactive WebGIS)
```

---

## 7. Data Description

### 7.1 Spatial Coverage

- **54 sovereign African states** with ISO 3166-1 alpha-3 identification
- **5 subregions**: Southern Africa, Central Africa, North Africa, West Africa, East Africa
- **Coordinate reference system**: EPSG:4326 (WGS 84)
- **Geometry type**: MultiPolygon (Natural Earth 1:50m)

### 7.2 Temporal Coverage

- **Period**: 2000--2024 (25 annual observations per country)
- **Maximum observations**: 53 countries x 25 years = 1,325 country-year records

### 7.3 Thematic Indicators (16 Core Variables)

| Indicator | Unit | Direction | Description |
|---|---|---|---|
| GDP per capita | USD | Higher is better | Gross domestic product divided by population |
| GDP growth | % | Higher is better | Annual real GDP growth rate |
| GDP | Billion USD | Higher is better | Total gross domestic product |
| Inflation | % | Lower is better | Consumer price index annual change |
| Public debt / GDP | % | Lower is better | Government debt as share of GDP |
| Banking rate | % | Higher is better | Share of population with a bank account |
| NPL ratio | % | Lower is better | Non-performing loans as share of total loans |
| Capital adequacy ratio | % | Higher is better | Bank capital to risk-weighted assets |
| Return on equity | % | Higher is better | Bank profitability measure |
| Credit to GDP | % | Higher is better | Domestic credit to private sector as share of GDP |
| Mobile money adoption | % | Higher is better | Share of population with a mobile money account |
| Financial inclusion score | 0--10 | Higher is better | Composite inclusion index |
| FDI inflows | Billion USD | Higher is better | Foreign direct investment inflows |
| Unemployment | % | Lower is better | Share of labor force without employment |
| PAR30 | % | Lower is better | Portfolio at risk over 30 days (microfinance) |
| HDI | 0--1 | Higher is better | Human Development Index |

---

## 8. Functional Features

### 8.1 Thematic Mapping

- Interactive choropleth with 16 selectable indicators
- Three classification methods: quantile, equal interval, natural breaks
- Configurable number of classes (3 to 7)
- Adjustable layer opacity (0--100%)
- Semantic color palettes adapted to indicator direction
- Dynamic legend with class boundaries and units

### 8.2 Supplementary Layers

- Country borders (toggle on/off)
- Country name labels (positioned at Natural Earth label coordinates)
- Capital city markers with tooltips
- Proportional circles (square-root scaling relative to indicator values)
- Heatmap (kernel density estimation for spatial concentration analysis)

### 8.3 Basemaps

Four basemap options: Dark (CartoDB Dark Matter), OpenStreetMap, Light (CartoDB Positron), Satellite (Esri World Imagery). A minimap overview is displayed in the bottom-left corner.

### 8.4 Temporal Navigation

- Year slider (2000--2024)
- Step-by-step navigation (previous/next buttons)
- Animated playback with automatic year progression
- Floating year indicator on the map

### 8.5 Measurement and Drawing Tools

- Distance measurement along polylines (kilometers, via Turf.js)
- Area measurement of polygons (square kilometers, via Turf.js)
- Freehand drawing tools: polygon, polyline, point marker (Leaflet.draw)
- Automatic area/distance computation for drawn features

### 8.6 Analytics Panel

- Key Performance Indicators (KPI) grid: total GDP, average growth, banking rate, NPL, inflation, total FDI, inclusion score, mobile money adoption
- Continental time-series chart (growth, inflation, banking rate over 25 years)
- Top 10 countries bar chart (dynamically updates with indicator and year selection)
- Spatial query engine: filter countries by indicator value with comparison operators (>, <, >=, <=)

### 8.7 Country Detail Panel

- Country name, region and selected year
- Eight statistical indicators displayed in a compact grid
- Two time-series charts: (1) GDP and growth, (2) banking rate, mobile money and NPL
- Country profile table (currency, central bank, stock exchange, population)

### 8.8 Attribute Table

- Modal table displaying all countries and 12 indicators for the selected year
- Column sorting (ascending/descending) by clicking headers
- CSV export and GeoJSON export functionality

### 8.9 Search and Rankings

- Autocomplete country search with region display
- Click-to-zoom and automatic detail panel opening
- Rankings for 10 variables with top 10 and bottom 10 countries

### 8.10 Internationalization

- Full bilingual support: English (default) and French
- Language toggle button switching all UI labels, indicator names, chart labels and section headings
- i18n dictionary with 40+ translated UI elements

---

## 9. Results

### 9.1 Data Pipeline Output

The ETL pipeline successfully processes:
- **55 geographic features** (54 countries + Bir Tawil) in the GeoJSON layer (2,298 KB)
- **1,325 country-year records** with up to 40 variables each in the indicator payload (1,190 KB)
- **16 continental KPIs** computed for the reference year 2024
- **25 years of continental time series** with 9 aggregate variables per year
- **53 individual country time series** with 7 variables per country
- **10 ranking variables** with top 10 and bottom 10 for each
- **53 country profiles** with institutional and geographic metadata

### 9.2 Key Findings (2024 Reference Year)

The choropleth mapping reveals several spatial patterns:

**GDP per capita.** A clear North-South gradient is visible, with North African countries (Libya, Algeria, Egypt, Tunisia) and Southern African economies (Botswana, South Africa, Namibia) displaying higher GDP per capita than the Sahelian belt (Niger, Chad, Central African Republic, Burundi).

**Banking penetration.** The banking rate shows strong regional clustering: North Africa and Southern Africa exceed 50%, while West and Central Africa remain below 30% in many countries, with notable exceptions (Ghana, Senegal, Cameroon).

**Mobile money adoption.** East Africa dominates, with Kenya, Tanzania and Uganda showing penetration rates above 50%. This confirms the well-documented mobile money corridor extending from the Great Rift Valley region.

**Financial inclusion.** The composite inclusion score reveals a multi-speed continent: countries with strong fintech ecosystems (Kenya, Ghana, Rwanda) score significantly higher than resource-dependent economies with underdeveloped financial infrastructure.

**Non-performing loans.** Elevated NPL ratios cluster in countries experiencing political instability or commodity price shocks, with visible spatial concentrations in Central Africa and parts of West Africa.

### 9.3 Temporal Dynamics

The continental time-series analysis reveals:
- A general upward trend in banking penetration across the continent from 2000 to 2024.
- Mobile money adoption showing exponential growth from 2010 onward.
- GDP growth volatility correlating with global commodity cycles and the COVID-19 shock (2020).
- Gradual improvement in financial stability indicators (CAR, NPL) in countries implementing Basel-aligned regulations.

---

## 10. Discussion

### 10.1 Spatial Patterns and Regional Disparities

The WebGIS reveals that African financial development is characterized by strong spatial heterogeneity. Rather than a uniform continental trajectory, the data shows five distinct regional profiles:

- **North Africa**: mature banking systems, high banking penetration, limited mobile money adoption, moderate debt levels.
- **West Africa**: rapid fintech growth, improving banking rates, persistent NPL challenges in some economies, strong remittance corridors.
- **East Africa**: global leadership in mobile money, innovative financial inclusion models, growing fintech investment.
- **Central Africa**: lower banking penetration, higher NPL ratios, resource-dependent economies with vulnerability to commodity shocks.
- **Southern Africa**: diversified financial systems (South Africa, Mauritius), significant intra-regional disparities (Botswana vs. Lesotho).

### 10.2 Methodological Contributions

This project demonstrates the value of WebGIS technology for financial analysis, a domain that has traditionally relied on tables and static charts. The spatial representation of financial indicators adds an analytical dimension that enables:

- Visual identification of spatial clusters and outliers.
- Exploration of neighborhood effects and cross-border financial corridors.
- Rapid temporal comparison through animated mapping.
- Multi-indicator analysis through layer switching and overlay.

### 10.3 Technical Considerations

The choice of a fully client-side architecture (no backend server) ensures deployment simplicity and eliminates infrastructure costs. However, it imposes constraints on data volume: the current payload (approximately 3.5 MB total) is suitable for country-level annual data but would require optimization (vector tiles, server-side rendering) for finer spatial or temporal granularity.

The use of quantile classification as the default method ensures balanced visual representation across the color scale, which is particularly important for skewed distributions common in African financial data (where a few large economies dominate aggregate indicators).

---

## 11. Limitations and Future Work

### 11.1 Limitations

- Data for certain countries and years may be incomplete or estimated, reflecting gaps in original source reporting.
- The natural breaks classification uses a quantile-based approximation rather than the full Jenks optimization algorithm.
- Subnational analysis is not supported in the current version (data is aggregated at the national level).
- The static deployment model limits the ability to integrate real-time or frequently updated data sources.

### 11.2 Future Development Directions

- Integration of subnational financial data where available (regional banking statistics, mobile money coverage maps).
- Addition of time-series forecasting models (ARIMA, Prophet) for projecting key indicators.
- Implementation of spatial autocorrelation analysis (Moran's I, LISA) to quantify clustering statistically.
- Development of a comparative dashboard mode for side-by-side country analysis.
- Connection to live data APIs (World Bank, IMF WEO) for automatic data updates.

---

## 12. Conclusion

The Africa Finance Observatory WebGIS represents a comprehensive geospatial platform for understanding financial development across the African continent. By combining 25 years of multidimensional financial data with interactive cartographic tools, the platform enables analytical workflows that were previously accessible only through desktop GIS software or custom research environments.

The project demonstrates that modern web mapping technologies (Leaflet, Chart.js, Turf.js) are mature enough to support professional-grade spatial analysis in domain-specific contexts. The fully static architecture ensures that the platform remains accessible, low-cost to maintain and easily reproducible.

With 54 countries, 16 core indicators, 25 years of temporal depth and a rich set of analytical tools, this WebGIS provides a solid foundation for evidence-based analysis of African financial systems.

---

## 13. Installation and Deployment

### Prerequisites

- Python 3.8+ with pandas, numpy and openpyxl
- A modern web browser (Chrome, Firefox, Edge, Safari)

### Local Development

```bash
# Clone the repository
git clone https://github.com/abdousamad387/WEBGIS_AFRICA_FINANCE.git
cd WEBGIS_AFRICA_FINANCE

# (Optional) Rebuild data from source Excel
python build_webgis.py

# Start local server
python server.py
# Opens automatically at http://localhost:9999
```

### Deployment

The application is deployed via GitHub Pages at:
**https://abdousamad387.github.io/WEBGIS_AFRICA_FINANCE/**

No build step or server configuration is required. The `index.html` file and `data/` directory are served directly as static files.

---

## 14. References

- Natural Earth. "Admin 0 -- Countries." Version 5.x. https://www.naturalearthdata.com/
- World Bank. "World Development Indicators." https://databank.worldbank.org/
- International Monetary Fund. "World Economic Outlook Database." https://www.imf.org/
- African Development Bank. "African Economic Outlook." https://www.afdb.org/
- GSMA. "State of the Industry Report on Mobile Money." https://www.gsma.com/
- Leaflet. "An open-source JavaScript library for interactive maps." https://leafletjs.com/
- Turf.js. "Advanced geospatial analysis for browsers and Node.js." https://turfjs.org/
- Chart.js. "Simple yet flexible JavaScript charting." https://www.chartjs.org/

---

**Author**: Abdou Samad

**License**: MIT

**Live Demo**: https://abdousamad387.github.io/WEBGIS_AFRICA_FINANCE/
