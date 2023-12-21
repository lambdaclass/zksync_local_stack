import os

import pandas as pd


def test_01_basic_loadtest_with_1_user():
    time_limit = 30  # seconds
    number_of_users = 1
    spawn_rate = 10
    _run_loadtest(time_limit, number_of_users, spawn_rate)

    _get_loadtest_results()


def test_02_loadtest_with_100_users():
    time_limit = 60  # seconds
    number_of_users = 100
    spawn_rate = 10
    _run_loadtest(time_limit, number_of_users, spawn_rate)

    _get_loadtest_results()


def test_03_loadtest_with_500_users():
    time_limit = 60  # seconds
    number_of_users = 1000
    spawn_rate = 500
    _run_loadtest(time_limit, number_of_users, spawn_rate)

    _get_loadtest_results()


def test_04_run_to_have_100_req_per_second():
    time_limit = 60  # seconds
    number_of_users = 1000
    spawn_rate = 500
    _run_loadtest(time_limit, number_of_users, spawn_rate)

    _get_loadtest_results()


def _run_loadtest(time_limit, number_of_users, spawn_rate):
    locust_command = f"locust --headless -u {number_of_users} --spawn-rate {spawn_rate} --csv results/results --run-time {time_limit} -f load_test/locust/locustfile.py"
    os.system(locust_command)


def _get_loadtest_results():
    df_stats = pd.read_csv("results/results_stats.csv")

    total_number_of_requests = df_stats["Request Count"][0]
    number_of_failures = df_stats["Failure Count"][0]
    average_response_time = df_stats["Average Response Time"][0]
    requests_per_second = df_stats["Requests/s"][0]
    percentage_of_failures = 100 * number_of_failures / total_number_of_requests

    print("percentage_of_failures: ", percentage_of_failures, "%")
    print("Average Response Time: ", average_response_time, "ms")
    print("Requests/s: ", requests_per_second, "R/s")


test_01_basic_loadtest_with_1_user()
