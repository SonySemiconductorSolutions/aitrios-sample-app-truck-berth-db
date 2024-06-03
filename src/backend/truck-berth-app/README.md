# Truck Berth DB Application

_**Note:**_ This Application can only run on one environment. So, all the below steps are recommended to be executed in one environment only.

## Prerequisites

- Use Windows OS 10
- Install `MongodDB` v7.0.5 for windows.
  https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/
- Install `Redis-x64-3.0.504.msi` from below link.
  https://github.com/microsoftarchive/redis/releases/download/win-3.0.504/Redis-x64-3.0.504.msi
  For Installation steps Refer https://kasunprageethdissanayake.medium.com/installing-redis-x64-3-2-100-on-windows-and-running-redis-server-94db3a98ae3d
- Install python >=3.9

## Install `MongoDB`

- Open https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/#install-mongodb-community-edition in Browser

- Click "**MongoDB Download Center**"<br/>
  <img src="..\..\..\docs\user_guide\mongo_db_imgs\install\1.png">

- Click [**Select package**]<br/>
  <img src="..\..\..\docs\user_guide\mongo_db_imgs\install\2.png">

- Select latest version `7.0.5` and Click [**Download**]<br/>
  <img src="..\..\..\docs\user_guide\mongo_db_imgs\install\3.png">

- Open Downloaded file and click [**Next**]<br/>
  <img src="..\..\..\docs\user_guide\mongo_db_imgs\install\4.png">

- "**Accept the license agreement**" and Click [**Next**]<br/>
  <img src="..\..\..\docs\user_guide\mongo_db_imgs\install\5.png">

- Click [**Complete**]<br/>
  <img src="..\..\..\docs\user_guide\mongo_db_imgs\install\6.png">

- Select "**Install MongoDB as Service**" and click [**Next**]<br/>
  <img src="..\..\..\docs\user_guide\mongo_db_imgs\install\7.png">

- Select "**Install MongoDB Compass**" and Click [**Next**]<br/>
  <img src="..\..\..\docs\user_guide\mongo_db_imgs\install\8.png">

- Click [**Install**]<br/>
  <img src="..\..\..\docs\user_guide\mongo_db_imgs\install\9.png">

## Setup Database

- Open `MongoDB Compass` app on windows and click on [**connect**].<br/>
  <img src="..\..\..\docs\user_guide\mongo_db_imgs\connect_mongo_db.PNG">

- Click [**+**] to add new Database.<br/>
  <img src="..\..\..\docs\user_guide\mongo_db_imgs\add_db.PNG">

- In "**Create Database**" enter "**Database Name**" as `truckberthapp` and "**Collection Name**" as `reservation_data` and click [**Create Database**] button.<br/>
  <img src="..\..\..\docs\user_guide\mongo_db_imgs\create_db.PNG">

- Click "**truckberthapp**" and confirm that `reservation_data` collection is created.<br/>
  <img src="..\..\..\docs\user_guide\mongo_db_imgs\db_complete.PNG">

## Setup environment

- Create a new virtual environment (Terminal 1)
  ```shell
  # Terminal 1
  python -m venv myenv
  .\myenv\Scripts\activate
  ```
- Create a database `truckberthapp`.
- Install python dependencies
  ```shell
  # Terminal 1
  pip install -r requirements.txt
  ```
- Copy the `truck_berth_backend_settings.yaml` to `src\backend\truck-berth-app\src\data`
  ```yaml
  truck_berth_backend_settings:
    console_endpoint: "__console_endpoint__"
    portal_authorization_endpoint: "__portal_authorization_endpoint__"
    client_secret: "__client_secret__"
    client_id: "__client_id__"
    mail_notification: false
    sendgrid_api_key: "__sendgrid_api_key__"
    sendgrid_api_endpoint: "__sendgrid_api_endpoint__"
    from_email: "__from_email__"
    email_subject: "__email_subject__"
    notifier_email_list: ["__notifier_email_list__"]
  ```
- Create `src\backend\truck-berth-app\src\data\berth_device_map.json`
  ```json
  {
    "B1": {
      "device_id": "__device_id__", //Provide the valid device id
      "inference_status": "start" //"start" if the model inference is started else "stop"
    }
  }
  ```

## Run the application

- Start the Flask Application (Terminal 1)
  ```shell
  # Terminal 1
  set REDIS_URL=redis://localhost:6379/0
  set MONGO_DB_URI=mongodb://localhost:27017
  cd src\backend\truck-berth-app\src
  python app.py
  ```
  _**Note:**_ 
  - To use cloud Mongo DB, replace `MONGO_DB_URI` with cloud Mongo DB URI.
  - The log files will be generated under the root folder as `app.log` file.
- Start the celery worker (Terminal 2)
  ```shell
  # Terminal 2
  .\myenv\Scripts\activate
  cd src\backend\truck-berth-app\src
  set REDIS_URL=redis://localhost:6379/0
  set MONGO_DB_URI=mongodb://localhost:27017
  celery -A app.celery worker --pool=solo --loglevel=info
  ```
  _**Note:**_ The log files will be generated under the root folder as `model_inference.log` file.
- Start the celery beat (Terminal 3)
  ```shell
  # Terminal 3
  .\myenv\Scripts\activate
  cd src\backend\truck-berth-app\src
  set REDIS_URL=redis://localhost:6379/0
  set MONGO_DB_URI=mongodb://localhost:27017
  celery -A app.celery beat --loglevel=info
  ```
