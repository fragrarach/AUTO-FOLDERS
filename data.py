import re


# Split payload string, return named variables
def payload_handler(payload):
    record_type = payload.split("], [")[0][1:]
    reference = payload.split("], [")[1]
    sigm_string = payload.split("], [")[-1][:-1]
    user = re.findall(r'(?<=aSIGMWIN\.EXE u)(.*)(?= m)', sigm_string)[0]
    station = re.findall(r'(?<= w)(.*)$', sigm_string)[0]
    return record_type, reference, user, station
