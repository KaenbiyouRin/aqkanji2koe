"""
Core implementation of AqKanji2Koe wrapper.
"""

import ctypes
import os
import sys
from typing import Optional, Union

class AquesTalkError(Exception):
    """Base exception for AquesTalk related errors."""
    def __init__(self, message: str, error_code: int = 0):
        self.error_code = error_code
        super().__init__(f"{message} (Error code: {error_code})")

class AqKanji2Koe:
    """
    Main class for interfacing with AqKanji2Koe library.
    
    This class provides a Pythonic interface to convert Japanese text
    to phoneme strings using AquesTalk's AqKanji2Koe library.
    """
    
    # DLL loading strategies for different platforms
    _dll_names = {
        'win32': ['AqKanji2Koe.dll', 'libAqKanji2Koe.dll'],
        'linux': ['libAqKanji2Koe.so', 'libAqKanji2Koe.so.1'],
        'darwin': ['libAqKanji2Koe.dylib', 'libAqKanji2Koe.so']
    }
    
    def __init__(self, dict_dir: str, dll_path: Optional[str] = None):
        """
        Initialize the AqKanji2Koe converter.
        
        Args:
            dict_dir: Directory containing the dictionary files (aqdic.bin)
            dll_path: Optional explicit path to the AqKanji2Koe library.
                     If not provided, will search in common locations.
        
        Raises:
            AquesTalkError: If initialization fails
            FileNotFoundError: If dictionary directory doesn't exist
        """
        # Validate dictionary directory
        if not os.path.isdir(dict_dir):
            raise FileNotFoundError(f"Dictionary directory not found: {dict_dir}")
        
        dict_path = os.path.join(dict_dir, "aqdic.bin")
        if not os.path.isfile(dict_path):
            raise FileNotFoundError(f"System dictionary not found: {dict_path}")
        
        self._dict_dir = os.path.abspath(dict_dir)
        self._handle = None
        self._dll = None
        
        try:
            # Load DLL
            self._dll = self._load_dll(dll_path)
            
            # Configure function prototypes
            self._configure_functions()
            
            # Initialize library
            self._initialize()
            
        except Exception as e:
            # Clean up on failure
            if self._handle:
                self._release_internal()
            raise AquesTalkError(f"Failed to initialize AqKanji2Koe: {e}")
    
    def _load_dll(self, dll_path: Optional[str] = None) -> ctypes.CDLL:
        """Load the AqKanji2Koe DLL/shared library."""
        if dll_path:
            paths = [dll_path]
        else:
            # Try platform-specific names
            platform = sys.platform
            dll_candidates = self._dll_names.get(platform, [])
            
            # Search in various locations
            paths = []
            for name in dll_candidates:
                paths.extend([
                    name,  # Current directory
                    os.path.join(os.path.dirname(__file__), name),
                    os.path.join(self._dict_dir, name),
                    os.path.join(os.path.dirname(sys.executable), name),
                    os.path.join(os.path.dirname(sys.executable), "lib", name),
                ])
        
        last_error = None
        for path in paths:
            try:
                return ctypes.CDLL(path)
            except OSError as e:
                last_error = e
                continue
        
        raise AquesTalkError(
            f"Could not load AqKanji2Koe library. "
            f"Tried: {', '.join(paths)}. "
            f"Last error: {last_error}"
        )
    
    def _configure_functions(self):
        """Configure the DLL function prototypes."""
        # AqKanji2Koe_Create
        self._dll.AqKanji2Koe_Create.argtypes = [
            ctypes.c_char_p,
            ctypes.POINTER(ctypes.c_int)
        ]
        self._dll.AqKanji2Koe_Create.restype = ctypes.c_void_p
        
        # AqKanji2Koe_Release
        self._dll.AqKanji2Koe_Release.argtypes = [ctypes.c_void_p]
        self._dll.AqKanji2Koe_Release.restype = None
        
        # AqKanji2Koe_Convert_utf8
        self._dll.AqKanji2Koe_Convert_utf8.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_int
        ]
        self._dll.AqKanji2Koe_Convert_utf8.restype = ctypes.c_int
        
        # AqKanji2Koe_Convert_sjis
        self._dll.AqKanji2Koe_Convert_sjis.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_int
        ]
        self._dll.AqKanji2Koe_Convert_sjis.restype = ctypes.c_int
        
        # AqKanji2Koe_SetDevKey
        self._dll.AqKanji2Koe_SetDevKey.argtypes = [ctypes.c_char_p]
        self._dll.AqKanji2Koe_SetDevKey.restype = ctypes.c_int
    
    def _initialize(self):
        """Initialize the library and create handle."""
        # Ensure directory ends with separator
        dict_path = self._dict_dir
        if not dict_path.endswith(os.sep):
            dict_path += os.sep
        
        err = ctypes.c_int(0)
        dict_path_bytes = dict_path.encode('utf-8')
        
        self._handle = self._dll.AqKanji2Koe_Create(
            dict_path_bytes,
            ctypes.byref(err)
        )
        
        if self._handle is None or err.value != 0:
            raise AquesTalkError(
                "Failed to create AqKanji2Koe instance",
                error_code=err.value
            )
    
    def _release_internal(self):
        """Internal method to release resources."""
        if self._handle:
            self._dll.AqKanji2Koe_Release(self._handle)
            self._handle = None
    
    def convert(self, text: str, encoding: str = 'utf-8', 
                buffer_size: int = 1024) -> str:
        """
        Convert Japanese text to phoneme string.
        
        Args:
            text: Japanese text to convert
            encoding: Input text encoding ('utf-8' or 'sjis')
            buffer_size: Size of output buffer
        
        Returns:
            Phoneme string in UTF-8 encoding
        
        Raises:
            AquesTalkError: If conversion fails
            ValueError: If encoding is not supported
        """
        if not self._handle:
            raise AquesTalkError("Converter not initialized or already released")
        
        # Validate encoding
        encoding = encoding.lower()
        if encoding not in ('utf-8', 'sjis', 'shift-jis', 'shift_jis'):
            raise ValueError(
                f"Unsupported encoding: {encoding}. "
                "Supported: 'utf-8', 'sjis'"
            )
        
        # Prepare input text
        if encoding == 'utf-8':
            text_bytes = text.encode('utf-8')
            convert_func = self._dll.AqKanji2Koe_Convert_utf8
        else:  # Shift-JIS
            # Try different Shift-JIS encodings
            for sjis_enc in ('cp932', 'shift_jis', 'shift-jis'):
                try:
                    text_bytes = text.encode(sjis_enc)
                    break
                except UnicodeEncodeError:
                    continue
            else:
                raise ValueError("Failed to encode text as Shift-JIS")
            convert_func = self._dll.AqKanji2Koe_Convert_sjis
        
        # Prepare output buffer
        output_buf = ctypes.create_string_buffer(buffer_size)
        
        # Perform conversion
        result = convert_func(
            self._handle,
            text_bytes,
            output_buf,
            buffer_size
        )
        
        if result != 0:
            raise AquesTalkError(
                "Text conversion failed",
                error_code=result
            )
        
        # Decode and clean output
        output = output_buf.value.decode('utf-8', errors='ignore')
        return output.rstrip('\x00')
    
    def set_developer_key(self, key: str) -> bool:
        """
        Set developer key for the library.
        
        Args:
            key: Developer key string
        
        Returns:
            True if successful, False otherwise
        """
        if not self._handle:
            return False
        
        if isinstance(key, str):
            key_bytes = key.encode('utf-8')
        else:
            key_bytes = key
        
        result = self._dll.AqKanji2Koe_SetDevKey(key_bytes)
        return result == 0
    
    def release(self):
        """Explicitly release library resources."""
        self._release_internal()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - auto release resources."""
        self.release()
    
    def __del__(self):
        """Destructor."""
        try:
            self.release()
        except:
            pass
    
    @property
    def is_initialized(self) -> bool:
        """Check if converter is properly initialized."""
        return self._handle is not None
    
    @property
    def dictionary_directory(self) -> str:
        """Get the dictionary directory path."""
        return self._dict_dir