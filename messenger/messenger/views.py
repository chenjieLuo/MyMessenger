from django.http import HttpResponse
from django.shortcuts import render, redirect


def starting_page(request):
    return render(request, 'Home/Welcome.html')