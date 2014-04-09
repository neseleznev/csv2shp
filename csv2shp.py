#!/usr/bin/python
import csv
from shapely.geometry import Point, mapping
import fiona
import sys
from optparse import OptionParser

def UnicodeDictReader(utf8_data, **kwargs):
  csv_reader = csv.DictReader(utf8_data, **kwargs)
  for row in csv_reader:
    yield dict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()])

usage = 'usage: %prog [options] inputFile [optional output filename]'
parser = OptionParser(usage=usage)
parser.add_option('--lat', dest='lat_col',
                  help='latitude column name')
parser.add_option('--lng', dest='lng_col',
                  help='longitude column name')
parser.add_option('-j', '--geojson', dest='use_geojson', action='store_true',
                  help='default to geojson output')
(options, args) = parser.parse_args()

if not args:
  print 'missing inputFile'
  print parser.usage()
  sys.exit(1)

input_filename = args[0]
output_filename = args[0] + '.shp'
if options.use_geojson:
  output_filename = args[0] + '.json'
output_format = 'ESRI Shapefile'
if len(args) == 2:
  output_filename = args[1]
if 'json' in output_filename:
  output_format = 'GeoJSON'

# guess if it's a tsv
tmp_input = open(input_filename)
first_line = next(tmp_input)
tmp_input.close()
delimiter = ' '
if 'tsv' in input_filename or '\t' in first_line:
  delimiter = '\t'
    
reader = UnicodeDictReader(open(input_filename), delimiter=delimiter)
field_names = csv.DictReader(open(input_filename), delimiter=delimiter).fieldnames 

if not options.lat_col and not options.lng_col:
  possible_lng_cols = ['lng', 'longitude', 'long', 'x']
  possible_lat_cols = ['lat', 'latitude', 'y']

  for f in field_names:
    if f in possible_lng_cols:
      if not options.lng_col:
        options.lng_col = f
      else:
        print 'ambiguous lng cols: %s and %s' % (options.lng_col, f)
    if f in possible_lat_cols:
      if not options.lat_col:
        options.lat_col = f
      else:
        print 'ambiguous lat cols: %s and %s' % (options.lat_col, f)

  if not options.lng_col:
    print 'Could not find lng col in %s, looked for %s' % (field_names, possible_lng_cols)
    sys.exit(1)

  if not options.lat_col:
    print 'Could not find lat col in %s, looked for %s' % (field_names, possible_lat_cols)
    sys.exit(1)
else:
  if options.lat_col not in field_names:
    print 'got %s as lat col, not in field_names: %s' % (options.lat_col, field_names)
  if options.lng_col not in field_names:
    print 'got %s as lng col, not in field_names: %s' % (options.lng_col, field_names)

props = dict([[k, 'str'] for k in field_names])
schema = { 'geometry': 'Point', 'properties': props }
output = fiona.open(output_filename, 'w', output_format, schema)
for index, row in enumerate(reader):
  if index % 10000 == 0:
    print 'wrote %d rows' % index
  point = Point(float(row[options.lng_col]), float(row[options.lat_col]))
  output.write({
    'properties': row,
    'geometry': mapping(point)
  })
output.close()
