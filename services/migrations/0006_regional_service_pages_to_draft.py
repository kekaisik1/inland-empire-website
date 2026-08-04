from django.db import migrations, models


def move_existing_regional_pages_to_draft(apps, schema_editor):
    ServicePage = apps.get_model("services", "ServicePage")
    Page = apps.get_model("wagtailcore", "Page")

    regional_page_ids = ServicePage.objects.filter(
        is_regional_service_page=True
    ).values_list("page_ptr_id", flat=True)
    Page.objects.filter(pk__in=regional_page_ids).update(
        live=False,
        has_unpublished_changes=True,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0005_servicepage_is_regional_service_page"),
    ]

    operations = [
        migrations.AlterField(
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
        migrations.RunPython(
            move_existing_regional_pages_to_draft,
            migrations.RunPython.noop,
        ),
    ]
