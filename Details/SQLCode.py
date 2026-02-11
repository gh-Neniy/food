CREATE_USER = """
create user if not exists `food`@`localhost` identified by 'yandextop';
grant all privileges on `food`.* to `food`@`localhost`;
flush privileges;
"""

CREATE_DATABASE = """
create schema if not exists `food` default character set utf8mb4 collate utf8mb4_unicode_ci;

create table if not exists `food`.`products` (
  `id` int not null primary key,
  `ingredients` text
);
"""

SELECT_ID_INGREDIENTS = 'select `id`, `ingredients` from `food`.`products`;'

INSERT = """
insert into `food`.`products` (`id`, `ingredients`)
values(%s, %s)
on duplicate key update
`ingredients` = values(`ingredients`);
"""
