"""Provides default and calculated paths to required directories and files."""
from __future__ import annotations

import functools
import logging
import os
import pathlib
import shutil
import sys

import platformdirs

from screenshot_ocr import utils

logger = logging.getLogger(__name__)


class DefaultPaths:
    """Provides default paths for known locations."""

    is_win = sys.platform.startswith("win")

    def __init__(self, allow_not_exist: bool = False) -> None:
        """Create a new instance.

        Args:
            allow_not_exist: Whether to allow files or folders to not exist.
        """
        self._allow_not_exist = allow_not_exist
        self._platform_dirs = platformdirs.PlatformDirs(
            utils.get_name_dash(),
            utils.get_author_dash(),
            ensure_exists=True,
        )

    @functools.cached_property
    def downloads_dir(self) -> pathlib.Path | None:
        """Get the Downloads directory.

        Returns:
            The Downloads directory, if known.
        """
        # result = self._platform_dirs.user_downloads_path
        result = self._get_user_downloads_dir_win_guess()
        if result:
            return result
        return self._get_user_downloads_dir_win_reg()

    @functools.cached_property
    def documents_dir(self) -> pathlib.Path | None:
        """Get the Documents directory.

        Returns:
            The Documents directory, if known.
        """
        result = self._platform_dirs.user_documents_path
        return self._get_path("Documents directory", "default user directories", result)

    @functools.cached_property
    def google_credentials_file(self) -> pathlib.Path | None:
        """Get the Google credentials file.

        Returns:
            The Google credentials file, if known.
        """
        result = self._platform_dirs.user_config_path
        return self._get_path(
            "Google credentials file",
            "default user config directory",
            result,
            "credentials.json",
        )

    @functools.cached_property
    def google_token_file(self) -> pathlib.Path | None:
        """Get the Google token file.

        Returns:
            The Google token file, if known.
        """
        result = self._platform_dirs.user_config_path
        return self._get_path(
            "Google token file",
            "default user config directory",
            result,
            "token.json",
        )

    @functools.cached_property
    def tesseract_exe_file(self) -> pathlib.Path | None:
        """Get the Tesseract executable file.

        Returns:
            The Tesseract executable file, if known.
        """
        available = [
            self._tesseract_exe_which_unix,
            self._tesseract_exe_which_windows,
            self._tesseract_exe_default_unix,
            self._tesseract_exe_winreg,
            self._tesseract_exe_default_win,
        ]
        for available_func in available:
            result = available_func()
            if result:
                return result
        return None

    @functools.cached_property
    def tesseract_data_file(self) -> pathlib.Path | None:
        """Get the Tesseract data directory.

        Returns:
            The Tesseract data directory, if known.
        """
        available = [
            self._tesseract_data_default_unix,
            self._tesseract_data_winreg,
            self._tesseract_data_default_win,
        ]
        for available_func in available:
            result = available_func()
            if result:
                return result
        return None

    def _tesseract_exe_which_unix(self) -> pathlib.Path | None:
        if self.is_win:
            return None
        exe_name = "tesseract"
        result = shutil.which(exe_name)
        if not result:
            return None

        return self._get_path(
            "tesseract executable",
            f"which {exe_name}",
            pathlib.Path(result),
        )

    def _tesseract_exe_which_windows(self) -> pathlib.Path | None:
        if not self.is_win:
            return None
        exe_name = "tesseract.exe"
        result = shutil.which(exe_name)
        if not result:
            return None

        return self._get_path(
            "tesseract executable",
            f"which {exe_name}",
            pathlib.Path(result),
        )

    def _tesseract_exe_default_unix(self) -> pathlib.Path | None:
        if self.is_win:
            return None
        result = pathlib.Path("/usr/bin/tesseract")
        return self._get_path(
            "tesseract executable",
            "default install path",
            result,
        )

    def _tesseract_exe_winreg(self) -> pathlib.Path | None:
        result = self._tesseract_install_dir_winreg()
        if not result:
            return None
        return self._get_path(
            "tesseract executable",
            "Windows install information",
            result,
            "tesseract.exe",
        )

    def _tesseract_exe_default_win(self) -> pathlib.Path | None:
        result = self._tesseract_install_dir_default()
        if not result:
            return None
        return self._get_path(
            "tesseract executable",
            "default install path",
            result,
            "tesseract.exe",
        )

    def _tesseract_data_default_unix(self) -> pathlib.Path | None:
        if self.is_win:
            return None
        result = pathlib.Path("/usr/share/tesseract-ocr/4.00/tessdata")
        return self._get_path(
            "tesseract data",
            "default install path",
            result,
        )

    def _tesseract_data_winreg(self) -> pathlib.Path | None:
        result = self._tesseract_install_dir_winreg()
        if not result:
            return None
        return self._get_path(
            "tesseract data",
            "Windows install information",
            result,
            "tessdata",
        )

    def _tesseract_data_default_win(self) -> pathlib.Path | None:
        result = self._tesseract_install_dir_default()
        if not result:
            return None
        return self._get_path(
            "tesseract data",
            "default install path",
            result,
            "tessdata",
        )

    def _tesseract_install_dir_winreg(self) -> pathlib.Path | None:
        try:
            import winreg

            tree_root = winreg.HKEY_LOCAL_MACHINE
            tree_leaf = winreg.OpenKeyEx(tree_root, r"SOFTWARE\\Tesseract-OCR\\")
            key_value, key_type = winreg.QueryValueEx(tree_leaf, "InstallDir")
            if tree_leaf:
                winreg.CloseKey(tree_leaf)

            if key_value and key_type == winreg.REG_SZ:
                return pathlib.Path(key_value)

        except ImportError:
            pass

        return None

    def _tesseract_install_dir_default(self) -> pathlib.Path | None:
        name = "Tesseract-OCR"
        available = [
            os.environ.get("PROGRAMFILES"),
            os.environ.get("PROGRAMFILES(X86)"),
        ]
        for available_item in available:
            if not available_item:
                continue
            return pathlib.Path(available_item, name)
        return None

    def _get_path(
        self,
        name: str,
        source: str,
        path_prefix: pathlib.Path,
        path_suffix: str | None = None,
    ) -> pathlib.Path | None:
        if not path_prefix:
            return None

        expected_path = path_prefix / path_suffix if path_suffix else path_prefix

        if not self._allow_not_exist and not expected_path.exists():
            logger.debug(
                "Could not find %s using %s at '%s'.",
                name,
                source,
                expected_path,
            )
            return None

        logger.debug(
            "Found %s using %s at '%s'.",
            name,
            source,
            expected_path,
        )
        return expected_path

    def _get_user_downloads_dir_win_guess(self) -> pathlib.Path | None:
        if not self.is_win:
            return None

        user_profile = os.environ.get("USERPROFILE")
        if not user_profile or not user_profile.strip():
            return None

        return self._get_path(
            "Downloads directory",
            "default user directories",
            pathlib.Path(user_profile),
            "Downloads",
        )

    def _get_user_downloads_dir_win_reg(self) -> pathlib.Path | None:
        try:
            import winreg

            tree_root = winreg.HKEY_CURRENT_USER
            tree_leaf = winreg.OpenKeyEx(
                tree_root,
                r"SOFTWARE\\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",
            )
            key_value, key_type = winreg.QueryValueEx(
                tree_leaf,
                "{374DE290-123F-4565-9164-39C4925E467B}",
            )
            if tree_leaf:
                winreg.CloseKey(tree_leaf)

            if key_value and key_type == winreg.REG_SZ:
                self._get_path(
                    "Downloads directory",
                    "default user directories",
                    pathlib.Path(key_value),
                    "Downloads",
                )
                return pathlib.Path(key_value)

            return None
        except ImportError:
            pass

        return None
