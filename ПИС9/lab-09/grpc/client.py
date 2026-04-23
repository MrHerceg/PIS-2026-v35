import grpc
import travel_pb2
import travel_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = travel_pb2_grpc.TravelServiceStub(channel)

    # Создание маршрута
    create_resp = stub.CreateRoute(travel_pb2.CreateRouteRequest(
        user_id="user42",
        title="Paris Trip",
        start_date="2026-07-01",
        end_date="2026-07-10",
        budget=2500.0
    ))
    print("CreateRoute:", create_resp)
    route_id = create_resp.route_id

    # Получение маршрута
    get_resp = stub.GetRoute(travel_pb2.GetRouteRequest(route_id=route_id))
    print("GetRoute:", get_resp)

    # Streaming обновлений мест
    print("Place updates:")
    for update in stub.StreamPlaceUpdates(
        travel_pb2.StreamPlaceRequest(route_id=route_id)
    ):
        print(update)

if __name__ == '__main__':
    run()
