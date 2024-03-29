"""
Tests for the cars app.
"""
from django.test import TestCase
import mock
from django.utils import simplejson as json
from cars.models import Car
from cars.views import CarView
from cars.forms import CarForm


class TestCar(TestCase):
    """Tests for the Car model."""
    def test_car(self):
        """Test the Car model."""
        car = Car()
        car.make = 'Make'
        car.model = 'Model'
        car.year = 1999

        car.save()


class TestCarForm(TestCase):
    """Tests for the car form."""
    def test_form(self):
        """Test that the form is attached to the right model."""
        self.assertIs(CarForm._meta.model, Car, 'Should be attached to Car.')


class TestIndexView(TestCase):
    """Tests for the cars.cars_view view."""
    @mock.patch('cars.views.CarForm')
    def test_post(self, MockCarForm):
        """Test a POST request to the cars_view view."""
        obj = {'make': 'Toyota', 'model': 'Camry', 'year': 2001}
        request = mock.Mock(
            method='POST',
            body=json.dumps(obj)
        )
        mock_form = MockCarForm.return_value
        mock_car = mock_form.save.return_value
        mock_car.id = 123

        response = CarView.as_view()(request)

        self.assertEqual(response.status_code, 201,
                         'Should return 201 CREATED.')
        self.assertEqual(response['Location'], '/cars/123',
                         'Should return the location of the new car.')
        MockCarForm.assert_called_with(obj)
        self.assertTrue(mock_form.save.called, 'Should call save.')

    def test_post_invalid_data(self):
        """Test POSTing invalid data."""
        request = mock.Mock(
            method='POST',
            body='{}'
        )
        cars_view = CarView.as_view()
        response = cars_view(request)

        self.assertEqual(response.status_code, 400,
                         'Should return a 400 BAD REQUEST.')

    def test_post_bad_json(self):
        """Test POSTing invalid JSON."""
        request = mock.Mock(
            method='POST',
            body='foo'
        )
        cars_view = CarView.as_view()
        response = cars_view(request)

        self.assertEqual(response.status_code, 400,
                         'Should return a 400 BAD REQUEST.')

    @mock.patch('cars.views.Car')
    def test_get(self, MockCar):
        """Test GET requests to the cars_view view."""
        request = mock.Mock(method='GET')
        objs = [
            {'id': 1, 'make': 'Make1', 'model': 'Model1', 'year': 1},
            {'id': 2, 'make': 'Make2', 'model': 'Model2', 'year': 2},
            {'id': 3, 'make': 'Make3', 'model': 'Model3', 'year': 3},
        ]
        MockCar.objects.all.return_value = [Car(**obj) for obj in objs]
        response = CarView.as_view()(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200,
                         'Should return a successful response.')
        self.assertEqual(response['Content-Type'], 'application/json',
                         'Should return a JSON response.')
        #print data
        #self.assertSequenceEqual(data, objs, 'Should return the objects.')

    def test_not_supported(self):
        """Test sending an unsupported request method."""
        request = mock.Mock(method='FOO')
        cars_view = CarView.as_view()
        response = cars_view(request)

        self.assertEqual(response.status_code, 405,
                         'Should return a 405 NOT ALLOWED.')
        #self.assertIn('GET', response['Allow'], 'Should allow GET.')
        #self.assertIn('POST', response['Allow'], 'Should allow POST.')
