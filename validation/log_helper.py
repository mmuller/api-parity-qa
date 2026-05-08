import os
import time
from datetime import datetime
from validation.config import LOG_PATH
import re


class LogHelper:

    LOG_FILE = LOG_PATH

    @staticmethod
    def get_logs():
        if not os.path.exists(LogHelper.LOG_FILE):
            return ""

        with open(LogHelper.LOG_FILE, "r") as f:
            return f.read()

    @staticmethod
    def get_logs_since(start_time):
        if not os.path.exists(LogHelper.LOG_FILE):
            return ""

        logs = []

        with open(LogHelper.LOG_FILE, "r") as f:
            for line in f:
                try:
                    timestamp_str = line[:23]
                    log_time = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")

                    if log_time >= start_time.replace(tzinfo=None):
                        logs.append(line)

                except Exception:
                    continue

        return "".join(logs)

    @staticmethod
    def wait_for_logs_since(start_time, timeout=3, interval=0.2):
        start = time.time()

        while time.time() - start < timeout:
            logs = LogHelper.get_logs_since(start_time)

            if logs:
                return logs

            time.sleep(interval)

        return ""

    @staticmethod
    def extract_correlation_ids(logs: str):
        pattern = r"\[corr_id=(.*?)\]"
        return re.findall(pattern, logs)
