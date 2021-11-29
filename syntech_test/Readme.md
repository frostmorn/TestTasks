# Syntech test task

Table reservation

## Install dependencies:

```
    python -m pip install -r requirements.txt
```

## Test credintails:

* Username:   ``root``
* Mail:       ``root@example.com``
* Password:   ``somekindofpass``
## Models:

* ``Hall`` - Represents hall where tables r placed
* ``Table`` - Represents tables in ``hall`` which used in ``Order``
* ``Order`` - Represents data such as reserved tables, user data, etc.
    ``is_paid`` field used to understand which orders used only for 
    table reservation purposes

REST API:
    hostname:hostport/table_orders/

You could reserve table by sending request to hostname:hostport/table_orders/orders
