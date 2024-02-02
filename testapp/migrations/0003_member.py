# Generated by Django 4.2.4 on 2023-08-13 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("testapp", "0002_book_book_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Member",
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
                ("name_of_member", models.CharField(max_length=500)),
                ("name_of_book_issued", models.CharField(max_length=500)),
                ("Book_id_issued", models.CharField(max_length=500)),
                ("Date_of_book_issued", models.DateTimeField()),
            ],
        ),
    ]