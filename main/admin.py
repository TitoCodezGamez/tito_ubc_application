from django.contrib import admin
from .models import FormEntry, Response

class FormEntryInline(admin.TabularInline):
	model = FormEntry
	extra = 0
	fields = ('name', 'dropdown', 'text')
	readonly_fields = ()

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
	list_display = ('name', 'created')
	inlines = [FormEntryInline]

@admin.register(FormEntry)
class FormEntryAdmin(admin.ModelAdmin):
	list_display = ('name', 'dropdown', 'text', 'response')
	list_filter = ('response',)
	search_fields = ('name', 'text', 'dropdown', 'response__name')
