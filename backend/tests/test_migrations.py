from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test.testcases import TransactionTestCase


class MigrationTestCase(TransactionTestCase):
    """A Test case for testing migrations"""

    # These must be defined by subclasses.
    migrate_from = None
    migrate_to = None

    def setUp(self):
        super(MigrationTestCase, self).setUp()

        self.executor = MigrationExecutor(connection)
        self.executor.migrate(self.migrate_from)

    def migrate_to_dest(self):
        self.executor.loader.build_graph()  # reload.
        self.executor.migrate(self.migrate_to)

    @property
    def old_apps(self):
        return self.executor.loader.project_state(self.migrate_from).apps

    @property
    def new_apps(self):
        return self.executor.loader.project_state(self.migrate_to).apps


class TestMigrationToAnnotatorProject_0015(MigrationTestCase):

    migrate_from = [('backend', "0014_annotation_time_to_complete")]
    migrate_to = [('backend', "0015_auto_20220318_1620")]

    def test_migration_to_0015(self):
        # Setup code
        User = self.old_apps.get_model('backend', "ServiceUser")
        Project = self.old_apps.get_model('backend', "Project")
        Document = self.old_apps.get_model('backend', "Document")
        Annotation = self.old_apps.get_model('backend', "Annotation")

        # Create a project
        test_projectname = "Test project1"
        project = Project.objects.create(name=test_projectname)
        project2 = Project.objects.create()
        project2_id = project2.id
        project3 = Project.objects.create()
        project3_id = project3.id


        # Create 10 users and add to project
        num_project_users = 10
        for i in range(num_project_users):
            User.objects.create(username=f"user{i}", annotates_id=project.id)

        # Create more users with no project
        num_non_project_users = 15
        for i in range(num_non_project_users):
            User.objects.create(username=f"nonprojuser{i}")

        # Create annotated documents for project 2 and 3 for user0 to test
        # that they're also migrated to projects they're currently not active in
        user0 = User.objects.get(username="user0")
        doc1 = Document.objects.create(project_id=project2_id)
        Annotation.objects.create(document_id=doc1.id, user_id=user0.id)

        doc2 = Document.objects.create(project_id=project3_id)
        Annotation.objects.create(document_id=doc2.id, user_id=user0.id)

        # Perform migration
        self.migrate_to_dest()

        User = self.new_apps.get_model('backend', "ServiceUser")
        Project = self.new_apps.get_model('backend', "Project")
        AnnotatorProject = self.new_apps.get_model('backend', 'AnnotatorProject')

        # assertions
        user = User.objects.get(username="user0")

        # User project associations
        self.assertEqual(3, user.annotates.count(), "User must be associated with 3 projects")

        # user0 must have 1 active project
        self.assertEqual(1, AnnotatorProject.objects.filter(annotator_id=user.id, status=0).count())
        for ap in AnnotatorProject.objects.filter(annotator_id=user.id, status=0):
            self.assertEqual(test_projectname, ap.project.name, f"Project name must be {test_projectname}")

        # user0 must have 2 inactive project
        self.assertEqual(2, AnnotatorProject.objects.filter(annotator_id=user.id, status=1).count())


        project = Project.objects.get(name=test_projectname)
        self.assertEqual(num_project_users, project.annotators.count(), f"Project must have {num_project_users} users")

