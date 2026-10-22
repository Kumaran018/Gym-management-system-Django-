from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from apps.authentication.decorators import role_required
from apps.members.models import Member
from .models import Payment
from .forms import PaymentForm
import datetime

@login_required
def record_payment(request):
    user = request.user
    if request.method == 'POST':
        if user.role == 'member':
            member = user.member_profile
            amount = request.POST.get('amount')
            method = request.POST.get('payment_method', 'upi')
            active_mem = member.memberships.filter(status='active').first()
            payment = Payment.objects.create(
                member=member,
                membership=active_mem,
                amount=amount,
                payment_method=method,
                payment_status='paid'
            )
            messages.success(request, f"Payment of ₹{payment.amount} completed successfully! Invoice: {payment.invoice_number}")
            return redirect('payments:payment_history')
        else:
            form = PaymentForm(request.POST)
            if form.is_valid():
                payment = form.save()
                messages.success(request, f"Payment recorded successfully! Invoice generated: {payment.invoice_number}")
                return redirect('payments:payment_history')
    else:
        # Pre-populate member if passed in GET params
        member_id = request.GET.get('member_id')
        initial_data = {}
        if member_id:
            member = Member.objects.filter(pk=member_id).first()
            if member:
                initial_data['member'] = member
                active_mem = member.memberships.filter(status='active').first()
                if active_mem:
                    initial_data['membership'] = active_mem
                    initial_data['amount'] = active_mem.paid_price
        form = PaymentForm(initial=initial_data)
        
    return render(request, 'payments/record.html', {'form': form})

@login_required
def payment_history(request):
    user = request.user
    if user.role == 'member':
        # Strictly show only this particular member's payment transactions
        payments = Payment.objects.filter(member__user=user).select_related('member__user').order_by('-payment_date')
    elif user.role == 'trainer':
        payments = Payment.objects.filter(member__assigned_trainer__user=user).select_related('member__user').order_by('-payment_date')
    else:
        payments = Payment.objects.all().select_related('member__user').order_by('-payment_date')
    
    # Search filter
    search_query = request.GET.get('search', '').strip()
    if search_query:
        payments = payments.filter(
            invoice_number__icontains=search_query) | payments.filter(
            member__user__first_name__icontains=search_query) | payments.filter(
            member__user__last_name__icontains=search_query)

    context = {
        'payments': payments,
        'search_query': search_query,
    }
    return render(request, 'payments/history.html', context)

@login_required
def generate_receipt(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    # Security: members can only view their own receipts
    if request.user.role == 'member' and payment.member.user != request.user:
        messages.error(request, "Access denied: Unauthorized receipt view.")
        return redirect('dashboard:member_home')
        
    return render(request, 'payments/receipt.html', {'payment': payment})

@login_required
@role_required(['admin'])
def monthly_revenue(request):
    today = datetime.date.today()
    this_year = today.year
    
    # Group payments by month for this year
    monthly_data = []
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    for i in range(1, 13):
        total = Payment.objects.filter(
            payment_date__year=this_year,
            payment_date__month=i,
            payment_status='paid'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        monthly_data.append({
            'month': months[i-1],
            'revenue': float(total)
        })

    # Calculations
    total_revenue_ytd = Payment.objects.filter(
        payment_date__year=this_year,
        payment_status='paid'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    pending_revenue = Payment.objects.filter(
        payment_status='pending'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'monthly_data': monthly_data,
        'total_revenue_ytd': total_revenue_ytd,
        'pending_revenue': pending_revenue,
        'year': this_year,
    }
    return render(request, 'payments/revenue.html', context)
