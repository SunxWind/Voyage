from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import (
  LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
)

from django.views.generic import TemplateView, FormView, ListView, UpdateView, DeleteView

from viewer.models import Trip, PurchasedTrip, City, Hotel, Airport
from viewer.forms import TripForm, TripPurchaseForm, SignUpForm

from weatherbit.api import Api
from Voyage.keys import pyweatherbit_key
from viewer.forcast_mock import forcast_mock


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        """Returns the error message if a user tries to get into company stuff section"""
        return JsonResponse({'message': 'Error: Only company staff have access to this page'})


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")

        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')

        return super().dispatch(request, *args, **kwargs)


def logout_page(request):
    """Custom logged out view funciton"""
    return render(request, 'registration/loggedout.html')


def purchase_approval(request):
    """The view function for the page approving a trip purchase"""
    return render(request, 'purchase_approval.html')


def trip_create_approval(request):
    """The view function for the page approving a new trip creation"""
    return render(request, 'trip_create_approval.html')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'


# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"
    model = Trip

    def get_context_data(self, **kwargs):
        promoted_trips = Trip.objects.filter(promoted=True,
                                             departure_date__gt=(datetime.now().date()+timedelta(days=3)))

        # Selecting 3 destinations countries from promoted trips
        max_count = min(len(promoted_trips), 3)
        countries_trips = promoted_trips[0:max_count]

        # Filtering trips within 30 days from todays date
        # Number of days can be changed in timedelda in the following line
        upcoming_cutoff_date = datetime.now().date() + timedelta(days=30)
        upcoming_trips = Trip.objects.filter(departure_date__lte=upcoming_cutoff_date,
                                             departure_date__gt=(datetime.now().date()) + timedelta(
                                                 days=3)).order_by('departure_date')

        recently_purchased_trips = PurchasedTrip.objects.order_by('-id')[:5]

        context = {
            'promoted_trips': promoted_trips,
            'countries_trips': countries_trips,
            'upcoming_trips': upcoming_trips,
            'recently_purchased_trips': recently_purchased_trips,
        }

        return context


class TripView(ListView):
    template_name = 'trips.html'
    model = Trip

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)


class TripDetailsView(TemplateView):
    template_name = "trip_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip_id = self.request.GET.get('trip')
        trip = Trip.objects.get(pk=trip_id)

        context['trip'] = trip
        context['service_standard'] = Trip.STANDARD_CHOICES[trip.service_standard]
        context['hotel'] = trip.where_to_hotel

        """
        Integrating weather API.
        Only 1500 requests per day to this API is free of charge.
        In order to make the forcast API working set mode = 'API',
        otherwise with mode = 'mockup' an unreal mockup forcast will be shown.
        The maximum forcast duration is 16 days.
        """

        FORCAST_DURATION = 16

        context['forcast'] = self.weather_forcast(country=str(trip.where_to.country.name),
                                                  city=str(trip.where_to.name),
                                                  days=FORCAST_DURATION,
                                                  tp='daily',
                                                  mode='mockup')

        return context

    def weather_forcast(self, country, city, days, tp, mode='API'):
        """
        Gets data for weather forcast from pyweatherbit API or from a mockup
        :param country:
        :param city:
        :param days: duration of the forcast in days (max 16 days)
        :param tp: type of the forcast (daily, hourly, etc.)
        :param mode: 'API' - get data from API, mockup - get data from an unreal mockup (see viewer.forcast_mock)
        :return: list of dictionaries; each dictionary corresponds to data (temperature, wind, etc.)
                for one day/hour etc.
        """

        forcast = []
        if mode == 'API':
            # Authorization to the API with a personal or company key
            api = Api(pyweatherbit_key)
            try:
                # Gets data from the API
                forcast = api.get_forecast(country=country,
                                           city=city,
                                           days=days,
                                           tp=tp).get()

                # Formats the dates to dd/mm and weekday
                for date in forcast:
                    date['week_day'] = date['datetime'].strftime('%A')[0:3]
                    date['date_smpl'] = date['datetime'].strftime('%d/%m')

            # If API.get request is failed returns ValueError and None for forcast data
            except ValueError:
                forcast = None

        elif mode == "mockup":
            # Gets data from a mockup
            forcast = forcast_mock
            for date in forcast:
                date['week_day'] = date['datetime'].strftime('%A')[0:3]
                date['date_smpl'] = date['datetime'].strftime('%d/%m')

        return forcast


