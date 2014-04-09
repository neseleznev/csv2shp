csv2shp
=======

```
Usage: csv2shp.py [options] inputFile [optional output filename]

Options:
  -h, --help     show this help message and exit
  --lat=LAT_COL  latitude column name
  --lng=LNG_COL  longitude column name
  -j, --geojson  default to geojson output
```

Converts an input tsv/csv to a shapefile/geojson. Requires an input file with the first row being headers.

tries very hard to make your life easy

- guesses if it's a tsv based on filename and first line (looks for tabs)
- guesses at lat/lng columns based on list of likely column names
- guesses if you want geojson if the output filename neds in .json

