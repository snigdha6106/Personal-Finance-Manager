from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from twilio.rest import Client
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from .forms import CategoryForm 
from .models import Category
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import TransactionForm
from .models import Transaction
from django.contrib.auth import logout as auth_logout
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
TWILIO_ACCOUNT_SID = 'ACf114eafc0c3743d3fd77da27a279c625'
TWILIO_AUTH_TOKEN = '92623fc9f57ff4e8a4f5241f0eeb3f69'
TWILIO_PHONE_NUMBER = '+14438430872'  # Replace with your Twilio number
def home(request):
    return render(request, 'login.html')
def signup(request):
    return render(request, 'signup.html')
def dashboard(request):
    return render(request, 'dashboard.html')
def categories(request):
    return render(request, 'categories.html')
def budgets(request):
    return render(request, 'budgets.html')
def reports(request):
    return render(request, 'reports.html')
def logout(request):
    return redirect('/')
def settings(request):
    return render(request, 'settings.html')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  
            return redirect('settings')  
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})
def save_settings(request):
    if request.method == 'POST':
        sms_enabled = request.POST.get('sms_enabled') == 'on'  # Checkbox value
        user_phone = request.POST.get('phone')  # User's phone number
        budget_reminder = request.POST.get('budget_reminder')  # Budget reminder bar value
        if sms_enabled:
            message_body = f"Your budget reminder has been set to {budget_reminder}%. View your budget tracking report here: http://127.0.0.1:8000/generate_report/"
            try:
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                client.messages.create(
                    to=user_phone,
                    from_=TWILIO_PHONE_NUMBER,
                    body=message_body,
                )
                return JsonResponse({"success": True, "message": "SMS notification sent successfully!"})
            except Exception as e:
                return JsonResponse({"success": False, "error": str(e)})
        return JsonResponse({"success": True, "message": "Settings saved without SMS notification."})
    return redirect('settings')  # Redirect to settings page if not POST
def generate_report(request):
    if request.method == "POST":
        report_type = request.POST.get('report-type')
        track_category = request.POST.get('category-tracking')
        start_date = request.POST.get('report-start-date')
        end_date = request.POST.get('report-end-date')
        if report_type == 'income-expense':
            dates = ['2024-11-05', '2024-11-07', '2024-11-10', '2024-11-12', '2024-11-15']
            income = [1000, 1200, 1500, 1300, 1100]  # Example income values
            expense = [500, 300, 450, 700, 650]  # Example expense values
            title = "Income vs Expense"
            ylabel = "Amount ($)"
            x = range(len(dates))  # For creating positions for the bars
            width = 0.4  # Bar width
            plt.figure(figsize=(10, 6))
            plt.bar(x, income, width=width, label='Income', color='green', alpha=0.7)
            plt.bar([p + width for p in x], expense, width=width, label='Expense', color='red', alpha=0.7)
            plt.title(f"{title} Report ({start_date} to {end_date})")
            plt.xlabel("Dates")
            plt.ylabel(ylabel)
            plt.xticks([p + width / 2 for p in x], dates, rotation=45)
            plt.legend()
            plt.tight_layout()
        elif report_type == 'budget-tracking':
            categories = ['Food', 'Transport', 'Entertainment', 'Health', 'Others']
            amounts = [1000, 800, 500, 200, 300]  # Example budget values by category
            title = "Budget Tracking by Category"
            ylabel = "Budget ($)"
            plt.figure(figsize=(6, 6))
            plt.pie(amounts, labels=categories, autopct='%1.1f%%', colors=['purple', 'blue', 'green', 'red', 'orange'], startangle=140)
            plt.title(f"{title} ({start_date} to {end_date})")
            plt.tight_layout()
        elif report_type == 'investment-growth':
            dates = ['2024-11-05', '2024-11-07', '2024-11-10', '2024-11-12', '2024-11-15']
            values = [5000, 5200, 5400, 5500, 5700]  # Example investment growth values
            title = "Investment Growth"
            ylabel = "Value ($)"
            plt.figure(figsize=(10, 6))
            plt.plot(dates, values, marker='o', label=title, color='blue', linestyle='-', linewidth=2, markersize=8)
            plt.title(f"{title} Report ({start_date} to {end_date})")
            plt.xlabel("Dates")
            plt.ylabel(ylabel)
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
        else:
            return HttpResponse("Invalid Report Type")
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        return render(request, 'report_generated.html', {
            'report_type': title,
            'start_date': start_date,
            'end_date': end_date,
            'image_base64': image_base64
        })
    return HttpResponse("Invalid Request")
def add_category(request):
    if request.method == 'POST':
        predefined_category = request.POST.get('predefined-categories')
        custom_category = request.POST.get('custom-category-name') if request.POST.get('add-custom-category') == 'yes' else None
        category_type = request.POST.get('category-type')
        new_category = Category(
            name=custom_category if custom_category else predefined_category,
            category_type=category_type,
        )
        new_category.save()
        return redirect('categories')  # Redirect to categories list page
    return render(request, 'categories.html')  # Your template
def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        category_type = request.POST.get('category_type')
        category.name = name
        category.category_type = category_type
        category.save()
        return redirect('categories')
    return render(request, 'edit_category.html', {'category': category})
def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('categories') 
def change_password(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to change your password.")
            return redirect('login')        
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('settings')
        user = request.user
        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect('settings')
        user.set_password(new_password)
        user.save()
        messages.success(request, "Your password has been changed successfully.")
        return redirect('settings')
    return render(request, 'change_password.html')
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new transaction
            return redirect('transactions') 
    else:
        form = TransactionForm()
    return render(request, 'add_transaction.html', {'form': form})
def transactions(request):
    transactions = Transaction.objects.all()  # Get all transactions
    return render(request, 'transactions.html', {'transactions': transactions})
def delete_transaction(request, id):
    if request.method == "POST":
        transaction = get_object_or_404(Transaction, id=id)
        transaction.delete()
        return redirect('transactions')  # Redirect to the transactions page
def logout(request):
    return redirect('logout_confirm')
def logout_confirm(request):
    if request.method == 'POST':
        if request.POST.get('confirm') == 'yes':
            # Log the user out
            auth_logout(request)
            return redirect('/')  # Redirect to homepage after logout
    return render(request, 'logout_confirm.html')

