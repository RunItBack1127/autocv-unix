# AutoCV
The backend of the app is built using [Flask](https://flask.palletsprojects.com), a lightweight microframework for standing up backends quickly.

## Compatability
| Platform | Initialization     | Invoke `GET /resume` | Invoke `GET /cv`   | Invoke `/copy`     |
| -------- | ------------------ | -------------------- | ------------------ | ------------------ |
| Windows  | :heavy_check_mark: | :heavy_check_mark:   | :heavy_check_mark: | :heavy_check_mark: |
| MacOS    | :heavy_check_mark: | :heavy_check_mark:   | :heavy_check_mark: | :heavy_check_mark: |
| Linux    | :heavy_check_mark: | :heavy_check_mark:   | :heavy_check_mark: | :heavy_check_mark: |

## Installation
Run the following commands in the `src/backend` directory:
### Windows
```
pip install virtualenv
virtualenv ENV_NAME
ENV_NAME\Scripts\activate
pip install -r requirements
python server.py
```

### OSX/Linux
```
pip install virtualenv
virtualenv ENV_NAME
source ENV_NAME/bin/activate
pip install -r requirements
python server.py
```
