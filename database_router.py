class DatabaseRouter:
    """
    Định tuyến database dựa vào db_table:
    - Nếu db_table thuộc MySQL -> MySQL
    - Ngược lại -> MongoDB
    """

    mysql_tables = {"customer", "name", "address"}  # Các bảng trong MySQL

    def db_for_read(self, model, **hints):
        """Chọn database để đọc dữ liệu"""
        if model._meta.db_table in self.mysql_tables:
            return "default"  # MySQL
        return "mongodb"  # MongoDB

    def db_for_write(self, model, **hints):
        """Chọn database để ghi dữ liệu"""
        if model._meta.db_table in self.mysql_tables:
            return "default"
        return "mongodb"

    def allow_relation(self, obj1, obj2, **hints):
        """Cho phép quan hệ giữa các model trong cùng một database"""
        if obj1._state.db == obj2._state.db:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Xác định migration cho từng database"""
        if db == "default":
            return model_name in self.mysql_tables  # Chỉ migrate model thuộc MySQL
        elif db == "mongodb":
            return model_name not in self.mysql_tables  # Model khác dùng MongoDB
        return None
