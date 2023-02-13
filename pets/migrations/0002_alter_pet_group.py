# Generated by Django 4.1.6 on 2023-02-06 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("groups", "0001_initial"),
        ("pets", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pet",
            name="group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="pets",
                to="groups.group",
            ),
        ),
    ]
