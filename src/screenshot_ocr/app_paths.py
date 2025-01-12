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

    def __init__(self, *, allow_not_exist: bool = False) -> None:
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
        result = self._platform_dirs.user_downloads_path
        return self._get_path("Downloads directory", "default user directories", result)

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
        paths = self._tesseract_paths
        return paths.get("exe_path", None)

    @functools.cached_property
    def tesseract_data_file(self) -> pathlib.Path | None:
        """Get the Tesseract data directory.

        Returns:
            The Tesseract data directory, if known.
        """
        paths = self._tesseract_paths
        return paths.get("data_path", None)

    @functools.cached_property
    def _tesseract_paths(  # noqa: C901, PLR0912, PLR0915
        self,
    ) -> dict[str, pathlib.Path | None]:
        # information to obtain
        install_path = None
        exe_path = None
        data_path = None

        if sys.platform.startswith("linux"):
            # Get exe from PATH.
            if not exe_path:
                available_exe1 = shutil.which("tesseract")
                if available_exe1:
                    available_path = pathlib.Path(available_exe1)
                    if available_path.exists():
                        exe_path = available_path.resolve()
                        logger.debug(
                            "Found tesseract exe path using Path at '%s'.", exe_path
                        )

            # Get exe from default path.
            if not exe_path:
                available_exe2 = pathlib.Path("/usr/bin/tesseract")
                if available_exe2:
                    available_path = pathlib.Path(available_exe2)
                    if available_path.exists():
                        exe_path = available_path.resolve()
                        logger.debug(
                            "Found tesseract exe path using default at '%s'.", exe_path
                        )

            # Get data from default path.
            if not data_path:
                available_data1 = pathlib.Path("/usr/share/tesseract-ocr/5/tessdata")
                if available_data1:
                    available_path = pathlib.Path(available_data1)
                    if available_path.exists():
                        data_path = available_path.resolve()
                        logger.debug(
                            "Found tesseract data path using default at '%s'.",
                            data_path,
                        )

        elif sys.platform.startswith("win"):
            # Get install dir using Windows default path.
            if not install_path:
                available_install1 = [
                    os.environ.get("PROGRAMFILES"),
                    os.environ.get("PROGRAMFILES(X86)"),
                ]
                for available_item in available_install1:
                    if not available_item:
                        continue
                    available_path = pathlib.Path(available_item, "Tesseract-OCR")
                    if available_path.exists():
                        install_path = available_path
                        logger.debug(
                            "Found tesseract install path using Program Files at '%s'.",
                            install_path,
                        )
                        break

            # Get install path from Windows Registry.
            if not install_path:
                try:
                    import winreg

                    tree_root = winreg.HKEY_LOCAL_MACHINE
                    tree_leaf = winreg.OpenKeyEx(
                        tree_root, r"SOFTWARE\\Tesseract-OCR\\"
                    )
                    key_value, key_type = winreg.QueryValueEx(tree_leaf, "InstallDir")
                    if tree_leaf:
                        winreg.CloseKey(tree_leaf)

                    if key_value and key_type == winreg.REG_SZ:
                        available_path = pathlib.Path(key_value)
                        if available_path.exists():
                            install_path = available_path
                            logger.debug(
                                "Found tesseract install path using "
                                "Windows Registry at '%s'.",
                                install_path,
                            )

                except ImportError:
                    pass

            # Get exe from PATH.
            if not exe_path:
                available = shutil.which("tesseract.exe")
                if available:
                    available_path = pathlib.Path(available)
                    if available_path.exists():
                        exe_path = available_path.resolve()
                        logger.debug(
                            "Found tesseract exe path using Path at '%s'.", exe_path
                        )

            # Get exe from install path.
            if install_path and not exe_path:
                available_path = install_path / "tesseract.exe"
                if available_path.exists():
                    exe_path = available_path.resolve()
                    logger.debug(
                        "Found tesseract exe path using install path at '%s'.", exe_path
                    )

            # Get data from install path.
            if install_path and not data_path:
                available_path = install_path / "tessdata"
                if available_path.exists():
                    data_path = available_path.resolve()
                    logger.debug(
                        "Found tesseract data path using install path at '%s'.",
                        data_path,
                    )
        else:
            msg = f"Tesseract paths not implemented for '{sys.platform}'."
            raise ValueError(msg)

        return {
            "exe_path": exe_path,
            "data_path": data_path,
        }

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
