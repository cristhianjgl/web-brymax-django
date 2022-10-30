from django import forms
from tasks.models import Task, Prediction

class TaskForm(forms.ModelForm):
  class Meta:
    model = Task
    fields = ['title','description','important']
    widgets = {
      'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Write a title'}),
      'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Write a description'}),
      'important': forms.CheckboxInput(attrs={'class':'form-check-input m-auto'})
    }

class PredictionForm(forms.ModelForm):
  class Meta:
    model = Prediction
    fields = ['nombres','apellidos','numero_documento','numero_embarazos','glucuosa','presion_arterial',
      'espesor_piel','insulina','indice_masa_corporal','funcion_pedigree_diabetes','edad']
    widgets = {
      'nombres': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombres'}),
      'apellidos': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Apellidos'}),
      'numero_documento': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Numero documento'}),
      'numero_embarazos': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Numero embarazos'}),
      'glucuosa': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Glucosa'}),
      'presion_arterial': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Presion arterial'}),
      'espesor_piel':forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Espesor de la Piel'}),
      'insulina': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Insulina'}),
      'indice_masa_corporal': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Indice de Masa Corporal'}),
      'funcion_pedigree_diabetes': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Funcion Pedigree Diabetes'}),
      'edad': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Edad'})
    }
