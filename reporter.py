import platform
from datetime import datetime

# import psutil

my_system = platform.uname()


def general_info(report_time: str):
    with open("report_" + report_time + ".txt", "a") as report:
        report.write("GENERAL INFO \n")
        report.write("System: " + my_system.system + "\n")
        report.write("Node Name: " + my_system.node + "\n")
        report.write("Release: " + my_system.release + "\n")
        report.write("Version: " + my_system.version + "\n")
        report.write("Machine: " + my_system.machine + "\n")
        report.write("Processor: " + my_system.processor + "\n")


# Gather info about disk

# Gather info about cpu

# Gather info about net

# Gather info about mem

# print(psutil.test())

if __name__ == "__main__":
    timestamp = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
    general_info(timestamp)
