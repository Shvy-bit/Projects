# ProjectsDjango
* [Project Lab 8](#-laboratorio-8-destinos-turisticos )
* [Project Lab 9](#-laboratorio-9-relaciones-muchos-a-muchos,-impresion-de-pdf-y-emails)
## .Gitignore
El .gitignore contiene principalmente los archivos creados por Github y adicionalmente
- /venv/
- \_\_pycache\_\_/
- .env

Lo cual evitar el envió del entorno virtual solo si es llamado 'venv' y las carpetas '\_\_pycache\_\_' creadas en la prueba de los proyectos de Django, también evita el envió el archivo .env que es usado para contener información privada para el envió de emails
## Requirements.txt
la lista es principalmente las librerías necesarias para la ejecución de Django y adicionalmente 'Pillow' para el manejo de imágenes en el Lab 8 y las librerías necesarias de 'xhtml2pdf' para la implementación de pdf en el Lab 9.
También contiene python-decouple para poder acceder al contenido de .env, y poder usar los datos para el envió de emails

## Laboratorio 8 Destinos turisticos

## Laboratorio 9 Relaciones muchos a muchos, impresión de pdf y emails
Para la creación del proyecto se ejecutó `django-admin startproject Lab09`

Antes de empezar, informar que la Carpeta Lab09/Lab09 fue renombrada por 'config' para evitar confusiones a la hora de realizar el laboratorio
### Objetivos
- #### __Implementar en__ una aplicación en Django el manejo de Bases de datos.
    Para empezar, se creó la aplicación que contendrá los modelos para la base de datos
    ```bash
    django-admin startapp SisVentas
    ```
    en la carpeta 'models' de la aplicación se crearon los modelos
    ```python
    class User(models.Model):
    user_name = models.CharField(max_length=20)
    def __str__(self):
        return self.user_name

    class Client(models.Model):
        client_name = models.CharField(max_length=20)
        whoulesaler = models.BooleanField()
        def __str__(self):
            return self.client_name
    ...
    ```
    [Ver modelos](Lab09/SisVentas/models.py)
- #### Relaciones uno a muchos y muchos a muchos.
    Las conexiones uno a muchos se realizaron con `models.ForeignKey()` y las conexiones muchos a muchos con `models.  ManyToManyField()` pero nombrando a la clase intermedia 'sale_detail' para poder guardar datos relacionados con las   conexiones de las 2 tablas, luego guardar los modelos con
    ```bash
    python manage.py makemigrations
    ```
    ```bash
    python manage.py migrate
    ```
    Pudiendo visualizarlo con el programa DB Browser al cargar el archivo 'db.sqlite3'

    [Tablas](Readme/Tablas.png)
- #### Navegación para visualizar ventas
    Se creó una carpeta templates que contendrá [index.html](Lab09/templates/index.html) que se ejecutará al iniciar el servidor en la ruta principal.
    Tambien se creo un boton que redirige a crear ventas desde /admin que ofrece django, para poder acceder se necesita registrarse.
    El usuario: user
    La contraseña: 12341234
    ```html
    ...
    {% for venta in VentasHtml %} <!--Este for hará que por cada venta, se muestre sus datos en una fila de una tabla-->
        <tr data-href="/venta/{{venta.id}}/pdf/" class="venta-click"> <!--Este 'data-href' hará que al seleccionar muestre el pdf de comprobante de pago-->
            <td>{{ venta.id }}</td>
            <td>{{ venta.date|date:"Y-m-d H:i" }}</td>
            <td>S/. {{ venta.total }}</td>
        </tr>
    ...
    ```
    Este html será llamado mediante 'views'.
    ```py
    ...
    from .models import Sale

    def index(request):
        ventas = Sale.objects.all()
        return render(request, 'index.html', {'VentasHtml': ventas})
    ```
    Para que el servidor pueda encontrar 'index.html' se necesita configurar 'settings'
    ```py
    ...
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'SisVentas', # El nombre de la aplicación
    ]
    ...
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'], # 'templates' o la carpeta que contendrá las plantillas
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
    ...
    ```
    y agregar las urls del proyecto, en la aplicación

    ```py
    ...
    from . import views

    urlpatterns = [
        path('', views.index, name='index'),
    ]
    ```
    
    en config

    ```py
    ...
    from django.urls import path, include # Agregamos 'include'

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('SisVentas.urls')), # Agregamos las urls de la aplicación
    ]
    ```
- #### Implementar la impresion de pdfs y el envio de emails desde una aplicación Django
    Para lograr esto primero creamos la clase que creara el pdf en views con xhml2pdf, en base a los datos de una venta que se buscara según su id y luego usa una [plantilla](Lab09/templates/reportes/factura.html) en la cual se cargaran los datos 
    ```py
    from django.views import View
    from django.http import HttpResponse
    from django.shortcuts import render
    from django.template.loader import get_template
    from django.shortcuts import get_object_or_404
    from xhtml2pdf import pisa
    from .models import Sale

    class DetalleDeVentaPdf(View):
        def get(self, request, sale_id, *args, **kwargs):

            venta = get_object_or_404(Sale, id=sale_id)
            detalles = venta.sale_detail_set.all()
            template = get_template('reportes/factura.html')
            context = {
                'venta': venta,
                'detalles': detalles,
            }

            html_string = template.render(context)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f"inline; filename='Venta {venta.id}.pdf'"

            pisa_status = pisa.CreatePDF(html_string, dest=response)
            if pisa_status.err:
                return HttpResponse('Ocurrió un error al generar el PDF', status=500)
            return response
    ```
    Y luego creamos la funcion que utilizara la instancia de la clase para crear y enviar el pdf por email
    ```py
    from django.core.mail import EmailMessage

    from .models import Sale

    def send(request , sale_id):
        venta = get_object_or_404(Sale, id=sale_id)

        pdf = DetalleDeVentaPdf.as_view()
        response = pdf(request, sale_id=sale_id)

        pdf_bytes = response.content
        email = EmailMessage(
            subject='Comprobante de pago',
            body=f'Adjuntamos el comprobante de pago del cliente {venta.client.client_name}',
            from_email="jcusiq@unsa.edu.pe",
            to=['comogeb679@brixozu.com']
        )
        email.attach(f'Venta_{venta.id}.pdf', pdf_bytes, 'application/pdf')
        email.send()
        return response
    ```
    una vez con los views realizados solo falta llamarlos mediante urls
    ```py
    from django.urls import path
    from .views import DetalleDeVentaPdf
    from . import views

    urlpatterns = [
        path('', views.index, name='index'),
        path('venta/<int:sale_id>/pdf/', DetalleDeVentaPdf.as_view(), name='venta_pdf'), 
        path('send/venta/<int:sale_id>/', views.send, name='enviar_correo') 
    ]
    ```
    y para tener acceso a estas urls y evitar tener que ingresar las urls manualmente, agregamos un boton a la tabla en la que se muestran las ventas
    ```html
    ...
    {% for venta in VentasHtml %}       
        <tr data-href="/venta/{{venta.id}}/pdf/" class="venta-click">
            <td>{{ venta.id }}</td>
            <td>{{ venta.date|date:"Y-m-d H:i" }}</td>
            <td>S/. {{ venta.total }}</td>
            <td><button onclick="window.location.href='send/venta/{{ venta.id }}/'"> <!--Redirige con una url dinamica-->
                    Enviar por Correo
                </button>
            </td>
        </tr>
    {% empty %}
    ...
    ```
    