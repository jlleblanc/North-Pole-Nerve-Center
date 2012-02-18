from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from twilio import twiml


@csrf_exempt
def recv_sms(request):
    if request.POST:
        sms_body = request.POST.get('Body', '')
        if " " in sms_body:
            action, arguments = sms_body.split(' ', 1)
        else:
            action = sms_body
            arguments = ""
        handler = sms_handles.get(action, DEFAULT_HANDLER)
        twiml_response = twiml.Response()
        twiml_response.sms(handler(arguments))
        return HttpResponse(str(twiml_response))
    else:
        return HttpResponse("gotta post, man")


def handle_help(rest):
    return "Commands are: buy <name> <number>, list <name>, who"


def handle_buy(rest):
    return "you bought %s" % rest


def handle_list(rest):
    return "listing stuff..."


def handle_who(rest):
    users = User.objects.all()
    names = [user.username for user in users]
    return "\n".join(names)


sms_handles = {
    'buy': handle_buy,
    'list': handle_list,
    'help': handle_help,
    'who': handle_who
}
DEFAULT_HANDLER = handle_help

