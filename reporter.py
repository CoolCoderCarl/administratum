import codecs
import platform
from datetime import datetime
from typing import Dict, Union

import psutil

# Pass args
# If args not pass - just create full report


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
    Generates a human-readable DISK usage info from ``psutil.disk_usage("/")``
    :return: A dict with 4 main fields (Total, Used, Free, Percent) and rounded disk usage
    """
    disk_usage = psutil.disk_usage("/")

    disk_util_mem = [
        disk_usage[idx] // (1024**3) for idx in range(len(disk_usage) - 1)
    ]
    disk_util_mem.append(disk_usage[-1])  # Add the percentage value (float)

    disk_util_kind = ["Total", "Used", "Free", "Used percent"]
    result = {disk_util_kind[idx]: disk_util_mem[idx] for idx in range(len(disk_usage))}

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


def get_swap_usage() -> Dict[str, Union[int, float]]:
    """
    Generates a human-readable SWAP usage info
    :return: A dict with 4 main fields (Total, Used, Free, Percent) and rounded swap usage
    """
    swap_usage = psutil.swap_memory()

    swap_usage_list = list(swap_usage)[:3]
    swap_usage_swap = [
        swap_usage_list[idx] // (1024**3) for idx in range(len(swap_usage_list))
    ]
    swap_usage_swap.append(swap_usage[3])

    swap_util_kind = ["Total", "Used", "Free", "Percent"]
    result = {
        swap_util_kind[idx]: swap_usage_swap[idx] for idx in range(len(swap_usage_swap))
    }

    return result


def swap_info(report_time: str):
    """
    Gather information about SWAP usage
    :param report_time:
    :return:
    """
    with codecs.open("report_" + report_time + ".md", "a", "utf-8") as report:
        report.write("### SWAP USAGE  \n")
        for key in get_swap_usage():
            if "percent" in key.lower():
                report.write(key + " : " + str(get_swap_usage()[key]) + "%  \n")
            else:
                report.write(key + " : " + str(get_swap_usage()[key]) + "GB  \n")
        report.write("\n")


def get_mem_usage() -> Dict[str, Union[int, float]]:
    """
    Generates a human-readable MEM usage info
    :return: A dict with 5 main fields (Total, Available, Used, Free, Percent) and rounded mem usage
    """
    mem_usage = psutil.virtual_memory()

    mem_percents = mem_usage[2]

    mem_usage_list = list(mem_usage[0:2] + mem_usage[3:5])

    mem_util_mem = [
        mem_usage_list[idx] // (1024**3) for idx in range(len(mem_usage_list))
    ]

    mem_util_mem.append(mem_percents)

    mem_util_kind = ["Total", "Available", "Used", "Free", "Percent"]
    result = {mem_util_kind[idx]: mem_util_mem[idx] for idx in range(len(mem_util_mem))}

    return result


# Use one method
def mem_info(report_time: str):
    """
    Gather information about MEM usage
    Call swap_info func which provide information about SWAP usage
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

    swap_info(report_time)


def network_interfaces_status(report_time: str):
    """
    Gather information about interfaces statuses
    :param report_time:
    :return:
    """
    net_activity = psutil.net_if_stats()
    with codecs.open("report_" + report_time + ".md", "a", "utf-8") as report:
        report.write("### INTERFACES STATUS  \n")
        for i in net_activity.items():
            report.write(
                "Connection Type Name: "
                + str(i[0])
                + " | UP: "
                + str(i[1][0])
                + " | Speed: "
                + str(i[1][2])
                + " MB"
                + " | MTU: "
                + str(i[1][3])
                + " bytes"
            )
            report.write("  \n")
        report.write("\n")


def net_info(report_time: str):
    """
    Gather information about NET usage
    Call network_interfaces_status func which provide interface statuses
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

    network_interfaces_status(report_time)


# print(psutil.test())


if __name__ == "__main__":
    timestamp = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
    general_info(timestamp)
    disk_info(timestamp)
    cpu_info(timestamp)
    mem_info(timestamp)
    net_info(timestamp)
