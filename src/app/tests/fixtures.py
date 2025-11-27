import csv
from pathlib import Path
from typing import Any

import pytest

from app.schemas.address import GeoCoordinates


@pytest.fixture
def mock_provider_data() -> dict[str, str]:
    return {"name": "Test Provider", "mobile_network_code": "12345"}


@pytest.fixture
def mock_site_data() -> dict[str, Any]:
    return {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "has_2g": False,
        "has_3g": False,
        "has_4g": True,
    }


@pytest.fixture
def mock_list_of_nearby_geo_coordinates() -> list[GeoCoordinates]:
    return [
        GeoCoordinates(latitude=48.8566, longitude=2.3522),
        GeoCoordinates(latitude=48.8567, longitude=2.3523),
    ]


@pytest.fixture
def mock_address() -> str:
    return "42 rue papernest 75011 Paris"


@pytest.fixture
def mock_adresse_api_response() -> dict[str, Any]:
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [2.380383, 48.860248],
                },
            }
        ],
    }


@pytest.fixture
def mock_csv_rows() -> list[dict[str, str]]:
    return [
        {
            "Operateur": "20801",
            "x": "102980",
            "y": "6847973",
            "2G": "1",
            "3G": "0",
            "4G": "1",
        },
        {
            "Operateur": "20810",
            "x": "103113",
            "y": "6848661",
            "2G": "0",
            "3G": "1",
            "4G": "1"
        },
    ]


@pytest.fixture
def mock_csv_file_path(
    tmp_path: Path,
    mock_csv_rows: list[dict[str, str]],
) -> Path:
    csv_path = tmp_path / "sites.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["Operateur", "x", "y", "2G", "3G", "4G"],
            delimiter=";",
        )
        writer.writeheader()
        writer.writerows(mock_csv_rows)
    return csv_path
