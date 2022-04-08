### About the app
This simple restaurant app handles authentication and restaurant data with the help of the AWS Cloud. This app is based on a serverless architecture. Its functioning involves the use of lambdas and AWS Api Gateway to access them and for data management it uses DynamoDB. To avoid complexity in the development environment to run the project, flask it's being used to replace the api gateway locally.

### Initiating development environment
The app uses `poetry` for its development environment, to configure it you need to execute the following commands:
1. Install poetry with pip 
```
    pip3 install poetry
```
2. Install app dependencies (from the root folder of the project)
```
    poetry install
```
3. Activate and get into poetry venvironment:
```
    poetry shell
```

Note: If the command `poetry` doesn't work, you can use `python3 -m poetry`.



### Configuring tables and parameters
To use the app locally, you still need to configure a DynamoDB table and some SystemManager secure parameters. To configure your tables you must go into your own AWS account's management console. Then go through the following steps. 
1. Go into `DynamoDB` service
2. Go into `Tables`
3. Create table (For Restaurants table)
    - Set any table name (You will need to use it on your environment as mentioned)
    - Set the partition key as `id`
    - Execute Create
4. Create table (For Users table)
    - Set any table name (You will need to use it on your environment as mentioned)
    - Set the partition key as `email`
    - Execute Create


Now, to configure the required secure parameters, on the management console do as follows:
0. Before following steps on the management console, you need to have 2 keys ready.
    - For `password encryption key`, execute the file `password_key.py` in the root folder of the project and save the returned key for later.
    - For the token key, execute the file `token__key.py` in the root folder of the project and save the returned key for later.
    - You can execute the files with the command 
    ```
        python3 <file_name>
    ```

1. Go into `SystemManager` tool
2. Under `ApplicationManager` go into `Parameter Store`
3. Go into `Create parameter`
4. Create parameter (For password encryption key)
    - Set any parameter name (You will need to use it on your environment as mentioned)
    - Set Type as `SecureString`
    - Set Value as the `password encryption key` you saved
    - Leave everything else by default 
    - Execute Create parameter
5. Create parameter (For token key)
    - Set any parameter name (You will need to use it on your environment as mentioned)
    - Set Type as `SecureString`
    - Set Value as the `token key` you saved
    - Leave everything else by default 
    - Execute Create parameter

#### Populating Tables
For using already generated data, use the following command on the root folder of the project.
```
    python3 populate.py
```


### Environment variables to configure
The variables you need to export to your local environment are as follow: 
- RESTAURANT_TABLE_NAME=<restaurant_table_name>
- USERS_TABLE_NAME=<users_table_name>
- PASSWORD_SECURE_PATH=<password_encryption_key_parameter_name>
- TOKEN_SECRET_KEY=<token_secret_key_parameter_name>

For simplicity, you can set these values on the `.env` file located on the root folder of this project. Then run the following command:
```
    source .env
```

### Running the app
After configuring the resources and environmental variables, execute the following command on the root folder 
```
    python3 main.py
```

The app should be up and running locally! To use it you can import the postman collection called `RestaurantApp.postman_collection.json` on postman.


Cheers!