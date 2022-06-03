# Cloud Platform

This work is for DSD2022 at JLU and UTAD. DSD represents **D**istributed **S**oftware **D**evelopment. This cycle of DSD in the spring of 2022 motivates students to design a large commercial intelligent prosthesis management system.

Team **Pigeonhole** is responsible for the code development and deployment of the core backend server. Our project includes two parts - cloud platform and embedded device backend.

## Introduction

This project is supported by [Flask](https://github.com/pallets/flask). Cloud platform receives requests from frontend clients and interacts with the database. All APIs, including authentication APIs and device management APIs are in RESTful architecture style. It aims at managing the whole system in a coherent, consistent and efficient manner.

## Usage

Run the following command to install the dependencies:

```
git clone https://github.com/PigeonholeDSD/cloud-platform.git
cd cloud-platform/
git submodule update --init
find . -name requirements.txt -exec pip install -r {} \;
```

Because we use submodule to manage database and algorithm module, if there're new commits, sync and commit with:

```
git submodule update --remote --merge
git commit -am 'chore: sync <mod>'
```

Run in the development mode:

```
python app.py
```

The default listening address would be `http://localhost:8000`.

If you would like to run in the debug mode, please pass `debug=True` to `app.run()`, i.e. `app.run(debug=True)`.

Use a production-ready WSGI server for deployment, for example:

```
gunicorn --chdir /path/to/cloud-platform app:app
```

## API Documentation

To learn more about API documentation, please see [API Documentation](https://doc.ciel.pro/_nz-ppsiSa6RPzR7zwd6Bg?both).

## License

All rights reserved. If you want to use this program, please contact https://pigeonhole.fun for a private license, free of charge maybe.
