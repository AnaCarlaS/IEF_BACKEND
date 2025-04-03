import folium
import math

def normalize_polygon(geometry):
    """
    Normaliza uma geometria (Polygon ou MultiPolygon) para uma lista simples de coordenadas.
    """
    # Se for um MultiPolygon (mais de um nível interno de listas)
    if isinstance(geometry[0][0][0], list):
        # Extrai as coordenadas do primeiro Polygon dentro do MultiPolygon
        return geometry[0][0]
    # Se for um Polygon
    elif isinstance(geometry[0][0], list):
        # Retorna diretamente o Polygon
        return geometry[0]
    else:
        raise ValueError("Formato de geometria não reconhecido.")


def get_bounds_and_center(polygon_coords):
    """
    Função para calcular os limites (bounding box) e o centro do polígono.
    """
    lats = [coord[1] for coord in polygon_coords]
    lons = [coord[0] for coord in polygon_coords]
    
    lat_min, lat_max = min(lats), max(lats)
    lon_min, lon_max = min(lons), max(lons)
    
    center_lat = sum(lats) / len(lats)
    center_lon = sum(lons) / len(lons)
    
    return (lat_min, lat_max, lon_min, lon_max), (center_lat, center_lon)

def approximate_distance(lat1, lon1, lat2, lon2):
    """
    Aproximação da distância entre dois pontos, em metros, utilizando a projeção Mercator.
    """
    R = 6371000  # Raio médio da Terra em metros
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def calculate_zoom_level(bounds):
    """
    Função que ajusta o nível de zoom baseado na distância máxima entre os pontos do bounding box.
    """
    lat_min, lat_max, lon_min, lon_max = bounds
    horizontal_distance = approximate_distance(lat_min, lon_min, lat_min, lon_max)
    vertical_distance = approximate_distance(lat_min, lon_min, lat_max, lon_min)
    max_distance = max(horizontal_distance, vertical_distance)
    zoom_table = [
        (20000000, 10),   # 20,000 km
        (10000000, 10),   # 10,000 km
        (5000000, 10),    # 5,000 km
        (2500000, 12),    # 2,500 km
        (1000000, 12),    # 1,000 km
        (500000, 12),     # 500 km
        (250000, 15),     # 250 km
        (100000, 15),     # 100 km
        (50000, 16),     # 50 km
        (25000, 16),     # 25 km
        (10000, 16),     # 10 km
        (5000, 16),      # 5 km
        (2500, 16),      # 2.5 km
        (1000, 17),      # 1 km
        (500, 17),       # 500 m
        (250, 17),       # 250 m
        (100, 17),       # 100 m
        (50, 17),        # 50 m
        (25, 17),        # 25 m
    ]
    for dist, zoom in zoom_table:
        if max_distance > dist:
            return zoom
    return 21  # Se a distância for muito pequena, usar o zoom máximo

def mapa_view(polygon_coords):
    polygon_coords = normalize_polygon(polygon_coords)
    bounds, center = get_bounds_and_center(polygon_coords)
    zoom_start = calculate_zoom_level(bounds)
    m = folium.Map(location=center, zoom_start=zoom_start, font_size="0.75rem", tiles="") #,width=300, height=300)
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Hybrid',
        overlay=False,
        control=False
    ).add_to(m)
    polygon_coords_inverted = [(y, x) for x, y in polygon_coords]
    folium.Polygon(locations=polygon_coords_inverted, color="#BD3D3A", weight=2.5, opacity=0.975, fill=True).add_to(m)
    style = """
        <style>
        .leaflet-control-zoom-in, .leaflet-control-zoom-out {
            width: 15px !important;
            height: 15px !important;
            line-height: 15px !important;
            font-size: 12px !important;
        }
        </style>
    """
    m.get_root().html.add_child(folium.Element(style))
    map_html = m._repr_html_()
    return map_html, center
