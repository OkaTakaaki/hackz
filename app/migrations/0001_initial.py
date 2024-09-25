<<<<<<< HEAD
# Generated by Django 4.2.6 on 2024-09-25 17:32
=======
# Generated by Django 4.2.6 on 2024-09-25 09:08
>>>>>>> developer2_jun

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomUser",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "created_at",
                    models.DateField(auto_now_add=True, verbose_name="登録日時"),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="AdminUser",
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
                ("adminname", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name="Aphorism",
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
                ("word", models.CharField(max_length=100)),
                ("author", models.CharField(blank=True, max_length=100, null=True)),
                ("picture", models.ImageField(upload_to="images/")),
                (
                    "rarity",
                    models.IntegerField(
                        choices=[
                            (1, "☆"),
                            (2, "☆☆"),
                            (3, "☆☆☆"),
                            (4, "☆☆☆☆"),
                            (5, "☆☆☆☆☆"),
                        ],
                        default="common",
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Schedule",
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
                ("summary", models.CharField(max_length=50, verbose_name="概要")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="詳細な説明"),
                ),
                (
                    "start_time",
                    models.TimeField(
                        default=datetime.time(7, 0), verbose_name="開始時間"
                    ),
                ),
                (
                    "end_time",
                    models.TimeField(
                        default=datetime.time(7, 0), verbose_name="終了時間"
                    ),
                ),
                ("date", models.DateField(verbose_name="日付")),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="作成日"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Goal",
            fields=[
<<<<<<< HEAD
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivation', models.IntegerField(blank=True, null=True, verbose_name='モチベーション')),
                ('objective', models.CharField(max_length=100, verbose_name='目標')),
                ('achievement', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='達成度')),
                ('number', models.IntegerField(blank=True, null=True, verbose_name='件数')),
                ('turned', models.CharField(blank=True, max_length=200, null=True, verbose_name='振り返り')),
                ('created_at', models.DateTimeField(verbose_name='作成日')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
=======
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "motivation",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(10),
                        ],
                        verbose_name="モチベーション",
                    ),
                ),
                ("objective", models.CharField(max_length=100, verbose_name="目標")),
                (
                    "achievement",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="達成度",
                    ),
                ),
                (
                    "number",
                    models.IntegerField(blank=True, null=True, verbose_name="件数"),
                ),
                (
                    "turned",
                    models.CharField(
                        blank=True, max_length=200, null=True, verbose_name="振り返り"
                    ),
                ),
                ("created_at", models.DateTimeField(verbose_name="作成日")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
>>>>>>> developer2_jun
            ],
        ),
        migrations.CreateModel(
            name="Collection",
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
                ("word", models.CharField(max_length=200)),
                ("author", models.CharField(max_length=200)),
                ("picture", models.ImageField(upload_to="images/")),
                (
                    "acquision_date",
                    models.DateTimeField(verbose_name="Acquisition dat"),
                ),
                (
                    "rarity",
                    models.IntegerField(
                        choices=[
                            (1, "☆"),
                            (2, "☆☆"),
                            (3, "☆☆☆"),
                            (4, "☆☆☆☆"),
                            (5, "☆☆☆☆☆"),
                        ]
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
