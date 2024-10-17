from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Category

def index(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories})

def add(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, 'add.html')
    
    name = request.POST.get('name')
    if name.strip() == '':
        return HttpResponse('Name is required')
    
    Category.objects.create(name=name)
    return redirect('index')

def edit(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        try:
            id = request.GET['id']
            category = Category.objects.get(id=id)
            return render(request, 'edit.html', {'category': category})
        except Category.DoesNotExist:
            return redirect('index')
    
    id = request.POST.get('id')
    name = request.POST.get('name')
    if name.strip() == '':
        return HttpResponse('Name is required')
    
    try:
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        
        return redirect('index')
    except Category.DoesNotExist:
        return HttpResponse("Category not found")

def delete(request: HttpRequest) -> HttpResponse:
    try:
        id = request.GET['id']
        category = Category.objects.get(id=id)
        
        category.delete()
        return redirect('index')
    except Category.DoesNotExist:
        return HttpResponse("Category not found")
