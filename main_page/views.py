from django.shortcuts import render, redirect
import telebot
from . import models

bot = telebot.TeleBot('5601170431:AAFbghZsRsFXMoTI-YHMoPBNZduG6oxg6UQ')

# Create your views here.
def home_page(request):
    all_categories = models.Category.objects.all()
    return render(request, 'index.html', {'all_categories':all_categories})


# получение всех продуктов
def get_all_products(request):
    all_products = models.Product.objects.all() #получить все товары

    return render(request, 'get_all_products.html', {'all_products': all_products}) #Передать на фронтэнд


# Получение конкретного товара
def get_exact_product(request, pk):
    current_product = models.Product.objects.get(product_name=pk)

    return render(request, 'get_exact_product_index.html', {'current_product': current_product})

# получение конкретной категории
def get_exact_category(request, pk):
    current_category = models.Category.objects.get(id=pk)  #Получаем данную категорию
    category_products = models.Product.objects.filter(product_category=current_category) # Выводим все товары из конкретной категории


    return render(request, 'get_exact_product_index.html', {'exact_category': category_products}) # Передать на фронтэнд

# Поиск определенного продукта
def search_exact_product(request):
    if request.method == 'POST':
        get_product = request.POST.get('search_product')
        try:
            models.Product.objects.get(product_name=get_product)

            return redirect(f'/product/{get_product}')

        except:
            return redirect('/')

# Добавление в корзину пользщователя
def add_product_to_user_cart(request, pk):
    if request.method == 'POST':
        checker = models.Product.objects.get(id = pk)
        if checker.product_count >= int(request.POST.get('pr_count')):
            models.UserCart.objects.create(user_id=request.user.id,
                                           user_product=checker,
                                           suer_product_quality=int(request.POST.get('pr_count'))).save()
            return redirect('/products')
        else:
            return redirect(f'/product/{checker.product_name}')



# Отображение корзины пользователя
def get_exact_user_cart(request):
    user_cart = models.UserCart.objects.filter(user_id=request.user.id)
    return render(request, 'UserCart.html', {'user_cart':user_cart})


# Удаление продукта с корзины
def delete_exact_user_cart(request, pk):
    product_to_delete = models.Product.objects.get(id=pk)

    models.UserCart.objects.filter(user_id=request.user.id,
                                user_product=product_to_delete).delete()

    return redirect('/user_cart')

# Оформление заказа
def checkout_page(request):
    checkout_cart_products = models.UserCart.objects.filter(user_id=request.user.id)
    total_price = 0
    text = 'Ваш заказ:  '
    for checkout in checkout_cart_products:
        text += f'{checkout.user_product.product_name} - {checkout.suer_product_quality} x {checkout.user_product.product_price} = {checkout.suer_product_quality * checkout.user_product.product_price} \n'
        total_price += int(checkout.suer_product_quality) * float(checkout.user_product.product_price)
    admin_id = 109839409
    text += f'\nОбщая сумма заказа: {total_price}'
    bot.send_message(admin_id, text)

    models.UserCart.objects.filter(user_id=request.user.id).delete()
    return redirect('/')







