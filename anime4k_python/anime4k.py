#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Anime4K Python
Author: K4YT3X
Date Created: May 8, 2023
Last Modified: May 8, 2023
"""
import os
import pathlib
import subprocess
from typing import Optional

import ffmpeg


class Anime4K:
    def __init__(self, backend="mpv", mode: str = "A", *_args, **_kwargs):
        self.backend = backend
        self.mode = mode

        assert backend in ["mpv", "ffmpeg"], "backend must be either mpv or ffmpeg"

        # locate shader file
        self.shader_path = (
            pathlib.Path(__file__).parent / "shaders" / f"Anime4K_Mode{self.mode}.glsl"
        )
        if not self.shader_path.exists():
            raise FileNotFoundError(str(self.shader_path.absolute()))

    def process_video(
        self,
        input_path: pathlib.Path,
        output_path: pathlib.Path,
        input_width: int,
        input_height: int,
        scale: Optional[int] = None,
        output_width: Optional[int] = None,
        output_height: Optional[int] = None,
    ):
        # calculate output width and height
        if scale is not None:
            output_width = input_width * scale
            output_height = input_height * scale
        elif output_width is None or output_height is None:
            raise ValueError("both output_width and output_height must be provided")

        if self.backend == "mpv":
            command = [
                "mpv",
                "--no-sub",
                f"--glsl-shaders={self.shader_path}",
                f"-vf=gpu=w={output_width}:h={output_height}",
                f"-o={output_path}",
                input_path,
            ]

            # xvfb is required to run mpv on a headless server
            if os.environ.get("DISPLAY") is None:
                command = ["xvfb-run", "-a"] + command

            subprocess.run(command, check=True)

        elif self.backend == "ffmpeg":
            (
                ffmpeg.input(str(input_path.absolute()))
                .output(
                    str(output_path.absolute()),
                    vf="format=yuv420p10,hwupload,"
                    f"libplacebo=w={output_width}:h={output_height}:upscaler=ewa_lanczos:"
                    f"custom_shader_path={self.shader_path},hwdownload,"
                    "format=yuv420p10",
                    init_hw_device="vulkan",
                )
                .global_args("-hide_banner")
                .run(overwrite_output=True)
            )

    def process_image(
        self,
        input_path: pathlib.Path,
        output_path: pathlib.Path,
        input_width: int,
        input_height: int,
        scale: Optional[int] = None,
        output_width: Optional[int] = None,
        output_height: Optional[int] = None,
    ):
        # calculate output width and height
        if scale is not None:
            output_width = input_width * scale
            output_height = input_height * scale
        elif output_width is None or output_height is None:
            raise ValueError("both output_width and output_height must be provided")

        # process video
        (
            ffmpeg.input(str(input_path.absolute()))
            .output(
                str(output_path.absolute()),
                vf="format=rgba,hwupload,"
                f"libplacebo=w={output_width}:h={output_height}:upscaler=ewa_lanczos:"
                f"custom_shader_path={self.shader_path},hwdownload,"
                "format=rgba",
                init_hw_device="vulkan",
            )
            .global_args("-hide_banner")
            .run(overwrite_output=True)
        )
