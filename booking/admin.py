from django.contrib import admin
from .models import BookingState, Booking, BookingItem, TrackingEvent, TrackingValue, Agreement, Payment


@admin.register(BookingState)
class BookingStateAdmin(admin.ModelAdmin):
    list_display = ('title', 'color', 'income')


@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'booking')
    ordering = ('-date', )


class AgreementInline(admin.TabularInline):
    model = Agreement
    fields = ('date', 'order', 'odt', 'pdf')
    extra = 1


class BookingItemInline(admin.TabularInline):
    model = BookingItem
    fields = ('product', 'title', 'headcount', 'begin', 'end', 'price_pppn', 'price_pn', 'price_pp', 'price',
              'cotisation')


class PaymentInline(admin.TabularInline):
    model = Payment
    fields = ('mean', 'date', 'amount', 'scan')
    extra = 1


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    inlines = (AgreementInline, BookingItemInline, PaymentInline)
    list_display = ('title', 'year', 'state', 'contact', 'email', 'tel', 'agreement')
    list_filter = ('state', 'year')
    search_fields = ('title', 'contact', 'email')


class TrackingValueInline(admin.TabularInline):
    model = TrackingValue
    fields = ('field', 'value')


@admin.register(TrackingEvent)
class TrackingEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'obj')
    inlines = (TrackingValueInline, )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('mean', 'date', 'amount', 'booking')
    search_fields = ('booking__title', )
    list_filter = ('mean', )
    date_hierarchy = 'date'
