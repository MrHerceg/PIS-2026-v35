import grpc
from concurrent import futures
import time
from datetime import datetime
import travel_pb2
import travel_pb2_grpc

routes = {}

class TravelService(travel_pb2_grpc.TravelServiceServicer):

    def CreateRoute(self, request, context):
        route_id = str(len(routes) + 1)
        routes[route_id] = {
            "route_id": route_id,
            "user_id": request.user_id,
            "title": request.title,
            "start_date": request.start_date,
            "end_date": request.end_date,
            "budget": request.budget,
            "status": "PLANNED"
        }
        return travel_pb2.CreateRouteResponse(
            route_id=route_id,
            status="PLANNED"
        )

    def GetRoute(self, request, context):
        r = routes.get(request.route_id)
        if not r:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Route not found')
            return travel_pb2.RouteDto()
        return travel_pb2.RouteDto(**r)

    def StreamPlaceUpdates(self, request, context):
        route_id = request.route_id
        places = [
            ("Eiffel Tower", "2026-07-01", "Must visit at sunset"),
            ("Louvre Museum", "2026-07-02", "Book tickets in advance"),
            ("Notre-Dame", "2026-07-03", "Reconstruction ongoing"),
        ]
        for place_name, visit_date, note in places:
            update = travel_pb2.PlaceUpdate(
                route_id=route_id,
                place_name=place_name,
                visit_date=visit_date,
                note=note,
                timestamp=str(datetime.now())
            )
            yield update
            time.sleep(1)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    travel_pb2_grpc.add_TravelServiceServicer_to_server(TravelService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
