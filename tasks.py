import data
import files


def listen_task(config, notify):
    raw_payload = notify.payload

    record_type, reference, user, station = data.payload_handler(raw_payload)

    if record_type != 'PRT RENAME':
        directory = files.create_dir(config, record_type, reference)
        # Additional files/folders for parts
        if record_type == 'PRT':
            prt_no = reference
            prt_folder = directory
            files.extend_dir(config, prt_no, prt_folder)
    else:
        old_prt_no = reference.split("}, {")[0][1:]
        new_prt_no = reference.split("}, {")[1][:-1]
        files.rename_prt_no(config, old_prt_no, new_prt_no)
