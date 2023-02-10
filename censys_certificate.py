import argparse
import csv
import datetime
import os

from censys.search import CensysCertificates


class CensysCertificate:
    __censys_cert_obj = None

    def __init__(self):
        """Initialize the Censys Certificates object"""
        self.__censys_cert_obj = CensysCertificates()

        if self.__censys_cert_obj is None:
            print("Error getting the Censys Certificate object!!! Make sure the API Key and Secret are populated.")
            return

    def populate_x_509_certificates(self, domain: str):
        """Fetches X.509 certificates through Censys search API for censys.io domain.
        Later the trusted (unexpired) certificates are populated to a csv file and the csv file location is printed.

        Args:
            domain str: The domain argument. If no domain is passed, it will be defaulted to censys.io

        :return: None
        """
        print("Fetching the certificates for domain: {0}".format(domain))

        fields = [
            "parsed.fingerprint_sha256",
            "parsed.validity.start",
            "parsed.validity.end",
        ]

        # Calling the search API
        pages = self.__censys_cert_obj.search(
            "{0} and tags: trusted".format(domain),
            fields
        )

        # If no certificates are retrieved from the search API, then break the flow
        if not pages:
            print("No certificates were fetched")
            return

        file_location = os.getcwd() + "/valid_certificates.csv"
        
        # Iterate through the certificates and populate them to a csv file
        with open(file_location, 'w', encoding="utf8") as csv_file:
            csv_writer = csv.writer(csv_file)

            print("Writing the certificates to a csv file...")

            # Populate the header row
            csv_writer.writerow(["SHA256 Fingerprint", "Validity Start Date", "Validity End Date"])

            for certificate in pages:
                if certificate is not None:
                    end_date = datetime.datetime.strptime(certificate["parsed.validity.end"], "%Y-%m-%dT%H:%M:%SZ")

                    # Ignore certificates whose validity end date is lesser than the current datetime,
                    # i.e. expired certificates
                    if end_date > datetime.datetime.now():
                        csv_writer.writerow([certificate["parsed.fingerprint_sha256"],
                                             certificate["parsed.validity.start"],
                                             certificate["parsed.validity.end"]]
                                            )
            print("The file can be found over here: {0}".format(file_location))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", type=str, required=False, default="censys.io")
    args = parser.parse_args()

    censys_certificate = CensysCertificate()
    censys_certificate.populate_x_509_certificates(args.domain)
