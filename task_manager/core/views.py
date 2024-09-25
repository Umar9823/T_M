from django.shortcuts import render, redirect
from .models import *
from django.db.models import Avg
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
matplotlib.use('Agg')


def add_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        role_id = request.POST['role']
        department_id = request.POST['department']

        User.objects.create(
            name=name,
            role_id=role_id,
            department_id=department_id
        )
        return redirect('dashboard')

    roles = Role.objects.all()
    departments = Department.objects.all()
    return render(request, 'add_user.html', {'roles': roles, 'departments': departments})


def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        assigned_to_id = request.POST['assigned_to']
        approved_by_id = request.POST['approved_by']  # Change variable name for clarity
        deadline = request.POST['deadline']

        # Get the User instance for assigned_to and approved_by
        assigned_to = User.objects.get(id=assigned_to_id)
        approved_by = User.objects.get(id=approved_by_id)

        # Create the Task instance
        Task.objects.create(
            title=title,
            description=description,
            assigned_to=assigned_to,  # Assign the User instance
            approved_by=approved_by,  # Assign the User instance
            deadline=deadline
        )
        return redirect('dashboard')  # Redirect to the dashboard after successful creation

    # Get all users for the dropdown options
    users = User.objects.all()
    return render(request, 'add_task.html', {'users': users})


def dashboard(request):
    tasks = Task.objects.all()
    task_data = []
    for task in tasks:
        task_data.append({
            'title': task.title,
            'assigned_to': task.assigned_to.name,
            'created_at': task.created_at,
            'completed_at': task.completed_at,
            'deadline': task.deadline,
        })
    
    # Generate performance metrics for users
    user_performance = {}
    for task in tasks:
        user_name = task.assigned_to.name
        if user_name not in user_performance:
            user_performance[user_name] = {'total_tasks': 0, 'completed_tasks': 0}
        user_performance[user_name]['total_tasks'] += 1
        if task.completed_at:
            user_performance[user_name]['completed_tasks'] += 1
    
    completion_rates = {user: (data['completed_tasks'] / data['total_tasks'] * 100 if data['total_tasks'] > 0 else 0)
                        for user, data in user_performance.items()}
    
    # Create line graph
    plt.figure()
    plt.plot(list(completion_rates.keys()), list(completion_rates.values()))
    plt.title('User Task Completion Rates (%)')
    plt.xlabel('Users')
    plt.ylabel('Completion Rate (%)')
    
    # Save to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    
    return render(request, 'dashboard.html', {
        'tasks': task_data,
        'chart': img_base64,
        'user_performance': user_performance
    })

def report(request):
    user_metrics = {}
    tasks = Task.objects.all()

    for task in tasks:
        user_name = task.assigned_to.name
        if user_name not in user_metrics:
            user_metrics[user_name] = {'on_time': 0, 'late': 0, 'not_completed': 0}

        if task.completed_at:
            if task.is_completed_on_time:
                user_metrics[user_name]['on_time'] += 1
            else:
                user_metrics[user_name]['late'] += 1
        else:
            user_metrics[user_name]['not_completed'] += 1

    return render(request, 'report.html', {'user_metrics': user_metrics})

def user_tasks(request):
    users = User.objects.all()
    user_tasks = None
    selected_user = None

    if request.method == 'POST':
        selected_user = request.POST.get('selected_user')
        if selected_user:
            user_tasks = Task.objects.filter(assigned_to_id=selected_user)

    return render(request, 'user_tasks.html', {
        'users': users,
        'user_tasks': user_tasks,
        'selected_user': User.objects.get(id=selected_user) if selected_user else None
    })