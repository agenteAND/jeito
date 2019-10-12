from csv import DictWriter, QUOTE_NONNUMERIC
from collections import OrderedDict
from datetime import date, timedelta
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import F, Q, Sum
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.formats import date_format
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.detail import SingleObjectMixin
from django_filters.views import FilterView
from .filters import BalanceFilter, AccountFilter
from .forms import PurchaseForm, PurchaseFormSet
from .models import BankStatement, Transaction, Entry, TransferOrder, ThirdParty, Letter, PurchaseInvoice, Year


class UserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_becours


class YearMixin():
    def dispatch(self, request, year_pk, *args, **kwargs):
        self.year = get_object_or_404(Year, pk=year_pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['year'] = self.year
        return super().get_context_data(**kwargs)


class ProjectionView(UserMixin, YearMixin, ListView):
    template_name = "accounting/projection.html"

    def get_queryset(self):
        qs = Transaction.objects.filter(entry__year=self.year)
        qs = qs.filter(account__number__regex=r'^[67]')
        qs = qs.values('account_id', 'account__number', 'account__title', 'analytic__id', 'analytic__title')
        qs = qs.order_by('account__number', 'analytic__title')
        qs = qs.annotate(solde=Sum(F('revenue') - F('expense')))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)  # year
        context['solde'] = sum([account['solde'] for account in self.object_list])
        return context


class AnalyticBalanceView(UserMixin, YearMixin, FilterView):
    template_name = "accounting/analytic_balance.html"
    filterset_class = BalanceFilter

    def get_queryset(self):
        return Transaction.objects.filter(entry__year=self.year)

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['aggregate'] = 'analytic'
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = self.object_list
        context['revenues'] = sum([analytic['revenues'] for analytic in self.object_list])
        context['expenses'] = sum([analytic['expenses'] for analytic in self.object_list])
        context['balance'] = sum([analytic['balance'] for analytic in self.object_list])
        return context


class ThirdPartyBalanceView(UserMixin, YearMixin, FilterView):
    template_name = "accounting/thirdparty_balance.html"
    filterset_class = BalanceFilter

    def get_queryset(self):
        return Transaction.objects.filter(entry__year=self.year)

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['aggregate'] = 'thirdparty'
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = self.object_list
        context['revenues'] = sum([thirdparty['revenues'] for thirdparty in self.object_list])
        context['expenses'] = sum([thirdparty['expenses'] for thirdparty in self.object_list])
        context['balance'] = sum([thirdparty['balance'] for thirdparty in self.object_list])
        return context


class BalanceView(UserMixin, YearMixin, FilterView):
    template_name = "accounting/balance.html"
    filterset_class = BalanceFilter

    def get_queryset(self):
        return Transaction.objects.filter(entry__year=self.year)

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['aggregate'] = 'account'
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = self.object_list
        context['revenues'] = sum([account['revenues'] for account in self.object_list])
        context['expenses'] = sum([account['expenses'] for account in self.object_list])
        context['balance'] = sum([account['balance'] for account in self.object_list])
        return context


