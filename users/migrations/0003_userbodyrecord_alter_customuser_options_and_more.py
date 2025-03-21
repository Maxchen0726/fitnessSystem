# Generated by Django 4.2 on 2025-03-03 19:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_profile"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserBodyRecord",
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
                ("date", models.DateField(verbose_name="记录日期")),
                ("weight", models.FloatField(verbose_name="体重(kg)")),
                (
                    "body_fat",
                    models.FloatField(blank=True, null=True, verbose_name="体脂率(%)"),
                ),
                (
                    "chest",
                    models.FloatField(blank=True, null=True, verbose_name="胸围(cm)"),
                ),
                (
                    "waist",
                    models.FloatField(blank=True, null=True, verbose_name="腰围(cm)"),
                ),
                (
                    "hips",
                    models.FloatField(blank=True, null=True, verbose_name="臀围(cm)"),
                ),
                ("notes", models.TextField(blank=True, verbose_name="备注")),
            ],
            options={
                "verbose_name": "身体指标记录",
                "verbose_name_plural": "身体指标记录",
                "ordering": ["-date"],
            },
        ),
        migrations.AlterModelOptions(
            name="customuser",
            options={"verbose_name": "用户", "verbose_name_plural": "用户"},
        ),
        migrations.AddField(
            model_name="customuser",
            name="bio",
            field=models.TextField(blank=True, verbose_name="个人简介"),
        ),
        migrations.AddField(
            model_name="customuser",
            name="birth_date",
            field=models.DateField(blank=True, null=True, verbose_name="出生日期"),
        ),
        migrations.AddField(
            model_name="customuser",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("M", "男"), ("F", "女"), ("O", "其他")],
                max_length=1,
                verbose_name="性别",
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="height",
            field=models.FloatField(blank=True, null=True, verbose_name="身高(cm)"),
        ),
        migrations.AddField(
            model_name="customuser",
            name="profile_picture",
            field=models.ImageField(
                blank=True, upload_to="profile_pics", verbose_name="头像"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="target_weight",
            field=models.FloatField(blank=True, null=True, verbose_name="目标体重(kg)"),
        ),
        migrations.AddField(
            model_name="customuser",
            name="weight",
            field=models.FloatField(blank=True, null=True, verbose_name="体重(kg)"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(
                blank=True, max_length=254, verbose_name="email address"
            ),
        ),
        migrations.DeleteModel(
            name="Profile",
        ),
        migrations.AddField(
            model_name="userbodyrecord",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="body_records",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="userbodyrecord",
            unique_together={("user", "date")},
        ),
    ]
