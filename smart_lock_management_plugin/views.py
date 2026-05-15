"""
Views for smart_lock_management_plugin.

For more information on NetBox views, see:
https://docs.netbox.dev/en/stable/plugins/development/views/

For generic view classes, see:
https://docs.netbox.dev/en/stable/development/views/
"""

import logging

from extras.models.models import ImageAttachment
from extras.ui.panels import ImageAttachmentsPanel
from extras.ui.panels import TagsPanel
from netbox.views.generic.feature_views import ObjectImageAttachmentsView
from netbox.ui.layout import SimpleLayout
from utilities.views import ViewTab, register_model_view
from netbox.views import generic
from utilities.exceptions import AbortRequest, PermissionsViolation
from utilities.forms.utils import restrict_form_fields
from django.db import transaction, router
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.core.exceptions import ValidationError
from utilities.views import GetRelatedModelsMixin
from .ui.panels import SmartLockPanel
from .utils import ImageAttachmentNewUploadMixin, ImageAttachmentUploadMixin 
from netbox.ui import panels
from .bulk_edit_form import SmartLockBulkEditForm
from .bulk_import_form import SmartLockBulkImportCSVForm

from . import filtersets, forms, models, tables

def get_image_count(obj):
    try:
        # Use object_type_id to match NetBox's internal field schema
        return ImageAttachment.objects.filter(
            object_type_id=ContentType.objects.get_for_model(obj).id,
            object_id=obj.pk
        ).count()
    except Exception:
        return 0

class SmartLockListView(generic.ObjectListView):
    queryset= models.SmartLock.objects.all()
    table= tables.SmartLockTable
    filterset= filtersets.SmartLockFilterSet
    filterset_form= forms.SmartLockFilterForm

class SmartLockView(GetRelatedModelsMixin, generic.ObjectView):
    queryset = models.SmartLock.objects.all()
    layout= SimpleLayout(
        left_panels=[
            SmartLockPanel(),
            TagsPanel()
        ],
        right_panels=[
            panels.RelatedObjectsPanel(),
            ImageAttachmentsPanel(),
             
        ]
    )
    def get_extra_context(self, request, instance):
        return {
            "related_models": self.get_related_models(
                request,
                instance,
                omit=[],
            )
        }
        

@register_model_view(model=models.SmartLock, name="images", path="images")
class SmartLockImageView(ObjectImageAttachmentsView):
    queryset= models.SmartLock.objects.all()
    child_model= ImageAttachment
    template_name = 'generic/object_children.html'

    tab = ViewTab(
        label='Images',
        badge=get_image_count,
        weight=500
    )
    def get(self, request, *args, **kwargs):
        kwargs['model'] = models.SmartLock
        return super().get(request, *args, **kwargs)
    

class SmartLockEditView(ImageAttachmentUploadMixin, generic.ObjectEditView):
    queryset= models.SmartLock.objects.all()
    form= forms.SmartLockEditForm

    def alter_object(self, obj, request, url_args, url_kwargs):
        
        if obj.pk is None and not obj.created_by:
            obj.created_by = request.user
        return obj

    def post(self, request, *args, **kwargs):
        logger = logging.getLogger("netbox.views.ObjectEditView")

        obj = self.get_object(**kwargs)
        model = self.queryset.model

        
        if obj.pk and hasattr(obj, "snapshot"):
            obj.snapshot()

        obj = self.alter_object(obj, request, args, kwargs)

        
        form_prefix = "quickadd" if request.GET.get("_quickadd") else None
        form = self.form(
            data=request.POST,
            files=request.FILES,
            instance=obj,
            prefix=form_prefix,
        )
        restrict_form_fields(form, request.user)

        if form.is_valid():
            logger.debug("Form validation was successful")
            obj._changelog_message = form.cleaned_data.pop(
                "changelog_message", ""
            )

            try:
                with transaction.atomic(using=router.db_for_write(model)):
                    object_created = form.instance.pk is None
                    obj = form.save()

   
                    if not self.queryset.filter(pk=obj.pk).exists():
                        raise PermissionsViolation()

                    uploaded_count = self.save_uploaded_attachments(
                                        request=request,
                                        obj=obj,
                                        form=form,
                                    )
                    if uploaded_count:
                        selected_images = form.cleaned_data.get(
                        "image_attachment"
                    )
                        if selected_images:
                            messages.success(
                                request,
                                f"Updated {min(len(selected_images), uploaded_count)} "
                                f"attachment(s) successfully."
                            )

                            extra_files = uploaded_count - len(selected_images)
                            if extra_files > 0:
                                messages.success(
                                        request,
                                        f"Created {extra_files} new attachment(s)."
                                    )
                        else:
                            messages.success(
                            request,
                            f"Uploaded {uploaded_count} new attachment(s)."
                        )
                
                msg = "{} {}".format(
                    "Created" if object_created else "Modified",
                    self.queryset.model._meta.verbose_name,
                )

                logger.info(f"{msg} {obj} (PK: {obj.pk})")

                if hasattr(obj, "get_absolute_url"):
                    msg = mark_safe(
                        f'{msg} <a href="{obj.get_absolute_url()}">'
                        f"{escape(obj)}</a>"
                    )
                else:
                    msg = f"{msg} {obj}"

                messages.success(request, msg)

                
                if "_quickadd" in request.POST:
                    return render(
                        request,
                        "htmx/quick_add_created.html",
                        {"object": obj},
                    )

                
                if "_addanother" in request.POST:
                    return redirect(request.path)

                
                return_url = self.get_return_url(request, obj)

                
                if request.htmx:
                    from django.http import HttpResponse

                    return HttpResponse(
                        headers={"HX-Location": return_url}
                    )

                return redirect(return_url)

            except (
                AbortRequest,
                PermissionsViolation,
                ValidationError,
            ) as e:
                error_message = getattr(e, "message", str(e))
                logger.debug(error_message)
                form.add_error(None, error_message)

        else:
            logger.debug("Form validation failed")

       
        context = {
            "model": model,
            "object": obj,
            "form": form,
            "return_url": self.get_return_url(request, obj),
            **self.get_extra_context(request, obj),
        }

        if "_quickadd" in request.POST:
            return render(
                request,
                "htmx/quick_add.html",
                context,
            )

        return render(
            request,
            self.template_name,
            context,
        )

