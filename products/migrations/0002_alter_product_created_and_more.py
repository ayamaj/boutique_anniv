# Generated by Django 5.2 on 2025-04-27 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['created'], name='products_pr_created_9a1943_idx'),
        ),
    ]
