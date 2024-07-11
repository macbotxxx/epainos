import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Sum
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from epainos.users.models import User, Contestant, ContestantImage, Transactions, ContestantVideo
from .forms import ContestantProfileForm, ContestantVote, ContestantEditProfileForm, FormatForm
from .tasks import sendSMS
from .filters import ContestantFilter, TransactionsFilter, ContestantFilter
from .admin import TransactionsResource, ContestantResource


def generate_random_10_digits():
    return "".join([str(random.randint(0, 9)) for _ in range(10)])

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()

class HomeIndex(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tranx_qs = Transactions.objects.all()
        contestant_qs = Contestant.objects.all().order_by("-number_of_vote")
        total_amount_paid = Transactions.objects.aggregate(total=Sum('amount_paid'))['total']
        total_vote = Contestant.objects.aggregate(total=Sum('number_of_vote'))['total']

        # Add additional context data if needed
        context["tranx_qs"] = tranx_qs[:10]
        context["tranx_qs_count"] = tranx_qs.count()
        context["contestant_qs"] = contestant_qs
        context["contestant_qs_count"] = contestant_qs.count()
        context["total_amount_paid"] = total_amount_paid
        context["total_vote"] = total_vote
        context["form"] = ContestantProfileForm()
        return context


home_index = HomeIndex.as_view()


class HomeContestantList(TemplateView):
    template_name = "pages/contestant_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tranx_qs = Transactions.objects.all()
        contestant_qs = Contestant.objects.all().order_by("-number_of_vote")
        total_amount_paid = Transactions.objects.aggregate(total=Sum('amount_paid'))['total']
        total_vote = Contestant.objects.aggregate(total=Sum('number_of_vote'))['total']

        # Add additional context data if needed
        context["tranx_qs"] = tranx_qs[:10]
        context["tranx_qs_count"] = tranx_qs.count()
        context["contestant_qs"] = contestant_qs
        context["contestant_qs_count"] = contestant_qs.count()
        context["total_amount_paid"] = total_amount_paid
        context["total_vote"] = total_vote
        context["form"] = ContestantProfileForm()
        return context


home_contestant_list = HomeContestantList.as_view()


class HomeContestantDetails(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tranx_qs = Transactions.objects.all()
        contestant_qs = Contestant.objects.all().order_by("-number_of_vote")
        total_amount_paid = Transactions.objects.aggregate(total=Sum('amount_paid'))['total']
        total_vote = Contestant.objects.aggregate(total=Sum('number_of_vote'))['total']

        # Add additional context data if needed
        context["tranx_qs"] = tranx_qs[:10]
        context["tranx_qs_count"] = tranx_qs.count()
        context["contestant_qs"] = contestant_qs
        context["contestant_qs_count"] = contestant_qs.count()
        context["total_amount_paid"] = total_amount_paid
        context["total_vote"] = total_vote
        context["form"] = ContestantProfileForm()
        return context


home_contestant_details = HomeContestantDetails.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        # for mypy to know that the user is authenticated
        assert self.request.user.is_authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()

class DashboardIndex(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tranx_qs = Transactions.objects.filter(settled=True)
        contestant_qs = Contestant.objects.all().order_by("-number_of_vote")
        total_amount_paid = Transactions.objects.filter(settled=True).aggregate(total=Sum('amount_paid'))['total']
        total_vote = Contestant.objects.aggregate(total=Sum('number_of_vote'))['total']

        # Add additional context data if needed
        context["tranx_qs"] = tranx_qs[:10]
        context["tranx_qs_count"] = tranx_qs.count()
        context["contestant_qs"] = contestant_qs
        context["contestant_qs_count"] = contestant_qs.count()
        context["total_amount_paid"] = total_amount_paid
        context["total_vote"] = total_vote
        context["form"] = ContestantProfileForm()
        return context


dashboard_index = DashboardIndex.as_view()


class ContestantUpload(LoginRequiredMixin ,TemplateView):
    template_name = "dashboard/contestant_upload.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contestant_qs"] = Contestant.objects.all()
        context["form"] = ContestantProfileForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContestantProfileForm(request.POST, request.FILES)
        files = request.FILES.getlist('contestant_image')
        if form.is_valid():
            contestant_qs = Contestant.objects.create(
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
                stage_name=form.cleaned_data.get("stage_name"),
                contestant_inspiration=form.cleaned_data.get("contestant_inspiration"),
                contestant_videos=form.cleaned_data.get("contestant_videos")
            )
            for f in files:
                image=ContestantImage.objects.create(image=f)
                contestant_qs.contestant_images.add(image)
            
            contestant_qs.save()
            return redirect('users:contestant_list')
        else:
            form = ContestantProfileForm()

        return self.get(request, *args, **kwargs)


contestant_upload = ContestantUpload.as_view()


class ContestantList(LoginRequiredMixin, ListView):
    model = Contestant
    template_name = "dashboard/contestant_list.html"
    context_object_name = "contestant_qs"
    form_class = FormatForm
    paginate_by = 100

    def get_queryset(self):
        queryset = Contestant.objects.all()
        self.filter = ContestantFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def post(self, request, *args, **kwargs):
        export_format = request.POST.get('format')

        dataset = ContestantResource().export()
        if export_format == "xls":
            exported_data = dataset.export('xls')
            content_type = 'application/vnd.ms-excel'
            filename = 'contestants.xls'
        elif export_format == "csv":
            exported_data = dataset.export('csv')
            content_type = 'text/csv'
            filename = 'contestants.csv'
        else:
            # Default to JSON if format is not specified or unknown
            exported_data = dataset.export('json')
            content_type = 'application/json'
            filename = 'contestants.json'

        response = HttpResponse(exported_data, content_type=content_type)
        response['Content-Disposition'] = f"attachment; filename={filename}"
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ContestantFilter()
        context['tranx_filter'] = self.filter
        context["form_export"] = FormatForm()
        context['count'] = self.filter.qs.count()  # Pass the filter object to the template
        return context


contestant_list = ContestantList.as_view()


class ContestantVoteList(LoginRequiredMixin, ListView):
    model = Contestant
    template_name = "dashboard/contestant_rank.html"
    context_object_name = "contestant_qs"
    # form_class = FormatForm
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tranx_qs = Transactions.objects.all()
        contestant_qs = Contestant.objects.all().order_by("-number_of_vote")
        # Add additional context data if needed
        context["tranx_qs"] = tranx_qs
        context["contestant_qs"] = contestant_qs
        return context


contestant_vote_list = ContestantVoteList.as_view()


class EditContestantProfileView(View):
    def get(self, request, pk):
        contestant = get_object_or_404(Contestant, pk=pk)
        form = ContestantEditProfileForm(instance=contestant)
        return render(request, 'dashboard/contestant_upload.html', {'form': form, 'contestant': contestant})

    def post(self, request, pk):
        contestant = get_object_or_404(Contestant, pk=pk)
        form = ContestantEditProfileForm(request.POST, request.FILES, instance=contestant)
        if form.is_valid():
            form.save()
            return redirect('users:contestant_list')  # Adjust the redirect URL as needed
        return render(request, 'dashboard/contestant_upload.html', {'form': form, 'contestant': contestant})
    

update_contestant_profile = EditContestantProfileView.as_view()


class ContestantDeleteView(LoginRequiredMixin, DeleteView):
    model = Contestant
    template_name = "dashboard/delete_warning.html"
    success_url = reverse_lazy("users:contestant_list")

    def get_queryset(self):
        # Filter Contestant objects based on the authenticated user
        return Contestant.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data if needed
        context["title"] = "Delete Contestant Record"
        context["button_content"] = "Yes, Delete The Following Account"
        context["card_header"] = "Are you sure! you want to delete the following Contestant record "
        return context


delete_contestant_record = ContestantDeleteView.as_view()


class ContestantDetailsView(DetailView):
    model = Contestant
    template_name = "pages/contestant_details.html"
    context_object_name = "contestant_qs"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contestant_id_value = self.object.pk
        # Add additional context data if needed
        context["more_contestant"] = Contestant.objects.all().order_by('-created_date')[:10]
        context["vote_form"] = ContestantVote(initial={'contestant_id': contestant_id_value})
        return context


contestant_view = ContestantDetailsView.as_view()


class TransactionList(LoginRequiredMixin, ListView, FormView):
    model = Transactions
    template_name = "dashboard/transactions.html"
    context_object_name = "tranx_qs"
    form_class = FormatForm
    paginate_by = 100

    def get_queryset(self):
        queryset = Transactions.objects.all()
        self.filter = TransactionsFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def post(self, request, *args, **kwargs):
        export_format = request.POST.get('format')

        dataset = TransactionsResource().export()
        if export_format == "xls":
            exported_data = dataset.export('xls')
            content_type = 'application/vnd.ms-excel'
            filename = 'transactions.xls'
        elif export_format == "csv":
            exported_data = dataset.export('csv')
            content_type = 'text/csv'
            filename = 'transactions.csv'
        else:
            # Default to JSON if format is not specified or unknown
            exported_data = dataset.export('json')
            content_type = 'application/json'
            filename = 'transactions.json'

        response = HttpResponse(exported_data, content_type=content_type)
        response['Content-Disposition'] = f"attachment; filename={filename}"
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TransactionsFilter()
        context['tranx_filter'] = self.filter
        context["form_export"] = FormatForm()
        context['count'] = self.filter.qs.count()  # Pass the filter object to the template
        return context


transaction_list = TransactionList.as_view()


class Vote(TemplateView):
    template_name = "pages/upload.html"

    def post(self, request, *args, **kwargs):
        form = ContestantVote(request.POST, request.FILES)
        ref = generate_random_10_digits()
        if form.is_valid():
            full_name=form.cleaned_data.get("full_name")
            email=form.cleaned_data.get("email")
            phone_number=form.cleaned_data.get("phone_number")
            vote_number=form.cleaned_data.get("number_of_vote")
            contestant_id=form.cleaned_data.get("contestant_id")
            number_of_vote=int(vote_number) * 100

            contestant_qs = Contestant.objects.get(id=contestant_id)

            Transactions.objects.create(
                contestant=contestant_qs,
                amount_paid=number_of_vote,
                payment_ref=f"EPAINOS_REF_{ref}",
                voter_name=full_name,
                voter_email=email,
                voter_phone_number=phone_number
            )
            
            # Return JSON response with validated inputs
            return JsonResponse({
                'success': True,
                'full_name': full_name,
                'email': email,
                'phone_number': phone_number,
                'number_of_vote': number_of_vote,
                'tx_ref': f"EPAINOS_REF_{ref}"
            })

        # Return JSON response indicating failure
        return JsonResponse({'success': False})


vote_submit = Vote.as_view()


class Payment(TemplateView):
    template_name = "pages/vote_payment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contestant_qs"] = Contestant.objects.all()
        context["form"] = ContestantProfileForm()
        return context


payment = Payment.as_view()


class PaymentVerify(TemplateView):
    template_name = "pages/verify.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = self.request.GET.get('status')
        tx_ref = self.request.GET.get('tx_ref')
        transaction_id = self.request.GET.get('transaction_id')

        trans_qs = Transactions.objects.get(
            payment_ref=tx_ref
        )
        trans_qs.settled=True
        trans_qs.status=status
        trans_qs.save()
        vote_count = trans_qs.amount_paid / 100
        # add the vote to the contestant account
        contestant_qs = Contestant.objects.get(id=trans_qs.contestant_id)
        contestant_qs.number_of_vote += int(vote_count)
        contestant_qs.save()
        # send sms
        voter_number = trans_qs.voter_phone_number
        sendSMS.delay(phone_number=voter_number)


        context["contestant_qs"] = Contestant.objects.all()
        context["form"] = ContestantProfileForm()
        return context


payment_verify = PaymentVerify.as_view()


class PolicyPage(TemplateView):
    template_name = "pages/policy.html"


policy_page = PolicyPage.as_view()