class TripCreateView(StaffRequiredMixin, FormView):
    template_name = 'form_trip.html'
    form_class = TripForm
    success_url = reverse_lazy('trip_create_approval')
    permission_required = 'viewer.create_trip'

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
            service_standard=cleaned_data['service_standard'],
            adult_price=cleaned_data['adult_price'],
            child_price=cleaned_data['child_price'],
            promoted=cleaned_data['promoted'],
            adult_places=cleaned_data['adult_places'],
            child_places=cleaned_data['child_places'],
            description=cleaned_data['description'],
            short_description=cleaned_data['short_description'],
            image=cleaned_data['image'],
            image_small=cleaned_data['image_small'],
        )

        return result

    def form_invalid(self, form):
        result = super().form_invalid(form)
        for field in form.errors:
            if field != '__all__':
                # Adds an alert-danger (highlighting) format to a field where wrong data were provided
                form[field].field.widget.attrs['class'] += ' alert-danger'

        return result

    # Redirects to url/trips when the user is not logged in
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('trips')

        return super().dispatch(request, *args, **kwargs)


class TripUpdateView(StaffRequiredMixin, UpdateView):
    template_name = 'form_trip.html'
    form_class = TripForm
    model = Trip
    success_url = reverse_lazy('trips')

    def form_valid(self, form):
        form.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('trips')

        return super().dispatch(request, *args, **kwargs)


class TripDeleteView(StaffRequiredMixin, DeleteView):
    template_name = 'trip_delete_form.html'
    model = Trip
    success_url = reverse_lazy('trips')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/trips')

        return super().dispatch(request, *args, **kwargs)


class PurchasedTripsView(ListView):
    template_name = 'purchased_trips.html'
    model = PurchasedTrip

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)


class TripPurchaseView(LoginRequiredMixin, FormView):
    template_name = "form_trip_purchase.html"
    form_class = TripPurchaseForm
    success_url = reverse_lazy('purchase_approval')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip_id = self.request.GET.get('trip')
        trip = Trip.objects.get(pk=trip_id)
        context['trip'] = trip
        context['adult_price'] = trip.adult_price
        context['child_price'] = trip.child_price

        return context

    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        trip_id = self.request.GET.get('trip')
        trip = Trip.objects.get(pk=trip_id)

        if (trip.adult_places >= form.cleaned_data['amount_adult'] and
           trip.child_places >= form.cleaned_data['amount_child']):

            # Places an order if there are enough places in the proposed trip
            PurchasedTrip.objects.create(
                trip=trip,
                firstname=cleaned_data['firstname'],
                lastname=cleaned_data['lastname'],
                birth_date=cleaned_data['birth_date'],
                email=cleaned_data['email'],
                phone_number=cleaned_data['phone_number'],
                amount_adult=cleaned_data['amount_adult'],
                amount_child=cleaned_data['amount_child'],
                total_price=cleaned_data['total_price']
            )

            # Reduces the number of available places in the trip proposal
            trip.adult_places -= cleaned_data['amount_adult']
            trip.child_places -= cleaned_data['amount_child']
            trip.save()
        else:
            # Raises errors if the amount of available places is less than those provided by the client in the form
            if trip.adult_places < form.cleaned_data['amount_adult']:
                if trip.adult_places > 0:
                    error_msg = (f'The amount of places currently available for adults is {trip.adult_places}. '
                                 f'Input equal or greater number, please.')
                else:
                    error_msg = f'Unfortunately, no places are currently available for adults.'
                form.add_error('amount_adult', error_msg)

                return self.form_invalid(form)

            if trip.child_places < form.cleaned_data['amount_child']:
                if trip.child_places > 0:
                    error_msg = (f'The amount of places currently available for children is {trip.child_places}. '
                                 f'Input equal or greater number, please.')
                else:
                    error_msg = f'Unfortunately, no places are currently available for children.'
                form.add_error('amount_child', error_msg)

                return self.form_invalid(form)

        return result

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        for field in form.errors:
            if field != '__all__':
                # Adds an alert-danger (highlighting) format to a field where wrong data were provided
                form[field].field.widget.attrs['class'] += ' alert-danger'

        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('purchase_approval')

        return super().dispatch(request, *args, **kwargs)


