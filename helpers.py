import yaml


def get_data_from_yaml(path):
    with open(path) as f:
        return yaml.load(f)

def dict_union(left, right):
    return dict(left, **right)