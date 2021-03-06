# Imports for syntax highlighting
from qgis.utils import iface
from qgis._core import QgsFeature, QgsGeometry, QgsMapLayerRegistry, QgsVectorLayer, QgsDistanceArea

# Paste code below to QGIS console with points layer opened
layer = iface.activeLayer()
feats = [feat for feat in layer.getFeatures()]
epsg = layer.crs().postgisSrid()
uri = "Polygon?crs=epsg:" + str(epsg) + "&field=id:string&field=x:real&field=y:real&field=point_id:integer""&index=yes"
mem_layer = QgsVectorLayer(uri, 'square_buffer', 'memory')
prov = mem_layer.dataProvider()

# Distance
# import itertools
# shortest_distance = 1000
# distance = QgsDistanceArea()
#
# for a, b in itertools.product(feats, feats):
#     if a == b:
#         continue
#     point_a = a.geometry().asPoint()
#     point_b = b.geometry().asPoint()
#     # Measure the distance between lat and long
#     lat = abs(point_a[0] - point_b[0])
#     lon = abs(point_a[1] - point_b[1])
#     if max(lat, lon) < shortest_distance:
#         shortest_distance = max(lat, lon)
# square_size = shortest_distance / 2
square_size = 0.0005

for i, feat in enumerate(feats):
    point = feat.geometry().asPoint()
    new_feat = QgsFeature()
    new_feat.setAttributes(['TAZ,' + str(i), point[0], point[1], feat.id()])
    tmp_feat = feat.geometry().buffer(square_size, -1).boundingBox().asWktPolygon()
    new_feat.setGeometry(QgsGeometry.fromWkt(tmp_feat))
    prov.addFeatures([new_feat])

QgsMapLayerRegistry.instance().addMapLayer(mem_layer)
