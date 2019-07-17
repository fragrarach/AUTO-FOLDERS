import re
from quatro import log


# Split payload string, return named variables
def payload_handler(raw_payload):
    log(raw_payload)
    split_payload = raw_payload.split("], [")
    record_type = split_payload[0][1:]
    reference = split_payload[1]
    sigm_string = split_payload[-1][:-1]
    user = re.findall(r'(?<=aSIGMWIN\.EXE u)(.*)(?= m)', sigm_string)[0]
    station = re.findall(r'(?<= w)(.*)$', sigm_string)[0]
    return record_type, reference, user, station
