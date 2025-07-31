class DatabaseRouter:
    """Database router for distributed system"""
    
    route_app_labels = {'core'}
    
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'core':
            if model.__name__ == 'User':
                return 'users_db'
            elif model.__name__ == 'Product':
                return 'products_db'
            elif model.__name__ == 'Order':
                return 'orders_db'
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'core':
            if model.__name__ == 'User':
                return 'users_db'
            elif model.__name__ == 'Product':
                return 'products_db'
            elif model.__name__ == 'Order':
                return 'orders_db'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        return True
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'core':
            if db == 'users_db' and model_name == 'user':
                return True
            elif db == 'products_db' and model_name == 'product':
                return True
            elif db == 'orders_db' and model_name == 'order':
                return True
            return False
        return db == 'default'