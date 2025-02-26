class DatabaseRouter:
    mysql_tables = {"customer", "name", "address", "django_session"}  # Dùng MySQL
    postgresql_tables = {"cart"}  # Dùng PostgreSQL

    def db_for_read(self, model, **hints):
        if model._meta.db_table in self.mysql_tables:
            return "default"  # MySQL
        elif model._meta.db_table in self.postgresql_tables:
            return "postgresql"  # PostgreSQL
        return "mongodb"  # Mặc định là MongoDB

    def db_for_write(self, model, **hints):
        if model._meta.db_table in self.mysql_tables:
            return "default"
        elif model._meta.db_table in self.postgresql_tables:
            return "postgresql"
        return "mongodb"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == "default":
            return model_name in self.mysql_tables
        elif db == "postgresql":
            return model_name in self.postgresql_tables
        elif db == "mongodb":
            return model_name not in self.mysql_tables and model_name not in self.postgresql_tables
        return None
