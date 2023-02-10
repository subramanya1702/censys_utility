## Censys Certificates Utility

A python utility to get the X.509 certificates from Censys for a particular domain and populate them to a csv file.

### Getting Started

Make sure you have installed the latest version of Python on your system.
If not, install python by following the instructions given here:
https://wiki.python.org/moin/BeginnersGuide/Download

After installing python, install the necessary dependencies using `pip`

```sh
pip install -r requirements.txt
```

You need to configure the Censys Search credentials for the utility to run without failing.
Run the `censys config` command or manually set the `CENSYS_API_ID` and `CENSYS_API_SECRET` environment variables.

```sh
$ censys config

Censys API ID: XXX
Censys API Secret: XXX
Do you want color output? [y/n]: y

Successfully authenticated for your@email.com
```

### Usage

Now that everything is setup, the utility can be run.
The utility takes in an optional `--domain` argument. If the domain is not passed, it will be defaulted to `censys.io`

Without domain argument
```sh
python censys_certificate.py
```

With domain argument
```sh
python censys_certificate.py --domain abc.xyz.com
```

The location of the certificates file will be printed at the end.

### Author

#### Subramanya Keshavamurthy

#### keshavas@oregonstate.edu