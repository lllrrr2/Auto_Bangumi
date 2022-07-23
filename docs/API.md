# API 文档
- 所有 API 都为 `/api/v2/APIName/methodName` 的格式

## Info
**APIName:** `info`
### Get all rules
**Name:** `Rules`

**Method:** `GET`

**Returns:** List

**Parameters:** 

| Content          | Type    | Example      |
|------------------|---------|--------------|
| `ID`             | Integer | 1            |
| `official_title` | String  | `official_title` |
| `title_zh`       | String  | `title_zh`   |
| `title_jp`       | String  | `title_en`   |
| `title_en`       | String  | `title_en`   |
| `year`           | Integer | 2022         |
| `season`         | String  | 1            |
| `cover_url`      | String  | `cover_url`  |
| `sub_group`      | String  | `sub_group`  |
| `resolution`     | String  | `resolution` |
| `source`         | String  | `source`     |
| `sub_language`   | String  | `sub_language` |
| `contain`        | String  | `contain`    |
| `not_contain`    | String  | `not_contain` |
| `added`          | Bool    | True         |
| `eps_collect`    | Bool  | True         |
| `ep_offset`      | Integer | 15           |

### Get log
**Name:** `Log`

**Method:** `GET`

**Returns:** 

```log
```

### Get config
**Name:** `Config`

**Method:** `GET`

**Returns:** 
```json{
    "host_ip": "localhost:8080",
    "sleep_time": 7200,
    "times": 20,
    "user_name": "admin",
    "password": "adminadmin",
    "download_path": "/downloads/Bangumi/",
    "method": "pn",
    "enable_group_tag": false,
    "not_contain": [
        "720",
        "\\d+-\\d+"
    ],
    "debug_mode": false,
    "remove_bad_torrent": false,
    "dev_debug": false,
    "eps_complete": false,
    "webui_port": 7892,
    "title_language": "zh",
    "tmdb_api": "32b19d6a05b512190a056fa4e747cbbc",
    "enable_tmdb": false,
    "http_proxy": null,
    "socks": null,
    "enable_rss_collector": true,
    "enable_rename": true,
    "reset_folder": false,
    "setting": false,
    "data_path": "/data/data.db"
}
```


## Set
**APIName:** `set`
### Set config
**Name:** `Config`

**Method:** `POST`

**Parameters:**

| Content          | Type    | Example      |
|------------------|---------|--------------|

### Rule
**Name:** `Rule`

**Method:** `POST`

**Parameters:**


### removeRule
**Name:** `removeRule`

**Method:** `POST`

**Parameters:**

| Content          | Type    | Example      |
|------------------|---------|--------------|
| `ID`             | Integer | 1            |

**Returns:**

| HTTP Status      | Description|
|------------------|------------|
| 200              | Success    |
| 400              | Bad Request|



### resetRule
**Name:** `resetRule`

**Method:** `GET`

**Return:** 

| HTTP Status Code | Description |
|------------------|-------------|
| 200              | OK          |
| 400              | Bad Request |

## Add
**APIName:** `add`
### Collection
**Name:** `Collection`

**Method:** `POST`

**Parameters:**

| Content          | Type    |
|------------------|---------|
| `rss_link`       | String  |

**Return:**

| HTTP Status Code | Description |
|------------------|-------------|
| 200              | OK          |
| 400              | Bad Request |

### Subscribe
**Name:** `Subscribe`

**Method:** `POST`

**Parameters:**

| Content          | Type    |
|------------------|---------|
| `rss_link`       | String  |

**Return:**

| HTTP Status Code | Description |
|------------------|-------------|
| 200              | OK          |
| 400              | Bad Request |

### Rule
**Name:** `Rule`

**Method:** `POST`

**Parameters**:

| Content          | Type    |
|------------------|---------|
| `rss_link`       | String  |


