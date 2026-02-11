"""
Unit tests for breach checker module.

Tests SHA-1 hashing, k-anonymity implementation, and API integration
using mocked responses.
"""

import pytest
from unittest.mock import patch, Mock
from securepass.core.breach import (
    _sha1_hash,
    _api_request,
    check_breach
)


class TestSHA1Hash:
    """Tests for _sha1_hash function."""
    
    def test_known_hash(self):
        """Test with known SHA-1 hash."""
        # "password" SHA-1 = 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8
        hash_result = _sha1_hash("password")
        assert hash_result == "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8"
    
    def test_uppercase_output(self):
        """Hash should be uppercase."""
        hash_result = _sha1_hash("test")
        assert hash_result.isupper()
    
    def test_hex_format(self):
        """Hash should be valid hexadecimal."""
        hash_result = _sha1_hash("test123")
        assert len(hash_result) == 40  # SHA-1 = 160 bits = 40 hex chars
        assert all(c in '0123456789ABCDEF' for c in hash_result)
    
    def test_empty_string(self):
        """Empty string should hash consistently."""
        hash_result = _sha1_hash("")
        # Empty string SHA-1 = DA39A3EE5E6B4B0D3255BFEF95601890AFD80709
        assert hash_result == "DA39A3EE5E6B4B0D3255BFEF95601890AFD80709"
    
    def test_different_inputs_different_hashes(self):
        """Different inputs should produce different hashes."""
        hash1 = _sha1_hash("password1")
        hash2 = _sha1_hash("password2")
        assert hash1 != hash2


class TestAPIRequest:
    """Tests for _api_request function (with mocked responses)."""
    
    @patch('securepass.core.breach.requests')
    def test_successful_request(self, mock_requests):
        """Test successful API request."""
        # Mock response
        mock_response = Mock()
        mock_response.text = "1E4C9B93F3F0682250B6CF8331B7EE68FD8:3861493\nABCDEF123456:100"
        mock_response.raise_for_status = Mock()
        mock_requests.get.return_value = mock_response
        
        # Make request
        suffixes = _api_request("5BAA6")
        
        # Verify
        assert len(suffixes) == 2
        assert suffixes[0] == ("1E4C9B93F3F0682250B6CF8331B7EE68FD8", 3861493)
        assert suffixes[1] == ("ABCDEF123456", 100)
    
    @patch('securepass.core.breach.requests')
    def test_request_headers(self, mock_requests):
        """Test that proper headers are sent."""
        mock_response = Mock()
        mock_response.text = ""
        mock_response.raise_for_status = Mock()
        mock_requests.get.return_value = mock_response
        
        _api_request("5BAA6")
        
        # Verify headers were set
        call_kwargs = mock_requests.get.call_args[1]
        assert 'headers' in call_kwargs
        assert 'User-Agent' in call_kwargs['headers']
    
    @patch('securepass.core.breach.requests')
    def test_timeout_handling(self, mock_requests):
        """Test timeout error handling."""
        mock_requests.Timeout = Exception  # Mock the Timeout exception class
        mock_requests.get.side_effect = mock_requests.Timeout("Timeout")
        mock_requests.RequestException = Exception
        
        with pytest.raises(Exception):
            _api_request("5BAA6", timeout=1)
    
    @patch('securepass.core.breach.requests')
    def test_connection_error_handling(self, mock_requests):
        """Test connection error handling."""
        mock_requests.ConnectionError = Exception
        mock_requests.get.side_effect = mock_requests.ConnectionError("No connection")
        mock_requests.RequestException = Exception
        
        with pytest.raises(Exception):
            _api_request("5BAA6")


class TestCheckBreach:
    """Tests for check_breach function (main integration)."""
    
    def test_empty_password(self):
        """Empty password should return (False, 0)."""
        is_breached, count = check_breach("")
        assert is_breached is False
        assert count == 0
    
    @patch('securepass.core.breach._api_request')
    def test_password_found_in_breach(self, mock_api):
        """Test password found in breach database."""
        # Mock API response for "password"
        # Hash: 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8
        # Prefix: 5BAA6
        # Suffix: 1E4C9B93F3F0682250B6CF8331B7EE68FD8
        mock_api.return_value = [
            ("1E4C9B93F3F0682250B6CF8331B7EE68FD8", 3861493),
            ("ABCDEF123456", 100)
        ]
        
        is_breached, count = check_breach("password")
        
        assert is_breached is True
        assert count == 3861493
        
        # Verify k-anonymity: only first 5 chars sent
        mock_api.assert_called_once()
        call_args = mock_api.call_args[0]
        assert call_args[0] == "5BAA6"
    
    @patch('securepass.core.breach._api_request')
    def test_password_not_found(self, mock_api):
        """Test password not in breach database."""
        # Mock API response with different suffixes
        mock_api.return_value = [
            ("ABCDEF123456", 100),
            ("FEDCBA654321", 50)
        ]
        
        is_breached, count = check_breach("uniquepassword123")
        
        assert is_breached is False
        assert count == 0
    
    @patch('securepass.core.breach._api_request')
    def test_k_anonymity_implementation(self, mock_api):
        """Test that k-anonymity is properly implemented."""
        mock_api.return_value = []
        
        # Check a password
        check_breach("testpassword")
        
        # Verify only first 5 chars of hash were sent
        call_args = mock_api.call_args[0]
        assert len(call_args[0]) == 5
    
    @patch('securepass.core.breach._api_request')
    def test_retry_on_failure(self, mock_api):
        """Test retry logic on failure."""
        # First two calls fail, third succeeds
        mock_api.side_effect = [
            Exception("Network error"),
            Exception("Network error"),
            []
        ]
        
        is_breached, count = check_breach("password", max_retries=3)
        
        # Should have retried and eventually returned (False, 0)
        assert mock_api.call_count == 3
        assert is_breached is False
        assert count == 0
    
    @patch('securepass.core.breach._api_request')
    def test_max_retries_exhausted(self, mock_api):
        """Test behavior when all retries fail."""
        mock_api.side_effect = Exception("Network error")
        
        # Should return (False, 0) after max retries
        is_breached, count = check_breach("password", max_retries=2)
        
        assert is_breached is False
        assert count == 0
        assert mock_api.call_count == 2
    
    @patch('securepass.core.breach._api_request')
    def test_case_sensitivity_hash_matching(self, mock_api):
        """Test that hash matching is case-sensitive (as it should be)."""
        # Mock with lowercase suffix
        mock_api.return_value = [
            ("1e4c9b93f3f0682250b6cf8331b7ee68fd8", 100)  # lowercase
        ]
        
        is_breached, count = check_breach("password")
        
        # Should not match because our hash is uppercase
        # and the mock returned lowercase
        assert is_breached is False
