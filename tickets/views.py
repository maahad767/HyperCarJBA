from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect


line_of_cars = {
    'car_count': 0,
    'serve_next': None,
    'change_oil': [],
    'inflate_tires': [],
    'diagnostic': [],
}


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):

    def get(self, request):
        return render(request, 'tickets/menu.html')


class ChangeOilView(View):

    def get(self, request):
        waiting_time = len(line_of_cars['change_oil']) * 2

        context = {
            'ticket_number': line_of_cars['car_count'],
            'waiting_time': waiting_time,
        }
        line_of_cars['car_count'] += 1
        line_of_cars['change_oil'].append(line_of_cars['car_count'])
        return render(request, 'tickets/ticket.html', context)


class InflateTiresView(View):

    def get(self, request):
        waiting_time = len(line_of_cars['change_oil']) * 2 \
                       + len(line_of_cars['inflate_tires']) * 5

        context = {
            'ticket_number': line_of_cars['car_count'],
            'waiting_time': waiting_time,
        }
        line_of_cars['car_count'] += 1
        line_of_cars['inflate_tires'].append(line_of_cars['car_count'])
        return render(request, 'tickets/ticket.html', context)


class DiagnosticView(View):

    def get(self, request):
        waiting_time = len(line_of_cars['change_oil']) * 2 \
                       + len(line_of_cars['inflate_tires']) * 5 \
                       + len(line_of_cars['diagnostic']) * 30


        context = {
            'ticket_number': line_of_cars['car_count'],
            'waiting_time': waiting_time,
        }
        line_of_cars['car_count'] += 1
        line_of_cars['diagnostic'].append(line_of_cars['car_count'])

        return render(request, 'tickets/ticket.html', context)


class ProcessingView(View):

    def get(self, request):
        context = {
            'oil_change_queue': len(line_of_cars['change_oil']),
            'inflate_tires_queue': len(line_of_cars['inflate_tires']),
            'diagnostic_queue': len(line_of_cars['diagnostic']),
        }
        return render(request, 'tickets/processing.html', context)

    def post(self, request):

        if len(line_of_cars['change_oil']) > 0:
            line_of_cars['serve_next'] = line_of_cars['change_oil'].pop(0)
        elif len(line_of_cars['inflate_tires']) > 0:
            line_of_cars['serve_next'] = line_of_cars['inflate_tires'].pop(0)
        elif len(line_of_cars['diagnostic']) > 0:
            line_of_cars['serve_next'] = line_of_cars['diagnostic'].pop(0)

        return redirect('/next')


class NextView(View):

    def get(self, request):

        context = {
            'serve_next': line_of_cars['serve_next']
        }
        return render(request, 'tickets/next.html', context)
