from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import UserProfile,QueueEntry
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
def user_login(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user=User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'queue_manager/login.html')

def register(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = email
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')
        department = request.POST.get('department')
        phone = request.POST.get('phone')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Email already registered")
            return redirect('register')
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        print("User created:", user.username)

        profile = UserProfile.objects.create(
            user=user,
            role=role,  # e.g., "Staff Member" → "staff"
            department=department,
            phone=phone
        )

        messages.success(request, "Account created successfully!")
        return redirect('login')

    else:
        return render(request, 'queue_manager/register.html')

@login_required(login_url='login')
def dashboard(request):
    user = request.user  # This is the built-in User
    user_profile = user.userprofile

    waiting=QueueEntry.objects.filter(status='waiting').count()
    progress=QueueEntry.objects.filter(status='in-progress').count()
    completed=QueueEntry.objects.filter(status='completed').count()
    context = {
        'user': user_profile,
        'waiting': waiting,
        'progress': progress,
        'completed': completed,
    }
    
    return render(request, 'queue_manager/dashboard.html', context)

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def generate_token(request):
    if request.method == "POST":
        name = request.POST.get("customer_name")
        service = request.POST.get("service_type")
        
        last_entry = QueueEntry.objects.order_by('-id').first()
        if last_entry :
            last_token = int(last_entry.token_number[1:])
            new_token = f"T{last_token + 1:03d}"
        else :
            new_token="T001"

        QueueEntry.objects.create(
            customer_name=name,
            service_type=service,
            token_number=new_token,
            added_by=request.user
        )
        return redirect('dashboard')  # or any success page

    return redirect('dashboard')

@login_required(login_url='login')
def queue_stats_api(request):
    waiting = QueueEntry.objects.filter(status='waiting' , added_by=request.user)
    in_progress = QueueEntry.objects.filter(status='in-progress', added_by=request.user)  # ✅ FIXED
    completed = QueueEntry.objects.filter(status='completed', added_by=request.user)

    data = {
        "waiting": waiting.count(),
        "in_progress": in_progress.count(),
        "completed": completed.count(),
        "total": waiting.count() + in_progress.count() + completed.count(),
        "waiting_entries": list(waiting.values("id","token_number", "customer_name", "service_type")),
        "in_progress_entries": list(in_progress.values("id", "token_number", "customer_name", "service_type")),  # ✅ add this
        "completed_entries": list(completed.values("id", "token_number", "customer_name", "service_type")),  # ✅ Add this line

    }
    return JsonResponse(data)


@csrf_exempt
@login_required(login_url='login')
def start_service(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            entry_id = data.get('entry_id')

            queue_entry = QueueEntry.objects.get(id=entry_id)
            queue_entry.status = 'in-progress'
            queue_entry.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        
@csrf_exempt
@login_required(login_url='login')
def complete_service(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            entry_id = data.get('entry_id')

            queue_entry = QueueEntry.objects.get(id=entry_id)
            queue_entry.status = 'completed'
            queue_entry.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


def display(request):
    waiting_entries = QueueEntry.objects.filter(status='waiting').order_by('-timestamp')
    in_progress_entries = QueueEntry.objects.filter(status='in-progress').order_by('-timestamp')
    completed_entries = QueueEntry.objects.filter(status='completed').order_by('-completed_at')[:10]  # Recent 10

    data = {
        "waiting_entries": waiting_entries,
        "in_progress_entries": in_progress_entries,
        "completed_entries": completed_entries,
    }
    return render(request, "queue_manager/display.html", data)