class AccountView(UserMixin, YearMixin, FilterView):
    template_name = "accounting/account.html"
    filterset_class = AccountFilter

    def get_queryset(self):
        return Transaction.objects.filter(entry__year=self.year).order_by('entry__date', 'pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solde = 0
        revenue = 0
        expense = 0
        for transaction in self.object_list:
            solde += transaction.revenue - transaction.expense
            transaction.solde = solde
            revenue += transaction.revenue
            expense += transaction.expense
        context['revenue'] = revenue
        context['expense'] = expense
        context['solde'] = solde
        return context

    def post(self, request):
        ids = [
            key[6:] for key, val in self.request.POST.items()
            if key.startswith('letter') and val == 'on'
        ]
        transactions = Transaction.objects.filter(id__in=ids)
        if transactions.filter(letter__isnull=False).exists():
            return HttpResponse("Certaines transactions sont déjà lettrées")
        if sum([transaction.balance for transaction in transactions]) != 0:
            return HttpResponse("Le lettrage n'est pas équilibré")
        if len(set([transaction.account_id for transaction in transactions])) > 1:
            return HttpResponse("Le lettrage doit concerner un seul compte général")
        if len(set([transaction.thirdparty_id for transaction in transactions])) > 1:
            return HttpResponse("Le lettrage doit concerner un seul tiers")
        if transactions:
            transactions.update(letter=Letter.objects.create())
        return HttpResponseRedirect(request.get_full_path())


class EntryListView(UserMixin, YearMixin, ListView):
    template_name = "accounting/entry_list.html"
    model = Entry

    def get_queryset(self):
        return Entry.objects.filter(year=self.year).order_by('date', 'pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        revenue = 0
        expense = 0
        balance = 0
        for entry in self.object_list:
            revenue += entry.revenue
            expense += entry.expense
            balance += entry.balance
        context['revenue'] = revenue
        context['expense'] = expense
        context['balance'] = balance
        return context


class BankStatementView(UserMixin, YearMixin, ListView):
    model = BankStatement
    template_name = "accounting/bankstatement_list.html"

    def get_queryset(self):
        return BankStatement.objects.filter(year=self.year)


class ReconciliationView(UserMixin, YearMixin, DetailView):
    template_name = 'accounting/reconciliation.html'
    model = BankStatement

    def get_queryset(self):
        return BankStatement.objects.filter(year=self.year)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            previous = BankStatement.objects.filter(date__lt=self.object.date).latest('date')
        except BankStatement.DoesNotExist:
            cond = Q()
        else:
            cond = Q(reconciliation__gt=previous.date)
        transactions = Transaction.objects.filter(account__number=5120000)
        cond = cond & Q(reconciliation__lte=self.object.date) | \
            Q(reconciliation=None, entry__date__lte=self.object.date)
        transactions = transactions.filter(cond)
        transactions = transactions.order_by('reconciliation', 'entry__date')
        context['transactions'] = transactions
        return context


class NextReconciliationView(UserMixin, YearMixin, ListView):
    template_name = 'accounting/next_reconciliation.html'

    def get_queryset(self):
        try:
            last = BankStatement.objects.latest('date')
        except BankStatement.DoesNotExist:
            cond = Q()
        else:
            cond = Q(reconciliation__gt=last.date)
        qs = Transaction.objects.filter(account__number=5120000)
        cond = cond & Q(reconciliation__lte=date.today()) | Q(reconciliation=None)
        qs = qs.filter(cond)
        qs = qs.order_by('reconciliation', 'entry__date')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = Transaction.objects.filter(account__number='5120000', reconciliation__lte=date.today())
        sums = transactions.aggregate(expense=Sum('expense'), revenue=Sum('revenue'))
        context['balance'] = sums['expense'] - sums['revenue']
        return context


class EntryView(UserMixin, YearMixin, DetailView):
    model = Entry

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions'] = self.object.transaction_set.order_by('account__number', 'analytic__title')
        return context


class CashFlowView(UserMixin, YearMixin, TemplateView):
    template_name = 'accounting/cash_flow.html'


class CashFlowJsonView(UserMixin, YearMixin, View):
    def serie(self, year):
        self.today = (settings.NOW() - timedelta(days=1)).date()
        start = year.start
        end = min(year.end, self.today)
        qs = Transaction.objects.filter(account__number__in=('5120000', '5300000'))
        qs = qs.filter(reconciliation__gte=start, reconciliation__lte=end)
        qs = qs.order_by('-reconciliation').values('reconciliation').annotate(balance=Sum('revenue') - Sum('expense'))
        qs = list(qs)
        data = OrderedDict()
        dates = [start + timedelta(days=n) for n in
                 range((end - start).days + 1)]
        balance = 0
        for d in dates:
            if qs and qs[-1]['reconciliation'] == d:
                balance += qs.pop()['balance']
            if d.month == 2 and d.day == 29:
                continue
            data[d] = -balance
        return data

    def get(self, request):
        reference = Year.objects.filter(start__lt=self.year.start).last()
        data = self.serie(self.year)
        ref_data = self.serie(reference)
        date_max = max(data.keys())
        ref_date_max = date_max + (reference.start - self.year.start)
        date1 = ref_date_max.strftime('%d/%m/%Y')
        date2 = date_max.strftime('%d/%m/%Y')
        nb1 = ref_data[ref_date_max]
        nb2 = data[date_max]
        diff = nb2 - nb1
        if nb1:
            percent = 100 * diff / nb1
            comment = """Au <strong>{}</strong> : <strong>{:+0.2f}</strong> €<br>
                         Au <strong>{}</strong> : <strong>{:+0.2f}</strong> €,
                         c'est-à-dire <strong>{:+0.2f}</strong> €
                         (<strong>{:+0.1f} %</strong>)
                      """.format(date1, nb1, date2, nb2, diff, percent)
        else:
            comment = """Au <strong>{}</strong> : <strong>{:+0.2f}</strong> €
                      """.format(date2, nb2)
        data = {
            'labels': [date_format(x, 'b') if x.day == 1 else '' for x in ref_data.keys()],
            'series': [
                list(ref_data.values()),
                list(data.values()),
            ],
            'comment': comment,
        }
        return JsonResponse(data)


class TransferOrderDownloadView(UserMixin, YearMixin, DetailView):
    model = TransferOrder

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(self.object.sepa(), content_type='application/xml')


class ThirdPartyCsvView(UserMixin, YearMixin, ListView):
    model = ThirdParty
    fields = ('number', 'title', 'type', 'account_number', 'iban', 'bic')

    def render_to_response(self, context):
        response = HttpResponse(content_type='text/csv; charset=cp1252')
        writer = DictWriter(response, self.fields, delimiter=';', quoting=QUOTE_NONNUMERIC)
        writer.writeheader()
        for obj in self.object_list:
            writer.writerow({field: getattr(obj, field) for field in self.fields})
        return response


class EntryCsvView(UserMixin, YearMixin, ListView):
    fields = (
        'journal_number', 'date_dmy', 'account_number', 'entry_id',
        'thirdparty_number', '__str__', 'expense', 'revenue'
    )

    def get_queryset(self):
        return Transaction.objects \
            .filter(entry__year=self.year, entry__exported=False) \
            .order_by('entry__id', 'id') \
            .select_related('entry', 'entry__journal', 'account', 'thirdparty')

    def render_to_response(self, context):
        response = HttpResponse(content_type='text/csv; charset=cp1252')
        writer = DictWriter(response, self.fields, delimiter=';', quoting=QUOTE_NONNUMERIC)
        writer.writeheader()

        def get_value(obj, field):
            value = getattr(obj, field)
            if callable(value):
                value = value()
            return value

        for obj in self.object_list:
            writer.writerow({field: get_value(obj, field) for field in self.fields})
        return response


class ChecksView(UserMixin, YearMixin, TemplateView):
    template_name = 'accounting/checks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = Transaction.objects.filter(entry__year=self.year)
        context['missing_analytic'] = transactions.filter(account__number__regex=r'^[67]', analytic__isnull=True)
        context['extraneous_analytic'] = transactions.filter(account__number__regex=r'^[^67]', analytic__isnull=False)
        letters = Letter.objects.annotate(balance=Sum('transaction__revenue') - Sum('transaction__expense'))
        context['unbalanced_letters'] = letters.exclude(balance=0)
        return context


class PurchaseListView(UserMixin, YearMixin, ListView):
    template_name = 'accounting/purchase_list.html'

    def get_queryset(self):
        return PurchaseInvoice.objects.filter(year=self.year).order_by('-date', '-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expense = 0
        for entry in self.object_list:
            expense += entry.expense
        context['expense'] = expense
        return context


class PurchaseDetailView(UserMixin, YearMixin, DetailView):
    template_name = 'accounting/purchase_detail.html'
    context_object_name = 'purchase'

    def get_queryset(self):
        return Entry.objects.filter(year=self.year, journal__number='HA')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['revenue'] = self.object.transaction_set.get(account__number='4010000')
        expenses = self.object.transaction_set.filter(account__number__startswith='6') \
            .order_by('account__number', 'analytic__title')
        context['expenses'] = expenses
        return context


class PurchaseCreateView(UserMixin, YearMixin, TemplateView):
    template_name = 'accounting/purchase_form.html'

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = PurchaseForm()
        if 'formset' not in kwargs:
            kwargs['formset'] = PurchaseFormSet()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = PurchaseForm(data=self.request.POST)
        formset = PurchaseFormSet(instance=form.instance, data=self.request.POST)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return HttpResponseRedirect(reverse_lazy('accounting:entry_list'))
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class PurchaseUpdateView(UserMixin, YearMixin, SingleObjectMixin, TemplateView):
    template_name = 'accounting/purchase_form.html'
    model = PurchaseInvoice

    def get_queryset(self):
        return PurchaseInvoice.objects.filter(year=self.year)

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = PurchaseForm(instance=self.object)
        if 'formset' not in kwargs:
            kwargs['formset'] = PurchaseFormSet(instance=self.object)
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PurchaseForm(instance=self.object, data=self.request.POST)
        formset = PurchaseFormSet(instance=self.object, data=self.request.POST)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return HttpResponseRedirect(reverse_lazy('accounting:entry_list'))
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))
