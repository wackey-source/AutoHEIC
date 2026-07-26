config = {}


def set_config(cfg):
    global config
    config = cfg.copy()


def get_config():
    return config
