import traceback
from milvus import default_server
from pymilvus import connections, utility

class DatabaseServer:
    def __init__(self, base_dir="milvus_data", port=19530):
        self.base_dir = base_dir
        self.port = port
        self.start()

    def start(self):
        try:
            # Set the base directory before starting
            default_server.set_base_dir(self.base_dir)
            
            # Set the port (optional, but recommended)
            default_server.listen_port = self.port

            if not default_server.running:  # ✅ Fix: Remove ()
                default_server.start()
                print(f"Milvus Database started at port {self.port}")
            else:
                print("Milvus is already running")

            # Connect to Milvus Lite
            connections.connect(host="127.0.0.1", port=self.port)

            # Check if the server is running correctly
            print("Milvus Version:", utility.get_server_version())

        except Exception as e:
            traceback.print_exc()
            print(f"Error starting database: {e}")

    def end(self):
        if default_server.running:  # ✅ Fix: Remove ()
            default_server.stop()
            print("Milvus Database stopped")
        else:
            print("Milvus was not running")