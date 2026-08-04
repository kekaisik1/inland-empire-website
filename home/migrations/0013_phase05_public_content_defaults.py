from django.db import migrations, models
import wagtail.fields


OLD_COMMERCIAL_BODY = (
    "<p>Commercial kitchens and homes both need dependable appliance repair. "
    "Use this editable block for target-approved commercial and residential "
    "service copy.</p>"
)
NEW_COMMERCIAL_BODY = (
    "<p>We repair household and light-commercial refrigerators, freezers, washers, "
    "dryers, dishwashers, ovens, and related appliances across the Inland Empire.</p>"
    "<p>Service begins with an on-site diagnosis. Before work starts, the technician "
    "explains the issue, available repair options, and the price for approval.</p>"
)
OLD_PROCESS_SUBHEADING = (
    "From booking to a finished repair, keep this process copy editable so later "
    "content phases can use target-approved wording."
)
NEW_PROCESS_SUBHEADING = (
    "Choose a service, confirm your service area, and schedule a visit. We diagnose "
    "the appliance before you approve any repair."
)
OLD_PRICING_NOTE = (
    "Final cost depends on the appliance type, specific issue, and replacement parts "
    "required. Use this editable note for approved pricing language."
)
NEW_PRICING_NOTE = (
    "Your final price depends on the appliance, the fault, and required parts. The "
    "technician confirms the repair price before work begins."
)
OLD_BRANDS_SUBHEADING = (
    "Use this editable copy for manufacturer and brand capability language after "
    "claims are reviewed."
)
NEW_BRANDS_SUBHEADING = (
    "We service common household and premium appliance brands. Select a linked brand "
    "for details, or call to confirm your model."
)
OLD_AREAS_SUBHEADING = (
    "Use this editable copy for reviewed Inland Empire service-area coverage and "
    "ZIP-code messaging."
)
NEW_AREAS_SUBHEADING = (
    "Serving homes and businesses across Corona, Riverside, and surrounding Inland "
    "Empire communities. Enter your ZIP code to confirm coverage."
)


def repair_legacy_phase05_content(apps, schema_editor):
    """Replace only known source/editorial defaults; preserve editor-owned values."""
    SiteSettings = apps.get_model("home", "SiteSettings")
    HomePage = apps.get_model("home", "HomePage")

    SiteSettings.objects.filter(
        business_name__in=("LOWL Appliance Repair", "LOWL Inland Repair")
    ).update(business_name="Inland Empire Appliance Repair")
    SiteSettings.objects.filter(booking_url__icontains="lowl").update(booking_url="")
    SiteSettings.objects.filter(booking_source__iexact="lowl").update(
        booking_source="inland"
    )

    replacements = (
        ("commercial_body", OLD_COMMERCIAL_BODY, NEW_COMMERCIAL_BODY),
        ("process_subheading", OLD_PROCESS_SUBHEADING, NEW_PROCESS_SUBHEADING),
        ("pricing_note", OLD_PRICING_NOTE, NEW_PRICING_NOTE),
        ("brands_subheading", OLD_BRANDS_SUBHEADING, NEW_BRANDS_SUBHEADING),
        ("areas_subheading", OLD_AREAS_SUBHEADING, NEW_AREAS_SUBHEADING),
    )
    for field, old_value, new_value in replacements:
        HomePage.objects.filter(**{field: old_value}).update(**{field: new_value})


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0012_sitesettings_navigation_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homepage",
            name="commercial_body",
            field=wagtail.fields.RichTextField(
                blank=True,
                default=NEW_COMMERCIAL_BODY,
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="process_subheading",
            field=models.TextField(
                blank=True,
                default=NEW_PROCESS_SUBHEADING,
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="pricing_note",
            field=models.TextField(
                blank=True,
                default=NEW_PRICING_NOTE,
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="brands_subheading",
            field=models.TextField(
                blank=True,
                default=NEW_BRANDS_SUBHEADING,
            ),
        ),
        migrations.AlterField(
            model_name="homepage",
            name="areas_subheading",
            field=models.TextField(
                blank=True,
                default=NEW_AREAS_SUBHEADING,
            ),
        ),
        migrations.RunPython(
            repair_legacy_phase05_content,
            migrations.RunPython.noop,
        ),
    ]
