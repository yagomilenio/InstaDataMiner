import argparse
import dataReader 
import miner 
from proxy import test_proxies

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
    subparsers_miner = miner_cmd.add_subparsers(dest="funcion", required=True)
    clean_cmd = subparsers_miner.add_parser("cleandata", help="Añade columnas limpias como name y description quitando los emojis y signos raros [name_c, descripcion_c]")
    gender_cmd = subparsers_miner.add_parser("getgenders", help="Obtiene generos basandose en el nombre de usuario")
    popularidad_cmd = subparsers_miner.add_parser("getpopularity", help="Obtiene la popularidad de una persona basandose en los seguidores, seguidos y los posts")
    ratio_cmd = subparsers_miner.add_parser("getratio", help="Obtiene el ratio de un perfil (seguidores/seguidos)")
    belleza_cmd = subparsers_miner.add_parser("getbeauty", help="Obtiene la belleza de cada cuenta basandose en la foto de perfil")
    belleza_cmd.add_argument("--input-img-folder", help="Directorio de origen de las fotos de perfiles")


    options=["option", "cleandata", "getgenders"]
    args = parser.parse_args()

    func_args = {k: v for k, v in vars(args).items() if v is not None and k not in options}


    if args.option == "getproxies":
        test_proxies.main(**func_args)

    if args.option == "miner":
        if args.option.miner == "cleandata":
            miner.limpiar_datos.clean(**func_args)
        if args.option.miner == "getgenders":
            miner.procesar_datos.calcular_genero_from_file(**func_args)
        if args.option.miner == "getpopularity":
            miner.procesar_datos.calcular_popularidad(**func_args)
        if args.option.miner == "getratio":
            miner.procesar_datos.calcular_influencia(**func_args)
        if args.option.miner == "getbeauty":
            miner.procesar_datos.calcular_belleza(**func_args)




if __name__ == "__main__":
    main()

