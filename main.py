import json

import requests
from requests.auth import HTTPBasicAuth


def main():
    url = ""
    headers = {"Accept": "application/json"}
    auth = HTTPBasicAuth('', '')

    accepted = ["accepted, good"]
    rejected = ["error", "rejected", "missing", "mis-labeled"]
    final_results = {}

    r = requests.request("GET", url, headers=headers, auth=auth)
    s = r.text

    result = json.loads(s)
    for task in result['docs']:
        if task.get('status') == 'canceled':
            final_results[task.get('task_id')] = 'Not available'
            continue
        if task.get('customer_review_comments'):
            customer_review = ''.join(task.get('customer_review_comments'))
            final_results[task.get('task_id')] = task.get('customer_review_comments')

            no_spaces = list(filter(None, customer_review))

            if len(no_spaces) < 1:
                final_results[task.get('task_id')] = 'Not audited'
                continue
            for response in customer_review:
                if response in accepted:
                    final_results[task.get('task_id')] = 'Accepted'
                elif response in rejected:
                    final_results[task.get('task_id')] = 'Rejected'
                else:
                    final_results[task.get('task_id')] = 'Rejected'

    json_object = json.dumps(final_results, indent=1)

    with open("quality_check.json", "w") as outfile:
        outfile.write(json_object)


if __name__ == '__main__':
    main()
