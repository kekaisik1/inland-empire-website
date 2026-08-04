# Generated target-natively for Inland Empire Phase 02 on 2026-07-31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0003_add_city_featured_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="citypage",
            name="public_h1",
            field=models.CharField(
                blank=True,
                help_text="Optional public H1/hero heading. Leave blank to use the default city SEO heading so navigation and menus keep using the page title.",
                max_length=255,
            ),
        ),
    ]
