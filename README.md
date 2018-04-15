# tabularius

> noun. a keeper of archives, a registrar, a public notary, scrivener

tabularius is a free and open platform for educators to help their students
succeed.

## Running

`cd` into the cloned repository and enter the following into your terminal:

```bash
export FLASK_APP=tabularius.py
flask run
```

Flask will give a port url to visit, most likely
[http://127.0.0.1:5000](http://127.0.0.1:5000), where you will find the website
running.

To enable debugging, also do the following:

```bash
export FLASK_DEBUG=1
```

To configure the email server, you need to add your email into the admin field in `config.py`.

Then, export the following:
```bash
exportexportexportMAIL_SERVER=smtp.googlemail.com
MAIL_PORT=587
MAIL_USE_TLS=1
exportexportMAIL_USERNAME=<your-gmail-username>
MAIL_PASSWORD=<your-gmail-password>
```

Where you replace the values in `<>` with the desired email address. Please,
for all that is good, do not upload these credentials onto a repository
anywhere online.
