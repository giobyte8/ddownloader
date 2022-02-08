from unittest.mock import patch
import pytest
import requests

from ddownloader import downloader
from ddownloader.downloader import UrlMetadata
from ddownloader.errors import MetadataReqError

# pylint: disable=R0201
class TestUrlMetadata:
    test_url = 'http://random.com/somefile.png'
    test_url_no_extension = 'http://random.com/somefile'

    def test_compute_filename_content_disposition(self):
        meta = UrlMetadata(self.test_url)
        meta.content_disposition = 'attachment;filename="testfilename.xyz"'

        meta.compute_file_name()
        assert 'testfilename.xyz' == meta.proposed_file_name

    def test_compute_filename_content_disposition_no_filename(self):
        meta = UrlMetadata(self.test_url)
        meta.content_disposition = 'attachment;'

        meta.compute_file_name()
        assert 'somefile.png' == meta.proposed_file_name

    @patch('ddownloader.downloader.uuid.uuid4')
    def test_compute_filename_uuid(self, mock_uuid4):
        uuidname = 'uuidname'
        mock_uuid4.return_value = uuidname

        meta = UrlMetadata('http://random.com/')

        meta.compute_file_name()
        assert uuidname == meta.proposed_file_name

    def test_compute_filename_jpeg_extension(self):
        meta = UrlMetadata(self.test_url_no_extension)
        meta.content_type = 'image/jpeg'

        meta.compute_file_name()
        assert 'somefile.jpeg' == meta.proposed_file_name

    def test_compute_filename_jpg_extension(self):
        meta = UrlMetadata(self.test_url_no_extension)
        meta.content_type = 'image/jpg'

        meta.compute_file_name()
        assert 'somefile.jpg' == meta.proposed_file_name

    def test_compute_filename_png_extension(self):
        meta = UrlMetadata(self.test_url_no_extension)
        meta.content_type = 'image/png'

        meta.compute_file_name()
        assert 'somefile.png' == meta.proposed_file_name


# pylint: disable=R0201
class TestMetadataReq:

    @patch('ddownloader.downloader.requests.head')
    def test_conn_error(self, mock_head):
        mock_head.side_effect = requests.exceptions.ConnectionError

        with pytest.raises(MetadataReqError):
            downloader.metadata('testurl.com')

    @patch('ddownloader.downloader.requests.head')
    def test_timeout_error(self, mock_head):
        mock_head.side_effect = requests.exceptions.Timeout

        with pytest.raises(MetadataReqError):
            downloader.metadata('testurl.com')

    @patch('ddownloader.downloader.requests.head')
    def test_too_many_redirects_error(self, mock_head):
        mock_head.side_effect = requests.exceptions.TooManyRedirects

        with pytest.raises(MetadataReqError):
            downloader.metadata('testurl.com')

    @patch('ddownloader.downloader.requests.head')
    def test_http_error(self, mock_head):
        mock_head.side_effect = requests.exceptions.HTTPError

        with pytest.raises(MetadataReqError):
            downloader.metadata('testurl.com')
