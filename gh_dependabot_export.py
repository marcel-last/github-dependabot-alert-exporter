import csv
from dotenv import load_dotenv
from datetime import datetime
import os
import requests
import sys

# Load in '.env' file
load_dotenv()

org_name = os.getenv('GH_ORG_NAME')
token = os.getenv('GH_ACCESS_TOKEN')
api_endpoint = f'https://api.github.com/orgs/{org_name}/dependabot/alerts'
headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': f'Bearer {token}',
    'X-GitHub-Api-Version': '2022-11-28'
}

export_dir = 'export'

# Create 'export' directory if not exists
if not os.path.isdir(export_dir):
    sys.stdout.write("Creating directory 'export/'...\n")
    os.makedirs('export')
    sys.stdout.write("DONE.\n\n")

gh_dependabot_alerts_csv_path = f'{export_dir}/dependabot_alerts_{datetime.today().strftime("%Y_%m_%d")}.csv'

alerts = []

# Retrieve all Dependabot alerts
sys.stdout.write(f"Retrieving GitHub Dependabot alerts for orgasnisation '{org_name}'...\n")
while api_endpoint:
    response = requests.get(api_endpoint, headers=headers)
    response.raise_for_status()
    data = response.json()
    alerts += data
    api_endpoint = response.links.get('next', {}).get('url')
sys.stdout.write("DONE.\n\n")


# Write alerts to a CSV file
with open(gh_dependabot_alerts_csv_path, 'w', newline='') as csvfile:
    sys.stdout.write("Generating GitHub Dependabot alerts CSV file...\n")
    fieldnames = ['number', 'state', 'repository_name', 'repository_url', 'ghsa_id',
                  'severity', 'cvss_vector_string', 'cvss_score', 'cwe_id', 'cwe_name',
                  'cve_id', 'cve_summary', 'cve_description',
                  'package_ecosystem', 'package_name','vulnerable_version_range', 'first_patched_version',
                  'dependency_manifest_path', 'dependency_scope',
                  'references', 'published_at', 'updated_at', 'withdrawn_at']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for alert in alerts:
        if 'number' in alert:

            # Split `url` entries into seperate line items under respective csv headers.
            references = [ref['url'] for ref in alert['security_advisory']['references']]
            references_urls = '\n'.join(references)

            # Split `cwe cwe_id` and `cwe name` entries into seperate line items under respective csv headers.
            cwe_ids = [cwe['cwe_id'] for cwe in alert['security_advisory']['cwes']]
            cwe_names = [cwe['name'] for cwe in alert['security_advisory']['cwes']]
            cwe_ids_str = '\n'.join(str(cwe_id) for cwe_id in cwe_ids)
            cwe_names_str = '\n'.join(str(cwe_name) for cwe_name in cwe_names)

            # Check to ensure that a key exists fonr `first_patched_version`
            first_patched_version = alert['security_vulnerability']['first_patched_version']
            first_patched_version_identifier = first_patched_version['identifier'] if first_patched_version else ''

            writer.writerow({
                'number': alert['number'],
                'state': alert['state'],
                'repository_name': alert['repository']['full_name'],
                'repository_url': alert['repository']['html_url'],
                'ghsa_id': alert['security_advisory']['ghsa_id'],
                'severity': alert['security_advisory']['severity'],
                'cvss_vector_string': alert['security_advisory']['cvss']['vector_string'],
                'cvss_score': alert['security_advisory']['cvss']['score'],
                'cwe_id': cwe_ids_str,
                'cwe_name': cwe_names_str,
                'cve_id': alert['security_advisory']['cve_id'],
                'cve_summary': alert['security_advisory']['summary'],
                'cve_description': alert['security_advisory']['description'],
                'package_ecosystem': alert['security_vulnerability']['package']['ecosystem'],
                'package_name': alert['security_vulnerability']['package']['name'],
                'vulnerable_version_range': alert['security_vulnerability']['vulnerable_version_range'],
                'first_patched_version': first_patched_version_identifier,
                'dependency_manifest_path': alert['dependency']['manifest_path'],
                'dependency_scope': alert['dependency']['scope'],
                'references': references_urls,
                'published_at': alert['security_advisory']['published_at'],
                'updated_at': alert['security_advisory']['updated_at'],
                'withdrawn_at': alert['security_advisory']['withdrawn_at']
            })
    sys.stdout.write(f"DONE.\n\nCSV export saved to: '{gh_dependabot_alerts_csv_path}'\n\n")
