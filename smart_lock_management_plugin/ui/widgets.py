from typing import Any

from django import forms
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected= True
    
class MultipleFileField(forms.FileField):
    widget= MultipleFileInput
    def clean(self, data: Any, initial: Any | None = ...) -> Any:
        if not data:
            return []

        if isinstance(data, (list, tuple)):
            return [super(MultipleFileField, self).clean(d, initial) for d in data]

        return [super(MultipleFileField, self).clean(data, initial)]