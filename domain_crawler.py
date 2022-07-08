import time
import dns.resolver
import whois
import csv
import sys
import argparse
import os.path


# *  MCF 1/4/2021
# The following application was developed to allow a user to quickly get domain information


def main(*args):
    # Setup command line inputs so a user can specify a file
    # By default the application looks for "domain_list.txt" in the current folder
    parser = argparse.ArgumentParser(
        description="This application gathers domain information \
                    it accepts a file containing a list of domains \
                    and generates a csv with all the information as output"
    )

    parser.add_argument(
        "-i",
        metavar="file",
        required=False,
        help="the file containing a list of domains",
    )

    received_args = parser.parse_args()

    # Check the arguments if there were any passed in
    if received_args.i is not None:
        # Check if the file specified exists otherwise throw an exception
        try:
            file_exists = os.path.exists(str(received_args.i))
            if not file_exists:
                raise FileNotFoundError
            input_file = str(received_args.i)
        # Display the exception message and kill execution
        except FileNotFoundError:
            print(
                f"File {received_args.i} was not found in the current folder"
            )
            sys.exit(1)
    # If no file is passed in default to searching for a "domain_list.txt" file
    else:
        # Check if the file "domain_list.txt" exists otherwise throw an exception
        try:
            file_exists = os.path.exists("domain_list.txt")
            if not file_exists:
                raise FileNotFoundError
            print("Successfully found 'domains_list.txt file' in current directory, using this as input\n")
            input_file = "domain_list.txt"
        # Display the exception message and kill execution
        except FileNotFoundError:
            print(
                "File 'domain_list.txt' was not found please use the '-i' argument and provide the name of your input "
                "file "
            )
            sys.exit(1)

    program_start_time = time.time()

    get_domain_data(input_file=input_file)

    program_end_time = time.time()

    total_execution_time = round(float(program_end_time - program_start_time), 2)

    print(f"\nTask completed successfully :) in [{total_execution_time} seconds]\n")


def get_domain_data(input_file):
    """Get The domain data for each domain in the input file"""

    # Override default nameservers to query.
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    # Use Google public nameservers for domain queries
    dns.resolver.default_resolver.nameservers = ["8.8.8.8"]

    # Get data from the input file Open the file and parse through line by line, this will minimize memory user over
    # having to load all contents to memory
    with open(input_file) as domain_list:

        # Initialize the output file
        with open("domain_information.csv", "w", newline='', encoding='utf-8') as output_file:
            # initialize the csv writer so we can output csv files
            writer = csv.writer(output_file, delimiter=",", dialect="excel")
            writer.writerow(
                [
                    "#:",
                    "DOMAIN:",
                    "REGISTRAR:",
                    "NAMESERVERS:",
                    "A RECORDS:",
                    "MX RECORDS:",
                    "EXPIRATION DATE:",
                    "HOSTED ON DM SG:",
                    "EMAIL HOSTING SERVICE:",
                ]
            )

            print("Starting Data Collection For Domains..\n")
            # Loop through the contents while using enumerate to allow us to access to the current loop index
            # Begin enumeration at index 1
            for index, domain in enumerate(domain_list, 1):
                raw_domain_name = domain.strip()

                # Get the data for the current domain

                # Attempt to query domain information and handle all expectations gracefully
                # The information is stored into arrays as there may multiple elements in each returned result
                print(f"Getting data for domain ({index}): {raw_domain_name}")
                # Gather domain Nameserver information
                try:
                    domain_nameservers = dns.resolver.resolve(raw_domain_name, "NS")
                except Exception as e:
                    domain_nameservers = [
                        f"Error: {e}",
                    ]
                # Gather domain a record information
                try:
                    domain_a_records = dns.resolver.resolve(raw_domain_name, "A")
                except Exception as e:
                    domain_a_records = [
                        f"Error: {e}",
                    ]
                # Gather domain mx record information
                try:
                    domain_mx_records = dns.resolver.resolve(raw_domain_name, "MX")
                except Exception as e:
                    domain_mx_records = [
                        f" Error: {e}",
                    ]
                # Gather domain whois information
                try:
                    domain_whois_records = whois.whois(raw_domain_name)
                except Exception as e:
                    domain_whois_records = [
                        f" Error: {e}",
                    ]

                ns_records = "".join([f"{item}\n" for item in domain_nameservers])
                a_records = "".join([f"{item}\n" for item in domain_a_records])
                mx_records = "".join([f"{item}\n" for item in domain_mx_records])

                # List if dune land media hosts the site
                if "35.206.96.200" in a_records:
                    dm_hosted = "Yes, LEGACY PLAN(Based on A record)"
                elif "35.208.132.251" in a_records:
                    dm_hosted = "Yes, CLOUD PLAN 1(Based on A record)"

                else:
                    dm_hosted = "No,(Based on A record)"

                # List location of emails (based on mx records)
                if "google" in mx_records:
                    email_hosting_service = "Google Workspaces: *Use caution when modifying nameserver records*"
                elif ".mailspamprotection.com" in mx_records:
                    email_hosting_service = "!WARNING!: Email's point to our SG account, email accounts may exist on " \
                                            "our SG account "
                elif ".mail.protection.outlook.com" in mx_records:
                    email_hosting_service = "Microsoft Office 360: *Use caution when modifying nameserver records*"
                elif "Error" in mx_records:
                    email_hosting_service = "Error getting mx records, the domain may not have any active email " \
                                            "service or mx records are down "
                else:
                    email_hosting_service = (
                        "Other/Unknown: Emails hosted at an external location"
                    )

                # * Output results as a row on the CSV file
                writer.writerow(
                    [
                        index,
                        raw_domain_name,
                        domain_whois_records["registrar"],
                        f"{ns_records}",
                        f"{a_records}",
                        mx_records,
                        domain_whois_records["expiration_date"],
                        dm_hosted,
                        email_hosting_service,
                    ]
                )


if __name__ == "__main__":
    main(sys.argv[1:])
