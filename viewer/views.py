from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.generic import TemplateView, FormView

from viewer.models import Trip, City, Airport
from viewer.forms import TripForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.contrib.auth.mixins import (
  LoginRequiredMixin, PermissionRequiredMixin
)


# @method_decorator(login_required(login_url='/login'), name='dispatch')
# class ProfileView(TemplateView):
#     template_name = 'profile.html'


class CustomLoginView(LoginView):
    template_name ='registration/login.html'

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"
    model = Trip

    def get_context_data(self, **kwargs):  # filter(self, request):
        template = 'index.html'
        trips = Trip.objects.filter(promoted=True)
        promoted_trips = []
        cards_block = []
        for i, trp in enumerate(trips):
            cards_block.append(trp)
            if (i + 1) % 3 == 0 or i == len(trips) - 1:
                promoted_trips.append(cards_block)
                cards_block = []

        context = {
            'promoted_trips': promoted_trips
        }
        return context  # render(request, template, context)

class TripDetailsView(TemplateView):
    template_name = "trip_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip_id = self.request.GET.get('trip')
        context['trip'] = Trip.objects.get(pk=trip_id)
        # context['reviews'] = ''  # Review.objects.filter(trip=trip_id)
        # context['percentage'] = Review.objects.get(pk=trip_id).rating * 10
        return context


class TripCreateView(FormView):
    template_name = 'form_trip.html'
    form_class = TripForm
    success_url = reverse_lazy('trip_add')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        Trip.objects.create(
            code=cleaned_data['code'],
            where_from=cleaned_data['where_from'],
            where_to=cleaned_data['where_to'],
            where_to_hotel=cleaned_data['where_to_hotel'],
            airport_depart=cleaned_data['airport_depart'],
            airport_arrive=cleaned_data['airport_arrive'],
            departure_date=cleaned_data['departure_date'],
            return_date=cleaned_data['return_date'],
            duration=cleaned_data['duration'],
            type=cleaned_data['type'],
            adult_price=cleaned_data['adult_price'],
            child_price=cleaned_data['child_price'],
            promoted=cleaned_data['promoted'],
            adult_places=cleaned_data['adult_places'],
            child_places=cleaned_data['child_places'],
        )
        return result

    # Redirect to url/trips when the user is not logged in
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return redirect('/trips')
    #     return super().dispatch(request, *args, **kwargs)
