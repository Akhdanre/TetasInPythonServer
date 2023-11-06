create table users(
   username varchar(100) not null,
   password varchar(100) not null,
   name varchar(100) not null,
   token varchar(100),
   primary key (username)
);



create table inkubators(
   id int(5) not null,
   token varchar(10) not null,
   min_temp int(2),
   max_temp int(2),
   min_humd int(2),
   max_humd int(2),
   water_volume int(2),
   primary key (id)
);


create table hatch_data(
   id int(8) not null,
   inkubator_id int(5),
   start_date date,
   end_date_estimation date,
   number_of_eggs int(2),
   primary key (id)
);


create table detail_hatch_data(
   id int(3) not null,
   id_hatch_data int(8) not null,
   temp int(2),
   humd int(2),
   water_volume int(2),
   time varchar(12),
   date_report date,
   primary key (id)
);