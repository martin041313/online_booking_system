# -*- coding:utf-8 -*-  
'''
@author: Zhao Liyong 
@license: NA
@contact: 3100102825@zju.edu.cn 
@see: NA
 
@version: 0.9.5 
@todo[1.0.0]: css and some form 


this code show how the form is constructed
'''  
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50,widget=forms.HiddenInput())
    file  = forms.FileField()