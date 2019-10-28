import data
import files
from quatro import log


def listen_task(config, notify):
    raw_payload = notify.payload

    record_type, reference, user, station = data.payload_handler(raw_payload)

    try:
        if not any(i in reference for i in ('<', '>', ':', '"', '/', '\\', '|', '?', '*')):
            if record_type not in ['PRT RENAME', 'CLI RENAME']:
                directory = files.create_dir(config, record_type, reference)
                # Additional files/folders for parts
                if record_type == 'PRT':
                    prt_no = reference
                    prt_folder = directory
                    files.extend_dir(config, prt_no, prt_folder)
            elif record_type == 'PRT RENAME':
                old_prt_no = reference.split("}, {")[0][1:]
                new_prt_no = reference.split("}, {")[1][:-1]
                files.rename_prt_no(config, old_prt_no, new_prt_no)
            elif record_type == 'CLI RENAME':
                old_cli_no = reference.split("}, {")[0][1:]
                new_cli_no = reference.split("}, {")[1][:-1]
                files.rename_cli_no(config, old_cli_no, new_cli_no)
        else:
            log(f'{record_type} {reference} includes illegal character')
    except:
        pass
