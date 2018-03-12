from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import RawResults, AggregatedResults, Comments, CommentCategories, CommentAnalysis

# admin.site.register(RawResults)
admin.site.register(AggregatedResults)
admin.site.register(Comments)
admin.site.register(CommentCategories)
admin.site.register(CommentAnalysis)

@admin.register(RawResults)
class RawResultsAdmin(ImportExportModelAdmin):
    pass

# from django.contrib import admin
# from .models import Person

# @admin.register(Person)
# class PersonAdmin(ImportExportModelAdmin):
#     pass
