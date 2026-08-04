# Generated target-natively for Inland Empire Phase 02 on 2026-07-31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0009_update_contact_info_corona"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="business_name",
            field=models.CharField(
                default="Inland Empire Appliance Repair",
                help_text="Business name shown in header, footer, and SEO",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="booking_url",
            field=models.URLField(
                blank=True,
                default="",
                help_text="External booking system URL (UTM params will be appended automatically)",
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="booking_source",
            field=models.CharField(
                blank=True,
                default="inland",
                help_text="Source parameter appended to booking URL (e.g. 'inland', 'website')",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="callrail_swap_url",
            field=models.URLField(
                blank=True,
                default="",
                help_text="CallRail swap.js URL for Dynamic Number Insertion (configured per target account; leave blank when disabled)",
            ),
        ),
    ]
