import codecs
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
    with codecs.open("report_" + report_time + ".md", "a", "utf-8") as report:
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
    Generates a human-readable DISK usage info from ``psutil.disk_usage("/")``.

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


# Use one method
def disk_info(report_time: str):
    """
    Gather information about DISK usage
    :param report_time:
    :return:
    """
    with codecs.open("report_" + report_time + ".md", "a", "utf-8") as report:
        report.write("## DISK USAGE  \n")
        for key in get_disk_usage():
            if "percent" in key.lower():
                report.write(key + " : " + str(get_disk_usage()[key]) + "%  \n")
            else:
                report.write(key + " : " + str(get_disk_usage()[key]) + "GB  \n")
        report.write("\n")


def cpu_info(report_time: str):
    """
    Gather information about CPU usage
    :param report_time:
    :return:
    """
    with codecs.open("report_" + report_time + ".md", "a", "utf-8") as report:
        report.write("## CPU USAGE  \n")
        report.write("Logical processors: " + str(psutil.cpu_count()) + "  \n")
        report.write("Frequency: " + str(psutil.cpu_freq()[0]) + "  \n")
        report.write("\n")


def get_mem_usage() -> Dict[str, Union[int, float]]:
    """
    Generates a human-readable MEM usage info.
    :return: A dict with 5 main fields (Total, Available, Used, Free, Percent) and rounded mem usage.
    """
    mem_usage = psutil.virtual_memory()

    mem_percents = mem_usage[2]

    mem_usage_list = list(mem_usage[0:2] + mem_usage[3:5])
    mem_usage_len = len(mem_usage_list)

    mem_util_mem = [mem_usage_list[idx] // (1024**3) for idx in range(mem_usage_len)]

    mem_util_mem.append(mem_percents)
    mem_util_len = len(mem_util_mem)

    mem_util_kind = ["Total", "Available", "Used", "Free", "Percent"]
    result = {mem_util_kind[idx]: mem_util_mem[idx] for idx in range(mem_util_len)}

    return result


# Use one method
def mem_info(report_time: str):
    """
    Gather information about MEM usage
    :param report_time:
    :return:
    """
    with codecs.open("report_" + report_time + ".md", "a", "utf-8") as report:
        report.write("## MEMORY USAGE  \n")
        for key in get_mem_usage():
            if "percent" in key.lower():
                report.write(key + " : " + str(get_mem_usage()[key]) + "%  \n")
            else:
                report.write(key + " : " + str(get_mem_usage()[key]) + "GB  \n")
        report.write("\n")
    # print(psutil.swap_memory())


def net_info(report_time: str):
    """
    Gather information about NET usage
    :param report_time:
    :return:
    """
    with codecs.open("report_" + report_time + ".md", "a", "utf-8") as report:
        report.write("## NETWORK USAGE  \n")
        net_if_address = psutil.net_if_addrs()
        for i in net_if_address:
            report.write(i + "  \n")
            # print(net_if_address[i][1])
            report.write(str(net_if_address[i][1][1:3]) + "  \n")
        report.write("\n")
    # print(psutil.net_if_stats())


# print(psutil.test())


if __name__ == "__main__":
    timestamp = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
    general_info(timestamp)
    disk_info(timestamp)
    cpu_info(timestamp)
    mem_info(timestamp)
    net_info(timestamp)