class PurchasedTripUpdateView(StaffRequiredMixin, UpdateView):
    template_name = 'form_trip_purchase.html'
    form_class = TripPurchaseForm
    model = PurchasedTrip
    success_url = reverse_lazy('purchased_trips')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Gets context data for calculation of the total trip price
        context['trip'] = context['object'].trip
        context['adult_price'] = context['object'].trip.adult_price
        context['child_price'] = context['object'].trip.child_price

        return context

    def form_valid(self, form):
        form.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)

        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)


class PurchasedTripDeleteView(StaffRequiredMixin, DeleteView):
    template_name = 'purchased_trip_delete_form.html'
    model = PurchasedTrip
    success_url = reverse_lazy('purchased_trips')

    def form_valid(self, form):
        messages.error(self.request, form.errors)

        purchased_trip_id = self.kwargs.get('pk')
        purchased_trip = PurchasedTrip.objects.get(pk=purchased_trip_id)

        trip = purchased_trip.trip
        # Increases the number of available places in the trip proposal after deletion of an ordered trip
        trip.adult_places += purchased_trip.amount_adult
        trip.child_places += purchased_trip.amount_child
        trip.save()

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('/purchased_trips')

        return super().dispatch(request, *args, **kwargs)


class CountriesListView(TemplateView):
    template_name = 'countries_list.html'

    def get_context_data(self, **kwargs):
        """Looking through the database for all the countries which the available trips pointing to"""

        all_trips = Trip.objects.filter()
        countries_list = []
        for trip in all_trips:
            countries_list.append(trip.where_to.country.name)

        countries_set = set(countries_list)
        countries_list = sorted(list(countries_set))

        context = {
            'countries_list': countries_list
        }
        return context


class SearchResultsView(TemplateView):
    template_name = 'filtered_trips.html'

    def get_context_data(self, *args, **kwargs):
        """
        Grabbing all relevant parameters from URL.
        Filtering trips based on the parameters.
        """

        trips = Trip.objects.filter(departure_date__gte=(datetime.now().date() + timedelta(days=3)))

        continent = self.request.GET.get('s_continent', '')
        country = self.request.GET.get('s_country', '')
        city = self.request.GET.get('s_city', '')
        hotel = self.request.GET.get('s_hotel', '')
        sort = self.request.GET.get('sort', '')
        standard = self.request.GET.get('standard', '')
        adults = self.request.GET.get('adults', '')
        children = self.request.GET.get('children', '')

        if continent:
            trips = trips.filter(where_to_id__continent=continent)

        if country:
            trips = trips.filter(where_to__country__name=country)

        if city:
            trips = trips.filter(where_to__name=city)

        if hotel:
            trips = trips.filter(where_to_hotel__name__icontains=hotel)

        if sort == 'price':
            trips = trips.order_by('adult_price')

        elif sort == 'date':
            trips = trips.order_by('departure_date')

        if standard:
            trips = trips.filter(service_standard=standard)

        if adults:
            trips = trips.filter(adult_places__gte=adults)

        if children:
            trips = trips.filter(child_places__gte=children)

        filtered_trips = trips
        context = {'filtered_trips': filtered_trips}

        return context
