# Cloud Platform of DSD 2022 Server

DSD represents **D**istributed **S**oftware **D**evelopment. This cycle of DSD in the spring of 2022 motivates students to design a large commercial intelligent prosthesis management system. Team **Pigeonhole** is responsible for the code development and deployment of the core backend server. Our project includes two parts - cloud platform and device-side backend.

This repository is the cloud platform of DSD 2022 Server. 

## Introduction

This project is supported by [Flask](https://github.com/pallets/flask). Cloud platform receives requests from frontend clients and interacts with the database. All APIs, including authentication APIs and device management APIs are in RESTful architecture style. It aims at managing the whole system correctly and efficiently.

## Usage

Run the following command to install the dependencies:

```
cd /path/to/this/project && pip install -r requirements.txt
```
Run in the development mode:

```
python app.py
```
The default listening address would be `http://localhost:5000`.

If you would like to run in the debug mode, please pass `debug=True` to `app.run()`, i.e. `app.run(debug=True)`. 

## API Documentation

To learn more about API documentation, please see [API Documentation](https://doc.ciel.pro/_nz-ppsiSa6RPzR7zwd6Bg?both).
