create_query = ('create table company ('
                'id integer not null primary key autoincrement,'
                'name text null,'
                'okved text not null,'
                'inn integer null,'
                'kpp integer null,'
                'address text null'
                ');'
                )

save_query = (
   'INSERT INTO company (name, okved, inn, kpp, address) VALUES (?, ?, ?, ?, ?)')
