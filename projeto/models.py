from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.gis.db import models

class Projeto(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")
    supressao_apos_2008 = models.CharField(max_length=255)
    tipo_area = models.CharField(max_length=255)
    tamanho_imovel = models.CharField(max_length=255)
    potencial_regeneracao_natural = models.CharField(max_length=255)
    dinamica_hidrica = models.CharField(max_length=255)
    pedregosidade_solo = models.CharField(max_length=255)
    estrutura_ecossistema = models.CharField(max_length=255)
    condicoes_solo = models.CharField(max_length=255)
    ocupacao_area = models.CharField(max_length=255)
    declividade = models.CharField(max_length=255)
    fatores_perturbacao = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    geometry = models.PolygonField(srid=4674)

    def __str__(self):
        return f"Projeto: {self.tipo_de_area}, Tamanho: {self.tamanho_do_imovel}"


class Bioma(models.Model):
    fid = models.IntegerField(verbose_name=_("FID"))
    bioma = models.CharField(max_length=255, verbose_name=_("Bioma"))
    bioma_name = models.CharField(max_length=255, verbose_name=_("Nome do Bioma"))
    bioma_code = models.IntegerField(verbose_name=_("Código do Bioma"))
    geometry = models.MultiPolygonField(srid=4674, verbose_name=_("Geometria"))
    
    class Meta:
        indexes = [
            models.Index(fields=['geometry'], name='bioma_geometry_idx', opclasses=['gist'])
        ]


class Subdominio(models.Model):
    fid = models.IntegerField(verbose_name=_("FID"))
    bioma = models.CharField(max_length=255, verbose_name=_("Bioma"))
    subdominio = models.CharField(max_length=255, verbose_name=_("Subdomínio"))
    subdominio_code = models.IntegerField(verbose_name=_("Subdomínio Code"))
    bioma_name = models.CharField(max_length=255, verbose_name=_("Nome do Bioma"))
    bioma_code = models.IntegerField(verbose_name=_("Código do Bioma"))
    geometry = models.MultiPolygonField(srid=4674, verbose_name=_("Geometria"))

    def __str__(self):
        return f'{self.bioma} - {self.subdominio}'
    
    class Meta:
        indexes = [
            models.Index(fields=['geometry'], name='subdominio_geometry_idx', opclasses=['gist'])
        ]

class Especie(models.Model):
    bioma = models.CharField(max_length=255, verbose_name='Bioma')
    bioma_name = models.CharField(max_length=255, verbose_name='Nome do Bioma')
    nome_cientifico = models.CharField(max_length=255, verbose_name='Nome Científico')
    codigo = models.IntegerField(verbose_name='Código')
    habito = models.CharField(max_length=255, verbose_name='Hábito')
    distribuicao = models.TextField(verbose_name='Distribuição')
    subdominio_list = ArrayField(
        models.CharField(max_length=255),
        verbose_name='Lista de Subdomínios'
    )
    fisionomias = models.TextField(verbose_name='Fisionomias')
    conservacao = models.CharField(max_length=255, verbose_name='Conservação')
    nomes_populares = models.TextField(verbose_name='Nomes Populares')
    categorias_ecofisiologicas = models.CharField(max_length=255, verbose_name='Categorias Ecofisiológicas')

    def __str__(self):
        return self.nome_cientifico
    
    class Meta:
        indexes = [
            GinIndex(fields=['subdominio_list']),
        ]