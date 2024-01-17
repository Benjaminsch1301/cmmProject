
api_url_paranal = "http://archive.eso.org/wdb/wdb/asm/meteo_paranal/query"

payload_paranal = {
            "wdbo": "csv/download",
            "max_rows_returned": "99999999999999999999999999999",
            "start_date": "",
            "integration": "",
            "tab_press": "on",
            "press": "",
            "tab_presqnh": "on",
            "presqnh": "",
            "tab_temp1": "on",
            "temp1": "",
            "tab_temp2": "on",
            "temp2": "",
            "tab_temp3": "on",
            "temp3": "",
            "tab_temp4": "on",
            "temp4": "",
            "tab_tempdew1": "on",
            "tempdew1": "",
            "tab_tempdew2": "on",
            "tempdew2": "",
            "tab_tempdew4": "on",
            "tempdew4": "",
            "tab_dustl1": "on",
            "dustl1": "",
            "tab_dustl2": "on",
            "dustl2": "",
            "tab_dusts1": "on",
            "dusts1": "",
            "tab_dusts2": "on",
            "dusts2": "",
            "tab_rain": "on",
            "rain": "",
            "tab_rhum1": "on",
            "rhum1": "",
            "tab_rhum2": "on",
            "rhum2": "",
            "tab_rhum4": "on",
            "rhum4": "",
            "tab_wind_dir1": "on",
            "wind_dir1": "",
            "tab_wind_dir1_180": "on",
            "wind_dir1_180": "",
            "tab_wind_dir2": "on",
            "wind_dir2": "",
            "tab_wind_dir2_180": "on",
            "wind_dir2_180": "",
            "tab_wind_speed1": "on",
            "wind_speed1": "",
            "tab_wind_speed2": "on",
            "wind_speed2": "",
            "tab_wind_speedu": "on",
            "wind_speedu": "",
            "tab_wind_speedv": "on",
            "wind_speedv": "",
            "tab_wind_speedw": "on",
            "wind_speedw": "", # modificated from here
            'tab_prestrend': '',
            'prestrend': '',
            'tab_press_inst': 'on',
            'press_inst': '',
            'tab_press_max': '',
            'press_max': '',
            'tab_press_min': '',
            'press_min': '',
            'tab_press_dev': '',
            'press_dev': '',
            'tab_presqnh_inst': '', # *
            'presqnh_inst': '',
            'tab_presqnh_max': '',
            'presqnh_max': '',
            'tab_presqnh_min': '',
            'presqnh_min': '',
            'tab_presqnh_dev': '',
            'presqnh_dev': '',
            'tab_temp1_inst': 'on',
            'temp1_inst': '',
            'tab_temp1_max': '',
            'temp1_max': '',
            'tab_temp1_min': '',
            'temp1_min': '',
            'tab_temp1_dev': '',
            'temp1_dev': '',
            'tab_temp2_inst': 'on',
            'temp2_inst': '',
            'tab_temp2_max': '',
            'temp2_max': '',
            'tab_temp2_min': '',
            'temp2_min': '',
            'tab_temp2_dev': '',
            'temp2_dev': '',
            'tab_temp3_inst': 'on',
            'temp3_inst': '',
            'tab_temp3_max': '',
            'temp3_max': '',
            'tab_temp3_min': '',
            'temp3_min': '',
            'tab_temp3_dev': '',
            'temp3_dev': '',
            'tab_temp4_inst': 'on',
            'temp4_inst': '',
            'tab_temp4_max': '',
            'temp4_max': '',
            'tab_temp4_min': '',
            'temp4_min': '',
            'tab_temp4_dev': '',
            'temp4_dev': '',
            'tab_tempdew1_inst': 'on',
            'tempdew1_inst': '',
            'tab_tempdew1_max': '',
            'tempdew1_max': '',
            'tab_tempdew1_min': '',
            'tempdew1_min': '',
            'tab_tempdew1_dev': '',
            'tempdew1_dev': '',
            'tab_tempdew2_inst': 'on',
            'tempdew2_inst': '',
            'tab_tempdew2_max': '',
            'tempdew2_max': '',
            'tab_tempdew2_min': '',
            'tempdew2_min': '',
            'tab_tempdew2_dev': '',
            'tempdew2_dev': '',
            'tab_tempdew4_inst': 'on',
            'tempdew4_inst': '',
            'tab_tempdew4_max': '',
            'tempdew4_max': '',
            'tab_tempdew4_min': '',
            'tempdew4_min': '',
            'tab_tempdew4_dev': '',
            'tempdew4_dev': '',
            'tab_rhum1_inst': 'on',
            'rhum1_inst': '',
            'tab_rhum1_max': '',
            'rhum1_max': '',
            'tab_rhum1_min': '',
            'rhum1_min': '',
            'tab_rhum1_dev': '',
            'rhum1_dev': '',
            'tab_rhum2_inst': 'on',
            'rhum2_inst': '',
            'tab_rhum2_max': '',
            'rhum2_max': '',
            'tab_rhum2_min': '',
            'rhum2_min': '',
            'tab_rhum2_dev': '',
            'rhum2_dev': '',
            'tab_rhum4_inst': 'on',
            'rhum4_inst': '',
            'tab_rhum4_max': '',
            'rhum4_max': '',
            'tab_rhum4_min': '',
            'rhum4_min': '',
            'tab_rhum4_dev': '',
            'rhum4_dev': '',
            'tab_dustl1_inst': 'on',
            'dustl1_inst': '',
            'tab_dustl1_max': '',
            'dustl1_max': '',
            'tab_dustl1_min': '',
            'dustl1_min': '',
            'tab_dustl1_dev': '',
            'dustl1_dev': '',
            'tab_dustl2_inst': 'on',
            'dustl2_inst': '',
            'tab_dustl2_max': '',
            'dustl2_max': '',
            'tab_dustl2_min': '',
            'dustl2_min': '',
            'tab_dustl2_dev': '',
            'dustl2_dev': '',
            'tab_dusts1_inst': 'on',
            'dusts1_inst': '',
            'tab_dusts1_max': '',
            'dusts1_max': '',
            'tab_dusts1_min': '',
            'dusts1_min': '',
            'tab_dusts1_dev': '',
            'dusts1_dev': '',
            'tab_dusts2_inst': 'on',
            'dusts2_inst': '',
            'tab_dusts2_max': '',
            'dusts2_max': '',
            'tab_dusts2_min': '',
            'dusts2_min': '',
            'tab_dusts2_dev': '',
            'dusts2_dev': '',
            'tab_rain_inst': 'on',
            'rain_inst': '',
            'tab_rain_max': '',
            'rain_max': '',
            'tab_rain_min': '',
            'rain_min': '',
            'tab_rain_dev': '',
            'rain_dev': '',
            'tab_wind_dir1_inst': 'on',
            'wind_dir1_inst': '',
            'tab_wind_dir1_min': '',
            'wind_dir1_min': '',
            'tab_wind_dir1_max': '',
            'wind_dir1_max': '',
            'tab_wind_dir1_dev': '',
            'wind_dir1_dev': '',
            'tab_wind_dir2_inst': 'on',
            'wind_dir2_inst': '',
            'tab_wind_dir2_min': '',
            'wind_dir2_min': '',
            'tab_wind_dir2_max': '',
            'wind_dir2_max': '',
            'tab_wind_dir2_dev': '',
            'wind_dir2_dev': '',
            'tab_wind_speed1_inst': 'on',
            'wind_speed1_inst': '',
            'tab_wind_speed1_min': '',
            'wind_speed1_min': '',
            'tab_wind_speed1_max': '',
            'wind_speed1_max': '',
            'tab_wind_speed1_dev': '',
            'wind_speed1_dev': '',
            'tab_wind_speed2_inst': 'on',
            'wind_speed2_inst': '',
            'tab_wind_speed2_min': '',
            'wind_speed2_min': '',
            'tab_wind_speed2_max': '',
            'wind_speed2_max': '',
            'tab_wind_speed2_dev': '',
            'wind_speed2_dev': '',
            'tab_wind_speedu_inst': 'on',
            'wind_speedu_inst': '',
            'tab_wind_speedu_min': '',
            'wind_speedu_min': '',
            'tab_wind_speedu_max': '',
            'wind_speedu_max': '',
            'tab_wind_speedu_dev': '',
            'wind_speedu_dev': '',
            'tab_wind_speedv_inst': 'on',
            'wind_speedv_inst': '',
            'tab_wind_speedv_min': '',
            'wind_speedv_min': '',
            'tab_wind_speedv_max': '',
            'wind_speedv_max': '',
            'tab_wind_speedv_dev': '',
            'wind_speedv_dev': '',
            'tab_wind_speedw_inst': 'on',
            'wind_speedw_inst': '',
            'tab_wind_speedw_min': '',
            'wind_speedw_min': '',
            'tab_wind_speedw_max': '',
            'wind_speedw_max': '',
            'tab_wind_speedw_dev': '',
            'wind_speedw_dev': '' , # end
            "order": "start_date"
        }
        
payload_lasierra = {}