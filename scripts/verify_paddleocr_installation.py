"""Verify the local PaddlePaddle and PaddleOCR installation."""

from __future__ import annotations

import importlib.metadata
import platform
import sys

import paddle
import paddleocr


EXPECTED_PADDLE_VERSION = "3.3.0"


def package_version(package_name: str) -> str:
    """Return an installed package version."""

    return importlib.metadata.version(package_name)


def main() -> None:
    """Run installation and environment checks."""

    python_version = platform.python_version()
    architecture = platform.architecture()[0]
    machine = platform.machine()
    paddle_version = paddle.__version__
    paddleocr_version = package_version("paddleocr")
    device = paddle.get_device()
    cuda_build = paddle.device.is_compiled_with_cuda()

    print("PaddleOCR Installation Verification")
    print("---------------------------------")
    print(f"Python:       {python_version}")
    print(f"Executable:   {sys.executable}")
    print(f"Architecture: {architecture}")
    print(f"Machine:      {machine}")
    print(f"PaddlePaddle: {paddle_version}")
    print(f"PaddleOCR:    {paddleocr_version}")
    print(f"Device:       {device}")
    print(f"CUDA build:   {cuda_build}")

    if not sys.prefix.endswith(".venv"):
        raise RuntimeError(
            "Python is not running from the project's .venv environment."
        )

    if architecture != "64bit":
        raise RuntimeError(
            f"Expected 64-bit Python, but found {architecture}."
        )

    if paddle_version != EXPECTED_PADDLE_VERSION:
        raise RuntimeError(
            "Unexpected PaddlePaddle version: "
            f"expected {EXPECTED_PADDLE_VERSION}, "
            f"found {paddle_version}."
        )

    if cuda_build:
        raise RuntimeError(
            "Expected the CPU PaddlePaddle build, "
            "but a CUDA build was detected."
        )

    if device != "cpu":
        raise RuntimeError(
            f"Expected the CPU device, but found {device}."
        )

    if not paddleocr_version.startswith("3."):
        raise RuntimeError(
            "This project expects PaddleOCR 3.x, "
            f"but found {paddleocr_version}."
        )

    # Referencing the imported module confirms that the import completed.
    print(f"PaddleOCR module: {paddleocr.__name__}")

    print("\nRunning PaddlePaddle's built-in check...")
    paddle.utils.run_check()

    print("\n[OK] PaddlePaddle CPU is installed.")
    print("[OK] PaddleOCR is installed.")
    print("[OK] Python is using the project virtual environment.")
    print("[DONE] PaddleOCR installation verification passed.")


if __name__ == "__main__":
    main()