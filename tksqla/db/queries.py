from . import models as m


def qry_vehiclemake(session):
    query = session.query(m.VehicleMake)
    return {row.name: row.id for row in query.all()}


def qry_filter_vehiclemodel(session, vehiclemake_id=None):
    query = session.query(m.VehicleModel)
    if vehiclemake_id:
        query = query.filter(m.VehicleModel.vehiclemake_id == vehiclemake_id)
    return {row.name: row.id for row in query.all()}
