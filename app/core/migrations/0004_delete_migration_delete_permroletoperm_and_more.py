# Generated by Django 5.0.1 on 2024-04-11 19:28

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_set_user_and_user_role_managed_false"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    # find all potential foreign key relationships and scrub the data to locate and
    #  remove any potential integrity errors
    # e.g. the "lti" table will have a relationship with the "widget_instance" table based
    #  on the "item_id" column, so find any situations where there is not a row in
    #  "widget_instance" with an "id" corresponding to any "item_id" in the "lti" table
    def cleanData(apps, schema_editor):
        from django.contrib.auth.models import User
        from django.db import connection

        import logging
        logger = logging.getLogger('django')

        logger.info("Deleting potentially invalid rows to avoid integrity errors in foreign keys")
        OldDateRange = apps.get_model("core", "DateRange")
        OldLogActivity = apps.get_model("core", "LogActivity")
        OldLogPlay = apps.get_model("core", "LogPlay")
        # OldLogStorage = apps.get_model("core", "LogStorage")
        OldLti = apps.get_model("core", "Lti")
        # OldMapQuestionToQset = apps.get_model("core", "MapQuestionToQset")
        # OldPermObjectToUser = apps.get_model("core", "PermObjectToUser")
        OldQuestion = apps.get_model("core", "Question")
        OldWidget = apps.get_model("core", "Widget")
        OldWidgetInstance = apps.get_model("core", "WidgetInstance")
        # OldWidgetMetadata = apps.get_model("core", "WidgetMetadata")
        OldWidgetQset = apps.get_model("core", "WidgetQset")

        # these three are foundational
        all_semester_ids = OldDateRange.objects.values_list("id", flat=True)
        all_user_ids = User.objects.values_list("id", flat=True)
        all_widget_ids = OldWidget.objects.values_list("id", flat=True)

        # Question -> User via user_id
        invalid_question_rows = OldQuestion.objects.exclude(user_id__in=all_user_ids)
        for invalid_question in invalid_question_rows:
            logger.info(f"deleting Question row {invalid_question.id} without matching User {invalid_question.user_id}")
            invalid_question.delete()

        # all Question rows should be valid by now
        all_question_ids = OldQuestion.objects.values_list("id", flat=True)

        # WidgetInstance -> User via published_by
        invalid_widget_instance_rows = OldWidgetInstance.objects.exclude(published_by__in=all_user_ids)
        for invalid_widget_instance in invalid_widget_instance_rows:
            logger.info(f"deleting WidgetInstance row {invalid_widget_instance.id} without matching published_by User {invalid_widget_instance.published_by}")
            invalid_widget_instance.delete()

        # WidgetInstance -> User via user_id
        invalid_widget_instance_rows = OldWidgetInstance.objects.exclude(user_id__in=all_user_ids)
        for invalid_widget_instance in invalid_widget_instance_rows:
            logger.info(f"deleting WidgetInstance row {invalid_widget_instance.id} without matching user_id User {invalid_widget_instance.user_id}")
            invalid_widget_instance.delete()

        # WidgetInstance -> Widget via widget_id
        invalid_widget_instance_rows = OldWidgetInstance.objects.exclude(widget_id__in=all_widget_ids)
        for invalid_widget_instance in invalid_widget_instance_rows:
            logger.info(f"deleting WidgetInstance row {invalid_widget_instance.id} without matching Widget {invalid_widget_instance.widget_id}")
            invalid_widget_instance.delete()

        # all WidgetInstance rows should be valid by now
        all_instance_ids = OldWidgetInstance.objects.values_list("id", flat=True)

        # WidgetQset -> WidgetInstance via inst_id
        invalid_widget_qset_rows = OldWidgetQset.objects.exclude(inst_id__in=all_instance_ids)
        for invalid_widget_qset in invalid_widget_qset_rows:
            logger.info(f"deleting WidgetQset row {invalid_widget_qset.id} without matching WidgetInstance {invalid_widget_qset.inst_id}")
            invalid_widget_qset.delete()

        # all WidgetQset rows should be valid by now
        all_qset_ids = OldWidgetQset.objects.values_list("id", flat=True)

        # LogActivity -> User via user_id
        invalid_log_activity_rows = OldLogActivity.objects.exclude(user_id__in=all_user_ids)
        for invalid_log_activity in invalid_log_activity_rows:
            logger.info(f"deleting LogActivity row {invalid_log_activity.id} without matching User {invalid_log_activity.user_id}")
            invalid_log_activity.delete()

        # LogPlay -> WidgetInstance via inst_id
        invalid_log_play_rows = OldLogPlay.objects.exclude(inst_id__in=all_instance_ids)
        for invalid_log_play in invalid_log_play_rows:
            logger.info(f"deleting LogPlay row {invalid_log_play.id} without matching WidgetInstance {invalid_log_play.inst_id}")
            invalid_log_play.delete()

        # LogPlay -> WidgetQset via qset_id
        invalid_log_play_rows = OldLogPlay.objects.exclude(qset_id__in=all_qset_ids)
        for invalid_log_play in invalid_log_play_rows:
            logger.info(f"deleting LogPlay row {invalid_log_play.id} without matching WidgetQset {invalid_log_play.qset_id}")
            invalid_log_play.delete()

        # LogPlay -> DateRange via semester_id
        invalid_log_play_rows = OldLogPlay.objects.exclude(semester__in=all_semester_ids)
        for invalid_log_play in invalid_log_play_rows:
            logger.info(f"deleting LogPlay row {invalid_log_play.id} without matching DateRange {invalid_log_play.semester}")
            invalid_log_play.delete()

        # LogPlay -> User via user_id
        invalid_log_play_rows = OldLogPlay.objects.exclude(user_id__in=all_user_ids)
        for invalid_log_play in invalid_log_play_rows:
            logger.info(f"deleting LogPlay row {invalid_log_play.id} without matching User {invalid_log_play.user_id}")
            invalid_log_play.delete()

        # Lti -> WidgetInstance via item_id
        invalid_lti_rows = OldLti.objects.exclude(item_id__in=all_instance_ids)
        for invalid_lti in invalid_lti_rows:
            logger.info(f"deleting Lti row {invalid_lti.id} without matching WidgetInstance {invalid_lti.item_id}")
            invalid_lti.delete()

        # Lti -> User via user_id
        invalid_lti_rows = OldLti.objects.exclude(user_id__in=all_user_ids)
        for invalid_lti in invalid_lti_rows:
            logger.info(f"deleting Lti row {invalid_lti.id} without matching User {invalid_lti.user_id}")
            invalid_lti.delete()

        # the remaining models have primary key "id" columns added to it as part of this migration,
        #  which means the existing tables will not have a primary key and ORM lookups will throw
        #  an OperationalError
        # we have to perform raw SQL deletions instead

        # LogStorage -> WidgetInstance via inst_id
        logger.info("deleting all LogStorage rows without matching WidgetInstance")
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM log_storage WHERE inst_id NOT IN (SELECT id FROM widget_instance)")
            logger.info(f"deleted {cursor.rowcount} LogStorage rows without matching WidgetInstance")

        # LogStorage -> LogPlay via play_id
        logger.info("deleting all LogStorage rows without matching LogPlay")
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM log_storage WHERE play_id NOT IN (SELECT id FROM log_play)")
            logger.info(f"deleted {cursor.rowcount} LogStorage rows without matching LogPlay")

        # LogStorage -> User via user_id
        logger.info("deleting all LogStorage rows without matching User")
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM log_storage WHERE user_id NOT IN (SELECT id FROM auth_user)")
            logger.info(f"deleted {cursor.rowcount} LogStorage rows without matching User")

        # MapQuestionToQset -> WidgetQset via qset_id
        logger.info("deleting all MapQuestionToQset rows without matching WidgetQset")
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM map_question_to_qset WHERE qset_id NOT IN (SELECT id FROM widget_qset)")
            logger.info(f"deleted {cursor.rowcount} MapQuestionToQset rows without matching WidgetQset")

        # MapQuestionToQset -> Question via question_id
        logger.info("deleting all MapQuestionToQset rows without matching Question")
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM map_question_to_qset WHERE question_id NOT IN (SELECT id FROM question)")
            logger.info(f"deleted {cursor.rowcount} MapQuestionToQset rows without matching Question")

        # PermObjectToUser -> User via user_id
        logger.info("deleting all PermObjectToUser rows without matching User")
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM perm_object_to_user WHERE user_id NOT IN (SELECT id FROM auth_user)")
            logger.info(f"deleted {cursor.rowcount} PermObjectToUser rows without matching User")

        # WidgetMetadata -> Widget via widget_id
        logger.info("deleting all WidgetMetadata rows without matching Widget")
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM widget_metadata WHERE widget_id NOT IN (SELECT id FROM widget)")
            logger.info(f"deleted {cursor.rowcount} WidgetMetadata rows without matching Widget")

    # no real way of restoring deleted rows, but we need something there
    def nothing(*args, **kwargs):
        pass

    operations = [
        # because Django won't allow us to supply None as a rollback operation
        migrations.RunPython(cleanData, nothing),

        migrations.DeleteModel(
            name="Migration",
        ),
        migrations.DeleteModel(
            name="PermRoleToPerm",
        ),
        migrations.DeleteModel(
            name="PermRoleToUser",
        ),
        migrations.DeleteModel(
            name="PermRoleToUserBackup",
        ),
        migrations.DeleteModel(
            name="Sessions",
        ),
        migrations.DeleteModel(
            name="UserMeta",
        ),
        migrations.DeleteModel(
            name="UserRole",
        ),
        migrations.DeleteModel(
            name="Users",
        ),
        migrations.RenameField(
            model_name="asset",
            old_name="type",
            new_name="file_type",
        ),
        migrations.AddField(
            model_name="daterange",
            name="end_at_dt",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="daterange",
            name="start_at_dt",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="log",
            name="created_at_dt",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="logactivity",
            name="created_at_dt",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="logplay",
            name="created_at_dt",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="logstorage",
            name="created_at_dt",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="lti",
            name="created_at_dt",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="lti",
            name="updated_at_dt",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="notification",
            name="created_at_dt",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="notification",
            name="updated_at_dt",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="permobjecttouser",
            name="expires_at_dt",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="question",
            name="created_at_dt",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="question",
            name="qset",
            field=models.ManyToManyField(
                through="core.MapQuestionToQset", to="core.widgetqset"
            ),
        ),
        migrations.AlterField(
            model_name="log",
            name="visible",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="logactivity",
            name="user_id",
            field=models.ForeignKey(
                db_column="user_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="activity_logs",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="logplay",
            name="auth",
            field=models.CharField(choices=[("", ""), ("lti", "lti")], max_length=100),
        ),
        migrations.AlterField(
            model_name="logplay",
            name="inst_id",
            field=models.ForeignKey(
                db_column="inst_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="play_logs",
                to="core.widgetinstance",
            ),
        ),
        migrations.AlterField(
            model_name="logplay",
            name="is_complete",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="logplay",
            name="is_valid",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="logplay",
            name="qset_id",
            field=models.ForeignKey(
                db_column="qset_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="play_logs",
                to="core.widgetqset",
            ),
        ),
        migrations.AlterField(
            model_name="logplay",
            name="semester",
            field=models.ForeignKey(
                db_column="semester_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="play_logs",
                to="core.daterange",
            ),
        ),
        migrations.AlterField(
            model_name="logplay",
            name="user_id",
            field=models.ForeignKey(
                db_column="user_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="play_logs",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="logstorage",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="logstorage",
            name="inst_id",
            field=models.ForeignKey(
                db_column="inst_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="storage_logs",
                to="core.widgetinstance",
            ),
        ),
        migrations.AlterField(
            model_name="logstorage",
            name="play_id",
            field=models.ForeignKey(
                db_column="play_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="storage_logs",
                to="core.logplay",
            ),
        ),
        migrations.AlterField(
            model_name="logstorage",
            name="user_id",
            field=models.ForeignKey(
                db_column="user_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="storage_logs",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="lti",
            name="item_id",
            field=models.ForeignKey(
                db_column="item_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="lti_embeds",
                to="core.widgetinstance",
            ),
        ),
        migrations.AlterField(
            model_name="lti",
            name="user_id",
            field=models.ForeignKey(
                db_column="user_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="lti_embeds",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="mapquestiontoqset",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="mapquestiontoqset",
            name="qset_id",
            field=models.ForeignKey(
                db_column="qset_id",
                on_delete=django.db.models.deletion.PROTECT,
                to="core.widgetqset",
            ),
        ),
        migrations.AlterField(
            model_name="mapquestiontoqset",
            name="question_id",
            field=models.ForeignKey(
                db_column="question_id",
                on_delete=django.db.models.deletion.PROTECT,
                to="core.question",
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="is_email_sent",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="notification",
            name="is_read",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="notification",
            name="item_type",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="permobjecttouser",
            name="perm",
            field=models.IntegerField(
                choices=[
                    (1, "visible/view scores"),
                    (30, "full"),
                    (85, "support user"),
                    (90, "super user"),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="permobjecttouser",
            name="user_id",
            field=models.ForeignKey(
                db_column="user_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="object_permissions",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="user_id",
            field=models.ForeignKey(
                db_column="user_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="questions",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="widget",
            name="in_catalog",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="widget",
            name="is_answer_encrypted",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="widget",
            name="is_editable",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="widget",
            name="is_playable",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="widget",
            name="is_qset_encrypted",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="widget",
            name="is_scalable",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="widget",
            name="is_scorable",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="widget",
            name="is_storage_enabled",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="widget",
            name="restrict_publish",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="widget",
            name="score_type",
            field=models.CharField(
                choices=[
                    ("SERVER", "widget is scored on the server"),
                    ("CLIENT", "widget is scored on the client"),
                    (
                        "SERVER-CLIENT",
                        "widget is partially scored in both server and client",
                    ),
                ],
                max_length=13,
            ),
        ),
        migrations.AlterField(
            model_name="widgetinstance",
            name="embedded_only",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="widgetinstance",
            name="guest_access",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="widgetinstance",
            name="is_deleted",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="widgetinstance",
            name="is_draft",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="widgetinstance",
            name="is_student_made",
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name="widgetinstance",
            name="published_by",
            field=models.ForeignKey(
                blank=True,
                db_column="published_by",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="published_instances",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="widgetinstance",
            name="user_id",
            field=models.ForeignKey(
                db_column="user_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="created_instances",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="widgetinstance",
            name="widget_id",
            field=models.ForeignKey(
                db_column="widget_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="instances",
                to="core.widget",
            ),
        ),
        migrations.AlterField(
            model_name="widgetmetadata",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="widgetmetadata",
            name="widget_id",
            field=models.ForeignKey(
                db_column="widget_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="metadata",
                to="core.widget",
            ),
        ),
        migrations.AlterField(
            model_name="widgetqset",
            name="inst_id",
            field=models.ForeignKey(
                db_column="inst_id",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="qsets",
                to="core.widgetinstance",
            ),
        ),
        migrations.AddIndex(
            model_name="assetdata",
            index=models.Index(fields=["hash"], name="asset_data_hash"),
        ),
        migrations.AddIndex(
            model_name="assetdata",
            index=models.Index(fields=["created_at"], name="asset_data_created_at"),
        ),
        migrations.AddIndex(
            model_name="log",
            index=models.Index(fields=["play_id"], name="log_play_id"),
        ),
        migrations.AddIndex(
            model_name="log",
            index=models.Index(fields=["type"], name="log_type"),
        ),
        migrations.AddIndex(
            model_name="log",
            index=models.Index(fields=["created_at"], name="log_created_at"),
        ),
        migrations.AddIndex(
            model_name="logactivity",
            index=models.Index(fields=["type"], name="log_activity_type"),
        ),
        migrations.AddIndex(
            model_name="logactivity",
            index=models.Index(fields=["item_id"], name="log_activity_item_id"),
        ),
        migrations.AddIndex(
            model_name="logactivity",
            index=models.Index(fields=["created_at"], name="log_activity_created_at"),
        ),
        migrations.AddIndex(
            model_name="logplay",
            index=models.Index(fields=["created_at"], name="log_play_created_at"),
        ),
        migrations.AddIndex(
            model_name="logplay",
            index=models.Index(fields=["is_complete"], name="log_play_is_complete"),
        ),
        migrations.AddIndex(
            model_name="logplay",
            index=models.Index(fields=["percent"], name="log_play_percent"),
        ),
        migrations.AddIndex(
            model_name="logstorage",
            index=models.Index(fields=["created_at"], name="log_storage_created_at"),
        ),
        migrations.AddIndex(
            model_name="logstorage",
            index=models.Index(fields=["name"], name="log_storage_name"),
        ),
        migrations.AddIndex(
            model_name="lti",
            index=models.Index(fields=["resource_link"], name="lti_resource_link"),
        ),
        migrations.AddIndex(
            model_name="lti",
            index=models.Index(fields=["consumer_guid"], name="lti_consumer_guid"),
        ),
        migrations.AddIndex(
            model_name="notification",
            index=models.Index(
                fields=["is_email_sent"], name="notification_is_email_sent"
            ),
        ),
        migrations.AddIndex(
            model_name="notification",
            index=models.Index(fields=["to_id"], name="notification_to_id"),
        ),
        migrations.AddIndex(
            model_name="notification",
            index=models.Index(fields=["from_id"], name="notification_from_id"),
        ),
        migrations.AddIndex(
            model_name="notification",
            index=models.Index(fields=["item_type"], name="notification_item_type"),
        ),
        migrations.AddIndex(
            model_name="question",
            index=models.Index(fields=["hash"], name="question_hash"),
        ),
        migrations.AddIndex(
            model_name="question",
            index=models.Index(fields=["type"], name="question_type"),
        ),
        migrations.AddIndex(
            model_name="userextraattempts",
            index=models.Index(fields=["user_id"], name="user_extra_attempts_user_id"),
        ),
        migrations.AddIndex(
            model_name="userextraattempts",
            index=models.Index(fields=["inst_id"], name="user_extra_attempts_inst_id"),
        ),
        migrations.AddIndex(
            model_name="widget",
            index=models.Index(fields=["clean_name"], name="widget_clean_name"),
        ),
        migrations.AddIndex(
            model_name="widget",
            index=models.Index(fields=["in_catalog"], name="widget_in_catalog"),
        ),
        migrations.AddIndex(
            model_name="widgetinstance",
            index=models.Index(
                fields=["created_at"], name="widget_instance_created_at"
            ),
        ),
        migrations.AddIndex(
            model_name="widgetinstance",
            index=models.Index(fields=["is_draft"], name="widget_instance_is_draft"),
        ),
        migrations.AddIndex(
            model_name="widgetinstance",
            index=models.Index(
                fields=["is_deleted"], name="widget_instance_is_deleted"
            ),
        ),
        migrations.AddIndex(
            model_name="widgetqset",
            index=models.Index(fields=["created_at"], name="widget_qset_created_at"),
        ),
        migrations.AddConstraint(
            model_name="assetdata",
            constraint=models.UniqueConstraint(
                fields=("id", "size"), name="asset_data_main"
            ),
        ),
        migrations.AddConstraint(
            model_name="daterange",
            constraint=models.UniqueConstraint(
                fields=("semester", "year", "start_at", "end_at"),
                name="date_range_main",
            ),
        ),
        migrations.AddConstraint(
            model_name="mapassettoobject",
            constraint=models.UniqueConstraint(
                fields=("object_id", "object_type", "asset_id"),
                name="map_asset_to_object_main",
            ),
        ),
        migrations.AddConstraint(
            model_name="permobjecttouser",
            constraint=models.UniqueConstraint(
                fields=("object_id", "user_id", "perm", "object_type"),
                name="perm_object_to_user_main",
            ),
        ),
        migrations.AddConstraint(
            model_name="widgetmetadata",
            constraint=models.UniqueConstraint(
                fields=("widget_id", "name"), name="widget_metadata_main"
            ),
        ),
    ]
