import glob
import json
import requests
import re
import sys


def parse_file_into_json_object(results_file):
    with open(results_file, 'r') as results:
        json_results = json.load(results)
    return json_results


def create_suite(json_results, test_bench, hw_serial_num):
    suite_name = json_results['included'][0]['attributes']['name'].split('/')[0]
    test_suite = {'suite_name': suite_name, 'test_bench': test_bench, 'system': hw_serial_num}
    return test_suite


def build_tests(json_results):
    testcase_list = []
    for test_entry in json_results['included']:
        full_name = test_entry['attributes']['name']

        testcase = {'suite_name': full_name.split('/')[0], 'test_module': re.split('/|::', full_name)[1],
                    'test_name': full_name.split('::')[1].split('[')[0],
                    'date_run': json_results['data'][0]['attributes']['created_at']}
        if test_entry['attributes'].get('call') is not None:
            testcase['status'] = test_entry['attributes']['call']['outcome']
        else:
            testcase['status'] = test_entry['attributes']['outcome']
        if testcase['status'] is 'xfailed' or testcase['status'] is 'failed':
            testcase['status'] = 'failed'
            testcase['failing_context'] = test_entry['attributes']['call']['longrepr'].strip()
        else:
            testcase['failing_context'] = ''
        testcase_list.append(testcase)
    return testcase_list


def complete_suite(json_results, test_list, test_suite):
    test_suite.update({'date_run': json_results['data'][0]['attributes']['created_at'],
                       'num_tests': 0, 'num_passed': 0, 'num_skipped': 0, 'num_failed': 0})
    for test in test_list:
        test_suite['num_tests'] += 1
        if test['status']:
            status = test['status']
            test_suite['num_{}'.format(status)] += 1
    return test_suite


def post_results(post_item, url):
    try:
        json_data = json.dumps(post_item)
        r = requests.post(url, data=json_data, headers={'Content-type': 'application/json'})
        print(r.status_code, r.reason)
    except ValueError as ve:
        print(ve)
    except TypeError as te:
        print(te)


if __name__ == '__main__':

    try:
        url = sys.argv[1]
        test_bench = sys.argv[2]
        hw_serial_num = sys.argv[3]
    except IndexError:
        url = 'http://127.0.0.1:8000/'
        test_bench = 'test_bench'
        hw_serial_num = 'test_hw_sn'

    results_files = glob.glob('*.json')
    for rf in results_files:
        json_results = parse_file_into_json_object(rf)

        test_suite = create_suite(json_results=json_results, test_bench=test_bench,
                                  hw_serial_num=hw_serial_num)
        test_list = build_tests(json_results=json_results)
        test_suite = complete_suite(json_results=json_results, test_list=test_list, test_suite=test_suite)

        post_results(post_item=test_suite, url=url)
        for test in test_list:
            post_results(post_item=test, url=url)
