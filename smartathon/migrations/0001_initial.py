# Generated by Django 4.1.5 on 2023-01-23 17:06

from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields
import smartathon.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Competition",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=40)),
                ("description", models.CharField(max_length=200)),
                ("date", models.DateTimeField()),
                ("venue", models.CharField(max_length=200)),
                ("max_members", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "name",
                    models.CharField(max_length=40, primary_key=True, serialize=False),
                ),
                ("password", models.CharField(max_length=69)),
                ("mail", models.CharField(max_length=69)),
            ],
        ),
        migrations.CreateModel(
            name="UserReference",
            fields=[
                (
                    "u_name",
                    models.CharField(
                        default="null u_name reference",
                        max_length=40,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TeamDetails",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=40)),
                ("vacant_spaces", models.IntegerField(default=0)),
                (
                    "members",
                    djongo.models.fields.ArrayField(
                        model_container=smartathon.models.UserReference
                    ),
                ),
                (
                    "competition",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="smartathon.competition",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Request",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("request_message", models.CharField(max_length=100)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="smartathon.user",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="smartathon.teamdetails",
                    ),
                ),
            ],
        ),
    ]
