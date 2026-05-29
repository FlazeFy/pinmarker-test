def template_get(response, expected_status: int, is_paginate: bool | None = None):
    # check status code
    assert response.status == expected_status
    body = response.json()

    # check message type
    assert isinstance(body["message"], str)

    # builder: decide data type
    data_type = "object" if (is_paginate is True or is_paginate is None) else "array"

    # test data structure
    if is_paginate is False:
        assert isinstance(body["data"], dict if data_type == "object" else list)

    if is_paginate is True:
        assert isinstance(body["data"]["data"], list)

    return body

def template_validate_column(data, fields: list[str], data_type: str, nullable: bool):
    # normalize to list
    data_array = data if isinstance(data, list) else [data]

    for item in data_array:
        assert isinstance(item, dict)
        for field in fields:
            assert field in item

            if nullable and item[field] is None:
                assert item[field] is None
            else:
                # type check
                if data_type == "string":
                    assert isinstance(item[field], str)
                elif data_type == "number":
                    assert isinstance(item[field], (int, float))
                    # integer vs float check
                    if isinstance(item[field], int):
                        assert item[field] % 1 == 0
                    else:
                        assert item[field] % 1 != 0
                elif data_type == "bool_number":
                    assert isinstance(item[field], int)
                    assert item[field] in [0, 1]
