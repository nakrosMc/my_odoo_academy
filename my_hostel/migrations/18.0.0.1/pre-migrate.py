def migrate(cr, version):
    print('PREMIGRATE')
    print(version)
    print(version)
    print(version)
    print(version)
    print(version)
    print('PREMIGRATE')
    # Primero, renombramos la columna antigua
    cr.execute('ALTER TABLE hostel_student RENAME COLUMN allocation_date TO allocation_date_char')
    