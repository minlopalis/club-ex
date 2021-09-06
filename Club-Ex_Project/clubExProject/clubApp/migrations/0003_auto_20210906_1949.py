# Generated by Django 3.2.7 on 2021-09-06 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('clubApp', '0002_auto_20210906_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videorating',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_ratings', to='accounts.customer'),
        ),
        migrations.AlterField(
            model_name='videowatchtime',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_watch_times', to='accounts.customer'),
        ),
    ]
