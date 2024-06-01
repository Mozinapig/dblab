# -*- encoding: utf-8 -*-
"""
@Modify Time : 2024/5/31 17:53      
@Author : Mozinapig   
@Version : 1.0  
@Desciption : None
  
"""
from django import forms

class BootStrap:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }

class BootStrapModelForm(BootStrap,forms.ModelForm):
    pass


class BootStrapForm(BootStrap,forms.Form):
    pass