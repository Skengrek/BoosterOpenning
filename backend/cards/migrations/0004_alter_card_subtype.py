# Generated by Django 4.1.3 on 2023-02-21 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cards", "0003_alter_card_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="card",
            name="subType",
            field=models.CharField(max_length=30, null=True),
        ),
    ]
