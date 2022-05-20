import platform
from datetime import datetime
from typing import Dict, Union

import psutil

# Pass args


def general_info(report_time: str):
    """
    Gather general info about host system
    :param report_time:
    :return:
    """
    system = platform.uname()
    with open("report_" + report_time + ".md", "a") as report:
        report.write("## GENERAL INFO \n")
        report.write("System: " + system.system + "  \n")
        report.write("Node Name: " + system.node + "  \n")
        report.write("Release: " + system.release + "  \n")
        report.write("Version: " + system.version + "  \n")
        report.write("Machine: " + system.machine + "  \n")
        report.write("Processor: " + system.processor + "  \n")
        report.write("\n")


def get_disk_usage() -> Dict[str, Union[int, float]]:
    """
    Generates a human-readable disk usage info from ``psutil.disk_usage("/")``.

    :return: A dict with 4 main fields (Total, Used, Free, Percent) and rounded disk usage.
    """
    disk_usage = psutil.disk_usage("/")
    disk_usage_len = len(disk_usage)

    disk_util_mem = [
        disk_usage[idx] // (1024**3) for idx in range(disk_usage_len - 1)
    ]
    disk_util_mem.append(disk_usage[-1])  # Add the percentage value (float)

    disk_util_kind = ["Total", "Used", "Free", "Percent"]
    result = {disk_util_kind[idx]: disk_util_mem[idx] for idx in range(disk_usage_len)}

    return result


def disk_info(report_time: str):
    """
    Gather information about disk usage
    :param report_time:
    :return:
    """
    with open("report_" + report_time + ".md", "a") as report:
        report.write("## DISK USAGE  \n")
        for key in get_disk_usage():
            if "percent" in key:
                report.write(key + " : " + str(get_disk_usage()[key]) + "%  \n")
            else:
                report.write(key + " : " + str(get_disk_usage()[key]) + " GB  \n")
        report.write("\n")


def cpu_usage(report_time: str):
    """
    Gather information about CPU usage
    :param report_time:
    :return:
    """
    with open("report_" + report_time + ".md", "a") as report:
        report.write("## CPU USAGE  \n")
        report.write("Logical processors: " + str(psutil.cpu_count()) + "  \n")
        report.write("Frequency: " + str(psutil.cpu_freq()[0]) + "  \n")


# Gather info about mem

# Gather info about net

# print(psutil.test())


if __name__ == "__main__":
    timestamp = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
    general_info(timestamp)
    disk_info(timestamp)
    cpu_usage(timestamp)
