from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Event, EventRegistration
from .forms import EventForm
from notifications.utils import send_bulk_notification
from users.models import User

def event_list(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    search_query = request.GET.get('search', '')
    event_type = request.GET.get('type', '')
    
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if event_type:
        events = events.filter(event_type=event_type)
    
    paginator = Paginator(events, 9)  # Show 9 events per page
    page = request.GET.get('page')
    events = paginator.get_page(page)
    
    return render(request, 'events/event_list.html', {
        'events': events,
        'search_query': search_query,
        'event_type': event_type,
    })

@login_required
def event_create(request):
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to create events.")
        return redirect('event_list')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            
            # Notify all users about new event
            users = User.objects.filter(is_active=True)
            send_bulk_notification(
                recipients=users,
                notification_type='event',
                title=f'New Event: {event.title}',
                message=f'New event scheduled: {event.title} on {event.date}',
                related_object=event
            )
            
            messages.success(request, 'Event created successfully!')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    
    return render(request, 'events/event_form.html', {'form': form})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    user_registered = False
    registration_status = None
    
    if request.user.is_authenticated:
        try:
            registration = EventRegistration.objects.get(event=event, user=request.user)
            user_registered = True
            registration_status = registration.status
        except EventRegistration.DoesNotExist:
            pass
    
    return render(request, 'events/event_detail.html', {
        'event': event,
        'user_registered': user_registered,
        'registration_status': registration_status,
    })

@login_required
def event_register(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if event.is_past_event:
        messages.error(request, 'This event has already taken place.')
        return redirect('event_detail', pk=pk)
    
    if not event.is_registration_open:
        messages.error(request, 'Registration is closed for this event.')
        return redirect('event_detail', pk=pk)
    
    if EventRegistration.objects.filter(event=event, user=request.user).exists():
        messages.warning(request, 'You are already registered for this event.')
        return redirect('event_detail', pk=pk)
    
    status = 'registered' if event.available_spots > 0 else 'waitlisted'
    EventRegistration.objects.create(
        event=event,
        user=request.user,
        status=status
    )
    
    messages.success(request, 
        'Successfully registered for the event!' if status == 'registered' 
        else 'Added to the waitlist.'
    )
    return redirect('event_detail', pk=pk)

@login_required
def event_unregister(request, pk):
    event = get_object_or_404(Event, pk=pk)
    registration = get_object_or_404(EventRegistration, event=event, user=request.user)
    
    if event.is_past_event:
        messages.error(request, 'Cannot unregister from a past event.')
        return redirect('event_detail', pk=pk)
    
    registration.delete()
    messages.success(request, 'Successfully unregistered from the event.')
    
    # If there was a waitlist, move the first person up
    waitlisted = EventRegistration.objects.filter(
        event=event, 
        status='waitlisted'
    ).order_by('registration_date').first()
    
    if waitlisted:
        waitlisted.status = 'registered'
        waitlisted.save()
    
    return redirect('event_detail', pk=pk)

@login_required
def my_events(request):
    registered_events = Event.objects.filter(
        eventregistration__user=request.user
    ).order_by('date')
    
    created_events = Event.objects.filter(
        created_by=request.user
    ).order_by('date')
    
    return render(request, 'events/my_events.html', {
        'registered_events': registered_events,
        'created_events': created_events,
    })

@login_required
def event_participants(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if not request.user.is_staff and request.user != event.created_by:
        messages.error(request, "You don't have permission to view participants.")
        return redirect('event_detail', pk=pk)
    
    registrations = EventRegistration.objects.filter(event=event).order_by('registration_date')
    
    return render(request, 'events/event_participants.html', {
        'event': event,
        'registrations': registrations,
    })

@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if not request.user.is_staff and request.user != event.created_by:
        messages.error(request, "You don't have permission to edit this event.")
        return redirect('event_detail', pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_detail', pk=pk)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/event_form.html', {
        'form': form,
        'action': 'Edit',
        'event': event,
    })

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if not request.user.is_staff and request.user != event.created_by:
        messages.error(request, "You don't have permission to delete this event.")
        return redirect('event_detail', pk=pk)
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('event_list')
    
    return render(request, 'events/event_confirm_delete.html', {'event': event})

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to update events.")
        return redirect('event_detail', pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save()
            
            # Notify registered participants about event updates
            registered_users = event.participants.all()
            send_bulk_notification(
                recipients=registered_users,
                notification_type='event',
                title=f'Event Updated: {event.title}',
                message=f'The event "{event.title}" has been updated. Please check the details.',
                related_object=event
            )
            
            messages.success(request, 'Event updated successfully!')
            return redirect('event_detail', pk=pk)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/event_form.html', {'form': form, 'event': event})
