from utils import *

"""Tests for 'clean_url(url: str) -> str'"""
def test_clean_url_https():
    assert clean_url("https://example.com/") == "https://example.com/"

def test_clean_url_http():
    assert clean_url("http://example.com/") == "http://example.com/"

def test_clean_url_www():
    assert clean_url("https://www.example.com/") == "https://example.com/"

def test_clean_url_question():
    assert clean_url("https://example.com?watch=v") == "https://example.com/"

def test_clean_url_hash():
    assert clean_url("https://example.com#watch=v") == "https://example.com/"

def test_clean_url_pages():
    assert clean_url("https://example.com/home/input") == "https://example.com/"