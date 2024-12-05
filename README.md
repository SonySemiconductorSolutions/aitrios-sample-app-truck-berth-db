# Truck Berth DB Application

## About this Software
This is a sample of "**Truck Berth DB Application**". Please note the following when using it：

* This sample is released with the assumption it will be used for development.
* This sample may contain errors or defects that obstruct regular operation of the device.
* "**Truck Berth DB Application**" runs using the AI model, Edge App, "**AITRIOS Console**" and FerretDB.
* Get the appropriate AI model, Edge App and command parameter file. 
* The AI model, Edge App and command parameter file can be obtained by contacting the SSS member (Logistics Team) via the following query: ["**Inquiry Form - Input**"](https://support.aitrios.sony-semicon.com/hc/en-us/requests/new)
* The User Guide describes how to develop and set up these components and start application.
* All the services in this application are tested and supposed to run on a single windows 10 environment. 

## Overview
"**Truck Berth DB Application**" helps in monitoring Truck Berth in Parking lots with the help of IMX500 Edge AI Device. Application uses ReactJS as the frontend and Flask, Celery as the backend. In Web UI, clearly shows the status of the berth allotment. For an in-depth view of the system, please refer [User Guide](docs/user_guide/user_guide.adoc).

### AI model
With the real-time truck's license plate data, this AI model can detect and recognize the number plate of trucks arriving at the parking lot.

### Use FlatBuffers-compiler to generate the source code
This sample application is designed for output from Edge AI Devices based on this data schema [FBS files](tools/deserialization_fbs)

**NOTE**: This procedure has been already implemented for the development of current sample application and user need not to perform again. Thus the below information is only for the reference showing how to use the FBS files for the deserialization of model output.

The version of FlatBuffers-compiler uses 23.1.21.

- Download the [FlatBuffers-compiler for Windows](https://github.com/google/flatbuffers/releases/download/v23.1.21/Windows.flatc.binary.zip)
- Extract the downloaded zip file to any folder by right-clicking and selecting [**Extract All**]
- Copy the `flatc.exe` into `tools/deserialization_fbs`
- Start a command prompt, move to the folder you extracted in the preceding, and make sure the version appears

```shell
> flatc.exe --version
```

In the directory where you saved the FBS file, run the following command.

For available options, see the official page [FlatBuffers:Using_schema_compiler](https://google.github.io/flatbuffers/flatbuffers_guide_using_schema_compiler.html)

```shell
> cd tools/deserialization_fbs
> flatc.exe --python *.fbs
```
- Replace the auto-generated code based on the FBS file in [src/backend/truck-berth-app/src/modules/cloudapp]

### Pre-requisites
#### Service and Edge AI Device
- The following service and Edge AI Device are required to run this software:

    - Buy Console Developer Edition Plan
    - Buy Edge AI Device

IMPORTANT: Please visit the ["**Portal User Manual**"](https://developer.aitrios.sony-semicon.com/en/documents/portal-user-manual) for client ID and secret.
Please visit the ["**Rest API Authentication**"](https://developer.aitrios.sony-semicon.com/en/file/download/rest-api-authentication) for console endpoint and portal authorization endpoint.
The AI model, Edge App and command parameter file can be obtained by contacting the SSS member (Logistics Team) via the following query: ["**Inquiry Form - Input**"](https://support.aitrios.sony-semicon.com/hc/en-us/requests/new)

#### AI model, Edge App, Command Parameter File
- Get the appropriate AI model, Edge App and command parameter file.
- Deploy AI model and Edge App to Edge AI Device.
- Bind Command Parameter file to Edge AI Device.
- For more details, refer [AI model setup](docs/user_guide/ai_model_setup.adoc).

#### Edge AI Device Firmwares
- Edge AI Device App firmware: AppFW_FF19.20 (version number: 070020)
- Edge AI Device Sensor Loader: FF19.20 (version number: 020301)
- Edge AI Device Sensor: FF19.20 (version number: 010701)

## Setup System
[Refer docs/user_guide/user_guide.adoc](docs/user_guide/user_guide.adoc)

## Get support
* About the AI model, Edge App and command parameter file for this application :
    * Contact SSS member (Logistics Team) via the following query: ["**Inquiry Form - Input**"](https://support.aitrios.sony-semicon.com/hc/en-us/requests/new)
* The others 
    * ["**Contact Us**"](https://support.aitrios.sony-semicon.com/hc/en-us/requests/new)

## See also
- ["**Developer Site**"](https://developer.aitrios.sony-semicon.com/en)

## Trademark
- ["**Read This First**"](https://developer.aitrios.sony-semicon.com/en/edge-ai-sensing/guides)

## Versioning
This repository aims to adhere to Semantic Versioning 2.0.0.

## Branch
See the "**Release Note**" from [**Releases**] for this repository.

Each release is generated in the main branch. Pre-releases are generated in the develop branch. Releases will not be provided by other branches.

## Security
Before using Codespaces, please read the Site Policy of GitHub and understand the usage conditions.
