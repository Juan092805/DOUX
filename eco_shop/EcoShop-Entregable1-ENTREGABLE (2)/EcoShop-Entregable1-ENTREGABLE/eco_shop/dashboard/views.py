from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, F
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from core.models import OrderItem, Product, Order

@staff_member_required
def stats(request):
    # Ventas por mes (total $)
    ventas_por_mes = (
        OrderItem.objects
        .annotate(month=TruncMonth("order__created_at"))
        .values("month")
        .annotate(total=Sum(F("price") * F("quantity")))
        .order_by("month")
    )

    # Productos con bajo stock
    bajo_stock = Product.objects.filter(is_active=True, stock__lte=5).order_by("stock")[:20]

    # Clientes más activos (más pedidos)
    clientes_top = (
        Order.objects.values("user__username")
        .annotate(cnt=Count("id"))
        .order_by("-cnt")[:10]
    )

    context = {
        "ventas_por_mes": ventas_por_mes,
        "bajo_stock": bajo_stock,
        "clientes_top": clientes_top,
    }
    return render(request, "dashboard/stats.html", context)
