from . import models as m


def vehiclemodel_by_vehiclemake(session, vehiclemake_id):
    query = session.query(m.VehicleModel).filter(m.VehicleModel.vehiclemake_id == vehiclemake_id)
    return {row.name: row.id for row in query.all()}
