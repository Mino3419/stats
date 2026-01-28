from django.db import models


class Stats(models.Model):
    id = models.BigAutoField(primary_key=True)
    sezona = models.CharField(blank=True, null=True)
    klub = models.TextField(blank=True, null=True)
    id_player = models.BigIntegerField(blank=True, null=True)
    hlava = models.TextField(blank=True, null=True)
    meno = models.TextField(blank=True, null=True)
    pozicia = models.TextField(blank=True, null=True)
    zapasy = models.BigIntegerField(blank=True, null=True)
    g = models.BigIntegerField(db_column='g', blank=True, null=True)  # Field name made lowercase.
    a = models.BigIntegerField(db_column='a', blank=True, null=True)  # Field name made lowercase.
    b = models.BigIntegerField(db_column='b', blank=True, null=True)  # Field name made lowercase.
    plusminus = models.BigIntegerField(db_column='plusminus', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    v = models.BigIntegerField(db_column='v', blank=True, null=True)  # Field name made lowercase.
    gvp = models.BigIntegerField(db_column='gvp', blank=True, null=True)  # Field name made lowercase.
    gvo = models.BigIntegerField(db_column='gvo', blank=True, null=True)  # Field name made lowercase.
    v_g = models.BigIntegerField(db_column='v_g', blank=True, null=True)  # Field name made lowercase.
    gvot = models.BigIntegerField(db_column='gvot', blank=True, null=True)  # Field name made lowercase.
    strely = models.BigIntegerField(blank=True, null=True)
    perc_strel = models.FloatField(blank=True, null=True)
    buly = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stats'
class ROK(models.Model):
    id=models.IntegerField(primary_key=True)
    sezona = models.CharField(blank=True, null=True)
    klub=models.CharField(blank=True,null=True)
    id_player = models.BigIntegerField(blank=True, null=True)
    hlava=models.TextField(blank=True, null=True)
    prve_meno=models.CharField(blank=True, null=True)
    druhe_meno=models.CharField(blank=True, null=True)
    cislo_dresu=models.CharField(blank=True, null=True)
    drzanie=models.CharField(blank=True, null=True)
    vyska=models.CharField(blank=True, null=True)
    vaha=models.CharField(blank=True, null=True)
    datum_nar=models.CharField(blank=True, null=True)
    mesto_nar=models.CharField(blank=True, null=True)
    krajina_nar=models.CharField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rok'
    
class CLUB(models.Model):
    id=models.SmallIntegerField(primary_key=True)
    kod=models.CharField(blank=True, null=True)
    cely_nazov_klubu=models.CharField(blank=True,null=True)
    class Meta:
        managed=False
        db_table="club"
class Logo(models.Model):
    index=models.BigIntegerField(primary_key=True)
    Abbreviation=models.CharField(null=True,blank=True)
    FullName=models.CharField(null=True,blank=True)
    LogoURL=models.CharField(null=True,blank=True)
    class Meta:
        managed=False
        db_table="logo"


