from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from activities.forms import CoffeeLogForm, GrinderSettingForm
from activities.models import CoffeeLog, GrinderSetting, BREW_METHODS
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q, Avg, Count, Max, Min, F
from django.db.models.functions import ExtractHour, ExtractMonth, TruncDate
from django.http import JsonResponse

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.method == 'POST':
        coffee_log_form = CoffeeLogForm(request.POST, user=request.user)
        if coffee_log_form.is_valid():
            log = coffee_log_form.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, "Coffee logged successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        coffee_log_form = CoffeeLogForm(user=request.user)
    
    # Get user's grinders for quick access
    user_grinders = GrinderSetting.objects.filter(user=request.user)
    
    return render(request, 'users/profile.html', { 
        'coffee_log_form': coffee_log_form,
        'user_grinders': user_grinders,
    })

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'users/home.html')

@login_required
def log_coffee(request):
    if request.method == 'POST':
        form = CoffeeLogForm(request.POST, user=request.user)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, "Coffee logged successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CoffeeLogForm(user=request.user)
    return render(request, 'users/log_coffee.html', {'form': form})

@login_required
def manage_grinders(request):
    """View for managing user's coffee grinders"""
    user_grinders = GrinderSetting.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = GrinderSettingForm(request.POST)
        if form.is_valid():
            grinder = form.save(commit=False)
            grinder.user = request.user
            grinder.save()
            messages.success(request, "Grinder added successfully!")
            return redirect('manage_grinders')
    else:
        form = GrinderSettingForm()
        
    return render(request, 'users/manage_grinders.html', {
        'form': form,
        'user_grinders': user_grinders
    })

@login_required
def edit_grinder(request, pk):
    """View for editing an existing grinder"""
    grinder = get_object_or_404(GrinderSetting, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = GrinderSettingForm(request.POST, instance=grinder)
        if form.is_valid():
            form.save()
            messages.success(request, "Grinder updated successfully!")
            return redirect('manage_grinders')
    else:
        form = GrinderSettingForm(instance=grinder)
        
    return render(request, 'users/edit_grinder.html', {
        'form': form,
        'grinder': grinder
    })

@login_required
def delete_grinder(request, pk):
    """View for deleting a grinder"""
    grinder = get_object_or_404(GrinderSetting, pk=pk, user=request.user)
    
    if request.method == 'POST':
        grinder.delete()
        messages.success(request, "Grinder deleted successfully!")
        return redirect('manage_grinders')
        
    return render(request, 'users/delete_grinder.html', {'grinder': grinder})

@login_required
def coffee_history(request):
    """Enhanced view for coffee history with analytics"""
    # Get filters from request
    brew_method = request.GET.get('brew_method', '')
    search_query = request.GET.get('q', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    rating_min = request.GET.get('rating_min', '')
    
    # Base queryset
    coffee_logs = CoffeeLog.objects.filter(user=request.user)
    
    # Apply filters
    if brew_method:
        coffee_logs = coffee_logs.filter(brew_method=brew_method)
    
    if search_query:
        coffee_logs = coffee_logs.filter(
            Q(coffee_name__icontains=search_query) | 
            Q(notes__icontains=search_query)
        )
    
    if date_from:
        coffee_logs = coffee_logs.filter(timestamp__gte=date_from)
    
    if date_to:
        coffee_logs = coffee_logs.filter(timestamp__lte=date_to)
    
    if rating_min:
        coffee_logs = coffee_logs.filter(rating__gte=rating_min)
    
    # Order the filtered results
    coffee_logs = coffee_logs.order_by('-timestamp')
    
    # Basic analytics data
    analytics = {}
    
    if coffee_logs.exists():
        # Top rated coffees
        top_coffees = coffee_logs.values('coffee_name').annotate(
            avg_rating=Avg('rating'),
            count=Count('id')
        ).filter(count__gte=2).order_by('-avg_rating')[:5]
        
        # Most used brew methods
        brew_methods_count = coffee_logs.values('brew_method').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Average rating by brew method
        rating_by_method = coffee_logs.values('brew_method').annotate(
            avg_rating=Avg('rating'),
            count=Count('id')
        ).order_by('brew_method')
        
        # Best grind size for each brew method (for methods with multiple entries)
        best_grinds = coffee_logs.exclude(grind_size__isnull=True).values('brew_method').annotate(
            best_grind=Avg('grind_size'),
            avg_rating=Avg('rating')
        ).filter(avg_rating__gte=4).order_by('brew_method')
        
        # Water to bean ratio stats
        ratio_stats = coffee_logs.exclude(
            Q(water_amount_ml__isnull=True) | Q(bean_grams__isnull=True)
        ).aggregate(
            avg_ratio=Avg(F('water_amount_ml') / F('bean_grams')),
            min_ratio=Min(F('water_amount_ml') / F('bean_grams')),
            max_ratio=Max(F('water_amount_ml') / F('bean_grams'))
        )
        
        analytics = {
            'top_coffees': top_coffees,
            'brew_methods_count': brew_methods_count,
            'rating_by_method': rating_by_method,
            'best_grinds': best_grinds,
            'ratio_stats': ratio_stats,
            'brew_methods': BREW_METHODS,
            'total_logs': coffee_logs.count(),
            'avg_rating': coffee_logs.aggregate(Avg('rating'))['rating__avg']
        }
    
    context = {
        'coffee_logs': coffee_logs,
        'search_query': search_query,
        'brew_method_filter': brew_method,
        'date_from': date_from,
        'date_to': date_to,
        'rating_min': rating_min,
        'brew_methods': BREW_METHODS,
        'analytics': analytics
    }
    
    return render(request, 'users/history.html', context)

@login_required
def get_analytics_data(request):
    """API endpoint to get analytics data for charts"""
    chart_type = request.GET.get('chart_type', '')
    brew_method = request.GET.get('brew_method', '')
    
    logs = CoffeeLog.objects.filter(user=request.user)
    if brew_method:
        logs = logs.filter(brew_method=brew_method)
    
    data = {}
    
    if chart_type == 'ratings_over_time':
        # Group logs by day and get average rating
        data = list(logs.annotate(
            date=TruncDate('timestamp')
        ).values('date').annotate(
            avg_rating=Avg('rating')
        ).order_by('date').values('date', 'avg_rating'))
        
    elif chart_type == 'grind_vs_rating':
        # Correlation between grind size and rating
        data = list(logs.exclude(grind_size__isnull=True).values(
            'grind_size', 'rating', 'brew_method'
        ))
        
    elif chart_type == 'ratio_vs_rating':
        # Correlation between water-to-bean ratio and rating
        data = []
        for log in logs.exclude(Q(water_amount_ml__isnull=True) | Q(bean_grams__isnull=True)):
            if log.brew_ratio:
                data.append({
                    'brew_ratio': log.brew_ratio,
                    'rating': log.rating,
                    'brew_method': log.get_brew_method_display()
                })
    
    return JsonResponse({'data': data})