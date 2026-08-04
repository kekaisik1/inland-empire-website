# Generated target-natively for Inland Empire Phase 02 on 2026-07-31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0011_homepage_section_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="footer_company_order",
            field=models.CharField(
                blank=True,
                default="about,contact,blog,service_areas,privacy_policy,terms_of_service",
                help_text="Comma-separated footer company link keys in display order. Allowed keys: about, contact, blog, service_areas, privacy_policy, terms_of_service. Remove a key to hide it.",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="main_nav_order",
            field=models.CharField(
                blank=True,
                default="home,services,service_areas,brands,blog,about,contact",
                help_text="Comma-separated top navigation keys in display order. Allowed keys: home, services, service_areas, brands, blog, about, contact. Remove a key to hide it.",
                max_length=255,
            ),
        ),
    ]
