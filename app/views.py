from django.shortcuts import render, redirect
from .models import Customer,Transaction

# REGISTER
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        pin = request.POST['upi_pin']

        if Customer.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        Customer.objects.create(username=username, password=password, upi_pin=pin)
        return redirect('login')

    return render(request, 'register.html')


# LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            customer = Customer.objects.get(username=username, password=password)
            return redirect('dashboard', username=customer.username)
        except Customer.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# DASHBOARD
def dashboard(request, username):
    customer = Customer.objects.get(username=username)
    transactions = Transaction.objects.filter(customer=customer).order_by('-date')

    return render(request, 'dashboard.html', {
        'customer': customer,
        'transactions': transactions
    })


# DEPOSIT
def deposit(request, username):
    customer = Customer.objects.get(username=username)

    if request.method == "POST":
        amount = float(request.POST['amount'])
        customer.balance += amount
        customer.save()

        Transaction.objects.create(customer=customer, t_type="DEPOSIT", amount=amount)
        return redirect('dashboard', username=username)

    return render(request, 'deposit.html', {'username': username})


# WITHDRAW
def withdraw(request, username):
    customer = Customer.objects.get(username=username)

    if request.method == "POST":
        amount = float(request.POST['amount'])
        pin = int(request.POST['upi_pin'])

        if pin != customer.upi_pin:
            return render(request, 'withdraw.html', {'error': 'Wrong PIN', 'username': username})

        if customer.balance >= amount:
            customer.balance -= amount
            customer.save()

            Transaction.objects.create(customer=customer, t_type="WITHDRAW", amount=amount)
            return redirect('dashboard', username=username)
        else:
            return render(request, 'withdraw.html', {'error': 'Insufficient Balance', 'username': username})

    return render(request, 'withdraw.html', {'username': username})


# CHANGE PIN
def change_pin(request, username):
    customer = Customer.objects.get(username=username)

    if request.method == "POST":
        old_pin = int(request.POST['old_pin'])
        new_pin = int(request.POST['new_pin'])

        if old_pin == customer.upi_pin:
            customer.upi_pin = new_pin
            customer.save()
            return redirect('dashboard', username=username)
        else:
            return render(request, 'change_pin.html', {'error': 'Wrong Old PIN', 'username': username})

    return render(request, 'change_pin.html', {'username': username})