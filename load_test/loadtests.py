
import os
import pandas as pd
import subprocess

def my_first_locust_test():
    time_limit = 60 # seconds
    number_of_users = 10
    locust_command = f"locust --headless -u {number_of_users} --csv results/results --run-time {time_limit}"

    os.system(locust_command)
    #subprocess.run(locust_command)

    df_stats = pd.read_csv("results/results_stats.csv")
    total_number_of_requests = df_stats["Request Count"][0]
    number_of_failures = df_stats["Failure Count"][0]

    percentage_of_failures = 100 * number_of_failures / total_number_of_requests
    print("percentage_of_failures: ", percentage_of_failures)


my_first_locust_test()
