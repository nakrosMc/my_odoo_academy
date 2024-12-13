from odoo import fields
from datetime import date

def migrate(cr, version):
    print('version')
    print('version')
    print('version')
    print(version)
    print('version')
    print('version')
    print('version')
    # Luego, cambiamos el tipo de la columna allocation_date a DATE (si aún no lo has hecho)
    cr.execute('ALTER TABLE hostel_student ADD COLUMN allocation_date DATE')
    
    # Seleccionamos todos los valores de la columna antigua (allocation_date_char)
    cr.execute('SELECT id, allocation_date_char FROM hostel_student')
    
    for record_id, old_date in cr.fetchall():
        new_date = None
        try:
            # Intentamos convertir la fecha en el formato estándar
            new_date = fields.Date.to_date(old_date)
        except ValueError:
            # Si la conversión falla y es un año solo, lo convertimos al primer día del año
            if len(old_date) == 4 and old_date.isdigit():
                new_date = date(int(old_date), 1, 1)

        if new_date:
            # Actualizamos la nueva columna allocation_date con el valor convertido
            cr.execute('UPDATE hostel_student SET allocation_date=%s WHERE id=%s', (new_date, record_id))
    
    # Finalmente, eliminamos la columna antigua (si es necesario)
    cr.execute('ALTER TABLE hostel_student DROP COLUMN allocation_date_char')


