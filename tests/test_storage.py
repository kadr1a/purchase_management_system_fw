from storage import load_data, save_data


def test_load_and_save_json(tmp_path):
    data = load_data(str(tmp_path))
    data["products"].append(
        {"id": "P1", "name": "Товар", "price": 100}
    )
    save_data(str(tmp_path), data)
    loaded = load_data(str(tmp_path))
    assert loaded["products"][0]["name"] == "Товар"
    assert loaded["orders"] == []
