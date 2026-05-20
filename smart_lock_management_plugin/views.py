"""
Views for smart_lock_management_plugin.

For more information on NetBox views, see:
https://docs.netbox.dev/en/stable/plugins/development/views/

For generic view classes, see:
https://docs.netbox.dev/en/stable/development/views/
"""

import json
import logging
import os
import shutil
import uuid

from django.http import JsonResponse, QueryDict

from extras.models.models import ImageAttachment
from extras.ui.panels import TagsPanel
from netbox import settings
from netbox.views.generic.feature_views import ObjectImageAttachmentsView
from netbox.ui.layout import SimpleLayout
from utilities.views import ViewTab, register_model_view
from netbox.views import generic
from utilities.exceptions import AbortRequest, PermissionsViolation
from utilities.forms.utils import restrict_form_fields
from django.db import transaction, router
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from utilities.views import GetRelatedModelsMixin
from .ui.panels import CustomImageAttachentPanels, SmartLockPanel
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from netbox.ui import panels
from .bulk_edit_form import SmartLockBulkEditForm
from .bulk_import_form import SmartLockBulkImportCSVForm
from upload_file_plugin.models import UploadedFile
from upload_file_plugin.views import SaveFilesView
from django.utils.translation import gettext_lazy as _

from . import filtersets, forms, models, tables

def get_image_count(instance):
    try:
        return UploadedFile.objects.filter(
            model_name=instance._meta.model_name,
            object_id=instance.pk
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
            CustomImageAttachentPanels(),
             
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
        

@register_model_view(model=models.SmartLock, name="attachments", path="attachments")
class SmartLockImageView(generic.ObjectView):
    queryset= models.SmartLock.objects.all()
    template_name = 'smart_lock_management_plugin/smartlock_attachments.html'

    tab = ViewTab(
        label=_('Attachments'),
        badge=get_image_count,
        weight=500
    )
    def get_extra_context(self, request, instance):
        uploaded_files = UploadedFile.objects.filter(
            model_name=instance._meta.model_name,
            object_id=instance.pk
        ).order_by("-created_at")

        return {
            "uploaded_files": uploaded_files,
        }
    

class SmartLockEditView(generic.ObjectEditView):
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
        
                    all_files = request.POST.get("all_files", "[]")
        
                    if all_files and all_files.strip() != "[]":
                        temp_data = QueryDict(mutable=True)
                        temp_data.update({
                            "all_files": all_files,
                            "model_name": obj._meta.model_name,
                            "object_id": str(obj.pk)
                        })
            
                        original_data = getattr(request, "_data", None)
                        request.data = temp_data
            
                        try:
                            save_view = SaveFilesView()
                            result = save_view.post(request)
                            result_data = json.loads(result.content)
                
                            if not result_data.get("success"):
                                raise AbortRequest(
                                f"Failed to save attachments: {result_data.get('errors')}"
                            )
                
                            saved_files = result_data.get("saved_files", [])
                
                            for file_info in saved_files:
                    
                                file_name = os.path.basename(file_info["path"])
                    
                    
                                old_full = os.path.join(settings.MEDIA_ROOT, file_name)
                                new_relative = os.path.join("uploads", obj._meta.model_name, file_name)
                                new_full = os.path.join(settings.MEDIA_ROOT, new_relative)
                    
                                os.makedirs(os.path.dirname(new_full), exist_ok=True)
                    
                                if os.path.exists(old_full):
                                    shutil.move(old_full, new_full)
                                    logger.info(f"Moved file: {old_full} -> {new_full}")
                                    UploadedFile.objects.filter(
                                    object_id=obj.pk,
                                    model_name=obj._meta.model_name,
                                    file=file_name
                                ).update(file=new_relative)
                                    logger.info(f"Updated DB path: {file_name} -> {new_relative}")
                                else:
                                    logger.warning(f"File not found after save: {old_full}")
                
                        
                            all_files_list = json.loads(all_files)
                            allowed_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', 'tmp')
                
                            for file_dict in all_files_list:
                                temp_path = file_dict.get("path", "")
                                abs_temp_path = os.path.abspath(temp_path)
                    
                                if not abs_temp_path.startswith(os.path.abspath(allowed_dir)):
                                    logger.warning(f"Invalid temp path, skipping: {temp_path}")
                                    continue
                    
                                if os.path.exists(abs_temp_path):
                                    try:
                                        os.remove(abs_temp_path)
                                        logger.info(f"Deleted temp file: {abs_temp_path}")
                                    except Exception as e:
                                        logger.error(f"Error deleting temp file {abs_temp_path}: {e}")
                            
                        finally:
                            if original_data is not None:
                                request.data = original_data
                            elif hasattr(request, "data"):
                                del request.data
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

class SmartLockCreateView(generic.ObjectEditView):
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
        
                    all_files = request.POST.get("all_files", "[]")
        
                    if all_files and all_files.strip() != "[]":
                        temp_data = QueryDict(mutable=True)
                        temp_data.update({
                            "all_files": all_files,
                            "model_name": obj._meta.model_name,
                            "object_id": str(obj.pk)
                        })
            
                        original_data = getattr(request, "_data", None)
                        request.data = temp_data
            
                        try:
                            save_view = SaveFilesView()
                            result = save_view.post(request)
                            result_data = json.loads(result.content)
                
                            if not result_data.get("success"):
                                raise AbortRequest(
                                f"Failed to save attachments: {result_data.get('errors')}"
                            )
                
                            saved_files = result_data.get("saved_files", [])
                
                            for file_info in saved_files:
                    
                                file_name = os.path.basename(file_info["path"])
                    
                    
                                old_full = os.path.join(settings.MEDIA_ROOT, file_name)
                                new_relative = os.path.join("uploads", obj._meta.model_name, file_name)
                                new_full = os.path.join(settings.MEDIA_ROOT, new_relative)
                    
                                os.makedirs(os.path.dirname(new_full), exist_ok=True)
                    
                                if os.path.exists(old_full):
                                    shutil.move(old_full, new_full)
                                    logger.info(f"Moved file: {old_full} -> {new_full}")
                                    UploadedFile.objects.filter(
                                    object_id=obj.pk,
                                    model_name=obj._meta.model_name,
                                    file=file_name
                                ).update(file=new_relative)
                                    logger.info(f"Updated DB path: {file_name} -> {new_relative}")
                                else:
                                    logger.warning(f"File not found after save: {old_full}")
                
                        
                            all_files_list = json.loads(all_files)
                            allowed_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', 'tmp')
                
                            for file_dict in all_files_list:
                                temp_path = file_dict.get("path", "")
                                abs_temp_path = os.path.abspath(temp_path)
                    
                                if not abs_temp_path.startswith(os.path.abspath(allowed_dir)):
                                    logger.warning(f"Invalid temp path, skipping: {temp_path}")
                                    continue
                    
                                if os.path.exists(abs_temp_path):
                                    try:
                                        os.remove(abs_temp_path)
                                        logger.info(f"Deleted temp file: {abs_temp_path}")
                                    except Exception as e:
                                        logger.error(f"Error deleting temp file {abs_temp_path}: {e}")
                            
                        finally:
                            if original_data is not None:
                                request.data = original_data
                            elif hasattr(request, "data"):
                                del request.data
                        
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
    
class UploadFileFormView(LoginRequiredMixin, TemplateView):
    template_name = "smart_lock_management_plugin/uploadmodal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_id"] = self.request.GET.get("object_id")
        context["model_name"] = self.request.GET.get("model_name")
        context["return_url"] = self.request.GET.get("return_url")
        return context
    
