# Home Assistant for Nature Remo

Home Assistant platform for Nature Remo.

In currently, It supports `switch` and `sensor` component only.


----


## Notice and Limitations

* This is UNOFFICIAL project for the convenience of users.

* This software has some limitations and is unstable, because it published under the testing phase.

    * I tested on Hass.io 0.89.2.

    * For now, this software can't control the Air Conditioners and the TVs.

* I don't any guarantee about this project.

* I don't have any relationship with the vendor company of the Nature Remo.


----


## Get Started

### 1. Get the access token of Nature Remo Cloud API

You can get the access token from here: http://home.nature.global/

### 2. Install the component to your Home Assistant

On Your Home Assistant server (Hass.io):
```
# cd /config

# wget https://github.com/mugifly/homeassistant-natureremo/archive/master.zip

# unzip master.zip
# rm master.zip

# cp -r homeassistant-natureremo/custom_components/ /config/
# rm -rf homeassistant-natureremo/
```

### 3. Make a configuration

In `configuration.yaml`:
```
switch:
  # Appliances via Nature Remo
  - platform: natureremo
    access_token: 'YOUR_ACCESS_TOKEN'

sensor:
  # Temperature and Humidity on Nature Remo
  - platform: natureremo
    access_token: 'YOUR_ACCESS_TOKEN'
```

### 4. Restart Home Assistant

After restarting, the appliances registered on Remo will be appeared on your Home Assistant.


----


## License and Thanks

```
The MIT License (MIT)
Copyright (c) 2019 Masanori Ohgita
```

And thank you to author of [pyture-remo](https://github.com/suzutan/pyture-remo).
