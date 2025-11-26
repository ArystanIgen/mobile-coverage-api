import pytest

from app.schemas.address import GeoCoordinates


@pytest.fixture(scope="session")
def mock_provider_data() -> dict[str, str]:
    return {
        "name": "Test Provider",
        "mobile_network_code": "12345"
    }


@pytest.fixture(scope="session")
def mock_site_data() -> dict[str, float | bool]:
    return {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "has_2g": False,
        "has_3g": False,
        "has_4g": True
    }


@pytest.fixture(scope="session")
def mock_list_of_nearby_geo_coordinates() -> list[GeoCoordinates]:
    return [
        GeoCoordinates(latitude=48.8566, longitude=2.3522),
        GeoCoordinates(latitude=48.8567, longitude=2.3523)
    ]


@pytest.fixture(scope="session")
def mock_address() -> str:
    return "42 rue papernest 75011 Paris"


@pytest.fixture(scope="session")
def mock_adresse_api_response() -> dict:
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [2.380383, 48.860248]
                },

            }
        ],
    }
