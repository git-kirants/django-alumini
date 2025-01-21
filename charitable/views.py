from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .models import Fund, Donation, ScholarshipApplication
from .forms import FundForm, DonationForm, ScholarshipApplicationForm, ScholarshipReviewForm

def fund_list(request):
    funds = Fund.objects.all().order_by('-created_at')
    return render(request, 'charitable/fund_list.html', {'funds': funds})

@login_required
@user_passes_test(lambda u: u.is_staff)
def fund_create(request):
    if request.method == 'POST':
        form = FundForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fund created successfully!')
            return redirect('fund_list')
    else:
        form = FundForm()
    return render(request, 'charitable/fund_form.html', {'form': form, 'action': 'Create'})

@login_required
def make_donation(request, fund_id):
    fund = get_object_or_404(Fund, id=fund_id)
    
    # Check if fund is already closed
    if not fund.is_active:
        messages.warning(request, 'This fund is no longer accepting donations.')
        return redirect('fund_detail', fund_id=fund.id)
    
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.fund = fund
            donation.donor = request.user
            
            # Check if donation would exceed target amount
            new_total = fund.current_amount + donation.amount
            if new_total > fund.target_amount:
                messages.warning(request, f'This donation would exceed the fund\'s target amount. Maximum donation allowed: ${fund.target_amount - fund.current_amount:.2f}')
                return render(request, 'charitable/donation_form.html', {'form': form, 'fund': fund})
            
            donation.save()
            
            # Update fund amount and check if target is reached
            fund.current_amount = new_total
            if fund.current_amount >= fund.target_amount:
                fund.is_active = False
                messages.success(request, 'Thank you! Your donation has helped reach the fund\'s target amount!')
            else:
                messages.success(request, 'Thank you for your donation!')
            
            fund.save()
            return redirect('fund_detail', fund_id=fund.id)
    else:
        form = DonationForm()
    
    return render(request, 'charitable/donation_form.html', {
        'form': form,
        'fund': fund,
    })

@login_required
def my_donations(request):
    donations = Donation.objects.filter(donor=request.user).order_by('-donation_date')
    total_donated = donations.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'charitable/my_donations.html', {
        'donations': donations,
        'total_donated': total_donated
    })

@login_required
def apply_scholarship(request, fund_id):
    fund = get_object_or_404(Fund, pk=fund_id)
    if request.method == 'POST':
        form = ScholarshipApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.fund = fund
            application.save()
            messages.success(request, 'Scholarship application submitted successfully!')
            return redirect('my_scholarship_applications')
    else:
        form = ScholarshipApplicationForm()
    return render(request, 'charitable/scholarship_application_form.html', {
        'form': form,
        'fund': fund
    })

@login_required
def my_applications(request):
    applications = ScholarshipApplication.objects.filter(
        student=request.user
    ).order_by('-applied_date')
    return render(request, 'charitable/my_applications.html', {'applications': applications})

@login_required
@user_passes_test(lambda u: u.is_staff)
def review_applications(request):
    applications = ScholarshipApplication.objects.filter(
        status='pending'
    ).order_by('applied_date')
    return render(request, 'charitable/review_applications.html', {'applications': applications})

@login_required
@user_passes_test(lambda u: u.is_staff)
def review_application(request, application_id):
    application = get_object_or_404(ScholarshipApplication, pk=application_id)
    if request.method == 'POST':
        form = ScholarshipReviewForm(request.POST, instance=application)
        if form.is_valid():
            application = form.save(commit=False)
            application.reviewed_by = request.user
            application.reviewed_date = timezone.now()
            application.save()
            messages.success(request, 'Application review completed!')
            return redirect('review_applications')
    else:
        form = ScholarshipReviewForm(instance=application)
    return render(request, 'charitable/review_application.html', {
        'form': form,
        'application': application
    })

def fund_detail(request, fund_id):
    fund = get_object_or_404(Fund, id=fund_id)
    context = {
        'fund': fund,
        'total_donations': fund.donations.count(),
        'recent_donations': fund.donations.filter(is_anonymous=False).order_by('-donation_date')[:5],
        'applications_count': fund.applications.count() if request.user.is_staff else None,
    }
    return render(request, 'charitable/fund_detail.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def fund_edit(request, fund_id):
    fund = get_object_or_404(Fund, pk=fund_id)
    if request.method == 'POST':
        form = FundForm(request.POST, instance=fund)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fund updated successfully!')
            return redirect('fund_detail', fund_id=fund.id)
    else:
        form = FundForm(instance=fund)
    return render(request, 'charitable/fund_form.html', {
        'form': form, 
        'action': 'Edit',
        'fund': fund
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def fund_toggle_status(request, fund_id):
    fund = get_object_or_404(Fund, pk=fund_id)
    fund.is_active = not fund.is_active
    fund.save()
    status = "activated" if fund.is_active else "deactivated"
    messages.success(request, f'Fund {status} successfully!')
    return redirect('fund_detail', fund_id=fund.id)

@login_required
@user_passes_test(lambda u: u.is_staff)
def fund_delete(request, fund_id):
    fund = get_object_or_404(Fund, pk=fund_id)
    if request.method == 'POST':
        fund.delete()
        messages.success(request, 'Fund deleted successfully!')
        return redirect('fund_list')
    return render(request, 'charitable/fund_delete.html', {'fund': fund})
