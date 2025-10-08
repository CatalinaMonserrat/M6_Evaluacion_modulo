from collections import defaultdict
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import TareaForm, RegistroForm

# Almacén en memoria
TASKS = defaultdict(list)  
_next_id = defaultdict(int)

def _new_id(user_id):
    _next_id[user_id] += 1
    return _next_id[user_id]

# ---- Auth ----
def login_view(request):
    if request.user.is_authenticated:
        return redirect('tareas_lista') 
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('tareas_lista')  
        messages.error(request, 'Credenciales incorrectas')
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('tareas_lista')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada. Inicia sesión')
            return redirect('login')
        else:
            messages.error(request, 'Revisa los errores del formulario.')
    else:
        form = RegistroForm()

    return render(request, 'auth/register.html', {'form': form})

# ---- Tareas ----
@login_required
def lista_tareas(request):
    user_tasks = TASKS[request.user.id]
    return render(request, 'tareas/lista.html', {'tareas': user_tasks})

@login_required
def detalle_tarea(request, tid: int):  
    tarea = _get_user_task_or_404(request.user.id, tid)
    return render(request, 'tareas/detalle.html', {'tarea': tarea})

@login_required
def agregar_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            t = {
                "id": _new_id(request.user.id), 
                "titulo": form.cleaned_data["titulo"],
                "descripcion": form.cleaned_data.get("descripcion", "")
            }
            TASKS[request.user.id].append(t)
            messages.success(request, '¡Tarea creada!')
            return redirect('tareas_lista')  
    else:
        form = TareaForm()
    return render(request, 'tareas/agregar.html', {'form': form})

@login_required
def eliminar_tarea(request, tid: int):  
    tarea = _get_user_task_or_404(request.user.id, tid)
    if request.method == 'POST':
        TASKS[request.user.id] = [t for t in TASKS[request.user.id] if t["id"] != tid]  # <- usa tid
        messages.success(request, 'Tarea eliminada')
        return redirect('tareas_lista')  # <- con "s"
    return render(request, 'tareas/eliminar.html', {'tarea': tarea})

# Helpers
def _get_user_task_or_404(user_id, tid: int):  
    for t in TASKS[user_id]:
        if t["id"] == tid:
            return t
    raise Http404("Tarea no encontrada")
