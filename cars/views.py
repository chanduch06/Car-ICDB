"""Views for the cars app."""
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from cars.models import Car
from cars.forms import CarForm

from django.views.generic import View


class CarView(View):
  """A view for cars."""
  http_method_names = ['get', 'post', 'put', 'delete']

  def get(self, request):
    """GET returns a list of objects.

    Args:
        request : Httprequest
        make: string
    Returns:
        HttpResponse
    """
    if request.GET.get('make'):
        cars = Car.objects.filter(make=request.GET.get('make')).values()
    else:
        cars = Car.objects.all()
    return render_to_response('cars.json', {'cars': cars},
                                  mimetype='application/json')

  def post(self, request):
      """Adding a car POST method
       Args:
        request : Httprequest
      Returns:
        HttpResponse
      """
      try:
        data = json.loads(request.body)
      except ValueError:
        return HttpResponseBadRequest('Not valid JSON!')

      form = CarForm(data)

      if form.is_valid():
        car = form.save()
        response = HttpResponse(status=201)
        response['Location'] = '/cars/' + str(car.id)
        return response
      else:
        return HttpResponseBadRequest('Invalid data!')

  def put(self, request):
    """updating a car through PUT METHOD
    Args:
        request : Httprequest
    Returns:
        HttpResponse
    """
    try:
        data = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest('Not valid JSON!')

    get_id = Car.objects.get(id=data.get('id'))
    form = CarForm(data, instance=get_id)
    if form.is_valid():
        form.save()
        response = HttpResponse(status=200)
        return response
    else:
        return HttpResponseBadRequest('Invalid data!')

  def delete(self, request):
    """deleting a car through DELETE METHOD.

    Args:
        request : Httprequest
    Returns:
        HttpResponse
    """
    try:
        data = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest('Not valid JSON!')
    Car.objects.filter(id=data.get('id')).delete()
    response = HttpResponse(status=202)
    return response
