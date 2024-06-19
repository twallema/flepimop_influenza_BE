# Data sources

## Raw

### Social contacts

+ `belgium_2010_all.xlsx` : Social contact data for Belgium, sheets were used to denote contact duration. Extracted using [SOCRATES](http://www.socialcontactdata.org/socrates/). Country: Belgium 2010 (Van Hoang 2020). Type of day: All (averages weekend/weekday).  Type of contacts: Physical and non-physical, excluding supplemental professional contacts. An integration of the contacts with the contact duration is performed in the sheet named 'integrated'.

### Literature

+ `antoine_etal_archpublichealth_2010.pdf` : Title: 'Influenza vaccination recording system in Belgium'. Of interest: Table 1. Reported vaccination coverage by age group and Belgian region, on 31 March 2010.
+ `goeyvaerts_etal_epidemics_2015.pdf` : Title: 'Estimating dynamic transmission model parameters for seasonal influenza by fitting to age and season-specific influenza-like illness incidence'. Of interest: Section 2.2.4 Vaccination coverage and vaccine efficacy. Reference Beutels et al. 2013 also points to large differences in vaccination incidence between Flanders and Wallonia.

### Demography

+ `TF_SOC_POP_STRUCT_2017.xlsx` : contains the number of inhabitants of age x in all 589 Belgian municipalities (pre-2019 fusions). Downloaded from [Statbel](https://statbel.fgov.be/nl/open-data/bevolking-naar-woonplaats-nationaliteit-burgerlijke-staat-leeftijd-en-geslacht).

### Cases

#### 2017-2018

+ `Influenza 2017-2018 End of Season_NL.pdf` : End of Influenza season report of the Belgian Scientific Institute of Public Health (Sciensano). Retrieved from [Sciensano](https://www.sciensano.be/sites/default/files/influenza_2017-2018_end_of_season_nl.pdf) (accessed Nov. 9 2022).

+ `ILI_weekly_1718.csv` : Weekly incidence of GP visits for Influenza-like illness in Belgium (per 100K inhabitats) during the 2017-2018 Influenza season. Data available for four age groups: [0,5(, [5,15(, [15,65(, [65,120(. Extracted from Fig. 2 in `Influenza 2017-2018 End of Season_NL.pdf` using [WebPlotDigitizer](https://automeris.io/WebPlotDigitizer/).

### Belgian Census 2011

+ `Pop_LPW_NL_25FEB15.xlsx` : contains the working population per sex, place of residence and place of work. Contains 591 municipalities (pre-2019 fusions). For a total of Data free for download at https://census2011.fgov.be/download/downloads_nl.html.

+ `census_demo_nl_04nov14.xlsx` : contains all demographic data from the 2011 Belgian census. Contains 591 municipalities (pre-2019 fusions). Data free for download at https://census2011.fgov.be/download/downloads_nl.html.

### Shape files

Folder contains the shape files of the 581 Belgian municipalities. Retrieved from [opendatasoft](https://public.opendatasoft.com/explore/dataset/georef-belgium-municipality-millesime/map/?disjunctive.mun_off_language&disjunctive.mun_name_fr&disjunctive.mun_name_nl&disjunctive.mun_name_de&disjunctive.reg_name_de&disjunctive.reg_name_nl&disjunctive.reg_name_fr&disjunctive.prov_name_de&disjunctive.prov_name_nl&disjunctive.prov_name_fr&disjunctive.arr_name_de&disjunctive.arr_name_nl&disjunctive.arr_name_fr&sort=year&location=9,50.74775,3.96469&basemap=jawg.light), updated Jan 19, 2024.

+ `georef-belgium-municipality-millesime.shp/.shx` loads the geography of Belgium.
+ `georef-belgium-municipality-millesime.prj` contains the name of the projection used.
+ `georef-belgium-municipality-millesime.dbf` contains the associated metadata.

## Interim

### Vaccination

+ `vaccination_municipalities_2010.csv` : contains the vaccination coverage in all 581 (post-2019 fusion) Belgian municipality and per age group (0-5, 5-15, 15-65, 65+). All municipalities located in the same region have the same vaccination coverage. However, vaccination coverage differs significantly per Belgian region: Flanders (10.2%), Wallonia (1.5%) and Brussels (1.9%). Made using the data in Table 1 of `data/raw/literature/antoine_etal_archpublichealth_2010.pdf` using the script `analysis/data_conversion/make_vaccination_coverage.py`.

### Demography

+ `demography_municipalities_2017.csv` : contains the number of inhabitants in age groups 0-5, 5-15, 15-65, 65+ in all 581 Belgian municipalities (post-2019 fusions). Generated from `data/raw/demography/TF_SOC_POP_STRUCT_2017.xlsx` with `analysis/data_conversion/format_demography.py`.

### Belgian Census 2011

+ `demography_municipalities_2011.xlsx` : contains the total number of inhabitants for the 581 municipalities of Belgium (edited by Rita Verstraeten to include the 2019 fusions). Based on the 2011 census data located in `data/raw/census/census_demo_nl_04nov14.xlsx`. Made by Rita Verstraten. Total number of inhabitants per municipality can be used to normalise the commuter's origin-destination matrix. # TODO: Rita should include her conversion scripts in this repository.
+ `mobility_municipalities_2011.xlsx` : contains the number of inhabitants of municipality i that commute to municipality j. For the 581 municipalities of Belgium (edited by Rita Verstraeten to include the 2019 fusions). Based on the 2011 census data located in `data/raw/census/Pop_LPW_NL_25FEB15.xlsx`. Made by Rita Verstraten. # TODO: Rita should include her conversion scripts in this repository.

+ `mobility_municipalities_2011_sorted.csv` : Names of municipalities have been ommitted in favor of NIS codes. Matrix sorted by means of the following python code: `df.sort_index().sort_index(axis=1)`.
+ `demography_municipalities_2011_sorted.csv` : Names of municipalities have been ommitted in favor of NIS codes, sorted.

### Cases

#### 2017-2018

+ `ILI_weekly_100K.csv` : Weekly incidence of GP visits for Influenza-like illness per 100K inhabitants in Belgium during the 2017-2018 season. Data available for four age groups: [0,5(, [5,15(, [15,65(, [65,120(. Dates are the reported week number's midpoint. Generated from `ILI_weekly_1718.csv` by executing the data conversion script `analysis/data_conversion/format_cases.py`.

+ `ILI_weekly_ABS.csv` : Weekly incidence of GP visits for Influenza-like illness in Belgium during the 2017-2018 season. Data available for four age groups: [0,5(, [5,15(, [15,65(, [65,120(. Dates are the reported week number's midpoint. Generated from `ILI_weekly_1718.csv` by executing the data conversion script `analysis/data_conversion/format_cases.py`.

## Conversion

Contains the scripts used to convert 'raw' to 'interim' data.