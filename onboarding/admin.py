# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models
from crm.models import Person, PersonState
from organizer.admin import admin_site

def signup_approver(modeladmin, request, queryset):
    for signup in queryset:
        person, _ = Person.objects.update_or_create(email=signup.email)
        if signup.event is not None:
            event = signup.event
            event.attendees.add(person)
            event.save()
        signup.approved = True
        signup.save()
signup_approver.short_description = "Approve selected signups"

class SignupAdmin(admin.ModelAdmin):
    actions = [
        signup_approver
    ]

    list_display = [
        'email', 'created', 'event', 'approved'
    ]
    search_fields = [
        'email', 'event__name'
    ]
    list_filter = ('approved', ('event', admin.RelatedOnlyFieldListFilter))
    raw_id_fields = ('event',)

class StatusAdmin(admin.ModelAdmin):
    list_display = [
        'person', 'component', 'created', 'success'
    ]

    list_filter = ('component', 'success')
    readonly_fields = ('message','created')

def disable_components(modeladmin, request, queryset):
    queryset.update(enabled=False)
disable_components.short_description = "Disable selected components"

def enable_components(modeladmin, request, queryset):
    queryset.update(enabled=False)
enable_components.short_description = "Enable selected components"

class ComponentAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'handler', 'filter', 'enabled'
    ]

    actions = [
        disable_components,
        enable_components
    ]

admin.site.register(models.NewNeighborNotificationTarget)
admin.site.register(models.Signup, SignupAdmin)
admin.site.register(models.OnboardingStatus, StatusAdmin)
admin.site.register(models.OnboardingComponent, ComponentAdmin)

admin_site.register(models.NewNeighborNotificationTarget)
admin_site.register(models.Signup, SignupAdmin)
