try:
    import config_private as config
except ImportError:
    try:
        import config as config
    except ImportError:
        print("No configuration file found.")
        config = None
