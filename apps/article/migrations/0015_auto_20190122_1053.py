# Generated by Django 2.0.8 on 2019-01-22 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0014_auto_20190121_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='recommend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_recommend', models.BooleanField(default=False, verbose_name='是否推荐')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '文章推荐',
                'verbose_name_plural': '文章推荐',
                'ordering': ('-add_time',),
            },
        ),
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('-add_time',), 'verbose_name': '文章', 'verbose_name_plural': '文章'},
        ),
        migrations.RemoveField(
            model_name='article',
            name='is_recommend',
        ),
        migrations.AddField(
            model_name='recommend',
            name='recommends',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.Article'),
        ),
    ]