"""Общие показатели, доступные навигации на всех страницах."""
from products_web.models import Product
from suppliers_web.models import Supplier
from applications_web.models import Application
from orders_web.models import PurchaseOrder


def procurement_context(request):
    """Передаёт количество сущностей в общий шаблон без дублирования view."""
    return {
        "procurement_counts": {
            "products": Product.objects.count(),
            "suppliers": Supplier.objects.count(),
            "applications": Application.objects.count(),
            "orders": PurchaseOrder.objects.count(),
        },
    }
