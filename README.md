<h1 align="center">Welcome to InstaDataMiner 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0 -- Prerelease-blue.svg?cacheSeconds=2592000" />
  <a href="#" target="_blank">
    <img alt="License: Apache 2.0" src="https://img.shields.io/badge/License-Apache 2.0-yellow.svg" />
  </a>
</p>

> Herramienta para obtener y analizar datos de Instagram. Permite extraer información de cuentas, seguidores, seguidos, calcular métricas como popularidad, ratio de influencia y belleza de perfiles, y gestionar proxies para las solicitudes.

## Install

```sh
pip install -r requirements.txt
```

## Usage

```sh
python3 instadataminer/main.py -h
```

## Proxy Management

# Get valid proxies

```sh
python3 instadataminer/main.py getproxies -i proxies-folder -o valid_proxies.txt -t 10
```

## Data Mining

# Clean data

```sh
python3 instadataminer/main.py miner -i input.csv -o output.csv cleandata
```

# Get genders

```sh
python3 instadataminer/main.py miner -i input.csv -o output.csv getgenders
```

# Calculate popularity

```sh
python3 instadataminer/main.py miner -i input.csv -o output.csv getpopularity
```

# Calculate follower/following ratio

```sh
python3 instadataminer/main.py miner -i input.csv -o output.csv getratio
```

# Calculate profile beauty

```sh
python3 instadataminer/main.py miner -i input.csv -o output.csv getbeauty --input-img-folder images/
```


## Get User Information

# Single user info

```sh
python3 instadataminer/main.py getuserinfo -d DEVICE_ID -u username
```

# Multiple users info

```sh
python3 instadataminer/main.py getusersinfo -d DEVICE_ID_1 DEVICE_ID_2 -i users_list.csv -o output.csv
```

# Get followers/following of a user

```sh
python3 instadataminer/main.py getusers -d DEVICE_ID --followers --following -o users.csv
```


## Author

👤 **Milenio**

* Website: www.htzone.netlify.app
* Github: [@yago\_milenio](https://github.com/yago\_milenio)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_