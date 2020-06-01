class UploadConfiguration:
    """
    This holds the configuration for a single `UploadSet`. The constructor's
    arguments are also the attributes.

    :param destination: The directory to save files to.
    :param base_url: The URL (ending with a /) that files can be downloaded
                     from. If this is `None`, Flask-Uploads will serve the
                     files itself.
    :param allow: A list of extensions to allow, even if they're not in the
                  `UploadSet` extensions list.
    :param deny: A list of extensions to deny, even if they are in the
                 `UploadSet` extensions list.
    """

    def __init__(self, destination, base_url=None, allow=(), deny=()):
        self.destination = destination
        self.base_url = base_url
        self.allow = allow
        self.deny = deny

    @property
    def _tuple(self):
        return (self.destination, self.base_url, self.allow, self.deny)

    def __eq__(self, other):
        return self._tuple == other._tuple
