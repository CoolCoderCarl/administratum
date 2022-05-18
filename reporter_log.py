import logging
import os

report = "reporter.log"


def log_init():
    if not os.path.exists(report):
        os.makedirs(report)

    logging.basicConfig(
        filename=report,
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logging.info("PID:" + str(os.getpid()))

    print("Log initiated")


def make_logs():
    logging.info("OS name " + os.name)
    logging.info("Current work dir " + os.getcwd())
