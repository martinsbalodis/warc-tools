"""Tests for http parsing."""
import unittest2

from hanzo.httptools.messaging import RequestMessage, ResponseMessage

get_request_lines = [
        "GET / HTTP/1.1",
        "Host: example.org",
        "",
        "",
        ]
get_request = "\r\n".join(get_request_lines)
get_response_lines = [
        "HTTP/1.1 200 OK",
        "Host: example.org",
        "Content-Length: 5",
        "",
        "tests",
        ]
get_response = "\r\n".join(get_response_lines)

class GetChar(unittest2.TestCase):
    """Test basic GET request parsing. Single character at a time."""
    def runTest(self):
        """Attempts to parse the contents of get_request and
        get_response."""
        p = RequestMessage()
        for t in get_request:
            text = p.feed(t)
            self.assertEqual(text, '')

        self.assertTrue(p.headers_complete())
        self.assertTrue(p.complete())

        self.assertEqual(get_request, p.get_decoded_message())

        p = ResponseMessage(p)
        for char in get_response:
            text = p.feed(char)
            self.assertEqual(text, '')

        self.assertTrue(p.headers_complete())
        self.assertTrue(p.complete())
        self.assertEqual(get_response, p.get_decoded_message())

class GetLines(unittest2.TestCase):
    """Test basic GET request parsing. Single line at a time."""
    def runTest(self):
        """Attempts to parse get_request_lines, i.e. get_request line
        at a time."""

        p = RequestMessage()
        for line in get_request_lines:
            text = p.feed(line)
            self.assertEqual(text, "")
            text = p.feed("\r\n")
            self.assertEqual(text, "")

        self.assertTrue(p.headers_complete())
        self.assertTrue(p.complete())

        self.assertEqual(get_request, p.get_decoded_message())

        p = ResponseMessage(p)
        for line in get_response_lines:
            text = p.feed(line)
            self.assertEqual(text, "")
            text = p.feed("\r\n")
            self.assertEqual(text, "")

        self.assertTrue(p.headers_complete())
        self.assertTrue(p.complete())
        
        self.assertEqual(get_response, p.get_decoded_message())

head_request = "\r\n".join( [
    "HEAD / HTTP/1.1",
    "Host: example.org",
    "",
    "",
])
head_response = "\r\n".join( [
    "HTTP/1.1 200 OK",
    "Host: example.org",
    "Content-Length: 5",
    "",
    "",
])


class HeadTest(unittest2.TestCase):

    def runTest(self):
        p = RequestMessage()
        text=p.feed(head_request)

        self.assertEqual(text, '')
        self.assertTrue(p.complete())
        self.assertEqual(head_request, p.get_decoded_message())
        
        p = ResponseMessage(p)
        text = p.feed(head_response)

        self.assertEqual(text, '')
        self.assertTrue(p.complete())
        self.assertEqual(head_response, p.get_decoded_message())

post_request = "\r\n".join( [
    "POST / HTTP/1.1",
    "Host: example.org",
    "Transfer-Encoding: chunked",
    "",
    "8",
    "abcdefgh",
    "0",
    "",
    "",
])
post_response = "\r\n".join( [
    "HTTP/1.1 100 Continue",
    "Host: example.org",
    "",
    "HTTP/1.0 204 No Content",
    "Date: now!",
    "",
    "",
])


class PostTest(unittest2.TestCase):

    def runTest(self):
        p = RequestMessage()
        text = p.feed(post_request)

        self.assertEqual(text, '')
        self.assertTrue(p.complete())

        p = ResponseMessage(p)
        text = p.feed(post_response)
        
        self.assertEqual(text, '')
        self.assertTrue(p.complete())


if __name__ == '__main__':
    unittest2.main()


