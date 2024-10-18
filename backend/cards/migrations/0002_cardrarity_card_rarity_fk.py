# Generated by Django 4.1.3 on 2024-10-16 13:59

from django.db import migrations, models
import django.db.models.deletion
from cards.models import Card, CardRarity, Set

def convert_rarity(*args, **kwargs):
    for card in Card.objects.all():
        rarity_name = card.rarity
        try:
            rarity_object = CardRarity.objects.get(set__extension_id=card.extension_id, name=rarity_name)
        except CardRarity.DoesNotExist:
            rarity_object = CardRarity(
                set=Set.objects.get(extension_id=card.extension_id),         
                name=rarity_name, 
                rate=1
            )
            rarity_object.save()
        card.rarity_fk = rarity_object
        card.save()

class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardRarity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('holo', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=30, null=True)),
                ('rate', models.IntegerField()),
                ('set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.set')),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='rarity_fk',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cards.cardrarity', null=True),
            preserve_default=False,
        ),
        migrations.RunPython(convert_rarity),
        migrations.RemoveField(
            model_name='card',
            name='rarity',
        ),
        migrations.RenameField(
            model_name='card',
            old_name='rarity_fk',
            new_name='rarity',
        ),
    ]
