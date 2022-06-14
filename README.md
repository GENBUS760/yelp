# Yelp Dataset MySQL Import

1. Download and extract the [Yelp dataset JSON files](https://yelp.com/dataset/) into the same folder as this repository.
2. Start your MySQL server.
3. Create and activate a new database called `yelp`: `CREATE DATABASE yelp; USE yelp;`.
4. Modify `models.py` with the username and password to connect to your database.
5. Run the import scripts:

```
python json_to_mysql.py reset # clears tables
python json_to_mysql.py business
python json_to_mysql.py user
python json_to_mysql.py review
```
