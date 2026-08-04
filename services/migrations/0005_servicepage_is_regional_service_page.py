from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0004_service_photo_carousel_foundation"),
    ]

    operations = [
        migrations.AddField(
            model_name="servicepage",
            name="is_regional_service_page",
            field=models.BooleanField(
                default=False,
                help_text=(
                    "Marks SEO service pages created for a specific city. Regional "
                    "pages are published manually and intentionally excluded from "
                    "service menus."
                ),
            ),
        ),
    ]
