from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
@receiver(post_delete, sender=Order)
def update_total_spent(sender, instance, **kwargs):
    """Update customer's total spent whenever an order is created, updated, or deleted."""
    if instance.customer and hasattr(instance.customer, "customer_profile"):
        print('tsting')
        instance.customer.customer_profile.update_total_spent()
