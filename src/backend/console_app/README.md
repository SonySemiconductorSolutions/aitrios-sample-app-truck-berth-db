### Command Line Interface (CLI APP)

  - Prepare a CSV file for reservation data as below mentioned columns.
    - email_id: Truck Owner/Driver Email ID.
    - start_time: Truck Reservation Start time.
    - end_time: Truck Reservation End time.
    - berth_number: Berth Number of Truck parking lot.
    - car_number: Truck Registration Number.
    - status: By default use "reserved".

  - _**Note:**_
    - Please use Japanese "`・`" for dot character and only numbers for Truck registration number in the car_number column.
    - Use the dateformat as `dd-mm-yyyy HH:MM`
    
      Example of sample reservation data.
      <img src="..\..\..\docs\user_guide\ui_imgs\sample_reservation_data.png">

### Install and use

- Get into a virtual environment (Terminal 4)

  ```shell
  # Terminal 4
  .\myenv\Scripts\activate
  ```

- Install the package
  ```shell
  # Terminal 4
  pip install src\backend\console_app
  ```

  _**Note:**_ Make sure the backend service is started before you use the commands

- Set the backend URL

  ```shell
  # Terminal 4
  set TB_BACKEND_URL=http://localhost:5000
  ```

  _**Note:**_ By default, app will call `http://localhost:5000` if not set.

- Import the reservation data with a CSV file
  ```shell
  # Terminal 4
  truck-berth-app start --csv-file <path to the reservation data csv file>
    ```

  Example for Importing Reservation data

  ```shell
  truck-berth-app start --csv-file c:\Users\Documents\reservation_data.csv
  ```

  Output:

  ```shell
  Data imported successfully!
  ```

- Export the reservation and actual data

  ```shell
  # Terminal 4
  truck-berth-app export --type <export type> --output-dir <dir to export the data>

  - export type : actual / reservation
  ```

  Example for exporting actual data

  ```shell
  # Terminal 4
  truck-berth-app export --type actual --output-dir C:\Users\Downloads
  ```

  Output:

  ```shell
  [2024-01-25 15:19:36,333] INFO: Data exported successfully! Path: C:\Users\Downloads\reservation_1706176176.csv
  ```

- Stop the model inference
  ```shell
  # Terminal 4
  truck-berth-app stop
  ```
  Output:
  ```shell
  Inference stopped for the following berths ['B1']
  ```
  _**Note:**_ Execute `truck-berth-app stop` before closing down the application services.
