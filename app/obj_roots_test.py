def resolve_common(expected_params):
    import datetime
    return {
        'now': lambda: datetime.datetime(2000, 1, 1)
    }


def resolve_IndexView(expected_params):
    return {
        'service1': 'testService1',
        'service2': 'testService2',
    }
