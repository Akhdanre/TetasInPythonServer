select * from inkubators;
select * from hatch_data;
select * from detail_hatch_data;

update inkubators set temp_limit = 35, humd_limit = 55;

desc users;
desc inkubators;
desc hatch_data;
desc detail_hatch_data;


INSERT INTO hatch_data (id, inkubator_id, start_date, end_date_estimation, number_of_eggs) 
VALUES (1, 'INKID01', '2024-03-07', '2024-03-27', 12);

show tables;

-- (pymysql.err.IntegrityError) (1452, 'Cannot add or update a child row: a foreign key constraint fails (`tetasin_db`.`detail_hatch_data`, CONSTRAINT `detail_hatch_data_ibfk_1` FOREIGN KEY (`id_hatch_data`) REFERENCES `hatch_data` (`id`))')
-- [SQL: INSERT INTO detail_hatch_data (id_hatch_data, temp, humd, water_volume, time_report, date_report, url_image) VALUES (%(id_hatch_data)s, %(temp)s, %(humd)s, %(water_volume)s, %(time_report)s, %(date_report)s, %(url_image)s)]
-- [parameters: {'id_hatch_data': 1, 'temp': 38, 'humd': 75, 'water_volume': 0, 'time_report': '15:13:20', 'date_report': '2024-03-06', 'url_image': None}]
-- (Background on this error at: https://sqlalche.me/e/20/gkpj)