from extras.models.models import ImageAttachment
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

class ImageAttachmentUploadMixin:
    
    attachment_field_name = "attachment"
    selected_images_field_name = "image_attachment"

    def save_uploaded_attachments(self, request, obj, form):
        uploaded_files = request.FILES.getlist(
            self.attachment_field_name
        )

        # Các ImageAttachment được chọn trong form
        selected_images = list(
            form.cleaned_data.get(
                self.selected_images_field_name,
                []
            )
        )

        
        if not uploaded_files:
            return 0

        content_type = ContentType.objects.get_for_model(obj)
        uploaded_count = 0

        
        for index, uploaded_file in enumerate(uploaded_files):
            try:
                
                if index < len(selected_images):
                    image = selected_images[index]

                    if image.image:
                        image.image.delete(save=False)
                    
                    image.name = uploaded_file.name.rsplit(".", 1)[0]

                else:
                    
                    image = ImageAttachment(
                        object_type=content_type,
                        object_id=obj.pk,
                        name=uploaded_file.name.rsplit(".", 1)[0],
                    )

                # Lưu file mới
                image.image.save(
                    uploaded_file.name,
                    uploaded_file,
                    save=True,
                )

                uploaded_count += 1

            except Exception as e:
                raise ValidationError(
                    f"Error uploading file "
                    f"'{uploaded_file.name}': {e}"
                )

        return uploaded_count
    
class ImageAttachmentNewUploadMixin:
    attach_field_name= "attachment"
    def save_new_upload_attachments(self, request, object, form):
        uploaded_files= request.FILES.getlist(self.attach_field_name)
        if not uploaded_files:
            return 0
        content_type= ContentType.objects.get_for_model(object)
        uploaded_count= 0
        for file in (uploaded_files):
            try:
                image= ImageAttachment(object_type= content_type, 
                                        object_id= object.pk, 
                                        name= file.name.rsplit(".", 1)[0])
                image.image.save(file.name, file, save=True)
                uploaded_count+=1
            except Exception as e:
                raise ValidationError(
                    f"Error uploading file "
                    f"'{file.name}': {e}"
                )
        return uploaded_count