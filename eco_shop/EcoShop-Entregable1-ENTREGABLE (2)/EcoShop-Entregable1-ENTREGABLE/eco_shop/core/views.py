from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, CartItem
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST

from .forms import CustomUserCreationForm
from .models import Product, Category, Wishlist, Order


# -------------------------
# 🔹 Autenticación
# -------------------------
def signup(request):
    """Registro de nuevos usuarios con email obligatorio"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # login automático tras registro
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def account(request):
    """Perfil del usuario"""
    return render(request, "registration/account.html")


# -------------------------
# 🔹 Tienda
# -------------------------
def home(request):
    products = Product.objects.filter(is_active=True)[:12]
    return render(request, "home.html", {"products": products})


def shop(request):
    products = Product.objects.filter(is_active=True)
    return render(request, "shop/list.html", {
        "products": products,
    })


def shop_gender(request, gender):
    products = Product.objects.filter(is_active=True, gender=gender)
    return render(request, "shop/list.html", {"products": products, "gender": gender})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)

    # Recomendaciones: productos de la misma categoría
    related = (
        Product.objects.filter(category=product.category, is_active=True)
        .exclude(id=product.id)[:6]
    )

    in_wishlist = (
        request.user.is_authenticated
        and Wishlist.objects.filter(user=request.user, product=product).exists()
    )

    return render(
        request,
        "shop/detail.html",
        {"product": product, "related": related, "in_wishlist": in_wishlist},
    )


def search(request):
    q = request.GET.get("q", "")
    products = Product.objects.filter(
        Q(name__icontains=q)
        | Q(description__icontains=q)
        | Q(category__name__icontains=q),
        is_active=True,
    )
    return render(request, "shop/list.html", {"products": products, "q": q})


# -------------------------
# 🔹 Wishlist
# -------------------------
@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user).select_related("product")
    return render(request, "shop/wishlist.html", {"items": items})


@login_required
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    w, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        w.delete()
    return redirect("product_detail", slug=product.slug)


# -------------------------
# 🔹 Órdenes
# -------------------------
@login_required
def order_history(request):
    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related("items__product")
        .order_by("-created_at")
    )
    return render(request, "orders/history.html", {"orders": orders})


# -------------------------
# 🔹 Secciones placeholder
# -------------------------
def collections(request):
    return render(request, "shop/collections.html")


def basics(request):
    return render(request, "shop/basics.html")


def cart(request):
    return render(request, "shop/cart.html")


def sale(request):
    return render(request, "sale.html")

from django.contrib.auth.decorators import login_required

@login_required
def account(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items__product").order_by("-created_at")
    return render(request, "auth/account.html", {"orders": orders})
@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    # Lógica básica para agregar a carrito (puedes usar Order + OrderItem)
    order, created = Order.objects.get_or_create(user=request.user, status="cart")
    item, created = order.items.get_or_create(product=product, defaults={"quantity": 1, "price": product.price})
    if not created:
        item.quantity += 1
        item.save()
    return redirect("cart")
@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect("cart")

@login_required
def cart_remove(request, product_id):
    item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
    item.delete()
    return redirect("cart")

@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user).select_related("product")
    total = sum(item.subtotal() for item in items)
    return render(request, "shop/cart.html", {"items": items, "total": total})
@login_required
@require_POST
def cart_update(request, product_id):
    item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
    action = request.POST.get("action")

    if action == "add":
        item.quantity += 1
        item.save()
    elif action == "remove":
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "cart"))
@login_required
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    w, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        w.delete()
    return redirect("shop")  # o "core:product_detail" según prefieras

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect("shop")
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Wishlist

def shop(request):
    # Obtener categoría seleccionada si existe
    category_id = request.GET.get('category', None)
    
    # Filtrar productos
    if category_id:
        products = Product.objects.filter(is_active=True, category_id=category_id)
    else:
        products = Product.objects.filter(is_active=True)
    
    # Obtener todas las categorías para el filtro
    categories = Category.objects.all()
    
    # Si el usuario está logueado, marcamos qué productos ya están en su wishlist
    if request.user.is_authenticated:
        wishlist_ids = Wishlist.objects.filter(user=request.user).values_list("product_id", flat=True)
        for p in products:
            p.in_wishlist = p.id in wishlist_ids
    
    return render(request, "shop/list.html", {
        "products": products, 
        "categories": categories,
        "selected_category": category_id
    })

@login_required
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        wishlist_item.delete()
        messages.success(request, f"{product.name} fue eliminado de tu Wishlist.")
    else:
        messages.success(request, f"{product.name} fue agregado a tu Wishlist.")
    return redirect("shop")
from django.shortcuts import render

def about(request):
    return render(request, "about.html")
    from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Wishlist

@login_required
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:  
        wishlist_item.delete()  # si ya estaba en wishlist, lo elimina

    return redirect("wishlist")

@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user).select_related("product")
    return render(request, "shop/wishlist.html", {"items": items})
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, CartItem

@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user).select_related("product")
    total = sum(item.subtotal() for item in items)
    return render(request, "shop/cart.html", {"items": items, "total": total})

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")

@login_required
def cart_remove(request, product_id):
    item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
    item.delete()
    return redirect("cart")

@login_required
def cart_update(request, product_id, action):
    item = get_object_or_404(CartItem, user=request.user, product_id=product_id)

    if action == "increase":
        item.quantity += 1
        item.save()
    elif action == "decrease":
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

    return redirect("cart")
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import CartItem, Order, OrderItem

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect("cart")  # carrito vacío

    # Crear pedido
    order = Order.objects.create(user=request.user, status="paid")

    # Crear los items del pedido
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    # Vaciar carrito
    cart_items.delete()

    return redirect("order_history")  # redirige a "Mis pedidos"

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import transaction
from .models import CartItem, Order, OrderItem

@login_required
@transaction.atomic
def checkout(request):
    if request.method != "POST":
        # Evita que GET cree pedidos por accidente
        messages.info(request, "Confirma el pago desde el carrito.")
        return redirect("cart")

    items = CartItem.objects.filter(user=request.user).select_related("product")
    if not items.exists():
        messages.warning(request, "Tu carrito está vacío.")
        return redirect("cart")

    # 1) Crear el pedido
    order = Order.objects.create(user=request.user, status="paid")  # o "processing"

    # 2) Crear las líneas
    bulk = []
    for it in items:
        bulk.append(OrderItem(
            order=order,
            product=it.product,
            quantity=it.quantity,
            price=it.product.price
        ))
    OrderItem.objects.bulk_create(bulk)

    # 3) Vaciar carrito
    items.delete()

    messages.success(request, "¡Pago procesado! Tu pedido fue creado.")
    return redirect("account")  # o la URL donde muestras el historial de pedidos