class SmartLockBulkEditView(generic.BulkEditView):
    queryset= models.SmartLock.objects.all()
    form= SmartLockBulkEditForm
    table= tables.SmartLockTable
    filterset= filtersets.SmartLockFilterSet

class SmartLockBulkDeleteView(generic.BulkDeleteView):
    queryset= models.SmartLock.objects.all()
    table= tables.SmartLockTable
    filterset= filtersets.SmartLockFilterSet

@require_http_methods(["POST"])
def save_smartlock_attachments(request):
    try:
        all_files_json = request.POST.get("all_files", "[]")
        model_name = request.POST.get("model_name", "smartlock").lower()
        object_id = request.POST.get("object_id")
        if not object_id:
            return JsonResponse({
                "success": False,
                "error": "Missing object_id"
            }, status=400)
        try:
            files= json.loads(all_files_json)
        except json.JSONDecodeError as e:
            return JsonResponse({
                "success": False,
                "error":"Invalid all_files JSON"
            }, status= 400)
        target_dir = os.path.join(settings.MEDIA_ROOT, "uploads", model_name)
        os.makedirs(target_dir, exist_ok=True)

        saved_files = []
        errors = []
        
        client_file_names = [
            f.get("file_name")
            for f in files
            if f.get("file_name")
        ]
        
        old_files_qs = UploadedFile.objects.filter(
            model_name=model_name,
            object_id=object_id
        )

        files_to_delete = old_files_qs.exclude(
            file_name__in=client_file_names
        )
        
        for file_obj in files_to_delete:
            try:
                if file_obj.file and file_obj.file.path and os.path.exists(file_obj.file.path):
                    os.remove(file_obj.file.path)
                file_obj.delete()
            except Exception as e:
                errors.append(
                    f"Failed to delete old file '{file_obj.file_name}': {e}"
                )

        existing_names = set(
            UploadedFile.objects.filter(
                model_name=model_name,
                object_id=object_id
            ).values_list("file_name", flat=True)
        )

        for file_dict in files:
            file_name = file_dict.get("file_name")
            temp_path = file_dict.get("path")

            if file_name in existing_names:
                continue
            
            if not temp_path or not os.path.exists(temp_path):
                continue

            try:
                
                base_name, ext = os.path.splitext(file_name)
                unique_name = f"{base_name}_{uuid.uuid4().hex}{ext}"

                final_path = os.path.join(target_dir, unique_name)

                os.replace(temp_path, final_path)

                relative_path = os.path.join(
                    "uploads",
                    model_name,
                    unique_name
                ).replace("\\", "/")

                uploaded_file = UploadedFile.objects.create(
                    file=relative_path,
                    file_name=file_name,
                    model_name=model_name,
                    object_id=object_id,
                )

                saved_files.append({
                    "id": uploaded_file.id,
                    "file_name": uploaded_file.file_name,
                    "path": uploaded_file.file.url,
                    "size": uploaded_file.file.size,
                })

            except Exception as e:
                errors.append(
                    f"Failed to save '{file_name}': {e}"
                )

        return JsonResponse({
            "success": len(errors) == 0,
            "saved_files": saved_files,
            "errors": errors,
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)