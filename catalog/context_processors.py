from . import models

def catalog_processor(request):
    context = {}

    if "vendor" in request.session:
        vendor = models.Vendor.objects.get(pk=request.session["vendor"])
        context["vendor"] = vendor
    
    if "user" in request.session:
        user = models.User.objects.get(pk=request.session["user"])
        context["sh_user"] = user

    return context