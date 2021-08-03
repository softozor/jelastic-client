class JelasticClientException(Exception):
    """
    Generic Jelastic Client Exception
    """

    pass


class ApiClientException(JelasticClientException):
    """
    Low-level API Exception
    """

    pass
