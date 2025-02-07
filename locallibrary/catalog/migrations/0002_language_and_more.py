# Generated by Django 4.2.19 on 2025-02-07 08:25

from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Language",
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
                (
                    "name",
                    models.CharField(
                        help_text="Enter a book language (e.g. Spanish, French etc.)",
                        max_length=200,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="language",
            constraint=models.UniqueConstraint(
                django.db.models.functions.text.Lower("name"),
                name="language_name_case_insensitive_unique",
                violation_error_message="Language already exists (case insensitive match)",
            ),
        ),
    ]
