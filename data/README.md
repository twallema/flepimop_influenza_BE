# Data sources

## Raw

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
