
# EcoShop — Entregable 1 (Base)

Proyecto Django 4 + SQLite3 con arquitectura MVT y login.

## Requisitos
- Python 3.13.x
- Crear y activar un virtualenv (opcional recomendado)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # cree un admin (is_staff)
python manage.py runserver
```

## Rutas principales
- `/` Inicio (usuario final)
- `/search/?q=...` Búsqueda de productos (Funcionalidad interesante #1)
- `/top-vendidos/` Top 3 productos más vendidos (Funcionalidad interesante #2)
- `/top-comentados/` Top 4 productos más comentados (Funcionalidad interesante #3)
- `/invoice/<order_id>/` Generar factura en PDF (o texto) (Funcionalidad interesante #4)
- `/core/dashboard/` Panel simple de admin (requiere usuario con `is_staff`)

## Datos de prueba
Ejecute el comando para cargar datos mínimos:
```bash
python manage.py loaddata demo.json
```
