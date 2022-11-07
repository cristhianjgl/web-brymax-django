
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from .form import TaskForm, PredictionForm
from .models import Prediction, Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# para la api
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json

# para el modelo de datos de machine
import joblib
from numpy import asarray


# Create your views here.
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        print('enviando formulario')
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if (request.POST['password1'] == request.POST['password2']):
            try:
                # register user
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
                # return HttpResponse('User created successfully')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password do not match'
        })


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })


@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {
        'tasks': tasks
    })


@login_required
def create_task(request):
    if (request.method == 'GET'):
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            print(new_task)
            return redirect('tasks')
        except ValueError:
            return render(request, 'signin.html', {
                'form': TaskForm,
                'error': 'Please valida data'
            })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'error updating task'
            })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password incorrect'
            })
        else:
            login(request, user)
            return redirect('home')

def prediction(request):
    if (request.method == 'GET'):
        return render(request, 'prediction.html', {
            'form': PredictionForm
        })
    else:
        try:
            # clf = joblib.load('./model-ml/modelo_entrenado_xgboost.pkl')
            # # print('clf', clf)
            # # row = [6,148,72,35,0,33.6,0.627,50] #1
            # # row = [1, 89, 66, 23, 94, 28.1, 0.167, 21] #0
            # # print('embarazosn ', request.POST['numero_embarazos'])
            row = [
                int(request.POST['numero_embarazos']),
                float(request.POST['glucuosa']),
                float(request.POST['presion_arterial']),
                float(request.POST['espesor_piel']),
                float(request.POST['insulina']),
                float(request.POST['indice_masa_corporal']),
                float(request.POST['funcion_pedigree_diabetes']),
                int(request.POST['edad'])
            ]
            resultPre =  getPredictionByModel(row)
            
            # new_data = asarray([row])
            # prueba = clf.predict(new_data)
            
            # # clf=joblib.load('./model-ml/modelo_entrenado.pkl')
            # # prueba = clf.predict([[6,148,72,35,0,33.6,0.627,50]])
            # # #prueba = clf.predict([[1,89,66,23,94,28.1,0.167,21]])
            # # print(prueba)

            # resultPre = prueba[0]
            # # print("🚀 ~ file: views.py ~ line 185 ~ resultPre", resultPre)

            form = PredictionForm(request.POST)
            new_prediction = form.save(commit=False)
            new_prediction.user = request.user
            new_prediction.resultado = float(resultPre)
            new_prediction.save()
            print(new_prediction)

            return render(request, 'prediction.html', {
                'resultPre': resultPre,
                'form': PredictionForm
            })
        except ValueError:
            return render(request, 'prediction.html', {
                'form': PredictionForm,
                'error': 'An Error Occurred, Please try again'
            })

def getPredictionByModel(row):
    try:
        clf = joblib.load('./model-ml/modelo_entrenado_xgboost.pkl')
        # print('clf', clf)
        # row = [6,148,72,35,0,33.6,0.627,50] #1
        # row = [1, 89, 66, 23, 94, 28.1, 0.167, 21] #0
        # print('embarazosn ', request.POST['numero_embarazos'])
        # row = [
        #     int(request.POST['numero_embarazos']),
        #     float(request.POST['glucuosa']),
        #     float(request.POST['presion_arterial']),
        #     float(request.POST['espesor_piel']),
        #     float(request.POST['insulina']),
        #     float(request.POST['indice_masa_corporal']),
        #     float(request.POST['funcion_pedigree_diabetes']),
        #     int(request.POST['edad'])
        # ]
        # print("🚀 ~ file: views.py ~ line 165 ~ row", row)
        new_data = asarray([row])
        prueba = clf.predict(new_data)
        
        # clf=joblib.load('./model-ml/modelo_entrenado.pkl')
        # prueba = clf.predict([[6,148,72,35,0,33.6,0.627,50]])
        # #prueba = clf.predict([[1,89,66,23,94,28.1,0.167,21]])
        # print(prueba)

        resultPre = prueba[0]
        return resultPre
    except:
        return 0

class PredictionView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    
    def get(self,request):
        predictions = list(Prediction.objects.values())
        if len(predictions)>0:
            datos={'message':"Success",'predictions':predictions}
        else:
            datos={'message':"Predictions Not Found...",'predictions':predictions}

        return JsonResponse(datos)


    def post(self,request):
        # print(request.body)
        jd = json.loads(request.body)
        print(jd)

        row = [
            int(jd['numero_embarazos']),
            float(jd['glucuosa']),
            float(jd['presion_arterial']),
            float(jd['espesor_piel']),
            float(jd['insulina']),
            float(jd['indice_masa_corporal']),
            float(jd['funcion_pedigree_diabetes']),
            int(jd['edad'])
        ]
        resultPre =  getPredictionByModel(row)
        Prediction.objects.create(
            nombres = jd['nombres'],
            apellidos = jd['apellidos'],
            numero_documento = jd['numero_documento'],
            numero_embarazos = int(jd['numero_embarazos']),
            glucuosa = float(jd['glucuosa']),
            presion_arterial = float(jd['presion_arterial']),
            espesor_piel = float(jd['espesor_piel']),
            insulina = float(jd['insulina']),
            indice_masa_corporal = float(jd['indice_masa_corporal']),
            funcion_pedigree_diabetes = float(jd['funcion_pedigree_diabetes']),
            edad = int(jd['edad']),
            resultado = float(resultPre),
            user_id = int(jd['user_id'])
        )
        print("🚀 ~ file: views.py ~ line 283 ~ resultPre", float(resultPre))
        datos={'message':"Success",'resultPrediction': float(resultPre)}
        print("🚀 ~ file: views.py ~ line 286 ~ datos", datos)
        return JsonResponse(datos)
        

