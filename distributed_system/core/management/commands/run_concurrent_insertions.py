import threading
import time
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.db import transaction
from core.models import User, Product, Order

class Command(BaseCommand):
    help = 'Run concurrent insertions for the distributed system simulation'
    
    def __init__(self):
        super().__init__()
        self.results = {
            'users': [],
            'products': [],
            'orders': []
        }
        self.results_lock = threading.Lock()
        
        # Test data from assignment
        self.users_data = [
            (1, "Alice", "alice@example.com"),
            (2, "Bob", "bob@example.com"),
            (3, "Charlie", "charlie@example.com"),
            (4, "David", "david@example.com"),
            (5, "Eve", "eve@example.com"),
            (6, "Frank", "frank@example.com"),
            (7, "Grace", "grace@example.com"),
            (8, "Alice", "alice@example.com"),
            (9, "Henry", "henry@example.com"),
            (10, "", "jane@example.com"),  # Invalid: empty name
        ]
        
        self.products_data = [
            (1, "Laptop", 1000.00),
            (2, "Smartphone", 700.00),
            (3, "Headphones", 150.00),
            (4, "Monitor", 300.00),
            (5, "Keyboard", 50.00),
            (6, "Mouse", 30.00),
            (7, "Laptop", 1000.00),
            (8, "Smartwatch", 250.00),
            (9, "Gaming Chair", 500.00),
            (10, "Earbuds", -50.00),  # Invalid: negative price
        ]
        
        self.orders_data = [
            (1, 1, 1, 2),
            (2, 2, 2, 1),
            (3, 3, 3, 5),
            (4, 4, 4, 1),
            (5, 5, 5, 3),
            (6, 6, 6, 4),
            (7, 7, 7, 2),
            (8, 8, 8, 0),  # Invalid: zero quantity
            (9, 9, 1, -1),  # Invalid: negative quantity
            (10, 10, 11, 2),
        ]
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-data',
            action='store_true',
            help='Clear existing data before insertion',
        )
    
    def handle(self, *args, **options):
        self.stdout.write("🚀 Starting Django Distributed System Simulation")
        self.stdout.write("=" * 60)
        
        if options['clear_data']:
            self.clear_databases()
        
        self.run_concurrent_insertions()
    
    def clear_databases(self):
        """Clear all databases before insertion"""
        self.stdout.write("🗑️  Clearing existing data...")
        
        User.objects.using('users_db').all().delete()
        Product.objects.using('products_db').all().delete()
        Order.objects.using('orders_db').all().delete()
        
        self.stdout.write("✅ Data cleared successfully")
    
    def insert_user(self, user_data: tuple, thread_id: int):
        """Insert a single user record"""
        try:
            with transaction.atomic(using='users_db'):
                user = User(id=user_data[0], name=user_data[1], email=user_data[2])
                user.save(using='users_db')
            
            result = {
                'thread_id': thread_id,
                'status': 'SUCCESS',
                'data': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                },
                'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3]
            }
            
        except Exception as e:
            result = {
                'thread_id': thread_id,
                'status': 'FAILED',
                'data': {
                    'id': user_data[0],
                    'name': user_data[1],
                    'email': user_data[2]
                },
                'error': str(e),
                'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3]
            }
        
        with self.results_lock:
            self.results['users'].append(result)
    
    def insert_product(self, product_data: tuple, thread_id: int):
        """Insert a single product record"""
        try:
            with transaction.atomic(using='products_db'):
                product = Product(
                    id=product_data[0],
                    name=product_data[1],
                    price=product_data[2]
                )
                product.save(using='products_db')
            
            result = {
                'thread_id': thread_id,
                'status': 'SUCCESS',
                'data': {
                    'id': product.id,
                    'name': product.name,
                    'price': float(product.price)
                },
                'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3]
            }
            
        except Exception as e:
            result = {
                'thread_id': thread_id,
                'status': 'FAILED',
                'data': {
                    'id': product_data[0],
                    'name': product_data[1],
                    'price': product_data[2]
                },
                'error': str(e),
                'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3]
            }
        
        with self.results_lock:
            self.results['products'].append(result)
    
    def insert_order(self, order_data: tuple, thread_id: int):
        """Insert a single order record"""
        try:
            with transaction.atomic(using='orders_db'):
                order = Order(
                    id=order_data[0],
                    user_id=order_data[1],
                    product_id=order_data[2],
                    quantity=order_data[3]
                )
                order.save(using='orders_db')
            
            result = {
                'thread_id': thread_id,
                'status': 'SUCCESS',
                'data': {
                    'id': order.id,
                    'user_id': order.user_id,
                    'product_id': order.product_id,
                    'quantity': order.quantity
                },
                'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3]
            }
            
        except Exception as e:
            result = {
                'thread_id': thread_id,
                'status': 'FAILED',
                'data': {
                    'id': order_data[0],
                    'user_id': order_data[1],
                    'product_id': order_data[2],
                    'quantity': order_data[3]
                },
                'error': str(e),
                'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3]
            }
        
        with self.results_lock:
            self.results['orders'].append(result)
    
    def run_concurrent_insertions(self):
        """Execute all insertions concurrently"""
        threads = []
        
        # Create threads for users
        for i, user_data in enumerate(self.users_data):
            thread = threading.Thread(
                target=self.insert_user,
                args=(user_data, i + 1),
                name=f"UserThread-{i + 1}"
            )
            threads.append(thread)
        
        # Create threads for products
        for i, product_data in enumerate(self.products_data):
            thread = threading.Thread(
                target=self.insert_product,
                args=(product_data, i + 1),
                name=f"ProductThread-{i + 1}"
            )
            threads.append(thread)
        
        # Create threads for orders
        for i, order_data in enumerate(self.orders_data):
            thread = threading.Thread(
                target=self.insert_order,
                args=(order_data, i + 1),
                name=f"OrderThread-{i + 1}"
            )
            threads.append(thread)
        
        # Start all threads
        start_time = time.time()
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        # Display results
        self.display_results(end_time - start_time)
    
    def display_results(self, execution_time: float):
        """Display insertion results"""
        self.stdout.write(f"\n⏱️  Total Execution Time: {execution_time:.3f} seconds")
        self.stdout.write(f"🧵 Total Threads Created: {len(self.users_data) + len(self.products_data) + len(self.orders_data)}")
        
        # Users results
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("👤 USERS INSERTION RESULTS")
        self.stdout.write("=" * 60)
        success_count = 0
        for result in sorted(self.results['users'], key=lambda x: x['data']['id']):
            status_icon = "✅" if result['status'] == 'SUCCESS' else "❌"
            self.stdout.write(f"{status_icon} Thread-{result['thread_id']} [{result['timestamp']}]")
            self.stdout.write(f"   ID: {result['data']['id']}, Name: '{result['data']['name']}', Email: '{result['data']['email']}'")
            if result['status'] == 'FAILED':
                self.stdout.write(f"   Error: {result['error']}")
            else:
                success_count += 1
            self.stdout.write("")
        
        self.stdout.write(f"📊 Users Summary: {success_count}/{len(self.users_data)} successful insertions")
        
        # Products results
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("📦 PRODUCTS INSERTION RESULTS")
        self.stdout.write("=" * 60)
        success_count = 0
        for result in sorted(self.results['products'], key=lambda x: x['data']['id']):
            status_icon = "✅" if result['status'] == 'SUCCESS' else "❌"
            self.stdout.write(f"{status_icon} Thread-{result['thread_id']} [{result['timestamp']}]")
            self.stdout.write(f"   ID: {result['data']['id']}, Name: '{result['data']['name']}', Price: ${result['data']['price']}")
            if result['status'] == 'FAILED':
                self.stdout.write(f"   Error: {result['error']}")
            else:
                success_count += 1
            self.stdout.write("")
        
        self.stdout.write(f"📊 Products Summary: {success_count}/{len(self.products_data)} successful insertions")
        
        # Orders results
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("🛒 ORDERS INSERTION RESULTS")
        self.stdout.write("=" * 60)
        success_count = 0
        for result in sorted(self.results['orders'], key=lambda x: x['data']['id']):
            status_icon = "✅" if result['status'] == 'SUCCESS' else "❌"
            self.stdout.write(f"{status_icon} Thread-{result['thread_id']} [{result['timestamp']}]")
            self.stdout.write(f"   ID: {result['data']['id']}, User ID: {result['data']['user_id']}, Product ID: {result['data']['product_id']}, Quantity: {result['data']['quantity']}")
            if result['status'] == 'FAILED':
                self.stdout.write(f"   Error: {result['error']}")
            else:
                success_count += 1
            self.stdout.write("")
        
        self.stdout.write(f"📊 Orders Summary: {success_count}/{len(self.orders_data)} successful insertions")
        
        # Final summary
        total_success = (len([r for r in self.results['users'] if r['status'] == 'SUCCESS']) +
                        len([r for r in self.results['products'] if r['status'] == 'SUCCESS']) +
                        len([r for r in self.results['orders'] if r['status'] == 'SUCCESS']))
        total_records = len(self.users_data) + len(self.products_data) + len(self.orders_data)
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("FINAL SUMMARY")
        self.stdout.write("=" * 60)
        self.stdout.write(f"Total Successful Insertions: {total_success}/{total_records}")
        self.stdout.write(f"Total Failed Insertions: {total_records - total_success}")
        self.stdout.write(f"Databases Created: users.db, products.db, orders.db")
        self.stdout.write("All validations handled at application level")
        self.stdout.write("Using Django ORM with multi-database routing")