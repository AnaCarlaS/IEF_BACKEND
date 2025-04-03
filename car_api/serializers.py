import json
from django.core.serializers import serialize


def serialize_geojson(model, cod_imovel, geometry_field='geometry'):
    data = serialize(
        'geojson',
        model.objects.filter(cod_imovel=cod_imovel),
        geometry_field=geometry_field
    )
    return json.loads(data)['features'] if data else None

