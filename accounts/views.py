from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from .models import Account
from .forms import AccountForm, LoginForm
import random
import hashlib

# Function to hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register new user
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.account_number = random.randint(10000, 99999)
            account.password = hash_password(account.password)
            account.save()
            messages.success(request, f"Account created successfully! Your account number is {account.account_number}.")
            return redirect('login')
    else:
        form = AccountForm()

    return render(request, 'accounts/create_account.html', {'form': form})

# Login functionality
def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            account = authenticate(request, username=username, password=password)

            if account is not None:
                auth_login(request, account)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

# User dashboard
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    account = request.user
    if request.method == 'POST':
        if 'deposit' in request.POST:
            amount = float(request.POST.get('deposit'))
            if amount > 0:
                account.balance += amount
                account.save()
                messages.success(request, f"Deposited R{amount}")
            else:
                messages.error(request, "Invalid deposit amount")

        elif 'withdraw' in request.POST:
            amount = float(request.POST.get('withdraw'))
            if amount > 0 and account.balance >= amount:
                account.balance -= amount
                account.save()
                messages.success(request, f"Withdrawn R{amount}")
            else:
                messages.error(request, "Insufficient funds or invalid amount")

        elif 'transfer' in request.POST:
            recipient_account_number = int(request.POST.get('transfer_to'))
            amount = float(request.POST.get('transfer_amount'))
            if amount > 0 and account.balance >= amount:
                try:
                    recipient_account = Account.objects.get(account_number=recipient_account_number)
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    messages.success(request, f"Transferred R{amount} to account {recipient_account_number}")
                except Account.DoesNotExist:
                    messages.error(request, f"Account {recipient_account_number} not found")
            else:
                messages.error(request, "Insufficient funds or invalid amount")

    return render(request, 'accounts/dashboard.html', {'account': account})
