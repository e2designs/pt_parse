This script is intended to be run after an automation run that generates pytest
results in json format. 

Args are all strings, & these include:
        url = sys.argv[1]
        test_bench = sys.argv[2]
        hw_serial_num = sys.argv[3]
   

results POSTED:

    suite_json_data = {
        'suite_name': suite_obj.suite_name,
        'date_run': suite_obj.date_run,
        'num_tests': suite_obj.num_tests,
        'num_passed': suite_obj.num_passed,
        'num_skipped': suite_obj.num_skipped,
        'num_failed': suite_obj.num_failed
    }

    testcase_json_data = {
        'test_suite': testcase.suite_name,
        'test_module': testcase.test_module,
        'test_name': testcase.test_name,
        'date_run': testcase.date_run,
        'status': testcase.status
        'failing_context': failing_context 
    }
        
questions, email gsirois@protonmail.com
