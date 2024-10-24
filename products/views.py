import os
import random
import time
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.core.files.storage import FileSystemStorage

from ecommerce.settings import MEDIA_ROOT
from products.models import Product, ProductImage
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
    except Category.DoesNotExist:
        return HttpResponse("Category not found")

    try:
        (image1Name, image2Name) = uploadFiles(request)
        newProduct = Product.objects.create(
            name=name, 
            price=price, 
            availableQuantity=stock, 
            category=existingCategory
        )
        
        ProductImage.objects.create(fileName=image1Name, product=newProduct)
        ProductImage.objects.create(fileName=image2Name, product=newProduct)

        return redirect('index')
    except Exception as ex:
        return HttpResponse(f"Error: {ex}")


def edit(request):
    if request.method == "GET":
        try:
            id = request.GET['id']
            product = Product.objects.get(id=id)
            categories = Category.objects.all()
            productImages = ProductImage.objects.filter(product=product)            
            
            return render(request, 'products/edit.html', {
                'product': product,
                'productImages': productImages, 
                'categories': categories,
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

def uploadFiles(request: HttpRequest) -> tuple:
    image1 = request.FILES['image1']
    image2 = request.FILES['image2']
    
    image1Extension = os.path.splitext(image1.name)[1]
    image2Extension = os.path.splitext(image2.name)[1]
    
    timestamp = time.time()
    randomValue = random.randint(0, 999999)
    
    image1Name = f"{timestamp}-{randomValue}-1{image1Extension}"
    image2Name = f"{timestamp}-{randomValue}-2{image2Extension}"
    
    storage = FileSystemStorage(MEDIA_ROOT / "product-images")
    storage.save(image1Name, image1)
    storage.save(image2Name, image2)
    
    return (image1Name, image2Name)
