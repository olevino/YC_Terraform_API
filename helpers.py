import yaml


def get_data_from_yaml(path):
    with open(path) as f:
        return yaml.load(f)


def dict_union(left, right):
    return dict(left, **right)


def filter_error_log(lines):
    new_lines = []

    for line in lines:
        if line in ["\x1b[31m\n", "\x1b[0m\x1b[0m\n", "\x1b[0m\n", "\n"]:
            continue

        line = line.replace('\x1b[1m\x1b[31m', '')
        line = line.replace('\x1b[0m\x1b[0m\x1b[1m', '')
        line = line.replace('\x1b[0m', '')
        line = line.replace('\x1b[4m{', '')

        new_lines.append(line)
    return new_lines


def filter_output_log(lines):
    return [line.replace("\x1b[0m", "").replace("\x1b[1m", "") for line in lines]


def filter_outputs(lines):
    for item in lines:
        item["value"] = item["value"].replace("\x1b[0m", "").replace("\x1b[1m", "")
    return lines
