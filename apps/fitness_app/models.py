# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')

class ActivityManager(models.Manager):
    def addActivity(self, name):
        errors = []
        if len(name) < 3:
            errors.append("Fitness Activity must be 3 letters or longer")
        
        if len(errors) > 0:
            return {"valid": False, "errors": errors}
        else:
            Activity.objects.create(name=name)
            return {"valid": True, "errors": errors}

class Activity(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ActivityManager()

    def __repr__(self):
        return "<Activity object: ({}) {}>".format(self.id, self.name)

class UserManager(models.Manager):
    def register(self, name, username, email, password, confirm):
        errors = []
        if len(name) < 2:
            errors.append("Name must be 2 characters or more")

        if len(username) < 2:
            errors.append("Username must be 2 characters or more")

        if len(email) < 1:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(email):
            errors.append("Invalid email")
        else:
            User.objects.filter(email=email)
            if len(email) > 0:
                errors.append("Email already in use")

        if len(password) < 1:
            errors.append("Password is required")
        elif len(password) < 8:
            errors.append("Password must be 8 characters or more")

        if len(confirm) < 1:
            errors.append("Confirm Password is required")
        elif password != confirm:
            errors.append("Confirm Password must match Password")

        response = {
            "errors": errors,
            "valid": True,
            "user": None 
        }

        if len(errors) > 0:
            response["valid"] = False
            response["errors"] = errors
        else:
            response["user"] = User.objects.create(
                name=name,
                username=username,
                email=email.lower(),
                password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            )

        return response

class User(models.Model):
    name = models.CharField(max_length=255) 
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class WorkoutManager(models.Manager):
    def addWorkout(self, duration, units, start, activity, user):
        errors = []
        if duration < 1:
            errors.append("You have to have done something")

        if len(units) < 1:
            errors.append("Units are required")

        if len(start) < 1:
            errors.append("Start Date and Time are required")
        else:
            st = datetime.strptime(start, "%Y-%m-%d")
            print st
            if st > datetime.now():
                errors.append("Start must be in the past")

        if len(errors) > 0:
            return {"valid": False, "errors": errors}
        else:
            Workout.objects.create(
                duration=duration,
                units=units,
                start=start,
                activity_id=activity,
                user_id=user
            )
            return {"valid": True, "errors": errors}


class Workout(models.Model):
    duration = models.IntegerField()
    units = models.CharField(max_length=255)
    start = models.DateTimeField()
    activity = models.ForeignKey(Activity, related_name="workouts")
    user = models.ForeignKey(User, related_name="workouts")

    objects = WorkoutManager()