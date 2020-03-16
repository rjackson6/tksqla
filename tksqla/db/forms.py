from . import models as m


class VehicleMakeForm:
    fields = {
        'name': {'label': 'Name', 'required': True}
    }

    def save(self, session, data):
        new_make = m.VehicleMake(name=data['name'])
        session.add(new_make)
        session.commit()
        return {'name': new_make.name, 'id': new_make.id}


class VehicleModelForm:
    fields = {
        'vehiclemake': {'label': 'Vehicle Make', 'required': True, 'values': {}, 'disabled': False, 'initial': ''},
        'name': {'label': 'Name', 'required': True}
    }

    def __init__(self, session, **kwargs):
        data = kwargs.get('data', None)
        vehiclemake_id = kwargs.get('vehiclemake_id', None)
        q_vehiclemake = session.query(m.VehicleMake)
        if vehiclemake_id:
            vehiclemake = q_vehiclemake.get(vehiclemake_id)
            self.fields['vehiclemake']['values'] = {vehiclemake.name: vehiclemake.id}
            self.fields['vehiclemake']['disabled'] = True
            self.fields['vehiclemake']['initial'] = vehiclemake.name
        elif not data:
            self.fields['vehiclemake']['values'] = {row.name: row.id for row in q_vehiclemake.all()}

    def save(self, session, data):
        new_model = m.VehicleModel(vehiclemake_id=data['vehiclemake_id'], name=data['name'])
        session.add(new_model)
        session.commit()
        return {'name': new_model.name, 'id': new_model.id}


class VehicleTrimForm:
    fields = {
        'vehiclemake': {'label': 'Vehicle Make', 'values': {}},
        'vehiclemodel': {'label': 'Vehicle Model', 'required': True, 'values': {}},
        'name': {'label': 'Name', 'required': True}
    }

    def __init__(self, session, data=None):
        self.data = data
        self.session = session
        if not self.data:
            q_vehiclemake = session.query(m.VehicleMake)
            self.fields['vehiclemake']['values'] = {row.name: row.id for row in q_vehiclemake.all()}

    def save(self):
        new_trim = m.VehicleTrim(vehiclemodel_id=self.data['vehiclemodel_id'], name=self.data['name'])
        try:
            self.session.add(new_trim)
            self.session.commit()
        except Exception as e:
            print('VehicleTrimForm caught an error! {}'.format(e))
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def requery_vehiclemake(self, session):
        q_vehiclemake = session.query(m.VehicleMake)
        return {row.name: row.id for row in q_vehiclemake.all()}
