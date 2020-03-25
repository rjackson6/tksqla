from . import models as m


def qry_vehiclemake(session):
    query = session.query(m.VehicleMake)
    return {row.name: row.id for row in query.all()}


def qry_filter_vehiclemodel(session, vehiclemake_id=None):
    query = session.query(m.VehicleModel)
    if vehiclemake_id:
        query = query.filter(m.VehicleModel.vehiclemake_id == vehiclemake_id)
    return {row.name: row.id for row in query.all()}


def qry_vehicletrim_view(session):
    query = session.query(
        m.VehicleMake.name.label('make_name'),
        m.VehicleModel.name.label('model_name'),
        m.VehicleTrim.name.label('trim_name'),
        m.VehicleTrim.id.label('trim_id')
    )
    query = query.select_from(m.VehicleTrim).\
        join(m.VehicleTrim.vehiclemodel).\
        join(m.VehicleModel.vehiclemake)
    result = {
        row.trim_id: {'make': row.make_name, 'model': row.model_name, 'trim': row.trim_name} for row in query.all()
    }
    return result
