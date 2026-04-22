import os

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'food.db')

CREATE_DATABASE = """
create table if not exists `products` (
  `id` integer primary key,
  `ingredients` text
);
"""

SELECT = 'select `id`, `ingredients` from `products`;'

INSERT = """
insert or replace into `products` (`id`, `ingredients`)
values (?, ?);
"""
