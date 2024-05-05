def _check_with_backup_source(proxies):
    import requests
    try:
        response = requests.get("http://ip-api.com/json", proxies=proxies, timeout=4)
        data = response.json()
        if 'country' in data:
            return data['country']
        else:
            return None
    except:
        return None

def check_proxy(proxies):
    import requests
    if proxies is None:
        return "没有使用代理"
    proxies_https = proxies['https']
    try:
        response = requests.get("https://ipapi.co/json/", proxies=proxies, timeout=4)
        data = response.json()
        if 'country_name' in data:
            country = data['country_name']
            result = f"代理配置 {proxies_https}, 代理所在地：{country}"
        elif 'error' in data:
            alternative = _check_with_backup_source(proxies)
            if alternative is None:
                result = f"代理配置 {proxies_https}, 代理所在地：未知，IP查询频率受限"
            else:
                result = f"代理配置 {proxies_https}, 代理所在地：{alternative}"
        else:
            result = f"代理配置 {proxies_https}, 代理数据解析失败：{data}"
        return result
    except:
        result = f"代理配置 {proxies_https}, 代理所在地查询超时，代理可能无效"
        return result

if __name__ == "__main__":
    check_proxy(proxies=None)