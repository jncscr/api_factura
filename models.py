from django.db import models
from django.forms.models import model_to_dict
#Darse cuenta de borrar Id para que retorne el Id grabado
class Atributo(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    estado = models.BooleanField(default=True)
    tipo_control = models.ForeignKey('TipoControl')
    
    def __init__(self, *args, **kwargs):
        super(Atributo, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(Atributo, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])
    
    
    class Meta:
        db_table = 'atributo'

class AtributoValor(models.Model):
    valor = models.CharField(max_length=255, blank=True)
    atributo = models.ForeignKey(Atributo)
    estado = models.IntegerField(blank=True, null=True)
    
    def __init__(self, *args, **kwargs):
        super(AtributoValor, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(AtributoValor, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])
    
    class Meta:
        db_table = 'atributo_valor'
        
class Caracteristica(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    estado = models.BooleanField(default=True)
    
    def __init__(self, *args, **kwargs):
        super(Caracteristica, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(Caracteristica, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])
    
    
    class Meta:
        db_table = 'caracteristica'

class Cobro(models.Model):
    no_recibo_caja = models.CharField(max_length=255, blank=True)
    no_cheque = models.CharField(max_length=255, blank=True)
    venta = models.ForeignKey('Venta')
    valor_cobro = models.FloatField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    usuario_sistema_id = models.IntegerField()
    fecha = models.DateField(blank=True, null=True)
    pago_inicial = models.IntegerField(blank=True, null=True)
    
    def __init__(self, *args, **kwargs):
        super(Cobro, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(Cobro, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])
    
    
    class Meta:
        db_table = 'cobro'

class Compra(models.Model):
    fecha = models.DateField(blank=True, null=True)
    personal = models.ForeignKey('Personal')
    estado = models.BooleanField(default=True)
    empresa_id = models.IntegerField()
    nombre = models.CharField(max_length=255, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    nit = models.IntegerField(blank=True, null=True)
    usuario_sistema_id = models.IntegerField()
    tipo = models.IntegerField(blank=True, null=True)
    formula = models.FloatField(blank=True, null=True)
    compra_tipo = models.ForeignKey('PagoTipo')
    
    def __init__(self, *args, **kwargs):
        super(Compra, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(Compra, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
       
    class Meta:
        db_table = 'compra'

class CompraAsignacion(models.Model):
    usuario_sistema_id = models.IntegerField()
    libras_asignadas = models.FloatField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    pollos_asignados = models.IntegerField(blank=True, null=True)
    tipo = models.IntegerField(blank=True, null=True)
    menudo_asignados = models.FloatField(blank=True, null=True)
    precio = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'compra_asignacion'

class CompraAtributo(models.Model):
    compra_detalle = models.ForeignKey('CompraDetalle')
    producto_atributo = models.ForeignKey('ProductoAtributo')
    estado = models.BooleanField(default=True)
    atributo_valor = models.ForeignKey(AtributoValor)
    
    def __init__(self, *args, **kwargs):
        super(CompraAtributo, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(CompraAtributo, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
    
    
    class Meta:
        db_table = 'compra_atributo'

class CompraDetalle(models.Model):
    compra = models.ForeignKey(Compra)
    producto = models.ForeignKey('Producto')
    cantidad = models.IntegerField(blank=True, null=True)
    precio = models.ForeignKey('Precio')
    estado = models.BooleanField(default=True)
    
    def __init__(self, *args, **kwargs):
        super(CompraDetalle, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(CompraDetalle, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
       
    class Meta:
        db_table = 'compra_detalle'

class Pago(models.Model):
    no_recibo_caja = models.CharField(max_length=255, blank=True)
    no_cheque = models.CharField(max_length=255, blank=True)
    valor_pago = models.FloatField(blank=True, null=True)
    compra = models.ForeignKey(Compra)
    usuario_sistema_id = models.IntegerField()
    fecha = models.DateField(blank=True, null=True)
    pago_inicial = models.IntegerField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    
    def __init__(self, *args, **kwargs):
        super(Pago, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(Pago, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
        
    class Meta:
        db_table = 'pago'

class PagoTipo(models.Model):
    descripcion = models.CharField(max_length=255, blank=True)
    estado = models.BooleanField(default=True)
    
    def __init__(self, *args, **kwargs):
        super(PagoTipo, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(PagoTipo, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
        
    class Meta:
        db_table = 'pago_tipo'

class Personal(models.Model):
    nombres = models.CharField(max_length=250, blank=True)
    apellidos = models.CharField(max_length=250, blank=True)
    telefono = models.CharField(max_length=250, blank=True)
    direccion = models.CharField(max_length=250, blank=True)
    empresa = models.CharField(max_length=250, blank=True)
    nit = models.IntegerField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    usuario_sistema_id = models.IntegerField()
    tipo = models.BooleanField(default=True)
    usuario_id = models.IntegerField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    empresa_id = models.IntegerField(blank=True, null=True)
    cliente_proveedor = models.IntegerField(blank=True, null=True)
    
    def __init__(self, *args, **kwargs):
        super(Personal, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(Personal, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
        
    class Meta:
        db_table = 'personal'

class PersonalPrecio(models.Model):
    personal = models.ForeignKey(Personal)
    precio = models.ForeignKey('Precio')
    estado = models.BooleanField(default=True)
    fecha = models.DateField(blank=True, null=True)
    precio_tipo = models.ForeignKey('PrecioTipo')
    usuario_sistema_id = models.IntegerField()
    
    def __init__(self, *args, **kwargs):
        super(PersonalPrecio, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(PersonalPrecio, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
    
    class Meta:
        db_table = 'personal_precio'

class Precio(models.Model):
    producto = models.ForeignKey('Producto')
    precio = models.FloatField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    precio_tipo = models.ForeignKey('PrecioTipo')
    empresa_id = models.IntegerField(blank=True, null=True)
    usuario_sistema_id = models.IntegerField()
    
    def __init__(self, *args, **kwargs):
        super(Precio, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(Precio, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
    
    class Meta:
        db_table = 'precio'

class PrecioTipo(models.Model):
    descripcion = models.CharField(max_length=255, blank=True)
    estado = models.BooleanField(default=True)
    
    def __init__(self, *args, **kwargs):
        super(PrecioTipo, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(PrecioTipo, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
    
    class Meta:
        db_table = 'precio_tipo'

class Producto(models.Model):
    fecha = models.DateTimeField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    nombre = models.CharField(max_length=255, blank=True)
    descripcion = models.TextField(blank=True)
    empresa_id = models.IntegerField(blank=True, null=True)
    producto_categoria = models.ForeignKey('ProductoCategoria', blank=True, null=True)
    img = models.CharField(max_length=255, blank=True)
    img_date = models.CharField(max_length=100, blank=True)
    def __init__(self, *args, **kwargs):
        super(Producto, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(Producto, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
    
    class Meta:
        db_table = 'producto'

class ProductoAtributo(models.Model):
    producto = models.ForeignKey(Producto)
    estado = models.BooleanField(default=True)
    atributo = models.ForeignKey(Atributo)
    tipo_control = models.ForeignKey('TipoControl')
    
    def __init__(self, *args, **kwargs):
        super(ProductoAtributo, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ProductoAtributo, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
    
    class Meta:
        db_table = 'producto_atributo'

class ProductoCaracteristica(models.Model):
    producto = models.ForeignKey(Producto)
    valor = models.CharField(max_length=255, blank=True)
    estado = models.BooleanField(default=True)
    caracteristica = models.ForeignKey('Caracteristica')
    
    def __init__(self, *args, **kwargs):
        super(ProductoCaracteristica, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ProductoCaracteristica, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
    
    class Meta:
        db_table = 'producto_caracteristica'

class ProductoCategoria(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    producto_categoria = models.ForeignKey('self', blank=True, null=True)
    es_nodo_principal = models.BooleanField(default=True)
    estado = models.BooleanField(default=True)
    numero = models.IntegerField(blank=True, null=True)
    
    def __init__(self, *args, **kwargs):
        super(ProductoCategoria, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ProductoCategoria, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
    
    class Meta:
        db_table = 'producto_categoria'

class TipoControl(models.Model):
    nombre = models.CharField(max_length=50, blank=True)
    
    def __init__(self, *args, **kwargs):
        super(TipoControl, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(TipoControl, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
    
    class Meta:
        db_table = 'tipo_control'

class TipoVenta(models.Model):
    descripcion = models.CharField(max_length=250, blank=True)
    estado = models.BooleanField(default=True)
    
    def __init__(self, *args, **kwargs):
        super(TipoVenta, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(TipoVenta, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
    
    class Meta:
        db_table = 'tipo_venta'

class UsuarioVenta(models.Model):
    usuario_sistema_id = models.IntegerField()
    venta = models.ForeignKey('Venta')
    hora_salida = models.TimeField(blank=True, null=True)
    hora_entrega = models.TimeField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    
    def __init__(self, *args, **kwargs):
        super(UsuarioVenta, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(UsuarioVenta, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
    
    class Meta:
        db_table = 'usuario_venta'

class Venta(models.Model):
    tipo_venta = models.ForeignKey(TipoVenta)
    fecha = models.DateField(blank=True, null=True)
    personal = models.ForeignKey(Personal)
    nombre = models.CharField(max_length=255, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    nit = models.IntegerField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    empresa_id = models.IntegerField()
    usuario_creado = models.IntegerField()
    pagado = models.BooleanField(default=True)
    fecha_creado = models.DateTimeField(blank=True, null=True)
    usuario_modificado = models.IntegerField(blank=True, null=True)
    fecha_modificado = models.DateTimeField(blank=True, null=True)
    
    def __init__(self, *args, **kwargs):
        super(Venta, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(Venta, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
    
    class Meta:
        db_table = 'venta'

class VentaAtributo(models.Model):
    producto_atributo = models.ForeignKey(ProductoAtributo)
    venta_detalle = models.ForeignKey('VentaDetalle')
    estado = models.BooleanField(default=True)
    atributo_valor = models.ForeignKey(AtributoValor)
    
    def __init__(self, *args, **kwargs):
        super(VentaAtributo, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(VentaAtributo, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
    
    class Meta:
        db_table = 'venta_atributo'

class VentaDetalle(models.Model):
    venta = models.ForeignKey(Venta)
    producto = models.ForeignKey(Producto)
    cantidad = models.IntegerField(blank=True, null=True)
    precio = models.ForeignKey(Precio)
    estado = models.BooleanField(default=True)
    
    def __init__(self, *args, **kwargs):
        super(VentaDetalle, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(VentaDetalle, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])   
    
    class Meta:
        db_table = 'venta_detalle'

