from django.shortcuts import render, redirect
from django.views import View

from lawyer.forms import ApplicationForm
from lawyer.models import ContactInformation, ContactNumber

contacts = ContactNumber.objects.all()


def get_whatsapp_number():
    instance = ContactNumber.objects.filter(whatsapp=True).first()
    if instance:
        return instance.number.replace(" ", "")
    return None


class HomeView(View):
    def get(self, request, *args, **kwargs):
        contact_info = ContactInformation.objects.filter(language__name="Русский").first()
        return render(request, 'index.html',
                      context={"contact_info": contact_info, "contacts": contacts,
                               "whatsapp_number": get_whatsapp_number})

    def post(self, request, *args, **kwargs):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("success")
        return render(request, 'index.html', {'form': form})


class SuccessPageView(View):
    def get(self, request, *args, **kwargs):
        contact_info = ContactInformation.objects.filter(language__name="Русский").first()
        return render(request, "success.html", context={"contact_info": contact_info,
                                                        "contacts": contacts, "whatsapp_number": get_whatsapp_number})


class HomeEnView(View):
    def get(self, request, *args, **kwargs):
        contact_info = ContactInformation.objects.filter(language__name="Английский").first()
        return render(request, "home-en.html", context={"contact_info": contact_info,
                                                        "contacts": contacts, "whatsapp_number": get_whatsapp_number})

    def post(self, request, *args, **kwargs):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("success-en")
        return render(request, 'index.html', {'form': form})


class SuccessPageEnView(View):
    def get(self, request, *args, **kwargs):
        contact_info = ContactInformation.objects.filter(language__name="Английский").first()
        return render(request, "success-en.html", context={"contact_info": contact_info,
                                                           "contacts": contacts,
                                                           "whatsapp_number": get_whatsapp_number})


class HomeCnView(View):
    def get(self, request, *args, **kwargs):
        contact_info = ContactInformation.objects.filter(language__name="Китайский").first()
        return render(request, "home-cn.html", context={"contact_info": contact_info,
                                                        "contacts": contacts, "whatsapp_number": get_whatsapp_number})

    def post(self, request, *args, **kwargs):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("success-cn")
        return render(request, 'index.html', {'form': form})


class SuccessPageCnView(View):
    def get(self, request, *args, **kwargs):
        contact_info = ContactInformation.objects.filter(language__name="Китайский").first()
        return render(request, "success-cn.html", context={"contact_info": contact_info,
                                                           "contacts": contacts,
                                                           "whatsapp_number": get_whatsapp_number})
