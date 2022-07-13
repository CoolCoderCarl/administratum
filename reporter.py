import argparse
import codecs
import json
import platform
import sys
import time
from datetime import datetime
from typing import Dict, Union

import psutil
import requests
import speedtest


def get_args():
    """
    Get arguments from CLI
    :return:
    """
    root_parser = argparse.ArgumentParser(
        prog="internet_checker",
        description="""Report about the castle""",
        epilog="""(c) CoolCoderCarl""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    root_parser.add_argument("--disk", action=argparse.BooleanOptionalAction)
    root_parser.add_argument("--cpu", action=argparse.BooleanOptionalAction)
    root_parser.add_argument("--mem", action=argparse.BooleanOptionalAction)
    root_parser.add_argument("--net", action=argparse.BooleanOptionalAction)

    # report.add_argument("-v", "--verbosity", action=argparse.BooleanOptionalAction)

    return root_parser


# Shortening
namespace = get_args().parse_args(sys.argv[1:])

# Start time
start_time = time.time()

# Using in provider_info func to retrieve information about provider
IP_SITE = "http://ipinfo.io/"

timestamp = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")


def general_info(report_time: str):
    """
    Gather general info about host system
    :param report_time:
    :return:
    """
    print("General info providing...")
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
    print("--- %s seconds ---" % (time.time() - start_time))
    print("General info provided.")


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
    print("Disk info providing...")
    with codecs.open("report_" + report_time + ".md", "a", "utf-8") as report:
        report.write("## DISK USAGE  \n")
        for key in get_disk_usage():
            if "percent" in key.lower():
                report.write(key + " : " + str(get_disk_usage()[key]) + "%  \n")
            else:
                report.write(key + " : " + str(get_disk_usage()[key]) + "GB  \n")
        report.write("\n")
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Disk info provided.")


def cpu_info(report_time: str):
    """
    Gather information about CPU usage
    :param report_time:
    :return:
    """
    print("CPU info providing...")
    with codecs.open("report_" + report_time + ".md", "a", "utf-8") as report:
        report.write("## CPU USAGE  \n")
        report.write("Logical processors: " + str(psutil.cpu_count()) + "  \n")
        report.write("Frequency: " + str(psutil.cpu_freq()[0]) + "  \n")
        report.write("\n")
    print("--- %s seconds ---" % (time.time() - start_time))
    print("CPU info provided.")


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
    print("SWAP info providing...")
    with codecs.open("report_" + report_time + ".md", "a", "utf-8") as report:
        report.write("### SWAP USAGE  \n")
        for key in get_swap_usage():
            if "percent" in key.lower():
                report.write(key + " : " + str(get_swap_usage()[key]) + "%  \n")
            else:
                report.write(key + " : " + str(get_swap_usage()[key]) + "GB  \n")
        report.write("\n")
    print("--- %s seconds ---" % (time.time() - start_time))
    print("SWAP info provided.")


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
    print("Memory info providing...")
    with codecs.open("report_" + report_time + ".md", "a", "utf-8") as report:
        report.write("## MEMORY USAGE  \n")
        for key in get_mem_usage():
            if "percent" in key.lower():
                report.write(key + " : " + str(get_mem_usage()[key]) + "%  \n")
            else:
                report.write(key + " : " + str(get_mem_usage()[key]) + "GB  \n")
        report.write("\n")

    swap_info(report_time)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Memory info provided.")


def network_interfaces_status(report_time: str):
    """
    Gather information about interfaces statuses
    :param report_time:
    :return:
    """
    print("Network interfaces info providing...")
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
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Network interfaces info provided.")


def isp_info(report_time: str):
    """
    Get ISP info & write down to report file
    Try-expect in case of connection error
    :param report_time:
    :return:
    """
    print("ISP info providing...")
    with codecs.open("report_" + report_time + ".md", "a", "utf-8") as report:
        report.write("### ISP INFO  \n")
        try:
            get_provider_info = json.loads(requests.get(IP_SITE).text)
            ignored_value = ["city", "region", "loc", "postal", "readme"]
            for k, v in get_provider_info.items():
                if k not in ignored_value:
                    if k == "ip":
                        report.write(k.upper() + ": " + v + "  \n")
                    else:
                        report.write(k.capitalize() + ": " + v + "  \n")
            report.write("\n")
        except ConnectionError as connection_error:
            report.write(str(connection_error))
            report.write("\n")

    print("--- %s seconds ---" % (time.time() - start_time))
    print("ISP info provided.")


def network_speed(report_time: str):
    """
    Report about upload and download speed of internet connection
    :param report_time:
    :return:
    """
    print("Network speed info providing...")
    speed_test = speedtest.Speedtest()
    download_speed = speed_test.download()
    upload_speed = speed_test.upload(pre_allocate=False)
    with codecs.open("report_" + report_time + ".md", "a", "utf-8") as report:
        report.write("### NETWORK SPEED  \n")
        report.write(
            "#### DOWNLOAD  \n"
            + str(int(download_speed))
            + " bytes. "
            + str(int(download_speed / 1024))
            + " MB."
            + "  \n"
        )
        report.write(
            "#### UPLOAD  \n"
            + str(int(upload_speed))
            + " bytes. "
            + str((upload_speed / 1024))
            + " MB."
            + "  \n"
        )
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Network speed info provided.")


def net_info(report_time: str):
    """
    Gather information about NET usage
    Call network_interfaces_status func which provide interface statuses
    Call provider_info func which provide information about provider, some info were ignored
    Call network_speed func which provide information about upload & download internet connection speed
    :param report_time:
    :return:
    """
    print("Network info providing...")
    with codecs.open("report_" + report_time + ".md", "a", "utf-8") as report:
        report.write("## NETWORK USAGE  \n")
        net_if_address = psutil.net_if_addrs()
        for i in net_if_address:
            report.write(i + "  \n")
            # print(net_if_address[i][1])
            report.write(str(net_if_address[i][1][1:3]) + "  \n")
        report.write("\n")

    network_interfaces_status(report_time)
    isp_info(timestamp)
    network_speed(report_time)

    print("--- %s seconds ---" % (time.time() - start_time))
    print("Network info provided.")


# print(psutil.cpu_times_percent())
# print(psutil.test())


if __name__ == "__main__":
    # Fix excluding
    if not (sys.argv[1:]):
        general_info(timestamp)
        disk_info(timestamp)
        cpu_info(timestamp)
        mem_info(timestamp)
        net_info(timestamp)
    else:
        general_info(timestamp)
        if namespace.disk:
            disk_info(timestamp)
        if namespace.cpu:
            cpu_info(timestamp)
        if namespace.mem:
            mem_info(timestamp)
        if namespace.net:
            net_info(timestamp)
