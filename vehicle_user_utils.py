import functools
from binary_search import binary_search

class VehicleUserUtils:
    """
    Handles caching a user_id and its respective filters
    Handles returning what users_ids in the cache match a vehicle specification
    """

    def __init__(self, user_id_filters):
        self.user_id_filters = user_id_filters 

    # this could probably be a private fn, but i couldn't figure out how to access that in the test
    def should_notify_user(self, vehicle_spec, user_filters):
        """
        Given a vehicle_spec dict and a user's filter dict, figure out if the user filter matches
        """

        user_filter_match = True

        # we need to evaluate every user filter against the relevant vehicle_spec value
        # 0(1) on an early failure, O(n^2) now I'm pretty sure at worse case (True)
        for filter_key, filter_val in user_filters.items():
            # one of the ANDs was False we can return early speeding up the checks
            if user_filter_match is False:
                return False
            else:
                # Last vehicle spec matched a user filter, keep going
                vehicle_val = vehicle_spec.get(filter_key)

                # OR user filter values if the user's specific filter is an array of values
                if isinstance(filter_val, list):
                    # TODO is there a better way to short circuit this?
                    try:
                        # binary search here should reduce this to log n filter search time
                        # no sort needed since happens on insert
                        user_filter_match = binary_search(filter_val, vehicle_val)
                    except ValueError:
                        # user filter list value didn't contain the vehicle value
                        user_filter_match = False
                else:
                    # it wasn't a list so we can just compare the two values
                    user_filter_match = (filter_val == vehicle_val)

        return True


    def get_user_ids_to_notifty(self, vehicle_spec):
        """
        Given a vehicle_spec dict will return a list of users
        """

        # create an initial dict e.g. {'flem': True, 'kirby': True ...}
        users_to_notify = dict.fromkeys(self.user_id_filters.keys(), False)

        # for each user, run a function that will check to see if their filter matches the vehicle spec
        # adds O(n) time complexity here I believe
        for user_id, user_filters in self.user_id_filters.items():
            # AND our dict user_id value with the returned filtered value
            users_to_notify[user_id] = self.should_notify_user(vehicle_spec, user_filters)

        #the accumulation function, returning a mutated new array of user_ids
        def user_id_filter_match(user_ids, user_id):
            if users_to_notify.get(user_id) is True: 
                user_ids.append(user_id)
            return user_ids

        # a little less human readable, but a neat shorthand nonetheless
        # using initialized list [], loop through all the users to notify, and determine if they should be returned
        # couldn't figure out how to lambda here :(
        return functools.reduce(user_id_filter_match, users_to_notify.keys(), [])


    def store_filters_for_user(self, user_id, user_filter_spec):
        """
        Set the key user_id to value user_filter_spec on self.user_id_filters dict
        """
        #sort any array filter values so we can look them up in log n time later
        for filter_key, filter_val in user_filter_spec.items():
            if isinstance(filter_val, list):
                user_filter_spec[filter_key] = sorted(filter_val)
            
        self.user_id_filters[user_id] = user_filter_spec
        