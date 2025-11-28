import argparse

def main():
    parser = argparse.ArgumentParser(
        description="CLI para InstaDataMiner: obtener datos de Instagram, exportarlos y calcular métricas."
    )
    
    subparsers = parser.add_subparsers(dest="option", required=True)

    proxy_cmd = subparsers.add_parser("getproxies", help="Obtencion de proxies")
    proxy_cmd.add_argument("-o", "--output-file", help="Fichero de salida con los proxies validos")
    proxy_cmd.add_argument("-i", "--input-folder", help="Fichero de entrada con carpeta donde estan los listados de proxies; se admiten los formatos http:ip:port, socks4:ip:port y socks5:ip:port en los ficheros que estén dentro de dicha carpeta especificada")
    proxy_cmd.add_argument("-t", "--threads", type=int, help="Numero de hilos")

    miner_cmd = subparsers.add_parser("miner", help="Funciones de minado de datos")
    miner_cmd.add_argument("-i", "--input-file", help="Fichero csv de la base de datos")
    miner_cmd.add_argument("-o", "--output-file", help="Fichero csv de la base de datos resultante")
    subparsers_miner = miner_cmd.add_subparsers(dest="miner_function", required=True)
    clean_cmd = subparsers_miner.add_parser("cleandata", help="Añade columnas limpias como name y description quitando los emojis y signos raros [name_c, descripcion_c]")
    gender_cmd = subparsers_miner.add_parser("getgenders", help="Obtiene generos basandose en el nombre de usuario")
    popularidad_cmd = subparsers_miner.add_parser("getpopularity", help="Obtiene la popularidad de una persona basandose en los seguidores, seguidos y los posts")
    ratio_cmd = subparsers_miner.add_parser("getratio", help="Obtiene el ratio de un perfil (seguidores/seguidos)")
    belleza_cmd = subparsers_miner.add_parser("getbeauty", help="Obtiene la belleza de cada cuenta basandose en la foto de perfil")
    belleza_cmd.add_argument("--input-img-folder", help="Directorio de origen de las fotos de perfiles")

    get_user_info_cmd=subparsers.add_parser("getuserinfo", help="Obtiene la informacion de un usuario")
    get_user_info_cmd.add_argument("-d", "--device", required=True, help="Dispositivo adb")
    get_user_info_cmd.add_argument("-u", "--user", help="Usuario del cual se quiere obtener la informacion")

    get_users_info_cmd=subparsers.add_parser("getusersinfo", help="Obtiene la informacion de una lista de usuarios")
    get_users_info_cmd.add_argument("-d", "--device", nargs="+", required=True, help="Dispositivo adb")    #lista separa por espacios
    get_users_info_cmd.add_argument("--emulator", action="store_true", help="Indica que los dispositivos son emuladores y no despositivos fisicos via usb")
    get_users_info_cmd.add_argument("-i", "--input-file", help="Fichero con listado de ususarios (usernames)")
    get_users_info_cmd.add_argument("-o", "--output-file", help="Fichero de salida de usuarios ya procesados")
    get_users_info_cmd.add_argument("-la", "--last-output-file", help="Ultimo fichero de salida para poder seguir la ejecución desde ese punto")
    get_users_info_cmd.add_argument("--output-folder", help="Carpeta destinataria donde se guardaran las fotos de perfil")

    get_users_from_user=subparsers.add_parser("getusers", help="Obtiene el listado de seguidos o seguidores de un usuario")
    get_users_from_user.add_argument("-d", "--device", required=True, help="Dispositivo adb")
    get_users_from_user.add_argument("--emulator", action="store_true", help="Indica que los dispositivos son emuladores y no despositivos fisicos via usb")
    get_users_from_user.add_argument("-o", "--output-file", help="Fichero de salida de usuarios ya procesados")
    get_users_from_user.add_argument("--followers", action="store_true", help="Exportar solo los seguidores")
    get_users_from_user.add_argument("--following", action="store_true", help="Exportar solo los seguidos")

    


    options=["option", "miner_function"]
    args = parser.parse_args()

    func_args = {k: v for k, v in vars(args).items() if v is not None and k not in options}


    if args.option == "getproxies":
        from proxy import test_proxies

        test_proxies.main(**func_args)

    if args.option == "miner":

        from miner.limpiar_datos import clean
        from miner.procesar_datos import miner

        if args.miner_function == "cleandata":
            clean(**func_args)
        if args.miner_function == "getgenders":
            m = miner(**func_args)
            m.calcular_genero_from_file()
            m.save_to_csv()
        if args.miner_function == "getpopularity":
            m = miner(**func_args)
            m.calcular_popularidad()
            m.save_to_csv()
        if args.miner_function == "getratio":
            m = miner(**func_args)
            m.calcular_influencia()
            m.save_to_csv()
        if args.miner_function == "getbeauty":
            init_args = {k: v for k, v in func_args.items() if k in ["input_file", "output_file"]}
            m = miner(**init_args)
            beauty_args = {k: v for k, v in func_args.items() if k not in ["input_file", "output_file"]}
            m.calcular_belleza(**beauty_args)
            m.save_to_csv()
    
    if args.option == "getusers":
        from dataReader import user_info, export_data

        if not func_args['following'] and not func_args["followers"]:
            parser.error("Debes usar --followers, --following o ambos.")
        else:
            export_data.main(**func_args)
    
    if args.option == "getuserinfo":
        from dataReader import user_info, export_data

        print(user_info.get_user_info(**func_args))

    if args.option == "getusersinfo":
        from dataReader import user_info, export_data

        user_info.get_users_info(**func_args)





if __name__ == "__main__":
    main()

