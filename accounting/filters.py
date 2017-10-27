from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.conf import settings
from django.http import QueryDict
import django_filters
from .models import Analytic, Account, Transaction


class YearFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field_with_label.html'
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            'year',
        )


class BudgetFilter(django_filters.FilterSet):
    year = django_filters.ChoiceFilter(label="Exercice", choices=[(i, i) for i in range(settings.NOW().year, 2015, -1)],
                                       name='entry__date', lookup_expr='year')

    class Meta:
        model = Transaction
        fields = ('year', )
        form = YearFilterForm

    def __init__(self, data, *args, **kwargs):
        if data is None:
            data = QueryDict('year={}'.format(settings.NOW().year))
        super().__init__(data, *args, **kwargs)


class BalanceFilter(django_filters.FilterSet):
    year = django_filters.ChoiceFilter(label="Exercice", choices=[(i, i) for i in range(settings.NOW().year, 2015, -1)],
                                       name='entry__date', lookup_expr='year')

    class Meta:
        model = Transaction
        fields = ('year', )
        form = YearFilterForm

    def __init__(self, data, *args, **kwargs):
        if data is None:
            data = QueryDict('year={}'.format(settings.NOW().year))
        super().__init__(data, *args, **kwargs)

    @property
    def qs(self):
        qs = super().qs.filter(entry__projected=False)
        return qs


class YearAccountFilterForm(YearFilterForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            'year',
            'account',
            'projected',
        )


class AccountFilter(django_filters.FilterSet):
    year = django_filters.ChoiceFilter(label="Exercice", choices=[(i, i) for i in range(settings.NOW().year, 2015, -1)],
                                       name='entry__date', lookup_expr='year')
    account = django_filters.ModelChoiceFilter(label="Compte", queryset=Account.objects)
    projected = django_filters.BooleanFilter(label="Projeté", name='entry__projected')

    class Meta:
        model = Transaction
        fields = ('year', 'account', 'projected')
        form = YearAccountFilterForm

    @property
    def qs(self):
        qs = super().qs.order_by('entry__date')
        qs = qs.select_related('entry', 'analytic')
        return qs

    def __init__(self, data, *args, **kwargs):
        if data is None:
            data = QueryDict('year={}'.format(settings.NOW().year))
        super().__init__(data, *args, **kwargs)


class AnalyticFilter(django_filters.FilterSet):
    year = django_filters.ChoiceFilter(label="Exercice", choices=[(i, i) for i in range(settings.NOW().year, 2015, -1)],
                                       name='entry__date', lookup_expr='year')
    account = django_filters.ModelChoiceFilter(label="Compte analytique", queryset=Analytic.objects, name='analytic')
    projected = django_filters.BooleanFilter(label="Projeté", name='entry__projected')

    class Meta:
        model = Transaction
        fields = ('year', 'account', 'projected')
        form = YearAccountFilterForm

    @property
    def qs(self):
        qs = super().qs.order_by('entry__date')
        qs = qs.select_related('entry', 'account')
        return qs

    def __init__(self, data, *args, **kwargs):
        if data is None:
            data = QueryDict('year={}'.format(settings.NOW().year))
        super().__init__(data, *args, **kwargs)
