from django.contrib.gis.db import models

class Task(models.Model):
    task_id = models.CharField(max_length=100, unique=True)
    is_running = models.BooleanField(default=False)
    last_status = models.CharField(max_length=100, null=True, blank=True)
    last_started = models.DateTimeField(null=True, blank=True)
    last_finished = models.DateTimeField(null=True, blank=True)
    cancel_requested = models.BooleanField(default=False)
    next_schedule = models.DateTimeField(null=True, blank=True)
    time_next_schedule = models.CharField(max_length=100, null=True, blank=True)
    retry_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class AreaImovel1(models.Model):
    gid = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    cod_imovel = models.CharField(max_length=255)
    cod_tema = models.TextField()
    nom_tema = models.TextField()
    mod_fiscal = models.FloatField()
    num_area = models.FloatField()
    ind_status = models.TextField()
    ind_tipo = models.TextField()
    des_condic = models.TextField()
    municipio = models.TextField()
    cod_estado = models.TextField()
    geometry = models.GeometryField(srid=4674)



class Apps1(models.Model):
    gid = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    cod_imovel = models.CharField(max_length=255)
    cod_tema = models.TextField(null=True)
    nom_tema = models.TextField(null=True)
    num_area = models.FloatField(null=True)
    ind_status = models.TextField(null=True)
    des_condic = models.TextField(null=True)
    geometry = models.GeometryField(srid=4674)



class Apps2(models.Model):
    gid = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    cod_imovel = models.CharField(max_length=255)
    cod_tema = models.TextField(null=True)
    nom_tema = models.TextField(null=True)
    num_area = models.FloatField(null=True)
    ind_status = models.TextField(null=True)
    des_condic = models.TextField(null=True)
    geometry = models.GeometryField(srid=4674)



class Apps3(models.Model):
    gid = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    cod_imovel = models.CharField(max_length=255)
    cod_tema = models.TextField(null=True)
    nom_tema = models.TextField(null=True)
    num_area = models.FloatField(null=True)
    ind_status = models.TextField(null=True)
    des_condic = models.TextField(null=True)
    geometry = models.GeometryField(srid=4674)



class Apps4(models.Model):
    gid = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    cod_imovel = models.CharField(max_length=255)
    cod_tema = models.TextField(null=True)
    nom_tema = models.TextField(null=True)
    num_area = models.FloatField(null=True)
    ind_status = models.TextField(null=True)
    des_condic = models.TextField(null=True)
    geometry = models.GeometryField(srid=4674)



class Apps5(models.Model):
    gid = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    cod_imovel = models.CharField(max_length=255)
    cod_tema = models.TextField(null=True)
    nom_tema = models.TextField(null=True)
    num_area = models.FloatField(null=True)
    ind_status = models.TextField(null=True)
    des_condic = models.TextField(null=True)
    geometry = models.GeometryField(srid=4674)


class Apps6(models.Model):
    gid = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    cod_imovel = models.CharField(max_length=255)
    cod_tema = models.TextField(null=True)
    nom_tema = models.TextField(null=True)
    num_area = models.FloatField(null=True)
    ind_status = models.TextField(null=True)
    des_condic = models.TextField(null=True)
    geometry = models.GeometryField(srid=4674)



class Apps7(models.Model):
    gid = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    cod_imovel = models.CharField(max_length=255)
    cod_tema = models.TextField(null=True)
    nom_tema = models.TextField(null=True)
    num_area = models.FloatField(null=True)
    ind_status = models.TextField(null=True)
    des_condic = models.TextField(null=True)
    geometry = models.GeometryField(srid=4674)



class AreaConsolidada1(models.Model):
    gid = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    cod_imovel = models.CharField(max_length=255) 
    cod_tema = models.TextField(null=True)
    nom_tema = models.TextField(null=True)
    num_area = models.FloatField(null=True)
    ind_status = models.TextField(null=True)
    des_condic = models.TextField(null=True)
    geometry = models.GeometryField(srid=4674)



class AreaConsolidada2(models.Model):
    gid = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    cod_imovel = models.CharField(max_length=255) 
    cod_tema = models.TextField(null=True)
    nom_tema = models.TextField(null=True)
    num_area = models.FloatField(null=True)
    ind_status = models.TextField(null=True)
    des_condic = models.TextField(null=True)
    geometry = models.GeometryField(srid=4674)



class AreaPousio1(models.Model):
    gid = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    cod_imovel = models.CharField(max_length=255)
    cod_tema = models.TextField(null=True)
    nom_tema = models.TextField(null=True)
    num_area = models.FloatField(null=True)
    ind_status = models.TextField(null=True)
    des_condic = models.TextField(null=True)
    geometry = models.GeometryField(srid=4674)



class Hidrografia1(models.Model):
    gid = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    cod_imovel = models.CharField(max_length=255)
    cod_tema = models.TextField(null=True)
    nom_tema = models.TextField(null=True)
    ind_status = models.TextField(null=True)
    des_condic = models.TextField(null=True)
    geometry = models.GeometryField(srid=4674)



class ReservaLegal1(models.Model):
    gid = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    cod_imovel = models.CharField(max_length=255)
    cod_tema = models.TextField(null=True)
    nom_tema = models.TextField(null=True)
    num_area = models.FloatField(null=True)
    ind_status = models.TextField(null=True)
    des_condic = models.TextField(null=True)
    geometry = models.GeometryField(srid=4674)



class ServidaoAdministrativa1(models.Model):
    gid = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    cod_imovel = models.CharField(max_length=255)
    cod_tema = models.TextField(null=True)
    nom_tema = models.TextField(null=True)
    num_area = models.FloatField(null=True)
    ind_status = models.TextField(null=True)
    des_condic = models.TextField(null=True)
    geometry = models.GeometryField(srid=4674)



class UsoRestrito1(models.Model):
    gid = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    cod_imovel = models.CharField(max_length=255)
    cod_tema = models.TextField(null=True)
    nom_tema = models.TextField(null=True)
    num_area = models.FloatField(null=True)
    ind_status = models.TextField(null=True)
    des_condic = models.TextField(null=True)
    geometry = models.GeometryField(srid=4674)



class VegetacaoNativa1(models.Model):
    gid = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    cod_imovel = models.CharField(max_length=255)
    cod_tema = models.TextField(null=True)
    nom_tema = models.TextField(null=True)
    num_area = models.FloatField(null=True)
    ind_status = models.TextField(null=True)
    des_condic = models.TextField(null=True)
    geometry = models.GeometryField(srid=4674)



class VegetacaoNativa2(models.Model):
    gid = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    cod_imovel = models.CharField(max_length=255)
    cod_tema = models.TextField(null=True)
    nom_tema = models.TextField(null=True)
    num_area = models.FloatField(null=True)
    ind_status = models.TextField(null=True)
    des_condic = models.TextField(null=True)
    geometry = models.GeometryField(srid=4674)


