# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Matches(models.Model):
    match_id = models.FloatField(primary_key=True, null=True)
    match = models.CharField(max_length=100, blank=True, null=True)
    who_win = models.CharField(max_length=20, blank=True, null=True)


    class Meta:
        db_table = 'matches'
        verbose_name_plural = "Matches"
        ordering = ['match_id']


class Players(models.Model):
    player_id = models.FloatField(primary_key=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Players"
        db_table = 'players'

    def __str__(self):
        return f"{self.name}"


class MatchDetails(models.Model):
    id = models.FloatField(primary_key=True, null=True)
    match_id = models.FloatField(blank=True, null=True)
    team = models.CharField(max_length=10, blank=True, null=True)
    runs_scored = models.FloatField(blank=True, null=True)
    fours_hit = models.FloatField(blank=True, null=True)
    sixes_hit = models.FloatField(blank=True, null=True)
    wickets = models.FloatField(blank=True, null=True)
    won = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'match_details'
        ordering = ['match_id']


class UserDetails(models.Model):
    #id = models.AutoField(primary_key=True, verbose_name="id")
    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'user_details'
