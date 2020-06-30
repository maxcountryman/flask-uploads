class UploadNotAllowed(Exception):
    """This exception is raised if the upload was not allowed.

    You should catch it in your view code and
    display an appropriate message to the user.
    """
