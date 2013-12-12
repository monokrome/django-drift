from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from ...models import Import
from ...tasks import drift_task


class Command(BaseCommand):
    args = '<import_id import_id ...>'
    help = 'Run drift imports for Imports with the provided IDs.'

    option_list = BaseCommand.option_list + (
        make_option(
            '--all',
            dest='all',
            default=False,

            help='Execute all new imports in the database',
            action='store_true'
        ),

        make_option(
            '--async',
            dest='async',
            default=False,

            help='Execute imports asyncronously via celery',
            action='store_true'
        ),

        make_option(
            '--verbose',
            dest='verbose',
            default=False,

            help='Provides verbose output from the import tasks',
            action='store_true'
        )
    )

    def handle_item(self, instance, options):
        if options['verbose'] is True:
            print('Running drift import for ' + str(instance))

        if options['async'] is True:
            drift_task.apply_async(
                (instance,)
            )
        else:
            drift_task(instance)

    def handle(self, *args, **options):
        if options['all'] is True:
            imports = Import.objects.filter(status='created')

        elif len(args) > 0:
            imports = [Import.objects.filter(pk__in=args)]

        else: raise CommandError(
                'The ID of a specific import is required by this command.'
            )

        if options['verbose'] is True:
            print('Drift imports will be executed asyncronously via celery.')

        results = [self.handle_item(item, options) for item in imports]

        if options['verbose'] is True:
            if options['async'] is True:
                print('Asyncronous import started for {0} items.'.format(
                    len(results))
                )

            else:
                print('Executed import task for {0} items.'.format(
                    len(results)
                ))
