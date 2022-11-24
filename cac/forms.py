from django import forms
from django.forms import ValidationError

from .models import Curso, Categoria, EstudianteM, Proyecto

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def solo_caracteres(valor):
    if any(char.isdigit() for char in valor):
        raise ValidationError('El campo no puede contener números. %(valor)s',
                                code='Error1',
                                params={'valor':valor}
                                )

class ContactoForm(forms.Form):

    TIPO_CONSULTA = (
        ('','-Seleccione-'),
        (1,'Inscripciones'),
        (2,'Soporte Aula Virtual'),
        (3,'Ser docente'),
    )
    
    nombre = forms.CharField(
            label='Nombre',
            max_length=50,
            required=False,
            validators=(solo_caracteres,),
            widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese nombre'})
        )
    email = forms.EmailField(
            label='Email',
            max_length=150,
            error_messages={
                'required':'Por favor completa el email'
            },
            widget=forms.TextInput(attrs={'class':'form-control','type':'email'})
        )
    asunto = forms.CharField(
            label='Asunto',
            max_length=100,
            widget=forms.TextInput(attrs={'class':'form-control'})
        )
    mensaje = forms.CharField(
            label='Mensaje',
            max_length=500,
            widget=forms.Textarea(attrs={'class':'form-control','rows':5})
        )
    suscripcion = forms.BooleanField(
        label='Deseo suscribirme a las novedades de codo a codo',
        required=False,
        widget=forms.CheckboxInput(attrs={'class':'form-check-input','value':1})
    )

    tipo_consulta = forms.ChoiceField(
        label='Tipo de consulta',
        choices=TIPO_CONSULTA,
        initial='2',
        widget=forms.Select(attrs={'class':'form-control'})
    )


    def clean_mensaje(self):
        data = self.cleaned_data['mensaje']
        if len(data) < 10:
            raise ValidationError('Debes especificar mejor el mensaje')
        return data

    def clean_asunto(self):
        data = self.cleaned_data['asunto']
        return 'Asunto-'+data

    
    def clean(self):
        cleaned_data = super().clean()
        asunto = cleaned_data.get("asunto")
        suscripcion = cleaned_data.get("suscripcion")


        if suscripcion and asunto and "suscripcion" not in asunto:
            msg = "Debe agregar la palabara 'suscripcion' al asunto."
            self.add_error('asunto', msg)
            
class CategoriaForm(forms.ModelForm):

    # nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese nombre'}),error_messages={'required':'Por favor no te olvide de mi!'})
    class Meta:
        model=Categoria
        #fields='__all__'
        fields=['nombre']
        #exclude=('baja',)
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese nombre'})
        }
        error_messages={
            'nombre': {
                'required':'No te olvides del nombre!'
            }
        }
    
class CategoriaFormValidado(CategoriaForm):

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if nombre.upper() == 'ORIGAMI':
            raise ValidationError('Codo a codo no dicta esta categoria de cursos')
        return nombre

class CursoForm(forms.ModelForm):

    class Meta:
        model=Curso
        fields=['nombre','fecha_inicio','portada','descripcion','categoria']

    nombre=forms.CharField(
            label='Nombre', 
            widget=forms.TextInput(attrs={'class':'form-control'})
        )
    fecha_inicio=forms.DateField(
            label='Fecha Inicio', 
            widget=forms.DateInput(attrs={'class':'form-control','type':'date'})
        )
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5,'class':'form-control'})
    )
    """Se utiliza ModelChoiceField para poder realizar un filtrado de lo que
    quiero mostrar en el selector"""
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(baja=False),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    portada = forms.ImageField(
        widget=forms.FileInput(attrs={'class':'form-control'})
    )

class EstudianteMForm(forms.ModelForm):

    class Meta:
        model=EstudianteM
        fields=['nombre_m','apellido_m','email_m','dni_m','matricula_m']
        widgets = {
            'nombre_m': forms.TextInput(attrs={'class':'form-control'}),
            'apellido_m': forms.TextInput(attrs={'class':'form-control'}),
            'email_m': forms.EmailInput(attrs={'class':'form-control'}),
            'dni_m': forms.NumberInput(attrs={'class':'form-control'}),
            'matricula_m': forms.TextInput(attrs={'class':'form-control'}),
        }


class ProyectoForm(forms.ModelForm):
    
    class Meta:
        model=Proyecto
        fields=['nombre','descripcion','anio','url','portada','estudiante']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'descripcion': forms.Textarea(attrs={'cols': 80, 'rows': 5,'class':'form-control'}),
            'anio': forms.NumberInput(attrs={'class':'form-control'}),
            'url': forms.URLInput(attrs={'class':'form-control'}),
            'portada': forms.FileInput(attrs={'class':'form-control'}),
            'estudiante': forms.Select(attrs={'class':'form-control'}),
        }


class RegistrarUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email' , 'password1', 'password2']