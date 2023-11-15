# Inkubator API Spec
<br><br>
# Mobile App


## information
EndPoint : Get /api/inkubatorInfo

Header Body :
- X-API-TOKEN : "token"

Response Body :
```json
{
    "temp" : 39,
    "humd" : 40,
    "water_volume" : 80
}
```

## weekly recap information
Endpoint : Get /api/inkuRecapInfo

Header Body : 
- X-API-TOKEN : "token"

Response Body :
```json
{
    "data" : [
        {
            "date" : "5/11/2023",
            "temp" : 38, 
            "humd" : 40,
            "water_volume" : 80
        },
        {
            "date" : "6/11/2023",
            "temp" : 39, 
            "humd" : 40,
            "water_volume" : 70
        },
        {
            "date" : "7/11/2023",
            "temp" : 38, 
            "humd" : 49,
            "water_volume" : 60
        }
        // until one week data
    ]
}
```


## temp and humd control

Endpoint : patch /api/control/temp_humd

Header Body :
- X-API-TOKEN : "Token"

Request Body :
```json
{
    "target_id" : 1,
    "target_token" : "ksdjle",
    "temp_limit" : 38,
    "humd_limit" : 40
}
```

Response Body : 
```json
{
   "message" : "success change min and max inkubator temperature"
}
```

## All Report history
Endpoint : Get /api/reportData

Header Body :
- X-API-TOKEN : "Token"

Response Body : 
```json
{
    "data" : [ // desc data with 10 data
        {
            "id_report" : 2,
            "date_start" : "2/1/2024",
            "date_end_estimation" : "1/3/2024",
            "number_of_egg" : 23,
        },
        {
            "id_report" : 1,
            "date_start" : "5/11/2023",
            "date_end_estimation" : "1/1/2024",
            "number_of_egg" : 23,
        }
    ]
}
```



## Detail Report history

Endpoint : Post /api/detailReportData

Header Body :
- X-API-TOKEN : "Token"

Request Body : 
```json
{
    "id_report" : 2
}
```

Note : get 10 data every request

Response Body : 
```json
{
    "data" : [ // desc data
        {
            "id_detal_report" : 3,
            "id_report" : 2,
            "time" : "12:00",
            "date" : "5/11/2023",
            "temp" : 39,
            "humd" : 40,
            "water_level" : 85,
            "is_hatch" : true,
            "hatch_count" : 1
        },
        {
            "id_detal_report" : 2,
            "id_report" : 2,
            "time" : "11:00",
            "date" : "5/11/2023",
            "temp" : 39,
            "humd" : 40,
            "water_level" : 87,
            "is_hatch" : true,
            "hatch_count" : 1
        },
        {
            "id_detal_report" : 1,
            "id_report" : 1,
            "time" : "10:00",
            "date" : "5/11/2023",
            "temp" : 39,
            "humd" : 40,
            "water_level" : 80,
            "is_hatch" : false,
            "hatch_count" : 0
        },

        ....
    ]
}
```

<br><br>
# Modul

## Temp Update
Server Sent Event

Endpoint : Get /sse/mdl/tempcontrol

Request Body :
```json
{
    "id_inkubator" : 1
}
```

Event :
```json 
{
    "newMinTemp" : 38,
    "newMaxTemp" : 40
}
```

## Humd Update
Server Sent Event

Endpoint : Get /sse/mdl/humdcontrol

Request Body :
```json
{
    "id_inkubator" : 1
}
```

Event :
```json 
{
    "newMinhumd" : 38,
    "newMaxhumd" : 40
}
```

## inkubator data report

Endpoint : post  /api/mdl/dataReport

Request Body :
```json
{
    "id_inkubator" : 1,
    "temp" : 39,
    "humd" : 41,
    "water_level" : 70, 
    "is_hatch" : true,
    "hatch_count" : 0
}
```