import unittest
from nose.tools import nottest
from vehicle_user_utils import VehicleUserUtils

class TestVehicleUserUtils(unittest.TestCase):
    """
        TestVehicleUserUtils is a unit testing class for the VehicleUserUtils class
    """

    def setUp(self):

        # TODO: do this with factoryboy and Faker in the future 
        # so we could do something nice like UserFilterFactory(...)
        self.utils = VehicleUserUtils({
            'flem': {
                'make': ['Toyota', 'Subaru'],
                'model': ['Corolla', 'Impreza'], 
                'year': [2010, 2011], 
                'transmission_type': 'automatic', 
                'type': ['sedan', 'sports car']
            },
            'kaliegh': {
                'make': 'Toyota', 
                'year': 2010, 
                'transmission_type': 'automatic'
            },
            'sara': {
                'year': [2016, 2017], 
                'make': 'Dodge',
                'type': 'Truck',
                'trim': ['LE', 'SE'],
                'transmission_type': 'automatic'
            },
            'kirby': {
                'year': 2017, 
                'type': 'sedan', 
                'transmission_type': ['automatic', 'manual']
            }
        })

    
    def test_stores_filter_for_userId(self):
        inserted_filter = {
            'year': [2017, 2016],
            'make': ['Chevrolet', 'Jeep'],
            'type': 'truck'
        }

        self.utils.store_filters_for_user('joe', inserted_filter)
        self.assertDictContainsSubset({'joe': inserted_filter}, self.utils.user_id_filters) 

    
    def test_returns_one_user_id_named_sara(self):
        actual_user_ids = self.utils.get_user_ids_to_notifty({
            'make': 'Dodge',
            'model': 'Caravan',
            'year': 2016,
            'trim': 'LE',
            'transmission_type': 'automatic',
            'type': 'Truck'
        })

        self.assertIn('sara', actual_user_ids)
        self.assertEqual(len(actual_user_ids), 1)

    
    def test_returns_two_user_ids_named_flem_and_kaliegh(self):
        actual_user_ids = self.utils.get_user_ids_to_notifty({
            'make': 'Toyota',
            'model': 'Corolla',
            'year': 2010,
            'trim': 'LE',
            'transmission_type': 'automatic',
            'type': 'sedan'
        })

        self.assertIn('flem', actual_user_ids)
        self.assertIn('kaliegh', actual_user_ids)
        self.assertEqual(len(actual_user_ids), 2)

    
    def test_returns_all_users_with_manual_transmission_type(self):
        similar_user_filter_utils = VehicleUserUtils({
            'flem': {
                'year': 2017, 
                'type': 'sedan', 
                'transmission_type': ['automatic', 'manual']
            },
            'kaliegh': {
                'year': 2017, 
                'type': 'sedan', 
                'transmission_type': ['automatic', 'manual']
            },
            'sara': {
                'year': 2017, 
                'type': 'sedan', 
                'transmission_type': ['automatic', 'manual']
            },
            'kirby': {
                'year': 2017, 
                'type': 'sedan', 
                'transmission_type': ['automatic', 'manual']
            }
        })

        actual_automatic_user_ids = similar_user_filter_utils.get_user_ids_to_notifty({
            'make': 'Toyota',
            'model': 'Corolla',
            'year': 2017,
            'trim': 'LE',
            'transmission_type': 'manual',
            'type': 'sedan'
        })

        self.assertIn('flem', actual_automatic_user_ids)
        self.assertIn('kaliegh', actual_automatic_user_ids)
        self.assertIn('sara', actual_automatic_user_ids)
        self.assertIn('kirby', actual_automatic_user_ids)
        self.assertEqual(len(actual_automatic_user_ids), 4)


    def test_returns_all_users_with_automatic_transmission_type(self):
        similar_user_filter_utils = VehicleUserUtils({
            'flem': {
                'year': 2017, 
                'type': 'sedan', 
                'transmission_type': ['automatic', 'manual']
            },
            'kaliegh': {
                'year': 2017, 
                'type': 'sedan', 
                'transmission_type': ['automatic', 'manual']
            },
            'sara': {
                'year': 2017, 
                'type': 'sedan', 
                'transmission_type': ['automatic', 'manual']
            },
            'kirby': {
                'year': 2017, 
                'type': 'sedan', 
                'transmission_type': ['automatic', 'manual']
            }
        })

        actual_manual_user_ids = similar_user_filter_utils.get_user_ids_to_notifty({
            'make': 'Subaru',
            'model': 'WRX',
            'year': 2017,
            'trim': 'SE',
            'transmission_type': 'manual',
            'type': 'sedan'
        })

        self.assertIn('flem', actual_manual_user_ids)
        self.assertIn('kaliegh', actual_manual_user_ids)
        self.assertIn('sara', actual_manual_user_ids)
        self.assertIn('kirby', actual_manual_user_ids)
        self.assertEqual(len(actual_manual_user_ids), 4)

    def test_returns_True_when_user_should_be_notified(self):
        user_id_filter = {
            'year': 2017, 
            'type': 'sedan', 
            'transmission_type': ['automatic', 'manual']
        }

        result = self.utils.should_notify_user({
            'make': 'Subaru',
            'model': 'WRX',
            'year': 2017,
            'trim': 'SE',
            'transmission_type': 'manual',
            'type': 'sedan'
        }, user_id_filter)

        self.assertTrue(result)

    def test_returns_False_user_should_not_be_notified(self):
        user_id_filter = {
            'year': 2017, 
            'type': 'sedan', 
            'transmission_type': ['automatic', 'manual']
        }

        result = self.utils.should_notify_user({
            'make': 'Subaru',
            'model': 'WRX',
            'year': 2017,
            'trim': 'SE',
            'transmission_type': 'manual',
            'type': 'truck'
        }, user_id_filter)

        self.assertEqual(result, False)
