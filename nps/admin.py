from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import RawResults, AggregatedResults, Comments, CommentCategories, CommentAnalysis, Products, ProductUsers

admin.site.register(AggregatedResults)
admin.site.register(Comments)
admin.site.register(CommentCategories)
admin.site.register(CommentAnalysis)


@admin.register(RawResults)
class RawResultsAdmin(ImportExportModelAdmin):
    pass


@admin.register(Products)
class ProductsAdmin(ImportExportModelAdmin):
    pass

@admin.register(ProductUsers)
class ProductUsers(ImportExportModelAdmin):
    pass
