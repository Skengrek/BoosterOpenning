# Generated by Django 4.1.3 on 2022-12-21 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cards", "0002_alter_card_rarity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="card",
            name="large_image",
            field=models.ImageField(default=None, null=True, upload_to="images/large/"),
        ),
        migrations.AlterField(
            model_name="card",
            name="small_image",
            field=models.ImageField(default=None, null=True, upload_to="images/small/"),
        ),
    ]