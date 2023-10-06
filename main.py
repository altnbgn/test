from predict import load_model
from predict import predict
from configs.config import config
import server_pb2_grpc
import server_pb2
import scheduler_pb2_grpc
import queue, uuid, threading, grpc, time
from concurrent import futures
from scheduler_pb2 import ClientRequest, ClientType, Register, Ping, Result


params = config(section='Model')
THRESHOLD = float(params['threshold'])
AREA_THRESHOLD = float(params['area_threshold'])

params = config(section='gRPC')
host=params['host']
port=int(params['port'])
my_ip=params['my_ip']
my_port=params['my_port']

params = config(section='Scheduler')
scheduler_host=params['scheduler_host']
scheduler_port=int(params['scheduler_port'])


def create_insecure_channel(server, host, port):
    server.add_insecure_port(f'{host}:{port}') 
    # Replace with your desired server address

def create_secure_channel(server, host, port):
    # Load the server certificate and private key
    with open('server.crt', 'rb') as f:
        server_cert = f.read()
    with open('server.key', 'rb') as f:
        server_key = f.read()

    # Create server credentials using the certificate and private key
    server_credentials = grpc.ssl_server_credentials([(server_key, server_cert)])

    # Add the credentials to the server
    server.add_secure_port(f'{host}:{port}', server_credentials)

# Define a class for the image service
class ImageService(server_pb2_grpc.ImageServiceServicer):
    def __init__(self, model, threshold, area_threshold, host, port, scheduler_host, scheduler_port):
        self.model = model
        self.threshold = threshold
        self.area_threshold = area_threshold
        self.host = host
        self.port = port
        self.scheduler_host = scheduler_host
        self.scheduler_port = scheduler_port
        self.id = str(uuid.uuid4())
        self.my_queue = queue.Queue()
        self.channel = grpc.insecure_channel(f"{scheduler_host}:{scheduler_port}")
        self.connected = False
        self.start_conn_thread()

    def register_with_server(self):
        self.my_queue = queue.Queue()
        register_request = ClientRequest(
            register=Register(id=str(self.id), type=ClientType.PROCESSOR, endpoint=str(f"{self.host}:{self.port}")))
        self.my_queue.put(register_request)

    def start_conn_thread(self):
        conn_thread = threading.Thread(target=self.connect)
        conn_thread.daemon = True  # Set the thread as a daemon so it exits when the main program exits
        conn_thread.start()

    def connect(self):
        while True:
            if not self.connected:
                try:
                    self.scheduler_service_stub = scheduler_pb2_grpc.SchedulerServiceStub(self.channel)
                    self.register_with_server()
                    print("Connecting to server")
                    self.connected = True
                    for result in self.scheduler_service_stub.connect(self.queue_iterator()):
                        pass
                except Exception as e:
                    self.connected = False
                    print("Server dead (X_X)")
                    time.sleep(5)  # Adjust the retry interval as needed

    def queue_iterator(self):
        while True:
            yield self.my_queue.get(block=True)

    def predict(self, image_bytes):
        predictions, oversized = predict(self.model, image_bytes, self.threshold, self.area_threshold)
        return predictions, oversized

    def SendImage(self, request_iterator, context):
        for request in request_iterator:
            try:
                start_time = time.time()
                print('+')
                prediction, oversized = self.predict(request.image_data)
                client_request = ClientRequest(result=Result(id=str(self.id), data=prediction, cameraId=str(request.cameraId), timestamp=request.timestamp))
                self.my_queue.put(client_request)
                end_time = time.time()
                print(end_time - start_time)
            except Exception:
                print('*')
                pass
        return server_pb2.ImageResponse(status="DONE")
    
def serve(model, host, port, scheduler_host, scheduler_port, my_ip, my_port, THRESHOLD, AREA_THRESHOLD):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_ImageServiceServicer_to_server(ImageService(model, THRESHOLD, AREA_THRESHOLD, my_ip, my_port, scheduler_host, scheduler_port), server)
    '''
    # Create secure channel
    create_secure_channel(server, host, port)
    '''
    # Create insecure channel
    create_insecure_channel(server, host, port)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    try:
        model = load_model()
    except Exception as e:
        print('Loading model failed:', e)
    
    try:
        print('Serving')
        serve(model, host, port, scheduler_host, scheduler_port, my_ip, my_port, THRESHOLD, AREA_THRESHOLD)
    except Exception as e:
        print('Detection error:', e)
