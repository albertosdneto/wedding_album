# Wedding album
Wedding album that allows the bride and groom to select which photos provided by guests will be shown.

## Working version
To see the app running access: https://weddingalbum2020.herokuapp.com/ 


## Get Started

Clone the project
```
git clone https://github.com/albertosdneto/wedding_album.git
cd wedding_album
```

Create the virtual environment
```
python3 -m venv venv
. venv/bin/activate
```

Install requirements
```
pip install --upgrade pip setuptools
pip install -r requirements.txt 
```

Setup your database on https://cloud.mongodb.com/

Environment Variables:

1 - If running locally, create a .env file based on example.env.

2 - If on Heroku, setup environment variables
```
IS_PROD=True
DEBUG=False
SECRET_KEY=SomeRandomKey
DATABASE_URL=mongodb+srv://<username>:<password>@clusterXX.vavnb.mongodb.net/<database>?retryWrites=true&w=majority
S3_BUCKET_NAME=bucket-name
S3_KEY=access_key
S3_SECRET=SECRET_ACCESS_KEY
```

Run the app
```
gunicorn 'wedding_album:create_app()'
```