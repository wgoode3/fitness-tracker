# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Activity(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return "<Activity object: ({}) {}>".format(self.id, self.name)

class User(models.Model):
    name = models.CharField(max_length=255) 
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Workout(models.Model):
    duration = models.IntegerField()
    units = models.CharField(max_length=255)
    start = models.DateTimeField()
    activity = models.ForeignKey(Activity, related_name="workouts")
    user = models.ForeignKey(User, related_name="workouts")