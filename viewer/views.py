from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse

from django.views.generic import TemplateView, FormView, ListView, UpdateView, DeleteView

from viewer.models import Trip, PurchasedTrip, City, Hotel, Airport
from viewer.forms import TripForm, TripPurchaseForm, SignUpForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.contrib.auth.mixins import (
  LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
)


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return JsonResponse(
            {'message': 'Only company staff have access to this page'}
        )


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
    return render(request, 'registration/loggedout.html')


def purchase_approval(request):
    return render(request, 'purchase_approval.html')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'


# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"
    model = Trip

    def get_context_data(self, **kwargs):
        trips = Trip.objects.filter(promoted=True)
        promoted_trips = []
        cards_block = []
        for i, trp in enumerate(trips):
            cards_block.append(trp)
            if (i + 1) % 3 == 0 or i == len(trips) - 1:
                promoted_trips.append(cards_block)
                cards_block = []

        three_trips = promoted_trips[slice(1)]

        context = {
            'promoted_trips': promoted_trips,
            'three_trips': three_trips
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
        context['trip_type'] = Trip.TYPE_CHOICES[trip.type]
        context['hotel'] = trip.where_to_hotel
        return context


class TripCreateView(StaffRequiredMixin, FormView):
    template_name = 'form_trip.html'
    form_class = TripForm
    success_url = reverse_lazy('trip_add')
    permission_required = 'viewer.create_trip'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        print("You are in the TripCreateView form_valid method")
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
                form[field].field.widget.attrs['class'] += ' alert-danger'
        return result

    # Redirect to url/trips when the user is not logged in
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
    success_url = reverse_lazy('index')

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
            trip.adult_places -= cleaned_data['amount_adult']
            trip.child_places -= cleaned_data['amount_child']
            trip.save()
        else:
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

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('/purchased_trips')
        return super().dispatch(request, *args, **kwargs)


class ContinentView(TemplateView):
    template_name = 'filtered_trips.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        continent = self.request.GET.get('continent')
        context['continent'] = continent

        if continent == "All":
            filtered_trips = Trip.objects.filter()
        else:
            filtered_trips = Trip.objects.filter(where_to_id__continent=continent)

        context = {
            'filtered_trips': filtered_trips
        }

        return context


class CountriesListView(TemplateView):
    template_name = 'countries_list.html'

    def get_context_data(self, **kwargs):
        all_trips = Trip.objects.filter()
        countries_list = []
        for trip in all_trips:
            countries_list.append(trip.where_to.country.name)

        countries_set = set(countries_list)
        countries_list = sorted(list(countries_set))

        print(countries_list)
        context = {
            'countries_list': countries_list
        }

        return context


class CountryTripsView(TemplateView):
    template_name = 'filtered_trips.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        country = self.request.GET.get('country')
        context['country'] = country

        filtered_trips = Trip.objects.filter(where_to_id__country__name=country)
        context = {
            'filtered_trips': filtered_trips
        }

        return context

