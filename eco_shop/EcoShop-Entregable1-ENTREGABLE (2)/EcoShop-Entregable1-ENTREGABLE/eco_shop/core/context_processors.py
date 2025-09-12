from django.conf import settings
from django.contrib.auth.models import AnonymousUser

def site_defaults(request):
    user = request.user if request.user.is_authenticated else AnonymousUser()
    wishlist_count = 0
    try:
        if user.is_authenticated:
            from core.models import Wishlist
            wishlist_count = Wishlist.objects.filter(user=user).count()
    except Exception:
        pass  # evita fallar si aún no migras

    cart_count = 0  # placeholder si luego agregas carrito
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "DOUX"),
        "wishlist_count": wishlist_count,
        "cart_count": cart_count,
    }
