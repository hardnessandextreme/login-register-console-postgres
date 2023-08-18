import logging as log

log.basicConfig(level=log.DEBUG,
                format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
                datefmt='%I:%M:%S %p',
                encoding='utf8',
                handlers=[
                    log.FileHandler('registros/registros_app.log'),
                    # log.StreamHandler()
                ])

if __name__ == '__main__':
    log.debug('Mensaje a nivel Debug.')  # No se mostrará en la consola, solo se guardará en el archivo
    log.info('Mensaje a nivel de info')
    log.warning('Mensaje a nivel warning')
    log.error('Mensaje a nivel error')
    log.critical('Mensaje a nivel critical')
