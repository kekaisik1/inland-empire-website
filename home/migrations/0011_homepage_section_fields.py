# Generated target-natively for Inland Empire Phase 02 on 2026-07-31

import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0010_add_callrail_swap_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="areas_heading",
            field=models.CharField(
                blank=True,
                default="Appliance Repair Across the Inland Empire",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="areas_subheading",
            field=models.TextField(
                blank=True,
                default="Use this editable copy for reviewed Inland Empire service-area coverage and ZIP-code messaging.",
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="brands_heading",
            field=models.CharField(
                blank=True,
                default="What Appliance Brands Do We Repair?",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="brands_subheading",
            field=models.TextField(
                blank=True,
                default="Use this editable copy for manufacturer and brand capability language after claims are reviewed.",
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="commercial_body",
            field=wagtail.fields.RichTextField(
                blank=True,
                default="<p>Commercial kitchens and homes both need dependable appliance repair. Use this editable block for target-approved commercial and residential service copy.</p>",
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="commercial_title",
            field=models.CharField(
                blank=True,
                default="Commercial & Residential Appliance Repair",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="faq_heading",
            field=models.CharField(
                blank=True,
                default="Frequently Asked Questions",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="hero_subtitle",
            field=models.TextField(
                blank=True,
                default="Professional appliance repair for refrigerators, washers, dryers, dishwashers, and ovens. Same-day service with certified technicians and warranty on all repairs.",
                help_text="Intro text shown under the homepage H1.",
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="hero_title",
            field=models.CharField(
                blank=True,
                default="Same-Day Appliance Repair",
                help_text="Main homepage H1. Leave blank to use the translated fallback.",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="pricing_heading",
            field=models.CharField(
                blank=True,
                default="How Much Does Appliance Repair Cost?",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="pricing_note",
            field=models.TextField(
                blank=True,
                default="Final cost depends on the appliance type, specific issue, and replacement parts required. Use this editable note for approved pricing language.",
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="process_heading",
            field=models.CharField(
                blank=True,
                default="How to Book Appliance Repair",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="process_subheading",
            field=models.TextField(
                blank=True,
                default="From booking to a finished repair, keep this process copy editable so later content phases can use target-approved wording.",
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="services_heading",
            field=models.CharField(
                blank=True,
                default="What Appliances Do We Repair?",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="homepage",
            name="testimonials_heading",
            field=models.CharField(
                blank=True,
                default="What Our Customers Say",
                max_length=255,
            ),
        ),
    ]
