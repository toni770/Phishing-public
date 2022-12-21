from django import forms
from .models import Empresas, Correos, Plantillas

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresas   
        fields = ('nombre',)



class CorreoForm(forms.ModelForm):
    class Meta:
        model = Correos   
        fields = ('correo', 'empresa')
        exclude = ('empresa',)

class PlantillaForm(forms.ModelForm):
    class Meta:
        model = Plantillas
        fields = ('servicio', 'email', 'password', 'asunto', 'mensaje')

        
class DeleteForm(forms.Form):
    delete = forms.CharField(max_length=6)


class PhishingForm(forms.Form):
    phishing = forms.CharField(max_length=8)
    servicio = forms.ModelChoiceField(queryset=Plantillas.objects.all())
