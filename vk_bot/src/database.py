import psycopg2
import logging
import sys


class Database:
    """PostgreSQL Database class."""

    def __init__(self):
        self.host = 'localhost'
        self.username = 'postgres'
        self.password = 'msi'
        self.dbname = 'vk_iot'
        self.conn = None

    def connect(self):
        """Connect to a Postgres database."""
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(host=self.host,
                                             user=self.username,
                                             password=self.password,
                                             dbname=self.dbname)
            except psycopg2.DatabaseError as e:
                logging.error(e)
                sys.exit()
            finally:
                logging.info('Connection opened successfully.')

    def db_add_user_and_device(self, user_id, serial):
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO client (id, vk_id, device_id) VALUES (DEFAULT, {0}, "
                    "(SELECT id FROM public.device WHERE "
                    "device.serial=\'{1}\'))".format(
                        user_id, serial)
                )
                self.conn.commit()
                logging.info("Records inserted successfully")
            except Exception:
                print(Exception)

    def db_update_user_device(self, user_id, serial):
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    "UPDATE public.client SET id=(SELECT id FROM public.client where vk_id=%s),"
                    " vk_id=%s, device_id=(SELECT id FROM public.device WHERE "
                    "device.serial=%s) WHERE vk_id=%s;",
                    (user_id, user_id, serial, user_id)
                )
                updated_rows = cur.rowcount
                self.conn.commit()
                print(updated_rows)
                cur.close()
                logging.info("Record updated successfully")
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

    # def db_has_user_device(self, user_id, serial):
    #     with self.conn.cursor() as cur:
    #         try:
    #             cur.execute(
    #                 'SELECT c.id, c.vk_id, d.serial FROM public.client c '
    #                 'inner join public.device d ON c.device_id = d.id '
    #                 'where d.serial = %s and c.vk_id = %s;', (serial, user_id)
    #             )
    #             print(cur)
    #             cur.fetchall()
    #             for row in cur:
    #                 print(row)
    #             self.conn.commit()
    #             logging.info("Records inserted successfully")
    #         except Exception:
    #             print(Exception.__str__())

    def db_get_user_device(self, user_id):
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    'SELECT d.serial FROM public.client c inner join public.device d ON c.device_id = d.id '
                    'where c.vk_id = %s;',
                    (user_id,)
                )
                device = cur.fetchone()[0]
                print(device)
                self.conn.commit()
                logging.info("Records inserted successfully")
                return device
            except Exception:
                print(Exception.__str__())

    def db_is_user_in(self, user_id):
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    'SELECT id, vk_id FROM public.client where vk_id=%s', (user_id,)
                )
                rows = cur.fetchall()
                self.conn.commit()
                logging.info("Found user")
            except Exception:
                print(Exception)
        return len(rows) > 0

    def db_user_has_device(self, user_id):
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    'SELECT device_id FROM public.client where vk_id=%s', (user_id,)
                )
                # device = cur.fetchone()[0]
                device = cur.fetchall()
                print(device)
                self.conn.commit()
                logging.info("Found user")
                return device != [] and device[0][0] is not None
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

    def db_get_users_with_device(self, serial):
        with self.conn.cursor() as cur:
            try:
                cur.execute(
                    'SELECT c.vk_id FROM public.client c inner join public.device d '
                    'on c.device_id = d.id where d.serial=%s;', (serial, )
                )
                users = cur.fetchall()
                # print(users)
                self.conn.commit()
                logging.info("Found user")
            except Exception:
                print(Exception)
        return users


if __name__ == '__main__':
    db = Database()
    db.connect()
    # db.db_add_user_and_device(12, '1')
    # db.db_has_user_device(12, 'testtest')
    # print(db.db_is_user_in(12))
    # db.db_delete_device_from_user(52588152)
    # db.db_update_user_device(52588152, None)
    print(db.db_user_has_device(52588152))
    # db.db_get_user_device(52588152, 'testtest')
    # db.db_get_users_with_device('testtest')
