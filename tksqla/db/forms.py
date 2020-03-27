from . import models as m


class Field:
    def __init__(self, default=None, disabled=False, initial=None, label=None, required=True, values=None):
        self.default = default
        self.disabled = disabled
        self.initial = initial
        self.label = label
        self.required = required
        self.values = values or {}


class Form:
    def __new__(cls, *args, **kwargs):
        cls._fields = {}
        for k, v in vars(cls).items():
            if isinstance(v, Field):
                cls._fields[k] = v
        return super().__new__(cls)

    @property
    def fields(self):
        f = {}
        for key, field in self._fields.items():
            f[key] = vars(field)
        return f


class VehicleMakeForm(Form):
    name = Field(label='Vehicle Make Name')

    def save(self, session, data):
        new_make = m.VehicleMake(name=data['name'])
        session.add(new_make)
        session.commit()
        return {'name': new_make.name, 'id': new_make.id}


class VehicleModelForm(Form):
    vehiclemake = Field(label='Vehicle Make', initial='')
    name = Field(label='Name')

    def __init__(self, session, **kwargs):
        super().__init__()
        data = kwargs.get('data', None)
        vehiclemake_id = kwargs.get('vehiclemake_id', None)
        q_vehiclemake = session.query(m.VehicleMake)
        if vehiclemake_id:
            vehiclemake = q_vehiclemake.get(vehiclemake_id)
            self.vehiclemake.values = {vehiclemake.name: vehiclemake.id}
            self.vehiclemake.disabled = True
            self.vehiclemake.initial = vehiclemake.name
        elif not data:
            self.vehiclemake.values = {row.name: row.id for row in q_vehiclemake.all()}

    def save(self, session, data):
        new_model = m.VehicleModel(vehiclemake_id=data['vehiclemake_id'], name=data['name'])
        session.add(new_model)
        session.commit()
        return {'name': new_model.name, 'id': new_model.id}


class VehicleTrimForm(Form):
    vehiclemake = Field(label='Vehicle Make')
    vehiclemodel = Field(label='Vehicle Model')
    name = Field(label='Name')

    def __init__(self, session, data=None):
        super().__init__()
        self.data = data
        self.session = session
        if not self.data:
            q_vehiclemake = session.query(m.VehicleMake)
            self.vehiclemake.values = {row.name: row.id for row in q_vehiclemake.all()}

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


class VehicleYearForm(Form):
    make_model_trim = Field(label='Make, Model, Trim')
    year = Field(label='Year')

    def __init__(self, session, data=None):
        self.data = data
        self.session = session
        query = session.query(
            m.VehicleMake.name.label('make_name'),
            m.VehicleModel.name.label('model_name'),
            m.VehicleTrim.name.label('trim_name'),
            m.VehicleTrim.id.label('trim_id')
        )
        query = query.select_from(m.VehicleTrim). \
            join(m.VehicleTrim.vehiclemodel). \
            join(m.VehicleModel.vehiclemake)
        for row in query.all():
            k = '{} {} {}'.format(row.make_name, row.model_name, row.trim_name)
            v = row.trim_id
            self.make_model_trim.values[k] = v

    def save(self):
        new_vyear = m.VehicleYear(
            vehicletrim_id=self.data['vehicletrim_id'],
            year=self.data['year']
        )
        self.session.add(new_vyear)
        self.session.commit()
