# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User, Activity, Workout
from django.contrib import messages

def index(request):
    return render(request, "fitness_app/index.html")

def register(request):
    check = User.objects.register(
        request.POST["name"],
        request.POST["username"],
        request.POST["email"],
        request.POST["dob"],
        request.POST["height"],
        request.POST["weight"],
        request.POST["password"],
        request.POST["confirm"]
    )

    if not check["valid"]:
        for error in check["errors"]:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/")
    else:
        request.session["user_id"] = check["user"].id
        messages.add_message(request, messages.SUCCESS, "Welcome to Dojo Fitness, {}".format(request.POST["username"]))
        return redirect("/dashboard")

def login(request):
    check = User.objects.login(
        request.POST["email"],
        request.POST["password"]
    )

    if not check["valid"]:
        for error in check["errors"]:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/")
    else:
        request.session["user_id"] = check["user"].id
        messages.add_message(request, messages.SUCCESS, "Welcome back, {}".format(check["user"].username))
        return redirect("/dashboard")

def dashboard(request):
    # BMI: height in meters divided by weight in kilograms squared

    workouts = Workout.objects.all()

    data = {
        "workouts": workouts
    }

    return render(request, "fitness_app/dashboard.html", data)

def logout(request):
    request.session.clear()
    messages.add_message(request, messages.SUCCESS, "See you later")
    return redirect("/")
