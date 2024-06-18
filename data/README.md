# Data sources

## Raw

### Cases

#### 2017-2018

+ `Influenza 2017-2018 End of Season_NL.pdf`: End of Influenza season report of the Belgian Scientific Institute of Public Health (Sciensano). Retrieved from [Sciensano](https://www.sciensano.be/sites/default/files/influenza_2017-2018_end_of_season_nl.pdf) (accessed Nov. 9 2022).

+ `ILI_weekly_1718.csv`: Weekly incidence of GP visits for Influenza-like illness in Belgium (per 100K inhabitats) during the 2017-2018 Influenza season. Data available for four age groups: [0,5(, [5,15(, [15,65(, [65,120(. Extracted from Fig. 2 in `Influenza 2017-2018 End of Season_NL.pdf` using [WebPlotDigitizer](https://automeris.io/WebPlotDigitizer/).

### Belgian Census 2011

+ `Pop_LPW_NL_25FEB15.xlsx` contains the working population per sex, place of residence and place of work. Contains 591 municipalities (pre-2019 fusions). For a total of Data free for download at https://census2011.fgov.be/download/downloads_nl.html.

+ `census_demo_nl_04nov14.xlsx` contains all demographic data from the 2011 Belgian census. Contains 591 municipalities (pre-2019 fusions). Data free for download at https://census2011.fgov.be/download/downloads_nl.html.

### Shape files

Contains the shape files of the 581 Belgian municipalities. Retrieved from [opendatasoft](https://public.opendatasoft.com/explore/dataset/georef-belgium-municipality-millesime/map/?disjunctive.mun_off_language&disjunctive.mun_name_fr&disjunctive.mun_name_nl&disjunctive.mun_name_de&disjunctive.reg_name_de&disjunctive.reg_name_nl&disjunctive.reg_name_fr&disjunctive.prov_name_de&disjunctive.prov_name_nl&disjunctive.prov_name_fr&disjunctive.arr_name_de&disjunctive.arr_name_nl&disjunctive.arr_name_fr&sort=year&location=9,50.74775,3.96469&basemap=jawg.light), updated Jan 19, 2024.

+ `georef-belgium-municipality-millesime.shp/.shx` loads the geography of Belgium.
+ `georef-belgium-municipality-millesime.prj` contains the name of the projection used.
+ `georef-belgium-municipality-millesime.dbf` contains the associated metadata.

## Interim

### Belgian Census 2011


+ `demography_municipalities.xlsx` contains the total number of inhabitants for the 581 municipalities of Belgium (post-2019 fusions).  Extracted from `data/raw/census/census_demo_nl_04nov14.xlsx` by Rita Verstraten. HOW?
+ `mobility_municipalities.xlsx` contains the number of commuters from municipality i to municipality j. For the 581 municipalities of Belgium (post-2019 fusions). Extracted from `data/raw/census/Pop_LPW_NL_25FEB15.xlsx` by Rita Verstraten. HOW?

### Cases

#### 2017-2018

+ `ILI_weekly_100K.csv`: Weekly incidence of GP visits for Influenza-like illness per 100K inhabitants in Belgium during the 2017-2018 season. Data available for four age groups: [0,5(, [5,15(, [15,65(, [65,120(. Dates are the reported week number's midpoint. Generated from `ILI_weekly_1718.csv` by executing the data conversion script `analysis/data_conversion/format_cases.py`.

+ `ILI_weekly_ABS.csv`: Weekly incidence of GP visits for Influenza-like illness in Belgium during the 2017-2018 season. Data available for four age groups: [0,5(, [5,15(, [15,65(, [65,120(. Dates are the reported week number's midpoint. Generated from `ILI_weekly_1718.csv` by executing the data conversion script `analysis/data_conversion/format_cases.py`.
