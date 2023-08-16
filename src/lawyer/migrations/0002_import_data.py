from django.db import migrations

languages = [{"name": "Русский"}, {"name": "Английский"}, {"name": "Китайский"}]
phone_numbers = [{"number": "0312 66 35 10"}, {"number": "0772 50 85 93"}, {"number": "0559 50 85 93"},
                 {"number": "0772 50 85 93", "whatsapp": True}]
contact_informations = [{"language_id": 1, "email": "hedefdva@gmail.com",
                         "address": "Кыргызская Республика г. Бишкек, ул. Абдырахманова 166, каб. 58"},
                        {"language_id": 2, "email": "hedefdva@gmail.com",
                         "address": "Kyrgyz Republic, Bishkek city, 166 Abdrakhmanov St., office 58"},
                        {"language_id": 3, "email": "hedefdva@gmail.com",
                         "address": "吉尔吉斯共和国，比什凯克,Abdrakhmanov 街 166 号，办公室 58 "}]


def import_data(app, _):
    Language = app.get_model("lawyer", "Language")
    ContactNumber = app.get_model("lawyer", "ContactNumber")
    ContactInformation = app.get_model("lawyer", "ContactInformation")

    for language in languages:
        Language.objects.create(name=language["name"])
    for phone_number in phone_numbers:
        ContactNumber.objects.create(number=phone_number["number"], whatsapp=phone_number.get("whatsapp", False))
    for contact_information in contact_informations:
        ContactInformation.objects.create(language_id=contact_information["language_id"],
                                          email=contact_information["email"],
                                          address=contact_information["address"])


class Migration(migrations.Migration):
    dependencies = [
        ("lawyer", "0001_initial"),
    ]

    operations = [migrations.RunPython(import_data, migrations.RunPython.noop)]
