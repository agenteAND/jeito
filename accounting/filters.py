from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.conf import settings
from django.http import QueryDict
import django_filters
from .models import Analytic, Account, ThirdParty, Transaction, Entry, BankStatement


class BaseFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'id': 'filter'}
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field_with_label.html'
        self.helper.form_method = 'get'


class BankStatementFilterForm(BaseFilterForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            'year',
        )


class BankStatementFilter(django_filters.FilterSet):
    year = django_filters.ChoiceFilter(label="Exercice", field_name='date', lookup_expr='year',
                                       choices=[(i, i) for i in range(settings.NOW().year + 1, 2015, -1)])

    class Meta:
        model = BankStatement
        fields = ('year', )
        form = BankStatementFilterForm

    def __init__(self, data, *args, **kwargs):
        if data is None:
            data = QueryDict('year={}'.format(settings.NOW().year))
        super().__init__(data, *args, **kwargs)


class BudgetFilterForm(BaseFilterForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            'year',
        )


class BudgetFilter(django_filters.FilterSet):
    year = django_filters.ChoiceFilter(label="Exercice", field_name='entry__date', lookup_expr='year',
                                       choices=[(i, i) for i in range(settings.NOW().year + 1, 2015, -1)])

    class Meta:
        model = Transaction
        fields = ('year', )
        form = BudgetFilterForm

    def __init__(self, data, *args, **kwargs):
        if data is None:
            data = QueryDict('year={}'.format(settings.NOW().year))
        super().__init__(data, *args, **kwargs)


class BalanceFilterForm(BaseFilterForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            'year', 'projected'
        )


class BalanceFilter(django_filters.FilterSet):
    year = django_filters.ChoiceFilter(label="Exercice", choices=[(i, i) for i in range(settings.NOW().year, 2015, -1)],
                                       field_name='entry__date', lookup_expr='year')
    projected = django_filters.BooleanFilter(label="Projeté", field_name='entry__projected')

    class Meta:
        model = Transaction
        fields = ('year', 'projected')
        form = BalanceFilterForm

    def __init__(self, data, *args, **kwargs):
        if data is None:
            data = QueryDict('year={}'.format(settings.NOW().year))
        super().__init__(data, *args, **kwargs)


class YearAccountFilterForm(BaseFilterForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            'year',
            'account',
            'thirdparty',
            'analytic',
            'projected',
        )


class AccountFilter(django_filters.FilterSet):
    year = django_filters.ChoiceFilter(label="Exercice", choices=[(i, i) for i in range(settings.NOW().year, 2015, -1)],
                                       field_name='entry__date', lookup_expr='year')
    account = django_filters.ModelChoiceFilter(label="Compte", queryset=Account.objects)
    thirdparty = django_filters.ModelChoiceFilter(label="Tiers", queryset=ThirdParty.objects)
    analytic = django_filters.ModelChoiceFilter(label="Compte analytique", queryset=Analytic.objects)
    projected = django_filters.BooleanFilter(label="Projeté", field_name='entry__projected')

    class Meta:
        model = Transaction
        fields = ('year', 'account', 'thirdparty', 'analytic', 'projected')
        form = YearAccountFilterForm

    @property
    def qs(self):
        qs = super().qs.order_by('entry__date')
        qs = qs.select_related('entry', 'account', 'thirdparty', 'analytic')
        return qs

    def __init__(self, data, *args, **kwargs):
        if data is None:
            data = QueryDict('year={}'.format(settings.NOW().year))
        super().__init__(data, *args, **kwargs)


class EntryFilterForm(BaseFilterForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            'year', 'projected'
        )


class EntryFilter(django_filters.FilterSet):
    year = django_filters.ChoiceFilter(label="Exercice", choices=[(i, i) for i in range(settings.NOW().year, 2015, -1)],
                                       field_name='date', lookup_expr='year')
    projected = django_filters.BooleanFilter(label="Projeté", field_name='projected')

    class Meta:
        model = Entry
        fields = ('year', 'projected')
        form = EntryFilterForm

    @property
    def qs(self):
        qs = super().qs.order_by('date')
        return qs

    def __init__(self, data, *args, **kwargs):
        if data is None:
            data = QueryDict('year={}'.format(settings.NOW().year))
        super().__init__(data, *args, **kwargs)
