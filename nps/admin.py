from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import RawResults, ClientAggregations, Comments, CommentCategories, CommentAnalysis, Products

admin.site.register(ClientAggregations)
admin.site.register(Comments)
admin.site.register(CommentCategories)
admin.site.register(CommentAnalysis)


@admin.register(RawResults)
class RawResultsAdmin(ImportExportModelAdmin):
    pass


@admin.register(Products)
class ProductsAdmin(ImportExportModelAdmin):
    pass

