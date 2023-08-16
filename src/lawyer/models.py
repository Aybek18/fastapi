from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=40, verbose_name="Язык")

    def __str__(self):
        return self.name


class ContactNumber(models.Model):
    number = models.CharField(max_length=20, verbose_name="Номер телефона")
    whatsapp = models.BooleanField(verbose_name="Whatsapp", default=False)

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = "Номер телефона"
        verbose_name_plural = "Номера телефона"


class ContactInformation(models.Model):
    language = models.ForeignKey(Language, verbose_name="Язык информации", on_delete=models.PROTECT)
    email = models.CharField(max_length=40, verbose_name="Почта")
    address = models.CharField(max_length=150, verbose_name="Адрес")

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактные информации"


class Application(models.Model):
    created_at = models.DateTimeField(auto_now=True, verbose_name="Дата создания заявки")
    name = models.CharField(max_length=50, verbose_name="Имя клиента")
    email = models.CharField(max_length=40, verbose_name="Почта клиента")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона клиента")
    date = models.DateField(verbose_name="Дата встречи")
    comment = models.TextField(verbose_name="Комментарий от клиента")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
