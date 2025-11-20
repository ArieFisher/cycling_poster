
# Reference
curl -X POST "https://maps.geoapify.com/v1/staticmap?apiKey=116d127dad7b43a18a7363e2260348f5" \
-H "Content-Type: application/json" \
-d @cycle_2025.geojson \
--output cycle_map_image.png

# Config
apiKey=116d127dad7b43a18a7363e2260348f5
geojson=https://storage.googleapis.com/cycle2025/cycle_2025.geojson


# Appendix
--------

 <!-- "styleCustomization": [
    {
        "layer": "water",
        "color": "#69c7fa"
    },
    {
        "layer": "landcover_wood",
        "color": "#34c112"
    },
    {
        "layer": "landuse_park",
        "color": "#048a06"
    },
    {
        "layer": "waterway",
        "color": "#61a3f4",
        "size": 3
    },
    {
        "layer": "building",
        "color": "#313030"
    },
    {
        "layer": "aeroway-taxiway",
        "color": "#8315c6"
    },
    {
        "layer": "highway_minor",
        "color": "#2a2929"
    },
    {
        "layer": "highway_name_other",
        "color": "#ffa00f"
    },
    {
        "layer": "highway_name_motorway",
        "color": "#ffa00f"
    }
  ], -->