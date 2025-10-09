from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_tareas, name='tareas_lista'),
    path('tarea/<int:tid>/', views.detalle_tarea, name='tareas_detalle'),
    path('agregar/', views.agregar_tarea, name='tareas_agregar'),
    path('eliminar/<int:tid>/', views.eliminar_tarea, name='tareas_eliminar'),
]