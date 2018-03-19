NPS Dashboard

1. Install packages
    ```
    $ pip install -r requirements.txt
    ```
2. Set up database in dashboard/settings.py
    - The default is a sqllite db - if you want to use this you don't need to change anything

3. Run DB migrations
    ```
    $ python manage.py migrate
    ```
4. Create a superuser
    ```
    $ python manage.py createsuperuser
    ```
5. Run the Django server
    ```
    $ python manage.py runserver
    ```
6. Log into the Django admin panel and import data into the Nps/Raw Results table and the Nps/Products table
    - You can modify/use the following script to prep your files for import
     ```
    $ python manage.py convert_file {input_file} {output_file} new
    ```
7. Update the global variables in the aggregation scripts and run the scripts
   ```
    $ python manage.py calculate_nps
    $ python manage.py calculate_nps_product
    $ python manage.py calculate_client_deltas
    ```
8. Run the React Server
   ```
    $ cd frontend
    $ npm install
    $ npm start
    ```
    
You're ready to go!

![Alt text](/images/survey_comparisons.png?raw=true "Survey Comparisons")
![Alt text](/images/client_comparisons.png?raw=true "Client Comparisons")
    
