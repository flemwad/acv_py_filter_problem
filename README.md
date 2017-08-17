# The Goal: 


1. One function should return an array of userId's based off a JSON vehicle object specification
1. The other function should return void and map a userId to a JSON user filter object specification
1. Humans should be able to read it
1. Clean and concise comments, also some helpful references/links
1. Big O Time Complexity for my functions
1. Tests - Taking this opportunity to expand my TDD skill set
1. Mention something about potential race conditions

---

**schema**
```javascript
{
    'make': 'Chevrolet',
    'model': 'Camaro',
    'year': 2014,
    'trim': 'SS 1LE',
    'transmission_type': 'manual',
    'type': 'sports car'
}
```

**example user filter**
```javascript
{
    'year': [2017, 2016],
    'make': ['Chevrolet', 'Jeep'],
    'type': 'truck'
}
```

**Found like:**
`where (year is 2017 or year is 2016) and (make is 'Chevrolet' OR make is 'Jeep')` ...

---

### Time spent: 
* About 2-3 hours setting up Visual Studio Code with Python. Reading and learning about Python, TDD, and how/what to import to acheive that minimally, writing this doc. This was my first delve into Python
* I spent about half an hour setting up failing tests, and creating json objects/researching factoryboy and Faker
* I spent about an hour on the actual implementation of each function to fix first two simple tests
* Proabably an additional 15 to 20 minutes expanding the tests from there to include edge cases and the private function

### Design:
* Storing the user_id_filters on the Class constructor, as to reduce race conditions, can be initialized via constructor
* store_filters_for_user simply sets the user_id and user_filter_spec on the Classes user_id_filters dict
* Created a dict users_to_notify of the user_id key mapped to whether or not it should be returned in the list
* Using dict.get and list.index where possible
* Using reduce to grab just they user_ids who end with a True value 

### Runtime:
* Best case should be O(n^2) as you must loop through each user, and then each user filter at every pass
* Average case should be O(n^2) when the .index scan on the user_id_filter returns early
* Worst case would be O(n^3) when the .index scan must traverse the entire list
* I believe this may be able to be improved to O(n log n) with Sorted Lists, calling .sorted on dicts and then

### Potential Race Conditions:
* Should be none, but I could be wrong 
* Dictionaries used are contextual to Class constructor and each function
* I'm not referncing any globally scoped class variables

---

**My thoughts:**
* Awesome primer for Python for me, realize there's a lot for me to learn
* I need to brush up on my Performance knowledge
* I've written Android projects in Java in the past so I wanted to try something new. Also to get excited about the stack. 
* Really interested to see what design patterns have been implemented on the ACV project itself


**Things I would do better next time:**
1. Learn Python sooner...
1. Use factoryboy & Faker to mock my userIds and filters
1. Delve deeper and see or get my hands on production ready Python unit tests
1. Learn more about abstract classes, factories, what's preferred in the community and such

---

**Resources Used:**

https://docs.python.org/3.6/index.html

https://docs.python.org/3/tutorial/datastructures.html

https://docs.python.org/3/tutorial/datastructures.html#dictionaries

https://docs.python.org/3.6/tutorial/

http://docs.python-guide.org/en/latest/dev/virtualenvs/

http://nose.readthedocs.io/en/latest/testing.html

http://book.pythontips.com/en/latest/map_filter.html

https://wiki.python.org/moin/TimeComplexity

http://docs.python-guide.org/en/latest/dev/virtualenvs/

https://stackoverflow.com/

---

## To Run

`pip install virtualenv`

`virtualenv acv_user_filter`

`pip install -r requirements.txt`

`nosetests`

---

Thanks to [ACV Auction](https://github.com/acv-auctions) for the opportunity and cool interview