#!/usr/bin/env python3
"""Check that high-tech factory animation keeps a fixed visual footprint."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ATLAS = (
    ROOT
    / "artifacts"
    / "hitech_review_v1"
    / "BUILD_HIGHTECH_HD4_PREVIEW.png"
)
HD2_ATLAS = (
    ROOT
    / "artifacts"
    / "hitech_review_v1"
    / "BUILD_HIGHTECH_HD2_PREVIEW.png"
)
FLAG_ATLAS = (
    ROOT
    / "artifacts"
    / "hitech_review_v1"
    / "BUILD_HIGHTECH_FLAG_HD4_PREVIEW.png"
)
FLAG_MASK_ATLAS = (
    ROOT
    / "artifacts"
    / "hitech_review_v1"
    / "HM_BUILD_HIGHTECH_FLAG_HD4_PREVIEW.png"
)
REFERENCE_FLAG_ATLAS = (
    ROOT
    / "artifacts"
    / "windtrap_review_v1"
    / "BUILD_WINDTRAP_FLAG_HD4_PREVIEW.png"
)
REFERENCE_FLAG_MASK_ATLAS = (
    ROOT
    / "artifacts"
    / "windtrap_review_v1"
    / "HM_BUILD_WINDTRAP_FLAG_HD4_PREVIEW.png"
)
FLAG_POSITION = (94, 96)
FRAME_WIDTH = 384
FRAME_HEIGHT = 256
FRAME_COUNT = 7
MAX_EDGE_DRIFT = 1
DYNAMIC_BAY = (108, 54, 294, 252)
LED_CENTERS = (
    (310, 21),
    (355, 78),
    (310, 137),
    (264, 78),
)
LED_RADIUS = 14


def frame_bounds(atlas: Image.Image) -> list[tuple[int, int, int, int]]:
    bounds: list[tuple[int, int, int, int]] = []
    for index in range(FRAME_COUNT):
        frame = atlas.crop(
            (
                0,
                index * FRAME_HEIGHT,
                FRAME_WIDTH,
                (index + 1) * FRAME_HEIGHT,
            )
        )
        box = frame.getchannel("A").getbbox()
        if box is None:
            raise AssertionError(f"кадр {index + 1} пуст")
        bounds.append(box)
    return bounds


def main() -> int:
    atlas = Image.open(ATLAS).convert("RGBA")
    expected_size = (FRAME_WIDTH, FRAME_HEIGHT * FRAME_COUNT)
    if atlas.size != expected_size:
        raise AssertionError(f"размер атласа {atlas.size}, ожидался {expected_size}")

    bounds = frame_bounds(atlas)
    edges = {
        "left": [box[0] for box in bounds],
        "top": [box[1] for box in bounds],
        "right": [box[2] for box in bounds],
        "bottom": [box[3] for box in bounds],
        "width": [box[2] - box[0] for box in bounds],
        "height": [box[3] - box[1] for box in bounds],
    }
    drift = {name: max(values) - min(values) for name, values in edges.items()}
    failures = [
        f"{name}: дрейф {value} px > {MAX_EDGE_DRIFT} px"
        for name, value in drift.items()
        if value > MAX_EDGE_DRIFT
    ]

    frames = np.stack(
        [
            np.asarray(
                atlas.crop(
                    (
                        0,
                        index * FRAME_HEIGHT,
                        FRAME_WIDTH,
                        (index + 1) * FRAME_HEIGHT,
                    )
                ),
                dtype=np.int16,
            )
            for index in range(FRAME_COUNT)
        ]
    )
    static_mask = np.ones((FRAME_HEIGHT, FRAME_WIDTH), dtype=bool)
    left, top, right, bottom = DYNAMIC_BAY
    yy, xx = np.ogrid[:FRAME_HEIGHT, :FRAME_WIDTH]
    center_x = (left + right) / 2
    center_y = (top + bottom) / 2
    radius_x = (right - left) / 2
    radius_y = (bottom - top) / 2
    bay_mask = (
        ((xx - center_x) / radius_x) ** 2
        + ((yy - center_y) / radius_y) ** 2
        <= 1
    )
    static_mask[bay_mask] = False
    for center_x, center_y in LED_CENTERS:
        static_mask[
            max(0, center_y - LED_RADIUS) : min(
                FRAME_HEIGHT, center_y + LED_RADIUS + 1
            ),
            max(0, center_x - LED_RADIUS) : min(
                FRAME_WIDTH, center_x + LED_RADIUS + 1
            ),
        ] = False

    reference = frames[0]
    static_changed_pixels: list[int] = []
    static_max_delta: list[int] = []
    for index in range(FRAME_COUNT):
        delta = np.abs(frames[index] - reference).max(axis=2)
        static_delta = delta[static_mask]
        static_changed_pixels.append(int(np.count_nonzero(static_delta > 2)))
        static_max_delta.append(int(static_delta.max(initial=0)))
    if any(static_changed_pixels[1:]):
        failures.append(
            "неподвижный корпус меняется между кадрами: "
            f"{static_changed_pixels[1:]} отличающихся пикселей"
        )

    led_levels: list[list[int]] = []
    for frame in frames:
        levels: list[int] = []
        for center_x, center_y in LED_CENTERS:
            patch = frame[
                center_y - 7 : center_y + 8,
                center_x - 7 : center_x + 8,
                :3,
            ]
            red_emission = (
                patch[:, :, 0].astype(np.int32)
                - (
                    patch[:, :, 1].astype(np.int32)
                    + patch[:, :, 2].astype(np.int32)
                )
                // 2
            )
            levels.append(int(np.percentile(red_emission, 90)))
        led_levels.append(levels)
    led_dominant = [int(np.argmax(levels)) for levels in led_levels]
    expected_led_dominant = [index % len(LED_CENTERS) for index in range(FRAME_COUNT)]
    if led_dominant != expected_led_dominant:
        failures.append(
            "нет последовательного обхода светодиодов: "
            f"{led_dominant}, ожидалось {expected_led_dominant}"
        )

    hd2 = Image.open(HD2_ATLAS).convert("RGBA")
    expected_hd2 = Image.new("RGBA", (192, 128 * FRAME_COUNT))
    for index in range(FRAME_COUNT):
        frame = atlas.crop(
            (
                0,
                index * FRAME_HEIGHT,
                FRAME_WIDTH,
                (index + 1) * FRAME_HEIGHT,
            )
        )
        expected_hd2.alpha_composite(
            frame.resize((192, 128), Image.Resampling.LANCZOS),
            (0, index * 128),
        )
    hd2_delta = np.abs(
        np.asarray(hd2, dtype=np.int16)
        - np.asarray(expected_hd2, dtype=np.int16)
    )
    hd2_max_delta = int(hd2_delta.max(initial=0))
    hd2_changed_values = int(np.count_nonzero(hd2_delta))
    if hd2_changed_values:
        failures.append(
            "HD2 собран не покадрово: "
            f"{hd2_changed_values} каналов отличаются, максимум {hd2_max_delta}"
        )

    flag = Image.open(FLAG_ATLAS).convert("RGBA")
    flag_mask = Image.open(FLAG_MASK_ATLAS).convert("RGBA")
    reference_flag = Image.open(REFERENCE_FLAG_ATLAS).convert("RGBA")
    reference_flag_mask = Image.open(REFERENCE_FLAG_MASK_ATLAS).convert("RGBA")
    expected_flag = Image.new("RGBA", flag.size)
    expected_flag_mask = Image.new("RGBA", flag_mask.size, (255, 255, 255, 0))
    reference_frame_height = reference_flag.height // 8
    for index in range(8):
        reference_frame = reference_flag.crop(
            (
                0,
                index * reference_frame_height,
                reference_flag.width,
                (index + 1) * reference_frame_height,
            )
        )
        reference_mask_frame = reference_flag_mask.crop(
            (
                0,
                index * reference_frame_height,
                reference_flag_mask.width,
                (index + 1) * reference_frame_height,
            )
        )
        box = reference_frame.getchannel("A").getbbox()
        mask_box = reference_mask_frame.getchannel("A").getbbox()
        if box is None or mask_box is None:
            raise AssertionError(f"эталонный флаг, кадр {index + 1}, пуст")
        expected_flag.alpha_composite(
            reference_frame.crop(box),
            (FLAG_POSITION[0], FLAG_POSITION[1] + index * FRAME_HEIGHT),
        )
        expected_flag_mask.alpha_composite(
            reference_mask_frame.crop(mask_box),
            (FLAG_POSITION[0], FLAG_POSITION[1] + index * FRAME_HEIGHT),
        )
    flag_delta = np.abs(
        np.asarray(flag, dtype=np.int16)
        - np.asarray(expected_flag, dtype=np.int16)
    )
    flag_mask_delta = np.abs(
        np.asarray(flag_mask, dtype=np.int16)
        - np.asarray(expected_flag_mask, dtype=np.int16)
    )
    flag_changed_values = int(np.count_nonzero(flag_delta))
    flag_mask_changed_values = int(np.count_nonzero(flag_mask_delta))
    if flag_changed_values or flag_mask_changed_values:
        failures.append(
            "фазы флага отличаются от утверждённой анимации: "
            f"цвет {flag_changed_values}, маска {flag_mask_changed_values}"
        )

    report = {
        "atlas": str(ATLAS),
        "bounds": [list(box) for box in bounds],
        "edges": edges,
        "drift": drift,
        "limit": MAX_EDGE_DRIFT,
        "static_changed_pixels": static_changed_pixels,
        "static_max_delta": static_max_delta,
        "led_levels": led_levels,
        "led_dominant": led_dominant,
        "expected_led_dominant": expected_led_dominant,
        "hd2_changed_values": hd2_changed_values,
        "hd2_max_delta": hd2_max_delta,
        "flag_changed_values": flag_changed_values,
        "flag_mask_changed_values": flag_mask_changed_values,
        "status": "failed" if failures else "passed",
        "failures": failures,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
