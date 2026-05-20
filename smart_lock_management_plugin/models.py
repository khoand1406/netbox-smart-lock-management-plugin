"""
Models for smart_lock_management_plugin.

For more information on NetBox models, see:
https://docs.netbox.dev/en/stable/plugins/development/models/

For NetBox model features (tags, custom fields, change logging, etc.), see:
https://docs.netbox.dev/en/stable/development/models/#netbox-model-features
"""


from django.db import models
from django.urls import reverse
from dcim.models.racks import Rack
from dcim.models.sites import Location, Site
from netbox import settings
from dcim.models.sites import Region
from netbox.models import NetBoxModel
from netbox.models.features import ImageAttachmentsMixin
from .choices import RackFaceChoices, SmartLockStatusChoices
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class SmartLock(ImageAttachmentsMixin, NetBoxModel):
    name= models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        unique= True
    )
    code= models.CharField(
        max_length=100,
        verbose_name=_("Code"),
        unique=True
    )
    status= models.CharField(
        max_length=30,
        choices=SmartLockStatusChoices,
        default= SmartLockStatusChoices.STATUS_ACTIVE,
        verbose_name=_("Status")
    )
    description = models.TextField(
        max_length=500,
        blank=True,
        verbose_name=_("Description")
    )

    device_type = models.CharField(
        max_length=100,
        blank=False,
        verbose_name=_("Device Type")
    )

    manufacturer= models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Manufacturer")
    )

    model = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Model")
    )

    serial = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Serial")
    )

    # Thông tin thời gian
    installation_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Installation Date")
    )

    purchase_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Purchase Date")
    )

    warranty_period = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
        verbose_name=_("Warranty Period (months)")
    )
    
    warranty_expiry_date= models.DateField(
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Warranty Expires Date")
    )

    # Vị trí
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="smart_locks",
        blank=True,
        null=True,
        verbose_name=_("Region")
    )
    
    site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        related_name="smart_locks",
        verbose_name=_("Site")
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="smart_locks",
        verbose_name=_("Location")
    )

    rack = models.ForeignKey(
        Rack,
        on_delete=models.PROTECT,
        related_name="smart_locks",
        blank=True,
        null=True,
        verbose_name=_("Rack")
    )

    rack_face = models.CharField(
        max_length=50,
        choices=RackFaceChoices,
        blank=True,
        verbose_name=_("Rack Face")
    )

    # Metadata
    created_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ("-last_updated",)
        verbose_name = _("Smart Lock")
        verbose_name_plural = _("Smart Locks")

    def __str__(self):
        return f"{self.name} ({self.code})"

    def clean(self):
        """
        Validation logic
        """
        from django.core.exceptions import ValidationError
        
        if self.location_id and self.site_id:
            location = Location.objects.filter(pk=self.location_id).first()
            if location and location.site_id != self.site_id:
                raise ValidationError({
                    "location": _("Location must belong to the assigned site.")
                })

        if self.rack_id and self.location_id:
            rack = Rack.objects.filter(pk=self.rack_id).first()
            if rack and rack.location_id != self.location_id:
                raise ValidationError({
                    "rack": _("Rack must belong to the assigned location.")
            })

        if self.rack_id and self.site_id:
            rack = Rack.objects.filter(pk=self.rack_id).first()
            if rack and rack.site_id != self.site_id:
                raise ValidationError({
                "rack": _("Rack must belong to the assigned site.")
            })
        

    def save(self, *args, **kwargs):
        """
        Override save method để tự động tính warranty_expiry_date
        """
        if self.purchase_date and self.warranty_period:
            from dateutil.relativedelta import relativedelta
            self.warranty_expiry_date = self.purchase_date + relativedelta(months=self.warranty_period)
        else:
            self.warranty_expiry_date = None
            
        super().save(*args, **kwargs)

    @property
    def is_under_warranty(self):
        """
        Kiểm tra thiết bị còn trong thời gian bảo hành hay không
        """
        if self.warranty_expiry_date:
            from django.utils import timezone
            return timezone.now().date() <= self.warranty_expiry_date
        return False
    
    
    def get_status_color(self):
        """
        Trả về màu sắc hiển thị cho trạng thái
        """
        status_colors = {
            SmartLockStatusChoices.STATUS_ACTIVE: _('success'),
            SmartLockStatusChoices.STATUS_INACTIVE: _('danger'),
            SmartLockStatusChoices.STATUS_MAINTENANCE: _('warning'),
            SmartLockStatusChoices.STATUS_FAULT: _('secondary'),
        }
        return status_colors.get(self.status, _('secondary'))
    def get_absolute_url(self):
        return reverse(
            "plugins:smart_lock_management_plugin:smartlock",
            args=[self.pk]
        )