class SmartLockCreateView(ImageAttachmentNewUploadMixin,generic.ObjectEditView):
    queryset= models.SmartLock.objects.all()
    form= forms.SmartLockForm
    def alter_object(self, obj, request, url_args, url_kwargs):
        if obj.pk is None and not obj.created_by:
            obj.created_by= request.user
        return obj
    def post(self, request, *args, **kwargs):
        logger = logging.getLogger('netbox.views.ObjectEditView')
        obj = self.get_object(**kwargs)
        model = self.queryset.model

        
        if obj.pk and hasattr(obj, 'snapshot'):
            obj.snapshot()

        obj = self.alter_object(obj, request, args, kwargs)

        form_prefix = 'quickadd' if request.GET.get('_quickadd') else None
        form = self.form(data=request.POST, files=request.FILES, instance=obj, prefix=form_prefix)
        restrict_form_fields(form, request.user)
        if form.is_valid():
            logger.debug("Form validation was successful")
            obj._changelog_message = form.cleaned_data.pop('changelog_message', '')

            try:
                with transaction.atomic(using=router.db_for_write(model)):
                    object_created = form.instance.pk is None
                    obj = form.save()

                    if not self.queryset.filter(pk=obj.pk).exists():
                        raise PermissionsViolation()

                    uploaded_file_count = self.save_new_upload_attachments(
                        request=request, 
                        object=obj, 
                        form= form
                    )
                    if uploaded_file_count:
                        
                        messages.success(request, f"Uploaded {uploaded_file_count} files successfully")
                        
                msg = '{} {}'.format(
                    'Created' if object_created else 'Modified',
                    self.queryset.model._meta.verbose_name
                )
                logger.info(f"{msg} {obj} (PK: {obj.pk})")
                if hasattr(obj, 'get_absolute_url'):
                    msg = mark_safe(f'{msg} <a href="{obj.get_absolute_url()}">{escape(obj)}</a>')
                else:
                    msg = f'{msg} {obj}'
                messages.success(request, msg)

                
                if '_quickadd' in request.POST:
                    return render(request, 'htmx/quick_add_created.html', {
                        'object': obj,
                    })

                
                if '_addanother' in request.POST:
                    redirect_url = request.path
                    return redirect(redirect_url)

                return_url = self.get_return_url(request, obj)

                # HTMX
                if request.htmx:
                    from django.http import HttpResponse
                    return HttpResponse(headers={'HX-Location': return_url})

                return redirect(return_url)

            except (AbortRequest, PermissionsViolation, ValidationError) as e:
                logger.debug(e.message)
                form.add_error(None, e.message)

        else:
            logger.debug("Form validation failed")

        context = {
            'model': model,
            'object': obj,
            'form': form,
            'return_url': self.get_return_url(request, obj),
            **self.get_extra_context(request, obj),
        }

        if '_quickadd' in request.POST:
            return render(request, 'htmx/quick_add.html', context)

        return render(request, self.template_name, context)
             
class SmartLockDeleteView(generic.ObjectDeleteView):
    queryset= models.SmartLock.objects.all()
    
class SmartLockBulkImportView(generic.BulkImportView):
    queryset= models.SmartLock.objects.all()
    model_form= SmartLockBulkImportCSVForm
    def save_object(self, object_form, request):
        obj = object_form.save(commit=False)
        if obj.pk is None and hasattr(obj, 'created_by'):
            obj.created_by = request.user
        obj.save()
        object_form.save_m2m()
        return obj
    
class SmartLockBulkEditView(generic.BulkEditView):
    queryset= models.SmartLock.objects.all()
    form= SmartLockBulkEditForm
    table= tables.SmartLockTable
    filterset= filtersets.SmartLockFilterSet

class SmartLockBulkDeleteView(generic.BulkDeleteView):
    queryset= models.SmartLock.objects.all()
    table= tables.SmartLockTable
    filterset= filtersets.SmartLockFilterSet

