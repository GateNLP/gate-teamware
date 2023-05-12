from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count, Q

from backend.models import Project, Annotation, Document


def check_repeat_annotation(cmd_object: BaseCommand):
    """
    Check the database to highlight any documents that has more than one annotation by a single annotator. This
    only includes annotations with status COMPLETED,PENDING and REJECTED. ABORTED and TIMED out annotations are ignored.
    """

    completed_pending_rejected_filter = Q(status=Annotation.COMPLETED) | Q(status=Annotation.PENDING) | Q(status=Annotation.REJECTED)
    repeat_count = Count("annotations")
    docs = Document.objects.annotate(num_annotations=repeat_count).filter(num_annotations__gt=1)
    docs_count = 0
    repeat_count = 0
    for doc in docs:
        annotator_id_set = set()
        has_repeat = False
        for annotation in doc.annotations.filter(completed_pending_rejected_filter):
            if annotation.user.pk not in annotator_id_set:
                annotator_id_set.add(annotation.user.pk)
            else:
                has_repeat = True

        if has_repeat:
            repeat_count += 1
            cmd_object.stdout.write(f"Document {doc.pk} has multiple annotations from the same annotator (ID {annotation.user.pk})")
            for annotation in doc.annotations.all():
                print(
                    f"\tAnnotation ID {annotation.pk} Annotator ID {annotation.user.pk}, status: {annotation.status} data: {annotation.data}")

        docs_count += 1

    cmd_object.stdout.write(f"Check completed\n\tNumber of documents checked: {docs_count}.\tNumber of documents with repeats {repeat_count}.")



class Command(BaseCommand):

    help = "Utility for performing various checks for diagnosing issues"

    def add_arguments(self, parser):
        parser.add_argument("check_type", type=str, help="Type of check to perform: repeat_annotation - Check for documents that have repeated annotations")


    def handle(self, *args, **options):
        if "check_type" in options:
            if "repeat_annotation" == options["check_type"]:
                check_repeat_annotation(self)
                return
            else:
                raise CommandError(f"Unknown check type: {options['check_type']}")









