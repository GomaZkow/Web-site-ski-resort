from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CartItem, Product, User

def index(request):
    return render(request, 'main/index.html')

def ski_trail(request):
    return render(request, 'main/ski_trail.html')

def ski_pass(request):
    return render(request, 'main/ski_pass.html')
def events(request):
    events = [
        {
            'event_image': '/img/svg/Events/снегоход.png',
            'event_title': 'Открытие зимнего сезона',
            'event_date': '2 декабря 2024',
            'event_description': 'Начало зимнего сезона традиционно ознаменуется праздничной программой, включающей динамичное шоу, музыкальные выступления и активные развлечения на склонах. В этот день будут доступны бесплатные уроки для новичков и специальные цены на аренду оборудования.',
            'event_family_info': 'Участие для семей с детьми до 12 лет - бесплатное.',
        },
        {
            'event_image': '/img/svg/Events/ночная_трасса.png',
            'event_title': 'Ночная трасса',
            'event_date': '31 декабря 2024',
            'event_description':'Присоединяйтесь к нам для незабываемого новогоднего праздника на склонах! Ночная трасса будет освещена, а трассы доступны для катания после заката. Программа включает фейерверк и праздничные угощения.',
            'event_family_info': 'Участие для семей с детьми до 12 лет - бесплатное.',
        },
        {
            'event_image': '/img/svg/Events/зимние_прогулки 1.png',
            'event_title': 'Снегоступы и зимние прогулки',
            'event_date': '20 февраля 2025',
            'event_description': 'Приглашаем вас насладиться зимней природой на наших снежных маршрутах! Мы предлагаем организованные походы с гидом для всех желающих, включая занятия по ориентированию на местности.',
            'event_family_info': 'Участие для семей с детьми до 12 лет - бесплатное.',
        },
        {
            'event_image': '/img/svg/Events/Зимние.png',
            'event_title': 'Фестиваль зимних видов спорта',
            'event_date': '10-12 марта 2025',
            'event_description': 'Трёхдневный фестиваль, посвящённый зимним видам спорта, будет включать конкурсы, мастер-классы и показательные выступления. Вы сможете поучаствовать в различных активностях и насладиться атмосферой зимних праздников.',
            'event_family_info': 'Участие для семей с детьми до 12 лет - бесплатное.',
        },
    ]
    return render(request, 'main/events.html', {'events': events})

def photos(request):
    return render(request, 'main/photos.html')

def reviews(request):
    testimonials = [
        {
            'image_path': 'img/svg/Отзывы/елена.png',
            'name': 'Елена',
            'text': 'Отличный выбор для семейного отдыха. Детские трассы и зоны отлично оборудованы. Есть инструкторы.'
        },
        {
            'image_path': 'img/svg/Отзывы/евгений.png',
            'name': 'Евгений',
            'text': 'Замечательное место для отдыха с детьми! Всегда чисто и уютно. Рекомендую!'
        },
        {
            'image_path': 'img/svg/Отзывы/марина.png',
            'name': 'Марина',
            'text': 'Прекрасные трассы для всех уровней! От начинающих до профессионалов. Персонал дружелюбный.'
        },
        {
            'image_path': 'img/svg/Отзывы/ксения.png',
            'name': 'Ксения',
            'text': 'Горнолыжный курорт с потрясающими склонами, все на высшем уровне. Персонал замечательный.'
        }
    ]
    return render(request, 'main/reviews.html', {'testimonials': testimonials})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Регистрация прошла успешно. Теперь вы можете войти.')
            return redirect('login')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(request, username=phone, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему.')
            return redirect('index')
        else:
            messages.error(request, 'Неверные данные. Проверьте номер телефона или пароль')
    return render(request, 'main/login.html')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'main/cart.html', {'cart_items': cart_items})

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        quantity_adults = request.POST.get('quantity_adults')
        quantity_children = request.POST.get('quantity_children')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            quantity_adults=quantity_adults,
            quantity_children=quantity_children,
            start_date=start_date,
            end_date=end_date
        )

        if not created:
            cart_item.quantity_adults += int(quantity_adults)
            cart_item.quantity_children += int(quantity_children)
            cart_item.save()

        return redirect('cart')
    else:
        return redirect('index')
