from django.http import HttpResponse

# Create your views here.
def recv_sms(request):
    return HttpResponse("<Sms>Thanks</Sms>")
