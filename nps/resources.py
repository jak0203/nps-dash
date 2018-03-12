from import_export import resources
from .models import AggregatedResults, RawResults


class AggregatedResultsResource(resources.ModelResource):
    class Meta:
        model = AggregatedResults


class RawResultsResource(resources.ModelResource):
    # def skip_row(self, instance, original):
    #     print(instance, original)
    #     return super(RawResultsResource, self).skip_row(instance, original)
    def before_import(self, dataset, dry_run):
        print('DELETING STUFF!')
        RawResults.objects.all().delete()

    class Meta:
        model = RawResults
        import_id_fields = ('client', 'survey_name', 'question_name', 'user_id')
        skip_unchanged = True
        report_skipped = True


