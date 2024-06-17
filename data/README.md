# Data sources

## Raw

### Belgian Census 2011

+ `Pop_LPW_NL_25FEB15.xlsx` contains the working population per sex, place of residence and place of work. Data free for download at https://census2011.fgov.be/download/downloads_nl.html.

+ `census_demo_nl_04nov14.xlsx` contains all demographic data from the 2011 Belgian census. Data free for download at https://census2011.fgov.be/download/downloads_nl.html.

### Shape files

Folder contains the shape files of the Belgian municipalities. Retrieved from [opendatasoft](https://public.opendatasoft.com/explore/dataset/georef-belgium-municipality-millesime/map/?disjunctive.mun_off_language&disjunctive.mun_name_fr&disjunctive.mun_name_nl&disjunctive.mun_name_de&disjunctive.reg_name_de&disjunctive.reg_name_nl&disjunctive.reg_name_fr&disjunctive.prov_name_de&disjunctive.prov_name_nl&disjunctive.prov_name_fr&disjunctive.arr_name_de&disjunctive.arr_name_nl&disjunctive.arr_name_fr&sort=year&location=9,50.74775,3.96469&basemap=jawg.light), updated Jan 19, 2024.

+ `georef-belgium-municipality-millesime.shp/.shx` loads the shape.
+ `georef-belgium-municipality-millesime.prj` contains the name of the projection used.
+ `georef-belgium-municipality-millesime.dbf` contains associated data.

## Interim

### Belgian Census 2011

+ `mobility_matrix.csv` contains the origin-destination mobility matrix.
+ `demography` contains the formatted demographic data.
