"""TestingFileStorage is intended to be used by users of `Flask-Reuploaded`

This means:
    - the name cannot be changed easily
    - it has to be importable
    - it can't be moved in the tests directory
"""
from typing import IO
from typing import Any
from typing import Optional

from werkzeug.datastructures import FileStorage


class TestingFileStorage(FileStorage):
    """
    This is a helper for testing upload behavior in your application. You
    can manually create it, and its save method is overloaded to set `saved`
    to the name of the file it was saved to. All of these parameters are
    optional, so only bother setting the ones relevant to your application.

    :param stream: A stream. The default is an empty stream.
    :param filename: The filename uploaded from the client. The default is the
                     stream's name.
    :param name: The name of the form field it was loaded from. The default is
                 `None`.
    :param content_type: The content type it was uploaded as. The default is
                         ``application/octet-stream``.
    :param content_length: How long it is. The default is -1.
    :param headers: Multipart headers as a `werkzeug.Headers`. The default is
                    `None`.
    """
    def __init__(
        self,
        stream: Optional[IO[bytes]] = None,
        filename: Optional[str] = None,
        name: Optional[str] = None,
        content_type: str = 'application/octet-stream',
        content_length: int = -1,
        headers: Optional[Any] = None
    ) -> None:
        FileStorage.__init__(
            self,
            stream,
            filename,
            name=name,
            content_type=content_type,
            content_length=content_length,
            headers=None
        )
        self.saved = None  # type: Optional[str]

    def save(self, dst: str, buffer_size: int = 16384) -> None:  # type: ignore
        """This marks the file as saved.

        The `saved` attribute gets set to the destination.

        Although unused, `buffer_size` is required to stay compatible
        with the signature of `werkzeug.datastructures.FileStorage.save`.

        :param dst: The destination file name or path.
        :param buffer_size: Ignored.
        """
        if isinstance(dst, str):
            self.saved = dst
        else:
            # currently kept for compatibility with Flask-Uploads
            raise RuntimeError(
                "dst currently has to be a `str`")  # pragma: no cover
