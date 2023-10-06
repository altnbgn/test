import grpc
import server_pb2
import server_pb2_grpc

def create_insecure_channel(host, port):
    channel = grpc.insecure_channel(f'{host}:{port}')  # Replace with your server address
    return channel

def create_secure_channel(host, port):
    # Load the client certificate and private key
    with open('client.crt', 'rb') as f:
        client_cert = f.read()
    with open('client.key', 'rb') as f:
        client_key = f.read()

    # Create client credentials using the certificate and private key
    client_credentials = grpc.ssl_channel_credentials(root_certificates=None, private_key=client_key, certificate_chain=client_cert)

    # Create a secure channel with the server's address and credentials
    channel = grpc.secure_channel(f'{host}:{port}', client_credentials)
    return channel

def send_image(image_data):
    host = 'localhost'
    port = 50052

    channel = create_insecure_channel(host, port)
    stub = server_pb2_grpc.ImageServiceStub(channel)
    
    # Create a request with the image data
    requests_list = [
        server_pb2.ImageRequest(image_data=image_data, camera_id='test', timestamp=1),
        server_pb2.ImageRequest(image_data=image_data, camera_id='test', timestamp=1),
        server_pb2.ImageRequest(image_data=image_data, camera_id='test', timestamp=1),
        server_pb2.ImageRequest(image_data=image_data, camera_id='test', timestamp=1)
    ]
    
    # Call the SendImage RPC
    response = stub.SendImage(iter(requests_list))
    print(response)

    print("Server Response:", response.message)

if __name__ == "__main__":
    with open("./examples/frame0-00-00.00.jpg", "rb") as f:
        image_data = f.read()
    
    send_image(image_data)