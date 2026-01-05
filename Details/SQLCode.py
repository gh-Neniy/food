CREATE_USER = """create user if not exists `food`@`localhost` identified by 'yandextop';
grant all privileges on `food`.* to `food`@`localhost`;
flush privileges;"""

CREATE_DATABASE = """create schema if not exists `food` default character set utf8mb4 collate utf8mb4_unicode_ci;

create table if not exists `food`.`products` (
  `id` int not null primary key,
  `name` varchar(255),
  `composition` text,
  `price` decimal(10, 2),
  `last_update` timestamp default current_timestamp on update current_timestamp
);"""

SELECT_ID_UPDATE = 'select `id`, `last_update` from `food`.`products`;'

SELECT_ESSENTIALS = 'select `id`, `name`, `composition`, `price` from `food`.`products`;'

INSERT = """
insert into `food`.`products` (`id`, `name`, `composition`, `price`)
values(%s, %s, %s, %s)
on duplicate key update
`name` = values(`name`),
`composition` = values(`composition`),
`price` = values(`price`);
"""
