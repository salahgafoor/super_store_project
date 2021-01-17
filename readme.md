# Super Store App

Serves as an online store

## Installation

I. Clone the repo
```bash
git clone https://github.com/salahgafoor/super_store_project.git
```
II. Set an environment
1. Install environment if not available
```bash
sudo apt install python3-venv
```
2. Switch to directory where we want to store the environment
```bash
python3 -m venv my-project-env
```
Here, I've selected environement as my-project-env
3. Activate environment
```bash
source my-project-env/bin/activate
```
Note: To exit from the environment
```bash
deactivate
```
III. Install the libraries using requirements.txt
```bash
pip3 install -r requirements.txt
```
IV.Run migrations
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
V.Test on server
```bash
python3 manage.py runserver
```

## License
[MIT](https://choosealicense.com/licenses/mit/)