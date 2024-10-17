from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product
from categories.models import Category

# Create your views here.
def index(request):
    products = Product.objects.all()
    return render(request, 'products/index.html', {'products': products})

def add(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, 'products/add.html', {'categories': categories})
    
    name = request.POST.get('name')
    if name.strip() == '':
        return HttpResponse('Name is required')
    
    price = request.POST.get('price')
    if price.strip() == '':
        return HttpResponse('Price is required')
    
    stock = request.POST.get('stock')
    if stock.strip() == '':
        return HttpResponse('Stock is required')
    
    category = request.POST.get('category')
    if category.strip() == '':
        return HttpResponse('Category is required')
    
    try:
        existingCategory = Category.objects.get(id=category)
        Product.objects.create(
            name=name, 
            price=price, 
            availableQuantity=stock, 
            category=existingCategory
        )

        return redirect('index')

    except Category.DoesNotExist:
        return HttpResponse("Category not found")

def edit(request):
    if request.method == "GET":
        try:
            id = request.GET['id']
            product = Product.objects.get(id=id)
            categories = Category.objects.all()
            
            return render(request, 'products/edit.html', {
                'product': product, 
                'categories': categories
            })
        
        except Product.DoesNotExist:
            return redirect('index')
    
    id = request.POST.get('id')
    name = request.POST.get('name')
    if name.strip() == '':
        return HttpResponse('Name is required')
    
    price = request.POST.get('price')
    if price.strip() == '':
        return HttpResponse('Price is required')
    
    stock = request.POST.get('stock')
    if stock.strip() == '':
        return HttpResponse('Stock is required')
    
    category = request.POST.get('category')
    if category.strip() == '':
        return HttpResponse('Category is required')
    
    try:
        existingCategory = Category.objects.get(id=category)
        product = Product.objects.get(id=id)
        product.name = name
        product.price = price
        product.availableQuantity = stock
        product.category = existingCategory
        
        product.save()
        return redirect('index')
    except Category.DoesNotExist:
        return HttpResponse("Category not found")
    except Product.DoesNotExist:
        return HttpResponse("Product not found")

def delete(request):
    try:
        id = request.GET['id']
        product = Product.objects.get(id=id)
        
        product.delete()
        return redirect('index')
    except Product.DoesNotExist:
        return HttpResponse("Product not found")
