# Generated by Django 2.1.2 on 2018-11-01 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20181027_1240'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topic',
            options={'verbose_name': 'Тематика'},
        ),
        migrations.AddField(
            model_name='topic',
            name='image',
            field=models.ImageField(default='/static/default_images/hashtag-default-image.jpg', upload_to='themes/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='published',
            field=models.BooleanField(default=False, verbose_name='Опубликовать'),
        ),
        migrations.AlterField(
            model_name='post',
            name='topics',
            field=models.ManyToManyField(to='blog.Topic', verbose_name='Тематика публикации'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='title',
            field=models.CharField(max_length=500, unique=True, verbose_name='наименованием'),
        ),
    ]
