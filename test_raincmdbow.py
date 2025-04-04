import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
from raincmdbow import rgb_to_ansi, rainbow_screen, rainbow_pipe

@pytest.fixture
def test_params():
    """Set up test parameters."""
    return {
        'delay': 0.05,
        'increment': 0.1,
        'char': '█',
        'saturation': 1.0,
        'brightness': 1.0,
        'reverse': False
    }

def test_rgb_to_ansi():
    """Test RGB to ANSI color code conversion."""
    test_cases = [
        ((1.0, 0.0, 0.0), "\033[38;2;255;0;0m"),
        ((0.0, 1.0, 0.0), "\033[38;2;0;255;0m"),
        ((0.0, 0.0, 1.0), "\033[38;2;0;0;255m"),
        ((0.0, 0.0, 0.0), "\033[38;2;0;0;0m"),
        ((1.0, 1.0, 1.0), "\033[38;2;255;255;255m")
    ]
    for rgb, expected in test_cases:
        assert rgb_to_ansi(*rgb) == expected

@patch('sys.stdout', new_callable=StringIO)
@patch('os.popen')
def test_rainbow_screen(mock_popen, mock_stdout, test_params):
    """Test rainbow screen generation."""
    # Mock terminal size
    mock_popen.return_value.read.return_value = "24 80"
    
    with patch('time.sleep') as mock_sleep:
        rainbow_screen(**test_params)
        
        # Verify output contains ANSI codes and character
        output = mock_stdout.getvalue()
        assert test_params['char'] in output
        assert "\033[38;2" in output
        assert "\033[0m" in output
        
        # Verify sleep was called
        mock_sleep.assert_called_with(test_params['delay'])

@patch('sys.stdin', new_callable=StringIO)
@patch('sys.stdout', new_callable=StringIO)
def test_rainbow_pipe(mock_stdout, mock_stdin, test_params):
    """Test pipe mode with sample input."""
    test_input = "Hello, Rainbow!\n"
    mock_stdin.write(test_input)
    mock_stdin.seek(0)
    
    with patch('time.sleep') as mock_sleep:
        rainbow_pipe(
            test_params['delay'],
            test_params['increment'],
            test_params['saturation'],
            test_params['brightness'],
            test_params['reverse']
        )
        
        # Verify output contains input text and color codes
        output = mock_stdout.getvalue()
        assert "\033[38;2" in output
        assert "\033[0m" in output
        
        # Remove ANSI codes to check text
        clean_output = output.replace("\033[0m", "")
        for char in test_input:
            assert char in clean_output

def test_invalid_parameters(test_params):
    """Test parameter validation."""
    with pytest.raises(ValueError):
        rainbow_screen(delay=-1, **{k:v for k,v in test_params.items() if k != 'delay'})
    
    with pytest.raises(ValueError):
        rainbow_screen(saturation=2.0, **{k:v for k,v in test_params.items() if k != 'saturation'})